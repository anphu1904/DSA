me_cung = [
    [1, 0, 0, 0],
    [1, 1, 0, 1],
    [0, 1, 0, 0],
    [1, 1, 1, 1]
]
n = len(me_cung)
duong_di = [[0] * n for _ in range(n)]
def hop_le(x, y):
    return 0 <= x < n and 0 <= y < n and me_cung[x][y] == 1
def tim_duong(x, y):
    if x == n - 1 and y == n - 1:
        duong_di[x][y] = 1
        for i in range(n):
            for j in range(n):
                print(duong_di[i][j], end=" ")
            print()
        print()
        return
    if hop_le(x, y):
        duong_di[x][y] = 1
        tim_duong(x + 1, y)
        tim_duong(x, y + 1)
        tim_duong(x - 1, y)
        tim_duong(x, y - 1)
        duong_di[x][y] = 0 
print("Các đường đi có thể từ (0,0) đến (n-1,n-1):")
tim_duong(0, 0)