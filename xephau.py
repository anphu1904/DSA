def an_toan(ban_co, hang, cot, n):
    for i in range(hang):
        if ban_co[i][cot] == 1:
            return False
    i, j = hang - 1, cot - 1
    while i >= 0 and j >= 0:
        if ban_co[i][j] == 1:
            return False
        i -= 1
        j -= 1
    i, j = hang - 1, cot + 1
    while i >= 0 and j < n:
        if ban_co[i][j] == 1:
            return False
        i -= 1
        j += 1
    return True

def xep_hau(ban_co, hang, n):
    if hang == n:
        for i in range(n):
            for j in range(n):
                print("H" if ban_co[i][j] == 1 else ".", end=" ")
            print()
        print()
        return
    for cot in range(n):
        if an_toan(ban_co, hang, cot, n):
            ban_co[hang][cot] = 1
            xep_hau(ban_co, hang + 1, n)
            ban_co[hang][cot] = 0

n = int(input("Nhập số quân hậu: "))
ban_co = [[0] * n for _ in range(n)]
print("Các cách xếp hậu:")
xep_hau(ban_co, 0, n)