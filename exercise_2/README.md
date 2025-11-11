# Exercise 2: Automated Testing & Coverage

This directory contains scripts and tools for measuring code coverage, improving tests through iterative generation, and evaluating fault detection capabilities.

## Structure

```
exercise_2/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── part1_baseline_coverage.py        # Part 1: Baseline coverage measurement
├── part2_llm_test_generation.py     # Part 2: Iterative test improvement
├── part3_fault_detection.py         # Part 3: Fault detection evaluation
└── results/                          # Generated results and reports
    ├── baseline_coverage.csv        # Part 1 results
    ├── improved_tests/               # Generated test files
    ├── llm_improvement_*.json       # Part 2 iteration results
    └── fault_detection_results.json  # Part 3 results
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. (Optional) Set up API keys for test generation:
```bash
# For automated test generation
set GEMINI_API_KEY=your_key_here

# Or alternative API
set MISTRAL_API_KEY=your_key_here
```

## Usage

### Part 1: Baseline Coverage (30%)

Measure baseline coverage for all Exercise 1 solutions:

```bash
python part1_baseline_coverage.py
```

This will:
- Measure line and branch coverage for all problems
- Generate `results/baseline_coverage.csv` with coverage metrics
- Print a summary table

**Output**: CSV file with columns:
- `problem_id`, `function_name`
- `line_coverage`, `branch_coverage` (percentages)
- `tests_passed`, `tests_total`
- `interpretation` (one-line analysis)

### Part 2: Iterative Test Generation (50%)

Improve tests iteratively through automated test generation:

```bash
python part2_llm_test_generation.py
```

This will:
- Select 2 problems with room for improvement (based on coverage gap)
- Generate additional tests iteratively
- Continue until convergence (3 iterations with <3% improvement)
- Save improved test files and iteration results

**Output**:
- `results/improved_tests/{problem_id}/test_iter{N}.py` - Test files for each iteration
- `results/llm_improvement_{problem_id}.json` - Coverage metrics per iteration

### Part 3: Fault Detection (20%)

Test if improved tests catch injected bugs:

```bash
python part3_fault_detection.py
```

This will:
- Inject realistic bugs (off-by-one, wrong boundary, etc.) into solutions
- Run tests against buggy code
- Report whether bugs were caught

**Output**:
- `results/buggy_solutions/{problem_id}/` - Buggy code and descriptions
- `results/fault_detection_results.json` - Test results

## Workflow

1. **Run Part 1** to establish baseline:
   ```bash
   python part1_baseline_coverage.py
   ```

2. **Run Part 2** to improve tests:
   ```bash
   python part2_llm_test_generation.py
   ```

3. **Run Part 3** to verify fault detection:
   ```bash
   python part3_fault_detection.py
   ```

4. **Generate Report**: Use the results to create your PDF report with:
   - Baseline coverage table (from Part 1)
   - Test generation prompts and before/after coverage (from Part 2)
   - Fault detection analysis (from Part 3)

## Results Interpretation

### Coverage Metrics

- **Line Coverage**: Percentage of code lines executed by tests
- **Branch Coverage**: Percentage of conditional branches tested (more important)

### Convergence Criteria (Part 2)

Tests converge when: `Coverage(i) - Coverage(i-2) <= 3%` for 3 consecutive iterations.

### Fault Detection (Part 3)

A good test suite should:
- Catch injected bugs (off-by-one, wrong operators, missing checks)
- Have high branch coverage (uncovered branches may hide bugs)

## Notes

- All scripts assume Exercise 1 is in `../exercise_1/`
- Coverage reports are generated in HTML/XML format by pytest-cov
- Test files are preserved at each iteration for reproducibility
- Buggy solutions are saved for inspection

## Troubleshooting

**Coverage is 0%**: 
- Check that solution files are being found
- Verify test files exist and are compatible
- Check pytest-cov installation

**Test generation fails**:
- Verify API keys are set (if using automated generation)
- Check internet connection
- Script will fall back to mock generation for testing

**Tests don't catch bugs**:
- This is expected for some cases - analyze why
- Check if the bug affects tested code paths
- Consider if branch coverage is sufficient


