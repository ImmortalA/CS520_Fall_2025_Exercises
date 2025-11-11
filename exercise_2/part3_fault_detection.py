"""
Part 3: Fault Detection Check
Injects bugs into solutions and checks if tests catch them.
"""
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple
import shutil
import random

def inject_bug(solution_code: str, bug_type: str = "random", function_name: str = None) -> Tuple[str, str]:
    """
    Inject a realistic bug into the solution code.
    Returns (buggy_code, bug_description)
    """
    lines = solution_code.split('\n')
    
    # Function-specific bug injection for better testability
    if function_name == "same_chars":
        # For same_chars: change == to != (inverts the result)
        if "set(s0) == set(s1)" in solution_code:
            buggy_code = solution_code.replace("set(s0) == set(s1)", "set(s0) != set(s1)", 1)
            bug_description = "Wrong operator: changed == to != (inverts result)"
            return buggy_code, bug_description
        # Alternative: always return False
        elif "return set(s0)" in solution_code:
            buggy_code = solution_code.replace("return set(s0) == set(s1)", "return False", 1)
            bug_description = "Always returns False (broken logic)"
            return buggy_code, bug_description
    
    elif function_name == "make_palindrome":
        # For make_palindrome: change range(n + 1) to range(n) (off-by-one)
        if "range(n + 1)" in solution_code:
            buggy_code = solution_code.replace("range(n + 1)", "range(n)", 1)
            bug_description = "Off-by-one error: changed range(n + 1) to range(n), missing empty string case"
            return buggy_code, bug_description
        # Alternative: don't reverse the prefix
        elif "[::-1]" in solution_code and "prefix_to_reverse" in solution_code:
            buggy_code = solution_code.replace("prefix_to_reverse[::-1]", "prefix_to_reverse", 1)
            bug_description = "Wrong operation: removed reversal of prefix, returns incorrect palindrome"
            return buggy_code, bug_description
        # Alternative: change palindrome check
        elif "is_palindrome(postfix)" in solution_code:
            buggy_code = solution_code.replace("is_palindrome(postfix)", "not is_palindrome(postfix)", 1)
            bug_description = "Wrong logic: inverted palindrome check, finds non-palindromic suffix"
            return buggy_code, bug_description
    
    # Generic bug injection (fallback)
    if bug_type == "random":
        bug_type = random.choice(["off_by_one", "wrong_boundary", "wrong_operator", "missing_check"])
    
    buggy_code = solution_code
    bug_description = ""
    
    if bug_type == "off_by_one":
        # Change range or index by 1
        for i, line in enumerate(lines):
            if "range(" in line and "len(" in line:
                # Change range(len(x)) to range(len(x) + 1) or range(len(x) - 1)
                if "range(len(" in line:
                    buggy_code = buggy_code.replace("range(len(", "range(len(" + " - 1", 1)
                    bug_description = "Off-by-one error: changed range to exclude last element"
                    break
            elif "range(" in line and " - 1" in line:
                buggy_code = buggy_code.replace(" - 1", "", 1)
                bug_description = "Off-by-one error: removed -1 from range, causing index out of bounds"
                break
            elif "range(" in line and " + 1" in line:
                buggy_code = buggy_code.replace(" + 1", "", 1)
                bug_description = "Off-by-one error: removed +1 from range"
                break
    
    elif bug_type == "wrong_boundary":
        # Change comparison operator
        replacements = [
            (" < ", " <= "),
            (" <= ", " < "),
            (" > ", " >= "),
            (" >= ", " > "),
            (" == ", " != "),
            (" != ", " == "),
        ]
        for old, new in replacements:
            if old in buggy_code:
                buggy_code = buggy_code.replace(old, new, 1)
                bug_description = f"Wrong boundary: changed {old.strip()} to {new.strip()}"
                break
    
    elif bug_type == "wrong_operator":
        # Change arithmetic operator
        replacements = [
            (" + ", " - "),
            (" - ", " + "),
            (" * ", " / "),
        ]
        for old, new in replacements:
            if old in buggy_code and old in buggy_code.split('\n')[2:]:  # Skip function def
                buggy_code = buggy_code.replace(old, new, 1)
                bug_description = f"Wrong operator: changed {old.strip()} to {new.strip()}"
                break
    
    elif bug_type == "missing_check":
        # Remove a conditional check
        for i, line in enumerate(lines):
            if "if " in line and "return" in lines[i+1] if i+1 < len(lines) else False:
                # Remove the if statement
                buggy_code = buggy_code.replace(line + "\n", "", 1)
                bug_description = f"Missing check: removed conditional '{line.strip()}'"
                break
    
    if not bug_description:
        # Fallback: simple modification - try to find return statement and modify it
        if "return " in solution_code:
            # Try to invert boolean returns
            if "return True" in solution_code:
                buggy_code = solution_code.replace("return True", "return False", 1)
                bug_description = "Changed return True to return False"
            elif "return False" in solution_code:
                buggy_code = solution_code.replace("return False", "return True", 1)
                bug_description = "Changed return False to return True"
            else:
                # Change == to != in return statement
                buggy_code = solution_code.replace(" == ", " != ", 1)
                bug_description = "Changed == to != in return statement"
        else:
            # Last resort: add a bug that will definitely break things
            buggy_code = solution_code + "\n    return None  # BUG: added invalid return"
            bug_description = "Added invalid return statement"
    
    return buggy_code, bug_description


