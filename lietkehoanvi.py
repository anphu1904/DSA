def hoan_vi(mang, i):
    if i == len(mang) - 1:
        print(mang)
        return
    for j in range(i, len(mang)):
        mang[i], mang[j] = mang[j], mang[i]
        hoan_vi(mang, i + 1)
        mang[i], mang[j] = mang[j], mang[i]

mang_so = [1, 2, 3]
print("Các hoán vị của mảng:", mang_so)
hoan_vi(mang_so, 0)