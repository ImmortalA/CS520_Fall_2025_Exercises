from typing import List


def factorize(n: int) -> List[int]:
    if n == 1:
        return []

    factors = []

    # Handle factor 2
    while n % 2 == 0:
        factors.append(2)
        n //= 2

    # Handle odd factors starting from 3
    divisor = 3
    # We only need to check divisors up to the square root of n.
    # If n is not 1 after this loop, the remaining n is a prime factor itself.
    while divisor * divisor <= n:
        while n % divisor == 0:
            factors.append(divisor)
            n //= divisor
        divisor += 2  # Increment by 2 to check only odd numbers

    # If n is still greater than 1 after checking up to sqrt(n),
    # it means the remaining n is a prime factor itself.
    # This covers cases where the original n was a prime number,
    # or the largest prime factor is greater than its square root.
    if n > 1:
        factors.append(n)

    return factors