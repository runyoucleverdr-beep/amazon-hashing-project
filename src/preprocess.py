from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import pandas as pd


RAW_DATA_PATH = Path("data/Reviews.csv")


COLUMN_RENAME_MAP = {
    "Id": "id",
    "ProductId": "product_id",
    "UserId": "user_id",
    "ProfileName": "profile_name",
    "HelpfulnessNumerator": "helpfulness_numerator",
    "HelpfulnessDenominator": "helpfulness_denominator",
    "Score": "score",
    "Time": "time",
    "Summary": "summary",
    "Text": "text",
}


STRING_COLUMNS = [
    "product_id",
    "user_id",
    "profile_name",
    "summary",
    "text",
]


NUMERIC_COLUMNS = [
    "id",
    "helpfulness_numerator",
    "helpfulness_denominator",
    "score",
    "time",
]


def normalize_text(value: Any) -> str | None:
    """
    Normalize text fields for cleaner downstream indexing and analysis.

    Rules:
    - keep missing values as None
    - convert to string if needed
    - strip leading/trailing whitespace
    - collapse repeated whitespace into a single space
    - convert empty strings to None
    """
    if pd.isna(value):
        return None

    text = str(value).strip()
    text = re.sub(r"\s+", " ", text)

    if text == "":
        return None

    return text


def load_raw_dataset(path: str | Path = RAW_DATA_PATH) -> pd.DataFrame:
    """
    Load the raw CSV dataset.
    """
    csv_path = Path(path)
    if not csv_path.exists():
        raise FileNotFoundError(f"Dataset file not found: {csv_path}")

    return pd.read_csv(csv_path)


def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Rename dataset columns to snake_case for easier processing.
    """
    return df.rename(columns=COLUMN_RENAME_MAP)


def clean_string_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and normalize selected string columns.
    """
    for col in STRING_COLUMNS:
        if col in df.columns:
            df[col] = df[col].apply(normalize_text)
    return df


def convert_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Force numeric columns into numeric dtype.
    Invalid values become NaN, then are converted to nullable integer type where possible.
    """
    for col in NUMERIC_COLUMNS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Keep integer-like columns as nullable integers for cleaner reporting
    for col in ["id", "helpfulness_numerator", "helpfulness_denominator", "time"]:
        if col in df.columns:
            df[col] = df[col].astype("Int64")

    if "score" in df.columns:
        df["score"] = df["score"].astype("Int64")

    return df


def add_derived_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add a few helpful derived fields for later analysis and hashing tasks.
    """
    if "summary" in df.columns:
        df["summary_length"] = df["summary"].apply(lambda x: len(x) if x is not None else 0)

    if "text" in df.columns:
        df["text_length"] = df["text"].apply(lambda x: len(x) if x is not None else 0)

    if {"helpfulness_numerator", "helpfulness_denominator"}.issubset(df.columns):
        def helpfulness_ratio(row: pd.Series) -> float | None:
            num = row["helpfulness_numerator"]
            den = row["helpfulness_denominator"]

            if pd.isna(num) or pd.isna(den) or den == 0:
                return None
            return float(num) / float(den)

        df["helpfulness_ratio"] = df.apply(helpfulness_ratio, axis=1)

    return df


def collect_data_quality_report(df: pd.DataFrame) -> dict[str, Any]:
    """
    Create a compact data-quality summary for later reporting and debugging.
    """
    report: dict[str, Any] = {
        "row_count": len(df),
        "column_count": len(df.columns),
        "missing_counts": df.isnull().sum().to_dict(),
        "missing_product_id_count": int(df["product_id"].isnull().sum()) if "product_id" in df.columns else None,
        "missing_user_id_count": int(df["user_id"].isnull().sum()) if "user_id" in df.columns else None,
        "missing_summary_count": int(df["summary"].isnull().sum()) if "summary" in df.columns else None,
        "missing_text_count": int(df["text"].isnull().sum()) if "text" in df.columns else None,
        "unique_product_count": int(df["product_id"].nunique(dropna=True)) if "product_id" in df.columns else None,
        "unique_user_count": int(df["user_id"].nunique(dropna=True)) if "user_id" in df.columns else None,
        "score_distribution": (
            df["score"].value_counts(dropna=False).sort_index().to_dict()
            if "score" in df.columns else {}
        ),
    }
    return report


def preprocess_dataset(path: str | Path = RAW_DATA_PATH) -> tuple[pd.DataFrame, dict[str, Any]]:
    """
    Full preprocessing pipeline:
    1. load raw dataset
    2. rename columns
    3. clean strings
    4. convert numeric columns
    5. add derived columns
    6. return cleaned DataFrame + quality report
    """
    df = load_raw_dataset(path)
    df = rename_columns(df)
    df = clean_string_columns(df)
    df = convert_numeric_columns(df)
    df = add_derived_columns(df)

    report = collect_data_quality_report(df)
    return df, report


def dataframe_to_records(df: pd.DataFrame) -> list[dict[str, Any]]:
    """
    Convert cleaned DataFrame to a list of dictionaries for hash-table-based processing.
    """
    return df.to_dict(orient="records")


def print_quality_report(report: dict[str, Any]) -> None:
    """
    Print the most important quality indicators.
    """
    print("=" * 60)
    print("PREPROCESSING REPORT")
    print("=" * 60)
    print(f"Rows: {report['row_count']}")
    print(f"Columns: {report['column_count']}")
    print(f"Unique products: {report['unique_product_count']}")
    print(f"Unique users: {report['unique_user_count']}")
    print(f"Missing product_id: {report['missing_product_id_count']}")
    print(f"Missing user_id: {report['missing_user_id_count']}")
    print(f"Missing summary: {report['missing_summary_count']}")
    print(f"Missing text: {report['missing_text_count']}")

    print("\nScore distribution:")
    for score, count in report["score_distribution"].items():
        print(f"  {score}: {count}")

    print("\nTop missing-value columns:")
    missing_counts = report["missing_counts"]
    top_missing = sorted(missing_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    for col, count in top_missing:
        print(f"  {col}: {count}")


if __name__ == "__main__":
    cleaned_df, quality_report = preprocess_dataset()
    print_quality_report(quality_report)

    print("\nSample cleaned rows:")
    print(cleaned_df.head(3))

    records = dataframe_to_records(cleaned_df)
    print(f"\nConverted to {len(records)} records.")