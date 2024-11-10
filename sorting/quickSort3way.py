"""
3-way quick sort and 3-way quick select

Code modified from Java https://algs4.cs.princeton.edu/23quicksort/Quick3way.java.html
"""
import random

class Quick3way:
    @classmethod
    def isSorted(cls, nums: list[int], lo: int, hi: int) -> bool:
        """Check if array[lo..hi] is sorted"""
        for i in range(lo+1, hi+1):
            if nums[i] < nums[i-1]:
                return False 
        return True

    @classmethod
    def swap(cls, nums: list[int], i: int, j: int) -> None:
        """Exchanges nums[i] and nums[j]"""
        nums[i], nums[j] = nums[j], nums[i]

    @classmethod
    def partition3way(cls, nums: list[int], lo: int, hi: int, pivot_id: int=None) -> tuple[int, int]:
        """expected O(n) 3-way partition
            in-place divide subarray nums[lo..hi] into 3 regions: 
                left: nums[lo..lt-1]  < pivot
                middle: nums[lt..gt] = pivot  
                right: nums[gt+1..hi] > pivot
            
            @params
            lo: lower bound of subarray
            hi: upper bound of subarray
            pivot_id: index of pivot, default to lo
            
            return lt, gt
            lt (less than): lower bound of middle region
            gt (greater than): upper bound of middle region
            
            n = hi-lo 
        """
        # 1. choose a pivot. 
        if pivot_id == None:
            # pivot_id = lo                              # normal 3-way quick sort
            pivot_id = random.choice(range(lo, hi+1))  # preferred. randomized 3-way quick sort
        cls.swap(nums, lo, pivot_id)   # move pivot to the start of the array
        pivot = nums[lo]  
        
        # 2. divide subarray[lo..hi] into 3 regions
        # 3 pointers
        # i: start of unsolved region
        # lt, gt: start and end of middle region

        # implementation 1 (preferred)
        # more general and can be adapted to scenario where the pivot is not necessarily at the lo position
        # e.g., leetcode problem 75. Sort Colors
        i = lo  # change here
        lt, gt = lo, hi   
        while i <= gt:
            if nums[i] < pivot:
                cls.swap(nums, i, lt)
                lt += 1
                i += 1      # change here
            elif nums[i] > pivot:
                cls.swap(nums, i, gt)
                gt -= 1
            else:
                i += 1
        return lt, gt
    
        # implementation 2
        i = lo+1    # change here
        lt, gt = lo, hi   
        while i <= gt:
            if nums[i] < pivot:
                cls.swap(nums, i, lt)
                lt += 1     # change here
            elif nums[i] > pivot:
                cls.swap(nums, i, gt)
                gt -= 1
            else:
                i += 1
        return lt, gt 
    


    @classmethod
    def helper(cls, nums: list[int], lo: int, hi: int) -> None:
        """recursively 3-way quick sort subarray nums[lo..hi]
           
           base case: n = 0 or 1, subarray is sorted

           subproblem: n >= 2
           1. 3-way partition: divide subarray nums[lo..hi] into 3 parts: left nums[lo..lt-1], middle nums[lt..gt], right nums[gt+1..hi]
           2. 3-way quick sort left part nums[lo..lt-1]
           3. 3-way quick sort right part nums[gt+1..hi]

           middle part nums[lt..gt] does not need to be processed further as all its elements are already in their final position.
        """
        if lo >= hi:   # base case: n = 0 or 1, subarray is sorted
            return 

        lt, gt = cls.partition3way(nums, lo, hi)   # 1. 3-way partition: divide subarray nums[lo..hi] into 3 parts: left nums[lo..lt-1], middle nums[lt..gt], right nums[gt+1..hi]
        cls.helper(nums, lo, lt-1)                 # 2. 3-way quick sort left part nums[lo..lt-1]
        cls.helper(nums, gt+1, hi)                 # 3. 3-way quick sort right part nums[gt+1..hi]
        
        assert cls.isSorted(nums, lo, hi)

    @classmethod
    def sort(cls, nums: list[int]) -> None:
        """3-way quick sort
            
            extension of quick sort. suitable for input with large amount of duplicates

            worst case: O(N^2)   3-way partition divide array into 3 regions of imbalanced length   
            Best case:  O(NlogN)  entropy-optimal: expected O(N) for input with many duplicates and 3-way partition always divide subarray into 3 regions of almost equal-length  (n/3, n/3, n/3)
        """
        n = len(nums)
        cls.helper(nums, 0, n-1)
        
        assert cls.isSorted(nums, 0, n-1)

    @classmethod
    def quickSelect3way(cls, nums: list[int], lo: int, hi: int, k: int):
        """expected O(n) 3-way quick select
           rearrange nums array such that nums[k] is the k+1th smallest element (not kth distinct smallest)
           and nums[0..k-1] <= nums[k] <= nums[k+1..n-1]
           e.g., call quickSelect with k = (n-1)//2 will make nums[k] be median
        """
        # base case, array has 0 or 1 items, is sorted
        if lo >= hi:
            return 

        # 1. 3-way partition nums[lo..hi]
        lt, gt = cls.partition3way(nums, lo, hi)

        # 2. recursively 3-way quick select left or right half
        if gt < k:
            cls.quickSelect3way(nums, gt+1, hi, k)
        else:
            cls.quickSelect3way(nums, lo, lt, k)
            

    @classmethod
    def kthSmallest(cls, nums: list[int], k: int) -> int:
        """
        O(n) return the kth smallest element in array
        e.g., nums = [1, 2, 2, 3, 4, 4, 5], k = 3, return 2

        Note: kth smallest is not kth smallest distinct
        """
        n = len(nums)
        cls.quickSelect3way(nums, k-1, 0, n-1)
        return nums[k-1]

    @classmethod
    def findKthLargest(cls, nums: list[int], k: int):
        """
        O(n) return the kth largest element in array

        e.g., nums = [1, 2, 2, 3, 4, 4, 5], k = 3, return 4
        Note: kth largest is not kth largest distinct
        """
        n = len(nums)
        cls.quickSelect3way(nums, 0, n-1, n-k)
        return nums[n-k]


if __name__ == '__main__':
    random.seed(123)
    #======================================================
    print("3-way Quick sort")

    nums = list(range(1, 100))
    print(f"worst case, sorted input = {nums}")
    Quick3way.sort(nums) 

    nums = list(reversed(range(1, 100)))
    print(f"worst case, reverse sorted input = {nums}")
    Quick3way.sort(nums)

    nums = random.sample(range(1, 100), 10) + [50] * 90
    print(f"best case, input with many duplicates = {nums}")
    Quick3way.sort(nums)

    #======================================================
    print("3-way Quick select")

    nums = [4, 1, 3, 6, 5, 7] + [2] * 100
    k = 3
    print(f"kth smallest element: {Quick3way.kthSmallest(nums, k)}")
    print(f"kth largest element: {Quick3way.kthLargest(nums, k)}")
