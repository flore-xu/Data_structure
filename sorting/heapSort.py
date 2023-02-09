class Heap:
    @classmethod
    def isSorted(cls, A: list[int], lo: int, hi: int) -> bool:
        """Check if array[lo, hi] is sorted"""
        for i in range(lo+1, hi):
            if A[i] < A[i-1]:
                return False 
        return True

    @classmethod
    def swap(cls, A: list[int], i: int, j: int) -> None:
        """Exchanges A[i] and A[j]
        Note: Indices are "off-by-one" to support 1-based indexing."""
        A[i-1], A[j-1] = A[j-1], A[i-1]

    @classmethod
    def less(cls, A: list[int], i: int, j: int) -> bool:
        """if priority of node i is less than node j, return True 
        Indices are "off-by-one" to support 1-based indexing.
        Heap type is Max-heap 
        """
        return A[i-1] < A[j-1]

    @classmethod
    def shift_down(cls, A: list[int], index: int, size: int) -> None:
        """Shift-down the node to maintain max-heap invariant
        O(logn)  Worst case node will shift-down from root to bottom

            if priority of current node < its childen, 
                swap with childen (i.e., shift-down current node to next level).
            Repeat until priority of current node ≥ its children or it is a leaf node.
        
        @param A: max-heap
                index: index of current node  
                size: number of nodes in the heap
        """
        cur = index		# position of pointer 
        l = index << 1	        # index of left child node (1-based indexing)
        r = (index << 1) + 1	# index of right child node 

        if l < size+1 and cls.less(A, cur, l):  # if priority of current node < its left childen
            cur = l                         # move pointer to left child
        if r < size+1 and cls.less(A, cur, r):  # if priority of current node < its right childen
            cur = r                         # move pointer to right child

        if cur != index:                    # if pointer changes position
            cls.swap(A, index, cur)
            cls.shift_down(A, cur, size)    # After swap position, child node may not at correct position, so recursively shift-down the child node

    @classmethod
    def sort(cls, A: list[int]) -> list[int]:
        """Heap sort by a max-heap
            O(NlogN) for all cases
        """
        
        # Step 1. O(N) construct a max-heap (from right to left of array)
        size = len(A)
        for index in range(size//2, 0, -1):
            cls.shift_down(A, index, size)  # 下堆，index是子堆的根节点

        # Step 2. O(NlogN) sort down (call heap.pop() N-1 times)
        while size > 1:       # O(N)
            cls.swap(A, 1, size)  # 交换根节点和末尾节点
            size -= 1         # 堆顶节点出堆，总节点数减1
            cls.shift_down(A, 1, size)  # 根节点下堆 O(logN)

        assert cls.isSorted(A, 0, len(A)-1)
    

if __name__ == '__main__':
    
    print("Heap sort")
    nums = [9, 8, 7, 6, 5, 4, 3, 2, 1]
    print(f"nums = {nums}")
    Heap.sort(nums)