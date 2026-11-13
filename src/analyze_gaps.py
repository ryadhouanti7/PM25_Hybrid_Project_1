import pandas as pd
from pathlib import Path

file_path = Path("data/raw/combined_gee_pm25.csv")

df = pd.read_csv(file_path)

df["date"] = pd.to_datetime(df["date"], errors="coerce")

df = df.sort_values(["sensor_name", "date"])

results = []

for station, group in df.groupby("sensor_name"):

    group = group.sort_values("date")

    gaps = group["date"].diff().dt.days.dropna()

    results.append({
        "station": station,
        "measurements": len(group),
        "first_date": group["date"].min(),
        "last_date": group["date"].max(),
        "gaps_over_1_day": (gaps > 1).sum(),
        "gaps_over_7_days": (gaps > 7).sum(),
        "max_gap_days": gaps.max()
    })

gaps_df = pd.DataFrame(results)

gaps_df = gaps_df.sort_values(
    "gaps_over_1_day",
    ascending=False
)

print("\n===== ANALYSE DES INTERRUPTIONS =====")
print(gaps_df.to_string(index=False))

print("\n===== STATISTIQUES GÉNÉRALES =====")
print("Nombre de stations :", len(gaps_df))
print("Interruption maximale :", gaps_df["max_gap_days"].max(), "jours")
print("Moyenne des interruptions par station :",
      round(gaps_df["gaps_over_1_day"].mean(), 2))

gaps_df.to_csv(
    "results/temporal_gaps.csv",
    index=False
)

print("\nFichier sauvegardé dans results/temporal_gaps.csv")
