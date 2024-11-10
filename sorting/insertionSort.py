"""
insertion sort
1. insertion by exchange
2. insertion by right shift
code modified from Java https://www.comp.nus.edu.sg/~stevenha/cs2040/demos/SortingDemo.py and https://algs4.cs.princeton.edu/21elementary/Selection.java.html
"""

import random
class Insertion:
    @classmethod
    def isSorted(cls, nums: list[int], lo: int, hi: int) -> bool:
        """Check if nums[lo..hi] is sorted"""
        for i in range(lo+1, hi+1):
            if nums[i] < nums[i-1]:
                return False 
        return True

    @classmethod
    def swap(cls, nums: list[int], i: int, j: int) -> None:
        """Exchanges nums[i] and nums[j]"""
        nums[i], nums[j] = nums[j], nums[i]

    @classmethod
    def sort(cls, nums: list[int]) -> None: 
        """insertion sort (insertion by exchange)

           Worst case O(N^2) for reverse sorted input
           best case O(N) for sorted/partially sorted input.
           average case O(N^2) for randomized input

            An array is divided into 2 parts, left part nums[0..i-1] is sorted and may be touched in the future,
                right part nums[i..n-1] is unsorted.
            For right part, each time extract the first item nums[i],
                plug into correct position in left part, 
                the items in left part will shift rightward for a step to cede a position for nums[i] to plug in.
            
            Outer loop: O(N) N-1 times
            Inner loop: Depends on input.
                Worst case: reverse sorted array
                            comparison O(N^2) (N-1) + ... + 1 = N(N-1)/2
                            exchange   O(N^2) (N-1) + ... + 1 = N(N-1)/2

                Best case:  sorted array/array with all equal keys
                            comparison O(N)       1 + ... + 1 = N-1
                            exchange   0

                            partially sorted array. assume m is number of inversions. 
                            comparison [m, m+n]
                            exchange   m

                Average case: random array with distinct keys
                            comparison and exchange O(N^2)
        """
        N = len(nums)
        for i in range(1, N): 
            for j in range(i, 0, -1):
                if nums[j] < nums[j-1]:
                    cls.swap(nums, j, j-1)
                else:
                    break 
            assert cls.isSorted(nums, 0, i)
        assert cls.isSorted(nums, 0, N-1)


    @classmethod
    def sort(cls, nums: list[int]) -> None: 
        """insertion sort (insertion by right shift)
        """
        N = len(nums)
        for i in range(1, N): 
            num = nums[i]     # item to be insert
            for j in range(i-1, -1, -1):
                if nums[j] > num:
                    nums[j+1] = nums[j]
                else:
                    nums[j+1] = num  # insert item at j+1
                    break 
            assert cls.isSorted(nums, 0, i)
        assert cls.isSorted(nums, 0, N-1)


    @classmethod 
    def numOfInversions(cls, nums: list[int]) -> int:
        """O(nlogn) return the number of inversions in nums array, 
            which is the number of exchanges that would be performed by insertion sort for that array)
            
            An inversion is a pair of keys (nums[i], nums[j]) that are out of order in the array, i < j but nums[i] > nums[j]
	        e.g. E X A M P L E has 11 inversions: E-A, X-A, X-M, X-P, X-L, X-E, M-L, M-E, P-L, P-E, and L-E
        """
        n = len(nums)
        aux1 = nums.copy()  # use a copy of nums array so that original array won't be affected by sorting
        aux2 = [0] * n
        return cls.helper(nums, aux1, aux2, 0, n-1)


    @classmethod 
    def brute(cls, nums: list[int], lo: int, hi: int) -> int:
        """O(n^2) return the number of inversions in subarray nums[lo..hi]
           calculated by brute force
        """
        count = 0
        for i in range(lo, hi+1):
            for j in range(i+1, hi+1):
                if nums[j] < nums[i]:
                    count += 1
        return count 

    @classmethod
    def helper(cls, nums: list[int], aux1: list[int], aux2: list[int], lo: int, hi: int) -> int:
        """O(nlogn) return the number of inversions in the subarray nums[lo..hi]
           side effect: aux1[lo..hi] is sorted in ascending order
        
        n = hi-lo+1

        Base case: n = 0 or 1, then the subarray is already sorted, return 0

        subproblem: n >= 2
        1. divide subarray into two halves, left nums[low..mid] and right nums[mid+1..high]
            if n is even, len(left) = len(right) = n//2
            if n is odd,  len(left) = n//2, len(right) = n//2+1
        2. count the left half by merge sort
        3. count the right half by merge sort
        4. count and merge the sorted left and right halves into a larger sorted subarray nums[low..high].
        5. return total count 
        """
        if lo >= hi:    # base case: subarray only has 0 or 1 item
            return 0
        
        count = 0
        mid = (lo + hi) // 2                           # 1. divide subarray into two halves
        count += cls.helper(nums, aux1, aux2, lo, mid)       # 2. merge sort the left half of the subarray.
        count += cls.helper(nums, aux1, aux2, mid+1, hi)     # 3. merge sort the right half of the subarray.
        count += cls.merge(aux1, aux2, lo, mid, hi)    # 4. merge the sorted left and right halves into an subarray.
        
        assert count == cls.brute(nums, lo, hi)        # compare count with ground truth calculated by brute force
        return count 


    @classmethod
    def merge(cls, nums: list[int], aux: list[int], lo: int, mid: int, hi: int) -> int:
        """O(N) return the number of inversions in the unsorted subarray[lo, hi]
                by merging two sorted subarrays nums[lo, mid] and nums[mid+1, hi] into a larger sorted array nums[lo, hi]
                
            N = hi-lo+1
            nums: original array 
            aux: an auxiliary array of length N to store a copy of array nums
        """
        # precondition: nums[lo, mid] and nums[mid+1, hi] are sorted
        assert cls.isSorted(nums, lo, mid)
        assert cls.isSorted(nums, mid+1, hi)

        # optimization: skip merge if nums[lo, hi] is already sorted
        if mid+1 <= hi and nums[mid] <= nums[mid+1]:
            return 0
        
        count = 0
        # 1. O(N) merge two sorted subarrays into an auxiliary array   
        # nums[lo, mid] + nums[mid+1, hi] -> aux[lo, hi]
        # 3 pointers, i for aux[lo, hi], l for nums[lo, mid], r for nums[mid+1, hi]
        i, l, r = lo, lo, mid+1

        # when both subarrays are available, add smaller integer to auxiliary array
        while l <= mid and r <= hi:
            if nums[l] <= nums[r]:
                aux[i] = nums[l]
                l += 1
            else:
                aux[i] = nums[r]
                r += 1
                count += mid-l+1
            i += 1    
        
        # when one of subarray is run out, append leftover of another subarray to auxiliary array
        if l <= mid:
            aux[i:hi+1] = nums[l: mid+1]
        elif r <= hi:
            aux[i:hi+1] = nums[r: hi+1]

        # 2. O(N) copy auxiliary array back to original array
        nums[lo: hi+1] = aux[lo: hi+1]

        # postcondition: nums[lo, hi] is sorted
        assert cls.isSorted(nums, lo, hi)

        return count 


if __name__ == '__main__':
    print("Insertion Sort")

    nums = list(reversed(range(1, 10))) 
    print(f"Worst case, reverse sorted input = {nums}, # inversions = {Insertion.numOfInversions(nums)}")
    Insertion.sort(nums)

    nums = [2,1,3,4,5,6,9,8,7]
    print(f"Best case, partially sorted = {nums}, # inversions = {Insertion.numOfInversions(nums)}")
    Insertion.sort(nums)
    
    random.seed(123)
    nums = random.sample(range(1, 100), 10)
    print(f"Average case, random array with distinct keys nums = {nums}, # inversions = {Insertion.numOfInversions(nums)}")
    Insertion.sort(nums)