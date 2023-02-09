class Bubble:

    @classmethod 
    def isSorted(cls, A: list[int], lo: int, hi: int) -> bool:
        """Check if A[lo: hi+1] is sorted"""
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
            
            An array is divided into 2 parts, the front part A[:i] is unsorted, the back part A[i:] is sorted and untouched.
            For front part, pass from left to right, repeatedly SWAP with next item if item > next item, 
                so the largest item will finally at A[i-1], like a bubble emerges water surface.
            
            Outer loop: O(N) N-1 times
            Inner loop: Depends on input.
                Worst case: comparison O(N^2) (N-1) + ... + 1 = N(N-1)/2
                            exchange   O(N^2) (N-1) + ... + 1 = N(N-1)/2
                Best case:  comparison O(N)   1 + 1 + ... + 1 = N-1
                            exchange   0
        """
        N = len(A)
        compareCounter = 0
        exchangeCounter = 0

        # O(N) pass from rightend to leftend of array
        # After each pass for i, A[i:] is sorted
        for i in range(N-1, 0, -1):
            swapped = False
            # Step1 O(N): for unsorted part, pass from 0 to i-1, swap if item is larger than its next item
            for j in range(i-1):
                compareCounter += 1
                if A[j] > A[j+1]:
                    cls.swap(A, j, j+1)
                    swapped = True
                    exchangeCounter += 1
            assert cls.isSorted(A, i, N-1)   # By now, the largest item will be at the last position
            
            # optimization, if array is already sorted, stop sorting immediately
            if not swapped:
                break
        
        print(f"N = {len(A)}, items are compared {compareCounter} times and exchanged {exchangeCounter} times")
        assert cls.isSorted(A, 0, N-1)


if __name__ == '__main__':
    nums = [9, 8, 7, 6, 5, 4, 3, 2, 1]
    print(f"worst case, nums = {nums}")
    Bubble.sort(nums)

    nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    print(f"best case, nums = {nums}")
    Bubble.sort(nums)