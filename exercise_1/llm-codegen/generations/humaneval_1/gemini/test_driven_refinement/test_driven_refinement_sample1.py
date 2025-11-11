def separate_paren_groups(paren_string: str) -> List[str]:
    """ Input to this function is a string containing multiple groups of nested parentheses. Your goal is to
    separate those group into separate strings and return the list of those.
    Separate groups are balanced (each open brace is properly closed) and not nested within each other
    Ignore any spaces in the input string.
    >>> separate_paren_groups('( ) (( )) (( )( ))')
    ['()', '(())', '(()())']
    """
    # 1. Clean the input string by removing all spaces.
    # Edge case: Empty string or string with only spaces will result in an empty cleaned_string.
    cleaned_string = paren_string.replace(' ', '')

    # Initialize an empty list to store the separated groups.
    result = []
    
    # Initialize a balance counter. This counter tracks the nesting level.
    # A balance of 0 at the start/end of a segment indicates a top-level, balanced group.
    balance = 0
    
    # Initialize the starting index for the current potential group.
    # This marks where the current top-level group begins in the cleaned_string.
    current_group_start_index = 0

    # Iterate through the cleaned string character by character.
    for i, char in enumerate(cleaned_string):
        if char == '(':
            balance += 1
        elif char == ')':
            balance -= 1
        
        # When balance returns to 0, it signifies the end of a complete,
        # top-level, and balanced parenthesis group.
        # Edge case: If cleaned_string is empty, this loop won't run, and result remains [].
        # Edge case: For "()", balance becomes 0 at i=1, capturing "()".
        # Edge case: For "(())", balance becomes 0 at i=3, capturing "(())".
        # Edge case: For "()()", balance becomes 0 at i=1 for first "()", then again at i=3 for second "()".
        if balance == 0:
            # Extract the substring for this complete group.
            # The slice goes from current_group_start_index up to and including the current character (i).
            group = cleaned_string[current_group_start_index : i + 1]
            result.append(group)
            
            # Reset the starting index for the next potential group.
            # The next group will start immediately after the current one ends.
            current_group_start_index = i + 1
            
    return result