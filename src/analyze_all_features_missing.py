import pandas as pd

df = pd.read_csv("data/processed/pm25_daily.csv")

features = [
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

# Pourcentage global de valeurs manquantes
print("===== VALEURS MANQUANTES GLOBALES =====")

missing = pd.DataFrame({
    "missing_count": df[features].isna().sum(),
    "missing_percentage": df[features].isna().mean() * 100
})

print(missing.round(2))

# Pourcentage par station
print("\n===== VALEURS MANQUANTES PAR STATION =====")

station_missing = df.groupby("sensor_name")[features].apply(
    lambda group: group.isna().mean() * 100
)

print(station_missing.round(2).to_string())

# Nombre de lignes complètes pour chaque groupe de variables
print("\n===== LIGNES COMPLETES =====")

groups = {
    "Toutes les variables": features,
    "Sans NO2, CO et O3": [
        "pm25", "temperature_celsius",
        "pressure_mb", "wind_u", "wind_v", "AOD"
    ],
    "Variables meteorologiques uniquement": [
        "pm25", "temperature_celsius",
        "pressure_mb", "wind_u", "wind_v"
    ]
}

for name, columns in groups.items():
    count = df[columns].notna().all(axis=1).sum()
    print(f"{name}: {count} lignes")

# Sauvegarder
missing.to_csv("results/all_features_missing.csv")
station_missing.to_csv("results/all_features_missing_by_station.csv")

print("\nRésultats enregistrés dans results/")
