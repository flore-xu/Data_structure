"""
heap sort
code modified from Java https://algs4.cs.princeton.edu/24pq/Heap.java.html
"""

class Heap:
    @classmethod
    def isSorted(cls, nums: list[int], lo: int, hi: int) -> bool:
        """Check if array[lo..hi] is sorted"""
        for i in range(lo+1, hi+1):
            if nums[i] < nums[i-1]:
                return False 
        return True

    @classmethod
    def swap(cls, nums: list[int], i: int, j: int) -> None:
        """Exchanges nums[i] and nums[j]
        Note: Indices are "off-by-one" to support 1-based indexing."""
        nums[i-1], nums[j-1] = nums[j-1], nums[i-1]

    @classmethod
    def less(cls, nums: list[int], i: int, j: int) -> bool:
        """if priority of node i is less than node j, return True 
        Indices are "off-by-one" to support 1-based indexing.
        Heap type is Max-heap 
        """
        return nums[i-1] < nums[j-1]

    @classmethod
    def shift_down(cls, nums: list[int], index: int, size: int) -> None:
        """(recursive) sink the node at index to maintain max-heap invariant
           O(logn)  Worst case node will shift-down from root to bottom

            if priority of current node < its childen, swap with childen (i.e., shift-down current node to next level).
            Repeat until priority of current node ≥ its children or it is a leaf node.
        
        @param 
        nums: max-heap
        index: index of current node  
        size: number of nodes in the heap
        """
        max_ = index		# node of max priority
        l = index * 2	    # index of left child node (1-based indexing)
        r = index * 2 + 1	# index of right child node 

        # find node of max priority from itself and its two children
        if l <= size and cls.less(nums, max_, l):  
            max_ = l                             
        if r <= size and cls.less(nums, max_, r):  
            max_ = r                            

        # put node of max priority at top
        if max_ != index:                        
            cls.swap(nums, index, max_)             
            cls.shift_down(nums, max_, size)        # adjust position of current node (index `max_`)

    @classmethod
    def sort(cls, nums: list[int]) -> list[int]:
        """Heap sort by a max-heap
            O(NlogN) for all cases

            best case: O(n) compares. all items have equal keys
            average and worst case: 2nlogn compares


            1. build a max-heap from array nums
            (1) naive method O(nlogn) forward iteration
            call heappush() n times
            
            max-heap = []
            for i in range(n):
                heapq.heappush(max-heap, nums[i])

            (2) optimized method O(n) backward iteration
            call heapify() once

            heapq.heapify(nums)

            2. O(NlogN) sort down. 
            call heappop() N-1 times.
            
            for i in range(N-1, 0, -1):
                nums[i] = heapq.heappop(nums)
        """
        size = len(nums)
        # 1. O(N) build a max-heap from array nums
        # proceed from right to left, iterates size//2 times
        for index in range(size//2, 0, -1): # node at index is root of a small subheap
            cls.shift_down(nums, index, size)  # sink node `index`

        # 2. O(NlogN) sort down.
        while size > 1:       
            # pop root from max-heap, put it at the vacated end of array as the max-heap shrinks
            cls.swap(nums, 1, size)  # swap root (max node) with last node of max-heap. max node is at its final position
            size -= 1             # max node is popped, reduce heap size by one
            cls.shift_down(nums, 1, size)  # O(logN) sink root to maintain max-heap invariant 

        assert cls.isSorted(nums, 0, len(nums)-1)
    

if __name__ == '__main__':
    print("Heap sort")
    nums = list(range(1, 100))
    print(f"nums = {nums}")
    Heap.sort(nums)