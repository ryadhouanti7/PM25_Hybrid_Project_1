
import pandas as pd

# Charger le dataset
df = pd.read_csv("data/processed/pm25_daily.csv")

print("===== DIMENSIONS DU DATASET =====")
print("Nombre de lignes :", len(df))
print("Nombre de colonnes :", len(df.columns))

# Calculer les valeurs manquantes
missing = pd.DataFrame({
    "Missing_Count": df.isnull().sum(),
    "Missing_Percentage": (
        df.isnull().sum() / len(df)
    ) * 100
})

# Trier par nombre de valeurs manquantes
missing = missing.sort_values(
    by="Missing_Count",
    ascending=False
)

print("\n===== VALEURS MANQUANTES PAR COLONNE =====")
print(missing.to_string())

# Nombre de lignes ayant au moins une valeur manquante
rows_with_missing = df.isnull().any(axis=1).sum()

print("\n===== BILAN =====")
print("Lignes avec au moins une valeur manquante :",
      rows_with_missing)

print("Lignes complètes :",
      len(df) - rows_with_missing)

# Sauvegarder les résultats
missing.to_csv(
    "results/missing_values.csv"
)

print("\nRésultats enregistrés dans results/missing_values.csv")
