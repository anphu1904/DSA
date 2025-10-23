def toi_uu_san_xuat(chi_phi, loi_nhuan, ngan_sach):
    n = len(chi_phi)
    dp = [[0]*(ngan_sach+1) for _ in range(n+1)]

    for i in range(1, n+1):
        for j in range(ngan_sach+1):
            if chi_phi[i-1] <= j:
                dp[i][j] = max(dp[i-1][j], dp[i-1][j-chi_phi[i-1]] + loi_nhuan[i-1])
            else:
                dp[i][j] = dp[i-1][j]
    return dp[n][ngan_sach]

chi_phi = [10, 20, 30]
loi_nhuan = [60, 100, 120]
ngan_sach = 50
print("Lợi nhuận tối đa:", toi_uu_san_xuat(chi_phi, loi_nhuan, ngan_sach))