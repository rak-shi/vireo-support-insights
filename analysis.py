
from pathlib import Path

import pandas as pd

# ============================================================
# CONFIGURATION
# ============================================================

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"

BLENDED_COST_INR = 290

CHANNEL_COSTS = {
    "chat": 210,
    "email": 260,
    "voice": 520,
    "social": 240,
}

SLA_MINUTES = {
    "chat": 15,
    "voice": 120,
    "social": 240,
    "email": 480,
}


# ============================================================
# LOAD INPUT FILES
# ============================================================

def load_data():
    required = [
        "tickets.csv",
        "agents.csv",
        "customers.csv",
        "orders.csv",
        "products.csv",
    ]

    for filename in required:
        if not (DATA / filename).exists():
            raise FileNotFoundError(
                f"Missing required file: data/{filename}"
            )

    tickets = pd.read_csv(
        DATA / "tickets.csv",
        dtype={
            "ticket_id": "string",
            "customer_id": "string",
            "agent_id": "string",
            "order_id": "string",
            "product_sku": "string",
        },
    )

    agents = pd.read_csv(
        DATA / "agents.csv",
        dtype={"agent_id": "string"},
    )

    customers = pd.read_csv(DATA / "customers.csv")
    orders = pd.read_csv(DATA / "orders.csv")
    products = pd.read_csv(DATA / "products.csv")

    # Ensure expected optional columns exist.
    defaults = {
        "customer_message": "",
        "agent_notes": "",
        "category": "Unknown",
        "channel": "Unknown",
        "assigned_team": "Unknown",
        "status": "Unknown",
        "customer_id": pd.NA,
        "product_sku": pd.NA,
        "agent_id": pd.NA,
        "ticket_id": pd.NA,
        "csat_score": pd.NA,
        "transfers": pd.NA,
        "refund_amount_inr": pd.NA,
    }

    for column, default in defaults.items():
        if column not in tickets.columns:
            tickets[column] = default

    for column in [
        "created_at",
        "first_response_at",
        "resolved_at",
    ]:
        if column not in tickets.columns:
            tickets[column] = pd.NaT

        tickets[column] = pd.to_datetime(
            tickets[column],
            errors="coerce",
        )

    for column in [
        "csat_score",
        "transfers",
        "refund_amount_inr",
    ]:
        tickets[column] = pd.to_numeric(
            tickets[column],
            errors="coerce",
        )

    # Legacy CSAT zero means no response.
    tickets.loc[
        tickets["csat_score"] == 0,
        "csat_score",
    ] = float("nan")

    # Prepare agent roster fields.
    for column in [
        "agent_id",
        "name",
        "team",
        "tier",
        "from_date",
        "to_date",
    ]:
        if column not in agents.columns:
            agents[column] = pd.NA

    agents["agent_id"] = agents["agent_id"].astype("string")

    agents["from_date"] = pd.to_datetime(
        agents["from_date"],
        errors="coerce",
    )

    agents["to_date"] = pd.to_datetime(
        agents["to_date"],
        errors="coerce",
    )

    return tickets, agents, customers, orders, products


# ============================================================
# COMPLAINT THEME CLASSIFICATION
# ============================================================

