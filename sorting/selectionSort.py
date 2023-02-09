class Selection:
    @classmethod
    def isSorted(cls, A: list[int], lo: int, hi: int) -> bool:
        """check if A[lo: hi+1] is sorted"""
        for i in range(lo+1, hi):
            if A[i] < A[i-1]:
                return False 
        return True

    @classmethod
    def swap(cls, A: list[int], i: int, j: int) -> None:
        A[i], A[j] = A[j], A[i]

    @classmethod
    def MinSort(cls, A: list[int]) -> None: 
        """ O(N^2) for ALL cases.

            An array is divided into 2 parts, the front part A[:i] is sorted and untouched, the back part A[i:] is unsorted.
            For back part, pass from left to right, repeatedly SELECT the smallest item and swap it with the first item A[i+1].
            Outer loop: O(N) N-1 times
            Inner loop: comparison O(N^2)  (N-1) + ... + 1 = N(N-1)/2
                        exchange   O(N)    1 + 1 + ... + 1 = N-1
        """
        N = len(A)
        comparisonCounter = 0
        exchangeCounter = 0

        # O(N) pass from leftend to rightend of array
        # after each pas for i, A[:i] is sorted
        for i in range(N-1):    
            # Step 1 O(N): for unsorted part, pass from i to N-1, find the smallest index of min item in A[i:]   
            min_idx = i             # min_idx = A.index(min(A[i:]))
            for j in range(i+1, N):
                if A[j] < A[min_idx]:
                    min_idx = j  
                comparisonCounter += 1
            
            # Step 2 O(1): swap smallest item with i-th item
            cls.swap(A, min_idx, i)
            exchangeCounter += 1
            assert cls.isSorted(A, 0, i)
        
        print(f"Min sort, N = {len(A)}, items are compared {comparisonCounter} times and swapped {exchangeCounter} times")
        assert cls.isSorted(A, 0, N-1)

    @classmethod 
    def MaxSort(cls, A: list[int]) -> None:
        """ O(N^2) for ALL cases.
            
            An array is divided into 2 parts, the front part A[:i] is unsorted, the back part A[i:] is sorted and untouched.
            For front part, pass from right to left, repeatedly SELECT the largest item and swap it with the last item A[i-1].
            Outer loop: O(N) N-1 times
            Inner loop: comparison O(N^2)  (N-1) + ... + 1 = N(N-1)/2
                        exchange   O(N)    1 + 1 + ... + 1 = N-1
        """
        N = len(A)
        comparisonCounter = 0
        exchangeCounter = 0

        # O(N) pass from rightend to leftend of array
        # After each pass for i, A[i:] is sorted
        for i in range(N-1, 0, -1):

            # Step 1 O(N): for unsorted part, pass from i to 0, find the smallest index of max item in A[:i+1] 
            max_id = i                    # max_id = A.index(max(A[:i+1]))
            for j in range(i-1, -1, -1): 
                if A[j] > A[max_id]:
                    max_id = j 
                comparisonCounter += 1
            
            # Step 2 O(1): swap largest item with i-th item
            cls.swap(A, max_id, i)
            exchangeCounter += 1
            assert cls.isSorted(A, i, N-1)

        print(f"Max sort, N = {len(A)}, items are compared {comparisonCounter} times and swapped {exchangeCounter} times")
        assert cls.isSorted(A, 0, N-1)

if __name__ == '__main__':
    print("Selection sort")

    nums = [9, 8, 7, 6, 5, 4, 3, 2, 1]
    print(f"nums = {nums}")
    Selection.MinSort(nums)
    
    Selection.MaxSort(nums) 
     