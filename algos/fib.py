# Fibonacci sequence implementations

# Recursion
def fib(n):
    """
    Calculate the nth Fibonacci number using recursion.
    
    Args:
        n (int): The position in the Fibonacci sequence (0-indexed).
        
    Returns:
        int: The nth Fibonacci number.
        
    Note:
        This implementation has exponential time complexity O(2^n) 
        and is not efficient for large values of n.
    """
    if n == 0: 
        return 0
    if n == 1: 
        return 1
    return fib(n - 1) + fib(n - 2)

print(fib(3))

# Iterative
def fib2(n): 
    """
    Calculate the nth Fibonacci number using an iterative approach.
    
    Args:
        n (int): The position in the Fibonacci sequence (0-indexed).
        
    Returns:
        int: The nth Fibonacci number.
        
    Note:
        This implementation has linear time complexity O(n) 
        and constant space complexity O(1).
    """
    a, b = 0, 1
    for i in range(n):
        temp = a
        a = b
        b = temp + b
        # a, b = b, a + b # This is an alternative, more concise way in Python.
    return a

print(fib2(3))

# Memoization with recursion
def fib3(n, memo={}): 
    """
    Calculate the nth Fibonacci number using recursion with memoization.
    
    Args:
        n (int): The position in the Fibonacci sequence (0-indexed).
        memo (dict): A dictionary to store previously computed Fibonacci numbers.
        
    Returns:
        int: The nth Fibonacci number.
        
    Note:
        This implementation has linear time complexity O(n) 
        and space complexity O(n) due to the memo dictionary.
    """
    if n in memo: 
        return memo[n]
    if n == 0: 
        return 0
    if n == 1: 
        return 1
    memo[n] = fib3(n - 1, memo) + fib3(n - 2, memo)
    return memo[n]

print(fib3(3))

# Bottom-up dynamic programming
def fib(n):
    """
    Calculate the nth Fibonacci number using bottom-up dynamic programming.
    
    Args:
        n (int): The position in the Fibonacci sequence (0-indexed).
        
    Returns:
        int: The nth Fibonacci number.
        
    Note:
        This implementation has linear time complexity O(n) 
        and space complexity O(n) due to the dp array.
    """
    if n == 0:
        return 0
    dp = [0, 1] + [0] * (n - 1)
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]

print(fib(3))