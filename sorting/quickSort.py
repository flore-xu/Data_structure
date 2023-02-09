# Code modified from https://visualgo.net/en/sorting
# Random quick sort implementation by randomly choose an item as pivot
import random 
class Quick:
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
    def sort(cls, A: list[int]) -> None:
        """in-place quick sort using a small auxiliary stack
        a divide-and-conquer paradigm
            worst case O(N^2)   inputs that are sorted/reverse sorted/with same items.
            Best case: O(N log N)  rare when partition always splits the array into two equal halves, like Merge Sort
                                e.g., A = [4, 1, 3, 2, 6, 5, 7]
        """
        def helper(A: list[int], low: int, high: int) -> None: 
            """Partitioning O(N) recursively divide subarray A[low, high] into 2 parts and sort each part independently

            - before partition, choose the first entry as pivot A[low] = p
            - during partition, remaining array A[low+1, high] is divided into 3 regions:
                1. S1 = A[low+1, m] where items <= p  
                2. S2 = A[m+1, k-1] where items >= p  
                3. Unknown = A[k, high] where items are wait to be assigned to either S1 or S2
            - after partition, subarray A[low, high] is divided into 2 regions:
                1. exchange A[low] and A[m], so pivot p is in its final position
                2. S1 = A[low, m-1] where items <= p  
                3. S2 = A[m+1, high] where items >= p
            """
            # partition O(N): repeatedly divide subarray A[low, high] of size > 1 into 3 regions
            if low < high:
                nonlocal compareCounter, swapCounter
                # 1. Before partition: choose the first index to be pivot
                # (Random Part) randomly choose an index between [low, high] to be pivot
                # r = random.choice(range(low, high+1)) 
                # swap(A, low, r)
                p = A[low] 
                m = low             # initialize middle index of S1 and S2 
                
                # remaining items [low+1, high] are divided into 3 regions:
                # S1: [low+1, m] where items are <= p  
                # S2: [m+1, k-1] (may empty) where items are >= p  
                # Unknown [k, high] where items are wait to be assigned to either S1 or S2

                # 2. During partition: expore unknown region O(N)
                # for each item A[k] in unknown region, compare A[k] with p
                for k in range(low+1, high+1): 
                    compareCounter += 1
                    # case 1: A[k] > p: put A[k] into S2
                    # case 2: A[k] < p: put A[k] into S1
                    # case 3: A[k] = p: throw a coin, if head: put A[k] into S1, if tail: S2
                    if A[k] < p or (A[k] == p and random.randrange(2) == 0):
                        m += 1  # increment m
                        cls.swap(A, k, m)
                        swapCounter += 1
                
                # final step, swap pivot = A[low] and A[m] to put pivot in the middle of S1 and S2
                # A[low...m...high] -> A[low...m-1], pivot, A[m+1...high]
                cls.swap(A, low, m)
                swapCounter += 1
                
                # 3. After partition, A[m] = pivot is in its correct place after partition
                helper(A, low, m-1) # recursively sort left subarray
                helper(A, m+1, high) # recursively sort right subarray

        n = len(A)
        compareCounter = 0
        swapCounter = 0
        helper(A, 0, n - 1) 
        print(f"N = {n}, compare {compareCounter} times, exchange {swapCounter} times")
        assert cls.isSorted(A, 0, n-1)

if __name__ == '__main__':
    nums = [7, 6, 5, 4, 3, 2, 1]
    print(f"worst case, nums = {nums}")
    Quick.sort(nums)

    nums =  [4, 1, 3, 2, 6, 5, 7]
    print(f"best case, nums = {nums}")
    Quick.sort(nums)