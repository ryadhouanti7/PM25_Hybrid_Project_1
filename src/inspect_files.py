import pandas as pd
from pathlib import Path

data_folder = Path("data/raw")

for file_path in sorted(data_folder.glob("*.csv")):
    print("\n" + "=" * 60)
    print("FICHIER :", file_path.name)
    print("=" * 60)

    try:
        df = pd.read_csv(file_path)

        print("\nDimensions :")
        print("Lignes :", df.shape[0])
        print("Colonnes :", df.shape[1])

        print("\nNoms des colonnes :")
        print(df.columns.tolist())

        print("\nPremières lignes :")
        print(df.head(3).to_string(index=False))

        print("\nTypes de données :")
        print(df.dtypes.to_string())

    except Exception as error:
        print("Erreur de lecture :", error)