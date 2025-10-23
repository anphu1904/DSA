def thap_ha_noi(so_dia, cot_nguon, cot_trung_gian, cot_dich):
    if so_dia == 1:
        print("Chuyển đĩa 1 từ", cot_nguon, "sang", cot_dich)
        return
    thap_ha_noi(so_dia - 1, cot_nguon, cot_dich, cot_trung_gian)
    print("Chuyển đĩa", so_dia, "từ", cot_nguon, "sang", cot_dich)
    thap_ha_noi(so_dia - 1, cot_trung_gian, cot_nguon, cot_dich)

n = int(input("Nhập số đĩa: "))
print("Các bước chuyển đĩa:")

thap_ha_noi(n, 'A', 'B', 'C')
