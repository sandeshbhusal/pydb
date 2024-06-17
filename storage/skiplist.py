from typing import Any
import random

MAX_LEVELS: int = 4


class SkipListNode:
    def __init__(self, value: Any, levels: int) -> None:
        self.value = value
        self.next = [None] * (levels)
        
    def insert_after(self, level: int, node: "SkipListNode") -> None:
        old_ref = self.next[level]
        self.next[level] = node
        node.next[level] = old_ref
        
    def __str__(self) -> str:
        return str(self.value)


class SkipList:
    def __init__(self, levels = MAX_LEVELS) -> None:
        self.maxlevels = levels
        self.root = SkipListNode(-1, levels=self.maxlevels)  # Sentinel node.

    def find_candidate(self, value: Any) -> SkipListNode:
        """
        Search for a key in the skiplist.
        """

        level = self.maxlevels - 1
        curr  = self.root
        
        updates = [None] * self.maxlevels 
         
        while level >= 0:
            next = curr.next[level]
            if next is None:
                updates[level] = curr
                level -= 1
            else:
                if next.value <= value: # made a mistake here. next.value is to be compared.
                    curr = next
                else:
                    updates[level] = curr
                    level -= 1
        
        return curr, updates
    
    def insert(self, value: Any):
        candidate, updates = self.find_candidate(value)
        node = SkipListNode(value, self.maxlevels)

        # made a second error here - circular ref by promoting the bottom-most
        # layer first and trying to do all things at once.
        for level, update in enumerate(updates):
            chance = True if level == 0 else random.random() < 0.5
            if chance:
                old_ref = update.next[level]
                node.next[level] = old_ref
                update.next[level] = node
            else:
                break
           
    def __str__(self) -> str:
        s = ""
        for i in range(self.maxlevels - 1, -1, -1):
            curr = self.root.next[i]
            s += f"ROOT {i} -> "
            while curr is not None:
                s += f"{curr} ->"
                curr = curr.next[i]
            s += "END\n"
        return s

if __name__ == "__main__":
    items = [ random.randint(0, 10000000) for i in range(10000) ] 
    sl = SkipList(levels = 16)
    for item in items:
        sl.insert(item)
    
    # search
    for item in items:
        assert(sl.find_candidate(item)[0].value == item)

    print(sl)
