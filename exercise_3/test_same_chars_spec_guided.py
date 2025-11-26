#!/usr/bin/env python3
"""
Spec-guided tests for same_chars function based on formal specifications.
Generated for Exercise 3 Part 2.
"""

import sys
import os
sys.path.append('../exercise_2/results')
from same_chars_solution import same_chars

def test_same_chars_spec_guided():
    """Test cases generated from formal specifications."""
    
    # Test cases targeting specification properties
    test_cases = [
        ("abc", "bca", True),
        ("aabbcc", "abcabc", True),
        ("", "", True),
        ("a", "a", True),
        ("abc", "def", False),
        ("ab", "abc", False),
        ("abc", "ab", False),
        ("a", "aa", True),
        ("xyz", "zyx", True),
        ("aaa", "a", True),
        ("abcdef", "fedcba", True),
        ("hello", "world", False),
        ("programming", "grampion", True),
        ("listen", "silent", True),
        ("abc123", "321cba", True),
    ]
    
    for s0, s1, expected in test_cases:
        result = same_chars(s0, s1)
        assert result == expected, f"same_chars('{s0}', '{s1}') = {result}, expected {expected}"
        print(f"PASS same_chars('{s0}', '{s1}') = {result}")

if __name__ == "__main__":
    test_same_chars_spec_guided()
    print("All same_chars spec-guided tests passed!")
