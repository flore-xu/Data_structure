class MergeSort:
    @classmethod
    def isSorted(cls, A: list[int], lo: int, hi: int) -> bool:
        """check if array[lo, hi] is sorted"""
        for i in range(lo+1, hi):
            if A[i] < A[i-1]:
                return False 
        return True

    @classmethod
    def merge(cls, A: list[int], aux: list[int], lo: int, mid: int, hi: int) -> None:
        """In-place merge two sorted arrays to a larger sorted array
        O(N) N = hi-lo+1
        """
        
        # precondition: A[lo, mid] and A[mid+1, hi] are sorted
        assert cls.isSorted(A, lo, mid)
        assert cls.isSorted(A, mid+1, hi)
        
        # Step1: copy all items in original array to an auxilary array
        for i in range(lo, hi+1):
            aux[i] = A[i]

        # Step2: merge back to original array   aux[lo, mid] + aux[mid+1, hi] -> A[lo, hi]
        # 2 pointers, one start from left part and the other one from right part respectively
        i, j = lo, mid+1
        for k in range(lo, hi+1): # pass original array from lo to hi
            if i > mid:         # left part run out
                A[k] = aux[j]
                j += 1 
            elif j > hi:        # right part run out
                A[k] =  aux[i]
                i += 1 
            elif aux[j] < aux[i]: # both left and right part aren't run out, choose the smaller one
                A[k] = aux[j]
                j += 1
            else:   # aux[j] >= aux[k]
                A[k] = aux[i]
                i += 1
        
        # postcondition: A[lo, hi] is sorted
        assert cls.isSorted(A, lo, hi)

    @classmethod
    def sort(cls, A: list[int], aux: list[int], lo: int, hi: int) -> None:
        """in-place merge sort A[lo, hi]
        Base case: if n < 2, then the array is already sorted. Stop now.
        Otherwise n > 1, perform the following three steps in sequence:
        1. Sort the left half of the array.
        2. Sort the right half of the array.
        3. Merge the sorted left and right halves into an array.
        """
        if lo >= hi:    # base case 
            return 
        
        mid = (lo + hi) // 2        
        cls.sort(A, aux, lo, mid)       # 1. Sort the left half of the array.
        cls.sort(A, aux, mid+1, hi)     # 2. Sort the right half of the array.
        cls.merge(A, aux, lo, mid, hi)  # 3. Merge the sorted left and right halves into an array.

    @classmethod
    def topdown(cls, A: list[int]) -> None: 
        """Top-down (recursive) merge sort 
        O(NlogN) for ALL cases
        Disadvantage: need extra space O(N) to do merge
        
        T(n) = T(n/2) + T(n/2) + n (n > 1)
        T(n) = 0                   (n = 1)
        T(n) is the number of comparisons required to sort an array of length n.
        T(n/2) for left and right halves, n for merge.
        Comparison:   O(NlogN) [1/2 NlogN, NlogN]
        Array access: O(NlogN) <= 6 NlogN
        """
        n = len(A)
        aux = [0] * len(A)      # O(N) extra space for an auxillary array
        cls.sort(A, aux, 0, n-1)

        assert cls.isSorted(A, 0, n-1)
    
    @classmethod
    def bottomup(cls, A: list[int]) -> None: 
        """Bottom-up (iterative) merge sort.
        O(N log N) for ALL cases
        Disadvantage: need extra space O(N) to do merge

            1. do a pass of 1-by-1 merges (subarray size = 1)
            2. do a pass of 2-by-2 merges (subarray size = 2)
            3. do a pass of 4-by-4 merges (subarray size = 4)
            ...
            4. do a pass of N/2-by-N/2 merges (subarray size = N/2)
        
        T(n) = T(n/2) + T(n/2) + n (n > 1)
        T(n) = 0                   (n = 1)
        T(n) is the number of comparisons required to sort an array of length n.
        T(n/2) for left and right halves, n for merge.
        Comparison:   O(NlogN) [1/2 NlogN, NlogN]
        Array access: O(NlogN) <= 6 NlogN
        """
        n = len(A)
        aux = [0] * n       # O(N) extra space for an auxillary array
        length = 1          # start from subarray size 1
        while length < n:
            for lo in range(0, n, 2*length):
                mid = min(lo + length - 1, n-1)
                hi = min(lo + 2*length - 1, n-1)
                cls.merge(A, aux, lo, mid, hi)
            length *= 2     # double the subarray size 

        assert cls.isSorted(A, 0, n-1)

    

if __name__ == '__main__':
    print("Merge sort")

    nums = [9, 8, 7, 6, 5, 4, 3, 2, 1]
    print(f"Top-down Merge sort of nums = {nums}")
    MergeSort.topdown(nums)

    nums = [9, 8, 7, 6, 5, 4, 3, 2, 1]
    print(f"Bottom-up Merge sort of nums = {nums}")
    MergeSort.bottomup(nums)