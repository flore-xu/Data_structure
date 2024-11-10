"""Shortest Path Faster Algorithm (SPFA) (Bellman Ford Moore) algorithm for single-source shortest path problem

    T: worst O(VE) best O(kE)  k is the number of iterations of outer loop
    S: O(V+E)   adjacency list
    
    ----------------------------------------------------------------------
    Variants of Bellman Ford algorithm

    standard Bellman Ford: T = O(VE)
    SPFA: queue-optimized T = O(kE)  k is the number of iterations of outer loop
    ----------------------------------------------------------------------
    Algorithm analysis

    up to O(E) enqueue operations and up to O(V) dequeue operations
    ----------------------------------------------------------------------
    Single-source shortest path problem 

    finding the shortest paths from a given source vertex to all other vertices in the weighted digraph
    input
        a weighted digraph G=(V, E)
        a single source vertex s ∈ V 
    output
        a set of V shortest path d(v) and corresponding weights
"""
from collections import deque
class SPFA:
    def __init__(self, V: int=0, s: int=0, edges: list[tuple[int, int, int]]=None) -> None:
        """O(VE) Shortest Path Faster Algorithm (SPFA) (Bellman Ford Moore) algorithm for single-source shortest path problem"""
        self.V = V                              # number of vertices in the weighted digraph
        self.s = s                              # the single source vertex
        self.edges = edges                      # edge list, edges[i] = (ui, vi, wi)
        self.dist = [float('inf')] * self.V     # distance array, dist[v] is distance/weights of shortest path from s to v
        self.dist[s] = 0                        # initialization: all the vertices except source vertex is infinity, means unvisited
        self.parent = [-1] * self.V            # parent array, parents[i] is parent vertex of vertex i, initialize as -1 means not exist
        self.adj = [[] for _ in range(self.V)]  
        self.in_queue = [False] * self.V        # self.in_queue[u] whether vertex [u] is enqueued

        # O(V+E) build adjacency list from edge list
        for u, v, w in edges:
            self.adj[u].append((v, w))

        # O(VE)
        self.in_queue[s] = True                 # mark source vertex as visited
        self.queue = deque([s])                 # enqueue source vertex
        while self.queue:
            u = self.queue.popleft()            # O(1) dequeue vertex u                    
            self.in_queue[u] = False            # mark vertex u as dequeued
            for v, w in self.adj[u]:    
                self.relax(u, v, w)             # O(1) relax operation/enqueue vertex v        

    def relax(self, u: int, v: int, w: int) -> None:
        """O(1) Relaxation 
        @Args 
            u: neighbor vertex of vertex v (intermediate vertex)
            v: target vertex
            w: weight of edge u -> v
            
        used in all the shortest path algorithms
        by relaxation, we lower the upper bound of distance of shortest path of each vertex, until they reached the true shortest distance.

        if the path to v through u is shorter than the current shortest known path to v
            dist(S, u) + dist(u, v) < dist(S, v) 
        we choose go through/relax the edge u -> v, we update the path to be s -> u -> v
        """
        if self.dist[v] > (d := self.dist[u] + w):   # if the path can be shortened
            self.dist[v] = d                         # 'relax' the edge u -> v
            self.parent[v] = u                       # update parent
            if not self.in_queue[v]:
                self.queue.append(v)                 # enqueue vertex v O(1)
                self.in_queue[v] = True
           
    def pathTo(self, t: int) -> list[int]:
        """O(V) Returns the path from source vertex s to target vertex t
        
        cases when the path does not exist: 
        (1) target vertex t is not reachable from source vertex S
        (2) vertex s or t is in the negative cycle
        """
        # case: no path from source vertex to vertex t
        if self.dist[t] == float('inf'):
            return 
        path = []
        while True:
            path.append(t)
            if t == self.s:
                break
            t = self.parent[t]
        return path[::-1] 

    def distTo(self, t: int) -> float:
        """O(1) return length of shortest path from source vertex s to target vertex t 

        cases when the path does not exist: 
        (1) vertex t is not reachable from vertex s
        (2) vertex t or vertex s is in the negative cycle
        """
        # case: no path from source vertex to vertex t
        if self.dist[t] == float('inf'):
            return 
        return self.dist[t]
      
    def allPaths(self) -> list[list[int]]:
        """O(V^2) Returns shortest paths from a single source vertex s to each other vertex in the graph.
           
           @return a list of length at most V, paths[v] is the shortest path from source vertex s to vertex v
        """
        paths = []
        for v in range(self.V):   
            print(f"{self.s} to {v} ({self.dist[v]:.2f}): {self.pathTo(v)}")
            paths.append(self.pathTo(v))
        return paths 

