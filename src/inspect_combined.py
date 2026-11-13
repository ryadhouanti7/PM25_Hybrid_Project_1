import pandas as pd
from pathlib import Path

file_path = Path("data/raw/combined_gee_pm25.csv")

df = pd.read_csv(file_path)

print("\n===== DIMENSIONS =====")
print(df.shape)

print("\n===== VALEURS MANQUANTES =====")
print(df.isnull().sum())

print("\n===== DOUBLONS COMPLETS =====")
print(df.duplicated().sum())

print("\n===== DOUBLONS DATE + STATION =====")
print(
    df.duplicated(subset=["date", "sensor_name"]).sum()
)

print("\n===== PÉRIODE =====")
df["date"] = pd.to_datetime(df["date"], errors="coerce")
print("Début :", df["date"].min())
print("Fin :", df["date"].max())

print("\n===== VALEURS DE PM2.5 =====")
print(df["pm25"].describe())

print("\n===== VALEURS DE PM2.5 INVALIDES OU SUSPECTES =====")
print("Valeurs négatives :", (df["pm25"] < 0).sum())
print("Valeurs égales à -999 :", (df["pm25"] == -999).sum())
print("Valeurs supérieures à 100 :", (df["pm25"] > 100).sum())

print("\n===== NOMBRE DE STATIONS =====")
print(df["sensor_name"].nunique())

print("\n===== VALEURS MANQUANTES DES VARIABLES ATMOSPHÉRIQUES =====")
features = [
    "temperature_celsius",
    "pressure_mb",
    "wind_u",
    "wind_v",
    "NO2",
    "CO",
    "O3",
    "AOD"
]

for col in features:
    print(f"{col}: {df[col].isna().sum()} valeurs manquantes")

print("\n===== DOUBLONS DATE + STATION =====")

duplicates = df[
    df.duplicated(
        subset=["date", "sensor_name"],
        keep=False
    )
].sort_values(["date", "sensor_name"])

if duplicates.empty:
    print("Aucun doublon.")
else:
    print(
        duplicates[
            [
                "date",
                "sensor_name",
                "id",
                "pm25",
                "temperature_celsius",
                "pressure_mb",
                "wind_u",
                "wind_v"
            ]
        ].to_string(index=False)
    )

print("\n===== RELATION ENTRE ID ET NOM DE STATION =====")

print(
    "Nombre d'identifiants différents :",
    df["id"].nunique()
)

print(
    "Nombre de noms de stations différents :",
    df["sensor_name"].nunique()
)

print("\n===== NOMS ASSOCIÉS À PLUSIEURS ID =====")

ids_per_station = df.groupby("sensor_name")["id"].nunique()

print(ids_per_station[ids_per_station > 1].sort_values(ascending=False))

print("\n===== STATIONS ASSOCIÉES À PLUSIEURS ID =====")

stations_per_id = df.groupby("id")["sensor_name"].nunique()

print(stations_per_id[stations_per_id > 1].sort_values(ascending=False))

print("\n===== NOMBRE DE MESURES PAR ID =====")

print(
    df.groupby(["id", "sensor_name"])
    .size()
    .sort_values(ascending=False)
    .head(15)
)