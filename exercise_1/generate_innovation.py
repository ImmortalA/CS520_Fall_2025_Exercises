"""
Generate solutions using the Test-Driven Refinement innovation strategy.
This is the Part 3 novel strategy.
"""
import os
import json
import time
from pathlib import Path

def generate_with_gemini(problem_id, description, function_name, prompt_template):
    """Generate using Gemini API."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return None
    
    try:
        import google.generativeai as genai
    except ImportError:
        return None
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('models/gemini-2.5-flash')
    
    prompt = f"{prompt_template}\n\nProblem:\n{description}\n\nFunction name: {function_name}\n\nIMPORTANT: Output ONLY the function implementation code. No explanations, no markdown."
    
    try:
        response = model.generate_content(prompt)
        code = response.text.strip()
        
        # Clean markdown
        if "```python" in code:
            code = code.split("```python")[1].split("```")[0].strip()
        elif "```" in code:
            code = code.split("```")[1].split("```")[0].strip()
        
        return code
    except Exception as e:
        print(f"    Error: {e}")
        return None

def generate_with_mistral(problem_id, description, function_name, prompt_template):
    """Generate using Mistral API."""
    api_key = os.environ.get("MISTRAL_API_KEY")
    if not api_key:
        return None
    
    try:
        from mistralai import Mistral
    except ImportError:
        return None
    
    client = Mistral(api_key=api_key)
    
    prompt = f"{prompt_template}\n\nProblem:\n{description}\n\nFunction name: {function_name}\n\nIMPORTANT: Output ONLY the function implementation code. No explanations, no markdown."
    
    try:
        response = client.chat.complete(
            model="mistral-large-latest",
            messages=[
                {"role": "system", "content": "You are an expert Python programmer. Output only code, no explanations."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        code = response.choices[0].message.content.strip()
        
        # Clean markdown
        if "```python" in code:
            code = code.split("```python")[1].split("```")[0].strip()
        elif "```" in code:
            code = code.split("```")[1].split("```")[0].strip()
        
        return code
    except Exception as e:
        print(f"    Error: {e}")
        return None

def main():
    repo_root = Path(__file__).parent
    
    # Load prompt template
    prompt_file = repo_root / "llm-codegen/prompts/test_driven_refinement.txt"
    prompt_template = prompt_file.read_text()
    
    # Load problems
    data_dir = repo_root / "llm-codegen/data"
    problems = sorted(data_dir.glob("*.json"))
    
    print("="*60)
    print("Part 3: Innovation Strategy - Test-Driven Refinement")
    print("="*60)
    print(f"\nGenerating for {len(problems)} problems with both families...")
    print()
    
    for data_file in problems:
        problem_data = json.loads(data_file.read_text())
        problem_id = problem_data["problem_id"]
        function_name = problem_data["function_name"]
        description = problem_data["description"]
        
        print(f"[{problem_id}] {function_name}")
        
        # Generate with Gemini
        print("  - Gemini...", end=" ")
        code = generate_with_gemini(problem_id, description, function_name, prompt_template)
        if code:
            output_dir = repo_root / f"llm-codegen/generations/{problem_id}/gemini/test_driven_refinement"
            output_dir.mkdir(parents=True, exist_ok=True)
            (output_dir / "test_driven_refinement_sample1.py").write_text(code, encoding='utf-8')
            print("✓")
        else:
            print("✗")
        
        time.sleep(1)
        
        # Generate with Mistral
        print("  - Mistral...", end=" ")
        code = generate_with_mistral(problem_id, description, function_name, prompt_template)
        if code:
            output_dir = repo_root / f"llm-codegen/generations/{problem_id}/mistral/test_driven_refinement"
            output_dir.mkdir(parents=True, exist_ok=True)
            (output_dir / "test_driven_refinement_sample1.py").write_text(code, encoding='utf-8')
            print("✓")
        else:
            print("✗")
        
        time.sleep(1)
    
    print("\n" + "="*60)
    print("✓ Innovation strategy generation complete!")
    print(f"✓ Generated 20 files (10 problems × 2 families)")
    print("\nNext: Evaluate with results_part3.csv")
    print("python llm-codegen\\eval\\run_eval.py --results llm-codegen\\eval\\results_part3.csv")
    print("="*60)

if __name__ == "__main__":
    main()

