def count_nums(arr):
    count = 0
    for num in arr:
        if num == 0:
            continue
        num_str = str(num)
        sum_digits = 0
        for ch in num_str:
            if ch == '-':
                continue
            sum_digits += int(ch)
        if sum_digits > 0:
            count += 1
    return count