"""
    Naive Dijkstra's algorithm for Single-source shortest path problem 

    T: O(V^2)  two nested loops
    S: O(V+E)  adjacency list 
    
    only applied to graph with positive weights
    ---------------------------------------------------------------------------------------------
    Variants of Dijkstra's algorithm:
    
    Naive Dijkstra: no heap
    standard Dijkstra: heap optimized, enqueue AFTER updating the distance
    Lazy Dijkstra: heap optimized, enqueue BEFORE updating the distance
    ---------------------------------------------------------------------------------------------
    Greedy algorithm:

    1. Initialization: start with a source vertex,
     
                       set the shortest distance to itself as 0 and to all other vertices as infinity.

                       mark all vertices as unvisited. (NOTE: don't mark source vertex as visited)

    2. Selection: Out of unvisited vertices, pick the one with the smallest known distance

                  mark the selected vertex as visited

                  A visited vertex will not be checked again; its shortest distance from the source is final and minimal.

    3. Relaxation: for the selected vertex, examine it's unvisited neighbors (distance infinity)
    
                  If find a shorter path to a neighbor via the current vertex, we update the distance.

    4. Repetition: repeat steps 2-3 until all vertices are visited/settled, 
    
        i.e., their shortest paths from the source have been permanently determined.
    
    All the vertices are divided into 2 sets
    S1 shortest path is solved
    S2 (heap) shortest path is unsolved
    ------------------------------------------------------------
    Single-source shortest path problem 

    finding the shortest paths from a given source vertex to all other vertices in the weighted digraph without negative cycles 
    input
        a weighted digraph without negative cycles G=(V, E)
        a single source vertex s ∈ V 
    output
        a set of V shortest paths d(v) and corresponding weights
"""
class NaiveDijkstra:
    def __init__(self, V: int=0, s: int=0, edges: list[tuple[int, int, int]]=None) -> None:
        self.V = V                              # number of vertices in the weighted digraph
        self.s = s                              # the single source vertex
        self.edges = edges                      # edge list, edges[i] = (ui, vi, wi)
        self.dist = [float('inf')] * self.V     # distance array, dist[v] is distance/weight of shortest path from s to v 
        self.dist[s] = 0                        # initialize distance of source vertex to itself as 0
        self.parents = [-1] * self.V            # parent array, parents[i] is parent vertex of vertex i along the shortest path from source vertex s to vertex i, initialize to be -1 for all vertices, i.e., parent not exist
        self.visited = [False] * self.V         # visited[i]: whether vertex i is visited, initialize all the vertices as unvisited
        self.self.adj = [[] for _ in range(self.V)]  # build adjacency list from edge list
        for u, v, w in edges:
            self.self.adj[u].append((v, w))          

        # Naive Dijkstra's algorithm O(V^2)
        # 1. start with a source vertex
        self.dist[s] = 0
        # 4. repeat steps 2-3 for V times, each vertex is visited exactly once
        for _ in range(self.V):
            # 2. out of unvisited vertices, select the vertex with the smallest tentative distance and 'settle' it
            u = min((i for i in range(self.V) if not self.visited[i]), key=lambda i: self.dist[i])
            self.visited[u] = True # mark the selected vertex as visited

            # 3. search neighbors of vertex u
            for v, w in self.adj[u]:
                self.relax(u, v, w)        # O(1) relax operation      

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
        # case 1: vertex v is visited
        if self.visited[v]:
            return 
        # case 2: path can't be shortend
        if self.dist[v] <= self.dist[u] + w:
            return 
        
        self.dist[v] = self.dist[u] + w         # 'relax' the edge u -> v 
        self.parents[v] = u                     # update parent of vertex v 
 
    def pathTo(self, t: int) -> list[int]:
        """O(V) Returns the path from source vertex s to target vertex t
        
        cases when the path does not exist: 
        (1) target vertex t is not reachable from source vertex S
        (2) vertex s or t is in the negative cycle
        """
        # case 1: no path from source vertex to vertex t
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
        # case 2: no path from source vertex to vertex t
        if self.dist[t] == float('inf'):
            return 
        return self.dist[t]
        
    def allPaths(self) -> list[list[int]]:
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
    # print(f"Naive Dijkstra Shortest Path")

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
    # g = NaiveDijkstra(V=V, s=s, edges=edges)   # run Dijkstra algorithm
    # print(f"All paths: {g.allPaths()}")
    """
    Naive Dijkstra Shortest Path
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
    # print(f"Naive Dijkstra Shortest Path")

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
    # g = NaiveDijkstra(V=V, s=s, edges=edges)   # run Dijkstra algorithm
    # print(f"All paths: {g.allPaths()}")

    """
    Naive Dijkstra Shortest Path
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
    print(f"Naive Dijkstra Shortest Path")
    
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
    g = NaiveDijkstra(V=V, edges=edges)    # run Dijkstra algorithm
    print(f"All paths: {g.allPaths()}")
    """
    This test case will run forever, Dijkastra can't work for graph with negative cycle
    """