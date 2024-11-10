"""
bucket sort

code modified from wiki
determine bucket size and number of buckets https://leetcode.cn/problems/maximum-gap/solutions/498577/python3-tong-pai-xu-by-yanghk/
"""

class Bucket:
    @classmethod
    def isSorted(cls, nums: list[int], lo: int, hi: int) -> bool:
        """Check if nums[lo..hi] is sorted"""
        for i in range(lo+1, hi+1):
            if nums[i] < nums[i-1]:
                return False 
        return True

    @classmethod
    def sort(cls, nums: list[int]) -> None:
        """Bucket sort. 
           T: best O(n+k)           items are uniformly distributed over k buckets
              average O(n+n^2/k+k)  items are randomly distributed over k buckets. simplifies to O(n) when k = Θ(n)
              worst O(n^2)  all the items are placed in a single bucket
           
           S: O(n+k)
           
           assumption: uniform distribution. 
                       items are uniformly distributed in the range [min, max]
           input types: integer, float, string

            bucket size is chosen to make data uniformly distributed in each bucket.
            ideally each bucket will contain n//k items, worst case 0 or n

            input is integer and float
            **set bucket size to be equal**: size = max(1, r//(n-1)) 
            - number of buckets k = r//size + 1
            - ith item will be put into bucket of index (nums[i] - min) // size
            - range of jth bucket is half-closed [min+j*size, min+(j+1)*size)  
            
            input is string
            e.g., all the items are consist of lowercase English letters
            **set number of buckets k = 26**
            - ith item will be put into bucket of index ord(nums[i][0]) - ord('a')
            - bucket sizes are not equal, size of jth bucket is the number of strings starting with letter chr(ord('a')+j)
            - range of jth bucket:  all the strings starting with letter chr(ord('a')+j)
        """
        n = len(nums)

        # 1. O(n) determine bucket size and number of buckets
        Min, Max = min(nums), max(nums)
        r = Max - Min  # range of array
        size = max(1, r // (n-1))   # bucket size
        k = r // size + 1                  # number of buckets
        buckets = [[] for _ in range(k)]    # initialize k empty buckets

        # 2. O(n) distribute items into corresponding bucket
        for num in nums:
            bucket_id = (num - Min) // size
            buckets[bucket_id].append(num)

        # 3. O(n) concatenate items from buckets and output to original array 
        idx = 0
        for bucket in buckets:
            bucket.sort()      # sort individual bucket O(n/k log(n/k))
            m = len(bucket)
            nums[idx: idx+m] = bucket
            idx += m 

        print(f"N = {n}, range = {r}, use {k} buckets, bucket size = {size}")
        buckets = {f"[{Min + i * size}, {Min + (i+1) * size})" : buckets[i] for i in range(k)}
        print(f"buckets = {buckets}")
        
        assert cls.isSorted(nums, 0, n-1)

if __name__ == '__main__':
    print("Bucket sort")

    nums = [9, 8, 7, 6, 4, 3, 1]   # numbers are nearly uniformly distributed in range [1, 9]
    print(f"input is nearly uniformly distributed = {nums}")
    # N = 7, range = 8, use 9 buckets, bucket size = 1
    # buckets = {'[1, 2)': [1], '[2, 3)': [], '[3, 4)': [], '[4, 5)': [4], '[5, 6)': [5], '[6, 7)': [6], '[7, 8)': [7], '[8, 9)': [8], '[9, 10)': [9]}

    Bucket.sort(nums)