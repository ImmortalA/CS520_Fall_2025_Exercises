"""
Generate self-repair solutions for failing cases using LLM APIs.
This automates Part 2 debugging by having LLMs fix their own failures.
"""
import os
import json
from pathlib import Path

# Failures to fix (from results.csv)
FAILURES = [
    {
        "problem_id": "humaneval_25",
        "family": "mistral",
        "strategy": "cot",
        "issue": "TIMEOUT on large primes - inefficient algorithm (divisor += 1 without sqrt optimization)",
        "test_case": "factorize(9999999967) should return [9999999967] but times out",
    },
    {
        "problem_id": "humaneval_54",
        "family": "mistral",
        "strategy": "cot",
        "issue": "Logic error - Counter checks frequency but should only check unique characters",
        "test_case": "same_chars('eabcdzzzz', 'dddzzzzzzzddeddabc') should return True but returns False",
    },
    {
        "problem_id": "humaneval_108",
        "family": "gemini",
        "strategy": "cot",
        "issue": "Edge case handling - incorrect negative number digit sum calculation",
        "test_case": "count_nums([-1, 11, -11]) should return 1 (only 11 has positive digit sum)",
    },
]

def generate_self_repair_with_gemini(problem_id, family, strategy, issue, test_case):
    """Generate fixed code using Gemini API."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY not set")
        return None
    
    try:
        import google.generativeai as genai
    except ImportError:
        print("ERROR: google-generativeai not installed")
        return None
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('models/gemini-2.5-flash')
    
    # Load files
    repo_root = Path(__file__).parent
    data_file = repo_root / f"llm-codegen/data/{problem_id}.json"
    failing_file = repo_root / f"llm-codegen/generations/{problem_id}/{family}/{strategy}/{strategy}_sample1.py"
    
    problem_data = json.loads(data_file.read_text())
    failing_code = failing_file.read_text()
    description = problem_data["description"]
    
    # Build self-repair prompt
    prompt = f"""You are given a failing function implementation and failing test feedback.

Goal: Produce a corrected implementation that fixes the described failures while preserving the contract.

Procedure:
- Diagnose the cause using the failing inputs/expected outputs.
- Propose a minimal, correct fix.
- Provide only the corrected function implementation; no prints.

Problem:
{description}

Failing implementation:
{failing_code}

Issue:
{issue}

Test case that failed:
{test_case}

IMPORTANT: Output ONLY the corrected Python function code. No explanations, no markdown.
"""
    
    print(f"\nGenerating self-repair for {problem_id}/{family}/{strategy}...")
    print(f"Issue: {issue}")
    
    try:
        response = model.generate_content(prompt)
        code = response.text.strip()
        
        # Clean markdown
        if "```python" in code:
            code = code.split("```python")[1].split("```")[0].strip()
        elif "```" in code:
            code = code.split("```")[1].split("```")[0].strip()
        
        # Save
        output_dir = repo_root / f"llm-codegen/generations/{problem_id}/{family}/self_repair"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / "self_repair_sample1.py"
        output_file.write_text(code, encoding='utf-8')
        
        print(f"✓ Saved to {output_file.relative_to(repo_root)}")
        return code
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return None

def main():
    print("="*60)
    print("Self-Repair Code Generation (Part 2)")
    print("="*60)
    print("\nThis script generates self-repair solutions using Gemini API")
    print("for the failures identified in Part 1.\n")
    
    for failure in FAILURES:
        generate_self_repair_with_gemini(
            failure["problem_id"],
            failure["family"],
            failure["strategy"],
            failure["issue"],
            failure["test_case"]
        )
    
    print("\n" + "="*60)
    print("✓ Self-repair generation complete!")
    print("\nNext steps:")
    print("1. Run: python llm-codegen\\eval\\run_eval.py")
    print("2. Check that self_repair solutions now pass")
    print("3. Document the before/after in your report")
    print("="*60)

if __name__ == "__main__":
    main()

