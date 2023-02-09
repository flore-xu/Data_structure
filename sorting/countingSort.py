class Counting:
    @classmethod
    def isSorted(cls, A: list[int], lo: int, hi: int) -> bool:
        """Check if A[lo: hi+1] is sorted"""
        for i in range(lo+1, hi):
            if A[i] < A[i-1]:
                return False 
        return True
    
    @classmethod
    def sort(cls, A: list[int]) -> None:
        """O(N+r). O(N) if r is small. r is range of array 
        """
        n = len(A)

        # 1. initialize an output array of length n
        output = [0] * n

        # 2. find min and max of array
        low, high = min(A), max(A)   # O(N)
        r = high - low  
        
        # 3. initialize a Counter of length r + 1
        counter = [0] * (r + 1) 
        
        # 4. store count of each item in Counter[item-min]
        for item in A:  # O(N)
            counter[item - low] += 1  # offset index by min
        
        # 5. calculate cumulative sum of Counter
        for i in range(1, r+1):  # O(r)
            counter[i] += counter[i-1]
        
        # 6. fill the output with sorted item
        for item in reversed(A):
            output[counter[item-low] - 1] = item 
            counter[item-low] -= 1

        # 7. copy output back to array A 
        for i in range(n):   # O(N)
            A[i] = output[i] 
        
        assert cls.isSorted(A, 0, n-1)
  

if __name__ == '__main__':
    print("Counting sort")
    # all Integers are within [-5..5]
    nums = [5, 4, 3, 3, 2, 2, -1, -2, -3, -4, -5]
    print(f"nums = {nums}")

    Counting.sort(nums)