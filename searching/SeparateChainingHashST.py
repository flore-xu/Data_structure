"""
   A symbol table implemented using a separate chaining hash.
"""

from SequentialSearchST import SequentialSearchST
from typing import Any

class SeparateChainingHashST:
    INIT_CAPACITY = 4

    def __init__(self, m :int=0):
        self.n = 0                        # number of key-value pairs in the hash table
        self.m = m or self.INIT_CAPACITY  # hash table size, a prime number, # generally make load factor alpha = 2 < N/M < 10

        # initialize an empty symbol table with m linked-lists
        self.st = [SequentialSearchST() for _ in range(self.m)]  

    def hash(self, key: Any) -> int:
        """Hash function for keys, return value between 0 and m-1"""
        return (hash(key) & 0x7FFFFFFF) % self.m

    def size(self) -> int:
        """return number of key-value pairs in the symbol table"""
        return self.n

    def resize(self, chains: int) -> None:
        """Resize the hash table to have the given number of chains
           rehashing all of the keys
        """
        tmp = SeparateChainingHashST(chains)
        for i in range(self.m):
            for key in self.st[i].keys():
                tmp.put(key, self.st[i].get(key))
        self.m = tmp.m
        self.n = tmp.n
        self.st = tmp.st

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
        return self.st[self.hash(key)].get(key)

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

        if val is None:
            self.delete(key)
            return

        # double table size if average length of linked list >= 10
        if self.n >= self.m * 10:
            self.resize(2 * self.m)

        i = self.hash(key)

        if not self.st[i].contains(key):
            self.n += 1
        self.st[i].put(key, val)

    def delete(self, key: Any) -> None:
        """removes specified key and its value from symbol table

            @param key: the key
            @raise ValueError if key is None
        """
        if not key:
            raise ValueError("Argument in delete() if None")

        i = self.hash(key)
        if self.st[i].contains(key):
            self.n -= 1
        self.st[i].delete(key)

        # halve table size if average length of list <= 2
        if self.m > self.INIT_CAPACITY and self.n <= 2 * self.m:
            self.resize(self.m // 2)

    def keys(self):
        """
         Returns all keys in the symbol table
         To iterate over all of the keys in the symbol table named st,
         use the for notation: {for key in st.keys}
        """
        res = []
        for linkedls in self.st:
            for key in linkedls.keys():
                res.append(key)
        return res



if __name__ == '__main__':

    input = [('L', 11), ('P', 10),('M', 9),('X', 7),('H', 5),('C', 4), ('R', 3), ('A', 8), ('E', 12), ('S', 0)]
    
    st = SeparateChainingHashST()   # initialize a Sequential Search Symbol Table

    for key, val in input:      # put key-value pairs into table from input
        st.put(key, val)

    st.delete('E')              # delete a key-value pair

    for key in st.keys():       # print all the key-value pairs in the table
        print(key, ' ', st.get(key))