def classify_complaint(row):
    """Simple keyword-based complaint classification."""

    message = str(row.get("customer_message", "") or "").lower()
    notes = str(row.get("agent_notes", "") or "").lower()
    category = str(row.get("category", "") or "").lower()

    text = f"{message} {notes} {category}"

    rules = [
        (
            "Delivery / tracking",
            [
                "delivery", "delayed", "late delivery",
                "tracking", "courier", "shipment",
                "not arrived", "not delivered", "lost parcel",
            ],
        ),
        (
            "Refund / payment",
            [
                "refund", "payment", "charged", "billing",
                "transaction", "money back", "invoice",
            ],
        ),
        (
            "Product defect / warranty",
            [
                "defect", "faulty", "broken", "not working",
                "warranty", "repair", "replacement",
                "damaged", "malfunction", "rma",
            ],
        ),
        (
            "Return / exchange",
            [
                "return", "exchange", "wrong product",
                "wrong item", "swap",
            ],
        ),
        (
            "Audio / connectivity",
            [
                "bluetooth", "pairing", "connectivity",
                "sound", "audio", "noise", "volume",
                "headphone", "earbud", "speaker",
            ],
        ),
        (
            "Order / product information",
            [
                "order status", "availability", "specification",
                "product information", "how to use",
            ],
        ),
        (
            "Customer service",
            [
                "agent", "support", "no response",
                "called again", "repeat", "colleague",
                "already told",
            ],
        ),
    ]

    for theme, keywords in rules:
        if any(keyword in text for keyword in keywords):
            return theme

    if not message.strip() and not notes.strip():
        return "Unclear / no text"

    return "Other / review"


# ============================================================
# PREPARE TICKETS
# ============================================================

def prepare_tickets(tickets):
    df = tickets.copy()

    # Do not automatically collapse repeated ticket IDs.
    # Only remove rows identical across every column.
    original_rows = len(df)
    df = df.drop_duplicates().copy()

    exact_duplicates_removed = original_rows - len(df)

    df["channel_normalized"] = (
        df["channel"]
        .astype("string")
        .str.lower()
        .str.strip()
    )

    df["created_week"] = (
        df["created_at"]
        .dt.to_period("W-SUN")
        .dt.start_time
    )

    df["is_completed"] = (
        df["status"]
        .astype("string")
        .str.lower()
        .isin(["resolved", "closed"])
    )

    df["contact_cost_inr"] = (
        df["channel_normalized"].map(CHANNEL_COSTS)
    )

    df["sla_target_minutes"] = (
        df["channel_normalized"].map(SLA_MINUTES)
    )

    df["response_minutes"] = (
        df["first_response_at"] - df["created_at"]
    ).dt.total_seconds() / 60

    df["sla_breach"] = (
        df["response_minutes"].notna()
        & df["sla_target_minutes"].notna()
        & (df["response_minutes"] > df["sla_target_minutes"])
    )

    df["duplicate_ticket_id"] = (
        df["ticket_id"].duplicated(keep=False)
    )

    df["complaint_theme"] = df.apply(
        classify_complaint,
        axis=1,
    )

    # Columns consumed by the dashboard.
    df["repeat_contact_proxy"] = False
    df["repeat_of_ticket_id"] = pd.NA

    df.attrs["exact_duplicates_removed"] = exact_duplicates_removed

    return df


# ============================================================
# ADD AGENT ROSTER INFORMATION
# ============================================================

def add_agent_information(df, agents):
    result = df.copy()

    roster = agents.copy()

    # A stable one-row-per-agent lookup prevents row multiplication.
    roster = roster.drop_duplicates(
        subset=["agent_id"],
        keep="last",
    )

    roster = roster.rename(
        columns={
            "name": "agent_name",
            "team": "roster_team",
            "tier": "agent_tier",
        }
    )

    roster_columns = [
        column
        for column in [
            "agent_id",
            "agent_name",
            "roster_team",
            "agent_tier",
            "site",
            "shift",
            "from_date",
            "to_date",
        ]
        if column in roster.columns
    ]

    roster = roster[roster_columns]

    result["agent_id"] = result["agent_id"].astype("string")

    result = result.merge(
        roster,
        on="agent_id",
        how="left",
        validate="many_to_one",
    )

    if "agent_name" not in result.columns:
        result["agent_name"] = pd.NA

    if "roster_team" not in result.columns:
        result["roster_team"] = pd.NA

    if "agent_tier" not in result.columns:
        result["agent_tier"] = pd.NA

    return result


# ============================================================
# REPEAT-CONTACT REVIEW QUEUE
# ============================================================

