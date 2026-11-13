import os
import numpy as np
import pandas as pd

# 1. Charger les sequences
data = np.load("data/processed/cnn_lstm_sequences.npz")

X = data["X"]
y = data["y"]

# 2. Charger les metadonnees
metadata = pd.read_csv(
    "results/cnn_lstm_sequences_metadata.csv"
)

metadata["target_date"] = pd.to_datetime(
    metadata["target_date"]
)

# 3. Verifier la correspondance
if len(X) != len(metadata) or len(y) != len(metadata):
    raise ValueError("Les sequences et metadonnees ne correspondent pas.")

# 4. Recuperer les dates uniques
unique_dates = np.sort(
    metadata["target_date"].unique()
)

n_dates = len(unique_dates)

# 5. Definir les limites chronologiques
train_end = int(n_dates * 0.70)
val_end = int(n_dates * 0.85)

train_cutoff = unique_dates[train_end]
test_cutoff = unique_dates[val_end]

# 6. Creer les masques
dates = metadata["target_date"]

train_mask = dates < train_cutoff

val_mask = (
    (dates >= train_cutoff) &
    (dates < test_cutoff)
)

test_mask = dates >= test_cutoff

# 7. Separer les donnees
X_train, y_train = X[train_mask], y[train_mask]
X_val, y_val = X[val_mask], y[val_mask]
X_test, y_test = X[test_mask], y[test_mask]

# 8. Verifier que les ensembles ne sont pas vides
if min(len(X_train), len(X_val), len(X_test)) == 0:
    raise ValueError("Un des ensembles est vide.")

# 9. Afficher les resultats
print("\n===== DECOUPAGE TEMPOREL =====")

print("\nNombre de dates uniques :", n_dates)

print("\nTRAIN")
print("Nombre de sequences :", len(X_train))
print("Premiere date :", dates[train_mask].min())
print("Derniere date :", dates[train_mask].max())

print("\nVALIDATION")
print("Nombre de sequences :", len(X_val))
print("Premiere date :", dates[val_mask].min())
print("Derniere date :", dates[val_mask].max())

print("\nTEST")
print("Nombre de sequences :", len(X_test))
print("Premiere date :", dates[test_mask].min())
print("Derniere date :", dates[test_mask].max())

print("\n===== DIMENSIONS =====")
print("X_train :", X_train.shape)
print("y_train :", y_train.shape)
print("X_val :", X_val.shape)
print("y_val :", y_val.shape)
print("X_test :", X_test.shape)
print("y_test :", y_test.shape)

# 10. Sauvegarder les ensembles
os.makedirs("data/processed", exist_ok=True)

np.savez_compressed(
    "data/processed/cnn_lstm_splits.npz",
    X_train=X_train,
    y_train=y_train,
    X_val=X_val,
    y_val=y_val,
    X_test=X_test,
    y_test=y_test
)

# 11. Sauvegarder le resume des dates
summary = pd.DataFrame({
    "set": ["Train", "Validation", "Test"],
    "sequences": [
        len(X_train),
        len(X_val),
        len(X_test)
    ],
    "first_date": [
        dates[train_mask].min(),
        dates[val_mask].min(),
        dates[test_mask].min()
    ],
    "last_date": [
        dates[train_mask].max(),
        dates[val_mask].max(),
        dates[test_mask].max()
    ]
})

summary.to_csv(
    "results/temporal_split_summary.csv",
    index=False
)

print("\nFichier sauvegarde :")
print("data/processed/cnn_lstm_splits.npz")
print("results/temporal_split_summary.csv")
