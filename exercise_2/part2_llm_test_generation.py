"""
Part 2: LLM-Assisted Test Generation & Coverage Improvement
Uses LLM to generate/improve tests iteratively until coverage convergence.
"""
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple
import csv
import tempfile
import shutil

def select_problems_for_improvement(baseline_csv: Path) -> List[str]:
    """
    Select 2 problems with room for improvement.
    Uses metric: highest |%test - %branch-coverage| × %test
    """
    import csv
    
    problems = []
    with open(baseline_csv) as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                test_pct = float(row['tests_passed']) / float(row['tests_total']) * 100
                branch_cov = float(row['branch_coverage'])
                coverage_gap = abs(test_pct - branch_cov)
                improvement_score = coverage_gap * test_pct
                
                problems.append({
                    'problem_id': row['problem_id'],
                    'improvement_score': improvement_score
                })
            except (ValueError, ZeroDivisionError):
                continue
    
    # Sort by improvement score and select top 2
    problems.sort(key=lambda x: x['improvement_score'], reverse=True)
    selected = [p['problem_id'] for p in problems[:2]]
    
    # Fallback if not enough problems
    if len(selected) < 2:
        with open(baseline_csv) as f:
            reader = csv.DictReader(f)
            all_problems = [row['problem_id'] for row in reader]
            selected = all_problems[:2] if len(all_problems) >= 2 else all_problems
    
    return selected


def create_pytest_test_file(solution_path: Path, test_file: Path, function_name: str, output_dir: Path) -> Path:
    """
    Create a pytest-compatible test file that imports both the solution and
    the original test module, ensuring check(...) or run_tests(...) is executed.
    """
    pytest_test = output_dir / f"test_{solution_path.stem}.py"
    
    test_content = f'''"""
Auto-generated pytest file for {function_name}
"""
import sys
from pathlib import Path
import importlib.util

solution_dir = Path(r"{solution_path.parent}")
tests_dir = Path(r"{test_file.parent}")
sys.path.insert(0, str(solution_dir))
sys.path.insert(0, str(tests_dir))

# Load candidate solution
spec_sol = importlib.util.spec_from_file_location("{function_name}_module", r"{solution_path}")
solution_module = importlib.util.module_from_spec(spec_sol)
spec_sol.loader.exec_module(solution_module)
{function_name} = getattr(solution_module, "{function_name}")

# Load benchmark test module
spec_t = importlib.util.spec_from_file_location("orig_tests", r"{test_file}")
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

def run_tests(func):  # unified entry
    return run_original_tests(func)

def test_{function_name}():
    passed, total = run_tests({function_name})
    assert passed == total, f"Tests failed: {{passed}}/{{total}} passed"
'''
    pytest_test.write_text(test_content, encoding="utf-8")
    return pytest_test


