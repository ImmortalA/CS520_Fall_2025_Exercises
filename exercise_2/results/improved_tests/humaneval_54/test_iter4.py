"""
Auto-generated pytest file for same_chars
"""
import sys
from pathlib import Path
import importlib.util

solution_dir = Path(r"D:\Umass\Semester_3\cs520\exercises\exercise_1\llm-codegen\generations\humaneval_54\gemini\scot")
tests_dir = Path(r"D:\Umass\Semester_3\cs520\exercises\exercise_1\llm-codegen\tests")
sys.path.insert(0, str(solution_dir))
sys.path.insert(0, str(tests_dir))

# Load candidate solution
spec_sol = importlib.util.spec_from_file_location("same_chars_module", r"D:\Umass\Semester_3\cs520\exercises\exercise_1\llm-codegen\generations\humaneval_54\gemini\scot\scot_sample1.py")
solution_module = importlib.util.module_from_spec(spec_sol)
spec_sol.loader.exec_module(solution_module)
same_chars = getattr(solution_module, "same_chars")

# Load benchmark test module
spec_t = importlib.util.spec_from_file_location("orig_tests", r"D:\Umass\Semester_3\cs520\exercises\exercise_1\llm-codegen\tests\test_humaneval_54.py")
orig_tests = importlib.util.module_from_spec(spec_t)
spec_t.loader.exec_module(orig_tests)

def run_original_tests(func):
    if hasattr(orig_tests, "check"):
        try:
            orig_tests.check(func)
            return (1, 1)
        except AssertionError:
            return (0, 1)
        except Exception:
            return (0, 1)
    elif hasattr(orig_tests, "run_tests"):
        return orig_tests.run_tests(func)
    else:
        return (0, 1)

def run_tests(func):
    # unified entry that combines original and additional tests
    o = run_original_tests(func)
    a = run_additional_tests(func)
    return (o[0] + a[0], o[1] + a[1])
    def assertion(out, exp, atol):
        assert out == exp, f'Expected {exp}, got {out}'

# LLM-generated additional tests
def check_additional(func):
    # Test cases for empty strings
    # 1. Both strings are empty
    # Expected: True (sets are both empty)
    assert func('', '') is True, "Test Case 1 Failed: Both empty strings"

    # 2. First string is non-empty, second is empty
    # Expected: False (sets have different lengths)
    assert func('a', '') is False, "Test Case 2 Failed: First non-empty, second empty"

    # 3. First string is empty, second is non-empty
    # Expected: False (sets have different lengths)
    assert func('', 'b') is False, "Test Case 3 Failed: First empty, second non-empty"

    # Test cases for single unique character strings
    # 4. Both strings have the same single unique character
    # Expected: True (sets are identical, single element)
    assert func('a', 'a') is True, "Test Case 4 Failed: Same single character"
    assert func('zzz', 'z') is True, "Test Case 5 Failed: Same single character, different multiplicity"

    # 5. Both strings have different single unique characters
    # Expected: False (sets have same length but different elements)
    assert func('a', 'b') is False, "Test Case 6 Failed: Different single characters"

    # Test cases for strings with same set length but different elements
    # 6. Strings with multiple characters, same length of unique chars, but different elements
    # Expected: False (e.g., {'a', 'b', 'c'} vs {'a', 'b', 'd'})
    assert func('abc', 'abd') is False, "Test Case 7 Failed: Same set length, one element differs"
    assert func('abc', 'def') is False, "Test Case 8 Failed: Same set length, all elements differ"

    # Test cases involving special characters and whitespace
    # 7. Strings with special characters (same set)
    # Expected: True
    assert func('!@#', '#!@') is True, "Test Case 9 Failed: Special characters, same set"

    # 8. Strings with whitespace characters (same set)
    # Expected: True
    assert func(' a b ', ' b a ') is True, "Test Case 10 Failed: Whitespace characters, same set"

    # 9. Case sensitivity check (assuming it's case-sensitive as per standard string/set behavior)
    # Expected: False
    assert func('abc', 'Abc') is False, "Test Case 11 Failed: Case sensitivity"
    assert func('ABC', 'abc') is False, "Test Case 12 Failed: Case sensitivity"

    # 10. Mixed alphanumeric and special chars
    # Expected: True
    assert func('a1b!', '!b1a') is True, "Test Case 13 Failed: Mixed characters"

    # 11. Unicode characters
    # Expected: True
    assert func('你好世界', '世界你好') is True, "Test Case 14 Failed: Unicode characters"
    assert func('你好', '世界') is False, "Test Case 15 Failed: Different Unicode characters"


def run_additional_tests(func):
    try:
        check_additional(func)
        return (1, 1)
    except AssertionError:
        return (0, 1)
    except Exception:
        return (0, 1)

