from typing import Union  

class Heap:
	"""Implementation of heap by Python built-in list, 
       specify heap type (max or min) via property `type`
    """

	def __init__(self, type: str ="min") -> None:
		"""Initialize a heap. 
		   1-based indexing, set index 0 to be dummy, i.e., None
		"""
		self.heap = [None]  # represent a heap of size n in array of length n+1 with array[0] unused
		self.type = type 	# "min": Min-heap，"max": Max-heap
		self.size = 1    	# size of heap
	
	def _parent(self, i: int) -> int:
		"""Return index of parent of node i O(1)
		   Use bit manipulation to speed up 
		"""
		return i >> 1   # i // 2
	
	def _left(self, i: int) -> int:
		"""Return index of left child of node i O(1)"""
		return i << 1 # i * 2
	
	def _right(self, i: int) -> int:
		"""Return index of right child of node i O(1)"""
		return (i << 1) + 1
	
	def __str__(self):
		"""Return a string representation of the heap"""
		return str(self.heap)
	
	def is_empty(self) -> bool:
		"""Check if heap is empty, returns True if empty, otherwise False"""
		return self.size <= 1
	
	def _less(self, i: int, j: int, type: str) -> bool:
		"""Compare priority of nodes based on heap type.
           Returns True if priority of node i less than node j, otherwise False
           
           @param type: either 'min' or 'max'
        """
		if type == 'min':
			return self.heap[i] > self.heap[j]
		elif type == 'max':
			return self.heap[i] < self.heap[j]
	
	def _swap(self, i: int, j: int) -> None:
		"""Exchanges two nodes
		   @param i, j: index of two nodes
		"""
		self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
	
	def _shift_up(self, index: int) -> None:
		"""Recursive version of shift up.
           After inserting a node, shift up the node to maintain heap invariant.
           If priority of node > parent node, swap it with parent (i.e., move node up for a level)
           Repeat until priority of node ≤  parent node or node is at root.
		   T: O(logn) Worst case node will move from bottom to root
		   
           @param index: index of current node 
		"""
		if index == 1:	# base case: current node is at root
			return 
		
		parent = self._parent(index)  # index of parent node 

		# If priority of node > parent node, swap it with parent (i.e., move node up for a level)
		if self._less(parent, index, self.type):
			self._swap(index, parent)
			self._shift_up(parent)   # After swap, position of parent node may not correct, so recursively shift-up parent node if necessary 

	
	def _shift_down(self, index: int) -> None:
		"""Recursive version of shift down.
           After deleting a node, shift down the current node to main heap invariant.
           Swap the node with the child node of smallest priority, i.e., move node down for a level.
           Repeat until priority of node ≥ child node or meet leaf node.
		   T: O(logn) Worst case node will move from root to bottom level.
		   
           @index: index of current node
		"""
		cur = index		        # position of a pointer to find node of smallest priority
		l = self._left(index)	# index of left child node
		r = self._right(index)	# index of right child node 

        # If priority of current node is less than left child node, pointer points to left child node
		if l < self.size and self._less(cur, l, self.type):  
			cur = l 
        # If priority of current node is less than right child node, pointer points to right child node
		if r < self.size and self._less(cur, r, self.type):
			cur = r

        # if pointer has changed position, swap node with the node pointed.
		if cur != index: 
			self._swap(index, cur)
			self._shift_down(cur)    # After swap, position of child node may not correct, so recursively shift-down the child node
	
	def _update_key(self, index: int, val: int) -> None:
		"""Update the priority of node to specified value and maintain heap invariant  O(logN)
		   index: index of node
		   val: new priority value
		"""
		old_val = self.heap[index]
		self.heap[index] = val 
		if val > old_val:
			self._shift_down(index)
		else:
			self._shift_up(index)
	
	def _delete(self, index: int) -> None:
		"""Delete the specified node and maintain heap invariant O(logN)"""

		# swap specified node and last node 
		self._swap(index, -1)

		# delete last node 
		self.heap.pop()

		self.size -= 1

		# shift-down last node
		self._shift_down(index)
		

	def peek(self) -> Union[tuple, int]:
		"""Returns top node O(1)
           Returns None if heap is empty.
        """
		if self.is_empty():
			return 
		else:
			return self.heap[1] 
	 
	
	def push(self, item: Union[tuple, int]) -> None:
		"""Insert a new node and maintain heap invariant   O(logN)
		"""
		# add new node to heap tail
		self.heap.append(item)

		self.size += 1

		# shift up the last node 
		self._shift_up(self.size-1)
	
	def pop(self) -> Union[tuple, int]:
		"""Returns and removes the top node and maintain heap invariant O(logN)
           Returns None if heap is empty
		"""
		if self.is_empty(): # safeguard
			return

		# record top node 
		top = self.heap[1]

		# swap top node and last node
		self._swap(1, -1)

		# removes last node
		self.heap.pop()

		self.size -= 1

		# shift down the new top node 
		self._shift_down(1)

		return top
	
	def replace(self, item: Union[tuple, int]) -> Union[tuple, int]:
		"""First removes and return top node, then insert a new node and maintain heap invariant 
           faster than 1 call for pop() plus 1 call for push(node)
        O(logN)
        """
		if self.is_empty():
			return

		# Record top node
		top = self.heap[1]

		# Add new node to tail
		self.heap.append(item)

		self.size += 1

		# Swap top node and tail node
		self._swap(1, -1)

		# Removes tail node
		self.heap.pop()

		self.size -= 1

		# Shift down new top node 
		self._shift_down(1)

		return top

