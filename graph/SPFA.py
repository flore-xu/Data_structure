"""SPFA (Bellman Ford Moore) algorithm  O(VE)
    最短路问题的通用版本 Bellman Ford的队列优化
    T: 最坏 O(VE) 最好 O(kE)  k: 外循环次数
    Computes the shortest path tree in edge-weighted digraph G from vertex s, 
    or finds a negative weight cycle

    单源最短路问题
    定义：给定一个有向加权图G(V, E)，从一个节点s到另一个节点u的最短路径，最短指权重之和最小。

    输入：一个有向加权图G(V, E), 一个源节点 s ∈ V 
    输出：权重δ(s, u), 1条路径

    因为对于每个节点，都要求最短路径
    输出：权重数组D（V个权重），V条路径

    0 to 0  (0.00)
    0 to 1  (0.93)  0->2  0.26   2->7  0.34   7->3  0.39   3->6  0.52   6->4 -1.25   4->5  0.35   5->1  0.32
    0 to 2  (0.26)  0->2  0.26
    0 to 3  (0.99)  0->2  0.26   2->7  0.34   7->3  0.39
    0 to 4  (0.26)  0->2  0.26   2->7  0.34   7->3  0.39   3->6  0.52   6->4 -1.25
    0 to 5  (0.61)  0->2  0.26   2->7  0.34   7->3  0.39   3->6  0.52   6->4 -1.25   4->5  0.35
    0 to 6  (1.51)  0->2  0.26   2->7  0.34   7->3  0.39   3->6  0.52
    0 to 7  (0.60)  0->2  0.26   2->7  0.34
"""
from collections import deque 
class SPFA:
    def __init__(self, V: int=0, s: int=0, edges: list[tuple[int, int, int]]=None) -> None:
        self.V = V                              # number of vertices in the weighted digraph
        self.s = s                              # source vertex
        self.edges = edges                      # edges[i] = (ui, vi, wi)
        self.dist = [float('inf')] * self.V     # distTo[v] = distance  of shortest s->v path 距离数组：记录每个节点的最小权重和(最新最短路长度), 初始化除源节点外所有节点都为正无穷 10^9, 即未访问节点
        self.dist[s] = 0
        self.parent = [-1] * self.V             # 父节点数组：记录每个节点的父节点, 初始化都为-1，即不存在
        self.adj = [[] for _ in range(self.V)]
        for u, v, w in edges:
            self.adj[u].append((v, w))
        
        self.in_queue = [False] * self.V        # 布尔数组：记录节点是否入队
        self.in_queue[s] = True 

        self.relaxed_edges = 0

        # 队列：初始化起点入队
        self.q = deque([s])
        while self.q:
            u = self.q.popleft()  # 节点出队                       
            self.in_queue[u] = False 
            for v, w in self.adj[u]:
                self.relax(u, v, w)  # relax operation                 


    def relax(self, u: int, v: int, w: int) -> None:
        """松弛操作 O(1)  用于所有最短路算法
            u: 当前节点; v: 邻接节点; w: 边(u, v)的权重
            若起点s→v的最短路长度 大于 s→u + u→v的边长，选择 s→u→v 这条路
            通过该操作，不断降低每个节点的最短路长度的上限，直到上限等于最短路长度
        """
        if self.dist[v] > (d := self.dist[u] + w):   # if the path can be shortened
            self.dist[v] = d                         # 'relax' the long edge
            self.parent[v] = u                       # update parent
            if not self.in_queue[v]:
                self.q.append(v)
                self.in_queue[v] = True
    
    def hasNegativeCycle(self) -> bool:
        """检查图是否存在负权环"""
        # 若经过V-1次循环，还有边能松弛，即dist[u]没收敛，存在负权环
        for u in range(self.V):                        
            if not self.dist[u] == float('inf'):
                for v, w in self.adj[u]:
                    if self.dist[v] > self.dist[u] + w:      # should be false
                        return True
        return False        

    def pathTo(self, v: int) -> list[int]:
        """Returns the path from vertex s to vertex v"""
        if self.hasNegativeCycle():
            print("Has negative cycle")
            return

        path = []
        while v != self.s:
            path.append(v)
            v = self.parent[v]
        path.append(self.s)
        return path[::-1] 

    def weight(self) -> list[int]:
        """Returns the distance array"""
        return self.dist 
    
    def allPath(self) -> list[list[int]]:
        """Returns shortest paths from vertex s to each vertex in graph.
           
           @return a list of length V, paths[v] is the shortest path from vertex s to vertex v"""
        
        if self.hasNegativeCycle():
            print("Has negative cycle")
            return
        for v in range(self.V):   # 0 to 3 ( 0.99)  0->2  0.26   2->7  0.34   7->3  0.39
            print(f"{self.s} to {v} ({self.dist[v]:.2f}): {self.pathTo(v)}")
        
        paths = [self.pathTo(v) for v in range(self.V)]
        return paths 

if __name__ == '__main__':

    edges = [(4, 5, 0.35), (5, 4, 0.35), (4, 7, 0.37), (5, 7, 0.28), 
    (7, 5, 0.28), (5, 1, 0.32), (0, 4, 0.38),  (0, 2, 0.26), 
    (7, 3, 0.39), (1, 3, 0.29), (2, 7, 0.34),
    (6, 2, -1.20), (3, 6, 0.52), (6, 0, -1.40), (6, 4, -1.25)]

    s = 0
    g = SPFA(V=8, s=s, edges=edges)

    print(f"SPFA Shortest Path")

    print(g.allPath())

     
