from threading import Lock
from random import randbytes, randint
from skiplist import SkipList

THRESHOLD = 1000

class sst_entry:
    def __init__(self, key, value) -> None:
        self.key = key
        self.value = value
    
    def __eq__(self, value: object) -> bool:
        return self.key == value.key

    def __lt__(self, other) -> bool:
        return self.key < other.key
    
    def __gt__(self, other) -> bool:
        return self.key > other.key
    
    def __ge__(self, other) -> bool:
        return self.key >= other.key
    
    def __le__(self, other) -> bool:
        return self.key <= other.key
    
    def __repr__(self) -> str:
        return str(self.key)

    def __hash__(self) -> int:
        return hash(self.key)
    
    def __str__(self) -> str:
        return f"{self.key}::{self.value}"
    
class InsertEntry(sst_entry):
    def __init__(self, key, value) -> None:
        super().__init__(key, value)

class SearchEntry(sst_entry):
    def __init__(self, key) -> None:
        super().__init__(key, None)

class Memtable:
    def __init__(self) -> None:
        self.current_sst = 0
        self.mutex = Lock()
        self.cache = SkipList(levels = 16)
        self.size  = 0
        self.locked = False

    def freeze(self):
        with self.mutex:
            self.locked = True
            # flush this sst to the disk.

    def insert(self, key, value):
        with self.mutex:
            # Check size.
            if self.size <= THRESHOLD:
                self.cache.insert(InsertEntry(key, value))
                self.size += len(key)
                self.size += len(value)

            else:
                # dump this file into a SST table.
                table_file = f"sst_{self.current_sst}.sst"
                with open(table_file, "w") as sstfile:
                    for item in self.cache.dump():
                        sstfile.write(item)
                self.cache = SkipList(levels = 16)
                self.size = 0
                self.locked = False
                self.current_sst += 1 
                

    def find(self, key):
        # At this point it's worth exploring bloom filters.
        with self.mutex:
            # search cache for skiplistnode
            found = self.cache.find(SearchEntry(key))
            # This returns a "candidate" key
            if found.value.key == key:
                return found.value.value
            else:
                return None

if __name__ == "__main__":
    INSERTIONS = 400000
    random_bytes_gen = { randbytes(randint(10, 15)) : randbytes(randint(15, 100)) for i in range(INSERTIONS) }
    import time
    start = time.time()
    table = Memtable()
    for k, v in random_bytes_gen.items():
        table.insert(k, v)
    
    for k in random_bytes_gen:
        assert table.find(k) is not None
    
    end = time.time()
    print(f"Took {end - start} seconds")