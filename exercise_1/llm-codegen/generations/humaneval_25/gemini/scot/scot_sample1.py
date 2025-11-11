from typing import List


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

    # Handle the case for n = 1
    if n == 1:
        return []

    # Handle factor 2
    while n % 2 == 0:
        factors.append(2)
        n //= 2

    # Handle odd factors
    # We only need to check up to sqrt(n) because if n has a prime factor greater than sqrt(n),
    # it must also have a prime factor smaller than sqrt(n).
    # The remaining n, if > 1, will be a prime factor itself.
    d = 3
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 2  # Increment by 2 to check only odd numbers

    # If n is still greater than 1, it means the remaining n is a prime factor
    # (this covers cases where the original n was prime, or had a large prime factor)
    if n > 1:
        factors.append(n)

    return factors