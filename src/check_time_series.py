import pandas as pd
from pathlib import Path

file_path = Path("data/raw/combined_gee_pm25.csv")

df = pd.read_csv(file_path)

df["date"] = pd.to_datetime(df["date"], errors="coerce")

df = df.sort_values(["sensor_name", "date"])

print("\n===== CONTINUITÉ TEMPORELLE =====")

for station in [
    "MOLINA DE SEGURA",
    "SAN BASILIO",
    "CENMO1"
]:
    station_df = df[df["sensor_name"] == station].copy()

    station_df = station_df.sort_values("date")

    print(f"\nStation : {station}")
    print("Nombre de lignes :", len(station_df))
    print("Première date :", station_df["date"].min())
    print("Dernière date :", station_df["date"].max())

    differences = station_df["date"].diff().dt.days

    print("\nÉcarts entre les dates (en jours) :")
    print(differences.value_counts().sort_index().head(10))

    print(
        "Nombre d'écarts supérieurs à 1 jour :",
        (differences > 1).sum()
    )
