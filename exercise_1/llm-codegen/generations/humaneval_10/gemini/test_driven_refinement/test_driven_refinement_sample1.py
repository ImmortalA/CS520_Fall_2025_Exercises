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
    longest_palindromic_suffix_start_index = len(string)

    for i in range(len(string)):
        suffix = string[i:]
        if is_palindrome(suffix):
            longest_palindromic_suffix_start_index = i
            break

    prefix_to_reverse = string[:longest_palindromic_suffix_start_index]
    reversed_prefix = prefix_to_reverse[::-1]
    
    return string + reversed_prefix