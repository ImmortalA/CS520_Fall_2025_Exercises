def correct_bracketing(brackets: str):
    balance = 0
    for char in brackets:
        if char == '(':
            balance += 1
        elif char == ')':
            balance -= 1
        
        # If balance ever drops below zero, it means a closing bracket appeared without a corresponding open one.
        if balance < 0:
            return False
            
    # After iterating through all characters, balance must be zero for correct bracketing.
    # If balance is positive, it means there are unclosed opening brackets.
    return balance == 0