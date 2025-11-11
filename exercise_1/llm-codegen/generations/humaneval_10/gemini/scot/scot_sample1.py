def is_palindrome(string: str) -> bool:
    """ Test if given string is a palindrome """
    return string == string[::-1]


def make_palindrome(string: str) -> str:
    """ Find the shortest palindrome that begins with a supplied string.
    Algorithm idea is simple:
    - Find the longest postfix of supplied string that is a palindrome.
    - Append to the end of the string reverse of a string prefix that comes before the palindromic suffix.
    >>> make_palindrome('')
    ''
    >>> make_palindrome('cat')
    'catac'
    >>> make_palindrome('cata')
    'catac'
    """
    n = len(string)

    # This variable will store the starting index of the longest palindromic postfix.
    # We are looking for string[i:] such that it's a palindrome and 'i' is minimized.
    start_index_of_pal_postfix = 0 

    # Iterate through all possible starting positions for a postfix.
    # i = 0 corresponds to the entire string (string[0:]).
    # i = n-1 corresponds to the last character (string[n-1:]).
    # i = n corresponds to the empty string (string[n:]).
    # The loop finds the first (smallest) 'i' for which string[i:] is a palindrome.
    # This ensures that string[i:] is the LONGEST palindromic postfix.
    for i in range(n + 1):
        postfix = string[i:]
        if is_palindrome(postfix):
            start_index_of_pal_postfix = i
            break # Found the longest palindromic postfix, no need to check shorter ones.

    # The prefix to reverse is the part of the original string
    # that comes *before* the longest palindromic postfix.
    # If string[start_index_of_pal_postfix:] is the palindromic postfix,
    # then string[:start_index_of_pal_postfix] is the prefix to reverse.
    prefix_to_reverse = string[:start_index_of_pal_postfix]
    
    # Construct the shortest palindrome: original string + reversed prefix.
    return string + prefix_to_reverse[::-1]