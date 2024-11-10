"""
Kruskal's algorithm for Minimal spanning tree problem

https://algs4.cs.princeton.edu/43mst/KruskalMST.java.html
T: O(ElogE) 
S: O(V+E)    O(V) for parent array and rank array in union find disjoint set. 
             O(E) for sorted edges array

1. initialize V MSTs, treating each vertex in the graph as a separate MST. 
2. combines 2 MSTs by adding the smallest edge between them
3. repeat step2 until all vertices are included in a single MST. 

MST definition: 
1. a tree of V vertices and V-1 edges
2. connected subgraph of G with smallest total weights containing all the vertices

input: connected undirected weighted graph G
output: either of (1) MSTs (not unique) (2) minimum weights
"""
class UnionFind:                                
    def __init__(self, n: int) -> None:
        """
        build n disjoint sets from n vertices
        T: O(N)
        """
        self.parents = list(range(n))    # S: O(V) parrent array: parent vertex of each vertex
        self.ranks = [0] * n            # rank array: max height of each vertex
        self.sizeSets = [1] * n         # size of each disjoint set
        self.numSets = n                # number of disjoint sets

    def findSet(self, i: int) -> int:
        """return root of vertex i's set
           T: amortized O(α(N))  effectively O(1)
             first O(N) then O(1)
           path-compression  
           Recursion
        """
        if self.parents[i] == i:
            return i
        else:
            self.parents[i] = self.findSet(self.parents[i])
            return self.parents[i]

    def isSameSet(self, i: int, j: int) -> bool:
        """return whether vertex i and j is in the same set
           T: O(α(N) first O(N) then O(1)
        """
        # path compression twice
        return self.findSet(i) == self.findSet(j)

    def unionSet(self, i: int, j: int) -> None:
        """if vertice i and j are from two disjoint sets, union this two sets
           union by rank   shorter tree as subtree of higher tree
           T: amortized O(α(N))  effectively O(1)
             first O(N) then O(1)
        """
        # base case: two vertices are from the same set
        # indirect path-compression   call findSet() twice
        if self.isSameSet(i, j):
            return
        ip, jp = self.findSet(i), self.findSet(j)
        # case 1: tree i is shortest than j, connect i to root of j, rank of new tree remains unchanged
        if self.ranks[ip] < self.ranks[jp]:
            self.parents[ip] = jp
            self.sizeSets[jp] += self.sizeSets[ip]
        # case 2: tree j is shortest than i, connect j to root of i, rank of new tree remains unchanged
        elif self.ranks[jp] < self.ranks[ip]:
            self.parents[jp] = ip
            self.sizeSets[ip] += self.sizeSets[jp]
        # case 3: two trees of equal height, choose either method, increment rank of new tree
        else:
            self.parents[jp] = ip
            self.sizeSets[ip] += self.sizeSets[jp]
            self.ranks[ip] += 1     # increment rank of new tree
        self.numSets -= 1           # decrement number of disjoint sets

    def sizeOfSet(self, i: int) -> int:
        """O(1) return size of disjoint set containing vertex i"""
        return self.sizeSets[self.findSet(i)]

    def numDisjointSets(self) -> int:
        """O(1) return number of disjoint sets"""
        return self.numSets


class KruskalMST:
    def __init__(self, v: int, edges: list[tuple[int, int, int]]) -> None:
        """Compute a MST for a undirected weighted graph
           T: O(ElogE) S: O(E)
        """
        self.V = v                              # total number of vertices
        self.weight = 0                         # total cost
        self.edges = []                         # edges of MST. edges[i]: (u, v, w) w: weight, u and v: vertices         
        num_taken = 0           # number of taken edges
        UF = UnionFind(self.V)  # initialize union find disjoint set with V isolated vertices

        # 1. O(E log E) sorting by weight ascendingly and small vertex and large vertex
        edges = sorted([(w, u, v) for u, v, w in edges])                                      

        # 2. O(E) union and find  
        for w, u, v in edges: 
            # base case 1: V-1 edges are taken, exit iterating edges                          
            if num_taken == self.V - 1:
                break
            # base case 2: O(1) a cycle will be formed by adding this edge
            if UF.isSameSet(u, v):    
                continue   
            UF.unionSet(u, v)               # O(1) connect two vertices u and v by an edge   
            num_taken += 1                  # increment number of edges taken
            self.weight += w                # update total weightes
            self.edges.append((u, v, w))    # add this edge to MST
        # return self.weight, self.edges 


if __name__ == '__main__':

    edges = [(4, 5, 0.35), (4, 7, 0.37), (5, 7, 0.28), (0, 7, 0.16),
    (1, 5, 0.32), (0, 4, 0.38), (2, 3, 0.17), (1, 7, 0.19),
    (0, 2, 0.26), (1, 2, 0.36), (1, 3, 0.29), (2, 7, 0.34),
    (6, 2, 0.40), (3, 6, 0.52), (6, 0, 0.58), (6, 4, 0.93)]

    g = KruskalMST(8, edges)

    print(f"MST Kruskal")

    print(f"weight = {g.weight}")

    print(f"edges = {g.edges}")

