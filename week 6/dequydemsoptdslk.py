class Nut:
    def __init__(self, du_lieu):
        self.du_lieu = du_lieu
        self.ke_tiep = None

def dem_phan_tu(nut):
    if nut is None:
        return 0
    return 1 + dem_phan_tu(nut.ke_tiep)

nut1 = Nut(10)
nut2 = Nut(20)
nut3 = Nut(30)
nut4 = Nut(40)

nut1.ke_tiep = nut2
nut2.ke_tiep = nut3
nut3.ke_tiep = nut4

so_luong = dem_phan_tu(nut1)
print("Số phần tử trong danh sách liên kết là:", so_luong)
