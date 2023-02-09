class Radix:
    count = 0

    @classmethod
    def isSorted(cls, A: list[int], lo: int, hi: int) -> bool:
        """Check if A[lo: hi+1] is sorted"""
        for i in range(lo+1, hi):
            if A[i] < A[i-1]:
                return False 
        return True
    
    @classmethod
    def countingSort(cls, A: list[int], aux: list[int], exp: int) -> None:
        """Sort array based on the log(exp)th digit
            O(n+b)  b is base for number, b = 10 for decimal 

            @param A: array to be sorted
                   aux: auxillary array
                   exp: exponential number
        """
        counter = [0] * 10

        for item in A:      # O(n)
            cls.count += 1
            digit = (item // exp) % 10 
            counter[digit] += 1
        
        for i in range(1, 10):  # O(b)
            counter[i] += counter[i - 1]
        
        for item in reversed(A):  # O(n)
            cls.count += 1
            digit = (item // exp) % 10
            aux[counter[digit] - 1] = item 
            counter[digit] -= 1 

        # copy auxillary array back to original array
        # NOTE: A = output does nothing
        for i in range(len(A)):   # O(n)
            cls.count += 1
            A[i] = aux[i]

    @classmethod 
    def sort(cls, A: list[int]) -> None:
        """Radix sort. O(d(N+b))
           d: maximum number of digits in a number
           N: number of items in an array
           b: base (radix) for representing number, i.e., the number of unique digits. 
                decimal is known as base 10.

           Suitable for input with large range but of few digits.
           Only applies to integers, fixed size strings, floating points
             
           Sorts the array of numbers digit-by-digits
                 from the least significant digit (LSD) to the most significant digit (MSD)
           Can use counting/insertion/bubble/bucket sort as a subroutine to sort individual digits. 
        """ 
        n = len(A)
        Max = max(A)    # O(n) use max number in array to find max digit size
        exp = 1 
        aux = [0] * n 
        d = 0           # max digit size in array

        # O(d): pass from rightmost digit (LSD) to leftmost digit (MSD)
        while Max // exp > 0: 
            # sort array based on dth digit, Can use counting/bucket sort as a subroutine
            cls.countingSort(A, aux, exp)  # O(n + b)  b = 10
            exp *= 10
            d += 1

        assert cls.isSorted(A, 0, n-1)
    
        print(f"Digit size d = {d}, N = {n}, b = 10, array access {cls.count} times")

if __name__ == '__main__':
    print("Radix sort")

    nums = [3221, 1, 10, 9680, 577, 9420, 7, 5622, 4793, 2030, 3138, 82, 2599, 743, 4127]
    print(f"nums = {nums}")
    Radix.sort(nums)