from __future__ import annotations

import random
import time
from pathlib import Path
from typing import Any

import pandas as pd
import matplotlib.pyplot as plt

from preprocess import preprocess_dataset, dataframe_to_records
from indexer import (
    build_product_index,
    build_user_index,
    build_score_frequency,
    build_product_review_counts,
    build_user_review_counts,
)


# ============================================================
# 1. Output directory
# ============================================================

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# 2. Record sampling helper
# ============================================================

def sample_records(records: list[dict[str, Any]], n: int) -> list[dict[str, Any]]:
    """
    Return the first n records for reproducible benchmarking.
    """
    return records[:n]


# ============================================================
# 3. Build-time benchmarks
# ============================================================

def benchmark_build_product_index(records: list[dict[str, Any]]) -> dict[str, Any]:
    start = time.perf_counter()
    table = build_product_index(records)
    elapsed = time.perf_counter() - start

    return {
        "task": "build_product_index",
        "num_records": len(records),
        "stored_keys": len(table),
        "time_seconds": elapsed,
        "load_factor": table.load_factor(),
        "collision_count": table.collision_count,
        "max_chain_length": table.max_chain_length(),
    }


def benchmark_build_user_index(records: list[dict[str, Any]]) -> dict[str, Any]:
    start = time.perf_counter()
    table = build_user_index(records)
    elapsed = time.perf_counter() - start

    return {
        "task": "build_user_index",
        "num_records": len(records),
        "stored_keys": len(table),
        "time_seconds": elapsed,
        "load_factor": table.load_factor(),
        "collision_count": table.collision_count,
        "max_chain_length": table.max_chain_length(),
    }


def benchmark_build_product_counts(records: list[dict[str, Any]]) -> dict[str, Any]:
    start = time.perf_counter()
    table = build_product_review_counts(records)
    elapsed = time.perf_counter() - start

    return {
        "task": "build_product_review_counts",
        "num_records": len(records),
        "stored_keys": len(table),
        "time_seconds": elapsed,
        "load_factor": table.load_factor(),
        "collision_count": table.collision_count,
        "max_chain_length": table.max_chain_length(),
    }


def benchmark_build_user_counts(records: list[dict[str, Any]]) -> dict[str, Any]:
    start = time.perf_counter()
    table = build_user_review_counts(records)
    elapsed = time.perf_counter() - start

    return {
        "task": "build_user_review_counts",
        "num_records": len(records),
        "stored_keys": len(table),
        "time_seconds": elapsed,
        "load_factor": table.load_factor(),
        "collision_count": table.collision_count,
        "max_chain_length": table.max_chain_length(),
    }


def benchmark_build_score_frequency(records: list[dict[str, Any]]) -> dict[str, Any]:
    start = time.perf_counter()
    table = build_score_frequency(records)
    elapsed = time.perf_counter() - start

    return {
        "task": "build_score_frequency",
        "num_records": len(records),
        "stored_keys": len(table),
        "time_seconds": elapsed,
        "load_factor": table.load_factor(),
        "collision_count": table.collision_count,
        "max_chain_length": table.max_chain_length(),
    }


# ============================================================
# 4. Lookup-time benchmarks
# ============================================================

def benchmark_lookup_product_index(
    records: list[dict[str, Any]],
    num_queries: int = 1000
) -> dict[str, Any]:
    table = build_product_index(records)

    product_ids = list({r["product_id"] for r in records if r.get("product_id") is not None})
    if not product_ids:
        raise ValueError("No product_id values available for lookup benchmark.")

    query_keys = random.sample(product_ids, min(num_queries, len(product_ids)))

    start = time.perf_counter()
    total_found = 0
    for key in query_keys:
        reviews = table.get(key, [])
        total_found += len(reviews)
    elapsed = time.perf_counter() - start

    return {
        "task": "lookup_product_index",
        "num_records": len(records),
        "num_queries": len(query_keys),
        "time_seconds": elapsed,
        "avg_time_per_query_ms": (elapsed / len(query_keys)) * 1000,
        "total_found_reviews": total_found,
    }


def benchmark_lookup_user_index(
    records: list[dict[str, Any]],
    num_queries: int = 1000
) -> dict[str, Any]:
    table = build_user_index(records)

    user_ids = list({r["user_id"] for r in records if r.get("user_id") is not None})
    if not user_ids:
        raise ValueError("No user_id values available for lookup benchmark.")

    query_keys = random.sample(user_ids, min(num_queries, len(user_ids)))

    start = time.perf_counter()
    total_found = 0
    for key in query_keys:
        reviews = table.get(key, [])
        total_found += len(reviews)
    elapsed = time.perf_counter() - start

    return {
        "task": "lookup_user_index",
        "num_records": len(records),
        "num_queries": len(query_keys),
        "time_seconds": elapsed,
        "avg_time_per_query_ms": (elapsed / len(query_keys)) * 1000,
        "total_found_reviews": total_found,
    }


# ============================================================
# 5. Output helpers
# ============================================================

def print_result(result: dict[str, Any]) -> None:
    print("=" * 60)
    print(result["task"].upper())
    print("=" * 60)
    for key, value in result.items():
        if key != "task":
            print(f"{key}: {value}")


