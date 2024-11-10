"""
search in grid

a 2D grid is an unweighted undirected graph
"""
from collections import deque 
class Grid:
    # 4 cardinal directions north (N), south (S), east (E), west (W)
    N, S, W, E = (-1, 0), (1, 0), (0, -1), (0, 1)
    # 4 intercardinal/ordinal directions, northeast (NE), southeast (SE), southwest (SW), northwest (NW).
    NE, SE, SW, NW = (-1, 1), (1, 1), (1, -1), (-1, -1)
    DIRECTIONS = [N, S, W, E, NE, SE, SW, NW] 

    @classmethod 
    def hasPath(cls, grid: list[list[int]], source: list[int], target: list[int]) -> bool:
        """
        return whether there is a path from source cell to target cell
        T: O(mn)  S: O(mn)
        """
        def bfs(row: int, col: int) -> bool: 
            queue = deque([(row, col)])           # enqueue source cell
            visited[row][col] = True 
            
            while queue:
                row, col = queue.popleft()

                # case: cell is target
                if [row, col] == target:
                    return True

                # search adjacent cells
                for dx, dy in Grid.DIRECTIONS:
                    nrow, ncol = nrow, ncol
                    # case 1: adjacent cell is out of boundary
                    if not (0 <= nrow < m and 0 <= ncol < n):
                        continue 
                    # case 2: adjacent cell is visited
                    if visited[nrow][ncol]:
                        continue 
                    queue.append((nrow, ncol))  # enqueue adjacent cell
                    visited[nrow][ncol] = True  # mark adjacent cell as visited
            return False

        def dfs(row: int, col: int) -> bool:
            # base case: cell is target
            if [row, col] == target:
                return True 

            visited[row][col] = True  # mark cell as visited
            
            # search adjacent cells
            for dx, dy in Grid.DIRECTIONS:
                nrow, ncol = row+dx, col+dy 
                # case 1: adjacent cell is out of boundary
                if not (0 <= nrow < m and 0 <= ncol < n):
                    continue  

                # case 2: adjacent cell is visited
                if visited[nrow][ncol]:
                    continue 

                if dfs(nrow, ncol):
                    return True
            return False

        m, n = len(grid), len(grid[0])
        visited = [[False] * n for _ in range(m)] 
        dfs(*source)   # change here to use bfs(*source)

    @classmethod
    def allCCs(cls, grid: list[list[int]], val: int) -> list[tuple[list[tuple[int, int]], int, bool]]:
        """Returns all the connected components (CC) of grid
           T: O(mn) S: O(mn)

           @Args 
           grid: 2D array
           val: value of cells in the CC

           @return CCs: a 2D array of length the number of CCs, 
                CCs[i][0]: list[tuple[int, int]], an array of all the cells in ith CC.
                CCs[i][1]: int, number of cells in ith CC
                CCs[i][2]: bool, whether ith CC is closed
        """
        def dfs(row: int, col: int) -> tuple[list[tuple[int]], int, bool]:
            """
            O(mn) search the CC from cell (row, col)

            return a tuple of all the cells in this CC, number of cells in the CC, whether CC is closed
            """
            nonlocal CCId
            visited[row][col] = True  # mark cell as visited
            CC = [(row, col)]
            SIZE = 1
            
            # search adjacent cells
            FLAG = True 
            for dx, dy in Grid.DIRECTIONS:
                nrow, ncol = row+dx, col+dy 
                # case 1: adjacent cell is out of boundary
                if not (0 <= nrow < m and 0 <= ncol < n):
                    FLAG = False 
                    continue  
                
                # case 2: adjacent cell is visited 
                if visited[row][col]:
                    continue 

                # case 3: adjacent cell is not target
                if grid[row][col] != val:
                    continue 
                
                cc, size, flag = dfs(nrow, ncol)
                CC += cc 
                SIZE += size 
                if not flag:
                    FLAG = False 
            return CC, SIZE, FLAG  

        def bfs(row: int, col: int) -> tuple[list[tuple[int]], int, bool]:
            """
            O(mn) search the CC from cell (row, col)

            return a tuple of all the cells in this CC, number of cells in the CC, whether CC is closed
            """
            queue = deque([(row, col)])        # enqueue the cell
            visited[row][col] = True           # mark cell as visited
            size = 1
            cells = [(row, col)]
            flag = True 

            while queue:
                row, col = queue.popleft()

                # search adjacent cells
                for dx, dy in Grid.DIRECTIONS:
                    nrow, ncol = row+dx, col+dy 
                    # case 1: adjacent cell is out of boundary
                    if not (0 <= nrow < m and 0 <= ncol < n):
                        flag = False 
                        continue 
                    # case 2: adjcent cell is visited
                    if visited[nrow][ncol]:
                        continue 
                    
                    # case 3: adjacent cell is not target
                    if grid[nrow][ncol] != val:
                        continue
                    queue.append((nrow, ncol))           # enqueue adjacent cell
                    visited[nrow][ncol] = True           # mark adjacent cell as visited
                    size += 1
                    cells.append((nrow, ncol)) 
            return cells, size, flag  
                                 
        m, n = len(grid), len(grid[0])
        visited = [[False] * n for _ in range(m)]
        CCId = 0
        closedCnt = 0 # number of closed CC 
        CCs = []
        
        # 1. O(mn) perform DFS/BFS of grid
        for i in range(m):
            for j in range(n):
                if grid[i][j] == val and not visited[i][j]:
                    cells, size, flag = dfs(i, j)   # change here to use bfs(i, j)
                    CCs.append((cells, size, flag))   
                    CCId += 1
                    if flag:
                        closedCnt += 1

        # 2. O(mn) map each cell to corresponding CC
        # CCs = [[] for _ in range(CCId)]
        # for i in range(m):
        #     for j in range(n):
        #         CCs[visited[i][j]].append((i, j))
        return CCs  
    

    @classmethod
    def SSSP(cls, grid: list[list[int]], source: tuple[int], target: tuple[int]) -> int:
        """
        BFS single-source shortest path
        T: O(mn)  S: O(mn)
        @params
        grid: a 2D array
        source: index of source cell (sx, sy)
        target: index of target cell (tx, ty)
        return: shortest distance from source cell to target cell
        """
        m, n = len(grid), len(grid[0])
        visited = [[False]* n for _ in range(m)]
        row, col = source
        queue = deque((row, col, 0))     # enqueue source cell 
        visited[row][col] = True 
        while queue:
            row, col, d = queue.popleft()

            # case: cell is target
            if (row, col) == target:
                return d 
            
            # search adjacent cells
            for dx, dy in Grid.DIRECTIONS:
                nrow, ncol = row+dx, col+dy
                # case 1: adjacent cell is out of boundary
                if not (0 <= nrow < m and 0 <= ncol < n):
                    continue 
                # case 2: adjacent cell is visited
                if visited[nrow][ncol]:
                    continue
                queue.append((nrow, ncol, d+1))            # enqueue adjacent cell
                visited[nrow][ncol] = True      # mark adjacent cell as visited
    
    @classmethod
    def MSSP(cls, grid: list[list[int]], src_val: int) -> list[list[float]]:
        """
        BFS multi-source shortest path
        T: O(mn)  S: O(mn)
        @params
        grid: 2D array
        src_val: value of source cells
        return: a distance array. dist[i][j] is shortest distance from source cell to target cell (i, j)
        """
        m, n = len(grid), len(grid[0])
        dist = [[math.inf] * n for _ in range(m)]
        queue = deque()

        # 1. O(mn) enqueue all the source cells
        for i in range(m):
            for j in range(n):
                if grid[i][j] == src_val:
                    queue.append((i, j))
                    dist[i][j] = 0

        # 2. O(mn) search from all source cells simultaneously
        while queue:
            row, col = queue.popleft()

            # search adjacent cells
            for dx, dy in Grid.DIRECTIONS:
                nrow, ncol = row+dx, col+dy 
                # base case 1: adjacent cell is out of boundary
                if not (0 <= nrow < m and 0 <= ncol < n):
                    continue 
                # base case 2: adjacent cell is visited
                if dist[nrow][ncol] <= d+1:
                    continue
                queue.append((nrow, ncol))            # enqueue adjacent cell
                dist[nrow][ncol] = d+1      # mark cell as visited

        return dist
    