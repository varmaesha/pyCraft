"""
i price i
max profit on ith day

greedy alog, maming best choces at given time
actual largets path
"""

def macPro(prices):
    l , r = 0,1
    maxPro = 0

    while r < len(prices):
        if prices[l] < prices[r]:
            maxPro = max(maxPro, prices[r] - prices[l])
        else:
            l = r
        r += 1
    return maxPro

prices = [7,1,5,3,6,4]

