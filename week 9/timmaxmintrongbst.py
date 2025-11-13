from xaydungbsttumang import build_bst
def find_min(root):
    while root.left:
        root = root.left
    return root.key
def find_max(root):
    while root.right:
        root = root.right
    return root.key
arr = [7, 3, 9, 1, 5, 8, 10]
bst = build_bst(arr)
print("Min =", find_min(bst))
print("Max =", find_max(bst))