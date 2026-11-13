import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/processed/pm25_daily.csv")

pm25 = df["pm25"].dropna()

print("===== ANALYSE DES VALEURS EXTRÊMES =====")

for threshold in [25, 50, 100, 200, 500]:
    count = (pm25 > threshold).sum()
    percentage = count / len(pm25) * 100

    print(
        f"Valeurs > {threshold}: "
        f"{count} ({percentage:.3f}%)"
    )

# Examiner les valeurs les plus élevées
print("\n===== TOP 20 DES VALEURS PM2.5 =====")

print(
    df.nlargest(20, "pm25")[
        ["date", "sensor_name", "pm25"]
    ].to_string(index=False)
)

# Histogramme sans les valeurs supérieures à 100
pm25_normal = pm25[pm25 <= 100]

plt.figure(figsize=(10, 5))

plt.hist(
    pm25_normal,
    bins=50,
    edgecolor="black"
)

plt.title("PM2.5 Distribution (Values <= 100)")
plt.xlabel("PM2.5")
plt.ylabel("Frequency")

plt.tight_layout()

plt.savefig(
    "results/pm25_distribution_zoom.png",
    dpi=300
)

plt.show()

print("\nGraphique enregistré.")