def test_buggy_solution(buggy_code: str, test_file: Path, function_name: str, output_dir: Path) -> Dict:
    """
    Test if the buggy solution is caught by tests.
    Returns dict with test results.
    """
    import tempfile
    import importlib.util
    
    # Write buggy solution with UTF-8 encoding
    buggy_file = output_dir / f"{function_name}_buggy.py"
    buggy_file.write_text(buggy_code, encoding='utf-8')
    
    # Read test file with UTF-8 encoding, ignore errors
    test_file_content = test_file.read_text(encoding='utf-8', errors='ignore')
    
    pytest_test = output_dir / f"test_{function_name}_buggy.py"
    
    # Check if test_file is a pytest wrapper (from Part 2) or original test file
    is_pytest_wrapper = "importlib.util" in test_file_content and "spec_from_file_location" in test_file_content
    
    if is_pytest_wrapper:
        # Test file is a pytest wrapper from Part 2
        # Modify it to use the buggy solution instead of the original
        # Replace the solution loading part with buggy solution loading
        buggy_file_abs = buggy_file.resolve()
        
        # Find and replace the solution loading section
        lines = test_file_content.split('\n')
        new_lines = []
        i = 0
        while i < len(lines):
            line = lines[i]
            # Look for solution loading section
            if 'spec_from_file_location' in line and function_name in line and '_module' in line:
                # Skip the original solution loading (next few lines until we load the function)
                # Replace with buggy solution loading
                new_lines.append(f'# Load buggy solution')
                new_lines.append(f'spec_sol = importlib.util.spec_from_file_location("{function_name}_buggy_module", r"{buggy_file_abs}")')
                new_lines.append(f'solution_module = importlib.util.module_from_spec(spec_sol)')
                new_lines.append(f'spec_sol.loader.exec_module(solution_module)')
                new_lines.append(f'{function_name} = getattr(solution_module, "{function_name}")')
                # Skip until we're past the function loading
                i += 1
                while i < len(lines) and (function_name not in lines[i] or 'getattr' not in lines[i]):
                    i += 1
                if i < len(lines):
                    i += 1  # Skip the getattr line
                continue
            new_lines.append(line)
            i += 1
        
        test_content = '\n'.join(new_lines)
        
        # Replace the test function to check for bug detection
        # Find the test function and modify it
        test_content = test_content.replace(
            f'def test_{function_name}():',
            f'def test_{function_name}_buggy():'
        )
        # Modify the assertion to check if bug was caught
        # Look for the assertion in the test function
        import re
        # Pattern to find the test function and replace its assertion
        pattern = rf'(def test_{function_name}_buggy\(\):.*?assert passed == total.*?f"Tests failed:.*?")'
        replacement = rf'''def test_{function_name}_buggy():
    passed, total = run_tests({function_name})
    # Bug was caught if fewer tests passed than total
    assert passed < total, "Bug NOT caught by tests"'''
        
        # Try to replace the test function
        if re.search(pattern, test_content, re.DOTALL):
            test_content = re.sub(pattern, replacement, test_content, flags=re.DOTALL)
        else:
            # Try simpler pattern - just replace the assertion line
            test_content = re.sub(
                rf'assert passed == total.*?',
                'assert passed < total, "Bug NOT caught by tests"',
                test_content,
                flags=re.DOTALL
            )
            
            # If still not found, add the buggy test function at the end
            if f'def test_{function_name}_buggy():' not in test_content:
                test_content += f'''

def test_{function_name}_buggy():
    passed, total = run_tests({function_name})
    # Bug was caught if fewer tests passed than total
    assert passed < total, "Bug NOT caught by tests"
'''
    else:
        # Test file is original test file - create wrapper like before
        solution_module_name = f"{function_name}_solution"
        solution_copy = output_dir / f"{solution_module_name}.py"
        solution_copy.write_text(buggy_code, encoding='utf-8')
        
        test_content = f'''
"""
Pytest test file for buggy {function_name}
"""
import sys
from pathlib import Path

# Add test directory to path so we can import the solution module
test_dir = Path(__file__).parent.resolve()
sys.path.insert(0, str(test_dir))

# Import solution as a regular module (coverage will track this)
from {solution_module_name} import {function_name}

# --- Original benchmark tests (may define check(candidate)) ---
{test_file_content}

# --- Uniform wrapper so we can always call run_tests(func) ---
def _has_name(name: str) -> bool:
    try:
        globals()[name]
        return True
    except KeyError:
        return False

if _has_name("check"):
    def run_original_tests(func):
        try:
            check(func)
            return (1, 1)
        except AssertionError:
            return (0, 1)
        except Exception:
            return (0, 1)
elif _has_name("run_tests"):
    def run_original_tests(func):
        return run_tests(func)
else:
    def run_original_tests(func):
        # Nothing available; mark as 0/1 so coverage still records
        return (0, 1)

def run_tests(func):
    # single-source wrapper used by our harness
    return run_original_tests(func)

# --- Pytest entrypoint ---
def test_{function_name}_buggy():
    result = run_tests({function_name})
    # Assert that fewer tests passed than total (bug was caught)
    assert result[0] < result[1], "Bug NOT caught by tests"
'''
    
    pytest_test.write_text(test_content, encoding='utf-8')
    
    # Run tests
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", str(pytest_test), "-v"],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=output_dir
        )
        
        # Check if tests failed (bug was caught)
        # Assertion: assert result[0] < result[1] means "bug was caught"
        # - If assertion PASSES (pytest returns 0): bug WAS caught
        # - If assertion FAILS (pytest returns non-zero): bug was NOT caught
        bug_caught = result.returncode == 0  # Zero exit code means assertion passed, bug was caught
        
        return {
            "bug_caught": bug_caught,  # Bug caught if pytest passed (assertion passed)
            "tests_passed": 1 if bug_caught else 0,  # Test passed = bug was caught
            "tests_total": 1,
            "pytest_output": result.stdout[:500]  # First 500 chars
        }
    except Exception as e:
        return {
            "bug_caught": False,
            "tests_passed": 0,
            "tests_total": 1,
            "error": str(e)
        }


