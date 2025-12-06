from collections import deque
import heapq
import time
from typing import Dict, List, Optional, Tuple, Generator
Cell = Tuple[int, int]
class Solver:
    """
    Full pathfinding solver with both batch and generator/animation-friendly methods:
      - BFS (batch + generator)
      - DFS (batch + generator)
      - Dijkstra (batch + generator)
      - A* (batch + generator)

    Generator mode yields visited cells one-by-one. When generator finishes it returns
    a result dictionary (via StopIteration.value) containing:
      {
        "visited_order": [...],
        "parent": {...},
        "path": [...],
        "visited_count": int,
        "time_ms": int
      }
    """
    def __init__(self, grid: List[List[int]]):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if self.rows else 0
    # Tính năng
    def in_bounds(self, r: int, c: int) -> bool:
        return 0 <= r < self.rows and 0 <= c < self.cols
    def is_free(self, r: int, c: int) -> bool:
        return self.in_bounds(r, c) and self.grid[r][c] == 0
    def neighbors(self, cell: Cell):
        r, c = cell
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if self.is_free(nr, nc):
                yield (nr, nc)
    # ----------------- PATH RECONSTRUCTION -----------------
    @staticmethod
    def get_path(parent: Dict[Cell, Optional[Cell]], goal: Cell) -> List[Cell]:
        if not parent or goal not in parent:
            # handle case goal==start
            if goal in parent:
                return [goal]
            return []
        path = []
        cur = goal
        while cur is not None:
            path.append(cur)
            cur = parent.get(cur)
        path.reverse()
        return path

    # ----------------- BFS (generator for animation) -----------------
    def solve_bfs_generator(self, start: Cell, goal: Cell) -> Generator[Cell, None, Dict]:
        start_time = time.perf_counter()
        if start is None or goal is None:
            return {'visited_order': [], 'parent': {}, 'path': [], 'visited_count': 0, 'time_ms': 0}

        if not self.is_free(*start) or not self.is_free(*goal):
            return {'visited_order': [], 'parent': {}, 'path': [], 'visited_count': 0, 'time_ms': 0}

        q = deque([start])
        parent: Dict[Cell, Optional[Cell]] = {start: None}
        visited_set = {start}
        visited_order: List[Cell] = []
        found = False

        while q:
            cur = q.popleft()
            visited_order.append(cur)

            # yield for animation (dequeued = visited)
            yield cur

            if cur == goal:
                found = True
                break

            for nb in self.neighbors(cur):
                if nb not in visited_set:
                    visited_set.add(nb)
                    parent[nb] = cur
                    q.append(nb)

        path = self.get_path(parent, goal) if found else []
        elapsed_ms = int((time.perf_counter() - start_time) * 1000)
        return {
            'visited_order': visited_order,
            'parent': parent,
            'path': path,
            'visited_count': len(visited_order),
            'time_ms': elapsed_ms
        }

    # ----------------- BFS (batch) -----------------
    def run_bfs(self, start: Cell, goal: Cell):
        if start is None or goal is None:
            return [], {}, []
        if not self.is_free(*start) or not self.is_free(*goal):
            return [], {}, []

        q = deque([start])
        parent: Dict[Cell, Optional[Cell]] = {start: None}
        visited_set = {start}
        visited_order: List[Cell] = []
        found = False

        while q:
            cur = q.popleft()
            visited_order.append(cur)

            if cur == goal:
                found = True
                break

            for nb in self.neighbors(cur):
                if nb not in visited_set:
                    visited_set.add(nb)
                    parent[nb] = cur
                    q.append(nb)

        path = self.get_path(parent, goal) if found else []
        return visited_order, parent, path

    # ----------------- DFS (generator) -----------------
    def solve_dfs_generator(self, start: Cell, goal: Cell) -> Generator[Cell, None, Dict]:
        start_time = time.perf_counter()
        if start is None or goal is None:
            return {'visited_order': [], 'parent': {}, 'path': [], 'visited_count': 0, 'time_ms': 0}
        if not self.is_free(*start) or not self.is_free(*goal):
            return {'visited_order': [], 'parent': {}, 'path': [], 'visited_count': 0, 'time_ms': 0}

        stack = [start]
        parent: Dict[Cell, Optional[Cell]] = {start: None}
        visited_set = set()
        visited_order: List[Cell] = []
        found = False

        while stack:
            cur = stack.pop()

            # If we haven't visited cur yet, mark visited and yield
            if cur not in visited_set:
                visited_set.add(cur)
                visited_order.append(cur)
                yield cur  # visited

                if cur == goal:
                    found = True
                    break

                # push neighbors (we reverse to preserve up/down/left/right order visually)
                neighs = list(self.neighbors(cur))
                for nb in reversed(neighs):
                    if nb not in visited_set:
                        parent[nb] = cur
                        stack.append(nb)

        path = self.get_path(parent, goal) if found else []
        elapsed_ms = int((time.perf_counter() - start_time) * 1000)
        return {
            'visited_order': visited_order,
            'parent': parent,
            'path': path,
            'visited_count': len(visited_order),
            'time_ms': elapsed_ms
        }

    # ----------------- DFS (batch) -----------------
    def run_dfs(self, start: Cell, goal: Cell):
        if start is None or goal is None:
            return [], {}, []
        if not self.is_free(*start) or not self.is_free(*goal):
            return [], {}, []

        stack = [start]
        parent: Dict[Cell, Optional[Cell]] = {start: None}
        visited_set = set()
        visited_order: List[Cell] = []
        found = False

        while stack:
            cur = stack.pop()

            if cur not in visited_set:
                visited_set.add(cur)
                visited_order.append(cur)

                if cur == goal:
                    found = True
                    break

                neighs = list(self.neighbors(cur))
                for nb in reversed(neighs):
                    if nb not in visited_set:
                        parent[nb] = cur
                        stack.append(nb)

        path = self.get_path(parent, goal) if found else []
        return visited_order, parent, path

    # ----------------- Dijkstra (generator) -----------------
    def solve_dijkstra_generator(self, start: Cell, goal: Cell) -> Generator[Cell, None, Dict]:
        start_time = time.perf_counter()
        if start is None or goal is None:
            return {'visited_order': [], 'parent': {}, 'path': [], 'visited_count': 0, 'time_ms': 0}
        if not self.is_free(*start) or not self.is_free(*goal):
            return {'visited_order': [], 'parent': {}, 'path': [], 'visited_count': 0, 'time_ms': 0}

        pq = []
        gscore: Dict[Cell, float] = {start: 0}
        parent: Dict[Cell, Optional[Cell]] = {start: None}
        heapq.heappush(pq, (0, start))
        closed = set()
        visited_order: List[Cell] = []
        found = False

        while pq:
            cost, cur = heapq.heappop(pq)
            if cur in closed:
                continue
            closed.add(cur)
            visited_order.append(cur)

            # yield when popped = visited in Dijkstra
            yield cur

            if cur == goal:
                found = True
                break

            for nb in self.neighbors(cur):
                new_cost = gscore[cur] + 1  # uniform weight = 1
                if new_cost < gscore.get(nb, float("inf")):
                    gscore[nb] = new_cost
                    parent[nb] = cur
                    heapq.heappush(pq, (new_cost, nb))

        path = self.get_path(parent, goal) if found else []
        elapsed_ms = int((time.perf_counter() - start_time) * 1000)
        return {
            'visited_order': visited_order,
            'parent': parent,
            'path': path,
            'visited_count': len(visited_order),
            'time_ms': elapsed_ms
        }

    # ----------------- Dijkstra (batch) -----------------
    def run_dijkstra(self, start: Cell, goal: Cell):
        if start is None or goal is None:
            return [], {}, []
        if not self.is_free(*start) or not self.is_free(*goal):
            return [], {}, []

        pq = []
        gscore: Dict[Cell, float] = {start: 0}
        parent: Dict[Cell, Optional[Cell]] = {start: None}
        heapq.heappush(pq, (0, start))
        closed = set()
        visited_order: List[Cell] = []

        while pq:
            cost, cur = heapq.heappop(pq)
            if cur in closed:
                continue
            closed.add(cur)
            visited_order.append(cur)

            if cur == goal:
                break

            for nb in self.neighbors(cur):
                new_cost = gscore[cur] + 1
                if new_cost < gscore.get(nb, float("inf")):
                    gscore[nb] = new_cost
                    parent[nb] = cur
                    heapq.heappush(pq, (new_cost, nb))

        path = self.get_path(parent, goal) if goal in parent else []
        return visited_order, parent, path

    # ----------------- A* (generator) -----------------
    @staticmethod
    def manhattan(a: Cell, b: Cell) -> int:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def solve_astar_generator(self, start: Cell, goal: Cell) -> Generator[Cell, None, Dict]:
        start_time = time.perf_counter()
        if start is None or goal is None:
            return {'visited_order': [], 'parent': {}, 'path': [], 'visited_count': 0, 'time_ms': 0}
        if not self.is_free(*start) or not self.is_free(*goal):
            return {'visited_order': [], 'parent': {}, 'path': [], 'visited_count': 0, 'time_ms': 0}

        open_heap = []
        gscore: Dict[Cell, float] = {start: 0}
        fscore: Dict[Cell, float] = {start: self.manhattan(start, goal)}
        heapq.heappush(open_heap, (fscore[start], start))
        parent: Dict[Cell, Optional[Cell]] = {start: None}
        closed = set()
        visited_order: List[Cell] = []
        found = False

        while open_heap:
            _, current = heapq.heappop(open_heap)
            if current in closed:
                continue
            closed.add(current)
            visited_order.append(current)

            # yield when popped = visited
            yield current

            if current == goal:
                found = True
                break

            for nb in self.neighbors(current):
                tentative_g = gscore[current] + 1
                if nb in closed:
                    continue
                if tentative_g < gscore.get(nb, float("inf")):
                    parent[nb] = current
                    gscore[nb] = tentative_g
                    f = tentative_g + self.manhattan(nb, goal)
                    fscore[nb] = f
                    heapq.heappush(open_heap, (f, nb))

        path = self.get_path(parent, goal) if found else []
        elapsed_ms = int((time.perf_counter() - start_time) * 1000)
        return {
            'visited_order': visited_order,
            'parent': parent,
            'path': path,
            'visited_count': len(visited_order),
            'time_ms': elapsed_ms
        }

    # ----------------- A* (batch) -----------------
    def run_astar(self, start: Cell, goal: Cell):
        if start is None or goal is None:
            return [], {}, []
        if not self.is_free(*start) or not self.is_free(*goal):
            return [], {}, []

        open_heap = []
        gscore: Dict[Cell, float] = {start: 0}
        fscore: Dict[Cell, float] = {start: self.manhattan(start, goal)}
        heapq.heappush(open_heap, (fscore[start], start))
        parent: Dict[Cell, Optional[Cell]] = {start: None}
        closed = set()
        visited_order: List[Cell] = []

        while open_heap:
            _, current = heapq.heappop(open_heap)
            if current in closed:
                continue
            closed.add(current)
            visited_order.append(current)

            if current == goal:
                break

            for nb in self.neighbors(current):
                tentative_g = gscore[current] + 1
                if nb in closed:
                    continue
                if tentative_g < gscore.get(nb, float("inf")):
                    parent[nb] = current
                    gscore[nb] = tentative_g
                    f = tentative_g + self.manhattan(nb, goal)
                    fscore[nb] = f
                    heapq.heappush(open_heap, (f, nb))

        path = self.get_path(parent, goal) if goal in parent else []
        return visited_order, parent, path

    # ----------------- Unified solve -----------------
    def solve(self, start: Cell, goal: Cell, mode: str = "bfs", as_generator: bool = False):
        """
        Unified entry:
          mode: "bfs", "dfs", "dijkstra", "astar" (or "a*")
          as_generator: if True returns a generator for animation; else returns (visited, parent, path)
        """
        m = mode.lower()
        if as_generator:
            if m == "bfs":
                return self.solve_bfs_generator(start, goal)
            elif m == "dfs":
                return self.solve_dfs_generator(start, goal)
            elif m == "dijkstra":
                return self.solve_dijkstra_generator(start, goal)
            elif m in ("astar", "a*"):
                return self.solve_astar_generator(start, goal)
            else:
                raise ValueError(f"Unknown generator mode: {mode}")
        else:
            if m == "bfs":
                return self.run_bfs(start, goal)
            elif m == "dfs":
                return self.run_dfs(start, goal)
            elif m == "dijkstra":
                return self.run_dijkstra(start, goal)
            elif m in ("astar", "a*"):
                return self.run_astar(start, goal)
            else:
                raise ValueError(f"Unknown solver mode: {mode}")
