"""
radix sort
- LSD radix sort for integers
- MSD radix sort for strings

code adapted from Java code https://www.cs.princeton.edu/courses/archive/spr15/cos226/lectures/51StringSorts.pdf
"""

from itertools import accumulate

class lsdRadix:
    @classmethod
    def isSorted(cls, nums: list[int], lo: int, hi: int) -> bool:
        """Check if nums[lo..hi] is sorted"""
        for i in range(lo+1, hi+1):
            if nums[i] < nums[i-1]:
                return False 
        return True
    
    @classmethod
    def countingSort(cls, nums: list[int], aux: list[int], exp: int) -> None:
        """O(n+b) counting sort nums array based on the log(exp)th digit
            
            counting sort is chosen as subroutine for sorting individual digit
            because it's stable and efficient for small range O(n+r) here r = b

            @param 
            nums: array to be sorted
            aux: auxiliary array
            exp: exponential number

            Steps
            1. create 10 buckets (for digit 0-9)
            2. for each item in array
                move item into respective bucket based on log(exp)th digit
            3. iterates over buckets from smallest digit to largest digit
               restore items in each bucket to array 
        """
        b = 10                          # base, 10 for decimal
        cnt = [0] * (b+1)                   # initialize b empty buckets
        indexAt = lambda x: (x//exp) % b  # function to get logexp th digit of integer x 

        # 1. O(n) count frequencies of items in nums array
        for num in nums:        
            cnt[indexAt(num)+1] += 1
        
        # 2. O(b) calculate cumulative count
        cnt = list(accumulate(cnt))
        
        # 3. O(n) output sorted num to auxiliary array
        for num in nums:
            aux[cnt[indexAt(num)]] = num 
            cnt[indexAt(num)] += 1 

        # 4. O(n) copy auxiliary array back to original array
        nums[:] = aux

    @classmethod 
    def sort(cls, nums: list[int]) -> None:
        """stable LSD Radix sort for integers
           T: O(d(N+b)) S: O(N+b)
           
           order: short keys come before longer keys, and then keys of the same length are sorted lexicographically.

           Assumption: d << n << r. input with large range but of few digits. 
           input types: integers
           
        d: max number of digits of nums[i]
        N: number of items in an array
        b: base (radix) for representing item, i.e., the number of unique digits, b = 10 for decimal with digit 0-9
             
        Steps
        1. padding
            treat each item as a string of d digits
            pad integers with length < d with leading zeros. e.g., d=4, item='32' -> '0032'

        2. sort items digit by digit
            from least significant digit (LSD) to the most significant digit (MSD)
        """ 
        n = len(nums)
        aux = [0] * n
        Max = max(nums)    # O(n) use max number in array to find max digit size
        b = 10
        exp = 1
        d = 0           # max digit size in array

        # O(d) pass from rightmost digit (LSD) to leftmost digit (MSD)
        while Max // exp: 
            # O(n+b) sort array based on log(exp)th digit
            cls.countingSort(nums, aux, exp)
            exp *= b
            d += 1

        assert cls.isSorted(nums, 0, n-1)
        print(f"range = {nums[-1]-nums[0]}, digit size = {d}")


class msdRadix:
    @classmethod
    def isSorted(cls, nums: list[int], lo: int, hi: int) -> bool:
        """Check if nums[lo..hi] is sorted"""
        for i in range(lo+1, hi+1):
            if nums[i] < nums[i-1]:
                return False 
        return True
    
    @classmethod
    def countingSort(cls, strs: list[str], aux: int, lo: int, hi: int, i: int) -> None:
        """O(n+b) counting sort strs subarray[lo..hi] based on the ith character
            
            counting sort is chosen as subroutine for sorting individual character
            because it's stable and efficient for small range O(n+r) here r = b

            @param 
            strs: array to be sorted
            aux: auxiliary array
            i: index of target character  e.g., i = 0 for 'a' of 'apple'
            
            Steps
            1. create 256 buckets (for ASCII characters)
            2. for each item in array
                move item into respective bucket based on ith character
            3. iterates over buckets from smallest character to largest character
               restore items in each bucket to array 
        """
        b = 26              # base for ASCII characters
        cnt = [0] * (b+2)    # initialize a counter array of length b+2, cnt[1] for character out of range
        indexAt = lambda s: ord(s[i])-ord('a') if i < len(s) else -1  # function to get ith character of string s

        # 1. O(n) count frequencies of items in strs array
        for s in strs[lo: hi+1]:
            cnt[indexAt(s)+2] += 1
        
        # 2. O(b) calculate cumulative count
        cnt = list(accumulate(cnt))  # length of counter array becomes b+2
        
        # 3. O(n) output sorted strs to auxiliary array
        for s in strs[lo: hi+1]:
            aux[cnt[indexAt(s)+1]] = s  
            cnt[indexAt(s)+1] += 1 

        # 4. O(n) copy auxiliary array back to original array
        strs[lo:hi+1] = aux[:hi-lo+1]
        
        return cnt 

 
    @classmethod
    def helper(cls, strs: list[str], aux: list[str], lo: int, hi: int, i: int) -> None:
        """O(n) MSD radix sort of subarray strs[lo..hi] from ith character
        n = hi-lo+1
        i: index of target character (from 0 to d-1)

        Base case: n = 0 or 1, subarray is already sorted.

        subproblem: n >= 2
        1. sort subarray strs[lo..hi] based on the ith character
        2. recursively sort array based on the i-1 th character
        """
        if lo >= hi:    # base case: subarray is already sorted.
            return 
        
        b = 26
        cnt = cls.countingSort(strs, aux, lo, hi, i)                  # 1. sort array based on the ith character
        for j in range(b):
            cls.helper(strs, aux, lo+cnt[j], lo+cnt[j+1]-1, i+1)      # 2. recursively sort subarray in individual bucket based on the i+1 th character


    @classmethod 
    def sort(cls, strs: list[str]) -> None:
        """stable MSD Radix sort for strings in lexicographic order
           T: O(d(N+b))  S: O(N+b)
           
           Assumption: d << n << r. input with large range but of few characters. 
           input types: strings of variable-length
           
        d: max length of strs[i]
        N: number of items in an array
        b: base (radix) for representing item, i.e., the number of unique characters
            b = 26 for lowercase English letters a-z
            b = 128 for ASCII characters
             
        Steps
        1. padding
            treat each item as a string of d characters
            pad strings with length < d with trailing spaces (or any character that comes before 'a'). 
            e.g., d = 4, s = 'ab' -> 'ab  '

        2. sort items character by character
            from most significant character (MSD) to the least significant character (LSD)
        """ 
        n = len(strs)
        aux = [''] * n 
        cls.helper(strs, aux, 0, n-1, 0)

        assert cls.isSorted(strs, 0, n-1)


if __name__ == '__main__':
    print("LSD Radix sort for integers")
    # r=9679, d=4
    nums = [3221, 1, 10, 9680, 577, 9420, 7, 5622, 4793, 2030, 3138, 82, 2599, 743, 4127]
    print(f"integer array in large range but with few digits = {nums}")
    lsdRadix.sort(nums)


    print("MSD Radix sort for strings")
    # r=26, d=9
    strs = ["she", "sells", "seashells", "by", "the", "sea", "shore", "the", "shells", "she", "sells", "are", "surely", "seashells"]

    print(f"string array with few characters = {strs}")
    msdRadix.sort(strs)
    print(f"sorted = {strs}")