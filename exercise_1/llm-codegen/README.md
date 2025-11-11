# LLM Code Generation Evaluation

This directory contains the core implementation for evaluating LLM code generation strategies.

## Structure

- **data/**: HumanEval+ problem specifications (10 selected problems)
- **prompts/**: Prompt templates for CoT, SCoT, self-repair, and innovation strategies
- **generations/**: Generated code solutions organized by problem/family/strategy
- **tests/**: Test cases for each problem
- **eval/**: Evaluation harness and results

## Key Files

- `eval/run_eval.py`: Main evaluation script
- `eval/harness.py`: Test execution utilities
- `eval/results*.csv`: Complete evaluation results
- `prompts/*.txt`: All prompt templates used in the study