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

def find_min(node):
    current = node
    while current.left:
        current = current.left
    return current

def delete(root, key):
    if root is None:
        return None
    if key < root.key:
        root.left = delete(root.left, key)
    elif key > root.key:
        root.right = delete(root.right, key)
    else:
        if root.left and root.right:
            temp = find_min(root.right)
            root.key = temp.key
            root.right = delete(root.right, temp.key)
        elif root.left is None:
            return root.right
        elif root.right is None:
            return root.left
    return root

arr = [50, 30, 70, 20, 40, 60, 80]
root = None
for x in arr:
    root = insert(root, x)

print("Trước khi xóa nút có 2 con (70):", inorder(root))
root = delete(root, 70)
print("Sau khi xóa nút có 2 con (70):", inorder(root))