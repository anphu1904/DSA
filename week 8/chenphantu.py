class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

def insert(root, key):
    if root is None:
        return Node(key)
    if key < root.key:
        root.left = insert(root.left, key)
    elif key > root.key:
        root.right = insert(root.right, key)
    return root

def inorder(root):
    if root is None:
        return []
    return inorder(root.left) + [root.key] + inorder(root.right)

arr = [50, 30, 70, 20, 40, 60, 80]
root = None
for x in arr:
    root = insert(root, x)

print("BST sau khi chèn:")
print(inorder(root))