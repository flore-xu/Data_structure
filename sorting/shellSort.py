class ShellSort:
    @classmethod
    def isSorted(cls, A: list[int], lo: int, hi: int) -> bool:
        """Check if A[lo: hi+1] is sorted"""
        for i in range(lo+1, hi):
            if A[i] < A[i-1]:
                return False 
        return True

    @classmethod
    def isHsorted(cls, A: list[int], h: int) -> bool:
        """check if array is h-sorted"""
        for i in range(h, len(A)):
            if A[i] < A[i-h]:
                return False 
        return True

    @classmethod
    def swap(cls, A: list[int], i: int, j: int) -> None:
        """Exchanges A[i] and A[j]"""
        A[i], A[j] = A[j], A[i]

    @classmethod
    def sort(cls, A: list[int]) -> list[int]:
        """Suitable for partially sorted array.
            An extension of Insertion Sort.
            Time complexity depends on gap sequence.
            (Knuth, 1973) gap sequence = 1, 4, 13, 40, 121, 364,...
            best case O(NlogN) worst case O(N^3/2)
        
            Starts from a large value of h, make the array h-sorted, 
                reducing h by a certian amount, repeat until h is 1. 
            A array is h-sorted if all sublists of every hth item is sorted.
            h is the length of gap in an array.
            A sorted array's h = 1. 
        """
        compareCounter = 0
        exchangeCounter = 0 
        
        n = len(A)

        # start from a large h
        h = 1 
        while h < n / 3:
            h = 3 * h + 1
        
        while h >= 1:
            # insertion sort to make array h-sorted
            for i in range(h, n):
                # plug A[i] in A[h:i] if necessary
                for j in range(i, h-1, -h): # step changes from -1 to -h
                    compareCounter += 1
                    if A[j] < A[j-h]:
                        cls.swap(A, j, j-h)
                        exchangeCounter += 1
                    else:
                        break 
            
            assert cls.isHsorted(A, h)
            h //= 3     # reduce h by a certain amount
        
        cls.isSorted(A, 0, n-1)
        print(f"N = {len(A)}, items are compared {compareCounter} times and swapped {exchangeCounter} times")


if __name__ == '__main__':
    import random 
    print("Shell sort (Knuth, 1973 version)")
    nums = random.sample(range(100), 100)
    print(f"nums = {nums}")
    ShellSort.sort(nums)