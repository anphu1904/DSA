import heapq

def dijkstra(graph, start):
    dist = {n: float('inf') for n in graph}
    dist[start] = 0
    pq = [(0, start)]
    parent = {n: None for n in graph}

    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in graph[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                parent[v] = u
                heapq.heappush(pq, (nd, v))
    return dist, parent

def get_path(parent, end):
    path = []
    while end:
        path.append(end)
        end = parent[end]
    return path[::-1]

graph = {
    "Hanoi": [("Haiphong", 120), ("NinhBinh", 90)],
    "Haiphong": [("Halong", 60)],
    "NinhBinh": [("ThanhHoa", 70)],
    "Halong": [("ThanhHoa", 300)],
    "ThanhHoa": []
}

dist, parent = dijkstra(graph, "Hanoi")
path = get_path(parent, "ThanhHoa")

print("Khoảng cách:", dist["ThanhHoa"])
print("Lộ trình:", path)