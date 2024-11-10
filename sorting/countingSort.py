"""
counting sort
- stable 1   code adapted from Java code https://www.cs.princeton.edu/courses/archive/spr15/cos226/lectures/51StringSorts.pdf
- stable 2   stable counting sort tab of https://visualgo.net/en/sorting
- unstable   simple counting sort tab of https://visualgo.net/en/sorting


"""

from itertools import accumulate
import random 

class Counting:
    @classmethod
    def isSorted(cls, nums: list[int], lo: int, hi: int) -> bool:
        """Check if nums[lo: hi+1] is sorted"""
        for i in range(lo+1, hi+1):
            if nums[i] < nums[i-1]:
                return False 
        return True


    @classmethod
    def sort(cls, nums: list[int]) -> None:
        """Counting sort (stable)
           condition: items are integers with small range
           T: O(N+r)
           S: O(N+r)    an auxiliary array of length N and a counter array of length r
           r is range of array  r = max(nums) - min(nums)

           this version of stable counting sort is adapted from Princeton COS226 slide
           https://www.cs.princeton.edu/courses/archive/spr15/cos226/lectures/51StringSorts.pdf
           which consistent with stable radix sort
        """
        n = len(nums)

        # 1. O(n) calculate range of array
        Min, Max = min(nums), max(nums)
        r = Max - Min   # range of array
        indexAt = lambda x: x-Min   # index of integer x, offset x by min so that all values are in the range [0, r-1], can handle negative integers
        cnt = [0] * (r+2) # initialize a counter array of length r+2
        aux = [0] * n  # initialize an auxiliary array of length n 
        
        # 2. O(n) count frequencies of items in array
        for num in nums:
            cnt[indexAt(num)+1] += 1

        # 3. O(r) calculate cumulative counts (prefix sum array over counter array)
        cnt = list(accumulate(cnt))
        
        # 4. O(n) output sorted item to auxiliary array
        for num in nums:  
            aux[cnt[indexAt(num)]] = num 
            cnt[indexAt(num)] += 1
        
        # 5. O(n) copy auxiliary array back to original array
        nums[::] = aux

        assert cls.isSorted(nums, 0, n-1)

    # @classmethod
    # def sort(cls, nums: list[int]) -> None:
    #     """Counting sort (stable)
    #        condition: items are integers with small range
    #        T: O(N+r)
    #        S: O(N+r)    an auxiliary array of length N and a counter array of length r
    #        r is range of array  r = max(nums) - min(nums)

    #        this version of stable counting sort is more common and adapted from leetcode and wiki
    #     """
    #     n = len(nums)

    #     # 1. O(n) calculate range of array
    #     Min, Max = min(nums), max(nums)
    #     r = Max - Min   # range of array
    #     indexAt = lambda x: x-Min   # index of integer x, offset x by min so that all values are in the range [0, r-1], can handle negative integers
    #     cnt = [0] * (r+1)   # initialize a counter array of length r+1
    #     aux = [0] * n       # initialize an auxiliary array of length n 
        
    #     # 2. O(n) count frequencies of items in array
    #     for num in nums:
    #         cnt[indexAt(num)] += 1  # offset value by min so that all values are in the range [0, r-1], can handle negative integers
        
    #     # 3. O(r) calculate cumulative counts (prefix sum array over counter array)
    #     cnt = list(accumulate(cnt))
        
    #     # 4. O(n) output sorted item to auxiliary array
    #     for num in reversed(nums):   # reverse order
    #         cnt[indexAt(num)] -= 1
    #         aux[cnt[indexAt(num)]] = num 
        
    #     # 5. O(n) copy auxiliary array back to original array
    #     nums[::] = aux

    #     assert cls.isSorted(nums, 0, n-1)

    # @classmethod
    # def sort(cls, nums: list[int]) -> None:
    #     """Counting sort (unstable)
    #        Assumption: r << n
    #                    input is in a fixed range (r) which is relatively small compared to number of items (n)
    #        Input types: integer.

    #        T: O(N+r)
    #        S: O(r)    a counter array of length r+1
    #        r is range of array  r = max(nums) - min(nums)
    #     """
    #     n = len(nums)

    #     # 1. O(N) calculate range of array
    #     Min, Max = min(nums), max(nums)
    #     r = Max - Min
    #     cnt = [0] * (r+1)  # initialize a counter array of length r+1
        
    #     # 2. O(N) count frequencies of items in array
    #     for num in nums:
    #         cnt[num - Min] += 1  # offset value by min to make index in range [0, r-1]
        
    #     # 3. O(r) output sorted item to nums array
    #     i = 0  # pointer iterates over nums array
    #     for num in range(Min, Max+1):
    #         while cnt[num - Min] > 0:
    #             nums[i] = num 
    #             i += 1
    #             cnt[num - Min] -= 1

    #     assert cls.isSorted(nums, 0, n-1)
  

if __name__ == '__main__':
    random.seed(123)
    print("Counting sort")
    
    nums = [random.randint(-5, 5) for _ in range(100)]   # all Integers are within [-5...5]  range = 10
    print(f"input is in small range = {max(nums)-min(nums)}: {nums}")

    Counting.sort(nums)

    print(nums)