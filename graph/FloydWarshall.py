"""Floyd-Warshall algorithm for Multi-source shortest path problem
    https://algs4.cs.princeton.edu/44sp/FloydWarshall.java.html

    T: O(V^3)  triple loop
    S: O(V^2)  distance array and parent array

    applied to graph with positive weights, or graph with negative weights but no negative cycle
    ----------------------------------------------------------------------
    Multi-source shortest path problem (all-pairs shortest paths)

    finding the shortest paths from K multiple source nodes to a single destination node or to all other nodes 
    in a weighted digraph without negative cycles 

    for a graph with negative cycle, those vertices that are not reachable from the negative cycle, can still have valid shortest paths

    input
        a weighted digraph without negative cycles G=(V, E)
        a set of source vertices S ⊆ V 
    output
        a set of V^2 shortest path d(v) and corresponding weights
        a path may not exist due to reachability or negative cycle
"""
class FloydWarshall:
    def __init__(self, V: int, edges: list[tuple[int, int, int]]) -> None:
        """O(V^3) Floyd-Warshall algorithm for Multi-source shortest path problem"""
        self.V = V                                                    # number of vertices in the weighted digraph
        self.dist = [[float('inf')]*self.V for _ in range(self.V)]    # distance array, dist[v][u]: length of shortest path from node v to node u
        self.parent = [[-1]*self.V for _ in range(self.V)]           # parent array, parent[v][u]: parent of vertex u along the shortest path from node v to node u
        self.negCycles = []                                         # vertices in the negative cycle or reachable from the negative cycle
        
        # O(V) initialize distance of vertex to itself as 0
        for v in range(self.V):                                       
            self.dist[v][v] = 0

        # O(E) initialize distance array and parent array by edge list
        for u, v, w in edges:
            self.dist[u][v] = w
            self.parent[u][v] = u 

        # O(V^3) try path s -> t via vertex i
        for i in range(self.V):             # intermediate vertex
            for s in range(self.V):         # source vertex s
                for t in range(self.V):     # target vertex t
                    self.relax(s, t, i)     # O(1) relaxation      

    def relax(self, s: int, t: int, i: int) -> None:
        """O(1) Relaxation
        @Args  
        s: source vertex
        t: target vertex
        i: intermediate vertex
        
        used in all the shortest path algorithms
        by relaxation, we lower the upper bound of distance of shortest path of each node, until they reached the true shortest distance.
        if dist(s, t) > dist(s, i) + dist(i, t), 
        we choose go through/relax the edge i -> t, update the path to be s -> i -> t
        """
        if self.dist[s][t] > self.dist[s][i] + self.dist[i][t]:
            self.dist[s][t] = self.dist[s][i] + self.dist[i][t]      
            self.parent[s][t] = i 

    def hasNegativeCycle(self) -> bool:
        """O(V) negative cycle detection"""
        for v in range(self.V):
            if self.dist[v][v] < 0:
                self.negCycles.append(v) 

        # print vertices in the negative cycle or vertices reachable from the negative cycle
        if self.negCycles:
            print(f"Has negative cycle: {self.negCycles}")
            return True 
        return False 

    def distTo(self, s: int, t: int) -> float:
        """O(1) return length of shortest path from source vertex s to target vertex t 

        cases when the path does not exist: 
        (1) vertex t is not reachable from vertex s
        (2) vertex t or vertex s is in the negative cycle
        """
        # case 1: path does not exist from s to t
        if self.dist[s][t] == float('inf'):
            return 
        # case 2: vertex s or t is in the negative cycles
        if s in self.negCycles or t in self.negCycles:
            return 
        return self.dist[s][t]


    def pathTo(self, s: int, t: int) -> list[int]:
        """O(V) return shortest path from source vertex s to target vertex t 
        
        cases when the path does not exist: 
        (1) vertex t is not reachable from vertex s
        (2) vertex t or vertex s is in the negative cycle
        """
        # case 1: path does not exist
        if self.dist[s][t] == float('inf'):
            return 
        # case 2: source or target vertex is in the negative cycles
        if s in self.negCycles or t in self.negCycles:
            return 
        
        # rebuild path from target vertex t 
        path = []
        while True:
            path.append(t)
            if t == s:          # stop iteration when meet source vertex s
                break
            t = self.parent[s][t]
            if t in self.negCycles:
                return 
        return path[::-1]       # reverse path
    

    def allPaths(self) -> list[list[int]]:
        """O(V^3) Returns shortest paths of all pairs of vertice in graph.
           
           @return a V*V list, paths[s][t] is the shortest path from vertex s to vertex t
        """
        # case 1: graph has negative cycles.
        if self.hasNegativeCycle():
            print("Graph contains negative cycles. Paths involving these vertices will not be displayed.")
        
        paths = []
        for s in range(self.V):
            for t in range(self.V): 
                print(f"{s} to {t} ({self.dist[s][t]:.2f}): {self.pathTo(s, t)}")
                paths.append(self.pathTo(s, t))
        return paths 


