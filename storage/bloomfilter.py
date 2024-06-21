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
    import random
    import time
    
    num_insertions = 4000
    valid_keys = [
        random.randbytes(random.randint(5, 10)) for _ in range(num_insertions // 2)
    ]
   
    invalid_keys = [
        random.randbytes(random.randint(5, 10)) for _ in range(num_insertions // 2)
    ]
    
    fp = 0
    start = time.time()
   
    for key in valid_keys:
        bf.insert(key)
    
    key_insert = time.time()
    
    for key in invalid_keys:
        output = bf.check(key)
        if output:
            fp += 1
    
    for key in valid_keys:
        output = bf.check(key)
        if not output:
            print("Assertion failed. The filter is producing NO for items that are definitely there")
    end = time.time() 
    key_check = time.time()
    print(f"Finished insertion in {key_insert - start} time and validity check in {end - start} seconds.")  