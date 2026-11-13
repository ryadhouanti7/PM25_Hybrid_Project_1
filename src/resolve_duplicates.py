
import pandas as pd

df = pd.read_csv("data/processed/pm25_cleaned.csv")

print("Lignes avant traitement :", len(df))

# Identifier les doublons
duplicates = df[
    df.duplicated(
        subset=["sensor_name", "date"],
        keep=False
    )
]

print("\nGroupes de doublons :", 
      duplicates.groupby(["sensor_name", "date"]).ngroups)

# Regrouper les mesures quotidiennes par station
df = df.groupby(
    ["sensor_name", "date"],
    as_index=False
).agg({
    "id": "first",
    "latitude": "first",
    "longitude": "first",
    "temperature_celsius": "mean",
    "pressure_mb": "mean",
    "wind_u": "mean",
    "wind_v": "mean",
    "NO2": "mean",
    "CO": "mean",
    "O3": "mean",
    "AOD": "mean",
    "pm25": "mean",
    "pm25_suspicious_high": "max"
})

# Trier chronologiquement
df = df.sort_values(
    ["sensor_name", "date"]
).reset_index(drop=True)

# Sauvegarder
df.to_csv(
    "data/processed/pm25_daily.csv",
    index=False
)

print("\n===== BILAN =====")
print("Lignes après traitement :", len(df))
print("Doublons restants :", 
      df.duplicated(["sensor_name", "date"]).sum())

print("\nFichier enregistré : data/processed/pm25_daily.csv")
