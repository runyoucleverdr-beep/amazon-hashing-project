from __future__ import annotations

from dataclasses import dataclass
from typing import Any


# ============================================================
# 1. Node structure for separate chaining
# ============================================================

@dataclass
class HashNode:
    """
    A single node used in one bucket chain.

    Attributes:
    - key: the hash key
    - value: the value associated with the key
    - next: pointer to the next node in the same bucket chain
    """
    key: Any
    value: Any
    next: "HashNode | None" = None


# ============================================================
# 2. Main hash table class
# ============================================================

class HashTable:
    """
    A simple hash table using separate chaining.

    Planned features:
    - insert(key, value)
    - get(key)
    - contains(key)
    - increment(key, amount)
    - append_to_list(key, item)
    - keys()
    - values()
    - items()
    - load factor
    - bucket length statistics
    - collision statistics
    """

    def __init__(self, capacity: int = 200003) -> None:
        """
        Initialize the hash table.

        TODO:
        - Store the table capacity
        - Create the bucket array with empty buckets
        - Initialize size counter
        - Initialize collision counter
        """
        pass

    def _hash(self, key: Any) -> int:
        """
        Compute the bucket index for the given key.

        TODO:
        - Use Python's built-in hash()
        - Map the raw hash value into the valid bucket index range
        """
        pass

    def insert(self, key: Any, value: Any) -> None:
        """
        Insert or update a key-value pair.

        Expected behavior:
        - If the bucket is empty, insert a new node
        - If the key already exists in the chain, overwrite its value
        - If the key does not exist but the bucket is occupied, append a new node
        - Update size when a new key is added
        - Update collision count when insertion happens in a non-empty bucket

        TODO:
        - Find target bucket
        - Traverse chain if needed
        - Update existing key or append a new node
        """
        pass

    def get(self, key: Any, default: Any = None) -> Any:
        """
        Retrieve the value associated with key.

        Expected behavior:
        - Search the target bucket chain
        - Return the stored value if found
        - Return default if the key does not exist

        TODO:
        - Compute bucket index
        - Traverse linked nodes in that bucket
        - Compare node keys with target key
        """
        pass

    def contains(self, key: Any) -> bool:
        """
        Check whether the key exists in the hash table.

        Expected behavior:
        - Return True if the key is found
        - Return False otherwise

        TODO:
        - Reuse get() or implement explicit traversal
        """
        pass

    def increment(self, key: Any, amount: int = 1) -> None:
        """
        Increment a numeric value stored at key.

        Expected behavior:
        - If key does not exist, initialize it with amount
        - If key already exists, increase its value by amount

        Typical use case:
        - frequency counting, e.g. score -> count

        TODO:
        - Retrieve current value
        - Insert new value or updated value
        """
        pass

    def append_to_list(self, key: Any, item: Any) -> None:
        """
        Append an item to a list stored at key.

        Expected behavior:
        - If key does not exist, initialize the value as a new list [item]
        - If key exists, append item to the existing list

        Typical use case:
        - product_id -> list of review records
        - user_id -> list of review records

        TODO:
        - Retrieve current value
        - Create new list or append to existing list
        """
        pass

    def keys(self) -> list[Any]:
        """
        Return all keys stored in the hash table.

        Expected behavior:
        - Traverse every bucket
        - Traverse every node in each bucket chain
        - Collect all keys into a list

        TODO:
        - Iterate over all buckets
        - Traverse linked lists
        """
        pass

    def values(self) -> list[Any]:
        """
        Return all values stored in the hash table.

        Expected behavior:
        - Traverse every bucket and chain
        - Collect all stored values into a list

        TODO:
        - Iterate over all buckets
        - Traverse linked lists
        """
        pass

    def items(self) -> list[tuple[Any, Any]]:
        """
        Return all key-value pairs stored in the hash table.

        Expected behavior:
        - Traverse every bucket and chain
        - Collect all (key, value) pairs into a list

        TODO:
        - Iterate over all buckets
        - Traverse linked lists
        """
        pass

    def load_factor(self) -> float:
        """
        Compute the current load factor.

        Common definition:
        - number of stored keys / number of buckets

        TODO:
        - Return size / capacity
        """
        pass

    def bucket_lengths(self) -> list[int]:
        """
        Compute the chain length of each bucket.

        Expected behavior:
        - For every bucket, count how many nodes are stored in its chain
        - Return a list of chain lengths

        Typical use case:
        - collision analysis
        - chain length distribution
        - max chain length calculation

        TODO:
        - Iterate through all buckets
        - Count linked nodes in each chain
        """
        pass

    def max_chain_length(self) -> int:
        """
        Return the maximum chain length among all buckets.

        Expected behavior:
        - Compute all bucket lengths
        - Return the largest one
        - If table is empty, return 0

        TODO:
        - Reuse bucket_lengths()
        """
        pass

    def __len__(self) -> int:
        """
        Return the number of stored keys.

        TODO:
        - Return self.size
        """
        pass


# ============================================================
# 3. Local demo / sanity check
# ============================================================

def _demo() -> None:
    """
    A small local sanity check for the hash table.

    Suggested demo steps:
    - Create a small hash table with a tiny capacity
    - Insert several keys
    - Increment some numeric values
    - Append records into a list value
    - Print:
        - retrieved values
        - contains() results
        - table size
        - collision count
        - load factor
        - max chain length

    TODO:
    - Add a few sample operations
    - Print the outputs clearly
    """
    pass


# ============================================================
# 4. Script entry
# ============================================================

if __name__ == "__main__":
    # TODO:
    # - Run the local demo
    # - Use it to verify whether the hash table works as expected
    pass