from typing import List

def factorize(n: int) -> List[int]:
    factors = []
    
    if n == 1:
        return []
    
    # Handle factor 2
    while n % 2 == 0:
        factors.append(2)
        n //= 2
        
    # Handle odd factors
    # We start from 3 and increment by 2 (3, 5, 7, ...)
    # We only need to check up to sqrt(n) because if n has a prime factor
    # greater than sqrt(n), it must also have a prime factor smaller than sqrt(n).
    # If after dividing by all factors up to sqrt(n), n is still > 1, then
    # the remaining n must be prime.
    d = 3
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 2 # Move to next odd number
        
    # If n is still greater than 1, it means the remaining n is a prime factor itself
    # (this happens when the original n was prime, or the largest prime factor
    # is greater than sqrt(original_n))
    if n > 1:
        factors.append(n)
        
    return factors