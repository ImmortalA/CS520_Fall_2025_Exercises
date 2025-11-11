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

# Make assertion() helper available from original test module
if hasattr(orig_tests, 'assertion'):
    assertion = orig_tests.assertion
else:
    # Fallback: define a simple assertion helper
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
def test_same_chars():
    passed, total = run_tests(same_chars)
    assert passed == total, f"Tests failed: {passed}/{total} passed"
