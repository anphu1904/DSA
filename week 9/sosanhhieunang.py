import time
def tim_kiem_tuan_tu(arr, x):
    for i, v in enumerate(arr):
        if v == x:
            return i
    return -1
def tim_kiem_nhi_phan(arr, x):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == x:
            return mid
        elif arr[mid] < x:
            left = mid + 1
        else:
            right = mid - 1
    return -1
def test(n):
    arr = list(range(n))
    x = n - 1
    start = time.time()
    tim_kiem_tuan_tu(arr, x)
    t1 = time.time() - start
    start = time.time()
    tim_kiem_nhi_phan(arr, x)
    t2 = time.time() - start
    print(f"n={n}: Tuần tự={t1:.6f}s | Nhị phân={t2:.6f}s")
for n in [1000, 10000]:
    test(n)