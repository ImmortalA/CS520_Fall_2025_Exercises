"""
Evaluation script specifically for Part 2 self-repair solutions.
Compares baseline (CoT/SCoT) results with self-repair improvements.
"""
import subprocess
import sys
from pathlib import Path

def main():
    eval_dir = Path(__file__).parent
    eval_script = eval_dir / "run_eval.py"
    
    print("="*60)
    print("Part 2: Self-Repair Evaluation")
    print("="*60)
    print()
    
    # Run evaluation with Part 2 results file
    print("Running evaluation with self-repair solutions...")
    print()
    
    result = subprocess.run(
        [
            sys.executable,
            str(eval_script),
            "--results", str(eval_dir / "results_part2.csv")
        ],
        cwd=eval_dir.parent.parent
    )
    
    if result.returncode != 0:
        print("\nEvaluation failed!")
        return
    
    print("\n" + "="*60)
    print("Part 2 Evaluation Complete!")
    print("="*60)
    print()
    print("Results saved to: llm-codegen/eval/results_part2.csv")
    print()
    print("Compare files:")
    print("  - results.csv        (Part 1 baseline - 7 failures)")
    print("  - results_part2.csv  (Part 2 with self-repair)")
    print()
    print("Check which self_repair solutions now pass!")
    print("="*60)

if __name__ == "__main__":
    main()

