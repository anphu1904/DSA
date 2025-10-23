def doi_tien(cac_menh_gia, so_tien):
    n = len(cac_menh_gia)
    dp = [0] * (so_tien + 1)
    dp[0] = 1

    for coin in cac_menh_gia:
        for i in range(coin, so_tien + 1):
            dp[i] += dp[i - coin]

    return dp[so_tien]
menh_gia = [1, 2, 5]
so_tien = 5
print("Số cách đổi tiền:", doi_tien(menh_gia, so_tien))