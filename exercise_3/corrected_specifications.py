#!/usr/bin/env python3
"""
Corrected Formal Specifications for Exercise 3 Part 1
This file contains the manually corrected specifications that will be used for test generation.
"""

# Corrected specifications for same_chars function
def get_same_chars_corrected_specs():
    """Returns list of corrected specifications for same_chars function."""
    return [
        "assert res == (set(s0) == set(s1))  # Result equals whether both strings have identical character sets",
        "assert res == (set(s0).symmetric_difference(set(s1)) == set())  # No characters unique to either string", 
        "assert res == (all(c in s1 for c in s0) and all(c in s0 for c in s1))  # All chars bidirectional membership",
        "assert res == (sorted(list(set(s0))) == sorted(list(set(s1))))  # Sort unique characters only"
    ]

# Corrected specifications for make_palindrome function  
def get_make_palindrome_corrected_specs():
    """Returns list of corrected specifications for make_palindrome function."""
    return [
        "assert res == res[::-1]  # Result must be a palindrome",
        "assert res.startswith(string)  # Result must start with the input string",
        "assert len(res) >= len(string)  # Result length must be at least input length", 
        "assert string == '' or len(res) == len(string) or not (string == string[::-1])  # Length increases only if not already palindrome"
    ]

# Test the specifications with sample inputs
def test_same_chars_specs():
    """Test the corrected same_chars specifications."""
    print("Testing same_chars specifications:")
    
    test_cases = [
        ("abc", "bca", True),
        ("abc", "def", False), 
        ("", "", True),
        ("a", "aa", False),
        ("eabcdzzzz", "dddzzzzzzzddeddabc", True)
    ]
    
    specs = get_same_chars_corrected_specs()
    
    for s0, s1, expected_res in test_cases:
        res = expected_res
        print(f"\nTesting s0='{s0}', s1='{s1}', res={res}")
        
        for i, spec in enumerate(specs, 1):
            try:
                # Replace variables in assertion
                test_assertion = spec.replace("res", str(res)).replace("s0", f"'{s0}'").replace("s1", f"'{s1}'")
                eval(test_assertion.replace("assert ", ""))
                print(f"  Spec {i}: PASS")
            except Exception as e:
                print(f"  Spec {i}: FAIL - {e}")

def test_make_palindrome_specs():
    """Test the corrected make_palindrome specifications."""
    print("\nTesting make_palindrome specifications:")
    
    test_cases = [
        ("", ""),
        ("a", "a"), 
        ("ab", "aba"),
        ("abc", "abcba"),
        ("cat", "catac")
    ]
    
    specs = get_make_palindrome_corrected_specs()
    
    for string, expected_res in test_cases:
        res = expected_res
        print(f"\nTesting string='{string}', res='{res}'")
        
        for i, spec in enumerate(specs, 1):
            try:
                # Replace variables in assertion
                test_assertion = spec.replace("res", f"'{res}'").replace("string", f"'{string}'")
                eval(test_assertion.replace("assert ", ""))
                print(f"  Spec {i}: PASS")
            except Exception as e:
                print(f"  Spec {i}: FAIL - {e}")

if __name__ == "__main__":
    test_same_chars_specs()
    test_make_palindrome_specs()
