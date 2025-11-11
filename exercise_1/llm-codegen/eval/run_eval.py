"""
Entrypoint for evaluating generated solutions.

Expected workflow:
- Discover problems from `../data` and solutions from `../generations`.
- Execute tests in `../tests` against generated code.
- Aggregate metrics and write to `results.csv`.
- Optionally save figures to `plots/`.

This is a scaffold; implement the logic as your project evolves.
"""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Tuple
from threading import Thread
import time

# Support running as a script without package context
try:  # pragma: no cover - simple import fallback
    from .harness import load_solution_function  # type: ignore[no-redef]
except Exception:  # noqa: BLE001
    import sys
    sys.path.append(str(Path(__file__).resolve().parent))
    from harness import load_solution_function  # type: ignore[no-redef]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run evaluation for LLM generations.")
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "data",
        help="Path to the data directory.",
    )
    parser.add_argument(
        "--generations-dir",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "generations",
        help="Path to the generations directory.",
    )
    parser.add_argument(
        "--tests-dir",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "tests",
        help="Path to the tests directory.",
    )
    parser.add_argument(
        "--results",
        type=Path,
        default=Path(__file__).resolve().parent / "results.csv",
        help="CSV file to write aggregated results to (e.g., results.csv)",
    )
    parser.add_argument(
        "--plots-dir",
        type=Path,
        default=Path(__file__).resolve().parent / "plots",
        help="Directory to save plots.",
    )
    return parser.parse_args()


@dataclass
class Problem:
    problem_id: str
    function_name: str


def discover_problems(data_dir: Path) -> List[Problem]:
    problems: List[Problem] = []
    for path in sorted(data_dir.glob("*.json")):
        meta = json.loads(path.read_text(encoding="utf-8"))
        problems.append(Problem(problem_id=meta["problem_id"], function_name=meta["function_name"]))
    return problems


def discover_candidates(generations_dir: Path, problem_id: str) -> List[Path]:
    paths: List[Path] = []
    problem_root = generations_dir / problem_id
    if not problem_root.exists():
        return paths
    # Each model family has subfolders; inside, one or more .py files (samples)
    for model_dir in sorted(problem_root.glob("*")):
        if not model_dir.is_dir():
            continue
        for py_file in sorted(model_dir.glob("*.py")):
            paths.append(py_file)
        for strat_dir in sorted(model_dir.glob("*")):
            if strat_dir.is_dir():
                for py_file in sorted(strat_dir.glob("*.py")):
                    paths.append(py_file)
    return paths


def run_tests_on_candidate(tests_dir: Path, problem_id: str, function_name: str, candidate_path: Path) -> Tuple[int, int]:
    """Return (num_passed, num_total) by executing the tests that import the candidate.

    We assume tests import `function_name` by loading from the candidate path dynamically.
    Tests should be written to call the provided callable directly.
    """
    try:
        func = load_solution_function(candidate_path, function_name)
    except Exception:
        return (0, 1)  # Failed to load
    
    # Execute problem-specific tests: test files named test_{problem_id}.py define a `run_tests(func)`
    test_file = tests_dir / f"test_{problem_id}.py"
    if not test_file.exists():
        return (0, 0)
    
    # Dynamically load test module
    from importlib.util import spec_from_file_location, module_from_spec

    spec = spec_from_file_location(f"tests_{problem_id}", test_file)
    assert spec and spec.loader
    mod = module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[arg-type]
    if not hasattr(mod, "run_tests"):
        raise AttributeError(f"Test module {test_file} must define run_tests(func) -> (passed,total)")
    
    # Run tests with timeout using threading (Windows-compatible)
    result = [None]
    def run_test_thread():
        try:
            result[0] = mod.run_tests(func)
        except Exception as e:
            result[0] = (0, 1)
    
    thread = Thread(target=run_test_thread)
    thread.daemon = True
    thread.start()
    thread.join(timeout=10)  # 10 second timeout
    
    if thread.is_alive():
        # Timeout occurred
        print(" [TIMEOUT]", end="")
        return (0, 1)
    
    if result[0] is None:
        return (0, 1)
    
    passed, total = result[0]
    return int(passed), int(total)


def nCk(n: int, k: int) -> float:
    if k < 0 or k > n:
        return 0.0
    if k == 0 or k == n:
        return 1.0
    # compute combinatorics safely
    num = 1.0
    den = 1.0
    k = min(k, n - k)
    for i in range(1, k + 1):
        num *= (n - (k - i))
        den *= i
    return num / den


def compute_pass_at_k(num_correct: int, num_samples: int, k: int) -> float:
    if num_samples == 0 or k <= 0:
        return 0.0
    k = min(k, num_samples)
    # HumanEval-style pass@k estimator: 1 - C(n-c, k) / C(n, k)
    return 1.0 - (nCk(num_samples - num_correct, k) / nCk(num_samples, k))


def main() -> None:
    args = parse_args()
    args.results.parent.mkdir(parents=True, exist_ok=True)
    args.plots_dir.mkdir(parents=True, exist_ok=True)

    problems = discover_problems(args.data_dir)
    rows: List[List[str]] = [[
        "problem_id",
        "family",
        "strategy",
        "n_samples",
        "n_correct",
        "pass@1",
        "pass@3",
    ]]

    print(f"Found {len(problems)} problems to evaluate")
    print("="*60)
    
    for problem in problems:
        print(f"\nEvaluating: {problem.problem_id} ({problem.function_name})")
        candidates = discover_candidates(args.generations_dir, problem.problem_id)
        print(f"  Found {len(candidates)} candidate solutions")
        # Group by family and strategy derived from path
        grouped: Dict[Tuple[str, str], List[Path]] = {}
        for cand in candidates:
            # cand path: generations/problem/family/[maybe strategy]/<name>.py
            parts = cand.parts
            # Find indices for family and filename
            # .../generations/problem_id/family/(optional strategy)/file
            try:
                problem_idx = parts.index(problem.problem_id)
            except ValueError:
                # skip unexpected layout
                continue
            family = parts[problem_idx + 1] if len(parts) > problem_idx + 1 else "unknown"
            filename = Path(parts[-1]).name
            # strategy from filename prefix before _sample or use parent dir if not present
            strategy = filename.split("_sample", 1)[0].lower().replace(".py", "")
            if strategy == filename.lower().replace(".py", "") and len(parts) > problem_idx + 2:
                # if no _sample pattern, fallback to directory name
                strategy = parts[-2]
            key = (family, strategy)
            grouped.setdefault(key, []).append(cand)

        for (family, strategy), files in sorted(grouped.items()):
            num_correct = 0
            print(f"  Testing {family}/{strategy}: ", end="")
            for cand in files:
                p, t = run_tests_on_candidate(args.tests_dir, problem.problem_id, problem.function_name, cand)
                result_symbol = "✓" if (t > 0 and p == t) else "✗"
                print(result_symbol, end=" ")
                if t > 0 and p == t:
                    num_correct += 1
            print(f"({num_correct}/{len(files)})")
            n = len(files)
            pass_at_1 = compute_pass_at_k(num_correct, n, k=1)
            pass_at_3 = compute_pass_at_k(num_correct, n, k=3)
            rows.append([
                problem.problem_id,
                family,
                strategy,
                str(n),
                str(num_correct),
                f"{pass_at_1:.3f}",
                f"{pass_at_3:.3f}",
            ])

    with args.results.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    
    print("\n" + "="*60)
    print(f"✓ Evaluation complete!")
    print(f"✓ Wrote results to {args.results}")
    print(f"✓ Total rows: {len(rows)-1}")
    print("="*60)


if __name__ == "__main__":
    main()



