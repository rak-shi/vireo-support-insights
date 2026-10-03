
import pandas as pd
from pathlib import Path

data_dir = Path(__file__).resolve().parent / "data"

df = pd.read_csv(
    data_dir / "tickets.csv",
    dtype={"ticket_id": "string"},
)

print("DUPLICATE AUDIT SUMMARY")
print("=" * 60)

# Keep only ticket IDs appearing more than once.
duplicate_ids = df.loc[
    df["ticket_id"].duplicated(keep=False),
    "ticket_id",
].dropna().unique()

duplicates = df[df["ticket_id"].isin(duplicate_ids)].copy()

# Count how often each field differs within a ticket-ID group.
comparison_columns = [
    col for col in df.columns
    if col not in ["ticket_id", "source_system"]
]

difference_counts = {}

for column in comparison_columns:
    groups_with_differences = 0

    for _, group in duplicates.groupby("ticket_id"):
        if group[column].nunique(dropna=False) > 1:
            groups_with_differences += 1

    if groups_with_differences:
        difference_counts[column] = groups_with_differences

print("\nRepeated-ID groups:", len(duplicate_ids))
print("\nGroups with differences by column:")

for column, count in sorted(
    difference_counts.items(),
    key=lambda item: item[1],
    reverse=True,
):
    print(f"{column}: {count}")

# Show missing and non-missing resolution dates by source.
print("\nRESOLUTION DATE COMPLETENESS BY SOURCE")
print("-" * 60)

print(
    duplicates.groupby("source_system")["resolved_at"]
    .agg(
        total_rows="size",
        missing_resolved_at=lambda s: s.isna().sum(),
        available_resolved_at=lambda s: s.notna().sum(),
    )
    .to_string()
)

# Show CSAT values by source.
print("\nCSAT VALUES BY SOURCE")
print("-" * 60)

print(
    duplicates.groupby("source_system")["csat_score"]
    .agg(
        total_rows="size",
        missing_csat=lambda s: s.isna().sum(),
        zero_csat=lambda s: (s == 0).sum(),
        nonzero_csat=lambda s: ((s.notna()) & (s != 0)).sum(),
    )
    .to_string()
)

# Save conflicting rows for inspection.
duplicates.sort_values(
    ["ticket_id", "source_system"]
).to_csv(
    data_dir / "repeated_ticket_ids_review.csv",
    index=False,
)

print("\nSaved detailed records to:")
print("data/repeated_ticket_ids_review.csv")
print("Original tickets.csv was not modified.")
