"""
A generic queue implemented using a singly linked list.

% more tobe.txt 
to be or not to - be - - that - - - is

% python queue.py < tobe.txt
to be not that or be (2 left on queue)
"""


class ListNode:
    """Definition for node of singly-linked list."""
    def __init__(self, val: int =0, next: 'ListNode' =None):
        self.val = val
        self.next = next

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

class Queue:

    def __init__(self):
        """Initializes an empty queue"""
        self.first = None   # beginning of queue
        self.last = None    # end of queue
        self.n = 0          # number of items in the queue

    def __str__(self) -> str:
        """Return a string representation of the queue
           @return the sequence of items in this queue in FIFO order, separated by spaces
        """
        return " ".join(str(i) for i in self)

    def __iter__(self) -> LinkIterator:
        """Returns an iterator to this queue that iterates through the items in LIFO order."""
        return LinkIterator(self.first)

    def size(self) -> int:
        """Returns the number of items in the queue"""
        return self.n

    def is_empty(self) -> bool:
        """Returns True if queue is empty, False otherwise"""
        return self.first is None

    def enqueue(self, val: int) -> None:
        """Adds item to the tail of the queue O(1)
        """
        node = ListNode(val)
        if self.is_empty():
            self.first = self.last = node  
        else:
            self.last.next = node
            self.last = self.last.next  

        self.n += 1


    def dequeue(self) -> int:
        """Removes and return the item from the head of queue O(1)

           @return first item
           @raise IndexError if queue is empty
        """
        if self.is_empty():
            raise IndexError("queue underflow")

        val = self.first.val 
        self.first = self.first.next 
        if self.is_empty():
            self.last = None # to avoid loitering
        self.n -= 1
        return val 

    def front(self) -> int:
        """Return the item at the head of queue O(1)

           @return first item
           @raise IndexError if queue is empty
        """
        if self.is_empty():
            raise IndexError("queue underflow")
        
        return self.first.val 

if __name__ == '__main__':

    numbers = [1,2,3,4,5]

    q = Queue()  # initiate a queue

    print(f"initial queue: {q}, size: {q.size()}")

    # 入队 push items to queue
    for item in numbers:
        q.enqueue(item)
        print(f"enqueue: {item}, queue: {q}, size: {q.size()}, front: {q.front()}")

    # 出队 pop items from queue
    while not q.is_empty():
        print(f"front: {q.front()}, dequeue: {q.dequeue()}, queue: {q}, size: {q.size()}")
