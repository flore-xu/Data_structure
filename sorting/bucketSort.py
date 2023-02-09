import math

class Bucket:
    @classmethod
    def isSorted(cls, A: list[int], lo: int, hi: int) -> bool:
        """Check if A[lo: hi+1] is sorted"""
        for i in range(lo+1, hi):
            if A[i] < A[i-1]:
                return False 
        return True

    @classmethod
    def sort(cls, A: list[int]) -> None:
        """Bucket sort. 
           O(N+r) r is range of array
           Suitable for array whose numbers are uniformly distributed in the range

            Try to make data uniformly distributed in each bucket.
            1. bucket size = `max(1, r // (n-1))` left closed right open
            2. number of buckets `k = r // size + 1`
            3. Which bucket should item i be put in? `index = (nums[i] - min) // size` 
        """
        n = len(A)
        Max, Min = max(nums), min(nums)
        # range of array
        r = Max - Min 

        # bucket size
        size = math.ceil(r / (n-1))
        # number of buckets
        k = r // size + 1
        # initialize k empty buckets
        buckets = [[] for _ in range(k)]

        # Scatter O(N) put item in the corresponding bucket
        for item in nums:
            buckets[(item - Min) // size].append(item)
        
        # sort each bucket independently by subroutine sort algo
        for i in range(k):
            buckets[i].sort()

        # Gather: concatenate items from all the buckets to original array 
        idx = 0
        for i in range(k):
            for j in range(len(buckets[i])):
                A[idx] = buckets[i][j]
                idx += 1

        print(f"N = {n}, use {k} buckets, bucket size = {size}")

        buckets = {f"[{Min + i * size}, {Min + (i+1) * size})" : buckets[i] for i in range(k)}
        
        print(f"buckets = {buckets}")
        
        assert cls.isSorted(A, 0, n-1)

if __name__ == '__main__':
    print("Bucket sort")
    # numbers are nearly uniformly distributed in range[1, 9]
    nums = [9,8,7,6,5,4,1]
    print(f"nums = {nums}")

    Bucket.sort(nums)