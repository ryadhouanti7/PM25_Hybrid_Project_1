
import pandas as pd
import matplotlib.pyplot as plt

# Charger les données
df = pd.read_csv("data/processed/pm25_daily.csv")

# Convertir la date
df["date"] = pd.to_datetime(df["date"])

# Extraire le mois
df["month"] = df["date"].dt.to_period("M")

# Variables à analyser
variables = ["O3", "CO", "NO2", "pm25"]

# Calculer le pourcentage de valeurs manquantes par mois
monthly_missing = (
    df.groupby("month")[variables]
    .apply(lambda group: group.isnull().mean() * 100)
)

print("===== VALEURS MANQUANTES PAR MOIS (%) =====")
print(monthly_missing.to_string())

# Créer le graphique
monthly_missing.index = monthly_missing.index.astype(str)

monthly_missing.plot(
    figsize=(13, 6),
    marker="o"
)

plt.title("Monthly Percentage of Missing Values")
plt.xlabel("Month")
plt.ylabel("Missing Values (%)")
plt.xticks(rotation=90)
plt.legend(title="Variables")
plt.tight_layout()

plt.savefig(
    "results/monthly_missing_values.png",
    dpi=300
)

plt.show()

print("\nGraphique enregistré dans results/monthly_missing_values.png")
