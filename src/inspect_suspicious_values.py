
import pandas as pd

df = pd.read_csv("data/raw/combined_gee_pm25.csv")

df["date"] = pd.to_datetime(df["date"], errors="coerce")

# Valeurs PM2.5 negatives
negative = df[df["pm25"] < 0].copy()

# Valeurs PM2.5 superieures a 100
high = df[df["pm25"] > 100].copy()

print("===== VALEURS NEGATIVES =====")
print("Nombre :", len(negative))

print("\nValeurs negatives distinctes :")
print(negative["pm25"].value_counts().sort_index().to_string())

print("\nExemples de lignes :")
print(
    negative[
        ["date", "sensor_name", "id", "pm25"]
    ].sort_values("pm25").to_string(index=False)
)

print("\n===== VALEURS SUPERIEURES A 100 =====")
print("Nombre :", len(high))

print(
    high[
        ["date", "sensor_name", "id", "pm25"]
    ].sort_values("pm25", ascending=False).to_string(index=False)
)

print("\n===== REPARTITION DES VALEURS SUPERIEURES A 100 =====")
print(
    high.groupby("sensor_name")["pm25"]
    .agg(["count", "min", "max"])
    .sort_values("max", ascending=False)
    .to_string()
)
