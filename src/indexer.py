from __future__ import annotations

from typing import Any

from hashtable import HashTable


def build_product_index(records: list[dict[str, Any]], capacity: int = 200003) -> HashTable:
    """
    Build a hash index:
        product_id -> list of review records
    """
    table = HashTable(capacity=capacity)

    for record in records:
        product_id = record.get("product_id")
        if product_id is not None:
            table.append_to_list(product_id, record)

    return table


def build_user_index(records: list[dict[str, Any]], capacity: int = 300007) -> HashTable:
    """
    Build a hash index:
        user_id -> list of review records
    """
    table = HashTable(capacity=capacity)

    for record in records:
        user_id = record.get("user_id")
        if user_id is not None:
            table.append_to_list(user_id, record)

    return table


def build_score_frequency(records: list[dict[str, Any]], capacity: int = 101) -> HashTable:
    """
    Build a frequency table:
        score -> count
    """
    table = HashTable(capacity=capacity)

    for record in records:
        score = record.get("score")
        if score is not None:
            table.increment(score)

    return table


def build_product_review_counts(records: list[dict[str, Any]], capacity: int = 200003) -> HashTable:
    """
    Build a frequency table:
        product_id -> review count
    """
    table = HashTable(capacity=capacity)

    for record in records:
        product_id = record.get("product_id")
        if product_id is not None:
            table.increment(product_id)

    return table


def build_user_review_counts(records: list[dict[str, Any]], capacity: int = 300007) -> HashTable:
    """
    Build a frequency table:
        user_id -> review count
    """
    table = HashTable(capacity=capacity)

    for record in records:
        user_id = record.get("user_id")
        if user_id is not None:
            table.increment(user_id)

    return table


def hash_items_to_sorted_list(table: HashTable, reverse: bool = True) -> list[tuple[Any, Any]]:
    """
    Convert hash table items to a sorted list by value.

    Useful for frequency tables such as:
    - product_id -> count
    - user_id -> count
    - score -> count
    """
    return sorted(table.items(), key=lambda x: x[1], reverse=reverse)


def top_k_from_frequency_table(table: HashTable, k: int = 10) -> list[tuple[Any, Any]]:
    """
    Return the top-k (key, count) pairs from a frequency table.
    """
    sorted_items = hash_items_to_sorted_list(table, reverse=True)
    return sorted_items[:k]


def get_reviews_by_product(product_index: HashTable, product_id: str) -> list[dict[str, Any]]:
    """
    Retrieve all reviews for a given product_id.
    """
    reviews = product_index.get(product_id, default=[])
    return reviews if reviews is not None else []


def get_reviews_by_user(user_index: HashTable, user_id: str) -> list[dict[str, Any]]:
    """
    Retrieve all reviews for a given user_id.
    """
    reviews = user_index.get(user_id, default=[])
    return reviews if reviews is not None else []


def summarize_index(table: HashTable, name: str) -> None:
    """
    Print a short summary of a hash-based index or frequency table.
    """
    print("=" * 60)
    print(f"{name.upper()} SUMMARY")
    print("=" * 60)
    print(f"Stored keys: {len(table)}")
    print(f"Capacity: {table.capacity}")
    print(f"Load factor: {table.load_factor():.4f}")
    print(f"Collision count: {table.collision_count}")
    print(f"Max chain length: {table.max_chain_length()}")


def _demo() -> None:
    """
    Small local demo using toy records.
    """
    sample_records = [
        {"product_id": "P1", "user_id": "U1", "score": 5, "text": "Great"},
        {"product_id": "P1", "user_id": "U2", "score": 4, "text": "Good"},
        {"product_id": "P2", "user_id": "U1", "score": 5, "text": "Nice"},
        {"product_id": "P3", "user_id": "U3", "score": 2, "text": "Bad"},
        {"product_id": "P1", "user_id": "U1", "score": 5, "text": "Loved it"},
    ]

    product_index = build_product_index(sample_records, capacity=11)
    user_index = build_user_index(sample_records, capacity=11)
    score_freq = build_score_frequency(sample_records, capacity=11)
    product_counts = build_product_review_counts(sample_records, capacity=11)
    user_counts = build_user_review_counts(sample_records, capacity=11)

    summarize_index(product_index, "product index")
    summarize_index(user_index, "user index")
    summarize_index(score_freq, "score frequency")

    print("\nTop products by review count:")
    print(top_k_from_frequency_table(product_counts, k=3))

    print("\nTop users by review count:")
    print(top_k_from_frequency_table(user_counts, k=3))

    print("\nReviews for product P1:")
    print(get_reviews_by_product(product_index, "P1"))

    print("\nReviews for user U1:")
    print(get_reviews_by_user(user_index, "U1"))


if __name__ == "__main__":
    _demo()