if __name__ == '__main__':
    ###################################################### 
    #  Example 1: positive weighted digraph
    ######################################################
    # print(f"SPFA Shortest Path")

    # V = 5   # V is number of vertics
    # E = 5   # E is number of edges 
    # s = 0   # a single source vertex

    # edges = [
    #     (0, 1, 2), 
    #     (0, 2, 6), 
    #     (0, 3, 7),
    #     (1, 3, 3), 
    #     (1, 4, 6),
    #     (1, 4, 1), 
    #     (2, 4, 1),
    #     (3, 4, 5)
    # ]
     
    # print(f"Positive weighted digraph: V = {V}, E = {E}, edges = {edges}")
    # g = SPFA(V=V, s=s, edges=edges)   # run SPFA algorithm
    # print(f"All paths: {g.allPaths()}")
    """
    SPFA Shortest Path
    Positive weighted digraph: V = 5, E = 5, edges = [(0, 1, 2), (0, 2, 6), (0, 3, 7), (1, 3, 3), (1, 4, 6), (1, 4, 1), (2, 4, 1), (3, 4, 5)]
    pass 1: 6 edges are relaxed
    pass 2: 0 edges are relaxed
    0 to 0 (0.00): [0]
    0 to 1 (2.00): [0, 1]
    0 to 2 (6.00): [0, 2]
    0 to 3 (5.00): [0, 1, 3]
    0 to 4 (3.00): [0, 1, 4]
    All paths: [[0], [0, 1], [0, 2], [0, 1, 3], [0, 1, 4]]
    """


    ###################################################### 
    # Example 2: negative weighted digraph without negative cycle
    ###################################################### 
    # print(f"SPFA Shortest Path")

    # V = 5   # V is number of vertics
    # E = 5   # E is number of edges 
    # s = 0   # a single source vertex

    # edges = [
    #     (0, 1, 1), 
    #     (0, 2, 10), 
    #     (1, 3, 2),
    #     (2, 3, -10), 
    #     (3, 4, 3)
    # ]

    # print(f"negative weighted digraph without negative cycle: V = {V}, E = {E}, edges = {edges}")
    # g = SPFA(V=V, s=s, edges=edges)   # run SPFA algorithm
    # print(f"All paths: {g.allPaths()}")

    """
    SPFA Shortest Path
    negative weighted digraph without negative cycle: V = 5, E = 5, edges = [(0, 1, 1), (0, 2, 10), (1, 3, 2), (2, 3, -10), (3, 4, 3)]
    pass 1: 5 edges are relaxed
    pass 2: 0 edges are relaxed
    0 to 0 (0.00): [0]
    0 to 1 (1.00): [0, 1]
    0 to 2 (10.00): [0, 2]
    0 to 3 (0.00): [0, 2, 3]
    0 to 4 (3.00): [0, 2, 3, 4]
    All paths: [[0], [0, 1], [0, 2], [0, 2, 3], [0, 2, 3, 4]]
    """


    ###################################################### 
    # Example 3: weighted digraph with negative cycle (1 -> 2 -> 1)
    ###################################################### 
    print(f"SPFA Shortest Path")
    
    V = 5   # V is number of vertics
    E = 5   # E is number of edges
    s = 0   # a single source vertex


    edges = [
        (0, 1, 99), 
        (0, 4, -99), 
        (1, 2, 15),
        (2, 1, -42), 
        (2, 3, 10)
    ]

    print(f"weighted digraph with negative cycle: V = {V}, E = {E}, edges = {edges}")
    g = SPFA(V=V, edges=edges)    # run SPFA algorithm
    print(f"All paths: {g.allPaths()}")
    """
    SPFA can't deal with graph with negative cycle
    """