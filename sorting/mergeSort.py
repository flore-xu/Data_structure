"""
merge sort
2 implementations
1. top-down recursive (divide-and-conquer)     code modified from https://algs4.cs.princeton.edu/22mergesort/Merge.java.html
2. bottom-up iterative                         code modified from https://algs4.cs.princeton.edu/22mergesort/MergeBU.java.html
"""
class MergeSort:
    @classmethod
    def isSorted(cls, nums: list[int], lo: int, hi: int) -> bool:
        """check if array[lo..hi] is sorted"""
        for i in range(lo+1, hi+1):
            if nums[i] < nums[i-1]:
                return False 
        return True

    @classmethod
    def merge(cls, nums: list[int], aux: list[int], lo: int, mid: int, hi: int) -> None:
        """O(N) merge two sorted subarrays nums[lo..mid] and nums[mid+1..hi] into a larger sorted array nums[lo..hi]
            N = hi-lo+1
            nums: original array 
            aux: an auxiliary array of length N to store a copy of array nums
        """
        # precondition: nums[lo..mid] and nums[mid+1..hi] are sorted
        assert cls.isSorted(nums, lo, mid)
        assert cls.isSorted(nums, mid+1, hi)

        # optimization: skip merge if nums[lo..hi] is already sorted
        # then for a sorted input, merge sort takes O(N)
        if mid+1 <= hi and nums[mid] <= nums[mid+1]:
            return
        
        # 1. O(N) merge two sorted subarrays into an auxiliary array   
        # nums[lo..mid] + nums[mid+1..hi] -> aux[lo..hi]
        # 3 pointers, i for aux[lo..hi], l for nums[lo..mid], r for nums[mid+1..hi]
        i, l, r = lo, lo, mid+1

        # when both subarrays are available, add smaller integer to auxiliary array
        while l <= mid and r <= hi:
            if nums[l] <= nums[r]:
                aux[i] = nums[l]
                l += 1
            else:
                aux[i] = nums[r]
                r += 1
            i += 1    
        
        # when one of subarray is run out, append leftover of another subarray to auxiliary array
        if l <= mid:
            aux[i:hi+1] = nums[l: mid+1]
        elif r <= hi:
            aux[i:hi+1] = nums[r: hi+1]

        # 2. O(N) copy auxiliary array back to original array
        nums[lo: hi+1] = aux[lo: hi+1]

        # postcondition: nums[lo..hi] is sorted
        assert cls.isSorted(nums, lo, hi)

    @classmethod
    def helper(cls, nums: list[int], aux: list[int], lo: int, hi: int) -> None:
        """O(nlogn) in-place merge sort subarray nums[lo..hi]
        
        n = hi-lo+1

        Base case: n = 0 or 1, then the subarray is already sorted, stop now.

        subproblem: n >= 2
        1. divide subarray into two halves, left nums[low..mid] and right nums[mid+1..high]
            if n is even, len(left) = len(right) = n//2
            if n is odd,  len(left) = n//2, len(right) = n//2+1
        2. merge sort the left half.
        3. merge sort the right half.
        4. merge the sorted left and right halves into a larger sorted subarray nums[low..high].
        """
        if lo >= hi:    # base case: subarray only has 0 or 1 item
            return 
        
        mid = (lo + hi) // 2                 # 1. divide subarray into two halves
        cls.helper(nums, aux, lo, mid)       # 2. merge sort the left half of the subarray.
        cls.helper(nums, aux, mid+1, hi)     # 3. merge sort the right half of the subarray.
        cls.merge(nums, aux, lo, mid, hi)    # 4. merge the sorted left and right halves into an subarray.

    @classmethod
    def topdown(cls, nums: list[int]) -> None: 
        """Top-down (recursive) merge sort 
        O(NlogN) for ALL cases
        Disadvantage: need extra space O(N) to do merge
        
        T(n) = T(n/2) + T(n/2) + n (n > 1)
        T(n) = 0                   (n = 1)
        T(n) is the number of comparisons required to sort an array of length n.
        T(n/2) for left and right halves, n for merge.
        Comparison:   O(NlogN) [1/2 NlogN, NlogN]
        Array access: O(NlogN) [0, 6 NlogN]
        """
        n = len(nums)
        aux = [0] * n     # O(N) extra space for an auxiliary array
        cls.helper(nums, aux, 0, n-1)

        assert cls.isSorted(nums, 0, n-1)
    
    @classmethod
    def bottomup(cls, nums: list[int]) -> None: 
        """Bottom-up (iterative) merge sort.
        O(NlogN) for ALL cases
        Disadvantage: need extra space O(N) to do merge

        Comparison:   O(NlogN) [1/2 NlogN, NlogN]   a reverse-sorted array of N = 2^k + 1 distinct keys uses approximately 1/2 NlogN - (k/2 - 1) compares.
        Array access: O(NlogN) [0, 6 NlogN]

        outer loop: O(logN) subarray size of ith iteration = 2^i, 
                            since subarray size of last iteration= N/2 = 2^(logN-1), 
                            number of iterations = logN
        
        inner loop: O(N)    1. O(N) divide array nums into n//size subarrays 
                                if n is even, length of all the n//size subarrays is size
                                if n is odd, length of n//size the subarrays is size, length of the last subarray is size-1
                            2. O(N) merges size-by-size subarray pairs into a larger subarray of length 2*size
                                T(merge) * number of pairs = O((2*size) * N//(2*size)) = O(N)
        """
        n = len(nums)
        aux = [0] * n       # O(N) extra space for an auxiliary array
        
        # O(NlogN) outer loop: iterates for logN times
        size = 1          # subarray size start from 1
        while size < n:
            # inner loop: O(N) divide and merge size-by-size subarray pairs
            for lo in range(0, n, 2*size):
                mid = min(lo + size - 1, n-1)
                hi = min(lo + 2*size - 1, n-1)
                cls.merge(nums, aux, lo, mid, hi)      
            size *= 2     # double the subarray size 

        assert cls.isSorted(nums, 0, n-1)

    

if __name__ == '__main__':
    print("Merge sort")

    nums = [9, 8, 7, 6, 5, 4, 3, 2, 1]
    print(f"Top-down Merge sort of nums = {nums}")
    MergeSort.topdown(nums)

    nums = [9, 8, 7, 6, 5, 4, 3, 2, 1]
    print(f"Bottom-up Merge sort of nums = {nums}")
    MergeSort.bottomup(nums)