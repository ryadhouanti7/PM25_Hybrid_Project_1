import pandas as pd

# Charger le dataset nettoyé
df = pd.read_csv("data/processed/pm25_daily.csv")

df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["pm25"] = pd.to_numeric(df["pm25"], errors="coerce")

# Récupérer les valeurs supérieures à 100
high_values = df[df["pm25"] > 100].copy()

high_values = high_values.sort_values(
    ["sensor_name", "date"]
)

print("===== VALEURS PM2.5 SUPERIEURES A 100 =====")

columns = [
    "date",
    "sensor_name",
    "pm25",
    "temperature_celsius",
    "pressure_mb",
    "wind_u",
    "wind_v",
    "NO2",
    "CO",
    "O3",
    "AOD"
]

print(high_values[columns].to_string(index=False))

# Vérifier les valeurs extrêmes par station
print("\n===== NOMBRE DE VALEURS EXTREMES PAR STATION =====")

print(
    high_values.groupby("sensor_name")
    .agg(
        nombre_valeurs=("pm25", "count"),
        maximum=("pm25", "max"),
        moyenne=("pm25", "mean")
    )
    .sort_values("nombre_valeurs", ascending=False)
)

# Vérifier les valeurs extrêmes consécutives
print("\n===== INTERVALLES ENTRE VALEURS EXTREMES =====")

for station, group in high_values.groupby("sensor_name"):
    dates = group["date"].sort_values()
    
    if len(dates) > 1:
        differences = dates.diff().dt.days.dropna()
        consecutive = (differences == 1).sum()

        print(
            f"{station}: {len(dates)} valeurs, "
            f"{consecutive} intervalles de 1 jour"
        )
