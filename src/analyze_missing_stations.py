import pandas as pd

df = pd.read_csv("data/processed/pm25_daily.csv")

variables = ["pm25", "NO2", "CO", "O3"]

# Calculer les statistiques par station
summary = df.groupby("sensor_name").agg(
    total_rows=("date", "count"),
    pm25_missing=("pm25", lambda x: x.isna().sum()),
    NO2_missing=("NO2", lambda x: x.isna().sum()),
    CO_missing=("CO", lambda x: x.isna().sum()),
    O3_missing=("O3", lambda x: x.isna().sum())
)

# Calculer les pourcentages
for variable in variables:
    column = variable + "_missing"
    summary[variable + "_missing_percent"] = (
        summary[column] / summary["total_rows"] * 100
    )

# Trier selon les valeurs manquantes de PM2.5
summary = summary.sort_values(
    "pm25_missing_percent",
    ascending=False
)

print("===== VALEURS MANQUANTES PAR STATION =====")
print(summary.to_string())

# Sauvegarder
summary.to_csv("results/missing_values_by_station.csv")

print("\nNombre de stations :", len(summary))
print("Résultats enregistrés.")