def run_fault_detection(problem_id: str, exercise1_root: Path, output_dir: Path) -> Dict:
    """
    Run fault detection for a problem.
    """
    data_dir = exercise1_root / "llm-codegen" / "data"
    generations_dir = exercise1_root / "llm-codegen" / "generations"
    tests_dir = exercise1_root / "llm-codegen" / "tests"
    
    # Load problem
    problem_file = data_dir / f"{problem_id}.json"
    problem_data = json.loads(problem_file.read_text(encoding='utf-8', errors='ignore'))
    function_name = problem_data["function_name"]
    
    # Find solution
    solution_path = None
    problem_generations = generations_dir / problem_id
    for family in ["gemini", "mistral"]:
        for strategy in ["scot", "cot"]:
            candidate = problem_generations / family / strategy / f"{strategy}_sample1.py"
            if candidate.exists():
                solution_path = candidate
                break
        if solution_path:
            break
    
    if not solution_path:
        return {"error": "No solution found"}
    
    # Try to use improved tests from Part 2, fallback to original tests
    improved_test_dir = Path(__file__).parent / "results" / "improved_tests" / problem_id
    test_file = None
    
    # Look for final improved test first
    if improved_test_dir.exists():
        final_test = improved_test_dir / "test_final.py"
        if final_test.exists():
            test_file = final_test
            print(f"    Using improved test from Part 2: {final_test}")
        else:
            # Look for the last iteration
            iter_files = sorted(improved_test_dir.glob("test_iter*.py"))
            if iter_files:
                test_file = iter_files[-1]
                print(f"    Using improved test from Part 2 (iteration): {test_file}")
    
    # Fallback to original test
    if test_file is None or not test_file.exists():
        test_file = tests_dir / f"test_{problem_id}.py"
        if not test_file.exists():
            return {"error": "No test file found"}
        print(f"    Using original test file: {test_file}")
    
    print(f"\n  Testing fault detection for {problem_id} ({function_name})...")
    
    # Read original solution
    original_code = solution_path.read_text(encoding='utf-8', errors='ignore')
    
    # Inject bug (pass function_name for function-specific bugs)
    buggy_code, bug_description = inject_bug(original_code, function_name=function_name)
    
    print(f"    Injected bug: {bug_description}")
    
    # Test buggy solution
    test_result = test_buggy_solution(buggy_code, test_file, function_name, output_dir)
    
    result = {
        "problem_id": problem_id,
        "function_name": function_name,
        "bug_description": bug_description,
        "bug_caught": test_result["bug_caught"],
        "tests_passed": test_result["tests_passed"],
        "tests_total": test_result["tests_total"],
    }
    
    if test_result["bug_caught"]:
        print(f"    SUCCESS: Bug was caught by tests!")
        result["conclusion"] = "Tests successfully detected the injected bug"
    else:
        print(f"    FAILED: Bug was NOT caught by tests")
        result["conclusion"] = "Tests failed to detect the injected bug - coverage may be insufficient"
    
    # Save buggy code for inspection
    buggy_dir = output_dir / "buggy_solutions" / problem_id
    buggy_dir.mkdir(parents=True, exist_ok=True)
    (buggy_dir / f"{function_name}_buggy.py").write_text(buggy_code, encoding='utf-8')
    (buggy_dir / "bug_description.txt").write_text(bug_description, encoding='utf-8')
    
    return result


