# graph representation

# Definition for a graph node.
class Node:
    def __init__(self, val: int = 0, neighbors: List[Node] = None):
        self.val = val
        self.neighbors = neighbors if neighbors else []

def edges2adjList(V: int, edges: List[List[int]], type: str ='undirected') -> List[List[int]]:
    """O(V+E) return an adjacency list of a graph from an edge list of a graph
    
    @params
    V: number of vertices
    E: number of edges
    edges: edge list.
    type: 'undirected': undirected graph, 'directed': digraph
    """
    g = [[] for _ in range(V)]  # g = defaultdict(list)

    if type == 'undirected':
        for u, v, w in edges:
            g[u].append((v, w))
            g[v].append((u, w))
    elif type == 'directed':
        for u, v in edges:
            g[u].append((v, w))
    return g 


def adjMat2adjList(adjMat: List[List[int]]) -> List[List[int]]:
    """O(V^2) return an adjacency list of a graph from an adjacency matrix of a graph
    
    @params
    adjMat: a V*V matrix. 
            adjMat[i][j] = w: vertex i and j is adjacent
            adjMat[i][j] = 0: vertex i and j is not adjacent
            set adjMat[i][i] = 0. self-loop is not allowed
    """
    V = len(adjMat)
    adj = [[] for _ in range(V)] # adj = defaultdict(list)

    for i in range(V):
        for j in range(V):
            if adjMat[i][j]:
                adj[i].append(j)
    return adj


def edge2adjMat(V: int, edges: List[List[int]], type: str='undirected') -> List[List[int]]:
    """O(V^2) return adjacency matrix from edge list

    @params
    V: number of vertices
    E: number of edges
    edges: edge list.
    type: 'undirected': undirected graph, 'directed': digraph
    """
    adjMat = [[0]*V for _ in range(V)]

    if type == 'undirected':
        for u, v, w in edges:
            adjMat[u][v] = w 
            adjMat[v][u] = w 
    elif type == 'directed':
        for u, v, w in edges:
            adjMat[u][v] = w      
    return adjMat