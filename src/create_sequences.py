import os
import numpy as np
import pandas as pd

# 1. Charger les donnees
df = pd.read_csv("data/processed/pm25_daily.csv")
df["date"] = pd.to_datetime(df["date"])

# 2. Parametres
WINDOW_SIZE = 7

features = [
    "pm25",
    "temperature_celsius",
    "pressure_mb",
    "wind_u",
    "wind_v",
    "AOD"
]

# 3. Verifier les doublons
duplicates = df.duplicated(
    subset=["sensor_name", "date"]
).sum()

print("Doublons station-date :", duplicates)

if duplicates > 0:
    raise ValueError("Des doublons station-date existent.")

# 4. Trier les donnees
df = df.sort_values(
    ["sensor_name", "date"]
).reset_index(drop=True)

X_sequences = []
y_targets = []
metadata = []

# 5. Construire les sequences
for station, group in df.groupby("sensor_name", sort=False):

    group = group.sort_values("date")

    dates = group["date"].to_numpy(dtype="datetime64[D]")
    values = group[features].to_numpy(dtype=np.float32)

    # Verifier les fenetres de 8 jours
    for i in range(len(group) - WINDOW_SIZE):

        # 8 dates : 7 jours d'entree + 1 jour cible
        if not np.all(np.diff(dates[i:i + WINDOW_SIZE + 1]) == np.timedelta64(1, "D")):
            continue

        input_data = values[i:i + WINDOW_SIZE]
        target = values[i + WINDOW_SIZE, 0]

        # Ignorer les valeurs manquantes
        if not np.isfinite(input_data).all():
            continue

        if not np.isfinite(target):
            continue

        X_sequences.append(input_data)
        y_targets.append(target)

        metadata.append({
            "sensor_name": station,
            "start_date": pd.Timestamp(dates[i]),
            "end_date": pd.Timestamp(dates[i + WINDOW_SIZE - 1]),
            "target_date": pd.Timestamp(dates[i + WINDOW_SIZE])
        })

# 6. Conversion en tableaux NumPy
X = np.asarray(X_sequences, dtype=np.float32)
y = np.asarray(y_targets, dtype=np.float32)

metadata_df = pd.DataFrame(metadata)

# 7. Sauvegarder les resultats
os.makedirs("data/processed", exist_ok=True)
os.makedirs("results", exist_ok=True)

np.savez_compressed(
    "data/processed/cnn_lstm_sequences.npz",
    X=X,
    y=y,
    feature_names=np.array(features)
)

metadata_df.to_csv(
    "results/cnn_lstm_sequences_metadata.csv",
    index=False
)

# 8. Afficher les resultats
print("\n===== RESULTATS DES SEQUENCES =====")
print("Nombre de sequences :", len(X))
print("Dimensions de X :", X.shape)
print("Dimensions de y :", y.shape)

print("\nVariables utilisees :", features)
print("Fenetre d'entree :", WINDOW_SIZE, "jours")
print("Prediction : J+1")

print("\n===== TOP 15 STATIONS =====")
if not metadata_df.empty:
    print(metadata_df["sensor_name"].value_counts().head(15))
else:
    print("Aucune sequence valide.")

print("\nFichiers sauvegardes :")
print("data/processed/cnn_lstm_sequences.npz")
print("results/cnn_lstm_sequences_metadata.csv")
