class ListNode:
    """Doubly linked list, each node has 3 attribute
    """         
    def __init__(self, val: int=0, next: 'ListNode'=None, prev: "ListNode"=None):
        self.val = val      # value of current node
        self.next = next    # a pointer points to the successor node
        self.prev = prev    # a pointer points to predecessor node

class LinkIterator:

    def __init__(self, cur: ListNode):
        self.cur = cur

    def __next__(self):
        if not self.cur:
            raise StopIteration()
        else:
            val = self.cur.val 
            self.cur = self.cur.next
            return val

class Deque():
    """define the deque constructor using double-linked list
    """
    def __init__(self):
        """initiate the deque"""
        self.head, self.tail = ListNode(0), ListNode(0)  # two Sentinel Nodes, one for head and one for tail
        # head points to tail, tail points to head
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0

    def __str__(self) -> str:
        """Return a string representation of the queue
           @return the sequence of items in this queue in FIFO order, separated by spaces
        """
        return " ".join(str(i) for i in self)

    def __iter__(self) -> LinkIterator:
        """Returns an iterator to this queue that iterates through the items in LIFO order."""
        return LinkIterator(self.head.next)    
       
    def size(self) -> int:
        """Return the size of the deque O(1)"""
        return self.size 
        

    def is_empty(self) -> bool:
        """
        Returns whether the deque is empty or not, O(1)
        True if empty, False if not empty
        """
        return self.size == 0


      
    def enqueueHead(self, item: int) -> None:
        """Adds item to the head of the deque O(1)
        """
        succ = self.head.next 
        node = ListNode(item, next=succ, prev=self.head)
        self.head.next = succ.prev = node

        self.size += 1
    
    def enqueueTail(self, item: int) -> None:
        """Adds item to the tail of the deque O(1)
        """
        pred = self.tail.prev 
        node = ListNode(item, next=self.tail, prev=pred)
        pred.next = self.tail.prev = node

        self.size += 1

    def dequeueHead(self) -> int:
        """Removes and return the item from the head of deque O(1)
           @return first item
           @raise IndexError if deque is empty
        """
        if self.is_empty():
            raise IndexError("Deque underflow")
        
        self.size -= 1
        item = self.head.next
        succ = item.next 
        self.head.next, succ.prev = succ, self.head

        return item.val    


    def dequeueTail(self) -> int:
        """Removes and return the item from the tail of deque O(1)
           @return last item
           @raise IndexError if deque is empty
        """
        if self.is_empty():
            raise IndexError("Deque underflow")
        self.size -= 1
        item = self.tail.prev
        succ = item.prev 
        self.tail.prev, succ.next = succ, self.tail 
        return item.val  

          
    def front(self) -> int:
        """Return the item at the head of deque O(1)
           @return first item
           @raise IndexError if deque is empty
        """
        if self.is_empty():
            raise IndexError("Deque underflow")
        
        return self.head.next.val 
    
    def rear(self) -> int:
        """Return the item at the tail of deque O(1)
           @return last item
           @raise IndexError if deque is empty
        """
        if self.is_empty():
            raise IndexError("Deque underflow")
        
        return self.tail.prev.val

if __name__ == '__main__':

    numbers = [1,2,3,4,5]

    q = Deque()  # initiate a deque

    print(f"initial deque: {q}, size: {q.size}")

    # enqueue: push items to head of deque
    for item in numbers:
        q.enqueueHead(item)
        print(f"enqueueHead: {item}, deque: {q}, size: {q.size}, front: {q.front()}")

    # dequeue: pop items out of head of deque
    while not q.is_empty():
        print(f"front: {q.front()}, dequeueHead: {q.dequeueHead()}, deque: {q}, size: {q.size}")


    print("Equivalency testing on a very large test case")

    import time, random
    from collections import deque 

    # large random test
    begin = time.time()

    ours = Deque()
    theirs = deque()
    assert ours.is_empty() and len(theirs) == 0 # both empty at the start
    N = 100000 # usually just a few seconds (10x smaller than the C++ version)
    for _ in range(N): # insert N random integers to both data structures
        value = random.randint(0, 2**31-1)
        ours.enqueueHead(value)
        theirs.appendleft(value)
    
    assert not ours.is_empty() and len(theirs) > 0 # both not empty (has N entries) by now
    while not ours.is_empty():
        assert ours.front() == theirs[0] # front-most value (index 0) should match
        ours.dequeueHead()
        theirs.popleft()
    assert ours.is_empty() and len(theirs) == 0 # both empty at the end

    print("Test time = %fs" % (time.time()-begin))
    print("If there is no assertion (Run Time Error), then all is good")
