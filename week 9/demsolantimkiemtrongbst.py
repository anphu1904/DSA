from xaydungbsttumang import build_bst
def search_bst(root, key):
    comparisons = 0
    while root:
        comparisons += 1
        if key == root.key:
            return True, comparisons
        elif key < root.key:
            root = root.left
        else:
            root = root.right
    return False, comparisons
arr = [7, 3, 9, 1, 5, 8, 10]
bst = build_bst(arr)
print("Tìm 9:", search_bst(bst, 9))
print("Tìm 6:", search_bst(bst, 6))