if __name__ == '__main__':
    ###################################################### 
    #  Example 1: positive weighted digraph
    ######################################################
    # print(f"Floyd-Warshall Shortest Path")

    # V = 5   # V is number of vertics
    # E = 5   # E is number of edges 

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
    # g = FloydWarshall(V=V, edges=edges)   # run Floyd-Warshall algorithm
    # print(f"All paths: {g.allPaths()}")

    """
    Floyd-Warshall Shortest Path
    Positive weighted digraph: V = 5, E = 5, edges = [(0, 1, 2), (0, 2, 6), (0, 3, 7), (1, 3, 3), (1, 4, 6), (1, 4, 1), (2, 4, 1), (3, 4, 5)]
    
    0 to 0 (0.00): [0]
    0 to 1 (2.00): [0, 1]
    0 to 2 (6.00): [0, 2]
    0 to 3 (5.00): [0, 1, 3]
    0 to 4 (3.00): [0, 1, 4]
    1 to 0 (inf): None
    1 to 1 (0.00): [1]
    1 to 2 (inf): None
    1 to 3 (3.00): [1, 3]
    1 to 4 (1.00): [1, 4]
    2 to 0 (inf): None
    2 to 1 (inf): None
    2 to 2 (0.00): [2]
    2 to 3 (inf): None
    2 to 4 (1.00): [2, 4]
    3 to 0 (inf): None
    3 to 1 (inf): None
    3 to 2 (inf): None
    3 to 3 (0.00): [3]
    3 to 4 (5.00): [3, 4]
    4 to 0 (inf): None
    4 to 1 (inf): None
    4 to 2 (inf): None
    4 to 3 (inf): None
    4 to 4 (0.00): [4]

    All paths: [[0], [0, 1], [0, 2], [0, 1, 3], [0, 1, 4], None, [1], None, [1, 3], [1, 4], None, None, [2], None, [2, 4], None, None, None, [3], [3, 4], None, None, None, None, [4]]
    """
    ###################################################### 
    # Example 2: negative weighted digraph without negative cycle
    ###################################################### 
    # V = 5   # V is number of vertics
    # E = 5   # E is number of edges

    # edges = [
    #     (0, 1, 1), 
    #     (0, 2, 10), 
    #     (1, 3, 2),
    #     (2, 3, -10), 
    #     (3, 4, 3)
    # ]

    # print(f"negative weighted digraph without negative cycle: V = {V}, E = {E}, edges = {edges}")
    # g = FloydWarshall(V=V, edges=edges)   # run Floyd-Warshall algorithm
    # print(f"All paths: {g.allPaths()}")

    """
    negative weighted digraph without negative cycle: V = 5, E = 5, edges = [(0, 1, 1), (0, 2, 10), (1, 3, 2), (2, 3, -10), (3, 4, 3)]
    0 to 0 (0.00): [0]
    0 to 1 (1.00): [0, 1]
    0 to 2 (10.00): [0, 2]
    0 to 3 (0.00): [0, 2, 3]
    0 to 4 (3.00): [0, 2, 3, 4]
    1 to 0 (inf): None
    1 to 1 (0.00): [1]
    1 to 2 (inf): None
    1 to 3 (2.00): [1, 3]
    1 to 4 (5.00): [1, 3, 4]
    2 to 0 (inf): None
    2 to 1 (inf): None
    2 to 2 (0.00): [2]
    2 to 3 (-10.00): [2, 3]
    2 to 4 (-7.00): [2, 3, 4]
    3 to 0 (inf): None
    3 to 1 (inf): None
    3 to 2 (inf): None
    3 to 3 (0.00): [3]
    3 to 4 (3.00): [3, 4]
    4 to 0 (inf): None
    4 to 1 (inf): None
    4 to 2 (inf): None
    4 to 3 (inf): None
    4 to 4 (0.00): [4]
    All paths: [[0], [0, 1], [0, 2], [0, 2, 3], [0, 2, 3, 4], None, [1], None, [1, 3], [1, 3, 4], None, None, [2], [2, 3], [2, 3, 4], None, None, None, [3], [3, 4], None, None, None, None, [4]]
    """

    ###################################################### 
    # Example 3: weighted digraph with negative cycle (1 -> 2 -> 1)
    ###################################################### 
    V = 5   # V is number of vertics
    E = 5   # E is number of edges

    edges = [
        (0, 1, 99), 
        (0, 4, -99), 
        (1, 2, 15),
        (2, 1, -42), 
        (2, 3, 10)
    ]

    print(f"weighted digraph with negative cycle: V = {V}, E = {E}, edges = {edges}")
    g = FloydWarshall(V=V, edges=edges)   # run Floyd-Warshall algorithm
    print(f"All paths: {g.allPaths()}")
    
    """
    weighted digraph with negative cycle: V = 5, E = 5, edges = [(0, 1, 99), (0, 4, -99), (1, 2, 15), (2, 1, -42), (2, 3, 10)]
    Has negative cycle: [1, 2]
    Graph contains negative cycles. Paths involving these vertices will not be displayed.
    0 to 0 (0.00): [0]
    0 to 1 (72.00): None
    0 to 2 (87.00): None
    0 to 3 (97.00): None
    0 to 4 (-99.00): [0, 4]
    1 to 0 (inf): None
    1 to 1 (-27.00): None
    1 to 2 (-12.00): None
    1 to 3 (-2.00): None
    1 to 4 (inf): None
    2 to 0 (inf): None
    2 to 1 (-69.00): None
    2 to 2 (-54.00): None
    2 to 3 (-44.00): None
    2 to 4 (inf): None
    3 to 0 (inf): None
    3 to 1 (inf): None
    3 to 2 (inf): None
    3 to 3 (0.00): [3]
    3 to 4 (inf): None
    4 to 0 (inf): None
    4 to 1 (inf): None
    4 to 2 (inf): None
    4 to 3 (inf): None
    4 to 4 (0.00): [4]
    All paths: [[0], None, None, None, [0, 4], None, None, None, None, None, None, None, None, None, None, None, None, None, [3], None, None, None, None, None, [4]]
    """