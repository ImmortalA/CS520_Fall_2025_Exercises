"""
Exercise 3 - Part 2: Use Specifications to Guide Test Improvement
This file contains the spec-guided test cases generated from the corrected specifications.
"""

import sys
from pathlib import Path
import importlib.util

# Load the solution functions
sys.path.insert(0, str(Path("../exercise_2/results")))

# Load same_chars solution
spec_sol = importlib.util.spec_from_file_location("same_chars_module", "../exercise_2/results/same_chars_solution.py")
same_chars_module = importlib.util.module_from_spec(spec_sol)
spec_sol.loader.exec_module(same_chars_module)
same_chars = getattr(same_chars_module, "same_chars")

# Load make_palindrome solution  
spec_pal = importlib.util.spec_from_file_location("make_palindrome_module", "../exercise_2/results/make_palindrome_solution.py")
make_palindrome_module = importlib.util.module_from_spec(spec_pal)
spec_pal.loader.exec_module(make_palindrome_module)
make_palindrome = getattr(make_palindrome_module, "make_palindrome")

print("="*80)
print("SPEC-GUIDED TEST GENERATION")
print("="*80)

print("\nLLM Prompt for Test Generation:")
test_generation_prompt = """
Based on the following corrected formal specifications, generate comprehensive test cases that validate each specification:

For same_chars(s0: str, s1: str) -> bool:
1. assert res == (set(s0) == set(s1))  # Result equals whether both strings have same unique characters
2. assert (s0 == '' and s1 == '') == (res and len(set(s0)) == 0 and len(set(s1)) == 0)  # Both empty strings return True
3. assert (len(set(s0)) == 1 and len(set(s1)) == 1 and set(s0) == set(s1)) == (res and len(set(s0 + s1)) == 1)  # Single same character case
4. assert (len(set(s0)) > 0 and len(set(s1)) > 0 and set(s0).isdisjoint(set(s1))) == (not res)  # Disjoint non-empty sets return False
5. assert (set(s0).issubset(set(s1)) and set(s1).issubset(set(s0))) == res  # Mutual subset relationship equals result

For make_palindrome(string: str) -> str:
1. assert res.startswith(string)  # Result must start with the input string
2. assert res == res[::-1]  # Result must be a palindrome
3. assert len(res) >= len(string)  # Result length must be at least input length
4. assert string == '' or len(res) <= 2 * len(string)  # Result length bounded by twice input length
5. assert (string == '') == (res == '')  # Empty input produces empty result

Generate test cases that specifically target each specification and cover edge cases.
"""
print(test_generation_prompt)

print("\n" + "="*80)
print("SPEC-GUIDED TESTS FOR same_chars")
print("="*80)

def test_same_chars_spec_guided():
    """Spec-guided tests for same_chars function"""
    
    # Specification 1: res == (set(s0) == set(s1))
    print("Testing Specification 1: Core set equality logic")
    
    # Basic set equality cases
    assert same_chars('abc', 'bca') == True, "Spec1: Same characters, different order"
    assert same_chars('hello', 'olleh') == True, "Spec1: Same characters with repetition"
    assert same_chars('abc', 'def') == False, "Spec1: Completely different characters"
    assert same_chars('aab', 'ab') == True, "Spec1: Different frequencies, same unique chars"
    
    # Specification 2: Empty string cases
    print("Testing Specification 2: Empty string behavior")
    
    assert same_chars('', '') == True, "Spec2: Both empty strings"
    assert same_chars('a', '') == False, "Spec2: One empty, one non-empty"
    assert same_chars('', 'b') == False, "Spec2: One empty, one non-empty (reversed)"
    
    # Specification 3: Single character cases
    print("Testing Specification 3: Single character scenarios")
    
    assert same_chars('a', 'a') == True, "Spec3: Same single character"
    assert same_chars('x', 'y') == False, "Spec3: Different single characters"
    assert same_chars('z', 'zzz') == True, "Spec3: Single char vs repeated same char"
    assert same_chars('mmm', 'n') == False, "Spec3: Repeated char vs different single char"
    
    # Specification 4: Disjoint sets
    print("Testing Specification 4: Disjoint character sets")
    
    assert same_chars('abc', 'xyz') == False, "Spec4: Completely disjoint sets"
    assert same_chars('123', '456') == False, "Spec4: Disjoint numeric characters"
    assert same_chars('!@#', '$%^') == False, "Spec4: Disjoint special characters"
    
    # Specification 5: Mutual subset relationship (equivalent to set equality)
    print("Testing Specification 5: Mutual subset relationship")
    
    assert same_chars('abcd', 'dcba') == True, "Spec5: Perfect mutual subsets"
    assert same_chars('aabbcc', 'abc') == True, "Spec5: One is subset with repetitions"
    assert same_chars('abc', 'abcd') == False, "Spec5: Not mutual subsets"
    
    # Additional edge cases targeting specifications
    print("Testing Additional Edge Cases")
    
    # Case sensitivity (targets spec 1)
    assert same_chars('Aa', 'aA') == True, "Edge: Case sensitivity - same chars"
    assert same_chars('A', 'a') == False, "Edge: Case sensitivity - different chars"
    
    # Unicode characters (targets spec 1)
    assert same_chars('αβγ', 'γβα') == True, "Edge: Unicode characters"
    assert same_chars('αβ', 'αγ') == False, "Edge: Different unicode characters"
    
    # Mixed character types (targets multiple specs)
    assert same_chars('a1!', '!1a') == True, "Edge: Mixed alphanumeric and special"
    assert same_chars('a1!', 'a1@') == False, "Edge: Mixed types, one different char"
    
    print("All same_chars spec-guided tests passed!")

