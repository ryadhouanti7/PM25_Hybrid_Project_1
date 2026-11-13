import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

df = pd.read_csv("data/processed/pm25_daily.csv")

# Variables numériques
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

# Sélectionner les colonnes
data = df[features].copy()

# Calculer les corrélations
correlation = data.corr(method="pearson")

print("===== MATRICE DE CORRÉLATION =====")
print(correlation.round(3))

# Sauvegarder la matrice
os.makedirs("results", exist_ok=True)

correlation.to_csv("results/correlation_matrix.csv")

# Visualisation
plt.figure(figsize=(11, 8))

sns.heatmap(
    correlation,
    annot=True,
    cmap="coolwarm",
    fmt=".2f",
    center=0
)

plt.title("Correlation Matrix of PM2.5 and Environmental Variables")
plt.tight_layout()

plt.savefig(
    "results/correlation_matrix.png",
    dpi=300
)

plt.show()

print("\nRésultats enregistrés dans results/")
