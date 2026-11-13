
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/processed/pm25_daily.csv")

# Calculer le pourcentage de valeurs manquantes
missing_percent = (
    df.isnull().mean() * 100
).sort_values(ascending=False)

# Garder uniquement les colonnes qui ont des valeurs manquantes
missing_percent = missing_percent[
    missing_percent > 0
]

# Créer le graphique
plt.figure(figsize=(9, 5))

missing_percent.plot(
    kind="bar",
    color="steelblue"
)

plt.title("Percentage of Missing Values by Variable")
plt.xlabel("Variables")
plt.ylabel("Missing Values (%)")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    "results/missing_values_plot.png",
    dpi=300
)

plt.show()

print("Graphique enregistré dans results/missing_values_plot.png")
