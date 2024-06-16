'''
A (very) simple sorted Linked list implementation.
'''

from typing import Self, Any

class LinkedListNode:
    def __init__(self, value: Any) -> None:
        self.next: Self | None = None
        self.value = value

    def set_next(self, node: Self) -> None:
        self.next = node


class LinkedList:
    def __init__(self) -> None:
        # Sentinel node
        self.root: LinkedListNode = LinkedListNode(-1)

    def find_candidate(self, value: Any) -> tuple[LinkedListNode, LinkedListNode]:
        # Requires values to be comparable to each other, and
        # types to be the same.
        prev = self.root
        current = self.root.next
        while current is not None and current.value < value:
            prev = current
            current = current.next
        return prev, current

    def find(self, value: Any) -> LinkedListNode | None:
        _, candidate = self.find_candidate(value)
        if candidate is not None and candidate.value == value:
            return candidate
        return None
    
    def insert(self, node: LinkedListNode) -> None:
        prev, candidate = self.find_candidate(node.value)
        node.next = candidate
        prev.next = node
        
    def __str__(self) -> str:
        current = self.root
        st = ""
        while current.next is not None:
            current = current.next
            st += str(current.value) + "->"
        st += "END"
        return st
       
if __name__ == "__main__":
    ll = LinkedList()
    l0 = LinkedListNode(0)
    l1 = LinkedListNode(1)
    l2 = LinkedListNode(2)
    l3 = LinkedListNode(4)
    l4 = LinkedListNode(3)
    ll.insert(l0)
    ll.insert(l1)
    ll.insert(l2)
    ll.insert(l3)
    ll.insert(l4)
    print(ll)
