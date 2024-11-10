"""
    Lazy Heap optimized Dijkstra's algorithm for Single-source shortest path problem 
    https://algs4.cs.princeton.edu/44sp/LazyDijkstraSP.java.html
    
    T: O((V+E)logV)
    S: O(V)     adjacency list and heap

    only applied to graph with positive weights
    ------------------------------------------------------------
    Variants of Dijkstra's algorithm:
    
    Naive Dijkstra: no heap
    standard Dijkstra: heap optimized, enqueue AFTER updating the distance
    Lazy Dijkstra: heap optimized, enqueue BEFORE updating the distance
    ------------------------------------------------------------
    Greedy algorithm:

    1. Initialization: start with a source vertex,
     
                       set the shortest distance to itself as 0 and to all other vertices as infinity.

                       mark all vertices as unvisited. (NOTE: don't mark source vertex as visited)

    2. Selection: Out of unvisited vertices, pick the one with the smallest known distance

                  mark the selected vertex as visited

                  A visited vertex will not be checked again; its shortest distance from the source is final and minimal.

    3. Relaxation: for the selected vertex, examine it's unvisited neighbors

                        the distance from source to the neighbor is infinity, 
    
                        If we find a shorter path to a neighbor via the current vertex, we update the distance.

    4. Repetition: repeat steps 2-3 until all vertices are visited/settled, 
    
        i.e., their shortest paths from the source have been permanently determined.
    
    All the vertices are divided into 2 sets
    S1 shortest path is solved
    S2 (heap) shortest path is unsolved

    ------------------------------------------------------------
    Time complexity analysis:

    T: O((V+E)logV)

    at most E enqueue operations and exactly V dequeue operations
    each enqueue or dequeue operation takes O(logV), thus ElogV + VlogV = (V+E)logV

    enqueue: when processing each edge, Each vertex is enqueued once when it is initially discovered 
            and it may be enqueued again each time a shorter path to it is found.

    dequeue: Each vertex is dequeued exactly once, 
            at the time when its shortest path from the source is permanently determined.

    ------------------------------------------------------------
    Single-source shortest path problem 

    finding the shortest paths from a given source vertex to all other vertices in the weighted digraph without negative cycles 
    input
        a weighted digraph without negative cycles G=(V, E)
        a single source vertex s ∈ V 
    output
        a set of V shortest path d(v) and corresponding weights
"""
from heapq import heappush, heappop  
class Dijkstra:
    def __init__(self, V: int=0, s: int=0, edges: list[tuple[int, int, int]]=None) -> None:
        self.V = V                              # number of vertices in the weighted digraph
        self.s = s                              # the single source vertex
        self.edges = edges                      # edge list, edges[i] = (ui, vi, wi)
        self.dist = [float('inf')] * self.V     # distance array, dist[v] is distance/weights of shortest path from s to v 
        self.dist[s] = 0                        # initialization: distance of source vertex to itself is 0
        self.parents = [-1] * self.V            # parent array, parents[i] is parent vertex of vertex i along the shortest path from source vertex s to vertex i, initialize to be -1 for all vertices, i.e., parent not exist
        self.adj = [[] for _ in range(self.V)]  # build adjacency list from edge list
        for u, v, w in edges:
            self.adj[u].append((v, w))              

        # Lazy Heap optimized Dijkstra's algorithm O((V+E)logV)
        # 1. start with a source vertex
        self.heap = [(0, s)]      # min-heap: store unsolved vertices, element is a tuple (dist[u], u), initialize as source vertex to be enqueued
        while self.heap: 
            # 2. out of unvisited vertices, select the vertex with the smallest tentative distance and 'settle' it
            d, u = heappop(self.heap)   # dequeue O(logV)
            # important check: vertex u must be unvisited
            if d > self.dist[u]:         
                continue 
            # 3. update the tentative distances of u's neighbors
            for v, w in self.adj[u]: 
                self.relax(u, v, w)        # relax operation, contains enqueue O(logV)     
  
      
    def relax(self, u: int, v: int, w: int) -> None:
        """O(logV) Relaxation   
           
           enqueue BEFORE updating the distance

            worst-case: E items in heap since we do relax operation for each edge
                        T = O(logE) <= O(logV^2) = O(2logV) = O(logV)
        """
        # enqueue before updating the distance O(log V)
        d = self.dist[u] + w
        heappush(self.heap, (d, v))                 
        # case 1: the path can't be shortend
        if self.dist[v] <= d:
            return 
        self.dist[v] = d                         # 'relax' the edge u -> v  
        self.parents[v] = u                       # update parent of vertex v 
            

    def pathTo(self, t: int) -> list[int]:
        """O(V) Returns the path from source vertex s to target vertex t

        cases when the path does not exist: 
        (1) target vertex t is not reachable from source vertex S
        (2) vertex s or t is in the negative cycle
        """
        # case: no path from source vertex to vertex t
        if self.dist[t] == float('inf'):
            return 
        # rebuild path from target vertex t
        path = []
        while True:
            path.append(t)
            if t == self.s:
                break 
            t = self.parents[t]
        return path[::-1]  # reverse path

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
        
    def allPaths (self) -> list[list[int]]:
        """O(V^2) Returns shortest paths from source vertex s to each other vertex in graph.
           
           @return a list of length V, paths[v] is the shortest path from vertex s to vertex v
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
    # print(f"Dijkstra Shortest Path")

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
    # g = Dijkstra(V=V, s=s, edges=edges)   # run Dijkstra algorithm
    # print(f"All paths: {g.allPaths ()}")
    """
    Dijkstra Shortest Path
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
    # print(f"Dijkstra Shortest Path")

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
    # g = Dijkstra(V=V, s=s, edges=edges)   # run Dijkstra algorithm
    # print(f"All paths: {g.allPaths ()}")

    """
    Dijkstra Shortest Path
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
    print(f"Dijkstra Shortest Path")
    
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
    g = Dijkstra(V=V, edges=edges)    # run Dijkstra algorithm
    print(f"All paths: {g.allPaths ()}")
    """
    This test case will run forever, Dijkastra can't do for graph with negative cycle
    """