from collections import deque
def move(state, pos, direction):
    new_state = list(state)
    x, y = divmod(pos, 3)
    if direction == 'up' and x > 0:
        swap_pos = pos - 3
    elif direction == 'down' and x < 2:
        swap_pos = pos + 3
    elif direction == 'left' and y > 0:
        swap_pos = pos - 1
    elif direction == 'right' and y < 2:
        swap_pos = pos + 1
    else:
        return None
    new_state[pos], new_state[swap_pos] = new_state[swap_pos], new_state[pos]
    return tuple(new_state)
def bfs_8_puzzle(start, goal):
    q = deque([(start, [])])
    visited = set([start])
    while q:
        state, path = q.popleft()
        if state == goal:
            return path
        pos = state.index(0)
        for d in ['up', 'down', 'left', 'right']:
            new_state = move(state, pos, d)
            if new_state and new_state not in visited:
                visited.add(new_state)
                q.append((new_state, path + [d]))
    return None
start = (1, 2, 3, 4, 0, 5, 6, 7, 8)
goal = (1, 2, 3, 4, 5, 0, 6, 7, 8)
print("Giải pháp BFS:", bfs_8_puzzle(start, goal))