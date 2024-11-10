from collections import deque 
from collections.abc import Iterable

from typing import Any

class TreeNode:
    def __init__(self, key: Any=None, val: int=0, size: int =0, left: 'TreeNode'=None, right: 'TreeNode'=None) -> None:
        self.key = key      # sorted by key
        self.val = val      # associated data
        self.left = left    # left subtree
        self.right = right  # right subtree
        self.count = size    # number of nodes in subtree (including root)

class BST:
    def __init__(self) -> None: 
        self.root = None # initialize an empty symbol table
    
    def is_empty(self) -> bool:
        """Returns True if symbol table is empty"""
        return self.size() == 0 
    
    def size(self) -> int:
        """Returns the number of key-values pairs in this symbol table"""
        return self._size(self.root)
    
    def _size(self, node: TreeNode) -> int:
        """Return number of key-value pairs in subtree rooted at node"""
        if not node:
            return 0
        else:
            return node.count 

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
        return self._get(self.root, key) 
    
    def _get(self, node: TreeNode, key: Any) -> int:
        """find node with specified key in the subtree rooted at node
           and return its associated value
           @param node: current node;  key: the key
           @return the value associated with the key if the key exists
                    None if key is not
            @raise ValueError if key is None 
        """
        if key is None:
            raise ValueError("argument to get() is None")
        
        if not node:        # a search miss
            return None 
        if key < node.key:
            return self._get(node.left, key)
        elif key > node.key:
            return self._get(node.right, key)
        else:               # a search hit
            return node.val 

    def insert(self, key: Any, val: int) -> None:
        """O(N) Inserts specified key-value pairs into symbol table.
            if key already exists, overwrites the old value with new value
            if specified value is None, delete the key and its value
                
            @param key: the key
            @return the value
            @raise ValueError if key is None
        """
        if key is None:
            raise ValueError("First argument in insert() if None")

        if val == None:
            self.delete(key)
            return  
        
        self.root = self._insert(self.root, key, val)

        assert self.check()

    def _insert(self, node: TreeNode, key: Any, val: int) -> TreeNode:
        """find the node with specified key to update its value in the subtree rooted at node
           @return the updated node
        """
        # key doesn't exist in table, insert a new node
        if not node:
            return TreeNode(key, val, 1)
        
        if key < node.key:  # go to left subtree
            node.left = self._insert(node.left, key, val)
        elif key > node.key:  # go to right subtree
            node.right = self._insert(node.right, key, val)
        else:  # find the node with key, update its value
            node.val = val 
        
        node.count = 1 + self._size(node.left) + self._size(node.right)

        return node 
    
    #***************************************************************************
    # Deletion
    #***************************************************************************
    def delete(self, key: Any) -> None:
        """removes specified key and its value from symbol table

            @param key: the key
            @raise ValueError if key is None
        """
        if key is None:
            raise ValueError("Argument in delete() is None")
        
        self.root = self._delete(self.root, key)
        assert self.check()

    def _delete(self, node: TreeNode, key: Any) -> TreeNode:
        """removes node with specified key in the subtree rooted at node
            Hibbard deletion: if node has 2 children, replace the node with its successor
                              disadvantage:  BST becomes left skewed

            @param node: current node; key: the key
            @return updated node
        """
        if not node:
            return None 
        
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        # current node is the one we look for 
        else:
            # if node only has one child, replace the node with that child
            if not node.left or not node.right:
                return node.right if node.right else node.left  
            # if node has 2 children, replace the node with its successor
            else:
                tmp = node 
                node = self._minKey(tmp.right)           # replace the node with the smallest node in its right subtree
                node.right = self._deleteMin(tmp.right)  # remove the link between new root and its father
                node.left = tmp.left                     # connect the left subtree to the new root
        # update node counts
        node.count = 1 + self._size(node.left) + self._size(node.right)
        return node 

    #***************************************************************************
    #*  Ordered symbol table methods
    #***************************************************************************
    
    #***************************************************************************
    # Delete minimum and maximum
    #***************************************************************************
    def deleteMin(self) -> None:
        """Removes the smallest key and its value from symbol table
           raise IndexError if the symbol table is empty
        """
        if self.is_empty():
            raise IndexError("Symbol table underflow error") 
        
        self.root = self._deleteMin(self.root)
        assert self.check()
    
    def _deleteMin(self, node: TreeNode) -> TreeNode:
        """removes the node with smallest key in the subtree rooted at node
           @return updated node
        """
        # go left until find the node has a None left pointer
        # replace pointer to that node by its right pointer
        if not node.left:
            return node.right 
        node.left = self._deleteMin(node.left)
        # update node counts
        node.count = 1 + self._size(node.left) + self._size(node.right)
        return node 
    
    def deleteMax(self) -> None:
        """Removes the largest key and its value from symbol table
           raise IndexError if the symbol table is empty
        """
        if self.is_empty():
            raise IndexError("Symbol table underflow error") 
        
        self.root = self._deleteMax(self.root)
        assert self.check()
    
    def _deleteMax(self, node: TreeNode) -> TreeNode:
        """remove the node with largest key in the subtree rooted at node
           @return updated node
        """
        # go right until find the node has a None right pointer
        # replace the pointer to that node with its left pointer
        if not node.right:
            return node.left  
        node.right = self._deleteMax(node.right)
        # update node counts
        node.count = 1 + self._size(node.left) + self._size(node.right)
        return node

    #***************************************************************************
    # Minimum and maximum
    #***************************************************************************
    def minKey(self) -> str:
        """Returns the smallest key in the symbol table
           raise IndexError if the symbol table is empty
        """
        if self.is_empty():
            raise IndexError("Symbol table underflow error")

        return self._minKey(self.root).key 
    
    def _minKey(self, node: TreeNode) -> TreeNode:
        """returns the node with smallest key in the subtree rooted at node
           @return the node with smallest key in subtree 
        """
        if not node.left:  # if not left subtree, smallest key in the root
            return node 
        else:               # go to left subtree
            return self._minKey(node.left)

    def maxKey(self) -> str:
        """Returns the largest key in the symbol table
           raise IndexError if the symbol table is empty
        """
        if self.is_empty():
            raise IndexError("Symbol table underflow error")

        return self._maxKey(self.root).key 
    
    def _maxKey(self, node: TreeNode) -> TreeNode:
        """returns the node with smallest key in the subtree rooted at node
           @return the node with largest key in subtree 
        """
        if not node.right:      # if no right subtree, largest key in the root
            return node 
        else:                   # go to right subtree
            return self._maxKey(node.right)  
    #***************************************************************************
    # Floor and ceiling
    #***************************************************************************
    def floor(self, key: Any) -> str:
        """Returns the largest key in the symbol table less than or equal to key.
           @param key: the key
           @return floor of the key
           @raise IndexError if there is no such or table is empty
           @raise ValueError if key is None
        """
        if key is None:
            raise ValueError("argument in floor() is None")
        if self.is_empty():
            raise IndexError("empty symbol table")

        node = self._floor(self.root, key)
        if not node:
            raise IndexError("argument to floor() is too small")
        else:
            return node.key 

    def _floor(self, node: TreeNode, key: Any) -> TreeNode:
        """Returns the node with largest key in the subtree rooted at node less than or equal to key.
           return None if node not found
        """
        if not node:
            return None 
        if key == node.key:
            return node 
        elif key < node.key:
            return self._floor(node.left, key)
        else:
            tmp = self._floor(node.right, key)
            if not tmp:
                return tmp 
            else:
                return node 

    def ceil(self, key: Any) -> str:
        """Returns the smallest key in the symbol table greater than or equal to key.
           @param key: the key
           @return ceiling of the key
           @raise IndexError if there is no such or table is empty
           @raise ValueError if key is None
        """
        if key is None:
            raise ValueError("argument in ceil() is None")
        if self.is_empty():
            raise IndexError("empty symbol table")

        node = self._ceil(self.root, key)
        if not node:
            raise IndexError("argument to ceil() is too large")
        else:
            return node.key 

    def _ceil(self, node: TreeNode, key: Any) -> TreeNode:
        """Returns the node with largest key in the subtree rooted at node less than or equal to key.
           return None if node not found
        """
        if not node:
            return None 
        if key == node.key:
            return node 
        elif key < node.key:
            tmp =  self._ceil(node.left, key)
            if not tmp:
                return tmp 
            else:
                return node 
        else:
            return self._ceil(node.right, key)


    #***************************************************************************
    # Selection
    #***************************************************************************
    def select(self, rank: int) -> str:
        """Returns the (rank+1)th smallest key in this symbol table

           @param rank: rank 
           @return the kth smallest key
           raise IndexError if k is not between 0 and self.n-1
        """
        if not (0 <= rank < self.size()):
            raise IndexError(f"called select() with invalid rank {rank}")
        
        return self._select(self.root, rank)   

    def _select(self, node: TreeNode, rank: int) -> int:
        """find and returns the key of specified rank in the subtree rooted at node

           @param node: current node; rank: rank 
           @return the kth smallest key
        """
        if not node:
            return None 
        
        # the number of keys in the left subtree
        leftSize = self._size(node.left)

        if leftSize > rank:   # go to left subtree
            return self._select(node.left, rank)
        elif leftSize < rank: # go to right subtree, but first remove leftSize + 1 from rank bc all nodes in left subtree and the root node must smaller than all nodes in right subtree
            return self._select(node.right, rank - leftSize - 1)   
        else:
            return node.key

    #***************************************************************************
    # Rank (1-based indexing)
    #***************************************************************************
    def rank(self, key: Any) -> int:
        """return the number of keys in the symbol table that strictly less than the specified key
            @param key: the key
            @return the number 
            @raise ValueError if key is None
        """
        if key is None:
            raise ValueError("argument to rank() is None")
        
        return self._rank(self.root, key)
    
    def _rank(self, node: TreeNode, key: Any) -> int:
        """return the number of keys in the subtree rooted at node
           that strictly less than the specified key
            @param node: root of subtree, key: the key
            @return the number 
        """
        if not node:
            return 0
        if key < node.key:
            return self._rank(node.left, key)
        elif key > node.key:
            return 1 + self._size(node.left) + self._rank(node.right, key)
        else:
            return self._size(node.left)
 
    #***************************************************************************
    # Range count and range search
    #***************************************************************************
    def keySize(self, lo: str, hi: str) -> int:
        """Returns the number of keys in the symbol table in the specified range
            
            @param lo: lower bound  hi: upper bound both inclusive 
            @return the number of keys
            @raise ValueError if key is None
        """
        if lo == None:
            raise ValueError("first argument to keySize() is None")
        if hi == None:
            raise ValueError("second argument to keySize() is None")
        if lo > hi:
            return 0
        if self.contains(hi):
            return self.rank(hi) - self.rank(lo) + 1
        else:
            return self.rank(hi) - self.rank(lo)


    def keys(self) -> Iterable:
        """Returns all keys in the symbol table in ascending order as an Iterable
            to iterate over all of the keys in the symbol table named st
            use for-loop: for key in st.keys()
        """
        if self.is_empty():
            return []
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
        
        queue = []
        self._keys(self.root, queue, lo, hi)
        return queue 

    def _keys(self, node: TreeNode, queue: Iterable, lo: str, hi: str):
        """Store all keys in a given range in the subtree rooted at node in a queue
           Inorder traversal: left-root-right
           @param queue: a container to store the keys
        """
        if not node:
            return  
        if lo > node.key or hi < node.key:
            return 
        if lo < node.key:
            self._keys(node.left, queue, lo, hi)
        if lo <= node.key <= hi:
            queue.append(node.key)
        if hi >= node.key:
            self._keys(node.right, queue, lo, hi)


    def height(self) -> int:
        """Returns the height of BST"""
        return self._height(self.root)

    def _height(self, node: TreeNode) -> int:
        """Returns the height of subtree rooted at node"""
        if not node:
            return -1
        return 1 + max(self._height(node.left), self._height(node.right))


    def levelOrder(self) -> Iterable:
        """Returns all the keys in the BST in level order"""
        level_order = []
        queue = deque([self.root])	
        while queue:
            tmp = []
            for _ in range(len(queue)):
                node = queue.popleft()	
                tmp.append(node.key)
                if node.left: 
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            level_order.append(tmp)
        return level_order

    #***************************************************************************
    #*  Check internal invariants.
    #***************************************************************************
    def check(self):
        if not self.isBST():
            print("BST not in symmetirc order")
        if not self.countCheck():
            print("Subtree counts not consistent")
        if not self.rankCheck():
            print("Ranks not consistent")
        return self.isBST() and self.countCheck() and self.rankCheck()
    
    def isBST(self) -> bool:
        """check if the whole tree is a BST
           does this binary tree satisfy symmetric order?
        """
        return self._isBST(self.root, None, None)

    def _isBST(self, node: TreeNode, min: str, max: str) -> bool:
        """Check if subtree rooted at node is a BST 
           with all keys strictly between min and max
           if min and max is None, treat as empty constraint
           Credit: elegant solution due to Bob Dondero
        """
        if not node:
            return True 
        if min != None and node.key <= min:
            return False 
        if max != None and node.key >= max:
            return False 
        return self._isBST(node.left, min, node.key) and self._isBST(node.right, node.key, max)
    
    def countCheck(self) -> bool:
        """Check if count of whole tree is correct"""
        return self._countCheck(self.root)
    
    def _countCheck(self, node: TreeNode) -> bool:
        """Check if count of subtree rooted at node is correct"""
        if not node:
            return True 
        if node.count != 1 + self._size(node.left) + self._size(node.right):
            return False 
        return self._countCheck(node.left) and self._countCheck(node.right)    
    
    def rankCheck(self) -> bool:
        """Check if ranks are consistent. i.e., rank(select(i)) = i"""
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
    
    st = BST()       # initialize a Binary Search Tree
    
    for key, val in input:      # insert key-value pairs from input into table
        st.insert(key, val)

    st.delete('E')              # delete a key-value pair
    
    print("All the key-value pairs in the table")
    for key in st.keys():
        print(key, ' ', st.get(key)) 

    print("All the key-value pairs in the table in level-order ")
    for keys in st.levelOrder():    
        print([(key, st.get(key)) for key in keys]) 
