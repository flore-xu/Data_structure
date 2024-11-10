"""
bubble sort

code modified from https://www.comp.nus.edu.sg/~stevenha/cs2040/demos/SortingDemo.py
"""

class Bubble:

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
        """bubble sort
           Worst case O(N^2) for reverse sorted input
           best case O(N) for sorted input.
           
           the number of swaps = the number of inverted pairs in the array

            An array is divided into 2 parts, left part nums[0..i-1] is unsorted, right part nums[i..n-1] is sorted and untouched.
            For left part, pass from left to right, repeatedly SWAP with next item if item > next item, 
            so the largest item will finally at nums[i-1], like a bubble emerges water surface (left is bottom, right is surface).
            
            Outer loop: O(N) N-1 times
            Inner loop: Depends on input.
                Worst case: comparison O(N^2) (N-1) + ... + 1 = N(N-1)/2
                            exchange   O(N^2) (N-1) + ... + 1 = N(N-1)/2
                Best case:  comparison O(N)       1 + ... + 1 = N-1
                            exchange   O(1)       0
        """
        N = len(nums)
        # O(N) pass from rightend to leftend of array
        # after each pass for i, nums[i..n-1] is sorted
        for i in range(N-1, 0, -1):  # O(n)
            swapped = False
            # Step 1 O(N): for unsorted part nums[0..i-1], swap adjacent pairs until nums[i] is max(nums[0..i])
            for j in range(i):
                if nums[j] > nums[j+1]:
                    cls.swap(nums, j, j+1)
                    swapped = True
            assert cls.isSorted(nums, i, N-1)   # nums[i..n-1] is sorted
            # optimization: no swapping means array is sorted, immediately exit 
            if not swapped:
                break
        assert cls.isSorted(nums, 0, N-1)


if __name__ == '__main__':
    nums = list(reversed(range(1, 100)))
    print(f"worst case, reverse sorted input = {nums}")
    Bubble.sort(nums)

    nums = list(range(1, 100))
    print(f"best case, sorted input = {nums}")
    Bubble.sort(nums)