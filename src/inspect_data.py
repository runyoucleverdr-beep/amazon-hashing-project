import pandas as pd
from pathlib import Path


def inspect_dataset(path: str, sample_rows: int = 5) -> None:
    csv_path = Path(path)

    if not csv_path.exists():
        print(f"Error: file not found -> {csv_path}")
        return

    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    print("=" * 60)
    print("BASIC INFO")
    print("=" * 60)
    print(f"File: {csv_path}")
    print(f"Number of rows: {len(df)}")
    print(f"Number of columns: {len(df.columns)}")

    print("\n" + "=" * 60)
    print("COLUMN NAMES")
    print("=" * 60)
    for i, col in enumerate(df.columns, start=1):
        print(f"{i}. {col}")

    print("\n" + "=" * 60)
    print("DATA TYPES")
    print("=" * 60)
    print(df.dtypes)

    print("\n" + "=" * 60)
    print("MISSING VALUES BY COLUMN")
    print("=" * 60)
    missing_counts = df.isnull().sum()
    missing_percent = (missing_counts / len(df) * 100).round(2)
    missing_df = pd.DataFrame({
        "missing_count": missing_counts,
        "missing_percent": missing_percent
    }).sort_values(by="missing_count", ascending=False)
    print(missing_df)

    print("\n" + "=" * 60)
    print(f"SAMPLE ROWS (first {sample_rows})")
    print("=" * 60)
    print(df.head(sample_rows))

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)


if __name__ == "__main__":
    inspect_dataset("data/amazon_reviews.csv")