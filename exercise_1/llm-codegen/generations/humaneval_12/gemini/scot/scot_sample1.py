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
    if not strings:
        return None

    longest_so_far = strings[0]
    max_len_so_far = len(strings[0])

    # Iterate from the second element, as the first is already our initial candidate.
    # The comparison len(s) > max_len_so_far correctly handles the "first one in case of ties" rule.
    for s in strings[1:]:
        current_len = len(s)
        if current_len > max_len_so_far:
            max_len_so_far = current_len
            longest_so_far = s
            
    return longest_so_far