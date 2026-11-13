import pandas as pd

df = pd.read_csv("data/processed/pm25_daily.csv")

variables = [
    "pm25",
    "temperature_celsius",
    "pressure_mb",
    "wind_u",
    "wind_v",
    "AOD",
    "NO2",
    "CO",
    "O3"
]

# Calculer la disponibilité par station
summary = df.groupby("sensor_name")[variables].agg(
    lambda x: x.notna().mean() * 100
)

summary = summary.round(2)

# Ajouter le nombre de mesures par station
summary.insert(
    0,
    "total_rows",
    df.groupby("sensor_name").size()
)

print("===== DISPONIBILITÉ DES VARIABLES PAR STATION (%) =====")
print(summary.to_string())

# Sauvegarder
summary.to_csv(
    "results/station_data_quality.csv"
)

print("\nNombre de stations :", len(summary))
print("Fichier enregistré : results/station_data_quality.csv")
