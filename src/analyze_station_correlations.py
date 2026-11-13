import pandas as pd

df = pd.read_csv("data/processed/pm25_daily.csv")

features = [
    "temperature_celsius",
    "pressure_mb",
    "wind_u",
    "wind_v",
    "NO2",
    "CO",
    "O3",
    "AOD"
]

results = []

for station, group in df.groupby("sensor_name"):

    for feature in features:

        valid = group[["pm25", feature]].dropna()

        if len(valid) >= 30:

            correlation = valid["pm25"].corr(
                valid[feature]
            )

            results.append({
                "station": station,
                "variable": feature,
                "correlation": correlation,
                "observations": len(valid)
            })

results_df = pd.DataFrame(results)

results_df.to_csv(
    "results/station_correlations.csv",
    index=False
)

print("===== CORRÉLATIONS PAR STATION =====")

for feature in features:

    subset = results_df[
        results_df["variable"] == feature
    ]

    print(f"\n--- {feature} ---")

    print(
        subset.sort_values(
            "correlation",
            ascending=False
        ).head(5).round(3).to_string(index=False)
    )

print("\nRésultats enregistrés dans results/station_correlations.csv")