# LLM-generated additional tests
def check_additional(candidate):
    def assertion(out, exp, atol):
        assert out == exp, f"Expected: {exp}, Got: {out}"

    # --- Edge Cases & Boundary Conditions ---

    # 1. Empty strings
    # Both strings are empty (should have the same set of characters: an empty set)
    assertion(candidate('', ''), True, 0)
    # One string is empty, the other is not
    assertion(candidate('a', ''), False, 0)
    assertion(candidate('', 'b'), False, 0)

    # 2. Single character strings
    # Both strings have the same single character
    assertion(candidate('x', 'x'), True, 0)
    # Both strings have different single characters
    assertion(candidate('x', 'y'), False, 0)
    # One string is a single character, the other is a repeated sequence of that char
    assertion(candidate('z', 'zzzzz'), True, 0)
    assertion(candidate('wwww', 'w'), True, 0)

    # --- Different Code Paths & Branches (based on potential internal logic) ---

    # 3. Strings with identical sets of characters but different order/repetitions
    # Simple permutations (anagrams, essentially checking the set logic)
    assertion(candidate('abc', 'cba'), True, 0)
    assertion(candidate('listen', 'silent'), True, 0)
    assertion(candidate('aabbcc', 'abcabc'), True, 0)

    # 4. Strings where one is a proper subset of the other's unique characters
    # s0 unique chars are a subset of s1 unique chars (and not equal)
    assertion(candidate('abc', 'abcd'), False, 0) # s1 has 'd'
    # s1 unique chars are a subset of s0 unique chars (and not equal)
    assertion(candidate('abcd', 'abc'), False, 0) # s0 has 'd'

    # --- Input Combinations & Character Types ---

    # 5. Case sensitivity (as implied by existing doctests showing 'e' vs 'd' as different)
    assertion(candidate('A', 'a'), False, 0)
    assertion(candidate('hello', 'Hello'), False, 0)
    assertion(candidate('PYTHON', 'python'), False, 0)
    assertion(candidate('PyThOn', 'python'), False, 0) # Mixed case vs lowercase

    # 6. Strings containing numbers
    assertion(candidate('123', '321'), True, 0)
    assertion(candidate('abc1', '1abc'), True, 0)
    assertion(candidate('123', '124'), False, 0) # Different digits

    # 7. Strings containing special characters
    assertion(candidate('!@#', '#@!'), True, 0)
    assertion(candidate('a!b@c#', 'c#b@a!'), True, 0)
    assertion(candidate('a-b-c', 'a-c-d'), False, 0) # Different special char combo

    # 8. Mixed alphanumeric and special characters
    assertion(candidate('a1!b2@', '@2b!1a'), True, 0)
    assertion(candidate('foo bar 123', '123 bar foo'), True, 0)
    assertion(candidate('foo bar', 'foo-bar'), False, 0) # Space vs hyphen treated differently

    # 9. Longer strings with complex character sets (to stress potential iteration loops)
    assertion(candidate('abcdefghijklmnopqrstuvwxyz', 'zyxwuvtsrqponmlkjihgfedcba'), True, 0)
    assertion(candidate('thequickbrownfoxjumpsoverthelazydog', 'abcdefghijklmnopqrstuvwxyz'), True, 0) # Same alphabet
    assertion(candidate('thequickbrownfoxjumpsoverthelazydog', 'thequickbrownfoxjumpsoverthelazydogg'), False, 0) # Extra char in s1


def run_additional_tests(func):
    try:
        check_additional(func)
        return (1, 1)
    except AssertionError:
        return (0, 1)
    except Exception:
        return (0, 1)

# LLM-generated additional tests
def check_additional(candidate):
    # 1. Edge cases: Empty strings
    assert candidate('', '') == True, "Test Case 1 Failed: Both empty strings"
    assert candidate('a', '') == False, "Test Case 2 Failed: One empty string, one non-empty"
    assert candidate('', 'b') == False, "Test Case 3 Failed: One empty string, one non-empty (reversed)"

    # 2. Edge cases: Single unique character strings with varying lengths
    assert candidate('a', 'a') == True, "Test Case 4 Failed: Single char, same"
    assert candidate('x', 'y') == False, "Test Case 5 Failed: Single char, different"
    assert candidate('aaaaa', 'a') == True, "Test Case 6 Failed: Single unique char, different lengths"
    assert candidate('a', 'aaaaa') == True, "Test Case 7 Failed: Single unique char, different lengths (reversed)"

    # 3. Case sensitivity (often a distinct branch in character comparison logic)
    assert candidate('abc', 'ABC') == False, "Test Case 8 Failed: Case sensitivity (all different case)"
    assert candidate('hello', 'Hello') == False, "Test Case 9 Failed: Case sensitivity (partial different case)"
    assert candidate('Apple', 'apple') == False, "Test Case 10 Failed: Case sensitivity (mixed case)"
    assert candidate('apple', 'apple') == True, "Test Case 11 Failed: Case sensitivity (same case, confirm base)"

    # 4. Strings with non-alphabetic characters (numbers, spaces, symbols)
    assert candidate('a b c', 'c a b') == True, "Test Case 12 Failed: Strings with spaces"
    assert candidate('a b c', 'c a b d') == False, "Test Case 13 Failed: Strings with spaces and difference"
    assert candidate('123', '312') == True, "Test Case 14 Failed: Strings with numbers"
    assert candidate('!@#$', '#$@!') == True, "Test Case 15 Failed: Strings with symbols"
    assert candidate('ab123!@', '!@123ab') == True, "Test Case 16 Failed: Mixed character types"
    assert candidate('ab123!@', '!@123abX') == False, "Test Case 17 Failed: Mixed character types with difference"

    # 5. More complex cases: similar length but different characters/ordering
    assert candidate('abcde', 'vwxyz') == False, "Test Case 18 Failed: No common characters"
    assert candidate('abcde', 'edcba') == True, "Test Case 19 Failed: Same characters, different order"
    assert candidate('abcde', 'abcdf') == False, "Test Case 20 Failed: One character difference at end"
    assert candidate('abcde', 'fbcde') == False, "Test Case 21 Failed: One character difference at beginning"
    assert candidate('abcde', 'axcde') == False, "Test Case 22 Failed: One character difference in middle"


