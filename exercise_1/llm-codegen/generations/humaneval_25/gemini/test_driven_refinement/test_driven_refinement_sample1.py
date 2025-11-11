def factorize(n: int) -> List[int]:
    """ Return list of prime factors of given integer in the order from smallest to largest.
    Each of the factors should be listed number of times corresponding to how many times it appeares in factorization.
    Input number should be equal to the product of all factors
    >>> factorize(8)
    [2, 2, 2]
    >>> factorize(25)
    [5, 5]
    >>> factorize(70)
    [2, 5, 7]
    """
    factors = []

    # Edge case: n = 1 has no prime factors.
    # The product of an empty list is 1, which is consistent.
    if n == 1:
        return []

    # Handle factor 2:
    # Continuously divide by 2 until n is odd
    while n % 2 == 0:
        factors.append(2)
        n //= 2

    # Handle odd factors:
    # Iterate through odd numbers starting from 3 up to sqrt(n)
    # We only need to check up to sqrt(n) because if n has a prime factor larger than sqrt(n),
    # it must also have a prime factor smaller than sqrt(n) (which would have already been found),
    # or n itself is a prime.
    d = 3
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 2 # Move to the next odd number

    # If after all divisions, n is still greater than 1,
    # it means the remaining n is a prime number itself.
    # This covers cases where the original n was a prime number,
    # or where the largest prime factor is greater than sqrt(original_n).
    if n > 1:
        factors.append(n)

    return factors