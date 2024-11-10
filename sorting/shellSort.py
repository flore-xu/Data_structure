"""
shell sort

code modified from Java https://algs4.cs.princeton.edu/21elementary/Shell.java.html
"""

import random
class ShellSort:
    @classmethod
    def isSorted(cls, nums: list[int], lo: int, hi: int) -> bool:
        """Check whether nums[lo..hi] is sorted"""
        for i in range(lo+1, hi+1):
            if nums[i] < nums[i-1]:
                return False 
        return True

    @classmethod
    def isHsorted(cls, nums: list[int], h: int) -> bool:
        """check whether array is h-sorted"""
        for i in range(h, len(nums)):
            if nums[i] < nums[i-h]:
                return False 
        return True

    @classmethod
    def swap(cls, nums: list[int], i: int, j: int) -> None:
        """Exchanges nums[i] and nums[j]"""
        nums[i], nums[j] = nums[j], nums[i]

    @classmethod
    def sort(cls, nums: list[int]) -> list[int]:
        """Shell sort

            An extension of Insertion Sort.
            Shell sort makes array h-sorted because Insertion sort is faster on partially-sorted inputs
            
            Time complexity depends on gap sequence.
            gap sequence: any increment sequence of h that starts with 1
            (Knuth, 1973) gap sequence = 1, 4, 13, 40, 121, 364,..., 3*i+1
            worst case O(N^3/2) average case O(N^4/3)  best case O(NlogN)
        
            Starts from a large value of h, make the array h-sorted, 
                reducing h by a certian amount, repeat until h is 1. 
            array is h-sorted if all subsequences of every hth item is sorted.
            h is the length of gap in an array.
            h of a sorted array is 1. 
        """
        n = len(nums)
        # start from a large h
        h = 1 
        while h < n / 3:
            h = 3 * h + 1
        while h >= 1:
            # insertion sort to make array h-sorted
            for i in range(h, n):
                # plug nums[i] in nums[h..i-1] if necessary
                for j in range(i, h-1, -h): # step changes from -1 to -h
                    if nums[j] < nums[j-h]:
                        cls.swap(nums, j, j-h)
                    else:
                        break 
            assert cls.isHsorted(nums, h)
            h //= 3     # reduce h by a certain amount
        cls.isSorted(nums, 0, n-1)


if __name__ == '__main__':
    print("Shell sort (Knuth, 1973 version)")
    random.seed(123)
    nums = random.sample(range(100), 100)
    print(f"Average case, random input with distinct keys = {nums}")
    ShellSort.sort(nums)