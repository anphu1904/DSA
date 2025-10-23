def tim_kiem(mang, n, gia_tri):
    if n == 0:
        return False
    if mang[n - 1] == gia_tri:
        return True
    return tim_kiem(mang, n - 1, gia_tri)

mang_so = [1, 2, 3, 4, 5]
gia_tri_can_tim = 3

print("Mảng:", mang_so)
print("Tìm thấy", gia_tri_can_tim, "trong mảng?", tim_kiem(mang_so, len(mang_so), gia_tri_can_tim))
