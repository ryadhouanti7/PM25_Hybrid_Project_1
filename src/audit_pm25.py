import pandas as pd

df = pd.read_csv("data/raw/combined_gee_pm25.csv")

df["date"] = pd.to_datetime(df["date"], errors="coerce")

print("===== QUALITÉ DES VALEURS PM2.5 =====")

print("\nNombre total de lignes :", len(df))
print("Valeurs manquantes :", df["pm25"].isna().sum())
print("Valeurs négatives :", (df["pm25"] < 0).sum())
print("Valeurs égales à -999 :", (df["pm25"] == -999).sum())
print("Valeurs supérieures à 100 :", (df["pm25"] > 100).sum())

print("\nStatistiques PM2.5 :")
print(df["pm25"].describe())

print("\n===== DOUBLONS STATION + DATE =====")

duplicates = df[
    df.duplicated(
        subset=["sensor_name", "date"],
        keep=False
    )
].sort_values(["sensor_name", "date"])

print("Nombre de lignes concernées :", len(duplicates))

if not duplicates.empty:
    print(duplicates[
        ["sensor_name", "date", "id", "pm25"]
    ].to_string(index=False))

print("\n===== VALEURS MÉTÉOROLOGIQUES MANQUANTES =====")

weather_columns = [
    "temperature_celsius",
    "pressure_mb",
    "wind_u",
    "wind_v",
    "NO2",
    "CO",
    "O3",
    "AOD"
]

for column in weather_columns:
    print(column, ":", df[column].isna().sum())

print("\n===== VALEURS PM2.5 PAR STATION =====")

station_stats = df.groupby("sensor_name")["pm25"].agg(
    total="count",
    negative=lambda x: (x < 0).sum(),
    above_100=lambda x: (x > 100).sum(),
    minimum="min",
    maximum="max"
)

print(
    station_stats.sort_values(
        "negative",
        ascending=False
    ).to_string()
)