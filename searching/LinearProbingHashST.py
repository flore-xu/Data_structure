"""
   Execution:    python LinearProbingHashST.py < input.txt

   Data files:   https://algs4.cs.princeton.edu/33balanced/tinyST.txt

   A symbol table implemented using a linear probing hash.
   This is the 2-3 version.

   % more tinyST.txt
   S E A R C H E X A M P L E

   % python LinearProbingHashST.py < tinyST.txt
   A 8
   C 4
   E 12
   H 5
   L 11
   M 9
   P 10
   R 3
   S 0
   X 7
"""
from typing import Any

class LinearProbingHashST:
    INIT_CAPACITY = 4

    def __init__(self, m: int=0) -> None:
        self.n = 0                        # # number of key-value pairs in the hash table
        self.m = m or self.INIT_CAPACITY  # hash table size  12.5% < α = N/M < 50%
        self.Keys = [None for _ in range(self.m)]
        self.vals = [None for _ in range(self.m)]

    def hash(self, key: Any) -> int:
        """Hash function for keys, return value between 0 and m-1"""
        return (hash(key) & 0x7FFFFFFF) % self.m

    def size(self) -> int:
        """return number of key-value pairs in the symbol table"""
        return self.n

    def resize(self, capacity: int) -> None:
        """Resize the hash table to specified capacity"""
        tmp = LinearProbingHashST(capacity)
        for i in range(self.m):
            if self.Keys[i]:
                tmp.put(self.Keys[i], self.vals[i])

        self.m = tmp.m
        self.Keys = tmp.Keys
        self.vals = tmp.vals

    def is_empty(self) -> bool:
        """return True if the symbol table is empty, False otherwise"""
        return self.size() == 0

    def get(self, key: Any) -> int:
        """return the value associated with the given key in the symbol table

            @param key: the key
            @return the value associated with the given key if the key exists
                    None if key is not
            @raise ValueError if key is None
        """
        if not key:
            raise ValueError("argument to get() is None")
        i = self.hash(key)
        while self.Keys[i]:
            if self.Keys[i] == key:
                return self.vals[i]
            i = (i + 1) % self.m

        return None

    def contains(self, key: Any) -> bool:
        """return True if the symbol table contains the specified key
           
           @param key: the key
           @return True if contains, False otherwise
           @raise ValueError if key is None
        """
        if not key:
            raise ValueError("argument to contains() is None") 
        return self.get(key) is not None

    def put(self, key: Any, val: int) -> None:
        """Inserts specified key-value pairs into symbol table.
           if key already exists, overwrites the old value with new value
           if specified value is None, delete the key and its value
            
            @param key: the key
            @return the value
            @raise ValueError if key is None
        """
        if not key:
            raise ValueError("First argument in put() if None")

        if not val:
            self.delete(key)
            return

        # double table size if 50% full
        if self.n >= self.m / 2:
            self.resize(2 * self.m)

        i = self.hash(key)
        while self.Keys[i]:
            if self.Keys[i] == key: # search hit
                self.vals[i] = val
                return
            # search for next position
            i = (i + 1) % self.m
        self.Keys[i] = key
        self.vals[i] = val
        self.n += 1

    def delete(self, key: Any) -> None:
        """removes specified key and its value from symbol table

            @param key: the key
            @raise ValueError if key is None
        """
        if not key:
            raise ValueError("Argument in delete() if None") 

        if not self.contains(key):
            return

        i = self.hash(key)
        while self.Keys[i] != key:
            i = (i + 1) % self.m
        
        # delete key and associated value
        self.Keys[i] = None
        self.vals[i] = None

        # rehash all keys in same cluster
        i = (i + 1) % self.m
        while self.Keys[i]:
            # delete keys[i] and vals[i] and reinsert
            key_to_hash = self.Keys[i]
            val_to_hash = self.vals[i]
            self.Keys[i] = None
            self.vals[i] = None
            self.n -= 1
            self.put(key_to_hash, val_to_hash)
            i = (i + 1) % self.m

        self.n -= 1
        # halves size of array if it's 12.5% full or less
        if self.n > 0 and self.n <= self.m / 8:
            self.resize(self.m // 2)

    def keys(self):
        """
         Returns all keys in the symbol table
         To iterate over all of the keys in the symbol table named st,
         use the for notation: {for key in st.keys}
        """
        res = []
        for key in self.Keys:
            if key:
                res.append(key)
        return res
    
    def check(self) -> bool:
        """Integrity check
           Don't check after each put() because integrity not maintained during a call to delete()
        """
        # check if hash table is at most 50% full
        if self.m < self.n * 2:
            print("Hash table size m = {m}; array size n = {n}")
            return False

        # check if each key in table can be found by get()
        for i in range(self.m):
            if not self.Keys[i]:
                continue 
            elif self.get(self.Keys[i]) != self.vals[i]:
                print(f"get(keys[i]) != vals[i], key = {self.Keys[i]}, val = {self.vals[i]}") 
                return False 
        return True 


if __name__ == '__main__':
    input = [('L', 11), ('P', 10),('M', 9),('X', 7),('H', 5),('C', 4), ('R', 3), ('A', 8), ('E', 12), ('S', 0)]
    
    st = LinearProbingHashST()   # initialize a Sequential Search Symbol Table

    for key, val in input:      # put key-value pairs into table from input
        st.put(key, val)

    st.delete('E')              # delete a key-value pair

    for key in st.keys():       # print all the key-value pairs in the table
        print(key, ' ', st.get(key))