# Code modified from Java https://algs4.cs.princeton.edu/23quicksort/Quick.java.html
# Random quick sort implementation by randomly shuffle array before sorting
import random

class RandomQuick:
    @classmethod
    def isSorted(cls, A: list[int], lo: int, hi: int) -> bool:
        """Check if array[lo, hi] is sorted"""
        for i in range(lo+1, hi):
            if A[i] < A[i-1]:
                return False 
        return True

    @classmethod
    def swap(cls, A: list[int], i: int, j: int) -> None:
        """Exchanges A[i] and A[j]"""
        A[i], A[j] = A[j], A[i]

    @classmethod
    def partition(cls, A: list[int], lo: int, hi: int) -> int:
        """in-place partitioning subarray A[lo, hi] to 2 regions: A[lo, j-1] <= A[j] <= A[j+1, hi]
        return index j
        """
        i, j = lo+1, hi
        pivot = A[lo]    # choose the first item to be pivot
        while True:
            # scan from left
            for i in range(lo+1, hi+1):
                if A[i] >= pivot: # make sure left pointer do not run off the left part
                    break 
            # scan from right
            for j in range(hi, lo-1, -1):
                if A[j] <= pivot: # make sure right pointer do not run off the right part
                    break 
            # stop loop if pointers cross
            if i >= j:
                break 
            # swap 2 pointers
            cls.swap(A, i, j)
        
        # put pivot in the middle of 2 regions
        cls.swap(A, lo, j)

        return j

    @classmethod
    def sort(cls, A: list[int]) -> None:
        """In-place Random quick sort using a small auxiliary stack
           Expected O(N log N) for ALL cases
        """
        def helper(A: list[int], lo: int, hi: int) -> None:
            """In-place random quick sort subarray A[low, high]
            recursively divide subarray A[low, high] into 2 parts and sort each part independently"""
            if hi <= lo: # base case
                return 

            j = cls.partition(A, lo, hi)
            helper(A, lo, j-1)
            helper(A, j+1, hi)
            assert cls.isSorted(A, lo, hi)
        
        n = len(A)

        # randomly shuffle array before sorting
        # # An alternate way to preserve randomness is to choose a random item for partitioning within partition().
        random.shuffle(A) 
        helper(A, 0, n-1)
        
        assert cls.isSorted(A, 0, n-1)

if __name__ == '__main__':
    print("Random quick sort")

    nums = [7, 6, 5, 4, 3, 2, 1]
    print(f"nums = {nums}")
    RandomQuick.sort(nums) 

    nums = [4, 1, 3, 2, 6, 5, 7]
    print(f"nums = {nums}")
    RandomQuick.sort(nums)