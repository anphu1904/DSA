def tim_kiem_nhi_phan(arr, x):
    left, right = 0, len(arr) - 1
    comparisons = 0
    while left <= right:
        comparisons += 1
        mid = (left + right) // 2
        if arr[mid] == x:
            return mid, comparisons
        elif arr[mid] < x:
            left = mid + 1
        else:
            right = mid - 1
    return -1, comparisons
arr = [1, 3, 5, 7, 9, 11]
print("Tìm 7:", tim_kiem_nhi_phan(arr, 7))
print("Tìm 4:", tim_kiem_nhi_phan(arr, 4))