class Nut:
    def __init__(self, du_lieu):
        self.du_lieu = du_lieu
        self.ke_tiep = None

def dao_nguoc_dslk(nut):
    if nut is None or nut.ke_tiep is None:
        return nut
    nut_moi = dao_nguoc_dslk(nut.ke_tiep)
    nut.ke_tiep.ke_tiep = nut
    nut.ke_tiep = None
    return nut_moi

def duyet_dslk(nut):
    if nut is None:
        return
    print(nut.du_lieu, end=" ")
    duyet_dslk(nut.ke_tiep)

nut1 = Nut(1)
nut2 = Nut(2)
nut3 = Nut(3)
nut4 = Nut(4)

nut1.ke_tiep = nut2
nut2.ke_tiep = nut3
nut3.ke_tiep = nut4

print("Danh sách ban đầu:")
duyet_dslk(nut1)

nut_moi = dao_nguoc_dslk(nut1)
print("\nDanh sách sau khi đảo ngược:")
duyet_dslk(nut_moi)