"""
Prim's algorithm for Minimal spanning tree problem
https://algs4.cs.princeton.edu/43mst/PrimMST.java.html
T = O(ElogV)   
S = O(E) for min-heap

1. initialize a MST with a random vertex
2. find all the edges of the MST that connect to new vertices (fringe vertex)
3. add smallest edge to the MST
4. repeat 2-3 until all vertices are visited

MST definition: 
1. a tree of V vertices and V-1 edges
2. connected subgraph of G with smallest total weights containing all the vertices

input: connected undirected weighted graph G
output: either of (1) MSTs (not unique) (2) minimum weights
"""
from heapq import heappush, heappop

class PrimMST:
    def __init__(self, V: int=0, edges: list[tuple[int, int, int]]=None) -> None:
        def process(v: int) -> None:
            """O(logV) push adjacent vertices of vertex v into min-heap"""
            # base case: vertex is visited
            if visited[v]:
                return  
            visited[v] = True 
            for u, w in self.adj[v]:
                heappush(heap, (w, u, v))

        # 1. build adajcency list
        self.V = V 
        self.weight = 0
        self.edges = []
        self.adj = [[] for _ in range(self.V)]
        for u, v, w in edges:
            self.adj[u].append((v, w))
            self.adj[v].append((u, w))
        
        # 2. Prim's algorithm 
        heap = []                     # min-heap: element is tuple (weight, neighbor_node)  each vertex will be pushed into heap once          
        num_taken = 0                 # number of taken edges
        visited = [False] * self.V    # records visited states of vertices to avoid cycle
        
        # O(logV) initialize a MST with a random source vertex 
        # push all the adjacent edges of vertex 0 into the min-heap
        process(0)   

        while heap and num_taken < self.V - 1: # O(E) exit when all the vertices are visited and all the edges are taken
            w, u, v = heappop(heap)   # O(logV) greedy, pop edge with smallset weight 
            # base case: vertex u connected to edge is visited, don't use thie edge
            if visited[u]:
                continue                       
            num_taken += 1                 # increment number of taken edges of MST          
            self.weight += w               # update total weights of MST
            self.edges.append((u, v, w))   # update edge list of MST                    
            process(u)                     # O(logV) push all the adjacent edges of vertex u into the min-heap  
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