class ListNode:
    def __init__(self, val: int=0, next: 'ListNode'=None, prev: "ListNode"=None):
        self.val = val      # value of node
        self.next = next    # a pointer points to the next node, can be null
        self.prev = prev    # a pointer points to the previous node, can be null


class DoublyLinkedList:
    def __init__(self):
        """O(1) Initialize an empty Doubly Linked list"""
        self.size = 0
        self.dummyHead = ListNode(0)   # sentinel node of dummy head
        self.dummyTail = ListNode(0)   # sentinel node of dummy tail

        # initialize as head -> tail, tail -> head
        self.dummyHead.next = self.dummyTail
        self.dummyTail.prev = self.dummyHead

    def __str__(self) -> str:
        """O(N) return string representation of the DLL
           e.g., return '5, 3, 1, 2, 4'
        """
        nodes = list()
        cur = self.dummyHead
        while cur:
            nodes.append(cur.val)
            cur = cur.next
        return str(nodes)

    def isEmpty(self) -> bool:
        """O(1) Returns true if the DLL is empty, or false otherwise."""
        return self.size == 0
    
    def get(self, idx: int) -> int:
        """O(N) return value of node with specified idx. return -1 if idx is invalid"""
        # index is invalid
        if idx < 0 or idx >= self.size:
            return -1

        # index is at left half, forward iterates from head
        if idx + 1 < self.size - idx:
            curr = self.dummyHead
            for _ in range(idx + 1):
                curr = curr.next
        # index is at right half, backward iterates from tail
        else:
            curr = self.dummyTail
            for _ in range(self.size - idx):
                curr = curr.prev
        return curr.val

    def addAtHead(self, val: int) -> None:
        """O(1) insert a new node at head"""
        self.size += 1
        pred, succ = self.dummyHead, self.dummyHead.next  
        node = ListNode(val, prev=pred, next=succ)
        pred.next = succ.prev = node

    def addAtTail(self, val: int) -> None:
        """O(1) insert a new node at tail"""
        self.size += 1
        pred, succ = self.dummyTail.prev, self.dummyTail 
        node = ListNode(val, prev=pred, next=succ)
        pred.next = succ.prev = node
        
    def addAtIndex(self, idx: int, val: int) -> None:
        """O(N) insert new node at specified index
            5 cases
            1. idx < 0 or idx >= N+1: invalid index
            2. idx = 0: add node after dummy head
            3. idx in [1, N-1]: add node in the middle of linked list
            4. index = N: add node after tail
            5. linked list is empty: same as case 2 because use of dummy head
        """
        # case 1: invalid index
        if idx < 0 or idx > self.size:
            return None 

        self.size += 1  # increment number of effective nodes

        # find node before and after index
        # index is at left half, forward iterates from head
        if idx < self.size - idx:
            pred = self.dummyHead
            for _ in range(idx):
                pred = pred.next
            succ = pred.next
        # index is at right half, backward iterates from tail
        else:
            succ = self.dummyTail
            for _ in range(self.size - idx):
                succ = succ.prev
            pred = succ.prev

        # create new node and make connection between precedensor and successor
        node = ListNode(val, prev=pred, next=succ)
        pred.next = succ.prev = node

    def deleteAtIndex(self, idx: int) -> None:
        """O(N) delete node at specified index
           4 cases
           1. idx < 0 or idx >= N: invalid index
           2. idx = 0: delete head
           3. idx = N-1: delete tail
           4. idx in [1, N-2]: detele middle node
        """
        # case 1: invalid index
        if idx < 0 or idx >= self.size:
            return None 
        
        # find node before and after index
        # index is at left half, forward iterates from head
        if idx < self.size - idx:
            pred = self.dummyHead
            for _ in range(idx):
                pred = pred.next
            succ = pred.next.next
        
        # index is at right half, backward iterates from tail
        else:
            succ = self.dummyTail
            for _ in range(self.size - idx - 1):
                succ = succ.prev
            pred = succ.prev.prev

        self.size -= 1  # decrement number of effective nodes
        pred.next, succ.prev = succ, pred 

    def deleteAtHead(self) -> None:
        """O(1) Deletes the node at head of DLL"""
        if self.isEmpty():
            return 
        pred, succ =  self.dummyHead, self.dummyHead.next.next 
        pred.next, succ.prev = succ, pred         
        self.size -= 1
        return True 

    def deleteAtTail(self) -> None:
        """O(1) Deletes the node at tail of DLL"""
        if self.isEmpty():
            return 
        pred, succ = self.dummyTail.prev.prev, self.dummyTail 
        pred.next, succ.prev = succ, pred
        self.size -= 1
        return True
    
if __name__ == '__main__':
    dll = DoublyLinkedList()
    dll.addAtHead(1)
    dll.addAtTail(3)
    dll.addAtIndex(1, 2) 
    print(f"Doubly Linked List: {dll}")

    print(f"get(1): {dll.get(1)}")   
    
    print("deleteAtIndex(1)")
    dll.deleteAtIndex(1)  
    print(f"Doubly Linked List: {dll}")
    print(f"get(1): {dll.get(1)}") 