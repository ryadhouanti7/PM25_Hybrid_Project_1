import pandas as pd

# Charger le dataset
df = pd.read_csv("data/processed/pm25_daily.csv")

df["date"] = pd.to_datetime(df["date"])

variables = ["pm25", "NO2", "CO", "O3"]

# 1. Valeurs manquantes par année
df["year"] = df["date"].dt.year

print("===== VALEURS MANQUANTES PAR ANNEE (%) =====")

missing_year = df.groupby("year")[variables].apply(
    lambda group: group.isna().mean() * 100
)

print(missing_year.round(2))

# 2. Valeurs manquantes par station
print("\n===== VALEURS MANQUANTES PAR STATION (%) =====")

missing_station = df.groupby("sensor_name")[variables].apply(
    lambda group: group.isna().mean() * 100
)

print(missing_station.round(2).to_string())

# 3. Stations les plus touchées
print("\n===== STATIONS LES PLUS TOUCHEES =====")

print(
    missing_station.sort_values(
        "NO2", ascending=False
    ).head(15).round(2)
)

# 4. Enregistrer les résultats
missing_year.to_csv("results/missing_by_year.csv")
missing_station.to_csv("results/missing_by_station.csv")

print("\nFichiers enregistrés dans results/")
