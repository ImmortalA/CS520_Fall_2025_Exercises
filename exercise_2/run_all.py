"""
Master script to run all parts of Exercise 2 in sequence.
"""
import sys
from pathlib import Path

def main():
    print("="*80)
    print("Exercise 2: Automated Testing & Coverage")
    print("="*80)
    
    scripts_dir = Path(__file__).parent
    
    # Part 1: Baseline Coverage
    print("\n[Part 1] Measuring baseline coverage...")
    print("-" * 80)
    import subprocess
    result1 = subprocess.run([sys.executable, str(scripts_dir / "part1_baseline_coverage.py")])
    if result1.returncode != 0:
        print("WARNING: Part 1 had errors, but continuing...")
    
    # Part 2: LLM Test Generation
    print("\n[Part 2] Improving tests with LLM...")
    print("-" * 80)
    result2 = subprocess.run([sys.executable, str(scripts_dir / "part2_llm_test_generation.py")])
    if result2.returncode != 0:
        print("WARNING: Part 2 had errors, but continuing...")
    
    # Part 3: Fault Detection
    print("\n[Part 3] Testing fault detection...")
    print("-" * 80)
    result3 = subprocess.run([sys.executable, str(scripts_dir / "part3_fault_detection.py")])
    if result3.returncode != 0:
        print("WARNING: Part 3 had errors")
    
    print("\n" + "="*80)
    print("All parts completed!")
    print("="*80)

if __name__ == "__main__":
    main()


