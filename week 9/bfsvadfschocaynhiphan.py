from collections import deque
from xaydungbsttumang import build_bst
def bfs(root):
    q = deque([root])
    while q:
        node = q.popleft()
        print(node.key, end=' ')
        if node.left:
            q.append(node.left)
        if node.right:
            q.append(node.right)
def dfs(root):
    if root:
        print(root.key, end=' ')
        dfs(root.left)
        dfs(root.right)
arr = [7, 3, 9, 1, 5, 8, 10]
bst = build_bst(arr)
print("BFS:", end=' ')
bfs(bst)
print("\nDFS:", end=' ')
dfs(bst)