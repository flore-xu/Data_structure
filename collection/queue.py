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


class Queue:

    def __init__(self):
        """Initializes an empty queue"""
        self.head = None   # beginning of queue
        self.tail = None    # end of queue
        self.n = 0          # number of items in the queue

    def size(self) -> int:
        """Returns the number of items in the queue"""
        return self.n

    def is_empty(self) -> bool:
        """Returns True if queue is empty, False otherwise"""
        return self.head is None

    def enqueue(self, val: int) -> None:
        """Adds item to the tail of the queue O(1)
        """
        node = ListNode(val)
        if self.is_empty():
            self.head = self.tail = node  
        else:
            self.tail.next = node
            self.tail = self.tail.next  

        self.n += 1


    def dequeue(self) -> int:
        """Removes and return the item from the head of queue O(1)

           @return head item
           @raise IndexError if queue is empty
        """
        if self.is_empty():
            raise IndexError("queue underflow")

        val = self.head.val 
        self.head = self.head.next 
        if self.is_empty():
            self.tail = None # to avoid loitering
        self.n -= 1
        return val 

    def front(self) -> int:
        """Return the item at the head of queue O(1)

           @return head item
           @raise IndexError if queue is empty
        """
        if self.is_empty():
            raise IndexError("queue underflow")
        
        return self.head.val 

if __name__ == '__main__':

    numbers = [1,2,3,4,5]

    q = Queue()  # initiate a queue

    print(f"initial queue: {q}, size: {q.size()}")

    # enqueue: push items to queue
    for item in numbers:
        q.enqueue(item)
        print(f"enqueue: {item}, queue: {q}, size: {q.size()}, front: {q.front()}")

    # dequeue: pop items from queue
    while not q.is_empty():
        print(f"front: {q.front()}, dequeue: {q.dequeue()}, queue: {q}, size: {q.size()}")
