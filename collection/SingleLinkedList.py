class ListNode:
    """单向链表
       节点有2个属性，val: 当前节点的值，next: 指向下一个节点的指针
    """
    def __init__(self, val, next=None):
        self.val = val
        self.next = next 

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

class SingleLinkedList:

    def __init__(self):
        """Initialize an empty single-linked list O(1)"""
        self.size = 0             # 有效节点数
        self.head = ListNode(0)   # 一个哨兵节点：作为头节点

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
            如果索引无效，则返回-1。索引都是0-based indexing
        """
        if index < 0 or index >= self.size:
            return -1
        cur = self.head
        for _ in range(index + 1):
            cur = cur.next
        return cur.val

    def addAtHead(self, val: int) -> None:
        """在链表的头节点之前插入新节点。O(1)
           插入后，新节点将成为链表的头节点。
        """
        node = ListNode(val, next = self.head.next)
        self.head.next = node 
        self.size += 1

    def addAtTail(self, val: int) -> None:
        """将新节点追加到链表末尾。O(N)"""
        self.addAtIndex(self.size, val)

    def addAtIndex(self, index: int, val: int) -> None:
        """在链表的指定索引处插入新节点 O(N)
            在链表中的索引为index的节点之前插入值为val的节点。
            5种情况:
            1. index < 0 or index >= N+1: 无效索引，不会插入节点
            2. index = 0, 在头节点之前插入节点
            3. index ∈ [1, N-1], 在链表中间插入节点
            4. index = N, 在链表尾后加节点
            5. 插入空链表 （因为使用了哨兵头节点所以与2相同）
        """
        # 若索引无效，返回
        if index < 0 or index > self.size:
            return None 

        # 有效节点数加1
        self.size += 1

        # 初始化前一个节点为虚拟头节点
        pre = self.head 

        # 找到插入位置的前一个节点
        for _ in range(index):
            pre = pre.next

        node = ListNode(val, next=pre.next)
        pre.next = node

    def deleteAtIndex(self, index: int) -> None:
        """删除链表中指定位置的节点。O(N)
           4种情况
           1. index < 0 or index >= N: 无效索引，不会删除节点
           2. index = 0: 删除头节点
           3. index = N-1: 删除尾节点
           4. index ∈ [1, N-2]: 删除中间节点
        """

        # 若索引无效，返回空节点
        if index < 0 or index >= self.size:
            return None 

        # 有效节点数减1
        self.size -= 1

        # 初始化前一个节点为虚拟头节点
        pred = self.head

        # 找到删除位置的前一个节点
        for _ in range(index):
            pred = pred.next
        
        # 前驱节点指向下下个节点就能跳过（删除）下个节点
        pred.next = pred.next.next



if __name__ == '__main__':
    sll = SingleLinkedList()
    sll.addAtHead(1)
    sll.addAtTail(3)
    sll.addAtIndex(1, 2)  # 链表变为1-> 2-> 3
    print(f"Single Linked List: {sll}")

    print(f"get(1): {sll.get(1)}")   # 返回2
    
    print("deleteAtIndex(1)")
    sll.deleteAtIndex(1)  # 现在链表是1-> 3
    print(f"Single Linked List: {sll}")
    print(f"get(1): {sll.get(1)}")   # 返回3
