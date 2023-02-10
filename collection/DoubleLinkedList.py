class ListNode:
    """双向链表
       每个节点有3个属性：当前节点的值val,指向后继节点的指针next，指向前驱节点的指针prev
    """
    def __init__(self, val: int=0, next: 'ListNode'=None, prev: "ListNode"=None):
        self.val = val 
        self.next = next 
        self.prev = prev 

class LinkIterator:

    def __init__(self, cur: ListNode):
        self.cur = cur

    def __next__(self):
        if not self.cur:
            raise StopIteration()
        else:
            val = self.cur.val 
            self.cur = self.cur.next
            return val

class DoubleLinkedList:

    def __init__(self):
        """Initialize an empty Double-Linked list O(1)"""
        self.size = 0
        self.head, self.tail = ListNode(0), ListNode(0)   # 2个哨兵节点：一头一尾

        # 头指向尾，尾指向头
        self.head.next = self.tail
        self.tail.prev = self.head


    def __str__(self) -> str:
        """Return a string representation of the queue
           @return the sequence of items in this queue in FIFO order, separated by spaces
        """
        return " ".join(str(i) for i in self)

    def __iter__(self) -> LinkIterator:
        """Returns an iterator to this queue that iterates through the items in LIFO order."""
        return LinkIterator(self.head.next)
        
    def get(self, index: int) -> int:
        """获取链表中索引为index的节点的值。 O(N)
           索引都是0-based indexing。如果索引无效，则返回-1。
        """
        # 若索引无效，返回-1
        if index < 0 or index >= self.size:
            return -1

        # 若索引在前半段，从头节点向后遍历
        if index + 1 < self.size - index:
            curr = self.head
            for _ in range(index + 1):
                curr = curr.next
        # 若索引在后半段，从尾节点向前遍历
        else:
            curr = self.tail
            for _ in range(self.size - index):
                curr = curr.prev
        return curr.val


    def addAtHead(self, val: int) -> None:
        """在链表的头节点之前插入新节点。O(1)
           插入后，新节点将成为链表的头节点。
        """
        self.addAtIndex(0, val)


    def addAtTail(self, val: int) -> None:
        """将新节点追加到链表末尾。O(1)"""
        # self.addAtIndex(self.size, val)
        pred = self.tail.prev 
        node = ListNode(val, next=self.tail, prev=pred)
        pred.next, self.tail.prev = node, node 

        self.size += 1



    def addAtIndex(self, index: int, val: int) -> None:
        """将新节点插入链表的指定位置 O(N)
            在链表中的索引为index的节点之前插入值为val的节点。
            5种情况:
            1. index < 0 or index >= N+1: 无效索引，不会插入节点
            2. index = 0, 在头节点之前插入节点
            3. index ∈ [1, N-1], 在链表中间插入节点
            4. index = N, 在链表尾后加节点
            5. 插入空链表 （因为使用了哨兵头节点所以与2相同）
        """
        # 无效索引，不插入节点。
        if index < 0 or index > self.size:
            return None 

        # 找到索引为index的节点的前驱节点pred和后继节点succ
        # 若索引在前半段，从头节点向后遍历
        if index < self.size - index:
            pred = self.head
            for _ in range(index):
                pred = pred.next
            succ = pred.next

        # 若索引在后半段，从尾节点向前遍历
        else:
            succ = self.tail
            for _ in range(self.size - index):
                succ = succ.prev
            pred = succ.prev

        # 有效节点数加1
        self.size += 1

        # 新建节点
        node = ListNode(val, prev=pred, next=succ)

        # 前驱节点的next指向新节点，后继节点的prev指向新节点
        pred.next, succ.prev = node, node


    def deleteAtIndex(self, index: int) -> None:
        """删除链表中指定位置的节点。O(N)
           4种情况
           1. index < 0 or index >= N: 无效索引，不会删除节点
           2. index = 0: 删除头节点
           3. index = N-1: 删除尾节点 O(1)
           4. index ∈ [1, N-2]: 删除中间节点
        """
        # 无效索引
        if index < 0 or index >= self.size:
            return None 
        
        # 找到索引为index的节点的前驱节点pred和后继节点succ
        # 若索引在前半段，从头节点向后遍历
        if index < self.size - index:
            pred = self.head
            for _ in range(index):
                pred = pred.next
            succ = pred.next.next
        
        # 若索引在后半段，从尾节点向前遍历
        else:
            succ = self.tail
            for _ in range(self.size - index - 1):
                succ = succ.prev
            pred = succ.prev.prev
        
        # 有效节点数减1
        self.size -= 1

        # 前驱节点的next指向后继节点，后继节点的prev指向前驱节点
        pred.next, succ.prev = succ, pred 


if __name__ == '__main__':
    dll = DoubleLinkedList()
    dll.addAtHead(1)
    dll.addAtTail(3)
    dll.addAtIndex(1, 2)  # 链表变为1-> 2-> 3
    print(f"Double Linked List: {dll}")

    print(f"get(1): {dll.get(1)}")   # 返回2
    
    print("deleteAtIndex(1)")
    dll.deleteAtIndex(1)  # 现在链表是1-> 3
    print(f"Double Linked List: {dll}")
    print(f"get(1): {dll.get(1)}")   # 返回3