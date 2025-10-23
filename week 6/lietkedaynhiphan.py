def liet_ke_nhi_phan(n, day=""):
    if len(day) == n:
        print(day)
        return
    liet_ke_nhi_phan(n, day + "0")
    liet_ke_nhi_phan(n, day + "1")

n = int(input("Nhập độ dài dãy nhị phân: "))
print("Các dãy nhị phân độ dài", n, ":")
liet_ke_nhi_phan(n)
