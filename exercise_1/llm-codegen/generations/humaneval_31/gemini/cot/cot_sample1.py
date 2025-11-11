def is_prime(n):
    """Return true if a given number is prime, and false otherwise.
    >>> is_prime(6)
    False
    >>> is_prime(101)
    True
    >>> is_prime(11)
    True
    >>> is_prime(13441)
    True
    >>> is_prime(61)
    True
    >>> is_prime(4)
    False
    >>> is_prime(1)
    False
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:  # All other even numbers are not prime
        return False
    
    # Check for odd divisors from 3 up to the square root of n
    # We use int(n**0.5) for the square root to avoid importing math
    limit = int(n**0.5)
    for i in range(3, limit + 1, 2):
        if n % i == 0:
            return False
            
    return True