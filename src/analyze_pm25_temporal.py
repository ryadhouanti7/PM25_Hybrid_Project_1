import pandas as pd
import matplotlib.pyplot as plt

# Charger les données
df = pd.read_csv("data/processed/pm25_daily.csv")

df["date"] = pd.to_datetime(df["date"])

# Retirer uniquement les PM2.5 manquants
df = df.dropna(subset=["pm25"])

# Extraire année et mois
df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.to_period("M")

# Moyenne annuelle
yearly = df.groupby("year")["pm25"].mean()

print("===== MOYENNE ANNUELLE PM2.5 =====")
print(yearly)

plt.figure(figsize=(10, 5))
yearly.plot(marker="o")

plt.title("Annual Average PM2.5 Concentration")
plt.xlabel("Year")
plt.ylabel("Average PM2.5")
plt.grid(True)
plt.tight_layout()

plt.savefig(
    "results/pm25_yearly_trend.png",
    dpi=300
)

plt.show()

# Moyenne mensuelle
monthly = df.groupby("month")["pm25"].mean()
monthly.index = monthly.index.astype(str)

plt.figure(figsize=(13, 5))
monthly.plot()

plt.title("Monthly Average PM2.5 Concentration")
plt.xlabel("Month")
plt.ylabel("Average PM2.5")
plt.xticks(rotation=90)
plt.grid(True)
plt.tight_layout()

plt.savefig(
    "results/pm25_monthly_trend.png",
    dpi=300
)

plt.show()

print("\nGraphiques enregistrés dans results/")
