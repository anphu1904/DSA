def dao_nguoc(mang, trai, phai):
    if trai >= phai:
        return
    mang[trai], mang[phai] = mang[phai], mang[trai]
    dao_nguoc(mang, trai + 1, phai - 1)

mang_so = [1, 2, 3, 4, 5]
print("Mảng ban đầu:", mang_so)

dao_nguoc(mang_so, 0, len(mang_so) - 1)
print("Mảng sau khi đảo ngược:", mang_so)
