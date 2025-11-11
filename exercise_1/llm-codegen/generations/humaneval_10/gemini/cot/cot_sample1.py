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
    def is_palindrome(s: str) -> bool:
        return s == s[::-1]

    if not string:
        return ""

    # Find the longest palindromic postfix
    # We iterate from the beginning of the string, checking postfixes.
    # The first palindromic postfix we find will be the longest,
    # because `string[i:]` gets shorter as `i` increases.
    longest_palindromic_postfix_start_index = 0
    for i in range(len(string)):
        current_postfix = string[i:]
        if is_palindrome(current_postfix):
            longest_palindromic_postfix_start_index = i
            break # Found the longest one

    # The prefix that comes before the longest palindromic suffix
    prefix_to_reverse = string[:longest_palindromic_postfix_start_index]

    # Reverse this prefix
    reversed_prefix = prefix_to_reverse[::-1]

    # Append the reversed prefix to the original string to form the shortest palindrome
    return string + reversed_prefix