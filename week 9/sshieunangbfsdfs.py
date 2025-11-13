import time
from collections import deque
def bfs(graph, start, goal):
    q = deque([(start, [start])])
    visited = set([start])
    while q:
        node, path = q.popleft()
        if node == goal:
            return path
        for nei in graph[node]:
            if nei not in visited:
                visited.add(nei)
                q.append((nei, path + [nei]))
    return None
def dfs(graph, start, goal):
    stack = [(start, [start])]
    visited = set()
    while stack:
        node, path = stack.pop()
        if node == goal:
            return path
        if node not in visited:
            visited.add(node)
            for nei in graph[node]:
                stack.append((nei, path + [nei]))
    return None
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['F'],
    'F': []
}
start, goal = 'A', 'F'
t1 = time.time()
path_bfs = bfs(graph, start, goal)
t_bfs = time.time() - t1
t2 = time.time()
path_dfs = dfs(graph, start, goal)
t_dfs = time.time() - t2
print("BFS path:", path_bfs, "time:", round(t_bfs, 6), "s")
print("DFS path:", path_dfs, "time:", round(t_dfs, 6), "s")