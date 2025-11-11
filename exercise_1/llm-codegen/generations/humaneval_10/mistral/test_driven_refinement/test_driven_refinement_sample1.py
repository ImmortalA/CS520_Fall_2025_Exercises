def make_palindrome(string: str) -> str:
    if not string:
        return string

    n = len(string)
    for i in range(n):
        substring = string[i:]
        if substring == substring[::-1]:
            return string + string[:i][::-1]

    return string + string[:-1][::-1]