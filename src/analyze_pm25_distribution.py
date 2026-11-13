import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/processed/pm25_daily.csv")

# Supprimer les valeurs manquantes de PM2.5
pm25 = df["pm25"].dropna()

print("===== STATISTIQUES DESCRIPTIVES PM2.5 =====")
print(pm25.describe())

print("\n===== QUANTILES =====")
print(pm25.quantile([0.01, 0.05, 0.25, 0.50, 0.75, 0.95, 0.99]))

# Histogramme
plt.figure(figsize=(10, 5))

plt.hist(pm25, bins=50, edgecolor="black")

plt.title("Distribution of PM2.5 Concentrations")
plt.xlabel("PM2.5")
plt.ylabel("Frequency")

plt.tight_layout()

plt.savefig(
    "results/pm25_distribution.png",
    dpi=300
)

plt.show()

print("\nGraphique enregistré dans results/pm25_distribution.png")