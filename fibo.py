def fibo_index(ind:int):
  

    if ind == 1:
        return 0
    if ind == 2:
        return 1

    return fibo_index(ind - 1) + fibo_index(ind - 2)


print(fibo_index(5))
