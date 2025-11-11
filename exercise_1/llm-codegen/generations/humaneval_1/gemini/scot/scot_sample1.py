from typing import List


def separate_paren_groups(paren_string: str) -> List[str]:
    """ Input to this function is a string containing multiple groups of nested parentheses. Your goal is to
    separate those group into separate strings and return the list of those.
    Separate groups are balanced (each open brace is properly closed) and not nested within each other
    Ignore any spaces in the input string.
    >>> separate_paren_groups('( ) (( )) (( )( ))')
    ['()', '(())', '(()())']
    """
    result = []
    current_group = []  # To build the current group, using a list for efficient character appending
    balance = 0         # Tracks the nesting level of parentheses

    for char in paren_string:
        if char == ' ':
            continue  # Ignore spaces

        current_group.append(char)

        if char == '(':
            balance += 1
        elif char == ')':
            balance -= 1

        # If balance returns to 0, it means a complete, balanced group has been found.
        # Since we only append '(' or ')' to current_group (non-space characters),
        # current_group will not be empty when balance is 0, unless the input was empty or only spaces.
        # For non-empty balanced groups, current_group will contain the characters of that group.
        if balance == 0:
            result.append("".join(current_group))
            current_group = []  # Reset for the next group

    return result