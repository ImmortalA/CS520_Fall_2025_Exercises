"""
Compare CoT, SCoT, and Innovation strategy results.
"""
import csv
from pathlib import Path
from collections import defaultdict

def load_results(csv_file):
    """Load results grouped by problem and family."""
    results = defaultdict(dict)
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            problem = row['problem_id']
            family = row['family']
            strategy = row['strategy']
            pass_at_1 = float(row['pass@1'])
            
            key = (problem, family)
            results[key][strategy] = pass_at_1
    return results

def main():
    eval_dir = Path(__file__).parent
    
    # Try to load all three result files
    part1_file = eval_dir / "results.csv"
    part3_file = eval_dir / "results_part3.csv"
    
    if not part3_file.exists():
        print("ERROR: results_part3.csv not found!")
        print("Run: python llm-codegen\\eval\\run_eval.py --results llm-codegen\\eval\\results_part3.csv")
        return
    
    part3_data = load_results(part3_file)
    
    print("="*80)
    print("Strategy Comparison: CoT vs SCoT vs Test-Driven Refinement")
    print("="*80)
    print()
    
    # Summary by family and strategy
    family_stats = defaultdict(lambda: defaultdict(list))
    
    for (problem, family), strategies in sorted(part3_data.items()):
        for strategy, score in strategies.items():
            if strategy in ['cot', 'scot', 'test_driven_refinement']:
                family_stats[family][strategy].append(score)
    
    print("Overall Performance by Family and Strategy:")
    print("-"*80)
    print(f"{'Family':<10} {'Strategy':<25} {'Avg pass@1':<12} {'Success Rate'}")
    print("-"*80)
    
    for family in sorted(family_stats.keys()):
        for strategy in ['cot', 'scot', 'test_driven_refinement']:
            if strategy in family_stats[family]:
                scores = family_stats[family][strategy]
                avg = sum(scores) / len(scores) if scores else 0
                count = sum(1 for s in scores if s > 0.99)
                total = len(scores)
                print(f"{family:<10} {strategy:<25} {avg:>6.3f}       {count}/{total} ({count/total*100:.1f}%)")
    
    print("-"*80)
    print()
    
    # Problem-by-problem comparison
    print("Problem-by-Problem Comparison:")
    print("-"*80)
    print(f"{'Problem':<15} {'Family':<10} {'CoT':<8} {'SCoT':<8} {'Innovation':<12} {'Best'}")
    print("-"*80)
    
    for (problem, family), strategies in sorted(part3_data.items()):
        cot = strategies.get('cot', 0)
        scot = strategies.get('scot', 0)
        innov = strategies.get('test_driven_refinement', 0)
        
        best = max(cot, scot, innov)
        best_name = 'CoT' if cot == best else ('SCoT' if scot == best else 'Innovation')
        
        print(f"{problem:<15} {family:<10} {cot:.3f}    {scot:.3f}    {innov:.3f}        {best_name}")
    
    print("-"*80)
    print()
    
    # Did innovation help?
    print("Innovation Strategy Impact:")
    print("-"*80)
    
    for family in sorted(family_stats.keys()):
        cot_avg = sum(family_stats[family]['cot']) / len(family_stats[family]['cot'])
        scot_avg = sum(family_stats[family]['scot']) / len(family_stats[family]['scot'])
        innov_avg = sum(family_stats[family].get('test_driven_refinement', [0])) / max(len(family_stats[family].get('test_driven_refinement', [1])), 1)
        
        baseline_best = max(cot_avg, scot_avg)
        improvement = innov_avg - baseline_best
        
        print(f"{family}:")
        print(f"  Best baseline (CoT/SCoT): {baseline_best:.3f}")
        print(f"  Innovation: {innov_avg:.3f}")
        print(f"  Change: {improvement:+.3f} ({improvement/baseline_best*100:+.1f}%)")
        print()
    
    print("="*80)

if __name__ == "__main__":
    main()

