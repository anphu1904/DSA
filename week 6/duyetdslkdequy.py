class Nut:
    def __init__(self, du_lieu):
        self.du_lieu = du_lieu
        self.ke_tiep = None

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

print("Duyệt danh sách liên kết:")
duyet_dslk(nut1)
