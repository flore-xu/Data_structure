from typing import Any

class ListNode:
    """a helper class of node of linked list of key-value pairs"""
    def __init__(self, key: Any =None, val: int =0, next: 'ListNode' =None):
        self.key = key 
        self.val = val
        self.next = next

class STKeyIterator:

    def __init__(self, current):
        self.current = current

    def __iter__(self):
        return self

    def __next__(self):
        if self.current is None:
            raise StopIteration()
        else:
            key = self.current.key
            self.current = self.current.next
            return key

class SequentialSearchST:
    """Implementation of Symbol Table by sequential search in unordered linked list of key-value pairs"""
    def __init__(self) -> None:
        self.head = None           # head of linked list of key-value pairs
        self.size = 0              # number of key-value pairs

    def size(self) -> int:
        """return number of key-value pairs in the symbol table"""
        return self.size  
    
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
        
        return self.get(key) is not None 
    
    def get(self, key: Any) -> int:
        """return the value associated with the given key in the symbol table

            @param key: the key
            @return the value associated with the given key if the key exists
                    None if key is not
            @raise ValueError if key is None
        """
        if key is None:
            raise ValueError("argument to get() is None")
        
        cur = self.head 
        while cur:
            if key == cur.key:
                return cur.val 
            cur = cur.next 
        return None 
    
    def put(self, key: Any, val: int) -> None:
        """Inserts specified key-value pairs into symbol table.
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
        
        cur = self.head  
        while cur:
            if cur.key == key:    # key is already in table
                cur.val = val 
                return 
            cur = cur.next
        
        # if key does not exist, put a new key-value pair 
        # and make this new node as head
        self.head = ListNode(key, val, self.head)
        self.size += 1
    
    def _deleteNode(self, node: ListNode, key: Any) -> ListNode:
        """delete key in linked list beginning at Node node
           warning: function call stack too large if table is large
        """
        if not node:
            return None 
        if node.key == key:
            self.size -= 1
            return node.next 
        else:
            # recursively search next node
            node.next = self._deleteNode(node.next, key)
            return node 
    
    def delete(self, key: Any) -> None:
        """removes specified key and its value from symbol table

            @param key: the key
            @raise ValueError if key is None
        """
        if key is None:
            raise ValueError("Argument in delete() if None")
        
        self.head = self._deleteNode(self.head, key)
    

    def keys(self) -> STKeyIterator:
        """Returns all keys in the symbol table as an Iterable
            to iterate over all of the keys in the symbol table named st
            use for-loop: for key in st.keys()
        """
        return STKeyIterator(self.head)
        # res = []
        # cur = self.head 
        # while cur:
        #     res.append(cur.key)
        #     cur = cur.next 
        # return res 

    
if __name__ == '__main__':
# Execute when the module is not initialized from an import statement.
    
    input = [('L', 11), ('P', 10),('M', 9),('X', 7),('H', 5),('C', 4), ('R', 3), ('A', 8), ('E', 12), ('S', 0)]
    
    st = SequentialSearchST()   # initialize a Sequential Search Symbol Table

    for key, val in input:      # put key-value pairs into table from input
        st.put(key, val)

    st.delete('E')              # delete a key-value pair

    for key in st.keys():       # print all the key-value pairs in the table
        print(key, ' ', st.get(key))