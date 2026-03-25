from __future__ import annotations

import random
import time
from typing import Any

from preprocess import preprocess_dataset, dataframe_to_records
from indexer import (
    build_product_index,
    build_user_index,
    build_score_frequency,
    build_product_review_counts,
    build_user_review_counts,
)


# ============================================================
# 1. Record sampling helper
# ============================================================

def sample_records(records: list[dict[str, Any]], n: int) -> list[dict[str, Any]]:
    """
    Return the first n records for reproducible benchmarking.
    """
    return records[:n]


# ============================================================
# 2. Build-time benchmarks
# ============================================================

def benchmark_build_product_index(records: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Benchmark building:
        product_id -> list of review records
    """
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
    """
    Benchmark building:
        user_id -> list of review records
    """
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
    """
    Benchmark building:
        product_id -> review count
    """
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
    """
    Benchmark building:
        user_id -> review count
    """
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
    """
    Benchmark building:
        score -> count
    """
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
# 3. Lookup-time benchmarks
# ============================================================

def benchmark_lookup_product_index(
    records: list[dict[str, Any]],
    num_queries: int = 1000
) -> dict[str, Any]:
    """
    Benchmark lookup performance on the product index.
    """
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
    """
    Benchmark lookup performance on the user index.
    """
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
# 4. Output helper
# ============================================================

def print_result(result: dict[str, Any]) -> None:
    """
    Print one benchmark result block.
    """
    print("=" * 60)
    print(result["task"].upper())
    print("=" * 60)
    for key, value in result.items():
        if key != "task":
            print(f"{key}: {value}")


# ============================================================
# 5. Main benchmark workflow
# ============================================================

def main() -> None:
    """
    Main driver for benchmarking the hash-based Amazon review application.
    """
    print("=" * 60)
    print("BENCHMARKING HASH-BASED AMAZON REVIEW APPLICATION")
    print("=" * 60)

    cleaned_df, _ = preprocess_dataset()
    records = dataframe_to_records(cleaned_df)

    sizes = [1000, 10000, 50000, 100000, len(records)]

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

        for result in results:
            print()
            print_result(result)


# ============================================================
# 6. Script entry
# ============================================================

if __name__ == "__main__":
    main()