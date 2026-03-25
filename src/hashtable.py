from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class HashNode:
    key: Any
    value: Any
    next: "HashNode | None" = None


class HashTable:
    """
    A simple hash table using separate chaining.

    Features:
    - insert(key, value)
    - get(key)
    - contains(key)
    - increment(key, amount)
    - append_to_list(key, item)
    - collision statistics
    """

    def __init__(self, capacity: int = 200003) -> None:
        self.capacity = capacity
        self.buckets: list[HashNode | None] = [None] * capacity
        self.size = 0
        self.collision_count = 0

    def _hash(self, key: Any) -> int:
        """
        Compute a bucket index for the given key.
        """
        return hash(key) % self.capacity

    def insert(self, key: Any, value: Any) -> None:
        """
        Insert or update a key-value pair.
        If the key already exists, overwrite its value.
        """
        index = self._hash(key)
        head = self.buckets[index]

        if head is None:
            self.buckets[index] = HashNode(key, value)
            self.size += 1
            return

        # Collision occurred because bucket already has at least one node
        self.collision_count += 1

        current = head
        while current is not None:
            if current.key == key:
                current.value = value
                return
            if current.next is None:
                break
            current = current.next

        current.next = HashNode(key, value)
        self.size += 1

    def get(self, key: Any, default: Any = None) -> Any:
        """
        Return the value for key if found; otherwise return default.
        """
        index = self._hash(key)
        current = self.buckets[index]

        while current is not None:
            if current.key == key:
                return current.value
            current = current.next

        return default

    def contains(self, key: Any) -> bool:
        """
        Return True if the key exists in the table.
        """
        return self.get(key, default=None) is not None

    def increment(self, key: Any, amount: int = 1) -> None:
        """
        Increment a numeric value stored at key.
        If key does not exist, initialize it with amount.
        """
        current_value = self.get(key)

        if current_value is None:
            self.insert(key, amount)
        else:
            self.insert(key, current_value + amount)

    def append_to_list(self, key: Any, item: Any) -> None:
        """
        Append an item to a list stored at key.
        If key does not exist, initialize it with a new list.
        """
        current_value = self.get(key)

        if current_value is None:
            self.insert(key, [item])
        else:
            current_value.append(item)

    def keys(self) -> list[Any]:
        """
        Return all keys in the hash table.
        """
        all_keys = []
        for bucket in self.buckets:
            current = bucket
            while current is not None:
                all_keys.append(current.key)
                current = current.next
        return all_keys

    def values(self) -> list[Any]:
        """
        Return all values in the hash table.
        """
        all_values = []
        for bucket in self.buckets:
            current = bucket
            while current is not None:
                all_values.append(current.value)
                current = current.next
        return all_values

    def items(self) -> list[tuple[Any, Any]]:
        """
        Return all key-value pairs in the hash table.
        """
        all_items = []
        for bucket in self.buckets:
            current = bucket
            while current is not None:
                all_items.append((current.key, current.value))
                current = current.next
        return all_items

    def load_factor(self) -> float:
        """
        Return the current load factor.
        """
        return self.size / self.capacity

    def bucket_lengths(self) -> list[int]:
        """
        Return the length of each bucket chain.
        Useful for collision analysis.
        """
        lengths = []
        for bucket in self.buckets:
            length = 0
            current = bucket
            while current is not None:
                length += 1
                current = current.next
            lengths.append(length)
        return lengths

    def max_chain_length(self) -> int:
        """
        Return the maximum chain length among all buckets.
        """
        return max(self.bucket_lengths(), default=0)

    def __len__(self) -> int:
        return self.size


def _demo() -> None:
    """
    Simple sanity check.
    """
    table = HashTable(capacity=11)

    table.insert("A", 10)
    table.insert("B", 20)
    table.increment("A")
    table.increment("C", 5)
    table.append_to_list("reviews", {"id": 1, "score": 5})
    table.append_to_list("reviews", {"id": 2, "score": 4})

    print("=" * 60)
    print("HASHTABLE DEMO")
    print("=" * 60)
    print("A ->", table.get("A"))
    print("B ->", table.get("B"))
    print("C ->", table.get("C"))
    print("reviews ->", table.get("reviews"))
    print("contains('A') ->", table.contains("A"))
    print("contains('Z') ->", table.contains("Z"))
    print("size ->", len(table))
    print("collision_count ->", table.collision_count)
    print("load_factor ->", round(table.load_factor(), 4))
    print("max_chain_length ->", table.max_chain_length())


if __name__ == "__main__":
    _demo()