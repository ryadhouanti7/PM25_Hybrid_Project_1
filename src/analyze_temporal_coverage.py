import pandas as pd

df = pd.read_csv("data/processed/pm25_daily.csv")

df["date"] = pd.to_datetime(df["date"])
df = df.dropna(subset=["pm25"])

# Analyse annuelle
df["year"] = df["date"].dt.year

yearly = df.groupby("year").agg(
    observations=("pm25", "count"),
    stations=("sensor_name", "nunique"),
    pm25_mean=("pm25", "mean")
)

print("===== COUVERTURE ANNUELLE =====")
print(yearly.round(2))

# Analyse mensuelle
df["month"] = df["date"].dt.to_period("M")

monthly = df.groupby("month").agg(
    observations=("pm25", "count"),
    stations=("sensor_name", "nunique"),
    pm25_mean=("pm25", "mean")
)

print("\n===== PREMIERS MOIS =====")
print(monthly.head(15).round(2))

print("\n===== DERNIERS MOIS =====")
print(monthly.tail(15).round(2))

# Sauvegarde
yearly.to_csv("results/yearly_coverage.csv")
monthly.to_csv("results/monthly_coverage.csv")

print("\nFichiers enregistrés dans results/")
