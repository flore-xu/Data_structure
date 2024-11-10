
"""
binary search

adapted from Python 3.10 bisect library method bisect_left and bisect_right
"""

from typing import Iterable

class Bisect:
    @classmethod
    def bisect_left(cls, nums: Iterable[int], target: int, l: int=0, r: int=None, key: callable=lambda x: x) -> int:
        """
        Return the index `i` where to insert item target in a sorted array A

            A = [key(nums[i]) for i in range(l, r)]  must be non-decreasing

            all element in A[:i] have value < target, and all elements in A[i:] have value >= target. 

            if target already appears in A, i points just at the leftmost target already there.

            If not, return the index where it would be if it were inserted in order.

        @params
            nums: the sorted array, or search range if `key` parameter is given
            l, r: lower and upper bound of the slice of array to be searched.
                searching range [l, r], l default to 0, r default to len(nums)
            target: the item to be insert in sorted array A
            key: check function, default to lambda x: x

            usage of key parameter
            1. customize check function
            2. reverse sorted array
            
            ```
            def bisect_left_customized(nums: list[int], target: int) -> int:
                l, r = 1, len(nums)
                check = lambda x: nums[x] * nums[x-1]

                # don't forget l plus, because the returned index is 0-based indexing
                return l + bisect.bisect_left(range(l, r), target, key=check)
            ```

            ```
            def bisect_left_desc(nums: list[int], target: int) -> int:
                l, r = 0, len(nums)-1
                check = lambda x: nums[x]

                # don't forget r minus
                return r - bisect.bisect_left(range(r, l-1, -1), target, key=check)
            ```
        Examples:

        nums = [], target = 1
        bisect_left(nums, target) = 0

        nums = [1, 3, 3, 3, 5, 7], target = -1
        bisect_left(nums, target) = 0

        nums = [1, 3, 3, 3, 5, 7], target = 3
        bisect_left(nums, target) = 1

        nums = [1, 3, 3, 3, 5, 7], target = 3
        bisect_left(nums, target, 2) = 2

        nums = [1, 3, 3, 3, 5, 7], target = 4
        bisect_left(nums, target) = 4

        nums = [1, 3, 3, 3, 5, 7], target = 8
        bisect_left(nums, target) = 6
        """
        if l < 0:
            raise ValueError('l must be non-negative')
        
        if r is None:
            r = len(nums)

        while l < r:        # exit loop when l = r
            mid = (l+r)//2  # calculate index of median 
            # Python has no issue of integer overflow and bitwise r shift is not necessarily faster than division
            # so mid = l + (r-l) >> 1 is equivalent to mid = (l+r)//2, while for Java and C, the latter is preferred

            if key(nums[mid]) < target:      # if nums is a decreasing array, if nums[mid] > target
                l = mid+1   # next searching range [mid+1, r]
            else: 
                r = mid     # next searching range [l, mid]

            # if nums[mid] == target:   # if nums array has not duplicate numbers
            #   return mid

        return l    # when exit loop, l = r, can return either l or r

    @classmethod
    def bisect_left(cls, nums: Iterable[int], target: int, l: int=0, r: int=None, key: callable=lambda x: x) -> int:
        """
        another implementation of bisect_left with searching range [l, r-1]
        """
        if l < 0:
            raise ValueError('l must be non-negative')
        
        if r is None:
            r = len(nums) - 1   # Note we subtract 1 here compared to version 1 of bisect_left

        while l <= r:        # exit loop when l > r  Note we add equal to here
            mid = (l+r)//2
            if key(nums[mid]) < target:  # if nums is a decreasing array, if nums[mid] > target
                l = mid+1   # next searching range [mid+1, r]
            else: 
                r = mid-1     # next searching range [l, mid-1]     Note that we subtract 1 here
            # if nums[mid] == target:
                # return mid  # if nums array has not duplicate numbers

        return l    # when exit loop, l > r = mid, must return l rather than r


    @classmethod
    def bisect_right(cls, nums: Iterable[int], target: int, l: int=0, r: int=None, key: callable=lambda x: x) -> int:
        """
        Return the index `i` where to insert item target in a sorted array A

            A = [key(nums[i]) for i in range(l, r)]  must be non-decreasing

            all elements in A[:i] have value <= target, and all elements in A[i:] have value > target. 

            if target already appears in the array, i points just after the rightmost target already there.

            If not, return the index where it would be if it were inserted in order.

            
        @params
        nums: the sorted array, or search range if key parameter is given
        l, r: lower and upper bound of the slice of array to be searched.
            searching range [l, r-1], l default to 0, r default to len(nums)
        target: the item to be insert in sorted array A
        key: check function, default to lambda x: x

        Examples:

        nums = [], target = 1
        bisect_right(nums, target) = 0

        nums = [1, 3, 3, 3, 5, 7], target = -1
        bisect_right(nums, target) = 0

        nums = [1, 3, 3, 3, 5, 7], target = 3
        bisect_right(nums, target) = 4          # l = 0, r = 6

        nums = [1, 3, 3, 3, 5, 7], target = 3
        bisect_right(nums, target, 2) = 3       # l = 2, r = 6

        nums = [1, 3, 3, 3, 5, 7], target = 4
        bisect_right(nums, target) = 4

        nums = [1, 3, 3, 3, 5, 7], target = 8
        bisect_right(nums, target) = 6

        nums = [1,3,5,7,9,11,13,15], target = 15
        l, r = 1, len(nums)
        check = lambda x: nums[x] * nums[x-1]
        ans = l + bisect_right(range(l, r), target, key=check) = 3
        """

        if l < 0:
            raise ValueError('l must be non-negative')
        
        if r is None:
            r = len(nums)
        
        while l < r:
            mid = (l+r)//2
            if key(nums[mid]) <= target: # Note: we add equal to here compared to bisect_left
                # if nums is a decreasing array, if nums[mid] >= target
                l = mid+1
            else: 
                r = mid

        return l        # when exit loop, l equals to r, can return either l or r


    @classmethod
    def bisect_right(cls, nums: Iterable[int], target: int, l: int=0, r: int=None, key: callable=lambda x: x) -> int:
        """
        another implementation of bisect_right with searching range [0, r-1]
        """
        if l < 0:
            raise ValueError('l must be non-negative')
        
        if r is None:
            r = len(nums) - 1 # Note that we subtract 1 here compared to version 1 of bisect_right 
        
        while l <= r:         # Note we add equal to here
            mid = (l+r)//2
            # if nums is a decreasing array, if nums[mid] >= target
            if key(nums[mid]) <= target: # Note: we add equal to here compared to bisect_left
                l = mid+1
            else: 
                r = mid-1

        return l            # when exit loop, l = mid > r, must return l or mid rather than r


    @classmethod
    def bisect_real(cls, l: float, r: float, precision: float, check: callable):
        """
        T: O(log(1/p))  binary search in real field

        proof: n is the number of iterations to halve the search space
        1/2^n <= p, take log base 2 of both sides we have n >= log(1/p)
        """
        while r - l > precision:
            mid = l + (r - l) / 2
            if check(mid):
                l = mid
            else:
                r = mid
        return l


