"""
   A directed graph, implemented using an array of lists.
   Parallel edges and self-loops allowed.
"""
from collections import deque 

class Digraph:

    def __init__(self, v: int, edges: list[tuple[int, int]] =None) -> None:
        """Initialize an empty digraph with v vertices and 0 edges."""
        self.V = v                              # number of vertices
        self.E = 0                              # number of edges
        self.adj = [[] for _ in range(self.V)]  # adjacency list of a graph
        self.edges = edges                      # edge list of a graph
        self.indeg = [0] * self.V               # indegree[v] indegree of vertex v
        self.outdeg = [0] * self.V              # outdegree[v] outdegree of vertex v

        # construct adjacency list
        if edges:
            for v, w in edges:
                self.add_edge(v, w)

    def __str__(self) -> str:
        """Returns an edge list representation of graph"""
        s = f"{self.V} vertices, {self.E} edges"

        for v in range(self.V):   # print vertex v and its neighbors
            s += "\n" + f"{v}: {' '.join(str(w) for w in self.adj[v])}"

        return s

    def add_edge(self, v: int, w: int) -> None:
        """adds the directed edge v->w to this graph"""
        self.adj[v].append(w)
        self.outdeg[w] += 1
        self.indeg[w] += 1
        self.E += 1 

    def indegree(self, v: int) -> int:
        """Returns the in-degree of vertex v"""
        if not (0 <= v < self.V):
            raise IndexError(f"Vertex {v} is not between 0 and {self.V-1}")
        return self.indeg[v]

    def outdegree(self, v: int) -> int:
        """Returns the out-degree of vertex v"""
        if not (0 <= v < self.V):
            raise IndexError(f"Vertex {v} is not between 0 and {self.V-1}")
        return self.outdeg[v]


    def number_of_self_loops(self) -> int:
        """Returns the number of self-loops in graph"""
        count = 0
        for v in range(self.V):
            for w in self.adj[v]:
                if w == v:
                    count += 1
        return count

    def postOrder(self) -> list[list[int]]:
        """Post-order traverse the digraph"""
        visited = [False] * self.V
        res = []

        def dfs(v: int) -> None:
            """遍历当前节点所在的连通分量"""
            visited[v] = True 
            for w in self.adj[v]:
                if not visited[w]:
                    dfs(w)
            res.append(v)
        
        for v in range(self.V):
            if not visited[v]:
                dfs(v)
        
        return res 


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
        """Returns the connected components (CC) of agraph
           
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

    def strongCC(self) -> list[list[int]]:
        """Returns the strong connected components (SCC) of a directed graph
           Kosaraju's algorithm 
           
           @return a 2D array of length the number of SCCs, each element is an array of vertices in a SCC.
        """

        def dfs(v: int) -> None:
            """遍历当前节点所在的强连通分量
                返回该连通分量包含的节点
                @param v: index of vertex v 
            """              
            visited[v] = True
            id[v] = count 
            # 遍历节点的邻接列表
            for w in self.adj[v]:
                if not visited[w]:
                    dfs(w)                  
        # 记录节点的访问状态
        visited = [False] * self.V
        # 记录节点属于的强连通分量
        id = [0] * self.V 
        count = 0

        # 反后序遍历 反向图
        for v in self.reverse().postOrder()[::-1]:
            # 若节点未访问过，说明属于新的强连通分量
            if not visited[v]:
                # 添加该节点所在的新连通分量
                dfs(v)
                count += 1
        
        # 存储强连通分量
        SCC = [[] for _ in range(count)]

        for v in range(self.V):
            SCC[id[v]].append(v)

        return SCC 


    def onePath(self, source: int, target: int, type: str='dfs') -> list[int]:
        """Returns a valid path from source vertex to target vertex. 
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
            
        visited = [False] * self.V  # visited[v] = is there an source->target path?

        # DFS: edge_to[v] = last edge on source->target path  
        # BFS: edge_to[v] = last edge on SHORTEST source->target path
        edge_to = [0] * self.V 

        # only for BFS  dist_to[v] = number of edges SHORTEST source->target path, i.e., shortest path length
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



    def reverse(self) -> 'Digraph':
        """Returns the reverse of digraph  O(E)"""
        g = Digraph(self.V)
        for v, w in self.edges:
            g.add_edge(w, v)
        return g  

    def topological(self) -> list[int]:
        """Returns the topological order of a digraph. O(V+E)
           if digraph is DAG, then it must has at least one topological order.
           if digraph is not a DAG, i.e., has cycle, then it doesn't have topological order.

           @return an empty list if no topological order
        """
        visited = [0] * self.V  # 记录节点的状态  3种：0：未访问，1：已访问未回溯，2：已访问并回溯
        result = []             # 栈：存储所有已回溯的节点. 先入栈的节点在拓扑排序中位于后面
        
        def dfs(v: int) -> bool:
            """判断通过当前节点的路径是否存在拓扑排序
               若存在，返回True；若不存在，返回False 
            """
            if visited[v] == 2:             # 若当前节点已访问并回溯，不需再次访问
                return True       
            elif visited[v] == 1:           # 若当前节点已访问未回溯，说明存在环，不存在拓扑排序
                return False 
            else:                           # 若当前节点还未访问，访问
                visited[v] = 1              # 当前节点标记为已访问未回溯
                for neighbor in self.adj[v]:
                    if not dfs(neighbor):   # 搜索邻接节点
                        return False  
                visited[v] = 2              # 当前节点的所有邻接节点已入栈，回溯完成
                result.append(v)            # 当前节点入栈
                return True 
        
        # 遍历所有个节点，判断节点是否存在拓扑排序
        for v in range(self.V):
            if not dfs(v): 
                return [] 
        
        return result[::-1]


if __name__ == '__main__':
    edges = [[0,2],[0,5],[2,4],[1,6],[5,4]]

    g = Digraph(7, edges)
    
    print(f"Directed graph {g}")

    # path source -> target
    source = 0
    print(f"DFS source = {source}")
    for target in range(g.V):
        g.onePath(source, target, type='dfs')

    source = 0
    print(f"BFS source = {source}")
    for target in range(g.V):
        g.onePath(source, target, type='bfs')
    
    # connected component
    components = g.CC()
    if len(components) > 1:
        print(f"Non-connected graph with {len(components)} Connected components:")
        for c in components:
            print(c)
    else:
        print("Connected graph")

    # strong connected component
    SCC = g.strongCC()
    print(f"{len(SCC)} Strong Connected components:")
    for scc in SCC:
        print(scc)
    
    # topological order
    order = g.topological()
    print(f"Topological order: {order}")
