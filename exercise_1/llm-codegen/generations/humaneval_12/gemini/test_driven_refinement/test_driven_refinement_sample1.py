from typing import List, Optional


def longest(strings: List[str]) -> Optional[str]:
    """ Out of list of strings, return the longest one. Return the first one in case of multiple
    strings of the same length. Return None in case the input list is empty.
    >>> longest([])

    >>> longest(['a', 'b', 'c'])
    'a'
    >>> longest(['a', 'bb', 'ccc'])
    'ccc'
    """
    # Edge Case 1: Handle an empty input list.
    # If the list is empty, there are no strings to compare, so return None.
    if not strings:
        return None

    # Initialize longest_string to store the current longest string found.
    # Initialize max_length to a value smaller than any possible string length (e.g., -1).
    # This ensures that the first string in the list will always become the initial longest_string.
    longest_string = None
    max_length = -1

    # Iterate through each string in the input list.
    for current_string in strings:
        current_length = len(current_string)

        # Compare the current string's length with the maximum length found so far.
        # Edge Case 2: "Return the first one in case of multiple strings of the same length."
        # This is handled by using a strictly greater comparison ('>').
        # If current_length is *equal* to max_length, we do not update longest_string,
        # thereby preserving the string that was encountered earlier.
        if current_length > max_length:
            max_length = current_length
            longest_string = current_string

    # After iterating through all strings, longest_string will hold the longest string
    # (or the first among equally longest ones).
    # This correctly handles cases with a single string, strings of varying lengths,
    # and lists containing empty strings.
    return longest_string