"""
calculate degree of a graph
"""
def degreeUndirected(V: int, edges: List[List[int]]) -> List[int]:
    """O(E) return degree of nodes in an undirected graph 
    
    return a degree array of length V
           degree[i] = degree of vertex i = number of edges connected to that vertex
    """
    degree = [0] * V
    for v, u in edges:
        degree[v] += 1
        degree[u] += 1
    return degree 

def degreeDirected(V: int, edges: List[List[int]]) -> List[int]:
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