def get_coverage_for_test_suite(solution_path: Path, test_file: Path, function_name: str, output_dir: Path) -> Dict[str, float]:
    """Get coverage metrics for a test suite."""
    try:
        # Create pytest test file
        pytest_test = create_pytest_test_file(solution_path, test_file, function_name, output_dir)
        
        # Run pytest with coverage - measure the solution directory
        coverage_json_path = output_dir / "coverage.json"
        result = subprocess.run(
            [
                sys.executable, "-m", "pytest",
                str(pytest_test),
                "--cov", str(solution_path.parent).replace("\\", "/"),
                "--cov-report", f"json:{coverage_json_path}",
                "--cov-branch",
                "-q"
            ],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=str(output_dir)
        )
        
        coverage_json = coverage_json_path
        line_coverage = 0.0
        branch_coverage = 0.0
        
        if coverage_json.exists():
            with open(coverage_json, 'r', encoding='utf-8') as f:
                cov_data = json.load(f)
                files = cov_data.get('files', {})
                
                # Look for the solution file by its path
                solution_path_str = str(solution_path).replace("\\", "/")
                file_cov = None
                for key in files:
                    # Try to match the solution file path
                    key_normalized = key.replace("\\", "/")
                    if solution_path_str in key_normalized or key_normalized.endswith(solution_path.name):
                        file_cov = files[key]
                        break
                
                # Fallback: look for any file with the function name
                if not file_cov:
                    for key in files:
                        if function_name in key and key.endswith('.py') and 'test' not in key.lower():
                            file_cov = files[key]
                            break
                
                if file_cov:
                    summary = file_cov.get('summary', {})
                    line_coverage = summary.get('percent_covered', 0.0)
                    # Prefer counts if present
                    covered_br = summary.get("covered_branches")
                    num_br = summary.get("num_branches")
                    if isinstance(covered_br, int) and isinstance(num_br, int) and num_br > 0:
                        branch_coverage = round(100.0 * covered_br / num_br, 1)
                    else:
                        # Fallback if the key exists
                        branch_coverage = summary.get("percent_covered_branches", 0.0)
                else:
                    totals = cov_data.get('totals', {})
                    line_coverage = totals.get('percent_covered', 0.0)
                    # Prefer counts if present for totals too
                    covered_br = totals.get("covered_branches")
                    num_br = totals.get("num_branches")
                    if isinstance(covered_br, int) and isinstance(num_br, int) and num_br > 0:
                        branch_coverage = round(100.0 * covered_br / num_br, 1)
                    else:
                        # Fallback if the key exists
                        branch_coverage = totals.get("percent_covered_branches", 0.0)
        
        return {"line": line_coverage, "branch": branch_coverage}
    except Exception as e:
        print(f"    ERROR: Error getting coverage: {e}")
        import traceback
        print(f"    TRACEBACK: {traceback.format_exc()[:200]}")
        return {"line": 0.0, "branch": 0.0}


