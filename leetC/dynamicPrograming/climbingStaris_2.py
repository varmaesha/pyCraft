"""
ns tepse to reach top
1 or 2 steps at time
how may distinct ways you can reach top
"""

def stps(n):
    dp = [0] *(n+1)
    dp[0] = 0
    dp[1] = 1
    dp[2] = 2

    for i in range(3,n+1):
        dp[i] = dp[i-1] + dp[i-2]

    return dp[n]

print(stps(4))

