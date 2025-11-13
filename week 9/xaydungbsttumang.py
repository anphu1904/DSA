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
    else:
        root.right = insert(root.right, key)
    return root
def build_bst(arr):
    root = None
    for num in arr:
        root = insert(root, num)
    return root
def inorder(root):
    if root:
        inorder(root.left)
        print(root.key, end=' ')
        inorder(root.right)
arr = [7, 3, 9, 1, 5, 8, 10]
bst = build_bst(arr)
inorder(bst)