def run_additional_tests(func):
    try:
        check_additional(func)
        return (1, 1)
    except AssertionError:
        return (0, 1)
    except Exception:
        return (0, 1)

# LLM-generated additional tests
def check_additional(candidate):
    # 1. Edge case: Both strings are empty
    assert candidate('', '') == True, "Test Case 1 Failed: Both empty strings"

    # 2. Edge case: One string is empty, the other is not
    assert candidate('a', '') == False, "Test Case 2 Failed: s0 not empty, s1 empty"
    assert candidate('', 'b') == False, "Test Case 3 Failed: s0 empty, s1 not empty"

    # 3. Edge case: Single character strings
    assert candidate('x', 'x') == True, "Test Case 4 Failed: Single identical character"
    assert candidate('y', 'z') == False, "Test Case 5 Failed: Single different characters"

    # 4. Case sensitivity test (assuming case-sensitive based on problem description context)
    assert candidate('A', 'a') == False, "Test Case 6 Failed: Different case, same letter"
    assert candidate('Python', 'python') == False, "Test Case 7 Failed: Different case in longer words"
    assert candidate('AbC', 'abC') == False, "Test Case 8 Failed: Mixed case, one character differs by case"

    # 5. Strings with non-alphabetic characters (numbers, symbols, spaces)
    assert candidate('123', '321') == True, "Test Case 9 Failed: Numeric characters, same set"
    assert candidate('hello world', 'world hello') == True, "Test Case 10 Failed: Strings with spaces, same set"
    assert candidate('!@#$', '$#@!') == True, "Test Case 11 Failed: Special characters, same set"
    assert candidate('abc1', '1abc') == True, "Test Case 12 Failed: Mixed alphanumeric, same set"
    assert candidate('abc1', 'abc2') == False, "Test Case 13 Failed: Mixed alphanumeric, different set"

    # 6. Strings with varying lengths but same set of unique characters (minimal repetitions)
    assert candidate('p', 'ppp') == True, "Test Case 14 Failed: Single unique char, repeated in other"
    assert candidate('unique', 'uunniiqquuee') == True, "Test Case 15 Failed: Multiple unique chars, repeated in other"
    assert candidate('aabbc', 'abc') == True, "Test Case 16 Failed: Repeated in s0, unique in s1"

    # 7. More complex scenarios resulting in True, ensuring no implicit order dependency with more typical words
    assert candidate('bac', 'abc') == True, "Test Case 17 Failed: Simple permutation of characters"
    assert candidate('rattlesnake', 'snakeattle') == True, "Test Case 18 Failed: Longer words, same characters, different arrangement"
    assert candidate('topcoderopen', 'openforcoder') == True, "Test Case 19 Failed: Another complex permutation"

    # 8. More complex scenarios resulting in False (minimal differences compared to existing tests)
    assert candidate('apple', 'aple') == False, "Test Case 20 Failed: s0 has an extra 'p' (distinct set)"
    assert candidate('aple', 'apple') == False, "Test Case 21 Failed: s1 has an extra 'p' (distinct set)"
    assert candidate('same', 'sameX') == False, "Test Case 22 Failed: s1 has an additional character"
    assert candidate('sameX', 'same') == False, "Test Case 23 Failed: s0 has an additional character"


def run_additional_tests(func):
    try:
        check_additional(func)
        return (1, 1)
    except AssertionError:
        return (0, 1)
    except Exception:
        return (0, 1)
def test_same_chars():
    passed, total = run_tests(same_chars)
    assert passed == total, f"Tests failed: {passed}/{total} passed"
