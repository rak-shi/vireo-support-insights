
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from analysis import BLENDED_COST_INR, build_all

# ============================================================
# PAGE CONFIGURATION
# ============================================================

ROOT = Path(__file__).resolve().parent

st.set_page_config(
    page_title="Vireo Audio | Support Insights",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# CUSTOM UI THEME
# ============================================================

st.markdown(
    """
    <style>
    /* Main application background */
    .stApp {
        background: linear-gradient(
            135deg,
            #0B1020 0%,
            #101827 55%,
            #102A32 100%
        );
        color: #F1F5F9;
    }

    /* Main content spacing */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #172554 0%,
            #151C30 55%,
            #111827 100%
        );
        border-right: 1px solid #334155;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #5EEAD4 !important;
    }

    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p {
        color: #E2E8F0 !important;
    }

    /* Main headings */
    h1 {
        color: #F8FAFC !important;
        font-weight: 800 !important;
        letter-spacing: -1px;
    }

    h2, h3 {
        color: #5EEAD4 !important;
        font-weight: 700 !important;
    }

    /* Body text */
    p, li, label {
        color: #E2E8F0;
    }

    /* KPI cards */
    [data-testid="stMetric"] {
        background: linear-gradient(
            135deg,
            rgba(45, 212, 191, 0.13),
            rgba(99, 102, 241, 0.15)
        );
        border: 1px solid rgba(94, 234, 212, 0.30);
        border-radius: 16px;
        padding: 18px 20px;
        min-height: 125px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.16);
    }

    [data-testid="stMetricLabel"] {
        color: #CBD5E1 !important;
        font-size: 0.92rem !important;
    }

    [data-testid="stMetricValue"] {
        color: #5EEAD4 !important;
        font-weight: 800 !important;
    }

    [data-testid="stMetricDelta"] {
        color: #A5B4FC !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 1px solid #334155;
    }

    .stTabs [data-baseweb="tab"] {
        background: rgba(30, 41, 59, 0.75);
        color: #CBD5E1;
        border-radius: 10px 10px 0 0;
        padding: 12px 18px;
    }

    .stTabs [aria-selected="true"] {
        background: rgba(45, 212, 191, 0.15) !important;
        color: #5EEAD4 !important;
        border-bottom: 3px solid #2DD4BF !important;
    }

    /* Buttons */
    .stButton > button,
    .stDownloadButton > button {
        background: linear-gradient(
            90deg,
            #0D9488,
            #6366F1
        );
        color: #FFFFFF;
        border: 1px solid rgba(94, 234, 212, 0.35);
        border-radius: 10px;
        font-weight: 650;
        transition: all 0.2s ease;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {
        background: linear-gradient(
            90deg,
            #14B8A6,
            #8B5CF6
        );
        color: #FFFFFF;
        border-color: #5EEAD4;
    }

    /* Select boxes and dropdowns */
    [data-testid="stSelectbox"] > div > div,
    [data-testid="stNumberInput"] input {
        background-color: #1E293B;
        border-radius: 10px;
    }

    /* Data tables */
    [data-testid="stDataFrame"],
    [data-testid="stTable"] {
        border: 1px solid #334155;
        border-radius: 12px;
        overflow: hidden;
    }

    /* Expanders */
    [data-testid="stExpander"] {
        border: 1px solid #334155;
        border-radius: 12px;
        background: rgba(15, 23, 42, 0.65);
    }

    /* Alerts */
    [data-testid="stAlert"] {
        border-radius: 12px;
        border: 1px solid #334155;
    }

    /* Dividers */
    hr {
        border-color: #334155 !important;
    }

    /* Captions */
    [data-testid="stCaptionContainer"] {
        color: #94A3B8 !important;
    }

    /* Slider accent */
    [data-testid="stSlider"] {
        color: #5EEAD4;
    }

    /* Links */
    a {
        color: #5EEAD4 !important;
    }

    /* Download buttons full width where appropriate */
    .stDownloadButton {
        margin-top: 8px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# CHART THEME
# ============================================================

BG_COLOR = "#111827"
TEXT_COLOR = "#E2E8F0"
GRID_COLOR = "#334155"
TEAL = "#2DD4BF"
INDIGO = "#818CF8"
VIOLET = "#A78BFA"


def style_chart(fig, ax, grid_axis="y"):
    """Apply the dashboard's dark chart styling."""
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)

    ax.tick_params(axis="both", colors=TEXT_COLOR, labelsize=9)

    ax.xaxis.label.set_color(TEXT_COLOR)
    ax.yaxis.label.set_color(TEXT_COLOR)
    ax.title.set_color("#F8FAFC")

    for spine in ax.spines.values():
        spine.set_color("#475569")

    ax.grid(
        axis=grid_axis,
        color=GRID_COLOR,
        linestyle="-",
        linewidth=0.7,
        alpha=0.8,
    )

    ax.set_axisbelow(True)
    fig.tight_layout()


def show_empty_message(message):
    st.info(message)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data(show_spinner="Preparing support data...")
def get_analysis():
    return build_all()


try:
    df, summary = get_analysis()
except Exception as exc:
    st.error("The dashboard could not load the input data.")
    st.markdown(
        """
        Check that these files are inside your project's `data` folder:

        - `tickets.csv`
        - `agents.csv`
        - `customers.csv`
        - `orders.csv`
        - `products.csv`
        """
    )
    st.exception(exc)
    st.stop()

if df.empty:
    st.error("No ticket records were found.")
    st.stop()

# ============================================================
# HEADER
# ============================================================

st.title("🎧 Vireo Audio Support Insights")

st.markdown(
    """
    <p style="
        color:#94A3B8;
        font-size:1.05rem;
        margin-top:-8px;
        margin-bottom:24px;
    ">
        Weekly support intelligence · SLA monitoring ·
        Customer experience · Team workload
    </p>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# SIDEBAR FILTERS
# ============================================================

with st.sidebar:
    st.markdown("## 🎛️ Dashboard filters")

    valid_dates = df["created_at"].dropna()

    if valid_dates.empty:
        st.error("No valid ticket creation dates were found.")
        st.stop()

    week_starts = sorted(
        valid_dates.dt.to_period("W-SUN")
        .dt.start_time.dropna()
        .unique()
    )

    selected_week = st.selectbox(
        "Week starting",
        options=week_starts,
        index=len(week_starts) - 1,
        format_func=lambda value: pd.Timestamp(value).strftime(
            "%d %b %Y"
        ),
    )

    teams = sorted(
        df["assigned_team"]
        .dropna()
        .astype(str)
        .unique()
    ) if "assigned_team" in df.columns else []

    selected_team = st.selectbox(
        "Assigned team",
        options=["All teams"] + teams,
        index=0,
    )

    st.divider()

    st.markdown("### 📌 Policy reminders")
    st.caption("Blended contact cost: ₹290 per contact.")
    st.caption(
        "SLA targets: chat 15 min, voice 2 hr, "
        "social 4 hr, email 8 hr."
    )
    st.caption(
        "Tier 2 / warranty work should be assessed by "
        "resolution time, not weekly closure volume."
    )

    st.divider()
    st.caption("Timestamps are interpreted as exported in IST.")

# ============================================================
# WEEK AND TEAM FILTERING
# ============================================================

week_start = pd.Timestamp(selected_week)
week_end = week_start + pd.Timedelta(days=7)

all_df = df.copy()

if selected_team != "All teams":
    all_df = all_df[
        all_df["assigned_team"].astype(str) == selected_team
    ].copy()

current = all_df[
    (all_df["created_at"] >= week_start)
    & (all_df["created_at"] < week_end)
].copy()

previous = all_df[
    (all_df["created_at"] >= week_start - pd.Timedelta(days=7))
    & (all_df["created_at"] < week_start)
].copy()

completed_mask = (
    all_df["status"].astype(str).str.lower().isin(
        ["resolved", "closed"]
    )
)

closed_current = all_df[
    (all_df["resolved_at"] >= week_start)
    & (all_df["resolved_at"] < week_end)
    & completed_mask
].copy()

# ============================================================
# KPI CALCULATIONS
# ============================================================

tickets_received = len(current)
tickets_completed = len(closed_current)

evaluable_sla = current[
    current["first_response_at"].notna()
    & current["created_at"].notna()
    & current["sla_target_minutes"].notna()
]

sla_breaches = int(
    current["sla_breach"].fillna(False).sum()
)

sla_breach_rate = (
    sla_breaches / len(evaluable_sla) * 100
    if len(evaluable_sla) > 0
    else 0
)

contact_cost = current["contact_cost_inr"].sum(
    min_count=1
)

if pd.isna(contact_cost):
    contact_cost = 0

previous_received = len(previous)
volume_delta = tickets_received - previous_received

repeat_flags_week = int(
    current["repeat_contact_proxy"].fillna(False).sum()
)

# ============================================================
# KPI DISPLAY
# ============================================================

st.markdown("## ✨ Weekly overview")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Tickets received",
    f"{tickets_received:,}",
    delta=f"{volume_delta:+,} vs previous week",
)

c2.metric(
    "Resolved / closed",
    f"{tickets_completed:,}",
    help="Tickets whose resolution timestamp falls within this week.",
)

c3.metric(
    "SLA breach rate",
    f"{sla_breach_rate:.1f}%",
    help=(
        f"{sla_breaches:,} breaches among "
        f"{len(evaluable_sla):,} tickets with a recorded first response."
    ),
)

c4.metric(
    "Estimated contact cost",
    f"₹{contact_cost:,.0f}",
    help=(
        "Calculated using the policy's channel-specific contact rates. "
        "This is an operational estimate, not a finance ledger."
    ),
)

st.caption(
    "Contact cost uses channel-specific policy rates. "
    "The policy's blended reference rate is ₹290 per contact."
)

st.divider()

# ============================================================
# WEEKLY DIGEST
# ============================================================

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "📊 Weekly digest",
        "🏆 Agent leaderboard",
        "🔁 Repeat contacts",
        "🔎 Data quality",
    ]
)

with tab1:
    st.markdown("## 1. Weekly support digest")

    if current.empty:
        show_empty_message(
            "No tickets were created for the selected week and team."
        )
    else:
        channel_counts = (
            current["channel"]
            .fillna("Unknown")
            .astype(str)
            .value_counts()
        )

        team_counts = (
            current["assigned_team"]
            .fillna("Unknown")
            .astype(str)
            .value_counts()
        )

        left, right = st.columns(2)

        # ---------------- Channel chart ----------------

        with left:
            st.markdown("### Tickets by channel")

            if channel_counts.empty:
                show_empty_message("No channel data is available.")
            else:
                fig, ax = plt.subplots(figsize=(7, 4))

                ax.bar(
                    channel_counts.index,
                    channel_counts.values,
                    color=TEAL,
                    edgecolor="#99F6E4",
                    linewidth=0.7,
                )

                ax.set_ylabel("Tickets")
                ax.set_xlabel("Channel")
                ax.set_title("Weekly channel volume")

                style_chart(fig, ax, grid_axis="y")
                st.pyplot(fig, use_container_width=True)
                plt.close(fig)

        # ---------------- Team chart ----------------

        with right:
            st.markdown("### Tickets by team")

            if team_counts.empty:
                show_empty_message("No team data is available.")
            else:
                sorted_counts = team_counts.sort_values(
                    ascending=True
                )

                fig, ax = plt.subplots(figsize=(7, 4))

                ax.barh(
                    sorted_counts.index,
                    sorted_counts.values,
                    color=INDIGO,
                    edgecolor="#C4B5FD",
                    linewidth=0.7,
                )

                ax.set_xlabel("Tickets")
                ax.set_title("Weekly team volume")

                style_chart(fig, ax, grid_axis="x")
                st.pyplot(fig, use_container_width=True)
                plt.close(fig)

        # ---------------- Observations ----------------

        st.markdown("### 💡 Operational observations")

        observation_items = []

        if not channel_counts.empty:
            observation_items.append(
                (
                    "Highest-volume channel",
                    f"{channel_counts.index[0]} "
                    f"({int(channel_counts.iloc[0])} tickets)",
                )
            )

        if not team_counts.empty:
            observation_items.append(
                (
                    "Highest-volume assigned team",
                    f"{team_counts.index[0]} "
                    f"({int(team_counts.iloc[0])} tickets)",
                )
            )

        completed_created_week = int(
            current["status"].astype(str).str.lower()
            .isin(["resolved", "closed"]).sum()
        )

        completion_rate = (
            completed_created_week / tickets_received * 100
            if tickets_received
            else 0
        )

        observation_items.append(
            (
                "Completion status of this week's created tickets",
                f"{completion_rate:.1f}% marked resolved/closed "
                "in the current snapshot",
            )
        )

        for label, value in observation_items:
            st.markdown(
                f"""
                <div style="
                    background:rgba(30,41,59,0.65);
                    border:1px solid #334155;
                    border-left:4px solid #2DD4BF;
                    border-radius:10px;
                    padding:12px 16px;
                    margin:8px 0;
                ">
                    <span style="color:#94A3B8;">{label}</span><br>
                    <strong style="color:#F8FAFC;">{value}</strong>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.caption(
            "The completion percentage above describes the current status "
            "of tickets created in the selected week. It is not the same "
            "as the count resolved during the week."
        )

        # ---------------- Themes ----------------

        st.divider()
        st.markdown("### 🧩 Complaint themes")

        theme_counts = (
            current["complaint_theme"]
            .fillna("Unclear / no text")
            .value_counts()
            .rename_axis("Complaint theme")
            .reset_index(name="Tickets")
        )

        theme_left, theme_right = st.columns([1, 1])

        with theme_left:
            st.dataframe(
                theme_counts,
                use_container_width=True,
                hide_index=True,
            )

        with theme_right:
            plot_themes = (
                theme_counts.sort_values("Tickets")
                .tail(8)
            )

            fig, ax = plt.subplots(figsize=(7, 4))

            ax.barh(
                plot_themes["Complaint theme"],
                plot_themes["Tickets"],
                color=VIOLET,
                edgecolor="#DDD6FE",
                linewidth=0.7,
            )

            ax.set_xlabel("Tickets")
            ax.set_title("Most frequent complaint themes")

            style_chart(fig, ax, grid_axis="x")
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

        st.caption(
            "Complaint themes are keyword-based classifications, "
            "not semantic AI judgements. Review sample tickets before acting."
        )

        # ---------------- Week-over-week comparison ----------------

        st.markdown("### 📈 Week-over-week changes")

        if not previous.empty:
            now = current["complaint_theme"].value_counts()
            before = previous["complaint_theme"].value_counts()

            comparison = pd.DataFrame(
                {
                    "This week": now,
                    "Previous week": before,
                }
            ).fillna(0).astype(int)

            comparison["Change"] = (
                comparison["This week"]
                - comparison["Previous week"]
            )

            comparison = comparison.sort_values(
                "This week",
                ascending=False,
            )

            st.dataframe(
                comparison,
                use_container_width=True,
            )
        else:
            st.caption(
                "There is no earlier week available for comparison."
            )

        # ---------------- Sample tickets ----------------

        with st.expander("🔍 Inspect sample tickets"):
            sample_cols = [
                col
                for col in [
                    "ticket_id",
                    "created_at",
                    "channel",
                    "assigned_team",
                    "category",
                    "complaint_theme",
                    "customer_message",
                    "agent_notes",
                ]
                if col in current.columns
            ]

            st.dataframe(
                current[sample_cols].head(30),
                use_container_width=True,
                hide_index=True,
            )

            st.download_button(
                "Download weekly ticket sample",
                data=current[sample_cols].to_csv(
                    index=False
                ).encode("utf-8"),
                file_name="weekly_ticket_sample.csv",
                mime="text/csv",
            )

# ============================================================
# AGENT LEADERBOARD
# ============================================================

with tab2:
    st.markdown("## 2. Agent leaderboard")

    st.write(
        "This is a weekly workload view based on tickets resolved or "
        "closed during the selected calendar week. It should not be "
        "used as a standalone performance assessment."
    )

    if closed_current.empty:
        show_empty_message(
            "No completed tickets were recorded for this week."
        )
    else:
        eligible = closed_current.copy()

        # Exclude Tier 2 / warranty from the ticket-volume ranking.
        tier_values = (
            eligible["agent_tier"].astype(str).str.lower()
            if "agent_tier" in eligible.columns
            else pd.Series("", index=eligible.index)
        )

        team_values = (
            eligible["roster_team"].astype(str).str.lower()
            if "roster_team" in eligible.columns
            else pd.Series("", index=eligible.index)
        )

        tier2_mask = (
            tier_values.str.contains("tier 2|tier2", regex=True)
            | team_values.str.contains(
                "escalations & warranty|warranty",
                regex=True,
            )
        )

        eligible = eligible[~tier2_mask].copy()

        if eligible.empty:
            show_empty_message(
                "No eligible non-Tier-2 agents were found for this week."
            )
        else:
            # Build optional aggregation fields safely.
            aggregations = {
                "Tickets closed": ("ticket_id", "count"),
                "SLA breaches": ("sla_breach", "sum"),
            }

            if "response_minutes" in eligible.columns:
                aggregations["Avg first response (min)"] = (
                    "response_minutes",
                    "mean",
                )

            if "csat_score" in eligible.columns:
                aggregations["Average CSAT"] = (
                    "csat_score",
                    "mean",
                )

            group_columns = [
                col
                for col in [
                    "agent_id",
                    "agent_name",
                    "roster_team",
                    "agent_tier",
                ]
                if col in eligible.columns
            ]

            if not group_columns:
                group_columns = ["agent_id"]

            board = (
                eligible.groupby(
                    group_columns,
                    dropna=False,
                )
                .agg(**aggregations)
                .reset_index()
            )

            board = board.sort_values(
                "Tickets closed",
                ascending=False,
            )

            board.insert(
                0,
                "Rank",
                range(1, len(board) + 1),
            )

            rename_map = {
                "agent_id": "Agent ID",
                "agent_name": "Agent name",
                "roster_team": "Agent team",
                "agent_tier": "Tier",
            }

            board = board.rename(columns=rename_map)

            if "Average CSAT" in board.columns:
                board["Average CSAT"] = (
                    board["Average CSAT"].round(2)
                )

            if "Avg first response (min)" in board.columns:
                board["Avg first response (min)"] = (
                    board["Avg first response (min)"].round(1)
                )

            st.dataframe(
                board,
                use_container_width=True,
                hide_index=True,
            )

            st.download_button(
                "Download leaderboard CSV",
                data=board.to_csv(index=False).encode("utf-8"),
                file_name="weekly_agent_leaderboard.csv",
                mime="text/csv",
            )

            st.caption(
                "Agent tier and team are matched from the roster where "
                "possible. Check unknown or unmatched agents before use. "
                "Workload, case complexity, shift, and quality can differ."
            )

    st.info(
        "Escalations & Warranty / Tier 2 is excluded from the volume "
        "leaderboard because the supplied policy says warranty work "
        "should be assessed by resolution time."
    )

# ============================================================
# REPEAT CONTACT INVESTIGATION
# ============================================================

with tab3:
    st.markdown("## 3. Repeat-contact investigation")

    st.write(
        "The policy defines a repeat contact as the same customer "
        "contacting support about the same issue within 30 days after "
        "resolution."
    )

    repeat = current[
        current["repeat_contact_proxy"].fillna(False)
    ].copy()

    all_repeat_flags = int(
        all_df["repeat_contact_proxy"].fillna(False).sum()
    )

    all_rows = len(all_df)

    flag_rate = (
        all_repeat_flags / all_rows * 100
        if all_rows
        else 0
    )

    # The cost is illustrative, not verified savings.
    illustrative_cost = all_repeat_flags * BLENDED_COST_INR

    r1, r2, r3 = st.columns(3)

    r1.metric(
        "Repeat-contact proxy flags",
        f"{len(repeat):,}",
        help="Flags within the selected week and team filter.",
    )

    r2.metric(
        "All-time flags in filtered data",
        f"{all_repeat_flags:,}",
    )

    r3.metric(
        "Illustrative contact cost",
        f"₹{illustrative_cost:,.0f}",
        help="Flag count multiplied by the policy's ₹290 blended rate.",
    )

    st.warning(
        "These are candidate cases for human review, not confirmed "
        "same-issue repeats. The prototype uses customer + product SKU "
        "+ category and a 30-day window after prior resolution. "
        "Matching fields do not prove that the issue is identical."
    )

    repeat_cols = [
        col
        for col in [
            "ticket_id",
            "repeat_of_ticket_id",
            "created_at",
            "customer_id",
            "product_sku",
            "category",
            "channel",
            "customer_message",
        ]
        if col in repeat.columns
    ]

    if repeat.empty:
        show_empty_message(
            "No repeat-contact proxy flags were found for this week."
        )
    else:
        st.dataframe(
            repeat[repeat_cols].head(200),
            use_container_width=True,
            hide_index=True,
        )

        st.download_button(
            "Download repeat-contact review sample",
            data=repeat[repeat_cols].to_csv(
                index=False
            ).encode("utf-8"),
            file_name="repeat_contact_review.csv",
            mime="text/csv",
        )

    st.divider()
    st.markdown("### 💰 Illustrative prevention scenario")

    reduction_pct = st.slider(
        "Assumed preventable share of flagged contacts (%)",
        min_value=0,
        max_value=100,
        value=15,
        step=5,
    )

    weeks_in_quarter = st.number_input(
        "Weeks in scenario",
        min_value=1,
        max_value=14,
        value=13,
        step=1,
    )

    date_weeks = (
        all_df["created_at"]
        .dropna()
        .dt.to_period("W-SUN")
        .nunique()
    )

    average_weekly_flags = (
        all_repeat_flags / date_weeks
        if date_weeks
        else 0
    )

    scenario_value = (
        average_weekly_flags
        * (reduction_pct / 100)
        * BLENDED_COST_INR
        * weeks_in_quarter
    )

    st.metric(
        "Scenario estimate",
        f"₹{scenario_value:,.0f}",
    )

    st.caption(
        "This is a hypothetical scenario, not realized savings or a "
        "causal estimate. Validate repeat cases and use channel-specific "
        "costs before making a business commitment."
    )

# ============================================================
# DATA QUALITY
# ============================================================

with tab4:
    st.markdown("## 4. Data quality and assumptions")

    st.write(
        "Repeated ticket IDs are flagged for review rather than "
        "automatically removed. The source notes warn that migration "
        "records can overlap and contain differences."
    )

    total_rows = len(df)

    distinct_ids = (
        df["ticket_id"].nunique()
        if "ticket_id" in df.columns
        else 0
    )

    repeated_rows = (
        int(df["duplicate_ticket_id"].fillna(False).sum())
        if "duplicate_ticket_id" in df.columns
        else 0
    )

    repeated_groups = (
        int(
            df.loc[
                df["duplicate_ticket_id"].fillna(False),
                "ticket_id",
            ].nunique()
        )
        if "duplicate_ticket_id" in df.columns
        and "ticket_id" in df.columns
        else 0
    )

    q1, q2, q3 = st.columns(3)

    q1.metric("Source rows analyzed", f"{total_rows:,}")
    q2.metric("Distinct ticket IDs", f"{distinct_ids:,}")
    q3.metric("Repeated ticket-ID groups", f"{repeated_groups:,}")

    st.markdown("### 📋 Data-quality summary")

    st.json(summary)

    # ---------------- Duplicate review ----------------

    st.markdown("### Repeated ticket IDs")

    if "duplicate_ticket_id" in df.columns:
        dup = df[
            df["duplicate_ticket_id"].fillna(False)
        ].copy()
    else:
        dup = pd.DataFrame()

    st.write(
        f"{len(dup):,} rows belong to repeated ticket IDs. "
        f"These represent {repeated_groups:,} distinct ID groups."
    )

    dup_cols = [
        col
        for col in [
            "ticket_id",
            "source_system",
            "created_at",
            "resolved_at",
            "customer_id",
            "product_sku",
            "category",
            "status",
            "csat_score",
        ]
        if col in dup.columns
    ]

    if dup.empty:
        show_empty_message("No repeated ticket IDs were detected.")
    else:
        st.dataframe(
            dup[dup_cols].head(200),
            use_container_width=True,
            hide_index=True,
        )

        st.download_button(
            "Download duplicate-ID review file",
            data=dup[dup_cols].to_csv(
                index=False
            ).encode("utf-8"),
            file_name="duplicate_ticket_ids_review.csv",
            mime="text/csv",
        )

    st.caption(
        "Do not automatically remove all repeated IDs. Review differences "
        "between helpdesk and legacy records, particularly resolution "
        "timestamps and CSAT representation."
    )

    # ---------------- Assumptions ----------------

    st.divider()
    st.markdown("### ⚠️ Important assumptions and limitations")

    st.markdown(
        """
        - **Complaint themes:** keyword-based classification; manual
          review is required.
        - **Repeat contacts:** customer + SKU + category is a proxy for
          the same issue, not semantic proof.
        - **Duplicate IDs:** flagged, not silently collapsed.
        - **Legacy monetary values:** not combined into financial totals
          because their native units differ from current INR values.
        - **SLA breaches:** calculated only when a first-response
          timestamp is available.
        - **CSAT:** blank and legacy zero values are treated as no response.
        - **Leaderboard:** a weekly volume view, not a complete measure
          of individual performance.
        - **Costs and savings:** estimates depend on policy rates and
          assumptions; they are not audited finance figures.
        """
    )

    st.markdown("### ✅ Recommended validation before submission")

    validation_items = [
        "Review a sample of complaint-theme classifications.",
        "Manually verify suspected repeat-contact cases.",
        "Compare weekly totals against an independent calculation.",
        "Review duplicate-ID groups before any reconciliation.",
        "Check unknown agents and roster assignments.",
    ]

    for item in validation_items:
        st.markdown(f"- {item}")

# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <div style="
        text-align:center;
        padding:12px 0;
        color:#94A3B8;
        font-size:0.85rem;
    ">
        <span style="color:#5EEAD4;font-weight:700;">
            VIREO AUDIO
        </span>
        &nbsp;·&nbsp; Support Insights Prototype
        <br>
        Validate data-quality exceptions and review flagged cases
        before making operational decisions.
    </div>
    """,
    unsafe_allow_html=True,
)