def generate_tests_with_llm(problem_data: Dict, current_coverage: Dict, existing_tests: str, iteration: int, api_key: str = None) -> str:
    """
    Use LLM to generate improved tests.
    """
    function_name = problem_data["function_name"]
    description = problem_data["description"]
    
    # Try Gemini first, fallback to Mistral
    if api_key is None:
        api_key = os.environ.get("GEMINI_API_KEY")
        use_gemini = True
    else:
        use_gemini = True
    
    if not api_key:
        api_key = os.environ.get("MISTRAL_API_KEY")
        use_gemini = False
    
    if not api_key:
        print("    WARNING: No API key found. Using mock generation.")
        return generate_mock_tests(function_name, description, current_coverage, iteration)
    
    prompt = f"""You are an expert at writing comprehensive unit tests for Python functions.

Current situation:
- Function: {function_name}
- Function description: {description}
- Current line coverage: {current_coverage['line']:.1f}%
- Current branch coverage: {current_coverage['branch']:.1f}%

Existing tests:
{existing_tests[:1000]}...

Your task:
Generate additional unit tests that will increase branch coverage. Focus on:
1. Testing edge cases and boundary conditions
2. Testing different code paths and branches
3. Testing error conditions if applicable
4. Testing various input combinations

Output format: Python code with test functions following this structure:

```python
def check_additional(candidate):
    # Your new test cases here
    # Use assertion(out, exp, atol) helper if needed
    # Example: assertion(candidate(arg1, arg2), expected_result, 0)
    pass

def run_additional_tests(func):
    try:
        check_additional(func)
        return (1, 1)
    except AssertionError:
        return (0, 1)
    except Exception:
        return (0, 1)
```

Generate ONLY the Python code, no explanations. Make sure tests are non-redundant with existing tests.
"""
    
    try:
        if use_gemini:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('models/gemini-2.5-flash')
            response = model.generate_content(prompt)
            generated_code = response.text.strip()
        else:
            from mistralai import Mistral
            client = Mistral(api_key=api_key)
            response = client.chat.complete(
                model="mistral-large-latest",
                messages=[
                    {"role": "system", "content": "You are an expert Python test writer. Output only code."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            generated_code = response.choices[0].message.content.strip()
        
        # Extract code from markdown if present
        if "```python" in generated_code:
            generated_code = generated_code.split("```python")[1].split("```")[0].strip()
        elif "```" in generated_code:
            generated_code = generated_code.split("```")[1].split("```")[0].strip()
        
        return generated_code
        
    except Exception as e:
        print(f"    WARNING: LLM generation failed: {e}. Using mock.")
        return generate_mock_tests(function_name, description, current_coverage, iteration)


def generate_mock_tests(function_name: str, description: str, current_coverage: Dict, iteration: int) -> str:
    """
    Deterministic, assertion-based mock tests that improve branch coverage
    when no LLM is available. We special-case the selected problems.
    """
    if function_name == "has_close_elements":
        # HumanEval 0: has_close_elements(lst, threshold) -> bool
        return r'''
def check_additional(candidate):
    # Trivial cases
    assert candidate([], 1.0) is False
    assert candidate([5.0], 0.1) is False

    # Positive cases (should be True)
    assert candidate([1.0, 1.05], 0.1) is True      # within threshold
    assert candidate([0.0, 10.0, 10.05], 0.1) is True
    assert candidate([-1.0, -1.04], 0.05) is True

    # Negative cases (should be False)
    assert candidate([1.0, 1.2], 0.1) is False
    assert candidate([0.0, 0.11, 0.23], 0.1) is False

    # Edge boundaries
    assert candidate([0.0, 0.1], 0.1) is True       # equality boundary counts
    assert candidate([0.0, 0.10001], 0.1) is False  # just outside

def run_additional_tests(func):
    try:
        check_additional(func)
        return (1, 1)
    except AssertionError:
        return (0, 1)
    except Exception:
        return (0, 1)
'''
    if function_name == "separate_paren_groups":
        # HumanEval 1: separate_paren_groups(s) -> List[str]
        return r'''
def check_additional(candidate):
    assert candidate("") == []
    assert candidate("()") == ["()"]
    assert candidate("()(())") == ["()", "(())"]
    assert candidate("(()())(())") == ["(()())", "(())"]
    assert candidate("((()))") == ["((()))"]

    # Unbalanced parentheses should typically return groups it can parse at top-level
    # (behavior depends on reference implementation; include a sanity case)
    assert candidate("()()()") == ["()", "()", "()"]

def run_additional_tests(func):
    try:
        check_additional(func)
        return (1, 1)
    except AssertionError:
        return (0, 1)
    except Exception:
        return (0, 1)
'''
    if function_name == "same_chars":
        # HumanEval 54: same_chars(s0, s1) -> bool (same set of unique characters)
        return r'''
def check_additional(candidate):
    # identical sets
    assert candidate("abca", "baca") is True
    # order/dupes shouldn't matter
    assert candidate("aabbcc", "cba") is True
    # missing a char
    assert candidate("abc", "ab") is False
    # extra char
    assert candidate("ab", "abd") is False
    # whitespace/punct considered characters
    assert candidate("a b", "b a") is True
    assert candidate("a,b", "ab") is False
    # case-sensitivity
    assert candidate("aA", "Aa") is True
    assert candidate("abc", "ABC") is False  # if implementation is case-sensitive

def run_additional_tests(func):
    try:
        check_additional(func)
        return (1, 1)
    except AssertionError:
        return (0, 1)
    except Exception:
        return (0, 1)
'''
    if function_name == "make_palindrome":
        # HumanEval 10: make_palindrome(s) -> shortest palindrome by appending chars
        return r'''
def check_additional(candidate):
    # already palindrome
    assert candidate("aba") == "aba"
    # append one at end
    assert candidate("ab") == "aba"
    # needs multiple appends
    assert candidate("abcd") == "abcdcba"
    # repeated chars
    assert candidate("aaab") == "aaabaaa"
    # single char
    assert candidate("x") == "x"
    # empty
    assert candidate("") == ""

def run_additional_tests(func):
    try:
        check_additional(func)
        return (1, 1)
    except AssertionError:
        return (0, 1)
    except Exception:
        return (0, 1)
'''
    # Generic fallback (light but branchy): try booleans and empty inputs
    return f'''
def check_additional(candidate):
    # Generic smoke/branch hints; adjust to your function if needed.
    try:
        candidate(None)
    except Exception:
        pass
    try:
        candidate([])
    except Exception:
        pass
    try:
        candidate("", 0)  # may raise or return
    except Exception:
        pass

def run_additional_tests(func):
    try:
        check_additional(func)
        return (1, 1)
    except AssertionError:
        return (0, 1)
    except Exception:
        return (0, 1)
'''


def merge_test_files(pytest_wrapper_file: Path, new_tests_code: str, output_file: Path):
    """Merge new tests into the pytest wrapper file."""
    # Read the pytest wrapper file
    wrapper_content = pytest_wrapper_file.read_text(encoding='utf-8', errors='ignore')
    
    # Check if original test module has assertion() helper and make it available
    # The wrapper loads orig_tests module, so we need to expose assertion if it exists
    has_assertion_helper = "orig_tests" in wrapper_content
    
    # Append new tests BEFORE the test_ function
    # Find where to insert (before def test_...)
    lines = wrapper_content.split('\n')
    new_lines = []
    insert_pos = len(lines)
    
    for i, line in enumerate(lines):
        if line.strip().startswith('def test_'):
            insert_pos = i
            break
    
    # Insert new tests before the test function
    new_lines = lines[:insert_pos]
    
    # Make assertion() helper available if it exists in orig_tests
    if has_assertion_helper and "def assertion" not in wrapper_content:
        new_lines.append("# Make assertion() helper available from original test module")
        new_lines.append("if hasattr(orig_tests, 'assertion'):")
        new_lines.append("    assertion = orig_tests.assertion")
        new_lines.append("else:")
        new_lines.append("    # Fallback: define a simple assertion helper")
        new_lines.append("    def assertion(out, exp, atol):")
        new_lines.append("        assert out == exp, f'Expected {exp}, got {out}'")
    new_lines.append("")
    new_lines.append("# LLM-generated additional tests")
    new_lines.append(new_tests_code)
    
    # Ensure run_additional_tests is defined
    if "def run_additional_tests" not in new_tests_code:
        new_lines.append("\ndef run_additional_tests(func):")
        new_lines.append("    return (0, 0)  # No additional tests")
    
    # Add the rest of the file (test function, etc.)
    new_lines.extend(lines[insert_pos:])
    
    # Update run_tests to combine original and additional tests
    merged_content = '\n'.join(new_lines)
    
    # Find and replace run_tests function
    import re
    # Pattern: def run_tests(func): ... return run_original_tests(func)
    pattern = r'(def run_tests\(func\):\s*#\s*unified entry\s*return run_original_tests\(func\))'
    replacement = '''def run_tests(func):
    # unified entry that combines original and additional tests
    o = run_original_tests(func)
    a = run_additional_tests(func)
    return (o[0] + a[0], o[1] + a[1])'''

    if re.search(pattern, merged_content, re.MULTILINE):
        merged_content = re.sub(pattern, replacement, merged_content, flags=re.MULTILINE)
    else:
        # Try simpler pattern - just look for the function and replace its body
        lines = merged_content.split('\n')
        new_lines = []
        i = 0
        found_run_tests = False
        while i < len(lines):
            line = lines[i]
            if line.strip() == "def run_tests(func):" and not found_run_tests:
                # Found run_tests definition - replace it
                new_lines.append("def run_tests(func):")
                new_lines.append("    # unified entry that combines original and additional tests")
                new_lines.append("    o = run_original_tests(func)")
                new_lines.append("    a = run_additional_tests(func)")
                new_lines.append("    return (o[0] + a[0], o[1] + a[1])")
                # Skip until we find the return statement or next function/class
                i += 1
                while i < len(lines):
                    next_line = lines[i].strip()
                    if next_line.startswith("return run_original_tests(func)"):
                        i += 1  # Skip the return line
                        break
                    elif next_line.startswith("def ") or next_line.startswith("class "):
                        # Next function/class, stop here (but don't skip it)
                        break
                    elif not next_line or next_line.startswith("#"):
                        # Empty line or comment, skip
                        i += 1
                    else:
                        # Something else, skip it
                        i += 1
                found_run_tests = True
                continue
            new_lines.append(line)
            i += 1
        merged_content = '\n'.join(new_lines)
    
    # Fallback: if run_tests doesn't exist at all, add it before test_ function
    if "def run_tests(func):" not in merged_content:
        # Find test function and insert before it
        lines = merged_content.split('\n')
        new_lines = []
        for i, line in enumerate(lines):
            if line.strip().startswith('def test_'):
                new_lines.append("\ndef run_tests(func):")
                new_lines.append("    o = run_original_tests(func)")
                new_lines.append("    a = run_additional_tests(func)")
                new_lines.append("    return (o[0] + a[0], o[1] + a[1])")
                new_lines.append("")
            new_lines.append(line)
        merged_content = '\n'.join(new_lines)
    
    output_file.write_text(merged_content, encoding='utf-8')


def improve_tests_iteratively(problem_id: str, exercise1_root: Path, output_dir: Path) -> List[Dict]:
    """
    Iteratively improve tests using LLM until convergence.
    Convergence: 3 consecutive iterations with <3% increase in coverage.
    """
    data_dir = exercise1_root / "llm-codegen" / "data"
    generations_dir = exercise1_root / "llm-codegen" / "generations"
    tests_dir = exercise1_root / "llm-codegen" / "tests"
    
    # Load problem data
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
        print(f"  WARNING: No solution found for {problem_id}")
        return []
    
    original_test = tests_dir / f"test_{problem_id}.py"
    if not original_test.exists():
        print(f"  WARNING: No test file found for {problem_id}")
        return []
    
    print(f"\n  Improving tests for {problem_id} ({function_name})...")
    
    iterations = []
    coverage_history = []
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        
        # Create initial pytest wrapper from original test
        current_pytest_wrapper = create_pytest_test_file(solution_path, original_test, function_name, tmp_path)
        
        iteration = 0
        convergence_count = 0
        
        while convergence_count < 3 and iteration < 10:  # Max 10 iterations
            iteration += 1
            print(f"    Iteration {iteration}...")
            
            # Measure current coverage using the current pytest wrapper
            coverage_json_path = tmp_path / "coverage.json"
            result = subprocess.run(
                [
                    sys.executable, "-m", "pytest",
                    str(current_pytest_wrapper),
                    "--cov", str(solution_path.parent).replace("\\", "/"),
                    "--cov-report", f"json:{coverage_json_path}",
                    "--cov-branch",
                    "-v"
                ],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(tmp_path)
            )
            
            # Debug: print test execution results
            if result.returncode != 0:
                print(f"      WARNING: Tests failed or had errors (return code: {result.returncode})")
                if result.stderr:
                    print(f"      Error output: {result.stderr[:200]}")
            
            # Parse coverage
            coverage = {"line": 0.0, "branch": 0.0}
            if coverage_json_path.exists():
                with open(coverage_json_path, 'r', encoding='utf-8') as f:
                    cov_data = json.load(f)
                    files = cov_data.get('files', {})
                    solution_path_str = str(solution_path).replace("\\", "/")
                    file_cov = None
                    for key in files:
                        key_normalized = key.replace("\\", "/")
                        if solution_path_str in key_normalized or key_normalized.endswith(solution_path.name):
                            file_cov = files[key]
                            break
                    if file_cov:
                        summary = file_cov.get('summary', {})
                        coverage['line'] = summary.get('percent_covered', 0.0)
                        covered_br = summary.get("covered_branches")
                        num_br = summary.get("num_branches")
                        if isinstance(covered_br, int) and isinstance(num_br, int) and num_br > 0:
                            coverage['branch'] = round(100.0 * covered_br / num_br, 1)
                        else:
                            coverage['branch'] = summary.get("percent_covered_branches", 0.0)
            
            coverage_history.append(coverage['branch'])
            
            # Generate new tests with LLM
            # Read the current wrapper to see what tests we have
            current_wrapper_content = current_pytest_wrapper.read_text(encoding='utf-8', errors='ignore')
            new_tests = generate_tests_with_llm(
                problem_data, coverage, current_wrapper_content, iteration
            )
            
            # Merge new tests into the current pytest wrapper
            next_wrapper = tmp_path / f"test_{problem_id}_iter{iteration}.py"
            merge_test_files(current_pytest_wrapper, new_tests, next_wrapper)
            current_pytest_wrapper = next_wrapper
            
            # Measure new coverage
            coverage_json_path = tmp_path / "coverage.json"
            result = subprocess.run(
                [
                    sys.executable, "-m", "pytest",
                    str(current_pytest_wrapper),
                    "--cov", str(solution_path.parent).replace("\\", "/"),
                    "--cov-report", f"json:{coverage_json_path}",
                    "--cov-branch",
                    "-v"
                ],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(tmp_path)
            )
            
            # Debug: print test execution results
            if result.returncode != 0:
                print(f"      WARNING: Tests failed or had errors (return code: {result.returncode})")
                if result.stderr:
                    print(f"      Error output: {result.stderr[:200]}")
            
            # Debug: check if additional tests are being called
            if "run_additional_tests" in current_wrapper_content:
                # Count test assertions in additional tests
                additional_test_count = current_wrapper_content.count("assert candidate(") + current_wrapper_content.count("assertion(candidate(")
                if additional_test_count > 0:
                    print(f"      DEBUG: Found {additional_test_count} additional test assertions")
            
            new_coverage = {"line": 0.0, "branch": 0.0}
            if coverage_json_path.exists():
                with open(coverage_json_path, 'r', encoding='utf-8') as f:
                    cov_data = json.load(f)
                    files = cov_data.get('files', {})
                    solution_path_str = str(solution_path).replace("\\", "/")
                    file_cov = None
                    for key in files:
                        key_normalized = key.replace("\\", "/")
                        if solution_path_str in key_normalized or key_normalized.endswith(solution_path.name):
                            file_cov = files[key]
                            break
                    if file_cov:
                        summary = file_cov.get('summary', {})
                        new_coverage['line'] = summary.get('percent_covered', 0.0)
                        covered_br = summary.get("covered_branches")
                        num_br = summary.get("num_branches")
                        if isinstance(covered_br, int) and isinstance(num_br, int) and num_br > 0:
                            new_coverage['branch'] = round(100.0 * covered_br / num_br, 1)
                        else:
                            new_coverage['branch'] = summary.get("percent_covered_branches", 0.0)
            
            improvement = new_coverage['branch'] - coverage['branch']
            
            print(f"      Coverage: {coverage['branch']:.1f}% → {new_coverage['branch']:.1f}% (+{improvement:.1f}%)")
            
            iterations.append({
                "iteration": iteration,
                "line_coverage": new_coverage['line'],
                "branch_coverage": new_coverage['branch'],
                "improvement": improvement,
                "test_code": new_tests
            })
            
            # Check convergence
            if iteration >= 3:
                # Check if Coverage(i) - Coverage(i-2) <= 3%
                if coverage_history[-1] - coverage_history[-3] <= 3.0:
                    convergence_count += 1
                else:
                    convergence_count = 0
            
            # Save improved test file for this iteration
            improved_test_dir = output_dir / "improved_tests" / problem_id
            improved_test_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy(current_pytest_wrapper, improved_test_dir / f"test_iter{iteration}.py")
    
    # Save final improved test (last iteration)
    if current_pytest_wrapper.exists():
        improved_test_dir = output_dir / "improved_tests" / problem_id
        improved_test_dir.mkdir(parents=True, exist_ok=True)
        final_test = improved_test_dir / "test_final.py"
        shutil.copy(current_pytest_wrapper, final_test)
        print(f"    Saved final improved test to {final_test}")
    
    return iterations


def main():
    exercise1_root = Path(__file__).parent.parent / "exercise_1"
    baseline_csv = Path(__file__).parent / "results" / "baseline_coverage.csv"
    
    if not baseline_csv.exists():
        print("Error: Baseline coverage CSV not found. Run part1_baseline_coverage.py first.")
        sys.exit(1)
    
    # Select 2 problems
    selected_problems = select_problems_for_improvement(baseline_csv)
    print(f"Selected problems for improvement: {selected_problems}")
    
    output_dir = Path(__file__).parent / "results"
    output_dir.mkdir(exist_ok=True)
    
    # Save selected problems for Part 3
    selected_path = output_dir / "selected_problems.json"
    selected_path.write_text(json.dumps(selected_problems), encoding="utf-8")
    print(f"Saved selected problems to {selected_path}")
    
    all_results = {}
    
    for problem_id in selected_problems:
        iterations = improve_tests_iteratively(problem_id, exercise1_root, output_dir)
        all_results[problem_id] = iterations
        
        # Save results
        results_file = output_dir / f"llm_improvement_{problem_id}.json"
        with open(results_file, 'w') as f:
            json.dump(iterations, f, indent=2)
    
    print("\n" + "="*80)
    print("LLM test improvement complete!")
    print("="*80)


if __name__ == "__main__":
    main()

