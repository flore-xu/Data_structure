class Insertion:
    @classmethod
    def isSorted(cls, A: list[int], lo: int, hi: int) -> bool:
        """Check if A[lo, hi] is sorted"""
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
        """Worst case O(N^2) for reverse sorted input, best case O(N) for sorted input.
            Suitable for partially sorted array.

            An array is divided into 2 parts, the front part A[:i] is sorted and may be touched in the future,
                the back part A[i:] is unsorted.
            For back part, each time extract the first item A[i], pass from right to left, 
                plug into correct position in the front part if necessary. If necessary, the items in the front part will move rightward 
                for a step to leave one position for A[i] to plug in.
            
            Outer loop: O(N) N-1 times
            Inner loop: Depends on input.
                Worst case: reverse sorted array
                            comparison O(N^2) (N-1) + ... + 1 = N(N-1)/2
                            exchange   O(N^2) (N-1) + ... + 1 = N(N-1)/2
                Best case:  sorted array
                            comparison O(N)   1 + 1 + ... + 1 = N-1
                            exchange   0
                Average case: no-repeat random array
                            comparison and exchange O(N^2)
        """
        N = len(A)
        comparisonCounter = 0
        exchangeCounter = 0

        #  O(N) pass from leftend to rightend of array
        for i in range(1, N): 
            # Step 1 O(N): plug A[i] in A[:i] if necessary.
            for j in range(i, 0, -1):
                comparisonCounter += 1
                if A[j] < A[j-1]:
                    cls.swap(A, j, j-1)
                    exchangeCounter += 1
                else:
                    break 

            assert cls.isSorted(A, 0, i)
        
        print(f"N = {len(A)}, items are compared {comparisonCounter} times and swapped {exchangeCounter} times")
        
        assert cls.isSorted(A, 0, N-1)


if __name__ == '__main__':
    import random 
    print("insertion Sort")

    nums = [9, 8, 7, 6, 5, 4, 3, 2, 1]
    print(f"worst case, nums = {nums}")
    Insertion.sort(nums)

    nums = [1,2,3,4,5,6,7,8,9]
    print(f"best case, nums = {nums}")
    Insertion.sort(nums)
    
    nums = random.sample(range(1, 10), 9)
    
    print(f"Random array with distinct keys nums = {nums}")
    Insertion.sort(nums)