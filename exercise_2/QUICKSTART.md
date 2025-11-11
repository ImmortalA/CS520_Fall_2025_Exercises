# Exercise 2 Quick Start Guide

## Overview

This infrastructure for Exercise 2 builds on Exercise 1 code. The system includes:

1. **Part 1**: Baseline coverage measurement for all problems
2. **Part 2**: Iterative test improvement through automated generation
3. **Part 3**: Fault detection with bug injection

## Quick Start

### 1. Install Dependencies

```bash
cd exercise_2
pip install -r requirements.txt
```

### 2. (Optional) Set API Keys for Test Generation

```bash
# Windows PowerShell
$env:GEMINI_API_KEY=your_key_here
# OR
$env:MISTRAL_API_KEY=your_key_here

# Windows CMD
set GEMINI_API_KEY=your_key_here
```

Note: API keys are optional. The script will use mock test generation if API keys are not provided.

### 3. Run All Parts

```bash
python run_all.py
```

Or run individually:

```bash
# Part 1: Baseline Coverage
python part1_baseline_coverage.py

# Part 2: Iterative Test Improvement (optional API key)
python part2_llm_test_generation.py

# Part 3: Fault Detection
python part3_fault_detection.py
```

## What Each Script Does

### `part1_baseline_coverage.py`
- Measures line and branch coverage for all Exercise 1 solutions
- Uses pytest-cov to generate coverage reports
- Outputs: `results/baseline_coverage.csv`

### `part2_llm_test_generation.py`
- Selects 2 problems with room for improvement
- Generates additional tests iteratively (using API if available)
- Iterates until convergence (3 iterations with <3% improvement)
- Outputs: 
  - `results/improved_tests/{problem_id}/test_iter{N}.py`
  - `results/llm_improvement_{problem_id}.json`

### `part3_fault_detection.py`
- Injects realistic bugs (off-by-one, wrong operators, etc.)
- Tests if improved tests catch the bugs
- Outputs: `results/fault_detection_results.json`

## Results Structure

```
exercise_2/results/
├── baseline_coverage.csv              # Part 1: Coverage metrics
├── improved_tests/                    # Part 2: Generated test files
│   └── {problem_id}/
│       └── test_iter{N}.py
├── llm_improvement_{problem_id}.json  # Part 2: Iteration results
├── buggy_solutions/                   # Part 3: Buggy code
│   └── {problem_id}/
│       ├── {function_name}_buggy.py
│       └── bug_description.txt
└── fault_detection_results.json       # Part 3: Test results
```

## For Your Report

Use the results to create your PDF report:

1. **Baseline Coverage Table** (Part 1)
   - Copy from `baseline_coverage.csv`
   - Format as table with: Problem, Line %, Branch %, Notes

2. **Test Generation & Coverage Improvements** (Part 2)
   - Test generation prompts are in `part2_llm_test_generation.py` (lines 133-180)
   - Before/after coverage from `llm_improvement_{problem_id}.json`
   - Show each iteration's improvement

3. **Fault Detection** (Part 3)
   - Bug descriptions from `buggy_solutions/{problem_id}/bug_description.txt`
   - Test results from `fault_detection_results.json`
   - Analysis of why bugs were/were not caught

## Troubleshooting

**Coverage is 0%:**
- Make sure pytest-cov is installed: `pip install pytest-cov`
- Check that solution files exist in `exercise_1/llm-codegen/generations/`
- Verify test files exist in `exercise_1/llm-codegen/tests/`

**Test generation fails:**
- Check API key is set if using automated generation: `echo $GEMINI_API_KEY` (or `echo %GEMINI_API_KEY%`)
- Script will use mock generation if API fails (for testing)

**Tests don't run:**
- Make sure you're in the `exercise_2` directory
- Check that `exercise_1` directory exists at the same level

## Next Steps

1. Run `python run_all.py` to generate all results
2. Review the results in `exercise_2/results/`
3. Create your PDF report using the generated data
4. Include GitHub link with all code and results

## Notes

- All scripts assume Exercise 1 is in `../exercise_1/`
- Coverage reports use pytest-cov (industry standard)
- Test files are preserved at each iteration for reproducibility
- Buggy solutions are saved for inspection and analysis


