import random 
class UnionFind:
    def __init__(self, n: int, m: int=None) -> None:
        """
        build m disjoint sets from n nodes
        T: O(N)
        """
        self.parents = list(range(n))    # parent array: parent[i]: parent node of node i
        self.ranks = [0] * n            # rank array: rank[i]: max height of subtree rooted at vertex i, used as guiding heuristic for UnionSet(i, j) operation
                                        # after 'path-compression' heuristic compresses some path, the rank values no longer reflect the true height of that subtree
        self.sizeSets = [1] * n         # sizeSets[i]: size of disjoint set rooted at vertex i
        self.numSets = n                # number of disjoint sets
        self.edgeCount = [0] * n        # edgeCount[i]: number of edges in disjoint set rooted at vertex i

        # 当m不等于n时，随机选2个互斥集合合并，直到有m个互斥集合
        if m:
            k = n-m
            while k:
                # 随机选2个互斥集合合并
                i, j = random.sample(self.parents, 2)
                while self.isSameSet(i, j):
                    i, j = random.sample(self.parents, 2)
                self.unionSet(i, j)
                k -= 1
    
    def findSet(self, i: int) -> int:
        """return root of node i's set
           T: amortized O(α(N))  effectively O(1)
             first O(N) then O(1)
           path-compression  
           Recursion
        """
        if self.parents[i] == i:
            return i
        else:
            self.parents[i] = self.findSet(self.parents[i])
            return self.parents[i]
        

    def findSet(self, i: int) -> int:
        """return root of node i's set
           T: amortized O(α(N))  effectively O(1)
             first O(N) then O(1)
           path-compression: keep the trees very flat
           Iteration
        """
        children = []   # 记录从当前节点到根节点路径上的所有节点

        # 从当前节点开始，向上查找父节点
        while i != self.parents[i]:
            children.append(i)
            i = self.parents[i]

        # 路径压缩：一条路径上的所有节点都变成叶节点，直接连接根节点
        # 路径压缩后，树会变矮，但不更新这些节点的rank值，继续用于union()
        for child in children:
            self.parents[child] = i 
        
        # 返回根节点
        return i
    
    def unionSet(self, i: int, j: int) -> None:
        """若节点i和节点j来自2个不同的互斥集合，将两个集合合并 
           union by rank   矮树作为高树的子树
           T: amortized O(α(N))  effectively O(1)
             first O(N) then O(1)
        """
        ip, jp = self.findSet(i), self.findSet(j)

        # 若两个节点来自同一互斥集合，返回
        if ip == jp:
            self.edgeCount[ip] += 1
            return 

        # 若A树矮，B树高，A树连到B树的根节点上，新树rank不变
        if self.ranks[ip] < self.ranks[jp]:
            self.parents[ip] = jp
            self.sizeSets[jp] += self.sizeSets[ip]
            self.edgeCount[jp] += self.edgeCount[ip] + 1

        # 若B树矮，A树高，B树连到A树的根节点上，新树rank不变
        elif self.ranks[jp] < self.ranks[ip]:
            self.parents[jp] = ip
            self.sizeSets[ip] += self.sizeSets[jp]
            self.edgeCount[ip] += self.edgeCount[jp] + 1

        # 若两树等高，任选一种方案，新树 rank +1
        else:
            self.parents[jp] = ip
            self.sizeSets[ip] += self.sizeSets[jp]
            self.edgeCount[ip] += self.edgeCount[jp] + 1
            self.ranks[ip] += 1

        # 互斥集总数-1
        self.numSets -= 1
    
    def isSameSet(self, i: int, j: int) -> bool:
        """判断节点i和节点j是否属于同一集合
           T: O(α(N) first O(N) then O(1)
        """
        # path compression twice
        return self.findSet(i) == self.findSet(j)
    
    def size(self, i: int) -> int:
        """
        返回节点i所在连通分量的大小
        """
        return self.sizeSets[self.findSet(i)]

if __name__ == '__main__':
    
    UF = UnionFind(8, 4)

    print(UF.numSets == 8)
    UF.unionSet(1, 2)
    print(UF.findSet(1) == UF.findSet(2))
    print(UF.findSet(1) != UF.findSet(3))
    print(UF.findSet(2) != UF.findSet(3))
    print(UF.size(1) == 2)
    print(UF.size(2) == 2)
    print(UF.size(3) == 1)
    print(UF.numSets == 7)
    UF.unionSet(1, 3)
    print(UF.findSet(1) == UF.findSet(2))
    print(UF.findSet(1) == UF.findSet(3))
    print(UF.findSet(2) == UF.findSet(3))
    print(UF.findSet(2) != UF.findSet(4))
    print(UF.size(1) == 3)
    print(UF.size(2) == 3)
    print(UF.size(3) == 3)
    print(UF.numSets == 6)
    UF.unionSet(2, 4)
    print(UF.findSet(1) == UF.findSet(3))
    print(UF.findSet(2) == UF.findSet(4))
    print(UF.size(1) == 4)
    print(UF.size(2) == 4)
    print(UF.numSets == 5)
    UF.unionSet(2, 3)
    print(UF.size(1) == 4)
    print(UF.size(2) == 4)
    print(UF.numSets == 5)