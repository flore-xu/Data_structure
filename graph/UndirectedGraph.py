"""
   An undirected graph
   Parallel edges and self-loops allowed.
 """
from collections import deque
from functools import lru_cache

class UndirectedGraph:
    def __init__(self, v: int, edges: list[tuple[int, int]]) -> None:
        """O(V+E) Initialize an empty undirected graph with v vertices and 0 edges.
        """
        self.V = v                                          # number of vertices
        self.E = 0                                          # number of edges
        self.edges = edges                                  # edge list of a graph
        self.adjList = [[] for _ in range(self.V)]          # adjacency list of graph
        self.adjMat = [[0]*self.V for _ in range(self.V)]   # adjacency matrix of a graph
        self.degree = [0] * self.V                          # degree[i]: degree of vertex i
        # O(E) construct adjacency list, adajcency matrix, degree array
        for v, u in edges:
            self.add_edge(v, u)

    def __str__(self) -> str:
        """Returns an edge list representation of graph O(V+E)"""
        s = f"{self.V} vertices, {self.E} edges"

        for v in range(self.V):   # print vertex v and its neighbors
            s += "\n" + f"{v}: {' '.join(str(u) for u in self.adjList[v])}"

        return s

    def add_edge(self, v: int, u: int) -> None:
        """O(1) adds the undirected edge v-u to this graph O(1)"""
        self.adjList[v].append(u)
        self.adjList[u].append(v)
        self.adjMat[v][u] = 1
        self.adjMat[u][v] = 1
        self.E += 1 
        self.degree[v] += 1
        self.degree[u] += 1

    def edges2adjList(self, V: int, edges: list[list[int]]) -> list[list[int]]:
        """O(V+E) return an adjacency list of a graph from an edge list of a graph
        
        @params
        V: number of vertices
        E: number of edges
        edges: edge list.
        """
        adjList = [[] for _ in range(V)]  # adjList = defaultdict(list)

        for u, v, w in edges:
            adjList[u].append((v, w))
            adjList[v].append((u, w))

        return adjList 


    def adjMat2adjList(self, adjMat: list[list[int]]) -> list[list[int]]:
        """O(V^2) return an adjacency list of a graph from an adjacency matrix of a graph
        
        @params
        adjMat: a V*V matrix. 
                adjMat[i][j] = w: vertex i and j is adjacent
                adjMat[i][j] = 0: vertex i and j is not adjacent
                set adjMat[i][i] = 0. self-loop is not allowed
        """
        V = len(adjMat)
        adjList = [[] for _ in range(V)] # adjList = defaultdict(list)

        for i in range(V):
            for j in range(V):
                if adjMat[i][j]:
                    adjList[i].append((j, adjMat[i][j]))
        return adjList


    def edge2adjMat(self, V: int, edges: list[list[int]]) -> list[list[int]]:
        """O(V^2) return adjacency matrix from edge list

        @params
        V: number of vertices
        E: number of edges
        edges: edge list.
        """
        adjMat = [[0] * V for _ in range(V)]

        for u, v, w in edges:
            adjMat[u][v] = w 
            adjMat[v][u] = w 
     
        return adjMat

    def degreeOfVertex(self, v: int) -> int:
        """O(1) Returns the degree of vertex v"""
        if not (0 <= v < self.V):
            raise IndexError(f"Vertex {v} is not between 0 and {self.V-1}")
        return self.degree[v]  # len(self.adjList[v])

    def degree(self, V: int, edges: list[list[int]]) -> list[int]:
        """O(E) return degree of nodes in an undirected graph 
        
        return a degree array of length V
            degree[i] = degree of vertex i = number of edges connected to that vertex
        """
        degree = [0] * V
        for v, u in edges:
            degree[v] += 1
            degree[u] += 1
        return degree

    def hasSelfLoop(self) -> bool:
        """O(V+E) self-loop detection"""
        for v in range(self.V):
            for u in self.adjList[v]:
                if u == v:
                    return True 
        return False  

    def allSelfLoops(self) -> list[int]:
        """O(V+E) Returns the all the self-loops in the undirected graph"""
        selfloops = set()
        for v in range(self.V):
            for u in self.adjList[v]:
                if u == v:
                    selfloops.add(u)
        return list(selfloops)

    def hasParallelEdges(self) -> bool:
        """O(V+E) Parallel edges detection"""
        visited = [False] * self.V 
        for v in range(self.V):
            # check parallel edges incident on v 
            for u in self.adjList[v]:
                if visited[u]:
                    return True 
                visited[u] = True 
            # reset visited[u] = False for all u
            for u in self.adjList[v]:
                visited[u] = False
        return False

    def isConneted(self) -> bool:
        """O(V+E) Check graph connectivity"""
        def dfs(v: int) -> None:
            """traverse the CC containing vertex v""" 
            visited[v] = True 
            for u in self.adjList[v]:
                if not visited[u]:
                    dfs(u)
        
        def bfs(v: int) -> list[int]:
            """traverse the CC containing vertex v"""
            queue = deque([v])
            visited[v] = True 
            while queue:
                v = queue.popleft() 
                for u in self.adjList[v]:
                    if not visited[u]: 
                        queue.append(u)
                        visited[u] = True 

        visited = [False] * self.V
        dfs(0)          # bfs(0)  choose start vertex 0 or random.choice(range(self.V))
        return sum(visited) == self.V 


    def allCCs(self) -> list[tuple[list, int, int]]:
        """O(V+E) Returns all the connected components (CC) of a graph
           https://algs4.cs.princeton.edu/41graph/CC.java.html
           @return CCs: a 2D array of length the number of CCs, 
                   CCs[i][0]: an array of all the vertices in ith CC.
                   CCs[i][1]: number of vertices in ith CC
                   CCs[i][2]: number of edges in ith CC
        """
        def dfs(v: int) -> tuple[int, int]:
            """return number of vertices in the CC, number of edges in the CC"""              
            nonlocal CCId
            visited[v] = CCId
            
            CC, V, E = [v], 1, 0
            for u in self.adjList[v]:
                if visited[u] == -1:
                    cc, v, e = dfs(u) 
                    CC += cc 
                    V += v 
                    E += 1 + e   # 1 accounts for edge (v, u)
            return CC, V, E

        def bfs(v: int) -> tuple[int, int]:
            """return number of vertices in the CC, number of edges in the CC"""
            nonlocal CCId
            queue = deque([v])
            visited[v] = CCId

            CC, V, E = [v], 1, 0
            while queue:
                v = queue.popleft()
                for u in self.adjList[v]:
                    E += 1
                    if visited[u] == -1: 
                        queue.append(u)
                        CC.append(u)
                        V += 1
                        visited[u] = CCId
            return CC, V, E

        def isConnected(self, v: int, u: int) -> bool:
            """return whether two vertices are connected"""
            return visited[v] == visited[u]   

        CCId = 0                    # index of CC
        visited = [-1] * self.V     # visited[v]: CC index which vertex v is in
        CCs = []
        # 1. O(V+E) perform DFS/BFS of graph
        for v in range(self.V):
            if visited[v] == -1:
                CCs.append(dfs(v))  # bfs(v) 
                CCId += 1

        # # 2. O(V) map each vertex to corresponding CC
        # CCs = [[] for _ in range(CCId)]
        # for v in range(self.V):
        #     CCs[visited[v]].append(v)
        return CCs   

    
    def hasCycle(self) -> bool:
        """O(V+E) Cycle detection"""     
        def dfs(v: int, p: int) -> bool:
            """Cycle detection in the subgraph reachable from vertex v
               @param v, p: current/parent vertex 
               https://algs4.cs.princeton.edu/41graph/Cycle.java.html  
            """ 
            visited[v] = True   # mark vertex as visited

            for u in self.adjList[v]:
                if visited[u]:
                    if u == p:
                        continue 
                    else:
                        return True 
                if dfs(u, v): 
                    return True 
            return False 

        def bfs(v: int, p: int) -> bool:
            """Cycle detection in the subgraph reachable from vertex v
               @param v, p: current/parent vertex 
            """ 
            queue = deque([(v, p)])
            visited[v] = True 
            while queue:
                v, p = queue.popleft()
                for u in self.adjList[v]:
                    if visited[u]:
                        if u == p:
                            continue 
                        else:
                            return True 
                    queue.append((u, v))
                    visited[u] = True 
            return False
        
        # special case: identify parallel edge as a cycle
        if self.hasParallelEdges():
            return True 
        
        visited = [False] * self.V 
        for v in range(self.V):
            if visited[v]:
                continue 
            if dfs(v, -1):  # change here to use bfs(v, -1)
                return True 
        return False 

    def allCycles(self) -> list[list[int]]:
        """O(V+E) Returns all the cycles in the undirected graph (using visited array)
           @return cycles, cycles[i] contains all the vertices in the ith cycle 
        """       
        def dfs(v: int, p: int) -> list[list[int]]:
            """return all the cycles in the subgraph reachable from vertex v
               https://algs4.cs.princeton.edu/41graph/Cycle.java.html
            """
            cycles = []
            visited[v] = 1               # mark vertex as visited but haven't been backtracked

            # search adjacent vertices
            for u in self.adjList[v]:
                
                # case 1: adjacent vertex is visited and backtracked, no cycle
                if visited[u] == 2:             
                    continue       
                
                # case 2: adjacent vertex is visited and not backtracked but is parent, no cycle
                if visited[u] == 1 and u == p:  
                    continue  
                
                # case 3: adjacent vertex is visited and not backtracked and is not parent, a cycle is found
                if visited[u] == 1 and u != p:       
                    # build the cycle by tracing from v to u:  v -> ... -> u (-> v)  
                    cycle = [v]
                    cur = v                 
                    while cur != u:
                        cur = edgeTo[cur]
                        cycle.append(cur)
                    cycles.append(cycle[::-1])  # reverse cycle because vertex u is entry of this cycle
                    continue 
                
                # search cycle in the subgraph reachable from adjacent vertex
                edgeTo[u] = v 
                dfs(u, v)    
            
            visited[v] = 2   # mark the current vertex as backtracked after all the adjacent vertices are explored, means no cycle
            return cycles               
        
        visited = [0] * self.V      # 3 kinds of vertex states  0: unvisited, 1: visited but haven't been backtracked, 2: visited and backtracked
        edgeTo = [-1] * self.V      # to rebuild cycles, edgeTo[v] is parent vertex of vertex v
        cycles = []                 # to store all the cycles, cycles[i] contains all the vertices in the ith cycle 
        
        # traverse all the vertices
        for v in range(self.V):
            if not visited[v]:
                cycles += dfs(v, -1) 
        return cycles 

    def allCycles(self) -> list[list[int]]:
        """O(V+E) Returns all the cycles in a undirected graph (using stack)
            @return  cycles, cycles[i] contains all the vertices in ith cycle 
        """
        def dfs(v: int, p: int) -> list[list[int]]:
            """return all the cycles in the subgraph that is reachable from vertex v."""
            cycles = []
            visited[v] = inStack[v] = True  # Mark vertex as visited and in stack

            # search adjacent vertices
            for u in self.adjList[v]:
                # case 1: adjacent vertex is visited and backtracked, no cycle
                if visited[u] and not inStack[u]:
                    continue 
                
                # case 2: adjacent vertex is visited and not backtracked, but adjacent vertex is parent, no cycle
                if visited[u] and inStack[u] and u == p:
                    continue 
                
                # case 3: adjacent vertex is visited and not backtracked, and adjacent vertex is not parent, find a cycle
                if visited[u] and inStack[u] and u != p:
                    # adjacent vertex is entry of the cycle, rebuild the cycle by tracing from v to u: v -> ... -> u
                    cycle = [v]     
                    cur = v 
                    while cur != u:
                        cur = edgeTo[cur]
                        cycle.append(cur)
                    cycles.append(cycle[::-1])  # reverse the cycle
                    continue 

                edgeTo[u] = v 
                dfs(u, v)
            
            inStack[v] = False  # mark current vertex as backtracked after all of its neighbours are visited
            return cycles 

        visited = [False] * self.V              # visited[u]: whether vertex u is unvisited
        inStack = [False] * self.V              # inStack[u]: whether vertex u is in recursion stack
        edgeTo = [-1] * self.V                  # To rebuild cycles, edgeTo[u]: parent vertex of u
        cycles = []                             # To store all cycles, cycles[i] contains all the vertices in ith cycle 

        # traverse all the vertices
        for v in range(self.V):
            if not visited[v]:
                cycles += dfs(v, -1)
        return cycles
    
    def hasPath(self, source: int, target: int) -> bool:
        """O(V+E) single-source reachability
        return whether a path exists from source vertex to target vertex
        """
        def dfs(v: int, target: int) -> bool:
            """return whether there is a path from current vertex to target vertex
               https://algs4.cs.princeton.edu/41graph/DepthFirstPaths.java.html
            """
            # base case: vertex is target
            if v == target:
                return True
            visited[v] = True   # mark vertex as visited
            # iterates over adjacent vertices
            for u in g[v]:
                if not visited[u] and dfs(u):  # there is a path from adjacent vertex to target vertex
                    return True 
            return False 

        def bfs(source: int, target: int) -> bool:
            """return whether there is a path from current vertex to target vertex"""
            queue = deque([source])
            visited[source] = True 
            while queue:
                v = queue.popleft()
                # case: vertex is target
                if v == target:
                    return True
                # iterates over adjacent vertices
                for u in g[v]:
                    if not visited[u]: 
                        queue.append(u)
                        visited[u] = True
            return False 

        visited = [False] * self.V 
        return dfs(source, target)  # bfs(source, target)

    def onePath(self, source: int, target: int) -> list[int]:
        """Returns a simple path from source vertex to target vertex. 
           O(V+E) DFS/BFS  if using BFS, the path is shortest
           @return a list of vertices. if no such path, return an empty list.
        """
        def dfs(v: int) -> None:
            visited[v] = True
            # base case: vertex is target
            if v == target:
                return 
            for u in self.adjList[v]:
                if not visited[u]:
                    edgeTo[u] = v 
                    dfs(u) 

        def bfs(v: int) -> None:
            """https://algs4.cs.princeton.edu/41graph/BreadthFirstPaths.java.html"""
            queue = deque([v])
            visited[v] = True 
            while queue:
                v = queue.popleft()
                if v == target:
                    return 
                for u in self.adjList[v]:
                    if not visited[u]:
                        queue.append(u) 
                        visited[u] = True 
                        edgeTo[u] = v
                             
        visited = [False] * self.V          # visited[u]: is there an source-u path?
        edgeTo = [0] * self.V               # edgeTo[u]: last edge on source-u path, i.e., parent of vertex u
        dfs(source)  # bfs(source)

        path = []
        if not visited[target]:     # no such path
            return path
        
        cur = target  
        while True:
            path.append(cur)
            if cur == source:
                break 
            cur = edgeTo[cur]
        return path[::-1] 
   
    def allPaths(self, source: int, target: int) -> tuple[int, list[list[int]]]:
        """Returns all the simple paths from source vertex to target vertex. 
           T: O(V*2^V)    O(V) for each path, worst-case 2^V paths
           Warning: there may be exponentially many simple paths in a graph, so no algorithm can run efficiently for large graphs.
        """
        @lru_cache(maxsize=None)
        def dfs(v: int, target: int, path: list[int]) -> tuple[int, list[list[int]]]:
            """return number of paths, and a list of all the paths from vertex v to target vertex
               DFS + backtracking
               https://algs4.cs.princeton.edu/41graph/AllPaths.java.html
            """
            numOfPaths, paths = 0, []
            path.append(v)       # add current vertex to path
            onPath[v] = True     # mark vertex as on path

            # O(V) case 1: vertex is target, add path to answer
            if v == target:
                numOfPaths += 1
                paths.append(path.copy())

            # case 2: vertex is not target, search adjacent vertices
            else:   
                for u in self.adjList[v]:
                    if not onPath[u]:
                        cnt, p = dfs(u, target, path)
                        numOfPaths += cnt 
                        paths += p 
            
            # explicit backtracking
            path.pop()              # remove vertex from path
            onPath[v] = False       # recover on path state of vertex
            return numOfPaths, paths 
        
        def bfs(source: int, target: int, path: list[int]) -> tuple[int, list[list[int]]]:
            """return number of paths, and a list of all the paths from vertex v to target vertex"""
            numOfPaths, paths = 0, []
            path.append(v)   # add vertex to path
            onPath[v] = True  # mark vertex as on path
            queue = deque([(source, path, onPath)])
            while queue:
                v, path = queue.popleft()

                # O(V) case 1: vertex is target, add path to answer
                if v == target:
                    paths.append(path)
                    numOfPaths += 1
                    continue
                # case 2: vertex is not target, search adjacent vertices
                for u in self.adjList[v]:
                    if not onPath[u]:
                        path.append(u)
                        onPath[u] = True 
                        queue.append((u, path.copy(), onPath.copy()))   # implicit backtracking: each adjacent vertex has its own path and onPath, and changes to one path do not affect other paths.
            return numOfPaths, paths

        onPath = [False] * self.V        # a vertex can be visited multiple times in different paths.
        return dfs(source, target, [])  # bfs(source, target, [])  

    def isBipartite(self) -> bool:
        """O(V+E) return whether the graph is bipartite

        an undirected graph is either a bipartite or has an odd-length cycle. 
        """
        def dfs(v: int, color: int) -> bool:
            """O(V+E) return whether the CC containing vertex v is bipartite

            @params color: correct color for vertex v 
            https://algs4.cs.princeton.edu/41graph/Bipartite.java.html
            """
            visited[v] = color                   # color the vertex
            # search adjacent vertices
            for u in self.adjList[v]:
                # adjacent vertex is visited
                if visited[u] != UNCOLORED:
                    # base case 1: colored incorrectly
                    if visited[u] == color:
                        return False 
                    # base case 2: colored correctly
                    else:
                        continue 
                if not dfs(u, color^1):         # flip color
                    return False 
            return True 

        def bfs(v: int, color: int) -> bool:
            """O(V+E) return whether the CC containing vertex v is bipartite

            @params color: color for vertex v 
            """
            queue = deque([(v, color)])
            visited[v] = color 
            while queue:
                v, color = queue.popleft()
                # search adjacent vertices
                for u in self.adjList[v]:
                    if visited[u] != UNCOLORED:
                        # case 1: adjacent vertex is incorrectly colored
                        if visited[u] == color:
                            return False 
                        # case 2: adjacent vertex is correctly colored
                        else:
                            continue 
                    queue.append((u, color^1))  # color for adjacency vertex is flipped color
                    visited[u] = color^1
            return True
        
        UNCOLORED, A, B = 0, 1, 2               # two kinds of colors
        visited = [UNCOLORED] * self.V          # visited[i]: colored state of vertex i, initialized as uncolored
        
        for v in range(self.V):
            if visited[v] == UNCOLORED and not dfs(v, A): # change here to use bfs(v, A)
                return False 
        return True


if __name__ == '__main__':
    edges = [[0,2],[0,5],[2,4],[1,6],[5,4]]
    g = UndirectedGraph(7, edges)
    print(f"Undirected graph {g}")

    # Graph connectivity
    CCs = g.allCCs()
    if len(CCs) > 1:
        print(f"Non-connected graph with {len(CCs)} Connected components:")
        for CC in CCs:
            print(CC)
    else:
        print("Connected graph")

    # Cycle detection
    if g.hasCycle():
        cycles = g.allCycle()
        print(f"Cycles: {cycles}")

    # a simple path from source vertex 0 to every vertex in graph
    source = 0
    print(f"\nDFS source = {source}")
    for target in range(g.V):
        path = g.onePath(source, target, type='dfs')
        print(f"{source} to {target}: {path}")

    # all the simple paths from vertex 0 to vertex 4
    paths = g.allPaths(0, 4, type='dfs')
    print(f"\nall the simple paths from vertex 0 to vertex 4: {paths}")
    
