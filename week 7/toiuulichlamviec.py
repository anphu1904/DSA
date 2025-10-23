from bisect import bisect_right

def max_profit(jobs):
    jobs.sort(key=lambda x: x[1])
    n = len(jobs)
    dp = [0] * n
    dp[0] = jobs[0][2]

    for i in range(1, n):
        l = bisect_right([j[1] for j in jobs], jobs[i][0]) - 1
        include = jobs[i][2] + (dp[l] if l >= 0 else 0)
        dp[i] = max(dp[i-1], include)

    return dp[-1]

jobs = [
    (1, 3, 50),
    (3, 5, 20),
    (6, 19, 100),
    (2, 100, 200)
]
print("Lợi nhuận tối đa:", max_profit(jobs))
