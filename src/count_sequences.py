import pandas as pd

df = pd.read_csv("data/raw/combined_gee_pm25.csv")

df["date"] = pd.to_datetime(df["date"], errors="coerce")

results = []

for station, group in df.groupby("sensor_name"):

    dates = (
        group["date"]
        .dropna()
        .drop_duplicates()
        .sort_values()
        .reset_index(drop=True)
    )

    if len(dates) < 2:
        continue

    differences = dates.diff().dt.days
    period_ids = differences.ne(1).cumsum()

    periods = dates.groupby(period_ids).size()

    sequences = {
        "sequences_7_days": sum(max(0, length - 7) for length in periods),
        "sequences_14_days": sum(max(0, length - 14) for length in periods),
        "sequences_21_days": sum(max(0, length - 21) for length in periods),
        "sequences_30_days": sum(max(0, length - 30) for length in periods)
    }

    results.append({
        "station": station,
        "unique_days": len(dates),
        **sequences
    })

result_df = pd.DataFrame(results)

result_df = result_df.sort_values(
    "sequences_7_days",
    ascending=False
)

print("\n===== SÉQUENCES TEMPORELLES EXPLOITABLES =====")
print(result_df.to_string(index=False))

print("\n===== TOTAL DES SÉQUENCES =====")

for column in [
    "sequences_7_days",
    "sequences_14_days",
    "sequences_21_days",
    "sequences_30_days"
]:
    print(column, ":", result_df[column].sum())

result_df.to_csv(
    "results/sequence_counts.csv",
    index=False
)

print("\nRésultats sauvegardés dans results/sequence_counts.csv")