
import pandas as pd

df = pd.read_csv("data/processed/pm25_cleaned.csv")

# Sélectionner les valeurs supérieures à 100
high_values = df[df["pm25"] > 100].copy()

# Trier par concentration décroissante
high_values = high_values.sort_values(
    by="pm25",
    ascending=False
)

print("Nombre de valeurs supérieures à 100 :", len(high_values))

print("\n===== VALEURS LES PLUS ÉLEVÉES =====")

print(
    high_values[
        ["date", "sensor_name", "pm25"]
    ].head(20).to_string(index=False)
)

print("\n===== RÉPARTITION PAR STATION =====")

print(
    high_values.groupby("sensor_name").size()
    .sort_values(ascending=False)
)
