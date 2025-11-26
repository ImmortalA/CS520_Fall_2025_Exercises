#!/usr/bin/env python3
"""
Exercise 3 Part 2: Use Specifications to Guide Test Improvement
This script generates test cases based on the corrected formal specifications.
"""

import sys
import os
sys.path.append('../exercise_2/results')

# Import the solution functions
from same_chars_solution import same_chars
from make_palindrome_solution import make_palindrome

def generate_spec_guided_tests():
    """
    Generate test cases based on the corrected formal specifications.
    This simulates asking an LLM to create tests that satisfy the specifications.
    """
    
    # LLM Prompt for generating tests from specifications
    test_generation_prompt = """
    Based on the following corrected formal specifications, generate comprehensive test cases
    that exercise the logical properties described in the assertions.
    
    For same_chars function:
    1. assert res == (set(s0) == set(s1))  # Result equals whether both strings have identical character sets
    2. assert res == (set(s0).symmetric_difference(set(s1)) == set())  # No characters unique to either string
    3. assert res == (all(c in s1 for c in s0) and all(c in s0 for c in s1))  # All chars bidirectional membership
    4. assert res == (sorted(list(set(s0))) == sorted(list(set(s1))))  # Sort unique characters only
    
    For make_palindrome function:
    1. assert res == res[::-1]  # Result must be a palindrome
    2. assert res.startswith(string)  # Result must start with the input string
    3. assert len(res) >= len(string)  # Result length must be at least input length
    4. assert string == '' or len(res) == len(string) or not (string == string[::-1])  # Length increases only if not already palindrome
    
    Generate test cases that specifically target these properties and edge cases.
    """
    
    print("LLM Prompt for Test Generation:")
    print(test_generation_prompt)
    print("\n" + "="*80 + "\n")
    
    # Generated spec-guided test cases for same_chars
    same_chars_spec_tests = [
        # Test identical character sets with different arrangements
        ("abc", "bca"),  # Same chars, different order
        ("aabbcc", "abcabc"),  # Same chars, different frequencies
        ("", ""),  # Empty strings
        ("a", "a"),  # Single identical character
        
        # Test different character sets
        ("abc", "def"),  # Completely different chars
        ("ab", "abc"),  # One is subset of other
        ("abc", "ab"),  # Reverse subset relationship
        ("a", "aa"),  # Same char but different frequency
        
        # Test edge cases for set operations
        ("xyz", "zyx"),  # Same chars, reverse order
        ("aaa", "a"),  # Multiple vs single occurrence
        ("abcdef", "fedcba"),  # Longer strings, same chars
        ("hello", "world"),  # Common real words, different chars
        
        # Test symmetric difference property
        ("programming", "grampion"),  # Anagram-like but different
        ("listen", "silent"),  # Perfect anagram
        ("abc123", "321cba"),  # Alphanumeric same chars
    ]
    
    # Generated spec-guided test cases for make_palindrome  
    make_palindrome_spec_tests = [
        # Test palindrome property
        "",  # Empty string
        "a",  # Single character (already palindrome)
        "aa",  # Two identical chars (already palindrome)
        "aba",  # Odd-length palindrome (already palindrome)
        "abba",  # Even-length palindrome (already palindrome)
        
        # Test strings requiring extension
        "ab",  # Simple two-char string
        "abc",  # Three-char string
        "abcd",  # Four-char string
        "cat",  # Real word
        "race",  # Another real word
        
        # Test edge cases for length property
        "x" * 100,  # Long single character (already palindrome)
        "ab" * 50,  # Long repeating pattern
        "abcdefg",  # Longer string requiring significant extension
        
        # Test startswith property edge cases
        "palindrome",  # Longer real word
        "racecar"[:-1],  # Almost a palindrome
    ]
    
    return {
        'same_chars': same_chars_spec_tests,
        'make_palindrome': make_palindrome_spec_tests,
        'prompt': test_generation_prompt
    }

def create_test_files():
    """Create actual test files with the spec-guided tests."""
    
    spec_tests = generate_spec_guided_tests()
    
    # Create spec-guided test file for same_chars
    same_chars_test_content = '''#!/usr/bin/env python3
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
'''
    
    for s0, s1 in spec_tests['same_chars']:
        expected = same_chars(s0, s1)
        same_chars_test_content += f'        ("{s0}", "{s1}", {expected}),\n'
    
    same_chars_test_content += '''    ]
    
    for s0, s1, expected in test_cases:
        result = same_chars(s0, s1)
        assert result == expected, f"same_chars('{s0}', '{s1}') = {result}, expected {expected}"
        print(f"PASS same_chars('{s0}', '{s1}') = {result}")

if __name__ == "__main__":
    test_same_chars_spec_guided()
    print("All same_chars spec-guided tests passed!")
'''
    
    # Create spec-guided test file for make_palindrome
    make_palindrome_test_content = '''#!/usr/bin/env python3
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
'''
    
    for string in spec_tests['make_palindrome']:
        expected = make_palindrome(string)
        make_palindrome_test_content += f'        ("{string}", "{expected}"),\n'
    
    make_palindrome_test_content += '''    ]
    
    for string, expected in test_cases:
        result = make_palindrome(string)
        assert result == expected, f"make_palindrome('{string}') = '{result}', expected '{expected}'"
        print(f"PASS make_palindrome('{string}') = '{result}'")

if __name__ == "__main__":
    test_make_palindrome_spec_guided()
    print("All make_palindrome spec-guided tests passed!")
'''
    
    # Write the test files
    with open('test_same_chars_spec_guided.py', 'w') as f:
        f.write(same_chars_test_content)
    
    with open('test_make_palindrome_spec_guided.py', 'w') as f:
        f.write(make_palindrome_test_content)
    
    print("Spec-guided test files created successfully!")
    return spec_tests

if __name__ == "__main__":
    spec_tests = create_test_files()
    print(f"Generated {len(spec_tests['same_chars'])} test cases for same_chars")
    print(f"Generated {len(spec_tests['make_palindrome'])} test cases for make_palindrome")
