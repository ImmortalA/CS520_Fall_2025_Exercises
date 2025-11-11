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

    def _sum_digits_of_num(n):
        s_n = str(n)
        total_sum = 0
        if s_n[0] == '-':
            # For negative numbers, the first digit is considered negative.
            # e.g., for -123, s_n[1] is '1', so -int(s_n[1]) becomes -1.
            total_sum += -int(s_n[1])
            # The remaining digits are added as positive values.
            # e.g., for -123, s_n[2:] are '2', '3'.
            for digit_char in s_n[2:]:
                total_sum += int(digit_char)
        else:
            # For positive numbers and zero, all digits are added as positive values.
            for digit_char in s_n:
                total_sum += int(digit_char)
        return total_sum

    count = 0
    for num in arr:
        if _sum_digits_of_num(num) > 0:
            count += 1
    return count