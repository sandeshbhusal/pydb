from typing import Any
import random

MAX_LEVELS: int = 4


class SkipListNode:
    def __init__(self, value: Any) -> None:
        self.value = value
        self.next = [None] * (MAX_LEVELS)
        
    def insert_after(self, level: int, node: "SkipListNode") -> None:
        old_ref = self.next[level]
        self.next[level] = node
        node.next[level] = old_ref
        
    def __str__(self) -> str:
        return str(self.value)


class SkipList:
    def __init__(self) -> None:
        self.root = SkipListNode(-1)  # Sentinel node.
        self.maxlevels = MAX_LEVELS

    def find_candidate(self, value: Any) -> SkipListNode:
        """
        Search for a key in the skiplist.
        """

        level = self.maxlevels - 1
        curr  = self.root
        
        while level >= 0:
            next = curr.next[level]
            if next is None:
                level -= 1
            else:
                if next.value <= value: # made a mistake here. next.value is to be compared.
                    curr = next
                else:
                    level -= 1
       
        return curr
    
    def insert(self, value: Any):
        candidate = self.find_candidate(value)
        node = SkipListNode(value)
        
        # update the bottom-most pointer. 
        old_ref = candidate.next[0]
        node.next[0] = old_ref
        candidate.next[0] = node
        
    def __str__(self) -> str:
        s = ""
        for i in range(MAX_LEVELS - 1, -1, -1):
            curr = self.root.next[i]
            s += f"ROOT {i} -> "
            while curr is not None:
                s += f"{curr} ->"
                curr = curr.next[i]
            s += "END\n"
        return s
                
sl = SkipList()
for i in range(0, 5):
    sl.insert(random.randint(0, 100))
print(sl)