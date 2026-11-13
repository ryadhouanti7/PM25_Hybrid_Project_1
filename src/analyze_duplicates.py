
import pandas as pd

df = pd.read_csv("data/processed/pm25_cleaned.csv")

# Identifier les doublons station + date
duplicates = df[
    df.duplicated(
        subset=["sensor_name", "date"],
        keep=False
    )
]

print("===== DOUBLONS STATION + DATE =====")

print(
    duplicates[
        ["date", "sensor_name", "id", "pm25"]
    ].sort_values(
        ["sensor_name", "date"]
    ).to_string(index=False)
)

print("\nNombre total de lignes concernées :", len(duplicates))

print("\nNombre de groupes concernés :",
      duplicates.groupby(["sensor_name", "date"]).ngroups)