def main():
    exercise1_root = Path(__file__).parent.parent / "exercise_1"
    
    # Get problems from Part 2 (same problems used for test improvement)
    results_dir = Path(__file__).parent / "results"
    selected_path = results_dir / "selected_problems.json"
    
    if selected_path.exists():
        # Load the problems selected by Part 2
        selected_problems = json.loads(selected_path.read_text(encoding="utf-8"))
        print(f"Loaded selected problems from Part 2: {selected_problems}")
    else:
        # Fallback: use baseline CSV to select first 2 problems
        baseline_csv = results_dir / "baseline_coverage.csv"
        if baseline_csv.exists():
            import csv
            problems = []
            with open(baseline_csv, encoding='utf-8', errors='ignore') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    problems.append(row['problem_id'])
            selected_problems = problems[:2] if len(problems) >= 2 else problems
            print(f"WARNING: Part 2 results not found. Using first 2 problems from baseline: {selected_problems}")
        else:
            # Default selection
            selected_problems = ["humaneval_0", "humaneval_1"]
            print(f"WARNING: No baseline CSV found. Using default problems: {selected_problems}")
    
    print(f"Running fault detection for: {selected_problems}")
    
    output_dir = Path(__file__).parent / "results"
    output_dir.mkdir(exist_ok=True)
    
    results = []
    
    for problem_id in selected_problems:
        result = run_fault_detection(problem_id, exercise1_root, output_dir)
        results.append(result)
    
    # Save results
    results_file = output_dir / "fault_detection_results.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\n" + "="*80)
    print("Fault detection complete!")
    print(f"Results saved to {results_file}")
    print("="*80)
    
    # Print summary
    print("\nFault Detection Summary:")
    print("-" * 80)
    for result in results:
        status = "CAUGHT" if result.get("bug_caught") else "NOT CAUGHT"
        print(f"{result['problem_id']:<20} {status:<12} {result.get('bug_description', '')[:50]}")


if __name__ == "__main__":
    main()

