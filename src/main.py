from __future__ import annotations

from preprocess import preprocess_dataset, dataframe_to_records, print_quality_report
from indexer import (
    build_product_index,
    build_user_index,
    build_score_frequency,
    build_product_review_counts,
    build_user_review_counts,
    summarize_index,
    top_k_from_frequency_table,
    get_reviews_by_product,
    get_reviews_by_user,
)


# ============================================================
# 1. Output helper: print top-k results
# ============================================================

def print_top_k(title: str, items: list[tuple], k: int = 10) -> None:
    """
    Print a top-k ranking list.

    Current implementation:
    - Print a title block
    - Print the first k items in ranking order
    """
    print("=" * 60)
    print(title.upper())
    print("=" * 60)

    for i, (key, value) in enumerate(items[:k], start=1):
        print(f"{i}. {key} -> {value}")


# ============================================================
# 2. Output helper: print score distribution
# ============================================================

def print_score_distribution(score_freq) -> None:
    """
    Print the score frequency distribution.

    Current implementation:
    - Get all (score, count) pairs
    - Sort by score
    - Print them clearly
    """
    print("=" * 60)
    print("SCORE DISTRIBUTION")
    print("=" * 60)

    items = sorted(score_freq.items(), key=lambda x: x[0])
    for score, count in items:
        print(f"Score {score}: {count}")


# ============================================================
# 3. Output helper: print sample reviews
# ============================================================

def print_review_samples(title: str, reviews: list[dict], limit: int = 3) -> None:
    """
    Print a small sample of review records.

    Current implementation:
    - Print a title block
    - Print at most `limit` sample reviews
    - Show selected fields only
    - Truncate long text for readability
    """
    print("=" * 60)
    print(title.upper())
    print("=" * 60)

    if not reviews:
        print("No reviews found.")
        return

    print(f"Total reviews found: {len(reviews)}")
    print()

    for i, review in enumerate(reviews[:limit], start=1):
        product_id = review.get("product_id")
        user_id = review.get("user_id")
        score = review.get("score")
        summary = review.get("summary")
        text = review.get("text")

        short_text = text[:200] + "..." if text and len(text) > 200 else text

        print(f"[Review {i}]")
        print(f"product_id: {product_id}")
        print(f"user_id: {user_id}")
        print(f"score: {score}")
        print(f"summary: {summary}")
        print(f"text: {short_text}")
        print("-" * 40)


# ============================================================
# 4. Main application workflow
# ============================================================

def main() -> None:
    """
    Main driver for the Amazon hashing project demo.

    Current implementation:
    1. Preprocess dataset
    2. Print preprocessing report
    3. Convert dataframe to records
    4. Build indexes and frequency tables
    5. Print summaries
    6. Print top-k results
    7. Query one real product and one real user
    """
    print("=" * 60)
    print("AMAZON HASHING PROJECT DEMO")
    print("=" * 60)

    # --------------------------------------------------------
    # Step 1: preprocess dataset
    # --------------------------------------------------------
    cleaned_df, quality_report = preprocess_dataset()
    print_quality_report(quality_report)

    # --------------------------------------------------------
    # Step 2: convert dataframe into record dictionaries
    # --------------------------------------------------------
    records = dataframe_to_records(cleaned_df)
    print(f"\nConverted cleaned dataframe into {len(records)} records.")

    # --------------------------------------------------------
    # Step 3: build hash-based structures
    # --------------------------------------------------------
    print("\nBuilding hash-based data structures...")

    product_index = build_product_index(records)
    user_index = build_user_index(records)
    score_freq = build_score_frequency(records)
    product_counts = build_product_review_counts(records)
    user_counts = build_user_review_counts(records)

    print("Done.")

    # --------------------------------------------------------
    # Step 4: print structure summaries
    # --------------------------------------------------------
    print()
    summarize_index(product_index, "product index")
    summarize_index(user_index, "user index")
    summarize_index(score_freq, "score frequency")

    # --------------------------------------------------------
    # Step 5: compute and print top-k frequency results
    # --------------------------------------------------------
    top_products = top_k_from_frequency_table(product_counts, k=10)
    top_users = top_k_from_frequency_table(user_counts, k=10)

    print()
    print_top_k("Top 10 most reviewed products", top_products, k=10)

    print()
    print_top_k("Top 10 most active users", top_users, k=10)

    print()
    print_score_distribution(score_freq)

    # --------------------------------------------------------
    # Step 6: query one real product and one real user
    # --------------------------------------------------------
    if top_products:
        sample_product_id = top_products[0][0]
        product_reviews = get_reviews_by_product(product_index, sample_product_id)

        print()
        print_review_samples(
            f"Sample reviews for product {sample_product_id}",
            product_reviews,
            limit=3
        )

    if top_users:
        sample_user_id = top_users[0][0]
        user_reviews = get_reviews_by_user(user_index, sample_user_id)

        print()
        print_review_samples(
            f"Sample reviews by user {sample_user_id}",
            user_reviews,
            limit=3
        )


# ============================================================
# 5. Script entry
# ============================================================

if __name__ == "__main__":
    main()