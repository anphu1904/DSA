class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

def insert_bst(root, key):
    if not root:
        return Node(key)
    if key < root.key:
        root.left = insert_bst(root.left, key)
    elif key > root.key:
        root.right = insert_bst(root.right, key)
    return root

def inorder(root):
    return inorder(root.left) + [root.key] + inorder(root.right) if root else []

def find_min(node):
    current = node
    while current.left:
        current = current.left
    return current

def delete_node(root, key):
    if not root:
        return root
    if key < root.key:
        root.left = delete_node(root.left, key)
    elif key > root.key:
        root.right = delete_node(root.right, key)
    else:
        if not root.left:
            return root.right
        elif not root.right:
            return root.left
        temp = find_min(root.right)
        root.key = temp.key
        root.right = delete_node(root.right, temp.key)
    return root

arr = [50, 30, 70, 20, 40, 60, 80]
root = None
for x in arr:
    root = insert_bst(root, x)

print("Duyệt cây ban đầu:", inorder(root))

root = delete_node(root, 30)
print("Duyệt cây sau khi xóa 30:", inorder(root))