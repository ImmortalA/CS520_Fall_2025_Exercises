"""
Compare Part 1 baseline results with Part 2 self-repair results.
"""
import csv
from pathlib import Path

def load_results(csv_file):
    """Load results into a dict."""
    results = {}
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (row['problem_id'], row['family'], row['strategy'])
            results[key] = {
                'n_correct': int(row['n_correct']),
                'n_samples': int(row['n_samples']),
                'pass@1': float(row['pass@1'])
            }
    return results

def main():
    eval_dir = Path(__file__).parent
    
    part1_file = eval_dir / "results.csv"
    part2_file = eval_dir / "results_part2.csv"
    
    if not part1_file.exists():
        print("ERROR: results.csv not found!")
        return
    
    if not part2_file.exists():
        print("ERROR: results_part2.csv not found!")
        print("Run: python run_eval_part2.py")
        return
    
    part1 = load_results(part1_file)
    part2 = load_results(part2_file)
    
    print("="*70)
    print("Part 2: Self-Repair Comparison")
    print("="*70)
    print()
    
    # Find self_repair entries in Part 2
    print("Self-Repair Results:")
    print("-"*70)
    print(f"{'Problem':<15} {'Family':<10} {'Before':<10} {'After':<10} {'Status'}")
    print("-"*70)
    
    repairs_found = []
    for key, data in sorted(part2.items()):
        problem_id, family, strategy = key
        if strategy == 'self_repair':
            # Find original failure
            original_cot = part1.get((problem_id, family, 'cot'), None)
            original_scot = part1.get((problem_id, family, 'scot'), None)
            
            # Determine which was worse
            if original_cot and original_scot:
                original = original_cot if original_cot['pass@1'] < original_scot['pass@1'] else original_scot
                original_strategy = 'cot' if original_cot['pass@1'] < original_scot['pass@1'] else 'scot'
            elif original_cot:
                original = original_cot
                original_strategy = 'cot'
            elif original_scot:
                original = original_scot
                original_strategy = 'scot'
            else:
                continue
            
            before = f"{original['pass@1']:.3f}"
            after = f"{data['pass@1']:.3f}"
            status = "FIXED" if data['pass@1'] > original['pass@1'] else "STILL FAILS"
            
            print(f"{problem_id:<15} {family:<10} {before:<10} {after:<10} {status}")
            repairs_found.append((problem_id, family, original['pass@1'], data['pass@1']))
    
    print("-"*70)
    print()
    
    # Summary
    if repairs_found:
        improved = sum(1 for _, _, before, after in repairs_found if after > before)
        print(f"Summary:")
        print(f"  Total self-repairs attempted: {len(repairs_found)}")
        print(f"  Successfully fixed: {improved}")
        print(f"  Still failing: {len(repairs_found) - improved}")
    else:
        print("No self-repair solutions found in results_part2.csv")
    
    print()
    print("="*70)

if __name__ == "__main__":
    main()

