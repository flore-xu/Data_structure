import random 
class UFDS:
    def __init__(self, n: int, m: int=None) -> None:
        self.parents = list(range(n))   # 每个节点的父节点
        self.ranks = [0] * n            # 每个节点的最大高度
        self.sizes = [1] * n            # 每个互斥集合的节点数
        self.numdisjoint = n            # 互斥集合的总数

        # 当m不等于n时，随机选2个互斥集合合并，直到有m个互斥集合
        if m:
            k = n-m
            while k:
                # 随机选2个互斥集合合并
                i, j = random.sample(self.parents, 2)
                while self.IsSameSet(i, j):
                    i, j = random.sample(self.parents, 2)
                self.union(i, j)
                k -= 1
    
    def find(self, i):
        """返回节点x所在集合的根节点 (递归版)
           第一次 O(N) 之后 O(1)
           path-compression heuristic
        """
        if self.p[i] == i:
            return i
        else:
            self.p[i] = self.findSet(self.p[i])
            return self.p[i]

    def find(self, x: int) -> int:
        """返回节点x所在集合的根节点 （迭代版）
           第一次 O(N) 之后 O(1)
           path-compression heuristic
        """
        xp = x  # parent of x 
        children = []   # 记录从当前节点到根节点路径上的所有节点

        # 从当前节点开始，递归地向上查找父节点
        while xp != self.parents[xp]:
            children.append(xp)
            xp = self.parents[xp]

        # 路径压缩：一条路径上的所有节点都变成叶节点，直接连接根节点
        # 路径压缩后，树会变矮，但不更新这些节点的rank值，继续用于union()
        for c in children:
            self.parents[c] = xp
        
        # 返回根节点
        return xp
    
    def union(self, a: int, b: int) -> None:
        """若节点i和节点j来自2个不同的互斥集合，将两个集合合并 O(1)
           union-by-rank heuristic 矮树作为高树的子树
        """
        # 若两个节点来自同一互斥集合，直接返回
        # indirect path-compression heuristic 这里也会调用find() 进行2次路径压缩
        if self.IsSameSet(a, b):
            return
        
        ap, bp = self.find(a), self.find(b)

        # 若A树矮，B树高，A树连到B树的根节点上，新树 rank不变
        if self.ranks[ap] < self.ranks[bp]:
            self.parents[ap] = bp
            self.sizes[bp] += self.sizes[ap]

        # 若B树矮，A树高，B树连到A树的根节点上，新树 rank不变
        elif self.ranks[bp] < self.ranks[ap]:
            self.parents[bp] = ap
            self.sizes[ap] += self.sizes[bp]

        # 若两树等高，任选一种方案，新树 rank +1
        else:
            self.parents[bp] = ap
            self.ranks[ap] += 1
            self.sizes[ap] += self.sizes[bp]

        # 互斥集总数-1
        self.numdisjoint -= 1
    
    def IsSameSet(self, i: int, j: int) -> bool:
        """判断节点i和节点j是否属于同一集合 O(1)"""

        # 2次路径压缩
        return self.find(i) == self.find(j)

    def size(self, x: int):
        """返回节点x所在集合的大小"""
        return self.sizes[self.find(x)]


if __name__ == '__main__':
    
    u = UFDS(8, 4)

    print(u.numdisjoint == 8)
    u.union(1, 2)
    print(u.find(1) == u.find(2))
    print(u.find(1) != u.find(3))
    print(u.find(2) != u.find(3))
    print(u.size(1) == 2)
    print(u.size(2) == 2)
    print(u.size(3) == 1)
    print(u.numdisjoint == 7)
    u.union(1, 3)
    print(u.find(1) == u.find(2))
    print(u.find(1) == u.find(3))
    print(u.find(2) == u.find(3))
    print(u.find(2) != u.find(4))
    print(u.size(1) == 3)
    print(u.size(2) == 3)
    print(u.size(3) == 3)
    print(u.numdisjoint == 6)
    u.union(2, 4)
    print(u.find(1) == u.find(3))
    print(u.find(2) == u.find(4))
    print(u.size(1) == 4)
    print(u.size(2) == 4)
    print(u.numdisjoint == 5)
    u.union(2, 3)
    print(u.size(1) == 4)
    print(u.size(2) == 4)
    print(u.numdisjoint == 5)