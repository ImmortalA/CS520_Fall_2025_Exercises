"""
Evaluation script specifically for Part 3 innovation strategy.
Evaluates Test-Driven Refinement solutions and compares with baseline.
"""
import subprocess
import sys
from pathlib import Path

def main():
    eval_dir = Path(__file__).parent
    eval_script = eval_dir / "run_eval.py"
    
    print("="*60)
    print("Part 3: Innovation Strategy Evaluation")
    print("Test-Driven Refinement")
    print("="*60)
    print()
    
    # Run evaluation with Part 3 results file
    print("Running evaluation with innovation strategy solutions...")
    print()
    
    result = subprocess.run(
        [
            sys.executable,
            str(eval_script),
            "--results", str(eval_dir / "results_part3.csv")
        ],
        cwd=eval_dir.parent.parent
    )
    
    if result.returncode != 0:
        print("\nEvaluation failed!")
        return
    
    print("\n" + "="*60)
    print("Part 3 Evaluation Complete!")
    print("="*60)
    print()
    print("Results saved to: llm-codegen/eval/results_part3.csv")
    print()
    print("This file includes:")
    print("  - All CoT and SCoT baseline results (from Part 1)")
    print("  - All self_repair results (from Part 2)")
    print("  - NEW: test_driven_refinement results (Part 3)")
    print()
    print("Next step: Compare strategies")
    print("  python llm-codegen\\eval\\compare_strategies.py")
    print("="*60)

if __name__ == "__main__":
    main()

