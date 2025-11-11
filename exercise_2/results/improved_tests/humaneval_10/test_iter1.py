"""
Auto-generated pytest file for make_palindrome
"""
import sys
from pathlib import Path
import importlib.util

solution_dir = Path(r"D:\Umass\Semester_3\cs520\exercises\exercise_1\llm-codegen\generations\humaneval_10\gemini\scot")
tests_dir = Path(r"D:\Umass\Semester_3\cs520\exercises\exercise_1\llm-codegen\tests")
sys.path.insert(0, str(solution_dir))
sys.path.insert(0, str(tests_dir))

# Load candidate solution
spec_sol = importlib.util.spec_from_file_location("make_palindrome_module", r"D:\Umass\Semester_3\cs520\exercises\exercise_1\llm-codegen\generations\humaneval_10\gemini\scot\scot_sample1.py")
solution_module = importlib.util.module_from_spec(spec_sol)
spec_sol.loader.exec_module(solution_module)
make_palindrome = getattr(solution_module, "make_palindrome")

# Load benchmark test module
spec_t = importlib.util.spec_from_file_location("orig_tests", r"D:\Umass\Semester_3\cs520\exercises\exercise_1\llm-codegen\tests\test_humaneval_10.py")
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
def check_additional(candidate):
    # Test cases where the input string is already a palindrome
    # This covers the 'is_palindrome' condition being true for i=0
    assert candidate('a') == 'a'
    assert candidate('aba') == 'aba'
    assert candidate('noon') == 'noon'
    assert candidate('racecar') == 'racecar'
    assert candidate('level') == 'level'

    # Test cases where the longest palindromic suffix is only the last character,
    # requiring the reversal of a long prefix. This tests the i=n-1 case for palindrome suffix.
    assert candidate('abc') == 'abcba'
    assert candidate('abcdef') == 'abcdefedcba'
    assert candidate('topcoder') == 'topcoderpocdot'

    # Test cases with intermediate palindromic suffixes (0 < i < n-1)
    # These scenarios ensure that the loop correctly identifies non-single-character palindromic suffixes
    # before reaching the final character.
    assert candidate('abcc') == 'abccba' # 'cc' is palindromic suffix, i=2
    assert candidate('banana') == 'bananab' # 'anana' is palindromic suffix, i=1

def run_additional_tests(func):
    try:
        check_additional(func)
        return (1, 1)
    except AssertionError:
        return (0, 1)
    except Exception:
        return (0, 1)
def test_make_palindrome():
    passed, total = run_tests(make_palindrome)
    assert passed == total, f"Tests failed: {passed}/{total} passed"
