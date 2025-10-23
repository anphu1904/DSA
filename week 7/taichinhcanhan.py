def tong_tiet_kiem(thu_nhap, chi_tieu, so_thang):
    tiet_kiem_hang_thang = thu_nhap - chi_tieu
    return tiet_kiem_hang_thang * so_thang

thu_nhap = 15000000
chi_tieu = 9000000
so_thang = 12
print("Tổng tiết kiệm:", tong_tiet_kiem(thu_nhap, chi_tieu, so_thang), "VND")