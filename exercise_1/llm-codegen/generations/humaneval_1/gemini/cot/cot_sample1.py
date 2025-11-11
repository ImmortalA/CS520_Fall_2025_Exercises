from typing import List


def separate_paren_groups(paren_string: str) -> List[str]:
    """ Input to this function is a string containing multiple groups of nested parentheses. Your goal is to
    separate those group into separate strings and return the list of those.
    Separate groups are balanced (each open brace is properly closed) and not nested within each other
    Ignore any spaces in the input string.
    >>> separate_paren_groups('( ) (( )) (( )( ))')
    ['()', '(())', '(()())']
    """
    cleaned_string = paren_string.replace(' ', '')
    
    result = []
    current_group_chars = [] 
    balance = 0
    
    for char in cleaned_string:
        current_group_chars.append(char)
        
        if char == '(':
            balance += 1
        elif char == ')':
            balance -= 1
            
        # If balance becomes 0, it means we have found a complete, top-level balanced group.
        if balance == 0:
            result.append("".join(current_group_chars))
            current_group_chars = [] # Reset for the next group
            
    return result