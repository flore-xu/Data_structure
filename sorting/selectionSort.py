"""
selection sort
2 implementations
1. min sort
2. max sort
"""
class Selection:
    @classmethod
    def isSorted(cls, nums: list[int], lo: int, hi: int) -> bool:
        """check if nums[lo..hi] is sorted"""
        for i in range(lo+1, hi+1):
            if nums[i] < nums[i-1]:
                return False 
        return True

    @classmethod
    def swap(cls, nums: list[int], i: int, j: int) -> None:
        nums[i], nums[j] = nums[j], nums[i]

    @classmethod
    def MinSort(cls, nums: list[int]) -> None: 
        """ O(N^2) for ALL cases.

            An array is divided into 2 parts, left part nums[0..i-1] is sorted and untouched, right part nums[i..n-1] is unsorted.
            For back part, pass from left to right, repeatedly SELECT the smallest item and swap it with the first item nums[i].
            Outer loop: O(N) N-1 times
            Inner loop: comparison O(N^2)  (N-1) + ... + 1 = N(N-1)/2
                        exchange   O(N)        1 + ... + 1 = N-1
        """
        N = len(nums)
        # O(N) pass from leftend to rightend of array
        # after each pass for i, nums[0..i-1] is sorted
        for i in range(N-1):    
            # Step 1 O(N): for unsorted part, find the smallest index of min item in nums[i..n-1]   
            min_idx = i             # min_idx = nums.index(min(nums[i:]))
            for j in range(i+1, N):
                if nums[j] < nums[min_idx]:
                    min_idx = j  
            
            # Step 2 O(1): swap smallest item with i-th item
            if nums[min_idx] < nums[i]:
                cls.swap(nums, min_idx, i)
            assert cls.isSorted(nums, 0, i)
        assert cls.isSorted(nums, 0, N-1)

    @classmethod 
    def MaxSort(cls, nums: list[int]) -> None:
        """ O(N^2) for ALL cases.
            
            An array is divided into 2 parts, left part nums[0..i] is unsorted, right part nums[i+1..n-1] is sorted and untouched.
            For front part, pass from right to left, repeatedly SELECT the largest item and swap it with the last item nums[i-1].
            Outer loop: O(N) N-1 times
            Inner loop: comparison O(N^2)  (N-1) + ... + 1 = N(N-1)/2
                        exchange   O(N)    1 + 1 + ... + 1 = N-1
        """
        N = len(nums)
        # O(N) pass from rightend to leftend of array
        # After each pass for i, nums[i..n-1] is sorted
        for i in range(N-1, 0, -1):
            # Step 1 O(N): for unsorted part, find the largest index of max item in nums[0..i] 
            max_id = i                    # max_id = nums.index(max(nums[:i+1]))
            for j in range(i-1, -1, -1): 
                if nums[j] > nums[max_id]:
                    max_id = j 
            
            # Step 2 O(1): swap largest item with i-th item
            if nums[max_id] > nums[i]:
                cls.swap(nums, max_id, i)
            assert cls.isSorted(nums, i, N-1)
        assert cls.isSorted(nums, 0, N-1)

if __name__ == '__main__':
    print("Selection sort")

    nums = [9, 8, 7, 6, 5, 4, 3, 2, 1]
    print(f"nums = {nums}")
    Selection.MinSort(nums)
    
    Selection.MaxSort(nums) 
     