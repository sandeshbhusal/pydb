from typing import Any
import mmh3


class BloomFilter:
    def __init__(self) -> None:
        # calculations from https://hur.st/bloomfilter/?n=4000&p=0.000001&m=&k=5
        # for 4K items, and 5 hash functions, with 1/1M prob. of false positives.
        self.size = 306871
        self.filter: int = 0
        # The 5 hash functions.
        self.hash_seeds = [52711, 648391, 9737333, 3713921, 1744400]

    def get_bit_pattern(self, input: Any) -> int:
        set_bits = 0
        for seed in self.hash_seeds:
            hash_value = mmh3.hash(input, seed=seed)
            set_bits |= 1 << (hash_value % self.size)
        return set_bits

    def insert(self, input: Any) -> None:
        self.filter |= self.get_bit_pattern(input)

    def check(self, input: Any) -> bool:
        check = self.get_bit_pattern(input)
        return (check & self.filter) == check


if __name__ == "__main__":
    bf = BloomFilter()
    bf.insert("abc")
    assert bf.check("abc")
