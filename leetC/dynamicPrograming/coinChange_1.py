"""
array of coins

amount to reach using min coins

dynamic programing, store subproblem
"""

def coinChange(coins,amt):

    pd = [amt+1] * (amt+1)
    pd[0] = 0

    for i in range(1,amt+1):

        for c in coins:

            if(i-c) >= 0:#not to fall below the index being evaluated
                pd[i] = min(pd[i],1+pd[i-c])
    return pd[amt] if (pd[amt] != amt+1) else -1

print(coinChange([1,2,5],11))
