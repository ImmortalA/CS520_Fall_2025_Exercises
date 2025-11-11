from typing import List


def has_close_elements(numbers: List[float], threshold: float) -> bool:
    """ Check if in given list of numbers, are any two numbers closer to each other than
    given threshold.
    >>> has_close_elements([1.0, 2.0, 3.0], 0.5)
    False
    >>> has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3)
    True
    """
    n = len(numbers)
    if n < 2:
        return False

    # Sort the list to bring potentially close elements next to each other.
    # If two numbers 'a' and 'b' are closer than 'threshold', and no number 'c'
    # lies between them such that 'abs(a-c)' or 'abs(b-c)' is even smaller,
    # then after sorting, 'a' and 'b' (or numbers even closer to them) will be adjacent.
    # The crucial insight is that if there's any pair (x, y) with |x-y| < threshold,
    # then in the sorted list, there must be an adjacent pair (s_i, s_{i+1})
    # such that |s_{i+1} - s_i| < threshold.
    # This is because if for all adjacent pairs, |s_{i+1} - s_i| >= threshold,
    # then for any non-adjacent pair (s_j, s_k) with j < k,
    # |s_k - s_j| = (s_k - s_{k-1}) + ... + (s_{j+1} - s_j) >= (k-j) * threshold >= threshold.
    sorted_numbers = sorted(numbers)

    # Iterate through adjacent elements and check their difference
    for i in range(n - 1):
        # Since the list is sorted, numbers[i+1] will always be >= numbers[i]
        # so abs(numbers[i+1] - numbers[i]) is simply numbers[i+1] - numbers[i].
        if sorted_numbers[i+1] - sorted_numbers[i] < threshold:
            return True

    return False