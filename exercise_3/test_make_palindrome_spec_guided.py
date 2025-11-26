#!/usr/bin/env python3
"""
Spec-guided tests for make_palindrome function based on formal specifications.
Generated for Exercise 3 Part 2.
"""

import sys
import os
sys.path.append('../exercise_2/results')
from make_palindrome_solution import make_palindrome

def test_make_palindrome_spec_guided():
    """Test cases generated from formal specifications."""
    
    # Test cases targeting specification properties
    test_cases = [
        ("", ""),
        ("a", "a"),
        ("aa", "aa"),
        ("aba", "aba"),
        ("abba", "abba"),
        ("ab", "aba"),
        ("abc", "abcba"),
        ("abcd", "abcdcba"),
        ("cat", "catac"),
        ("race", "racecar"),
        ("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"),
        ("abababababababababababababababababababababababababababababababababababababababababababababababababab", "ababababababababababababababababababababababababababababababababababababababababababababababababababa"),
        ("abcdefg", "abcdefgfedcba"),
        ("palindrome", "palindromemordnilap"),
        ("raceca", "racecar"),
    ]
    
    for string, expected in test_cases:
        result = make_palindrome(string)
        assert result == expected, f"make_palindrome('{string}') = '{result}', expected '{expected}'"
        print(f"PASS make_palindrome('{string}') = '{result}'")

if __name__ == "__main__":
    test_make_palindrome_spec_guided()
    print("All make_palindrome spec-guided tests passed!")
