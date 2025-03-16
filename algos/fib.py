#recursion
def fib(n):
    if n == 0: 
        return 0
    if n == 1: 
        return 1
    return fib (n-1 ) + fib(n-2)
print (fib(3))

#iterative
def fib2(n): 
    a,b = 0,1
    for i in range(n):
        temp = a
        a = b
        b = temp + b
        #a,b=b,a+b #is also acceptable in python
    return a
print (fib2(3))

#memoization with recursion
def fib3(n, memo={}): 
    if n in memo: 
        return memo[n]
    if n == 0: 
        return 0
    if n == 1: 
        return 1
    memo[n] = fib3(n-1, memo) + fib3(n-2, memo)
    return memo[n]
    
print (fib3(3))

#bottom up dp 
def fib(n):
    if n == 0:
        return 0
    dp = [0, 1] + [0] * (n - 1)
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]

print(fib(3)) 