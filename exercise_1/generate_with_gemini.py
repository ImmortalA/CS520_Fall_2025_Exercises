"""
Generate solutions using Gemini API for all 10 HumanEval+ problems.

Usage:
1. Get API key from https://aistudio.google.com/app/apikey
2. Set environment variable: set GEMINI_API_KEY=your_key_here
3. Run: python generate_with_gemini.py
"""
import os
import json
import time
from pathlib import Path

def main():
    # Check for API key
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY environment variable not set!")
        print("\nSteps:")
        print("1. Get API key from: https://aistudio.google.com/app/apikey")
        print("2. In CMD: set GEMINI_API_KEY=your_key_here")
        print("3. Run this script again")
        return
    
    try:
        import google.generativeai as genai
    except ImportError:
        print("ERROR: google-generativeai not installed")
        print("Run: pip install google-generativeai")
        return
    
    # Configure Gemini
    genai.configure(api_key=api_key)
    # Use the latest stable flash model (fast and free)
    model = genai.GenerativeModel('models/gemini-2.5-flash')
    
    # Load prompt templates
    repo_root = Path(__file__).parent
    cot_template = (repo_root / "llm-codegen/prompts/cot_generic.txt").read_text()
    scot_template = (repo_root / "llm-codegen/prompts/scot_generic.txt").read_text()
    
    # Process each problem
    data_dir = repo_root / "llm-codegen/data"
    problems = sorted(data_dir.glob("*.json"))
    
    print(f"Generating solutions for {len(problems)} problems...")
    print("="*60)
    
    for data_file in problems:
        problem_data = json.loads(data_file.read_text())
        problem_id = problem_data["problem_id"]
        function_name = problem_data["function_name"]
        description = problem_data["description"]
        
        print(f"\n[{problem_id}] {function_name}")
        
        # Generate CoT
        print("  - Generating CoT...")
        cot_prompt = f"{cot_template}\n\nProblem:\n{description}\n\nFunction name: {function_name}\n\nIMPORTANT: Output ONLY the function implementation code. No explanations, no markdown."
        
        try:
            response = model.generate_content(cot_prompt)
            code = response.text.strip()
            
            # Clean up markdown if present
            if "```python" in code:
                code = code.split("```python")[1].split("```")[0].strip()
            elif "```" in code:
                code = code.split("```")[1].split("```")[0].strip()
            
            # Save CoT
            cot_dir = repo_root / f"llm-codegen/generations/{problem_id}/gemini/cot"
            cot_dir.mkdir(parents=True, exist_ok=True)
            (cot_dir / "cot_sample1.py").write_text(code, encoding="utf-8")
            print("    ✓ Saved to cot_sample1.py")
            
            time.sleep(2)  # Rate limiting
            
        except Exception as e:
            print(f"    ✗ Error: {e}")
        
        # Generate SCoT
        print("  - Generating SCoT...")
        scot_prompt = f"{scot_template}\n\nProblem:\n{description}\n\nFunction name: {function_name}\n\nIMPORTANT: Output ONLY the function implementation code. No explanations, no markdown."
        
        try:
            response = model.generate_content(scot_prompt)
            code = response.text.strip()
            
            # Clean up markdown if present
            if "```python" in code:
                code = code.split("```python")[1].split("```")[0].strip()
            elif "```" in code:
                code = code.split("```")[1].split("```")[0].strip()
            
            # Save SCoT
            scot_dir = repo_root / f"llm-codegen/generations/{problem_id}/gemini/scot"
            scot_dir.mkdir(parents=True, exist_ok=True)
            (scot_dir / "scot_sample1.py").write_text(code, encoding="utf-8")
            print("    ✓ Saved to scot_sample1.py")
            
            time.sleep(2)  # Rate limiting
            
        except Exception as e:
            print(f"    ✗ Error: {e}")
    
    print("\n" + "="*60)
    print("✓ Generation complete!")
    print(f"✓ Generated 20 files (10 problems × 2 strategies)")
    print("\nNext step: Generate solutions using ChatGPT-5 browser")
    print("See INSTRUCTIONS.md for details")

if __name__ == "__main__":
    main()

