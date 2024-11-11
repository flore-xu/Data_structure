"""
   A directed graph
   Parallel edges and self-loops allowed.
"""
from collections import deque
from functools import lru_cache 

class Digraph:
    def __init__(self, v: int, edges: list[tuple[int, int]] =None) -> None:
        """O(V+E) Initialize an empty digraph with v vertices and 0 edges."""
        self.V = v                              # number of vertices
        self.E = 0                              # number of edges
        self.adjList = [[] for _ in range(self.V)]  # adjacency list of a graph
        self.adjMatrix = [[0]*self.V for _ in range(self.V)]   # adjacency matrix of a graph
        self.edges = edges                      # edge list of a graph
        self.indeg = [0] * self.V               # indegree[v] indegree of vertex v
        self.outdeg = [0] * self.V              # outdegree[v] outdegree of vertex v
        self.preorder = []                      # vertices in the pre-order traversal
        self.postorder = []                     # vertices in the post-order traversal
        self.reversePostorder = []              # vertices in the reverse post-order traversal

        # O(E) construct adjacency list, adjacency matrix, indegree array, outdegree array
        for v, u in self.edges:
            self.add_edge(v, u)
        
        # O(V+E) compute preorder, postorder and reverse postorder of graph
        self.depthFirstOrder()

    def __str__(self) -> str:
        """O(V+E) Returns an edge list representation of graph """
        s = f"{self.V} vertices, {self.E} edges"
        for v in range(self.V):   # print vertex v and its neighbors
            s += "\n" + f"{v}: {' '.join(str(u) for u in self.adjList[v])}"
        return s

    def add_edge(self, v: int, u: int) -> None:
        """O(1) adds the directed edge v->u to this graph"""
        self.adjList[v].append(u)
        self.adjMatrix[v][u] = 1
        self.outdeg[u] += 1
        self.indeg[u] += 1
        self.E += 1 

    def depthFirstOrder(self) -> None:
        """O(V+E) compute preorder and postorder for a digraph
           https://algs4.cs.princeton.edu/42digraph/DepthFirstOrder.java.html
        """
        def dfs(v: int) -> None:
            """search the CC containing vertex v"""
            self.preorder.append(v)     # pre-order is order of dfs() calls. Put the vertex on a queue BEFORE the recursive calls.
            visited[v] = True 
            for u in self.adjList[v]:
                if not visited[u]:
                    dfs(u)
            self.postorder.append(v)    # post-order is order in which vertices are done. Put the vertex on a queue AFTER the recursive calls.

        visited = [False] * self.V
        for v in range(self.V):
            if not visited[v]:
                dfs(v)  
        self.reversePostorder = self.postorder[::-1]    # reverse post-order is just reversing post-order. Put the vertex on a stack after the recursive calls.
    
    def reverse(self) -> 'Digraph':
        """O(E) reverse all the edges in the digraph, return a reversed digraph """
        reversedEdges = [(u, v) for v, u in self.edges]
        return Digraph(self.V, reversedEdges)

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
        type: 'undirected': undirected graph, 'directed': digraph
        """
        adjMat = [[0]*V for _ in range(V)]

        for u, v, w in edges:
            adjMat[u][v] = w      
        return adjMat

    def degree(self, V: int, edges: list[list[int]]) -> list[int]:
        """O(E) return degree of nodes in a digraph 

        return a degree array of length V
                degree[i][0] = indegree of vertex i = number of edges coming into the vertex
                degree[i][1] = outdegree of vertex i = number of edges going out from the vertex
        """
        degree = [[0, 0] for _ in range(V)]  # defaultdict(lambda: [0, 0]) if V is unknown
        for v, u in edges:
            degree[v][1] += 1
            degree[u][0] += 1
        return degree

    def indegree(self, v: int) -> int:
        """O(1) Returns the in-degree of vertex v"""
        if not (0 <= v < self.V):
            raise IndexError(f"Vertex {v} is not between 0 and {self.V-1}")
        return self.indeg[v]

    def outdegree(self, v: int) -> int:
        """O(1) Returns the out-degree of vertex v """
        if not (0 <= v < self.V):
            raise IndexError(f"Vertex {v} is not between 0 and {self.V-1}")
        return self.outdeg[v]

    def hasSelfLoop(self) -> bool:
        """O(V+E) self-loop detection """
        for v in range(self.V):
            for u in self.adjList[v]:
                if u == v:
                    return True 
        return False  

    def allSelfLoops(self) -> list[int]:
        """O(V+E) Returns the all the self-loops in graph"""
        selfloops = set()
        for v in range(self.V):
            for u in self.adjList[v]:
                if u == v:
                    selfloops.add(u)
        return list(selfloops)
 
    def hasCycle(self) -> bool:
        """O(V+E) Cycle detection in a digraph (using stack)
           different from undirected graph, 
           adjacent vertex can't be parent of vertex if not a cycle because edge is uni-directional
        """
        def dfs(v: int) -> bool:
            """Cycle detection in the subgraph reachable from vertex v"""
            visited[v] = inStack[v] = True   # mark vertex as visited and put vertex in stack
            # search adjacent vertices
            for u in self.adjList[v]:
                if visited[u]:
                    # case 1: adjacent vertex is visited and is in stack, a cycle is found
                    if inStack[u]:
                        return True 
                    # case 2: adjacent vertex is visited and backtracked, no cycle
                    else:
                        continue 
                if dfs(u):
                    return True 
            inStack[v] = False          # remove vertex from stack
            return False
        
        # special case: identify parallel edge as a cycle
        if self.hasParallelEdges():
            return True 
        
        visited = [False] * self.V
        inStack = [False] * self.V
        for v in range(self.V):
            if not visited[v] and dfs(v):
                return True
        return False


    def hasCycle(self) -> bool:
        """O(V+E) Cycle detection in digraph (using visited array)"""     
        def dfs(v: int) -> bool:
            """Cycle detection in the subgraph reachable from vertex v""" 
            visited[v] = 1     # mark vertex as visited but not backtracked
            for u in self.adjList[v]:
                # case 1: adjacent vertex is visited and backtracked, means no cycle
                if visited[u] == 2:             
                    continue   
                # case 2: adjacent vertex is visited but not backtracked, means a cycle exists, vertex u is entry of this cycle
                if visited[u] == 1:  
                    return True 
                if dfs(u):
                    return True 
            
            visited[v] = 2  # mark vertex as backtracked, means no cycle
            return False 
        
        # special case: identify parallel edge as a cycle
        if self.hasParallelEdges():
            return True 
        
        visited = [0] * self.V      # 3 kinds of vertex states  0: unvisited, 1: visited but haven't been backtracked, 2: visited and backtracked
        for v in range(self.V):
            if not visited[v] and dfs(v, -1):
                return True 
        return False 

    def allCycles(self) -> list[list[int]]:
        """O(V+E) Returns all the cycles in a digraph (using visited array)
            @return cycles: cycles[i] contains all the vertices in ith cycle 
        """
        def dfs(v: int) -> list[list[int]]:
            """return a list of cycles that is reachable from vertex v."""
            cycles = []
            visited[v] = 1          # mark vertex as visited and not backtracked
             
            # search adjacent vertices
            for u in self.adjList[v]:
                # case 1: adjacent vertex is visited and backtracked, means no cycle
                if visited[u] == 2:             
                    continue 
                
                # case 2: adjacent vertex is visited but not backtracked, means a cycle exists, vertex u is entry of this cycle
                if visited[v] == 1:
                    # rebuild cycle from parent vertex: v -> ... -> u
                    cycle = [v]
                    cur = v 
                    while cur != u:
                        cur = edgeTo[cur]
                        cycle.append(cur)
                    cycles.append(cycle[::-1]) 
                    continue 
                
                edgeTo[u] = v           # Keep track of parent vertex
                dfs(u, v)

            visited[v] = 2  # mark vertex as backtracked, means no cycle
            return cycles 

        visited = [0] * self.V                  # 3 kinds of vertex states  0: unvisited, 1: visited but haven't been backtracked, 2: visited and backtracked
        edgeTo = [-1] * self.V                  # to rebuild cycles, edgeTo[u]: parent of vertex u
        cycles = []                             # to store all cycles
        # traverse all the vertices
        for v in range(self.V): 
            if not visited[v]: 
                cycles += dfs(v)
        return cycles  # Return all found cycles


    def allCycles(self) -> list[list[int]]:
        """O(V+E) Returns all the cycles in a digraph (using stack)
            @return cycles: cycles[i] contains all the vertices in ith cycle 
        """
        def dfs(v: int, p: int) -> None:
            """Search the subgraph that is reachable from vertex v.
               https://algs4.cs.princeton.edu/42digraph/DirectedCycle.java.html
            """
            cycles = []
            visited[v] = inStack[v] = True      # Mark vertex as visited and in stack
            
            # search all the adjacent vertices
            for u in self.adjList[v]:
                # case 1: adjacent vertex is visited and backtracked
                if visited[u] and not inStack[u]:
                    continue  
                # case 2: adjacent vertex is visited but not backtracked, a cycle is found 
                if visited[u] and inStack[u]:
                    # adjacent vertex is entry of the cycle, rebuild the cycle by tracing from v to u: v -> ... -> u
                    cycle = [v]
                    cur = v 
                    while cur != u:
                        cur = edgeTo[cur]
                        cycle.append(cur)
                    cycles.append(cycle[::-1]) 
                    continue
                edgeTo[u] = v             # Keep track of parent vertex
                dfs(u, v)
            
            inStack[v] = False      # remove vertex from stack after all the adjacent vertices are explored
            return cycles

        visited = [False] * self.V              # visited[u]: whether vertex u is unvisited
        inStack = [False] * self.V              # inStack[u]: whether vertex u is in recursion stack
        edgeTo = [-1] * self.V                  # To rebuild cycles, edgeTo[u]: parent vertex of u
        cycles = []                             # To store all cycles

        # traverse all the vertices
        for v in range(self.V):  
            if not visited[v]:
                cycles += dfs(v)
        return cycles  # Return all found cycles
    
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
        dfs(0)          # bfs(0) 0 or random.choice(range(self.V))
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
 
    def bruteSCC(self) -> list[list[int]]:
        """O(V(V+E)) brute force 
        https://algs4.cs.princeton.edu/42digraph/BruteSCC.java.html
        Returns the strong connected components (SCC) of a digraph
        """
        # 1. O(V) initialize each vertex in its own SCC
        id = range(self.V)

        # 2. O(V(V+E)) compute transitive closure
        tc = self.transitiveClosure()

        # 3. O(V^2) if vertex v and u are mutually reachable, assign v to u's component
        for v in range(self.V):
            for u in range(v):
                if tc[v][u] and tc[u][v]:
                    id[v] = id[u]
        
        # 4. O(V) count number of SCCs
        cnt = sum(id[v] == v for v in range(self.V))

        # 5. O(V) map each vertex to its corresponding SCC
        SCCs = [[] for _ in range(cnt)]
        for v in range(self.V):
            SCCs[id[v]].append(v)
        return SCCs
 
    def KosarajuSharirSCC(self) -> list[list[int]]:
        """O(V+E) Kosaraju's algorithm
            Returns the strong connected components (SCC) of a digraph
            https://algs4.cs.princeton.edu/42digraph/KosarajuSharirSCC.java.html
           
           @return a 2D array of length the number of SCCs, each element is an array of vertices in a SCC.
        """
        def dfs(v: int) -> None:
            """search the SCC containing vertex v""" 
            nonlocal SCCId
            
            visited[v] = SCCId 
            for u in self.adjList[v]:
                if visited[u] == -1:
                    dfs(u)                  

        def isStronglyConnected(self, v: int, u: int) -> bool:
            """return whether two vertices are strongly connected"""
            return visited[v] == visited[u]
    
        visited = [-1] * self.V   # visited[v]: index of SCC of vertex v, -1 means unvisited
        SCCId = 0                 # index of SCC

        # 1. O(V+E) search reverse graph in the reverse postorder
        for v in self.reverse().reversePostorder:
            if visited[v] == -1:
                dfs(v)
                SCCId += 1
        
        # 2. O(V) map each vertex to its corresponding SCC
        SCCs = [[] for _ in range(SCCId)]
        for v in range(self.V):
            SCCs[visited[v]].append(v)
        return SCCs 


    def TarjanSCC(self) -> list[list[int]]:
        """O(V+E) Tarjan's algorithm 
            https://algs4.cs.princeton.edu/42digraph/TarjanSCC.java.html
            Returns the strong connected components (SCC) of a digraph
           @return a 2D array of length the number of SCCs, each element is an array of vertices in a SCC.
        """
        def dfs(v: int) -> None:
            """search the SCC containing vertex v""" 
            nonlocal preorderCnt, SCCId 
            
            visited[v] = True  
            low[v] = Min = preorderCnt 
            preorderCnt += 1
            stack.append(v)

            for u in self.adjList[v]:
                if not visited[u]:
                    dfs(u)      
                    Min = min(Min, low[u])      # update smallest index of vertices reachable from vertex v

            if Min < low[v]:
                low[v] = Min 
                return 

            while True:
                u = stack.pop()
                id[u] = SCCId 
                low[u] = self.V 
                if u == v:
                    break            
            SCCId += 1

        visited = [False] * self.V
        stack = []
        id = [-1] * self.V       # id[v] = index of SCC containing vertex v
        low = [0] * self.V      # low[v]: smallest index of vertices reachable from vertex v, including the vertex itself.
        preorderCnt = 0         # preorder number counter
        SCCId = 0                 # number of SCCs

        # 1. O(V+E) perform DFS of graph
        for v in range(self.V):
            if not visited[v]:
                dfs(v)
                
        # 2. O(V) map each vertex to its corresponding SCC
        SCCs = [[] for _ in range(SCCId)]
        for v in range(self.V):
            SCCs[id[v]].append(v)
        return SCCs 


    def GabowSCC(self) -> list[list[int]]:
        """O(V+E) Gabow's algorithm (aka Cheriyan-Mehlhorn algorithm)
            Returns the strong connected components (SCC) of a digraph           
            https://algs4.cs.princeton.edu/42digraph/GabowSCC.java.html
           @return a 2D array of length the number of SCCs, each element is an array of vertices in a SCC.
        """
        def dfs(v: int) -> None:
            """search the SCC containing vertex v""" 
            nonlocal preorderCnt, SCCId 
            
            visited[v] = True  
            preorder[v] = preorderCnt 
            preorderCnt += 1
            stack1.append(v)
            stack2.append(v)

            # search adjacent vertices
            for u in self.adjList[v]:
                if visited[u]:
                    if id[u] == -1:
                        while preorder[stack2[-1]] > preorder[u]:
                            stack2.pop()
                    continue 

                dfs(u)      

            # find SCC containing vertex v
            if stack2[-1] == v:
                stack2.pop()
                while True:
                    u = stack1.pop()
                    id[u] = SCCId
                    if u == v:
                        break 
                SCCId += 1            
    
        visited = [False] * self.V
        stack1 = []              # contains vertices of the original graph in preorder
        stack2 = []              # boundary stack. identify the boundaries of SCC
        id = [-1] * self.V       # id[v] = index of SCC containing vertex v
        preorder = [0] * self.V      # preorder[v]: preorder number of vertex v
        preorderCnt = 0         # preorder number counter
        SCCId = 0                 # number of SCCs

        # 1. O(V+E) perform DFS of graph
        for v in range(self.V):
            if not visited[v]:
                dfs(v)
        
        # 2. O(V) map each vertex to its corresponding SCC
        SCCs = [[] for _ in range(SCCId)]
        for v in range(self.V):
            SCCs[id[v]].append(v)
        return SCCs
    
    def hasPath(self, source: int, target: int) -> bool:
        """O(V+E) single-source reachability
        return whether a directed path exist from source vertex to target vertex
        """
        @lru_cache(maxsize=None)
        def dfs(v: int, target: int) -> bool:
            """return whether a valid path exist from vertex v to target vertex
               https://algs4.cs.princeton.edu/42digraph/DirectedDFS.java.html
            """
            # base case: vertex is target
            if v == target:
                return True 
            visited[v] = True   # mark vertex as visited
            # search adjacent vertices
            for u in g[v]:
                if not visited[u] and dfs(u, target):
                    return True
            return False 

        def bfs(source: int, target: int) -> bool: 
            """return whether a valid path exist from source vertex to target vertex"""
            queue = deque([source])     # enqueue source vertex
            visited[source] = True 
            while queue:
                v = queue.popleft() 
                # base case: vertice is target
                if v == target:
                    return True

                # search adjacent vertices
                for u in g[v]:
                    if not visited[u]:
                        queue.append(u)      # enqueue adjacent vertex
                        visited[u] = True 
            return False 

        visited = [False] * self.V 
        return dfs(source, target)  # change here to use bfs(source, target)

    def onePath(self, source: int, target: int) -> list[int]:
        """O(V+E) Returns a valid path from source vertex to target vertex. 
           return a path. if no such path, return an empty list.
        """
        @lru_cache(maxsize=None)
        def dfs(v: int) -> None:
            """https://algs4.cs.princeton.edu/42digraph/DepthFirstDirectedPaths.java.html"""
            # base case: vertex is target 
            if v == target:
                return
            
            visited[v] = True
            for u in self.adjList[v]:
                if not visited[u]:
                    edgeTo[u] = v
                    dfs(u) 

        def bfs(v: int) -> None:
            """https://algs4.cs.princeton.edu/42digraph/BreadthFirstDirectedPaths.java.html"""
            queue = deque([v])
            visited[v] = True 
            while queue:
                v = queue.popleft()
  
                if v == target:
                    return

                for u in self.adjList[v]:
                    if not visited[u]:
                        edgeTo[u] = v 
                        queue.append(u)  
                        visited[u] = True      
            
        visited = [False] * self.V  
        edgeTo = [0] * self.V 
        dfs(source)  # change here to use bfs(source)

        # find path by tracing back
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

    def topological(self) -> list[int]:
        """O(V+E) DFS/BFS Returns the topological order of a digraph. 
           if digraph is DAG, it has at least one topological order.
           if digraph is not a DAG, i.e., has cycle, it doesn't have topological order, return an empty list
        """
        def dfs() -> list[int]:
            """O(V+E) Returns reverse postorder of a digraph.
               https://algs4.cs.princeton.edu/42digraph/Topological.java.html
            """
            if self.hasCycle():
                return []
            return self.reversePostorder
        
            def helper(v: int) -> bool:
                """O(V+E) return whether the CC containing vertex v has cycle"""
                visited[v] = 1              # mark vertex as visited but haven't been backtracked
                
                # search adjacent vertices
                for u in self.adjList[v]:   # if DFS on reversed graph `self.reverse().adjList[v]`, return `top_order` not `top_order[::-1]`
                    # case 1: adjacent vertex is visited and backtracked, means no cycle
                    if visited[u] == 2:             
                        continue       
                    # case 2: adjacent vertex is visited but haven't been backtracked, means a cycle exists, no topological sort. vertex u is entry of this cycle
                    if visited[u] == 1:           
                        return False                     
                    
                    if not helper(u):   # search cycle in the subgraph reachable from neighbor
                        return False  
                visited[v] = 2           # mark vertex as backtracked, means no cycle
                postorder.append(v)      # postorder
                return True 
            
            postorder = []                # stack: store all the backtracked vertices, vertices entered stack/backtracked first is located last of topological sort
            visited = [0] * self.V  # 3 types of visited state of vertex, 0: unvisited, 1: visited but not backtracked, 2: visited and backtracked
            
            for v in range(self.V):
                if not helper(v): 
                    return [] 
            return postorder[::-1]  # reverse postorder

        def bfs(self) -> list[int]:
            """O(V+E) Returns the topological order of a digraph
               https://algs4.cs.princeton.edu/42digraph/TopologicalX.java.html
            """
            top_order = []             # vertices in topological order
            indeg = self.indeg.copy()  # make a copy of indegree array
            cnt = 0                    # number of vertices in the array of topological order

            # enqueue all the vertices with indegree 0, which will be placed first in the topological order
            queue = deque([v for v in range(self.V) if indeg[v] == 0])
            while queue:
                v = queue.popleft()
                top_order.append(v)
                cnt += 1
                # search adjacent vertices
                for u in self.adjList[v]:
                    indeg[u] -= 1           # remove all the incoming edges from vertex v
                    if indeg[u] == 0:       # enqueue adjacent vertex if no incoming edges any more
                        queue.append(u)
            return top_order if cnt == self.V else []  # or check if sum(indeg) == 0
        
        return dfs()  # bfs()

    def transitiveClosure(self) -> list[list[bool]]:
        """O(V(V+E)) return a transitive closure matrix of digraph
            https://algs4.cs.princeton.edu/42digraph/TransitiveClosure.java.html
            suitable for small graph and dense graph, not a solution for the large digraphs 
            transitive closure of a digraph G is another digraph with the same set of vertices, 
            but with an edge from v to u if and only if u is reachable from v in G.
        """
        def dfs(v: int) -> list[int]:
            """O(V+E) return all the vertices that are reachable from vertex v"""
            visited[v] = True
            reachable = [v]

            for u in self.adjList[v]:
                if not visited[u]:
                    reachable += dfs(u) 
            return reachable
        
        tc = [[False]*self.V for _ in range(self.V)]    # a V*V matrix. tc[v][u]: whether u is reachable from v in G
        
        for v in range(self.V):
            visited = [False] * self.V 
            for u in dfs(v):
                tc[v][u] = True
        return tc 

    def FloydWarshallTC(self) -> list[list[bool]]:
        """O(V^3) Floyd Warshall algorithm
            https://algs4.cs.princeton.edu/42digraph/WarshallTC.java.html

            return transitive closure matrix of digraph
            suitable for dense graph, not a solution for the large digraphs 
            transitive closure of a digraph G is another digraph with the same set of vertices, 
            but with an edge from v to u if and only if u is reachable from v in G.
        """
        tc = [[False]*self.V for _ in range(self.V)]    # a V*V matrix. tc[v][u]: whether u is reachable from v in G
        
        # 1. O(V+E) set edges as reachable
        for v in range(self.V):
            for u in self.adjList[v]:
                tc[v][u] = True
            tc[v][v] = True 

        # 2. O(V^3) try path s -> t via vertex i
        for i in range(self.V):             # intermediate vertex
            for s in range(self.V):         # source vertex s
                # optimization
                if not tc[s][i]:
                    continue 
                for t in range(self.V):     # target vertex t
                    if tc[s][i] and tc[i][t]:
                        tc[s][t] = True
        return tc                 

if __name__ == '__main__':
    edges = [[0,2],[0,5],[2,4],[1,6],[5,4]]

    g = Digraph(7, edges)
    
    print(f"Directed graph {g}")

    # path source -> target
    source = 0
    print(f"DFS source = {source}")
    for target in range(g.V):
        g.onePath(source, target)

    # all the simple paths from vertex 0 to vertex 4
    paths = g.allPaths(0, 4)
    print(f"\nall the simple paths from vertex 0 to vertex 4: {paths}")

    # connected component
    CCs = g.allCCs()
    if len(CCs) > 1:
        print(f"Non-connected graph with {len(CCs)} Connected components:")
        for c in CCs:
            print(c)
    else:
        print("Connected graph")

    # strong connected component
    SCCs = g.KosarajuSharirSCC()
    print(f"{len(SCCs)} Strong Connected components:")
    for scc in SCCs:
        print(scc)
    
    # topological order
    order = g.topological()
    print(f"Topological order: {order}")
