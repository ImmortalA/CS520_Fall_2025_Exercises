from typing import List

def has_close_elements(numbers: List[float], threshold: float) -> bool:
    n = len(numbers)
    if n < 2:
        return False

    sorted_numbers = sorted(numbers)

    for i in range(n - 1):
        if sorted_numbers[i+1] - sorted_numbers[i] < threshold:
            return True

    return False