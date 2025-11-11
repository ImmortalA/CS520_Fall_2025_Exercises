"""
Part 1: Baseline Coverage Measurement
Measures line and branch coverage for all Exercise 1 solutions using pytest-cov.
"""
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List
import csv
import tempfile
import shutil

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


def get_coverage_for_solution(solution_path: Path, test_file: Path, function_name: str, output_dir: Path) -> Dict[str, float]:
    """
    Run pytest-cov on a solution and extract coverage metrics.
    """
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
                "--cov-report", "term",
                "--cov-branch",
                "-v"
            ],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=str(output_dir)
        )
        
        # Debug: check if test ran and show output
        if result.returncode != 0:
            if result.stderr:
                print(f"    DEBUG: pytest stderr: {result.stderr[:300]}")
            if result.stdout:
                print(f"    DEBUG: pytest stdout: {result.stdout[:300]}")
        else:
            # Test passed, check if coverage was generated
            if "coverage" not in result.stdout.lower():
                print(f"    DEBUG: No coverage info in stdout")
        
        # Parse JSON coverage report
        coverage_json = coverage_json_path
        line_coverage = 0.0
        branch_coverage = 0.0
        tests_passed = 0
        tests_total = 0
        
        if not coverage_json.exists():
            print(f"    DEBUG: coverage.json not found at {coverage_json}")
        
        if coverage_json.exists():
            with open(coverage_json, 'r', encoding='utf-8') as f:
                cov_data = json.load(f)
                # Find coverage for our solution file
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
                    # Try to get totals if file not found
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
                    # Debug: show available files and what we're looking for
                    if files:
                        print(f"    DEBUG: Looking for solution file: {solution_path.name}")
                        print(f"    DEBUG: Available files in coverage: {list(files.keys())[:5]}")
                    else:
                        print(f"    DEBUG: No files found in coverage data")
        
        # Parse test results from pytest output
        # Look for patterns like "1 passed" or "1 passed, 0 failed"
        for line in result.stdout.split('\n'):
            line_lower = line.lower()
            if 'passed' in line_lower or 'failed' in line_lower:
                # Format: "X passed" or "X passed, Y failed in Zs"
                parts = line.split()
                for i, part in enumerate(parts):
                    if part == 'passed' and i > 0:
                        try:
                            tests_passed = int(parts[i-1])
                            if tests_total == 0:
                                tests_total = tests_passed
                        except (ValueError, IndexError):
                            pass
                    elif part == 'failed' and i > 0:
                        try:
                            tests_failed = int(parts[i-1])
                            tests_total = tests_passed + tests_failed
                        except (ValueError, IndexError):
                            pass
        
        if tests_total == 0:
            # Try alternative parsing - look for test outcome indicators
            stdout_lower = result.stdout.lower()
            if 'passed' in stdout_lower:
                # If we see "passed" but no number, assume 1 test
                tests_passed = 1
                tests_total = 1
            elif 'failed' in stdout_lower and 'passed' not in stdout_lower:
                tests_passed = 0
                tests_total = 1
            else:
                # No test results found
                print(f"    DEBUG: Could not parse test results from: {result.stdout[:200]}")
        
        return {
            "line": line_coverage,
            "branch": branch_coverage,
            "tests_passed": tests_passed,
            "tests_total": tests_total
        }
        
    except subprocess.TimeoutExpired:
        print(f"    ERROR: Test timeout")
        return {"line": 0.0, "branch": 0.0, "tests_passed": 0, "tests_total": 0}
    except Exception as e:
        print(f"    ERROR: {e}")
        import traceback
        print(f"    TRACEBACK: {traceback.format_exc()[:300]}")
        return {"line": 0.0, "branch": 0.0, "tests_passed": 0, "tests_total": 0}


