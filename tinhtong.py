def tong(n):
    if n == 1:
        return 1
    else:
        return n + tong(n - 1)
print("Tổng từ 1 đến 5 là:", tong(5))