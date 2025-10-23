def luy_thua(a, n):
    if n == 0:
        return 1
    else:
        return a * luy_thua(a, n - 1)
print("2^5 =", luy_thua(2, 5))