def measure_baseline_coverage(exercise1_root: Path) -> List[Dict]:
    """
    Measure baseline coverage for all problems in Exercise 1.
    """
    results = []
    
    data_dir = exercise1_root / "llm-codegen" / "data"
    generations_dir = exercise1_root / "llm-codegen" / "generations"
    tests_dir = exercise1_root / "llm-codegen" / "tests"
    
    problems = sorted(data_dir.glob("*.json"))
    
    print(f"Measuring baseline coverage for {len(problems)} problems...")
    print("="*80)
    
    # Create temp directory for test files
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        
        for problem_file in problems:
            problem_data = json.loads(problem_file.read_text(encoding='utf-8', errors='ignore'))
            problem_id = problem_data["problem_id"]
            function_name = problem_data["function_name"]
            
            print(f"\n[{problem_id}] {function_name}")
            
            test_file = tests_dir / f"test_{problem_id}.py"
            if not test_file.exists():
                print(f"  WARNING: No test file found")
                continue
            
            # Find best solution (prefer gemini/scot)
            solution_path = None
            problem_generations = generations_dir / problem_id
            
            if problem_generations.exists():
                for family in ["gemini", "mistral"]:
                    for strategy in ["scot", "cot"]:
                        candidate = problem_generations / family / strategy / f"{strategy}_sample1.py"
                        if candidate.exists():
                            solution_path = candidate
                            break
                    if solution_path:
                        break
                
                # Fallback to any solution
                if not solution_path:
                    for py_file in problem_generations.rglob("*.py"):
                        if "sample" in py_file.name:
                            solution_path = py_file
                            break
            
            if not solution_path:
                print(f"  WARNING: No solution found")
                continue
            
            print(f"  Solution: {solution_path.relative_to(exercise1_root)}")
            
            # Measure coverage
            coverage_data = get_coverage_for_solution(solution_path, test_file, function_name, tmp_path)
            
            result = {
                "problem_id": problem_id,
                "function_name": function_name,
                "solution_path": str(solution_path.relative_to(exercise1_root)),
                "line_coverage": coverage_data["line"],
                "branch_coverage": coverage_data["branch"],
                "tests_passed": coverage_data["tests_passed"],
                "tests_total": coverage_data["tests_total"],
            }
            
            # Add interpretation
            branch_cov = coverage_data["branch"]
            if branch_cov < 50:
                result["interpretation"] = "Low branch coverage - many conditional paths untested"
            elif branch_cov < 80:
                result["interpretation"] = "Moderate branch coverage - some edge cases missing"
            else:
                result["interpretation"] = "High branch coverage - most paths tested"
            
            results.append(result)
            
            print(f"  Line: {coverage_data['line']:.1f}%, Branch: {coverage_data['branch']:.1f}%")
            print(f"  Tests: {coverage_data['tests_passed']}/{coverage_data['tests_total']}")
    
    return results


def save_results(results: List[Dict], output_file: Path):
    """Save coverage results to CSV."""
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        if not results:
            return
        
        writer = csv.DictWriter(f, fieldnames=[
            "problem_id", "function_name", "line_coverage", "branch_coverage",
            "tests_passed", "tests_total", "interpretation"
        ])
        writer.writeheader()
        for result in results:
            writer.writerow({
                "problem_id": result["problem_id"],
                "function_name": result["function_name"],
                "line_coverage": f"{result['line_coverage']:.2f}",
                "branch_coverage": f"{result['branch_coverage']:.2f}",
                "tests_passed": result["tests_passed"],
                "tests_total": result["tests_total"],
                "interpretation": result.get("interpretation", "")
            })


def main():
    exercise1_root = Path(__file__).parent.parent / "exercise_1"
    
    if not exercise1_root.exists():
        print(f"Error: Exercise 1 directory not found at {exercise1_root}")
        sys.exit(1)
    
    results = measure_baseline_coverage(exercise1_root)
    
    output_dir = Path(__file__).parent / "results"
    output_dir.mkdir(exist_ok=True)
    
    csv_file = output_dir / "baseline_coverage.csv"
    save_results(results, csv_file)
    
    print("\n" + "="*80)
    print(f"Baseline coverage measurement complete!")
    print(f"Results saved to {csv_file}")
    print(f"Measured {len(results)} problems")
    print("="*80)
    
    # Print summary table
    print("\nSummary Table:")
    print("-" * 100)
    print(f"{'Problem':<20} {'Line %':<10} {'Branch %':<12} {'Tests':<12} {'Notes':<40}")
    print("-" * 100)
    for result in results:
        tests_str = f"{result['tests_passed']}/{result['tests_total']}"
        print(f"{result['problem_id']:<20} {result['line_coverage']:>6.1f}%    {result['branch_coverage']:>6.1f}%      {tests_str:<12} {result.get('interpretation', '')[:38]}")


if __name__ == "__main__":
    main()
