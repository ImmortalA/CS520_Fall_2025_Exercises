def factorize(n: int) -> List[int]:
    if not isinstance(n, int) or n <= 0:
        raise ValueError("Input must be a positive integer")

    if n == 1:
        return []

    factors = []
    current = n

    # Handle 2 separately to skip even numbers later
    while current % 2 == 0:
        factors.append(2)
        current = current // 2

    # Check odd divisors up to sqrt(current)
    i = 3
    max_factor = int(current**0.5) + 1
    while i <= max_factor:
        while current % i == 0:
            factors.append(i)
            current = current // i
            max_factor = int(current**0.5) + 1
        i += 2

    if current > 1:
        factors.append(current)

    return factors