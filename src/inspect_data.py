from pathlib import Path
import pandas as pd

# Path to the raw data directory
DATA_DIR = Path("data/raw")

# Find all CSV files
csv_files = list(DATA_DIR.glob("*.csv"))

if not csv_files:
    print("No CSV files found in data/raw!")
else:
    print(f"Found {len(csv_files)} CSV files")

    for file in sorted(csv_files):
        print("\n" + "=" * 60)
        print(f"FILE: {file.name}")

        try:
            df = pd.read_csv(file)

            print(f"Rows: {df.shape[0]}")
            print(f"Columns: {df.shape[1]}")

            print("\nColumn names:")
            print(df.columns.tolist())

            print("\nData types:")
            print(df.dtypes)

            print("\nMissing values (%):")
            missing = (df.isnull().mean() * 100).round(2)
            print(missing[missing > 0].sort_values(ascending=False))

            print("\nFirst 3 rows:")
            print(df.head(3).to_string(index=False))

        except Exception as error:
            print(f"Error reading {file.name}: {error}")
