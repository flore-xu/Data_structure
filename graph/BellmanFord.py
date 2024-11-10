"""Bellman Ford's algorithm for Single-source shortest path problem 
    https://algs4.cs.princeton.edu/44sp/BellmanFordSP.java.html
    T: O(VE)
    S: O(V)  edge list

    applied to graph with positive weights, or graph with negative weights but no negative cycle
    ----------------------------------------------------------------------
    Variants of Bellman Ford algorithm

    standard Bellman Ford: T = O(VE)
    SPFA: queue-optimized T = O(kE)  k is the number of iterations of outer loop
    ----------------------------------------------------------------------
    Bellman-Ford killer

    requires the algorithm to perform the maximum number of iterations: V-1
    e.g., a singly linked list   v0 -> v1 -> v2 -> ... -> vn
    graph structure: the shortest path from the source to the ‘furthest’ vertex has at most V-1 edges.
    vertices can be ordered (v1, v2, …, vn) such that for every edge (vi, vj), we have i < j. 
    ----------------------------------------------------------------------
    Dynamic programming

        breaks this problem down into simpler overlapping subproblems 
        for all i from 1 to V−1, finding the shortest path using at most i edges 
        using the solutions to these subproblems to build up the solution to the original problem. 
        results are stored in a table (distance array) to avoid redundant computation.

    1. Initialize array: dp = [inf] * V  a 1D array of length V, set all the distances as infinity
    2. State definition: dp[u]: shortest distance from source vertex to vertex u
    3. state transition equation: dp[u] = min(dp[u], dp[v]+dist(v, u))   relax the edge v -> u
    4. set initial state: dp[s] = 0  set the shortest distance to source vertex as 0
    5. set return value: dp
    ----------------------------------------------------------------------
    Negative Cycle Detection: 

        After V-1 passes, Perform relaxation for all edges one more time. 
        If a shorter path can be found for any vertex, a negative weight cycle exists 
    ----------------------------------------------------------------------
    Single-source shortest path problem 

    finding the shortest paths from a given source vertex to all other vertices in the weighted digraph without negative cycles 

    for graph with negative cycle, those vertices that are NOT reachable from the negative cycle, we can still compute the shortest path

    input
        a weighted digraph without negative cycles G=(V, E)
        a single source vertex s ∈ V 
    output
        a set of V shortest path d(v) and corresponding weights
"""
class BellmanFord:
    def __init__(self, V: int=0, s: int=0, edges: list[tuple[int, int, int]]=None) -> None:
        """O(VE) Bellman Ford's algorithm for Single-source shortest path problem"""
        self.V = V                              # number of vertices in the weighted digraph
        self.s = s                              # the single source vertex
        self.edges = edges                      # edge list, edges[i] = (ui, vi, wi)
        self.dist = [float('inf')] * self.V     # distance array, dist[v] is distance/weights of shortest path from s to v, initialize to infinitely large (all the vertices haven't visited)
        self.dist[s] = 0                        # initialize distance of source vertex to itself to 0
        self.parents = [-1] * self.V            # parent array, parents[i] is parent node of node i, 初始化都为-1，即不存在

        # at most V-1 relaxation: the longest possible shortest path without a cycle can have at most V-1 edges
        for _ in range(self.V - 1):     # O(V)                 
            for u, v, w in self.edges:  # O(E) traverse all the edges u -> v 
                self.relax(u, v, w)     # try relax the edge from u to v
                self.relax(v, u, w)     # if graph is undirected, also try relax the edge from v to u

        ###### Optimized version O(kE)  k = number of iterations in the outer-loop  #######
        for _ in range(self.V - 1):                      
            self.modified = False   
            for u, v, w in self.edges:  
                # try relax the edge from u to v
                # Optimization 1: skip unvisited vertex
                if self.dist[u] != float('inf'): 
                    self.relax(u, v, w)     
                # if graph is undirected, also try relax the edge from v to u
                if self.dist[v] != float('inf'):  
                    self.relax(v, u, w)

            # Optimization 2: exit outer loop if distance array converges
            if not self.modified: 
                break                 


    def relax(self, u: int, v: int, w: int) -> None:
        """O(1) Relaxation
        @Args
        u: neighbor node of node v (intermediate node)
        v: target node
        w: weight of edge u -> v
        
        used in all the shortest path algorithms
        by relaxation, we lower the upper bound of distance of shortest path of each node, until they reached the true shortest distance.

        if the path to v through u is shorter than the current shortest known path to v
            dist(s, u) + dist(u, v) < dist(s, v) 
        we choose go through/relax the edge u -> v, we update the path to be s -> u -> v
        """
        # case 1: the path can't be shortend
        if self.dist[v] <= self.dist[u] + w:
            return
        self.dist[v] = self.dist[u] + w          # 'relax' the edge u -> v
        self.parents[v] = u                      # update parent
        self.modified = True                     # the path is updated
        self.relaxed_edges += 1                  # increment number of relaxed edges
    
    def hasNegativeCycle(self) -> bool:
        """O(E) negative cycle detection

            return whether input graph contains AT LEAST ONE negative weight cycle reachable from the source vertex s.
            perform one more relaxation step after V-1 passes of relaxation in the initialization, 
            if at least one edge can be relaxed, then there exists a negative-weight cycle reachable from the source vertex s.
        """
        for u, v, w in self.edges:
            if self.dist[u] != float('inf') and self.dist[v] > self.dist[u] + w:  
                return True 
        return False         

    def pathTo(self, t: int) -> list[int]:
        """O(V) Returns the path from source vertex s to target vertex t
        
        Cases when the path does not exist: 
        (1) target vertex t is not reachable from source vertex s
        (2) vertex s or t is in the negative cycle
        """
        # case 1: target vertex t is not reachable from source vertex s
        if self.dist[t] == float('inf'):
            return 
        # rebuild path from target vertex t
        path = []
        while True:
            path.append(t)
            if t == self.s:
                break
            t = self.parents[t]
        return path[::-1]   # reverse path

    def distTo(self, t: int) -> float:
        """O(1) return length of shortest path from source vertex s to target vertex t 

        cases when the path does not exist: 
        (1) vertex t is not reachable from vertex s
        (2) vertex t or vertex s is in the negative cycle
        """
        # case 1: target vertex t is not reachable from source vertex s
        if self.dist[t] == float('inf'):
            return 
        return self.dist[t]
        
    def allPaths(self) -> list[list[int]]:
        """O(V^2) Returns shortest paths from a single source vertex s to each other vertex in the graph.
           
           @return a list of length at most V, paths[v] is the shortest path from source vertex s to vertex v
        """
        # case 1: graph has negative cycle, no paths is found
        if self.hasNegativeCycle():
            print("Graph contains negative cycles.")
            return 
        
        paths = []
        for v in range(self.V):   
            print(f"{self.s} to {v} ({self.dist[v]:.2f}): {self.pathTo(v)}")
            paths.append(self.pathTo(v))
        return paths 

if __name__ == '__main__':
    ###################################################### 
    #  Example 1: positive weighted digraph
    ######################################################
    # print(f"BellmanFord Shortest Path")

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
    # g = BellmanFord(V=V, s=s, edges=edges)   # run Bellman-Ford algorithm
    # print(f"All paths: {g.allPaths()}")
    """
    BellmanFord Shortest Path
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
    # print(f"BellmanFord Shortest Path")

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
    # g = BellmanFord(V=V, s=s, edges=edges)   # run Bellman-Ford algorithm
    # print(f"All paths: {g.allPaths()}")

    """
    BellmanFord Shortest Path
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
    print(f"BellmanFord Shortest Path")
    
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
    g = BellmanFord(V=V, edges=edges)    # run Bellman-Ford algorithm
    print(f"All paths: {g.allPaths()}")
    """
    BellmanFord Shortest Path
    weighted digraph with negative cycle: V = 5, E = 5, edges = [(0, 1, 99), (0, 4, -99), (1, 2, 15), (2, 1, -42), (2, 3, 10)]
    pass 1: 5 edges are relaxed
    pass 2: 3 edges are relaxed
    pass 3: 3 edges are relaxed
    pass 4: 3 edges are relaxed
    Has negative cycle
    All paths: None
    """