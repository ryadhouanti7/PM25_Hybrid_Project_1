import pandas as pd

file_path = "data/raw/combined_gee_pm25.csv"

df = pd.read_csv(file_path)

df["date"] = pd.to_datetime(df["date"], errors="coerce")

results = []

for station, group in df.groupby("sensor_name"):

    # Une seule date par station pour analyser la continuité
    dates = (
        group["date"]
        .dropna()
        .drop_duplicates()
        .sort_values()
        .reset_index(drop=True)
    )

    if len(dates) == 0:
        continue

    # Détecter les interruptions
    differences = dates.diff().dt.days

    # Chaque interruption commence une nouvelle période
    new_period = differences.ne(1)

    period_ids = new_period.cumsum()

    # Calculer la longueur de chaque période
    periods = dates.groupby(period_ids).size()

    results.append({
        "station": station,
        "unique_days": len(dates),
        "longest_period_days": periods.max(),
        "periods_7_days_or_more": (periods >= 7).sum(),
        "periods_30_days_or_more": (periods >= 30).sum(),
        "periods_90_days_or_more": (periods >= 90).sum(),
        "periods_180_days_or_more": (periods >= 180).sum()
    })

result_df = pd.DataFrame(results)

result_df = result_df.sort_values(
    "longest_period_days",
    ascending=False
)

print("\n===== PÉRIODES CONTINUES PAR STATION =====")
print(result_df.to_string(index=False))

result_df.to_csv(
    "results/continuous_periods.csv",
    index=False
)

print("\nFichier sauvegardé : results/continuous_periods.csv")