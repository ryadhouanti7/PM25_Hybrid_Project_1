import pandas as pd
from pathlib import Path

# Chemin vers le fichier de données
file_path = Path("data/raw/pm25.csv")

# Vérifier que le fichier existe
if not file_path.exists():
    print("Erreur : le fichier pm25.csv est introuvable.")
else:
    # Charger les données
    df = pd.read_csv(file_path)

    # Afficher les premières lignes
    print("\n===== APERÇU DES DONNÉES =====")
    print(df.head())

    # Afficher les dimensions
    print("\n===== DIMENSIONS =====")
    print(f"Nombre de lignes : {df.shape[0]}")
    print(f"Nombre de colonnes : {df.shape[1]}")

    # Afficher les noms des colonnes
    print("\n===== COLONNES =====")
    print(df.columns.tolist())

    # Afficher les types de données
    print("\n===== TYPES DE DONNÉES =====")
    print(df.dtypes)

    # Compter les valeurs manquantes
    print("\n===== VALEURS MANQUANTES =====")
    print(df.isnull().sum())

    # Afficher les statistiques descriptives
    print("\n===== STATISTIQUES DESCRIPTIVES =====")
    print(df.describe(include="all").T)

# Analyse complémentaire de la qualité des données

print("\n===== PÉRIODE DES DONNÉES =====")
df["date"] = pd.to_datetime(df["date"], errors="coerce")
print("Date de début :", df["date"].min())
print("Date de fin :", df["date"].max())

print("\n===== VALEURS MANQUANTES =====")
print(df.isnull().sum())

print("\n===== DOUBLONS =====")
print("Nombre de lignes dupliquées :", df.duplicated().sum())

print("\n===== STATIONS =====")
print("Nombre de stations :", df["sensor_name"].nunique())
print(df["sensor_name"].value_counts().head(10))

print("\n===== STATISTIQUES DE PM2.5 =====")
print(df["pm25"].describe())

print("\n===== VALEURS DE PM2.5 MANQUANTES =====")
print("Valeurs manquantes :", df["pm25"].isnull().sum())

print("\n===== VALEURS DE PM2.5 NÉGATIVES =====")
print("Valeurs négatives :", (df["pm25"] < 0).sum())

print("\n===== ANALYSE DES VALEURS ANORMALES =====")

print("Valeurs égales à -999 :", (df["pm25"] == -999).sum())

print("Valeurs inférieures ou égales à 0 :",
      (df["pm25"] <= 0).sum())

print("Valeurs supérieures à 100 :",
      (df["pm25"] > 100).sum())

print("\n===== PLUS GRANDES VALEURS =====")
print(
    df.nlargest(10, "pm25")[
        ["date", "sensor_name", "pm25"]
    ]
)

print("\n===== VALEURS NÉGATIVES PAR STATION =====")
negative_values = df[df["pm25"] < 0]

print(
    negative_values.groupby("sensor_name")["pm25"]
    .agg(["count", "min", "max"])
    .sort_values("count", ascending=False)
    .head(10)
)
