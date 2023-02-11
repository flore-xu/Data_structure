"""
   An undirected graph, implemented using an array of lists.
   Parallel edges and self-loops allowed.
 """
from collections import deque

class UndirectedGraph:

    def __init__(self, v: int, edges: list[tuple[int, int]]) -> None:
        """Initialize an empty undirected graph with v vertices and 0 edges."""
        self.V = v                              # number of vertices
        self.E = len(edges)                     # number of edges
        self.adj = [[] for _ in range(self.V)]  # adjacency list of graph

        # construct adjacency list
        for v, w in edges:
            self.add_edge(v, w)


    def __str__(self) -> str:
        """Returns an edge list representation of graph"""
        s = f"{self.V} vertices, {self.E} edges"

        for v in range(self.V):   # print vertex v and its neighbors
            s += "\n" + f"{v}: {' '.join(str(w) for w in self.adj[v])}"

        return s

    def add_edge(self, v: int, w: int) -> None:
        """adds the undirected edge v-w to this graph"""
        self.adj[v].append(w)
        self.adj[w].append(v)
        self.E += 1 


    def degree(self, v: int) -> int:
        """Returns the degree of vertex v"""
        if not (0 <= v < self.V):
            raise IndexError(f"Vertex {v} is not between 0 and {self.V-1}")
        return len(self.adj[v])

    def max_degree(self) -> int:
        """Returns the max degree of vertex in graph"""
        max_deg = 0
        for v in self.V:
            max_deg = max(max_deg, self.degree(v))
        return max_deg

    def hasSelfLoop(self) -> bool:
        """Does the graph have a self-loop?"""
        for v in range(self.V):
            for w in self.adj[v]:
                if w == v:
                    return True 
        return False 
    
    def hasCycle(self) -> bool:
        """Cycle detection. 
           @Return True if the graph has a cycle, False otherwise
        """

        def dfs(v: int, parent: int) -> bool:
            """Detect cycle in subgraph reachable from vertex v
               @param v: start vertex   parent: parent vertex of v
            """ 
            visited[v] = True 

            for w in self.adj[v]:
                if not visited[w] and dfs(w, v):
                    return True 
                elif w != parent:
                    return True 
            return False 
        
        # special case: identify parallel edge as a cycle
        if self.hasParallelEdges():
            return True 
        visited = [False] * self.V 
        for v in range(self.V):
            if not visited[v] and dfs(v, -1):
                return True 
        return False 

    def allCycle(self) -> list[list[int]]:
        """Returns all the cycles in a graph. 

           @return  cycles, cycles[i] contains all the vertices in ith cycle 
                    an empty list if no cycle
        """
        visited = [0] * self.V  # 记录节点的状态  3种：0：未访问，1：已访问未回溯，2：已访问并回溯
        cycles = []             # store possible cycles
        edge_to = [0] * self.V  # edge_to[v] is parent vertex of v
        
        def dfs(v: int, parent: int) -> bool:
            """Does the subgraph search from vertex v has cycles?
               若存在，返回True；若不存在，返回False 
               Side effects: change `cycles` if find cycle
            """
            if visited[v] == 2:             # 若当前节点已访问并回溯，不需再次访问
                return False        
            elif visited[v] == 1:           # 若当前节点已访问未回溯，说明存在环，不存在拓扑排序
                cycle = []
                cycle.append(parent)
                cur = parent
                while cur != v:
                    cur = edge_to[cur]
                    cycle.append(cur)
                    
                cycles.append(cycle)
                return True 
            else:                            # 若当前节点还未访问，访问
                edge_to[v] = parent 
                visited[v] = 1               # 当前节点标记为已访问未回溯
                for w in self.adj[v]: # 搜索邻接节点
                    if w != parent and dfs(w, v):        # 子图存在环
                        return True   
                visited[v] = 2              # 当前节点的所有邻接节点已入栈，回溯完成
                return False  
        
        # 遍历所有节点，搜索图中的所有环
        for v in range(self.V):
            if not visited[v]:
                dfs(v, -1) 
        
        return cycles 

    def hasParallelEdges(self) -> bool:
        """Parallel edges detection.
           @return True if the graph have 2 parallel edges, False otherwise
        """
        visited = [False] * self.V 
        for v in range(self.V):
            # check parallel edges incident on v 
            for w in self.adj[v]:
                if visited[w]:
                    return True 
                visited[w] = True 
            # reset visitied[w] = False for all w
            for w in self.adj[v]:
                visited[w] = False
        return False


    def isConneted(self) -> bool:
        """Check if graph is connected
           Return True if connected False otherwise
        """
        visited = [False] * self.V 

        def dfs(v: int) -> None:
            """遍历当前节点所在的连通分量"""
            visited[v] = True 
            for w in self.adj[v]:
                if not visited[w]:
                    dfs(w)
        dfs(0)
        return sum(visited) == self.V 
    
    def CC(self) -> list[list[int]]:
        """Returns the connected components (CC) of a graph
           
           @return a 2D array of length the number of CCs, each element is an array of vertices in a CC.
        """
        def dfs(v: int) -> list[int]:
            """遍历当前节点所在的连通分量
                返回该连通分量包含的节点
                @param v: index of vertex v 
            """
            component = [v]                 
            visited[v] = True

            # 遍历节点的邻接列表
            for w in self.adj[v]:
                if not visited[w]:
                    component += dfs(w)
            return component                    

        # 记录节点的访问状态
        visited = [False] * self.V
        
        # 储存连通分量
        components = []

        # 遍历V个节点
        for v in range(self.V):
            # 若节点未访问过，说明属于新的连通分量
            if not visited[v]:
                # 添加该节点所在的连通分量
                components.append(dfs(v))

        return components


    def onePath(self, source: int, target: int, type: str='dfs') -> list[int]:
        """Returns a simple path from source vertex to target vertex. 
           DFS/BFS O(V+E)
           
           @param type: either 'dfs' or 'bfs' different way to search the graph
           @return a path. if no such path, return an empty list.
        """
        def dfs(v: int) -> None:
            """DFS a CC from vertex v"""
            visited[v] = True

            for w in self.adj[v]:
                if not visited[w]:
                    edge_to[w] = v  
                    dfs(w) 

        def bfs(v: int) -> None:
            """BFS a CC from vertex v"""
            visited[v] = True
            q = deque([v])
            dist_to[v] = 0
            while q:
                v = q.popleft()
                for w in self.adj[v]:
                    if not visited[w]:
                        edge_to[w] = v 
                        dist_to[w] = dist_to[v] + 1
                        q.append(w) 
                        visited[w] = True         
            
        visited = [False] * self.V  # visited[v] = is there an source-target path?

        # DFS: edge_to[v] = last edge on source-target path  i.e. parent vertex of v
        # BFS: edge_to[v] = last edge on SHORTEST source-target path
        edge_to = [0] * self.V 

        # only for BFS  dist_to[v] = number of edges SHORTEST source-target path, i.e., shortest path length
        dist_to = [float('inf')] * self.V   
        
        if type == 'dfs':
            dfs(source)  
        elif type == 'bfs':
            bfs(source)   

        path = []
        if not visited[target]:     # no such path
            print(f"{source} to {target}: not connected")
            return 
            # return path
        
        cur = target  
        while cur != source:
            path.append(cur)
            cur = edge_to[cur]
        path.append(source)

        path = path[::-1]

        if type == 'dfs':     # 0 to 5: [0, 2, 4, 5]
            print(f"{source} to {target}: {path}")
        elif type == 'bfs':   # 0 to 5 (1): [0, 5]    1 is shortest path length
            print(f"{source} to {target} ({dist_to[target]}): {path}")
        
        # return path 

    
    def allPath(self, source: int, target: int) -> list[list[int]]:
        """Returns all the simple paths from source vertex to target vertex. 
           DFS + backtracking
           Warning: there many be exponentially many simple paths in a graph, so no algorithm can run efficiently for large graphs.
           
           @param type: either 'dfs' or 'bfs' different way to search the graph
           @return all the paths. if no such path, return an empty list.
        """
        def dfs(v: int) -> None:
            """搜索从当前节点到达目标节点的路径
            """
            visited[v] = True
            path.append(v)       # add current vertex to path

            if v == target:      # 若当前节点就是目标节点，当前路径加入答案
                paths.append(path.copy())

            for neighbor in self.adj[v]:
                if not visited[neighbor]:
                    dfs(neighbor)   # 搜索从邻接节点到达目标节点的路径
            
            # backtracking: done exploring from v, so remove v from path and recover the visited[v]
            path.pop()
            visited[v] = False

        visited = [False] * self.V
        path, paths = [], []
        dfs(source)

        return paths 

    def isBipartite(self) -> bool:
        """Determine a graph is either (i) a bipartition or (ii) an odd-length cycle. O(V+E)
        """
        visited = [0] * self.V          # 记录所有节点染色情况，初始化都未染色
        A, B = 1, 2                     # 可以染的两种颜色/属于的2种集合

        def dfs(node: int, color: int) -> bool:
            """判断当前节点所在连通分量是否为二分图
               color: 当前节点应染的颜色
            """
            visited[node] = color           # 对当前节点染色
            
            cNei = B if color == A else A   # 邻接节点应染成的颜色
            
            # 遍历所有邻接节点
            for neighbor in self.adj[node]:
                if not visited[neighbor] and not dfs(neighbor, cNei):
                    return False 
                elif visited[neighbor] != cNei:
                    return False 
            return True 

        # 对每个连通分量，任选一个节点染成A，从该节点开始遍历整个分量
        for v in range(self.V):
            if not visited[v] and not dfs(v, A):
                return False 
        
        return True





if __name__ == '__main__':
    edges = [[0,2],[0,5],[2,4],[1,6],[5,4]]

    g = UndirectedGraph(7, edges)
    
    print(f"Undirected graph {g}")

    # a simple path from source 0 to every vertex in graph
    source = 0
    print(f"\nDFS source = {source}")
    for target in range(g.V):
        g.onePath(source, target, type='dfs')

    source = 0
    print(f"\nBFS source = {source}")
    for target in range(g.V):
        g.onePath(source, target, type='bfs')
    
    # all the simple paths from vertex 0 to vertex 4
    paths = g.allPath(0, 4)
    print(f"\nall the simple paths from vertex 0 to vertex 4: {paths}")
    
    components = g.CC()

    if len(components) > 1:
        print(f"Non-connected graph with {len(components)} Connected components:")
        for c in components:
            print(c)
    else:
        print("Connected graph")
    
    # cycle detection
    if g.hasCycle():
        cycles = g.allCycle()
        print(f"Cycles: {cycles}")