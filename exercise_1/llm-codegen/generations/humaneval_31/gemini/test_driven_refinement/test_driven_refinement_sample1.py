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
    # Numbers less than 2 are not prime (0, 1, negative numbers)
    if n <= 1:
        return False

    # 2 is the only even prime number
    if n == 2:
        return True

    # All other even numbers greater than 2 are not prime
    if n % 2 == 0:
        return False

    # Check for odd divisors from 3 up to the square root of n
    # We only need to check odd numbers as potential divisors
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2 # Increment by 2 to check only odd numbers

    # If no divisors were found, the number is prime
    return True