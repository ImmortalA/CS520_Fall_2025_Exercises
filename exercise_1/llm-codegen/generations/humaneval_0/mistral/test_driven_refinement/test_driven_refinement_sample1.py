def has_close_elements(numbers: List[float], threshold: float) -> bool:
    if len(numbers) < 2:
        return False

    sorted_numbers = sorted(numbers)

    for i in range(len(sorted_numbers) - 1):
        if abs(sorted_numbers[i] - sorted_numbers[i + 1]) < threshold:
            return True

    return False