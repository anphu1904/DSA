def tap_con_tong_m(mang, m, i=0, tap_con=None, tong_hien_tai=0):
    if tap_con is None:
        tap_con = []
    if tong_hien_tai == m:
        print(tap_con)
        return
    if i >= len(mang) or tong_hien_tai > m:
        return
    tap_con.append(mang[i])
    tap_con_tong_m(mang, m, i + 1, tap_con, tong_hien_tai + mang[i])
    tap_con.pop()
    tap_con_tong_m(mang, m, i + 1, tap_con, tong_hien_tai)
mang_so = [2, 3, 5, 7]
M = int(input("Nhập giá trị M: "))
print(f"Các tập con có tổng bằng {M}:")
tap_con_tong_m(mang_so, M)
