class ListNode:
    def __init__(self, val: int, next: 'ListNode'=None):
        self.val = val      # value of node
        self.next = next    # a pointer points to the next node, can be null

class SingleLinkedList:

    def __init__(self):
        """O(1) Initialize an empty single-linked list"""
        self.size = 0                  # number of effective nodes, not including dummy head
        self.dummyHead = ListNode(0)   # sentinel

    def __str__(self) -> str:
        """O(N) return string representation of the SLL
           e.g., return '5, 3, 1, 2, 4'
        """
        nodes = list()
        cur = self.dummyHead
        while cur:
            nodes.append(cur.val)
            cur = cur.next
        return str(nodes)

    def isEmpty(self) -> bool:
        """O(1) Returns true if the SLL is empty, or false otherwise."""
        return self.size == 0
    
    def get(self, idx: int) -> int:
        """O(n) return value of node with idx, return -1 if idx is invalid"""
        if idx < 0 or idx >= self.size:
            return -1
        cur = self.dummyHead
        for _ in range(idx + 1):
            cur = cur.next
        return cur.val

    def addAtHead(self, val: int) -> None:
        """O(1) insert a new node at head"""
        node = ListNode(val, next = self.dummyHead.next)
        self.dummyHead.next = node 
        self.size += 1

    def addAtTail(self, val: int) -> None:
        """O(N) insert a new node at tail"""
        self.addAtIndex(self.size, val)

    def addAtIndex(self, idx: int, val: int) -> None:
        """O(N) insert a new node at specified index 

            5 cases
            1. idx < 0 or idx >= N+1: invalid index
            2. idx = 0: add node after dummy head
            3. idx in [1, N-1]: add node in the middle of linked list
            4. index = N: add node after tail
            5. linked list is empty: same as case 2 because use of dummy head
        """
        # case 1: invalid index
        if idx < 0 or idx > self.size:
            return 

        self.size += 1  # increment number of effective nodes

        # find the node before insertion position
        pre = self.dummyHead 
        for _ in range(idx):
            pre = pre.next

        # insert the node
        node = ListNode(val, next=pre.next)
        pre.next = node

    def deleteAtIndex(self, idx: int) -> None:
        """O(N) delete the node at specified index
           4 cases
           1. idx < 0 or idx >= N: invalid index
           2. idx = 0: delete head
           3. idx = N-1: delete tail
           4. idx in [1, N-2]: detele middle node
        """
        # case 1: invalid index
        if idx < 0 or idx >= self.size:
            return None 
        self.size -= 1      # decrement number of effective nodes

        # find node before deletion position
        pred = self.dummyHead
        for _ in range(idx):
            pred = pred.next
        
        # delete the node
        pred.next = pred.next.next


    def traverse(self, head: ListNode) -> tuple[list[int], list[int]]:
        def iterative(head: ListNode) -> None:
            """O(N) traverse SLL by iteration"""
            cur = head
            while cur: 
                preOrder.append(cur.val)
                cur = cur.next

        def recursive(node: ListNode) -> None:
            """O(N) traverse SLL by recursion"""
            if not node:
                return 
            
            preOrder.append(node.val)   # top-down recursion
            recursive(node.next)
            postOrder.append(node.val)  # bottom-up recursion

        
        if not head:
            return [], []
        preOrder = []      
        postOrder = []     
        iterative(head)
        # recursive(head)
        return preOrder, postOrder


    def removeElements(self, head: ListNode, val: int) -> ListNode:
        """remove all the nodes with specified value, return the new head"""
        def iterative(head: ListNode, val: int) -> ListNode:
            if not head:
                return 

            # create a dummy head in case head is to be deleted
            dummyHead = ListNode(-1, next=head)

            # initialize predecessor and current node
            pre, cur = dummyHead, head 

            while cur: 
                # find target, delete current node 
                if cur.val == val:
                    pre.next = cur.next
                else:
                    pre = pre.next  
                cur = cur.next   # move pointer one step forward

            return dummyHead.next

        def recursive(head: ListNode, val: int) -> ListNode:
            """postorder recursion"""
            # base case 1: at the end of SLL  
            if not head:
                return 

            head.next = recursive(head.next, val)
            
            # base case 2: node is target, delete node, return the next node
            if head.val == val:
                return head.next
            return head

        return iterative(head, val)  # recursive(head, val) 
    

    def reverse(self, head: ListNode) -> ListNode:
        """O(N) reverse the SLL, return new head, i.e. the tail of original SLL
           leetcode 206 Reverse Linked List I
        """
        def iterative1(head: ListNode) -> ListNode:
            if not head:
                return
            pre, cur = None, head
            while cur:
                suc = cur.next         # temporarily save successor
                cur.next = pre         # reverse step
                pre, cur = cur, suc  # two pointers forward a step
            return pre
        
        def iterative2(head: ListNode) -> ListNode:
            """head insertion"""
            dummyHead = ListNode(-1, next=head)
            
            cur = head
            while cur:
                suc = cur.next   # temporarily save successor

                # case 1: current node is head
                if dummyHead.next == cur:
                    cur.next = None            # break link to successor to avoid loop  head -X-> node
                # case 2: current node is successor
                else:
                    cur.next = dummyHead.next  # cur -> head

                dummyHead.next = cur  # dummyHead -> cur
                cur = suc            # pointer forward a step
            return dummyHead.next
        
        def recursive1(head: ListNode) -> ListNode:
            # base case: head is null or no next node
            if not head or not head.next:
                return head
            
            # search the next node
            newHead = self.reverseList(head.next)

            # reverse current node
            suc = head.next 
            suc.next, head.next = head, None
            return newHead
        
        def recursive2(head: ListNode) -> ListNode:
            def dfs(node: ListNode, p: ListNode) -> ListNode:
                """reverse linked list headed at node, return the new head of reversed linked list"""
                # base case: at the end of SLL, return the previous node
                if not node: 
                    return p     
                newNode = dfs(node.next, node)   # recursively reverse the next node
                node.next = p                  # reverse step
                return newNode                   # return head of reversed linked list
            
            return dfs(head, None)
        
        return iterative1(head)   # iterative2(head), recursive1(head), recursive2(head)


    def middleNode(self, head: ListNode) -> tuple[ListNode, ListNode]:
        """O(N) return the middle node of the linked list.
           linked list of even length has two middle nodes, return both
        """
        def firstMiddleNode(head: ListNode) -> ListNode:
            """O(N) for linked list of even length, return the first middle node with index (n-1)//2"""
            if not head:
                return 
            fast = slow = head 
            while fast.next and fast.next.next:
                fast = fast.next.next
                slow = slow.next
            return slow
        
        def secondMiddleNode(head: ListNode) -> ListNode:   
            """O(N) for linked list of even length, return the second middle node with index (n-1)//2"""   
            if not head:
                return 
            fast = slow = head 
            while fast and fast.next:
                fast = fast.next.next
                slow = slow.next 
            return slow
        
        mid1 = firstMiddleNode(head)
        mid2 = secondMiddleNode(head)
        return mid1, mid2
    
    def mergeTwoLists(self, l1: ListNode, l2: ListNode) -> ListNode:
        """O(n1+n2) leetcode 21. Merge Two Sorted Lists
            Return the head of the merged linked list.
        """
        def iterative(l1: ListNode, l2: ListNode) -> ListNode:
            dummyHead = ListNode(0)
            cur = dummyHead

            # 1. from head, compare value of node pair from 2 linked lists, add smaller node to tail of new linked list
            while l1 and l2:
                if l1.val < l2.val:
                    cur.next = l1
                    l1 = l1.next 
                else:
                    cur.next = l2
                    l2 = l2.next 
                cur = cur.next

            # 2. after iteration of one linked list, add all rest of nodes of another linked list to tail of new linked list
            cur.next = l1 if l1 else l2
            return dummyHead.next

        def recursive(l1: ListNode, l2: ListNode) -> ListNode:
            # base case: reach the end of one linked list, return another linked list
            if not l1 or not l2:
                return l1 if l1 else l2
            
            if l1.val < l2.val:
                l1.next = recursive(l1.next, l2)
                return l1 
            else:
                l2.next = recursive(l1, l2.next)
                return l2 
            
        return iterative(l1, l2)  # recursive(l1, l2)

    def split(self, head: ListNode, size: int) -> tuple[ListNode, ListNode]:
        """O(N) cut a sublist of length at most size from SLL, 
        return head of sublist and head of next sublist
        """
        # 1. cut a sublist of length at most size from SLL
        length = 0
        cur = head 
        while cur and length < size:
            length += 1
            cur = cur.next 
        
        # 2. break link between tail of sublist and head of next sublist
        if not cur:     # length of sublist < size, can't cut one more sublist
            return head, None

        # length of sublist = size, can cut one more sublist
        head2 = cur.next 
        cur.next = None 
        return head, head2
    
    def mergeSort(self, head: ListNode) -> ListNode:
        """O(nlogn) merge sort the linked list, return the head of sorted list"""
        
        def recursive(head: ListNode) -> ListNode:
            # base case: length of linked list <= 1
            if not head or not head.next:
                return head

            # 1. O(N) split the linked list into 2 halves
            mid = self.middleNode(head) # find middle node of the linked list
            head2 = mid.next 
            mid.next = None     # break the link between 2 sublists

            # 2. O(NlogN) sort two halves respectively
            l1 = recursive(head)
            l2 = recursive(head2)

            # 3. O(N) merge two sorted halves
            return self.mergeTwoLists(l1, l2)
        
        def iterative(head: ListNode) -> ListNode:
            if not head:
                return head
            
            dummyHead = ListNode(0, head)

            # 1. O(N) calculate length of the linked list
            n = 0
            cur = head
            while cur:
                n += 1
                cur = cur.next
            
            # 2-3. O(NlogN) outer loop: iterates for logN times
            size = 1
            while size < n:
                pre, cur = dummyHead, dummyHead.next
                
                # inner loop: O(N) divide and merge size-by-size sublist pairs until pointer `cur` reaches the tail of linked list
                while cur:
                    # 2. cut two sublists of size from the linked list 
                    head1, cur = self.split(cur, size)   # head1 is head of the first sublist
                    head2, cur = self.split(cur, size)   # head2 is head of the second sublist
                    
                    # 3. merge 2 sublists
                    pre.next = self.mergeTwoLists(head1, head2)

                    # move pointer `pre` to the tail of the merged linked list
                    while pre.next:
                        pre = pre.next
                size *= 2   # double the sublist size
            
            return dummyHead.next
        
        return recursive(head)  # iterative(head)
        

    def swapPairs(self, head: ListNode) -> ListNode:
        """O(N) swap every two adjacent nodes and return its head.
           e.g. Input: head = [1,2,3,4], Output: [2,1,4,3] 
        """
        def iterative(head: ListNode) -> ListNode:
            dummyHead = ListNode(0, next=head)
            pred, curr = dummyHead, head 
            while curr and curr.next:
                succ = curr.next 
                # swap the node pair cur and suc
                curr.next, succ.next, pred.next = succ.next, curr, succ 
                # forward a step
                pred, curr = curr, curr.next 
            return dummyHead.next
        
        def recursive(head: ListNode) -> ListNode:
            # base case: linked list has <= 1 nodes
            if not head or not head.next:
                return head 
            suc = head.next 
            head.next = self.swapPairs(suc.next)
            suc.next = head 
            return suc
    
        return iterative(head) # recursive(head)
    
if __name__ == '__main__':
    sll = SingleLinkedList()
    sll.addAtHead(1)
    sll.addAtTail(3)
    sll.addAtIndex(1, 2)  # SLL: 1 -> 2 -> 3
    print(f"Single Linked List: {sll}")

    print(f"get(1): {sll.get(1)}")   # return 2
    
    print("deleteAtIndex(1)")
    sll.deleteAtIndex(1)  # SLL: 1 -> 3
    print(f"Single Linked List: {sll}")
    print(f"get(1): {sll.get(1)}")   # return 3