def results_to_dataframe(results: list[dict[str, Any]]) -> pd.DataFrame:
    """
    Convert benchmark result dictionaries into a DataFrame.
    """
    df = pd.DataFrame(results)

    preferred_cols = [
        "task",
        "num_records",
        "stored_keys",
        "num_queries",
        "time_seconds",
        "avg_time_per_query_ms",
        "load_factor",
        "collision_count",
        "max_chain_length",
        "total_found_reviews",
    ]

    existing_cols = [col for col in preferred_cols if col in df.columns]
    remaining_cols = [col for col in df.columns if col not in existing_cols]
    return df[existing_cols + remaining_cols]


def save_results_table(df: pd.DataFrame, filename: str = "benchmark_results.csv") -> Path:
    """
    Save the benchmark results table as CSV.
    """
    output_path = OUTPUT_DIR / filename
    df.to_csv(output_path, index=False)
    return output_path


# ============================================================
# 6. Plot helpers
# ============================================================

def plot_build_time(df: pd.DataFrame) -> Path:
    """
    Plot build-time benchmarks as a line chart.
    """
    build_tasks = [
        "build_product_index",
        "build_user_index",
        "build_product_review_counts",
        "build_user_review_counts",
        "build_score_frequency",
    ]
    plot_df = df[df["task"].isin(build_tasks)].copy()

    plt.figure(figsize=(10, 6))
    for task in build_tasks:
        task_df = plot_df[plot_df["task"] == task].sort_values("num_records")
        if not task_df.empty:
            plt.plot(task_df["num_records"], task_df["time_seconds"], marker="o", label=task)

    plt.xlabel("Number of Records")
    plt.ylabel("Build Time (seconds)")
    plt.title("Build Time vs Dataset Size")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    output_path = OUTPUT_DIR / "build_time_vs_size.png"
    plt.savefig(output_path, dpi=200)
    plt.close()
    return output_path


def plot_lookup_time(df: pd.DataFrame) -> Path:
    """
    Plot lookup-time benchmarks as a line chart.
    """
    lookup_tasks = [
        "lookup_product_index",
        "lookup_user_index",
    ]
    plot_df = df[df["task"].isin(lookup_tasks)].copy()

    plt.figure(figsize=(10, 6))
    for task in lookup_tasks:
        task_df = plot_df[plot_df["task"] == task].sort_values("num_records")
        if not task_df.empty:
            plt.plot(
                task_df["num_records"],
                task_df["avg_time_per_query_ms"],
                marker="o",
                label=task
            )

    plt.xlabel("Number of Records")
    plt.ylabel("Average Time per Query (ms)")
    plt.title("Lookup Time vs Dataset Size")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    output_path = OUTPUT_DIR / "lookup_time_vs_size.png"
    plt.savefig(output_path, dpi=200)
    plt.close()
    return output_path


def plot_load_factor(df: pd.DataFrame) -> Path:
    """
    Plot load factor for build tasks.
    """
    build_tasks = [
        "build_product_index",
        "build_user_index",
        "build_product_review_counts",
        "build_user_review_counts",
        "build_score_frequency",
    ]
    plot_df = df[df["task"].isin(build_tasks) & df["load_factor"].notna()].copy()

    plt.figure(figsize=(10, 6))
    for task in build_tasks:
        task_df = plot_df[plot_df["task"] == task].sort_values("num_records")
        if not task_df.empty:
            plt.plot(task_df["num_records"], task_df["load_factor"], marker="o", label=task)

    plt.xlabel("Number of Records")
    plt.ylabel("Load Factor")
    plt.title("Load Factor vs Dataset Size")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    output_path = OUTPUT_DIR / "load_factor_vs_size.png"
    plt.savefig(output_path, dpi=200)
    plt.close()
    return output_path


# ============================================================
# 7. Main benchmark workflow
# ============================================================

def main() -> None:
    print("=" * 60)
    print("BENCHMARKING HASH-BASED AMAZON REVIEW APPLICATION")
    print("=" * 60)

    cleaned_df, _ = preprocess_dataset()
    records = dataframe_to_records(cleaned_df)

    sizes = [1000, 10000, 50000, 100000, len(records)]
    all_results: list[dict[str, Any]] = []

    for size in sizes:
        print("\n" + "#" * 60)
        print(f"DATA SIZE: {size}")
        print("#" * 60)

        subset = sample_records(records, size)

        results = [
            benchmark_build_product_index(subset),
            benchmark_build_user_index(subset),
            benchmark_build_product_counts(subset),
            benchmark_build_user_counts(subset),
            benchmark_build_score_frequency(subset),
            benchmark_lookup_product_index(subset, num_queries=1000),
            benchmark_lookup_user_index(subset, num_queries=1000),
        ]

        all_results.extend(results)

        for result in results:
            print()
            print_result(result)

    # --------------------------------------------------------
    # 8. Convert results to table
    # --------------------------------------------------------
    df = results_to_dataframe(all_results)

    print("\n" + "=" * 60)
    print("BENCHMARK RESULTS TABLE")
    print("=" * 60)
    print(df.to_string(index=False))

    csv_path = save_results_table(df)
    print(f"\nSaved benchmark table to: {csv_path}")

    # --------------------------------------------------------
    # 9. Save plots
    # --------------------------------------------------------
    build_plot = plot_build_time(df)
    lookup_plot = plot_lookup_time(df)
    load_plot = plot_load_factor(df)

    print(f"Saved build-time plot to: {build_plot}")
    print(f"Saved lookup-time plot to: {lookup_plot}")
    print(f"Saved load-factor plot to: {load_plot}")


# ============================================================
# 8. Script entry
# ============================================================

if __name__ == "__main__":
    main()