if __name__ == '__main__':
    #*****************************************************
    # Equivalency testing on a very large test case
    #******************************************************
    print("Equivalency testing on a very large test case")
    import time, random, heapq

    begin = time.time()

    ours = Heap('min')
    theirs = []

    assert ours.is_empty() and theirs == [] # both empty at the start

    N = 100000 # usually just a few seconds (10x smaller than the C++ version)
    for _ in range(N): # insert N random integers to both data structures
        value = random.randint(0, 2**31-1)
        ours.push(value)
        heapq.heappush(theirs, value)

    assert not ours.is_empty() and theirs # both not empty (has N entries) by now
    assert ours.size-1 == len(theirs) # heap size should match

    while not ours.is_empty():
        assert ours.peek() == theirs[0] # max value should match (note that theirs contains negative values)
        ours.pop()
        heapq.heappop(theirs)
        assert ours.size-1 == len(theirs) # heap size should match
    assert ours.is_empty() and not theirs # both empty at the end

    print("Test time = %fs" % (time.time()-begin))
    print("If there is no assertion (Run Time Error), then all is good")

    #*****************************************************
    # Test on Min-heap
    #******************************************************
    print("Test on Min-heap")

    items = [1, 3, 5, 4, 2]

    heap = Heap('min')  # initiate a min heap

    print(f"initial min-heap: {heap}, size: {heap.size}")

    # push items to heap
    print("push items to heap")
    for item in items:
        heap.push(item)
        print(f"push: {item}, peek: {heap.peek()}, size: {heap.size}, min-heap: {heap}")

    # pop items from heap
    print("pop items from heap")
    while not heap.is_empty():
        print(f"pop: {heap.pop()}, peek: {heap.peek()}, size: {heap.size}, min-heap: {heap}")

    #*****************************************************
    # Test on Max-heap
    #******************************************************
    print("Test on Max-heap")

    items = [1, 3, 5, 4, 2]

    heap = Heap("max")  # initiate a max heap

    print(f"initial max-heap: {heap}, size: {heap.size}")


    # push nodes to heap
    for item in items:
        heap.push(item)
        print(f"push: {item}, peek: {heap.peek()}, size: {heap.size}, max-heap: {heap}")


    # pop items from heap
    while not heap.is_empty():
        print(f"pop: {heap.pop()}, peek: {heap.peek()}, size: {heap.size}, max-heap: {heap}")