def correct_bracketing(brackets: str):
    balance = 0
    for char in brackets:
        if char == '(':
            balance += 1
        elif char == ')':
            balance -= 1
        # If balance ever drops below zero, it means we have a closing bracket
        # without a corresponding opening bracket before it.
        if balance < 0:
            return False
    
    # After iterating through all characters, if balance is 0,
    # all opening brackets have been closed.
    return balance == 0