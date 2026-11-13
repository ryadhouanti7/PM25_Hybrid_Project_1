
import pandas as pd
import os

# 1. Charger le dataset original
df = pd.read_csv("data/raw/combined_gee_pm25.csv")

print("Nombre de lignes initial :", len(df))

# 2. Convertir les colonnes nécessaires
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["pm25"] = pd.to_numeric(df["pm25"], errors="coerce")

# 3. Identifier les valeurs suspectes AVANT le nettoyage
negative_count = (df["pm25"] < 0).sum()
high_count = (df["pm25"] > 100).sum()

# 4. Remplacer les valeurs négatives par NaN
df.loc[df["pm25"] < 0, "pm25"] = float("nan")

# 5. Ajouter un indicateur pour les valeurs élevées
df["pm25_suspicious_high"] = df["pm25"] > 100

# 6. Trier les données par station et par date
df = df.sort_values(
    ["sensor_name", "date"]
).reset_index(drop=True)

# 7. Créer le dossier de sortie s'il n'existe pas
os.makedirs("data/processed", exist_ok=True)

# 8. Enregistrer le dataset nettoyé
output_path = "data/processed/pm25_cleaned.csv"
df.to_csv(output_path, index=False)

# 9. Afficher le bilan
print("\n===== BILAN DU NETTOYAGE =====")
print("Nombre de lignes :", len(df))
print("Valeurs négatives remplacées par NaN :", negative_count)
print("Valeurs supérieures à 100 signalées :", high_count)
print("Valeurs PM2.5 manquantes après nettoyage :", df["pm25"].isna().sum())
print("Doublons station + date conservés :", 
      df.duplicated(["sensor_name", "date"]).sum())

print("\nFichier enregistré :", output_path)
print("\nStatistiques PM2.5 après nettoyage :")
print(df["pm25"].describe())
