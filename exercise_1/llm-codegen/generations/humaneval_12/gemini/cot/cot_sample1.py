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
    
    # The built-in max function, when given a key, will return the
    # first item encountered that has the maximum value according to the key.
    # This satisfies the requirement to return the first one in case of ties.
    return max(strings, key=len)