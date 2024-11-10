"""
A generic stack implemented using a singly linked list.

% more tobe.txt 
to be or not to - be - - that - - - is

% python stack.py < tobe.txt
to be not that or be (2 left on stack)
"""


class ListNode:
    """Definition for node of singly-linked list."""
    def __init__(self, val: int =0, next: 'ListNode' =None):
        self.val = val
        self.next = next
 

class Stack:

    def __init__(self):
        """Initializes an empty stack"""
        self.first = None   # top of stack, not head of linked list, actually tail
        self.n = 0          # size of stack

    def size(self) -> int:
        """Returns the number of items in the stack"""
        return self.n

    def is_empty(self) -> bool:
        """Returns True if stack is empty, False otherwise"""
        return self.first is None

    def push(self, val: int) -> None:
        """Adds an item to stack O(1)"""

        self.first = ListNode(val, self.first)
        self.n += 1

    def pop(self) -> int:
        """Removes and return the item from the top of Stack O(1)
           @return top item
           @raise IndexError if stack is empty
        """
        if self.is_empty():
            raise IndexError("Stack underflow")
        else:
            val = self.first.val
            self.first = self.first.next
            self.n -= 1
            return val

    def peek(self) -> int:
        """Return the last item from the Stack O(1)
           @return top item
           @raise IndexError if stack is empty
        """
        if self.is_empty():
            raise IndexError("Stack underflow")
        return self.first.val 

if __name__ == '__main__':

    numbers = [1,2,3,4,5]

    stk = Stack()  # initiate a stack

    print(f"initial stack: {stk}, size: {stk.size()}")

    # instack: push items to stack
    for item in numbers:
        stk.push(item)
        print(f"push: {item}, stack: {stk}, size: {stk.size()}, peek: {stk.peek()}")

    # outstack: pop items from stack
    while not stk.is_empty():
        print(f"pop: {stk.pop()}, stack: {stk}, size: {stk.size()}")