def flag_repeat_contacts(df):
    """
    Flag candidate repeat contacts.

    Candidate rule:
    same customer + product SKU + category,
    created within 30 days after a previous ticket's resolution.

    This is a proxy, not proof that the underlying issue is identical.
    """

    result = df.copy()

    result["repeat_contact_proxy"] = False
    result["repeat_of_ticket_id"] = pd.NA

    required = [
        "customer_id",
        "product_sku",
        "category",
        "created_at",
        "resolved_at",
        "ticket_id",
    ]

    if any(column not in result.columns for column in required):
        return result

    valid = result[
        result["customer_id"].notna()
        & result["product_sku"].notna()
        & result["category"].notna()
        & result["created_at"].notna()
    ].copy()

    valid = valid.sort_values(
        ["created_at", "ticket_id"]
    )

    for idx, row in valid.iterrows():
        candidates = valid[
            (valid["customer_id"] == row["customer_id"])
            & (valid["product_sku"] == row["product_sku"])
            & (valid["category"] == row["category"])
            & (valid["resolved_at"].notna())
            & (valid["resolved_at"] < row["created_at"])
            & (
                valid["resolved_at"]
                >= row["created_at"] - pd.Timedelta(days=30)
            )
            & (valid["ticket_id"] != row["ticket_id"])
        ]

        if candidates.empty:
            continue

        # Use the most recent earlier resolution.
        previous = candidates.sort_values(
            "resolved_at"
        ).iloc[-1]

        result.at[idx, "repeat_contact_proxy"] = True
        result.at[idx, "repeat_of_ticket_id"] = previous["ticket_id"]

    return result


# ============================================================
# DATA QUALITY SUMMARY
# ============================================================

def get_data_quality_summary(df):
    return {
        "rows": int(len(df)),
        "distinct_ticket_ids": int(df["ticket_id"].nunique()),
        "rows_with_repeated_ids": int(
            df["duplicate_ticket_id"].sum()
        ),
        "distinct_repeated_ticket_ids": int(
            df.loc[
                df["duplicate_ticket_id"],
                "ticket_id",
            ].nunique()
        ),
        "completed_tickets": int(df["is_completed"].sum()),
        "sla_breaches": int(df["sla_breach"].sum()),
        "missing_customer_messages": int(
            df["customer_message"].isna().sum()
        ),
        "missing_resolution_dates": int(
            df["resolved_at"].isna().sum()
        ),
        "repeat_contact_proxy_flags": int(
            df["repeat_contact_proxy"].sum()
        ),
        "exact_duplicate_rows_removed": int(
            df.attrs.get("exact_duplicates_removed", 0)
        ),
        "date_start": str(df["created_at"].min()),
        "date_end": str(df["created_at"].max()),
    }


# ============================================================
# MAIN FUNCTION USED BY APP.PY
# ============================================================

def build_all():
    """
    Load and prepare data for the Streamlit dashboard.

    Returns:
        df: Prepared ticket data with dashboard fields.
        summary: Data-quality summary dictionary.
    """

    tickets, agents, customers, orders, products = load_data()

    df = prepare_tickets(tickets)

    df = add_agent_information(df, agents)

    df = flag_repeat_contacts(df)

    summary = get_data_quality_summary(df)

    return df, summary


# ============================================================
# COMMAND-LINE CHECK
# ============================================================

if __name__ == "__main__":
    df, summary = build_all()

    print("\nVIREO SUPPORT DATA QUALITY SUMMARY")
    print("=" * 45)

    for key, value in summary.items():
        print(f"{key}: {value}")

    print("\nTICKETS BY CHANNEL")
    print(df["channel"].value_counts(dropna=False))

    print("\nTICKETS BY STATUS")
    print(df["status"].value_counts(dropna=False))

    print("\nTICKETS BY TEAM")
    print(df["assigned_team"].value_counts(dropna=False))

    print("\nAGENT ROSTER MATCH")
    print(
        f"Rows without a matched agent name: "
        f"{df['agent_name'].isna().sum():,}"
    )
