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
        digit_sum = 0
        
        # Convert the number to a string to easily access digits
        s_num = str(num)
        
        if num < 0:
            # For negative numbers, the first digit is negative
            # and subsequent digits are positive.
            # int(s_num[0]) will correctly give the negative first digit (e.g., -1 for "-123")
            digit_sum += int(s_num[0])
            
            # Add the absolute values of the remaining digits
            for i in range(1, len(s_num)):
                digit_sum += int(s_num[i])
        else:
            # For non-negative numbers (including 0), all digits are positive.
            for digit_char in s_num:
                digit_sum += int(digit_char)
        
        if digit_sum > 0:
            count += 1
            
    return count