"""
2-way quick sort and 2-way quick select

partition
1. two pointers (head and tail)        Code modified from https://leetcode.cn/problems/kth-largest-element-in-an-array/solutions/307351/shu-zu-zhong-de-di-kge-zui-da-yuan-su-by-leetcode-/ and https://algs4.cs.princeton.edu/23quicksort/Quick.java.html
2. sliding window                      Code modified from https://www.comp.nus.edu.sg/~stevenha/cs2040/demos/SortingDemo.py
"""
import random

class Quick:
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
    def partition(cls, nums: list[int], lo: int, hi: int, pivot_id: int=None) -> int:
        """expected O(n) in-place divide subarray nums[lo..hi] into 3 regions:
                left: nums[lo..mid-1]  <= pivot
                middle: nums[mid] = pivot  
                right: nums[mid+1..hi] >= pivot

            implementation 1: two pointers (head and tail)
            see below for implementation2 sliding window
            two implementations use different ways to handle the case when key equal to pivot
            
            n = hi-lo+1
            
            @param
            lo: lower bound of nums array
            hi: upper bound of nums array
            pivot_id: index of pivot, default to lo
            
            return 
            mid: index of pivot at final correct position


            sorted input: n+1 compares
            reverse sorted input: n compares
        """
        # 1. choose a pivot
        if pivot_id is None:   # if pivot_id is not given
            # pivot_id = lo                              # (normal quick sort) choose the first item to be pivot
            pivot_id = random.choice(range(lo, hi+1))  # preferred (Random quick sort) randomly choose an integer in the subarray to be pivot
        cls.swap(nums, lo, pivot_id)    # move pivot to the start of the array
        pivot = nums[lo]
       
        # 2. divide subarray into 3 regions
        # l: end of left half
        # r: start of right half
        l, r = lo-1, hi+1

        # stop when the scan indices cross
        while l < r:
            # (1) (IMPORTANT) increment l and decrement r to avoid TLE O(N^2) on items equal to pivot
            l += 1      
            r -= 1
            # (2) -> left scan: stop on key equal to pivot
            while nums[l] < pivot:
                l += 1
            # (3) <- right scan: stop on key equal to pivot
            while nums[r] > pivot:
                r -= 1
            # (4) swap two items stop the scan, nums[l] >= pivot while nums[r] <= pivot
            if l < r: 
                nums[l], nums[r] = nums[r], nums[l]
        return r  # l >= r


    @classmethod
    def partition(cls, nums: list[int], lo: int, hi: int, pivot_id: int=None) -> int:
        """expected O(n) in-place divide subarray nums[lo..hi] into 3 regions
            implementation2  sliding window
        """
        # 1. choose a pivot
        if pivot_id is None:   # if pivot_id is not given
            # pivot_id = lo                              # (normal quick sort) choose the first item to be pivot
            pivot_id = random.choice(range(lo, hi+1))  # preferred (Random quick sort) choose an integer in the subarray uniformly at random to be pivot
        cls.swap(nums, lo, pivot_id)    # move pivot to the start of the array
        pivot = nums[lo]

        # 2. divide subarray into 3 regions
        # i: start of unsolved region
        # l: end of left half
        l = lo 
        for i in range(lo+1, hi+1): 
            # optimization to avoid TLE O(N^2) on array with duplicates
            # if nums[i] = pivot, throw a coin, if head: add to left half, if tail: add to right half
            if nums[i] < pivot or (nums[i] == pivot and random.randrange(2) == 0):
                l += 1
                cls.swap(nums, i, l)   
        # put pivot in the middle of 2 halves. pivot is at its final position
        cls.swap(nums, lo, l)
        return l
         

    @classmethod
    def helper(cls, nums: list[int], lo: int, hi: int) -> None:
        """recursively quick sort subarray nums[low, high]
           
           base case: n = 0 or 1, subarray is sorted

           subproblem: n >= 2
           1. divide subarray into 3 parts: left half nums[lo..mid-1], pivot nums[mid], right half nums[mid+1..hi]
           2. quick sort left half nums[lo..mid-1]
           3. quick sort right half nums[mid+1..hi]
        """
        if lo >= hi:   # base case: n = 0 or 1, subarray is sorted
            return 

        mid = cls.partition(nums, lo, hi)   # 1. partition: divide subarray into 3 parts: left half nums[lo..mid-1], pivot nums[mid], right half nums[mid+1..hi]
        cls.helper(nums, lo, mid-1)         # 2. quick sort left half nums[lo..mid-1]
        cls.helper(nums, mid+1, hi)         # 3. quick sort right half nums[mid+1..hi]
        
        assert cls.isSorted(nums, lo, hi)

    @classmethod
    def sort(cls, nums: list[int]) -> None:
        """quick sort

            Normal quick sort: worst case: O(N^2)   input is sorted/reverse sorted/all items are equal/pivot is always chosen as the smallest/largest items
                                                    compares N^2/2
                                                    partition divide array into 2 halves of imbalanced length
                                                    e.g., nums = [1, 2, 3, 4, 5, 6, 7] pivot = nums[0] = 1, left half [] right half [2, 3, 4, 5, 6, 7]
                                                    size of subproblem only reduced by 1

                               Best case: O(NlogN)  input is element-distinct
                                                    compares 2NlogN exchange 1/3NlogN
                                                    partition always splits the array into two halves of almost equal length, like Merge Sort
                                                    e.g., nums = [4, 1, 3, 2, 6, 5, 7] pivot = nums[0] = 4, left half [1,3,2] right half [6,5,7]
            Randomized quick sort: expected O(NlogN) for ALL cases
        """
        n = len(nums)
        random.shuffle(nums)    # randomly shuffle array before sorting, an alternate way is in partition().
        cls.helper(nums, 0, n-1)
        
        assert cls.isSorted(nums, 0, n-1)

    @classmethod
    def quickSelect(cls, nums: list[int], lo: int, hi: int, k: int):
        """expected O(n) quick select

           k: indexing from 0

           rearrange nums array such that nums[k] is the k+1th smallest element (not kth distinct smallest)
	       and nums[0, k-1] <= nums[k] <= nums[k+1, n-1]
           
           e.g., call quickSelect with k = (n-1)//2 will make nums[k] be median
        """
        # base case: array only has 0 or 1 items, already sorted
        if lo >= hi:
            return 

        # 1. 2-way partition nums[lo..hi]
        mid = cls.partition(nums, lo, hi)

        # 2. recursively quick select left or right half
        if mid < k:
            cls.quickSelect(nums, mid+1, hi, k)     # quick select right half
        else:
            cls.quickSelect(nums, lo, mid, k)     # quick select left half

    @classmethod
    def kthSmallest(cls, nums: list[int], k: int) -> int:
        """
        O(n) return the kth smallest element in array
        e.g., nums = [1, 2, 2, 3, 4, 4, 5], k = 3, return 2

        Note: kth smallest is not kth smallest distinct
        """
        n = len(nums)
        cls.quickSelect(nums, k-1, 0, n-1)
        return nums[k-1]
    

    @classmethod
    def kthLargest(cls, nums: list[int], k: int) -> int:
        """
        O(n) return the kth largest element in array

        e.g., nums = [1, 2, 2, 3, 4, 4, 5], k = 3, return 4
        Note: kth largest is not kth largest distinct
        """
        n = len(nums)
        cls.quickSelect(nums, n-k, 0, n-1)
        return nums[n-k]
    

if __name__ == '__main__':
    random.seed(123)
    #======================================================
    print("Quick sort")

    nums = list(range(1, 100))
    print(f"worst case, sorted input = {nums}")
    Quick.sort(nums)

    nums = list(reversed(range(1, 100)))
    print(f"worst case, reverse sorted input = {nums}")
    Quick.sort(nums)

    nums = random.sample(range(1, 100), 10) + [50] * 90
    print(f"worst case, input with many duplicates = {nums}")
    Quick.sort(nums) 

    nums = random.sample(range(1, 10000), 100)
    print(f"best case, random input with distinct keys = {nums}")
    Quick.sort(nums)

    #======================================================
    print("Quick select")
    nums = [1, 2, 2, 3, 4, 4, 5]
    k = 3
    print(f"kth smallest element: {Quick.kthSmallest(nums, k)}")
    print(f"kth largest element: {Quick.kthLargest(nums, k)}")