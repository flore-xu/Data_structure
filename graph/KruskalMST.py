"""
Kruskal's algorithm for Minimal spanning tree problem

T: O(ElogE) S: O(E)

MST 定义：给定一个连通无向加权图G， MST是包含G全部节点的权重总和最小的连通子图，即一棵有N个节点和N-1条边的树

输入：连通无向加权图G

输出：二选一 (1) MSTs 不唯一 (2) 最小权重
"""

class UnionFind:                                
    def __init__(self, N):
        self.parent = [i for i in range(N)]
        self.rank = [0 for i in range(N)]
        self.setSize = [1 for i in range(N)]
        self.numSets = N

    def findSet(self, i):
        if self.parent[i] == i:
            return i
        else:
            self.parent[i] = self.findSet(self.parent[i])
            return self.parent[i]

    def isSameSet(self, i, j):
        return self.findSet(i) == self.findSet(j)

    def unionSet(self, i, j):
        if (not self.isSameSet(i, j)):
            self.numSets -= 1
            x = self.findSet(i)
            y = self.findSet(j)

        # rank is used to keep the tree short
        if (self.rank[x] > self.rank[y]):
            self.parent[y] = x
            self.setSize[x] += self.setSize[y]
        else:
            self.parent[x] = y
            self.setSize[y] += self.setSize[x]

            if (self.rank[x] == self.rank[y]):
                self.rank[y] += 1

    def numDisjointSets(self):
        return self.numSets

    def sizeOfSet(self, i):
        return self.setSize[self.findSet(i)]


class KruskalMST:
    def __init__(self, v: int, list[tuple[int, int, int]]) -> None:
        """Compute a MST for a undirected weighted graph
           T: O(ElogE) S: O(E)
        """
        self.V = v                              # number of vertices
        self.weight = 0                         # total cost
        self.edges = []                           # edges of MST. edges[i]: (u, v, w) w: weight, u and v: nodes         
    
        num_taken = 0           # 已用边数为0
        UF = UnionFind(self.V)  # 初始化并查集：V个孤立节点

        # Step 1 O(E log E): 按权重对边升序排序  bottleneck .Sorting key: weight, small node, large node
        edges = sorted([(w, u, v) for u, v, w in edges])                                      

        # Step 2 O(V): 遍历每条边 
        for w, u, v in edges: 
            # 当已用V-1条边时，立即结束遍历                             
            if num_taken == self.V - 1:
                break

            # cycle check: 判断加入这条边是否会形成一个环，O(1) 
            # 若不会成环，加入该边
            if not UF.isSameSet(u, v):      
                UF.unionSet(u, v)           # 连接2个节点成边 O(1)     
                num_taken += 1              # 已用边数加1
                self.weight += w            # 总权重加weight
                self.edges.append((u, v, w))  # 该边加入MST

        # return self.weight, self.edges 


if __name__ == '__main__':

    edges = [(4, 5, 0.35), (4, 7, 0.37), (5, 7, 0.28), (0, 7, 0.16),
    (1, 5, 0.32), (0, 4, 0.38), (2, 3, 0.17), (1, 7, 0.19),
    (0, 2, 0.26), (1, 2, 0.36), (1, 3, 0.29), (2, 7, 0.34),
    (6, 2, 0.40), (3, 6, 0.52), (6, 0, 0.58), (6, 4, 0.93)]

    g = KruskalMST(8, edges)

    print(f"MST Kruskal")

    print(f"weight = {g.weight}")

    print(f"edges = {g.edges}")

