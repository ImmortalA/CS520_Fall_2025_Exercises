def count_nums(arr):
    """
    Write a function count_nums which takes an array of integers and returns
    the number of elements which has a sum of digits > 0.
    If a number is negative, then its first signed digit will be negative:
    e.g. -123 has signed digits -1, 2, and 3.
    >>> count_nums([]) == 0
    >>> count_nums([-1, 11, -11]) == 1
    >>> count_nums([1, 1, 2]) == 3
    """
    count = 0
    for num in arr:
        s = str(num)
        current_sum = 0
        
        if num < 0:
            # The first digit is negative
            current_sum += -int(s[1])
            # Subsequent digits are positive
            for char_digit in s[2:]:
                current_sum += int(char_digit)
        else: # num >= 0
            # All digits are positive (or 0 for the number 0 itself)
            for char_digit in s:
                current_sum += int(char_digit)
        
        if current_sum > 0:
            count += 1
            
    return count