"""
Prim's algorithm for Minimal spanning tree problem

T = O(E logV) S = O(V)

MST 定义：给定一个连通无向加权图G， MST是包含G全部节点的权重总和最小的连通子图，即一棵有N个节点和N-1条边的树

输入：连通无向加权图G

输出：二选一 (1) MSTs 不唯一 (2) 最小权重
"""

from heapq import heappush, heappop

class PrimMST:
    def __init__(self, V: int=0, edges: list[tuple[int, int, int]]=None) -> None:
        self.V = V 
        self.weight = 0
        self.edges = []
        self.adj = [[] for _ in range(self.V)]
        for u, v, w in edges:
            self.adj[u].append((v, w))
            self.adj[v].append((u, w))

        def process(v: int) -> None:
            """访问节点u, 将u的邻边全部入堆 O(logV)"""
            visited[v] = True 
            for u, w in self.adj[v]:
                if not visited[u]:
                    heappush(pq, (w, u, v))

        visited = [False] * self.V    # 布尔数组：记录节点是否已访问，防止成环
        
        pq = []                       # 最小堆: 元素 (weight, neighbor_node)  每个节点入堆一次           
        num_taken = 0                 # 已用边数
        # step 1: 从源节点出发，通常为0                      
        process(0) 

        # step 2: 当队列非空且已用边数小于总边数时 O(E)
        while pq and num_taken < self.V - 1: 
            w, u, v = heappop(pq)   # 贪心：最小权重的边出堆 O(logV)
            
            if not visited[u]:      # 若与该边相连的节点未访问，用该边，否则不用                      
                num_taken += 1                         
                self.weight += w 
                self.edges.append((u, v, w))                         
                process(u)          # 节点的所有邻接边入堆   O(logV)

        # return self.weight, self.edges    

if __name__ == '__main__':

    edges = [(4, 5, 0.35), (4, 7, 0.37), (5, 7, 0.28), (0, 7, 0.16),
    (1, 5, 0.32), (0, 4, 0.38), (2, 3, 0.17), (1, 7, 0.19),
    (0, 2, 0.26), (1, 2, 0.36), (1, 3, 0.29), (2, 7, 0.34),
    (6, 2, 0.40), (3, 6, 0.52), (6, 0, 0.58), (6, 4, 0.93)]

    g = PrimMST(8, edges)

    print(f"MST Prim")

    print(f"weight = {g.weight}")

    print(f"edges = {g.edges}")           