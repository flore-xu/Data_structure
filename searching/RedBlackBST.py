from collections import deque
from collections.abc import Iterable
from typing import Any

class TreeNode:
    """Red black tree node class"""
    def __init__(self, key: Any, val: int, color: bool, size: int):
        self.key = key      # key
        self.val = val      # associated data
        self.left = None    # pointer to left subtree
        self.right = None   # pointer to right subtree
        self.color = color  # color of parent link, True if red, False if black. By convention, None pointers are black
        self.size = size    # subtree count


class RedBlackBST:
    """A symbol table implementation using a left-leaning red-black BST"""
    RED = True
    BLACK = False

    def __init__(self):
        self.root = None    # initialize an empty symbol table

    def isRed(self, node: TreeNode) -> bool:
        """Check if the node is red, 
           return True if node is red, 
           return False if node is black or None"""
        if not node:
            return False
        return node.color == RedBlackBST.RED

    def size(self):
        """Returns number of key-value pairs in this symbol table."""
        return self._size(self.root)

    def _size(self, node: TreeNode) -> int:
        """Returns number of node in the subtree rooted at node x"""
        if not node:
            return 0
        return node.size

    def is_empty(self) -> bool:
        """Check if the table is empty?"""
        return self.root is None

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
        if key == None:
            raise ValueError("argument to get() is None")
        
        if not node:        # a search miss
            return None 
        if key < node.key:
            return self._get(node.left, key)
        elif key > node.key:
            return self._get(node.right, key)
        else:               # a search hit
            return node.val 

    def contains(self, key: Any) -> bool:
        """return True if the symbol table contains the specified key
           
           @param key: the key
           @return True if contains, False otherwise
           @raise ValueError if key is None
        """
        if key == None:
            raise ValueError("argument to contains() is None") 
        
        return self.get(key) != None


    #***************************************************************************
    #*  Red-black tree insertion.
    #***************************************************************************

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

        self.root = self._put(self.root, key, val)
        self.root.color = RedBlackBST.BLACK

    def _put(self, node: TreeNode, key: Any, val: int) -> TreeNode:
        """find the node with specified key to update its value in the subtree rooted at node
           @return the updated node
        """
        # key doesn't exist in table, insert a new node
        if not node:
            return TreeNode(key, val, RedBlackBST.RED, 1)
        
        if key < node.key:  # go to left subtree
            node.left = self._put(node.left, key, val)
        elif key > node.key:  # go to right subtree
            node.right = self._put(node.right, key, val)
        else:  # find the node with key, update its value
            node.val = val 

        # fix-up any right-leaning links
        if self.isRed(node.right) and not self.isRed(node.left):
            node = self.rotate_left(node)
        if self.isRed(node.left) and self.isRed(node.left.left):
            node = self.rotate_right(node)
        if self.isRed(node.left) and self.isRed(node.right):
            self.flip_colors(node)

        node.size = 1 + self._size(node.left) + self._size(node.right)
        return node
    
    #***************************************************************************
    #*  Red-black tree deletion.
    #***************************************************************************/
    def delete(self, key: Any) -> None:
        """removes specified key and its value from symbol table

            @param key: the key
            @raise ValueError if key is None
        """
        if key is None:
            raise ValueError("Argument in delete() is None")

        # if both children of root are black, set root to red
        if not self.isRed(self.root.left) and not self.isRed(self.root.right):
            self.root.color = RedBlackBST.RED

        self.root = self._delete(self.root, key)

        if not self.is_empty():
            self.root.color = RedBlackBST.BLACK

    def _delete(self, h: TreeNode, key: Any) -> TreeNode:
        """removes node with specified key in the subtree rooted at node
            Hibbard deletion: if node has 2 children, replace the node with its successor
                              disadvantage:  BST becomes left skewed

            @param node: current node; key: the key
            @return updated node
        """
        if key < h.key:
            if not self.isRed(h.left) and not self.isRed(h.left.left):
                h = self.move_red_left(h)
            h.left = self._delete(h.left, key)
        else:
            if self.isRed(h.left):
                h = self.rotate_right(h)
            if key == h.key and not h.right:
                return None
            if not self.isRed(h.right) and not self.isRed(h.right.left):
                h = self.move_red_right(h)

            if key == h.key:
                x = self._minKey(h.right)
                h.key = x.key
                h.val = x.val
                h.right = self._deleteMin(h.right)
            else:
                h.right = self._delete(h.right, key)

        return self.balance(h)


    def deleteMin(self) -> None:
        """Removes the smallest key and its value from symbol table
           raise IndexError if the symbol table is empty
        """
        if self.is_empty():
            raise IndexError("BST underflow")

        # if both children of root are black, set root to red
        if not self.isRed(self.root.left) and not self.isRed(self.root.right):
            self.root.color = RedBlackBST.RED

        self.root = self._deleteMin(self.root)
        if not self.is_empty():
            self.root.color = RedBlackBST.BLACK

    def _deleteMin(self, h: TreeNode) -> TreeNode:
        """removes the node with smallest key in the subtree rooted at node
           @return updated node
        """
        if h.left is None:
            return None
        if not self.isRed(h.left) and not self.isRed(h.left.left):
            h = self.move_red_left(h)

        h.left = self._deleteMin(h.left)
        return self.balance(h)


    def deleteMax(self) -> None:
        """Removes the largest key and its value from symbol table
           raise IndexError if the symbol table is empty
        """
        if self.is_empty():
            raise IndexError("Symbol table underflow error") 
        
        # if both children of root are black, set root to red
        if not self.isRed(self.root.left) and not self.isRed(self.root.right):
            self.root.color = RedBlackBST.RED

        self.root = self._deleteMax(self.root)
        if not self.is_empty():
            self.root.color = RedBlackBST.BLACK
    
    def _deleteMax(self, h: TreeNode) -> TreeNode:
        """remove the node with largest key in the subtree rooted at node
           @return updated node
        """
        if self.isRed(h.left):
            h = self.rotate_left(h)
        if not h.right:
            return None
        if not self.isRed(h.right) and not self.isRed(h.right.left):
            h = self.move_red_right(h)

        h.right = self._deleteMax(h.right)
        return self.balance(h)

    #***************************************************************************
    #*  Red-black tree helper functions.
    #***************************************************************************/

    def rotate_left(self, h: TreeNode) ->TreeNode:
        """make a right-leaning link lean to left"""
        assert h and self.isRed(h.right)
        x = h.right
        h.right = x.left
        x.left = h
        x.color = h.color
        h.color = RedBlackBST.RED
        x.size = h.size
        h.size = 1 + self._size(h.left) + self._size(h.right)
        return x

    def rotate_right(self, h: TreeNode) ->TreeNode:
        """make a left-leaning link lean to right"""
        assert h and self.isRed(h.left)
        x = h.left
        h.left = x.right
        x.right = h
        x.color = h.color
        h.color = RedBlackBST.RED
        x.size = h.size
        h.size = 1 + self._size(h.left) + self._size(h.right)
        return x

    def flip_colors(self, h: TreeNode) -> None:
        """
        flip the colors of a node and its two children

        The implementation might allow a black parent to have two red children. 
        flip operation flips the colors of two red children to black and the color of black parent to red.
        """
        h.color = not h.color
        h.left.color = not h.left.color
        h.right.color = not h.right.color

    def move_red_left(self, h: TreeNode) -> TreeNode:
        """
        Assuming that h is red and both h.left and h.left.left
        are black, make h.left or one of its children red.
        """
        self.flip_colors(h)
        if self.isRed(h.right.left):
            h.right = self.rotate_right(h.right)
            h = self.rotate_left(h)
            self.flip_colors(h)
        return h

    def move_red_right(self, h: TreeNode) -> TreeNode:
        """
        Assuming that h is red and both h.right and h.right.left
        are black, make h.right or one of its children red.
        """
        self.flip_colors(h)
        if self.isRed(h.left.left):
            h = self.rotate_right(h)
            self.flip_colors(h)
        return h

    def balance(self, h: TreeNode) -> TreeNode:
        """restore red-black tree invariant"""
        if self.isRed(h.right) and not self.isRed(h.left):
            h = self.rotate_left(h)

        if self.isRed(h.left) and self.isRed(h.left.left):
            h = self.rotate_right(h)

        if self.isRed(h.left) and self.isRed(h.right):
            self.flip_colors(h)

        h.size = 1 + self._size(h.left) + self._size(h.right)

        return h

    #***************************************************************************
    #*  Utility functions.
    #***************************************************************************/

    def height(self) -> int:
        """Returns the height of BST"""
        return self._height(self.root)

    def _height(self, node: TreeNode) -> int:
        """Returns the height of subtree rooted at node"""
        if not node:
            return -1
        return 1 + max(self._height(node.left), self._height(node.right))

    def level_order(self) -> Iterable:
        """Return the keys in the BST in level order"""
        keys = []
        queue = deque([self.root])

        while queue:
            tmp = []

            # 依次从队列中取 len(queue) 个元素拓展
            for _ in range(len(queue)):
                node = queue.popleft()	# 队首元素出队
                tmp.append(node.key)

                # 如果节点的左/右子树不为空，也放入队列中
                if node.left: 
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            
            # 将该层全部节点组成的列表加入最终返回结果中
            keys.append(tmp)

        return keys


    #***************************************************************************
    #*  Ordered symbol table methods.
    #***************************************************************************/


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
        if key == None:
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
        if key == None:
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
        leftSize = self._nodeSize(node.left)

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
        if key == None:
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
            return 1 + self._nodeSize(node.left) + self._rank(node.right, key)
        else:
            return self._nodeSize(node.left)

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
        if node.size != 1 + self._size(node.left) + self._size(node.right):
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


    def is23(self) -> bool:
        """Does the tree have no red right links, and at most one (left)
           red links in a row on any path?
           A red-black BST and a 2-3 tree has a 1-1 correspondence.
        """
        return self.is23(self.root)
    
    def _is23(self, x: TreeNode) -> bool:
        """Does the subtree rooted at x have no red right links, and at most one (left)
           red links in a row on any path?
        """
        if not x:
            return True
        if self.isRed(x.right):
             return False
        if x != self.root and self.isRed(x) and self.isRed(x.left):
            return False
        return self.is23(x.left) and self.is23(x.right)


    def isBalanced(self) -> bool:
        """do all paths from root to leaf have same number of black edges?
        """
        black = 0     # number of black links on path from root to min
        x = self.root
        while x: 
            if not self.isRed(x):
                black += 1
            x = x.left

        return self._isBalanced(self.root, black)
    


    def _isBalanced(self, x: TreeNode, black: int) -> bool:
        """does every path from the node x to a leaf have the given number of black links?"""
        if not x:
            return black == 0
        if not self.isRed(x):
            black -= 1

        return self._isBalanced(x.left, black) and self._isBalanced(x.right, black)



if __name__ == '__main__':
# Unit test: Execute when the module is not initialized from an import statement.
    
    input = [('L', 11), ('P', 10),('M', 9),('X', 7),('H', 5),('C', 4), ('R', 3), ('A', 8), ('E', 12), ('S', 0)]
    
    st = RedBlackBST()       # initialize a Binary Search Tree
    
    for key, val in input:      # insert key-value pairs from input into table
        st.put(key, val)

    st.delete('E')              # delete a key-value pair
    
    print("All the key-value pairs in the table")
    for key in st.keys(): 
        print(key, ' ', st.get(key)) 


    print("All the key-value pairs in level-order")
    for keys in st.level_order(): 
        print([(key, st.get(key)) for key in keys]) 