def test_make_palindrome_spec_guided():
    """Spec-guided tests for make_palindrome function"""
    
    # Specification 1: res.startswith(string)
    print("Testing Specification 1: Result starts with input")
    
    test_inputs_1 = ['', 'a', 'ab', 'abc', 'hello', 'racecar']
    for inp in test_inputs_1:
        result = make_palindrome(inp)
        assert result.startswith(inp), f"Spec1 failed: '{result}' should start with '{inp}'"
    
    # Specification 2: res == res[::-1] (palindrome property)
    print("Testing Specification 2: Result is palindrome")
    
    test_inputs_2 = ['', 'a', 'ab', 'abc', 'test', 'palindrome', 'x' * 100]
    for inp in test_inputs_2:
        result = make_palindrome(inp)
        assert result == result[::-1], f"Spec2 failed: '{result}' is not a palindrome"
    
    # Specification 3: len(res) >= len(string)
    print("Testing Specification 3: Result length >= input length")
    
    test_inputs_3 = ['', 'a', 'ab', 'abc', 'long_string', 'a' * 50]
    for inp in test_inputs_3:
        result = make_palindrome(inp)
        assert len(result) >= len(inp), f"Spec3 failed: len('{result}') < len('{inp}')"
    
    # Specification 4: len(res) <= 2 * len(string) for non-empty strings
    print("Testing Specification 4: Result length upper bound")
    
    test_inputs_4 = ['a', 'ab', 'abc', 'test', 'example', 'x' * 20]
    for inp in test_inputs_4:
        result = make_palindrome(inp)
        assert len(result) <= 2 * len(inp), f"Spec4 failed: len('{result}') > 2 * len('{inp}')"
    
    # Specification 5: (string == '') == (res == '')
    print("Testing Specification 5: Empty input produces empty result")
    
    assert make_palindrome('') == '', "Spec5 failed: Empty input should produce empty result"
    
    # Additional edge cases targeting specifications
    print("Testing Additional Edge Cases")
    
    # Single character (should satisfy all specs)
    result_single = make_palindrome('x')
    assert result_single.startswith('x'), "Edge: Single char - startswith"
    assert result_single == result_single[::-1], "Edge: Single char - palindrome"
    assert len(result_single) >= 1, "Edge: Single char - length >= input"
    assert len(result_single) <= 2, "Edge: Single char - length <= 2*input"
    
    # Already palindrome cases
    palindromes = ['a', 'aa', 'aba', 'racecar', 'madam']
    for pal in palindromes:
        result = make_palindrome(pal)
        assert result.startswith(pal), f"Edge: Palindrome '{pal}' - startswith"
        assert result == result[::-1], f"Edge: Palindrome '{pal}' - is palindrome"
        assert len(result) >= len(pal), f"Edge: Palindrome '{pal}' - length >= input"
        if pal:  # non-empty
            assert len(result) <= 2 * len(pal), f"Edge: Palindrome '{pal}' - length <= 2*input"
    
    # Worst case scenarios (no palindromic suffix except last char)
    worst_cases = ['ab', 'abc', 'abcd', 'abcde']
    for case in worst_cases:
        result = make_palindrome(case)
        assert result.startswith(case), f"Edge: Worst case '{case}' - startswith"
        assert result == result[::-1], f"Edge: Worst case '{case}' - is palindrome"
        assert len(result) >= len(case), f"Edge: Worst case '{case}' - length >= input"
        assert len(result) <= 2 * len(case), f"Edge: Worst case '{case}' - length <= 2*input"
    
    print("All make_palindrome spec-guided tests passed!")

if __name__ == "__main__":
    print("Running spec-guided tests...")
    test_same_chars_spec_guided()
    print()
    test_make_palindrome_spec_guided()
    print("\nAll spec-guided tests completed successfully!")
