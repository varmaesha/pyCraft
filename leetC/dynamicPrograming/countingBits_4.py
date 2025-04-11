"""
base2-base10 values
2^x - 10^x
find number of 1s
repeating pattern

when we reach 2^x, some extra value which wasnt previously evaluated
o(n)
no of 1's = 1+dp[n-significant bit]
"""

def coutBits(n):
    dp = [0]* (n+1)# ist value
    offset = 1

    for i in range(1,n+1):
        if offset*2 == i:
            offset = i
        dp[i] = 1 + dp[i-offset]
    return dp

print(coutBits(5))#list with each number index has number of 1's
