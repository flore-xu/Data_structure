from collections.abc import Iterable
from typing import Any

class BinarySearchST:
    """Ordered symbol table implementation via binary search in an ordered array
       Underlying data structure is 2 parallel arrays, a sorted keys array and a value array.
       The heart is rank() method, which tells us where to find the key in the keys array. 
    """
    INIT_CAPACITY = 2
    def __init__(self) -> None:
        self.n = 0
        self.Keys = [None] * self.INIT_CAPACITY    # ordered key array
        self.vals = [0] * self.INIT_CAPACITY     # value array

    def size(self) -> int:
        """return number of key-value pairs in the symbol table"""
        return self.n  
    
    def _resize(self, capacity: int) -> None:
        """Resize the underlying keys array and value array to the specified capacity"""
        assert capacity >= self.n 
        N = len(self.Keys) 
        self.Keys += [''] * (capacity - N)
        self.vals += [0] * (capacity - N)
        # tmpk, tmpv = [''] * capacity, [0] * capacity 

        # tmpk[:self.n], tmpv[:self.n] = self.Keys[: self.n], self.vals[: self.n]
        # self.Keys, self.vals = tmpk, tmpv  

    def is_empty(self) -> bool:
        """return True if the symbol table is empty, False otherwise"""
        return self.size() == 0 

    def contains(self, key: Any) -> bool:
        """return True if the symbol table contains the specified key
           
           @param key: the key
           @return True if contains, False otherwise
           @raise ValueError if key is None
        """
        if key is None:
            raise ValueError("argument to contains() is None") 
        
        return self.get(key) != None


    def get(self, key: Any) -> int:
        """return the value associated with the given key in the symbol table

            @param key: the key
            @return the value associated with the given key if the key exists
                    None if key is not
            @raise ValueError if key is None
        """
        if key is None:
            raise ValueError("argument to get() is None")
        if self.is_empty():
            return None 
        i = self.rank(key)
        if i < self.n and self.Keys[i] == key:
            return self.vals[i]
        return None 

    def rank(self, key: Any) -> int:
        """binary search O(logN) to find position index for key to put in the table 
            @param key: the key
            @return the number of keys in the symbol table that strictly less than the specified key
            @raise ValueError if key is None
        """
        if key is None:
            raise ValueError("argument to rank() is None")

        lo, hi = 0, self.n-1
        while lo <= hi:
            mid = (lo + hi) // 2 
            if key < self.Keys[mid]:
                hi = mid - 1 
            elif key > self.Keys[mid]:
                lo = mid + 1 
            else:
                return mid 
        return lo 

    def put(self, key: Any, val: int) -> None:
            """O(N) Inserts specified key-value pairs into symbol table.
            if key already exists, overwrites the old value with new value
            if specified value is None, delete the key and its value
                
                @param key: the key
                @return the value
                @raise ValueError if key is None
            """
            if key is None:
                raise ValueError("First argument in put() if None")

            if val is None:
                self.delete(key)
                return  
            
            # O(logN) get position index for key to put in the table
            i = self.rank(key)

            ## key is already in table
            if i < self.n and key == self.Keys[i]:
                self.vals[i] = val 
                return 

            ## put new key-value pair
            if self.n == (N := len(self.Keys)):
                self._resize(2*N)
            
            # O(N) move array[i:] rightward for a step to array[i+1:] to leave space for key to put
            self.Keys[i+1 : self.n+1] = self.Keys[i : self.n]
            self.vals[i+1 : self.n+1] = self.vals[i : self.n]
            self.Keys[i], self.vals[i] = key, val 
            self.n += 1 

            assert self._check()

    def delete(self, key: Any) -> None:
        """removes specified key and its value from symbol table

            @param key: the key
            @raise ValueError if key is None
        """
        if key is None:
            raise ValueError("argument in delete() is None")
        if self.is_empty():
            return 
        
        # position index to find key in table 
        i = self.rank(key)

        # key is not in table 
        if i == self.n or self.Keys[i] != key:
            return 

        # key is in table, move array[i+1:] leftward for a step to overwrite array[i:]
        self.Keys[i : self.n] = self.Keys[i+1 : self.n+1]
        self.vals[i : self.n] = self.vals[i+1 : self.n+1]
        self.n -= 1

        # to avoid loitering
        self.Keys[self.n] = self.vals[self.n] = None

        # resize if 1/4 full
        N = len(self.Keys)
        if self.n > 0 and self.n == N // 4:
            self._resize(N//2)
        
        assert self._check()

    #***************************************************************************
    #*  Ordered symbol table methods
    #***************************************************************************
    
    def deleteMin(self) -> None:
        """Removes the smallest key and its value from symbol table
           raise IndexError if the symbol table is empty
        """
        if self.is_empty():
            raise IndexError("Symbol table underflow error") 
        
        self.delete(self.minKey())

    def deleteMax(self) -> None:
        """Removes the largest key and its value from symbol table
           raise IndexError if the symbol table is empty
        """
        if self.is_empty():
            raise IndexError("Symbol table underflow error") 
        
        self.delete(self.maxKey())

    def minKey(self) -> str:
        """Returns the smallest key in the symbol table
           raise IndexError if the symbol table is empty
        """
        if self.is_empty():
            raise IndexError("Symbol table underflow error")

        return self.Keys[0] 

    def maxKey(self) -> str:
        """Returns the largest key in the symbol table
           raise IndexError if the symbol table is empty
        """
        if self.is_empty():
            raise IndexError("Symbol table underflow error")

        return self.Keys[self.n-1]  

    def select(self, k: int) -> str:
        """Returns the kth smallest key in this symbol table

           @param k: rank 
           @return the kth smallest key
           raise IndexError if k is not between 0 and self.n-1
        """
        if not (0 <= k < self.size()):
            raise IndexError(f"called select() with invalid k {k}")
        
        return self.Keys[k]

    def floor(self, key: Any) -> str:
        """Returns the largest key that smaller than or equal to key in this symbol table

           @param k: rank 
           @return the largest key <= key
           @raise ValueError if key is None
           @raise IndexError if there is no such key
        """
        if key is None:
            raise ValueError("argument in floor() is None")

        i = self.rank(key)

        if i < self.n and key == self.Keys[i]:
            return self.Keys[i]
        if i == 0:
            raise IndexError("argument 'key' to floor() is too small")
        else:
            return self.Keys[i-1]


    def ceiling(self, key: Any) -> str:
        """Returns the smallest key that greater than or equal to key in this symbol table

           @param k: rank 
           @return the smallest key >= key
           @raise ValueError if key is None
           @raise IndexError if there is no such key
        """
        if key is None:
            raise ValueError("argument in ceiling() is None")

        i = self.rank(key)

        if i == self.n:
            raise IndexError("argument 'key' to ceiling() is too large")
        else:
            return self.Keys[i]

    def keySize(self, lo: str, hi: str) -> int:
        """Returns the number of keys in the symbol table in the specified range
            
            @param lo: lower bound  hi: upper bound both inclusive 
            @return the number of keys
            @raise ValueError if key is None
        """
        if lo is None:
            raise ValueError("first argument to keySize() is None")
        if hi is None:
            raise ValueError("second argument to keySize() is None")
        if lo > hi:
            return 0
        if self.contains(hi):
            return self.rank(hi) - self.rank(lo) + 1
        else:
            return self.rank(hi) - self.rank(lo)


    def keys(self) -> Iterable:
        """Returns all keys in the symbol table as an Iterable
            to iterate over all of the keys in the symbol table named st
            use for-loop: for key in st.keys()
        """
        # return self.Keys[ : self.n]
        return self.rangeKeys(self.minKey(), self.maxKey())
    

    def rangeKeys(self, lo: str, hi: str) -> Iterable:
        """Returns all keys in a given range in the symbol table as an Iterable

            @param lo: lower bound  hi: upper bound both inclusive 
            @return all the keys in [lo, hi] as iterable
            @raise ValueError if lo or hi is None
            to iterate over all of the keys in the symbol table named st
            use for-loop: for key in st.rangeKeys()
        """
        if lo == None:
            raise ValueError("first argument to keySize() is None")
        if hi == None:
            raise ValueError("second argument to keySize() is None")
        res = []
        if lo > hi:
            return res 
        
        for i in range(self.rank(lo), self.rank(hi)):
            res.append(self.Keys[i])
        
        if self.contains(hi):
            res.append(self.Keys[self.rank(hi)])

        return res
    
    #***************************************************************************
    #*  Check internal invariants.
    #***************************************************************************
    def _check(self):
        return self._isSorted() and self._rankCheck()
    
    def _isSorted(self) -> bool:
        """Check if array is in ascending order"""
        for i in range(1, self.size()):
            if self.Keys[i] < self.Keys[i-1]:
                return False 
        return True 
    
    def _rankCheck(self) -> bool:
        """Check if rank(select(i)) = i"""
        for i in range(self.size()):
            if i != self.rank(self.select(i)):
                return False 
        for key in self.keys():
            if key != self.select(self.rank(key)):
                return False 
        return True 

if __name__ == '__main__':
# Unit test: Execute when the module is not initialized from an import statement.
    
    input = [('L', 11), ('P', 10),('M', 9),('X', 7),('H', 5),('C', 4), ('R', 3), ('A', 8), ('E', 12), ('S', 0)]
    
    st = BinarySearchST()       # initialize a Binary Search Symbol Table
    
    for key, val in input:      # put key-value pairs from input into table
        st.put(key, val)

    st.delete('E')              # delete a key-value pair
    
    for key in st.keys():    # print all the key-value pairs in the table
        print(key, ' ', st.get(key)) 
 