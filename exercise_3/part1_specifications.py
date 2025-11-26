"""
Exercise 3 - Part 1: Generate, Evaluate, and Refine Specifications
This file contains the formal specifications generated for the two selected problems.
"""

# Problem 1: humaneval_54 - same_chars function
print("="*80)
print("PROBLEM 1: humaneval_54 - same_chars")
print("="*80)

print("\nProblem Description:")
problem_1_description = """
Check if two words have the same characters.
>>> same_chars('eabcdzzzz', 'dddzzzzzzzddeddabc')
True
>>> same_chars('abcd', 'dddddddabc')
True
>>> same_chars('dddddddabc', 'abcd')
True
>>> same_chars('eabcd', 'dddddddabc')
False
>>> same_chars('abcd', 'dddddddabce')
False
>>> same_chars('eabcdzzzz', 'dddzzzzzzzddddabc')
False
"""
print(problem_1_description)

print("\nMethod Signature:")
print("def same_chars(s0: str, s1: str) -> bool")

print("\nLLM Prompt for Specifications:")
prompt_1 = """
Problem description: Check if two words have the same characters.
Method signature: def same_chars(s0: str, s1: str) -> bool

Please write formal specifications as Python assertions that describe the correct behavior of this method.
Let 'res' denote the expected return value of 'same_chars(s0, s1)'.
Do not call 'same_chars()' in your assertions.
Do not use methods with side effects such as print, file I/O, random number generation, or timing functions.
Express the relationship between 's0', 's1', and 'res' using pure set operations, string operations, and boolean logic only.
Generate about 5 meaningful specifications.
"""
print(prompt_1)

print("\nGenerated Specifications (Before Correction):")
generated_specs_1 = [
    "assert res == (set(s0) == set(s1))  # Result equals whether both strings have same unique characters",
    "assert (len(set(s0)) == 0 and len(set(s1)) == 0) == (res and s0 == '' and s1 == '')  # Both empty strings return True",
    "assert (len(set(s0)) == 1 and len(set(s1)) == 1 and list(set(s0))[0] == list(set(s1))[0]) == (res and len(set(s0 + s1)) == 1)  # Single same character case",
    "assert (set(s0).isdisjoint(set(s1))) == (not res and len(set(s0)) > 0 and len(set(s1)) > 0)  # Disjoint non-empty sets return False",
    "assert (set(s0).issubset(set(s1)) and set(s1).issubset(set(s0))) == res  # Mutual subset relationship equals result"
]

for i, spec in enumerate(generated_specs_1, 1):
    print(f"{i}. {spec}")

print("\nEvaluation of Generated Specifications:")
evaluations_1 = [
    {"spec_num": 1, "status": "Correct", "explanation": "Directly captures the core logic - same unique characters"},
    {"spec_num": 2, "status": "Incorrect", "explanation": "Overly complex and contains redundant conditions. The empty string case is already covered by spec 1."},
    {"spec_num": 3, "status": "Incorrect", "explanation": "Uses list(set()) which can have undefined order, and the logic is unnecessarily complex for single character case."},
    {"spec_num": 4, "status": "Incorrect", "explanation": "Logic is inverted - disjoint sets should return False, but the assertion structure is confusing."},
    {"spec_num": 5, "status": "Correct", "explanation": "Mutual subset relationship is equivalent to set equality, correctly captures the behavior."}
]

for eval_item in evaluations_1:
    print(f"Spec {eval_item['spec_num']}: {eval_item['status']} - {eval_item['explanation']}")

accuracy_1 = 2 / 5  # 2 correct out of 5
print(f"\nAccuracy Rate: {accuracy_1:.1%} (2/5)")

print("\nCorrected Specifications:")
corrected_specs_1 = [
    "assert res == (set(s0) == set(s1))  # Result equals whether both strings have same unique characters",
    "assert (s0 == '' and s1 == '') == (res and len(set(s0)) == 0 and len(set(s1)) == 0)  # Both empty strings return True",
    "assert (len(set(s0)) == 1 and len(set(s1)) == 1 and set(s0) == set(s1)) == (res and len(set(s0 + s1)) == 1)  # Single same character case",
    "assert (len(set(s0)) > 0 and len(set(s1)) > 0 and set(s0).isdisjoint(set(s1))) == (not res)  # Disjoint non-empty sets return False",
    "assert (set(s0).issubset(set(s1)) and set(s1).issubset(set(s0))) == res  # Mutual subset relationship equals result"
]

for i, spec in enumerate(corrected_specs_1, 1):
    print(f"{i}. {spec}")

print("\n" + "="*80)
print("PROBLEM 2: humaneval_10 - make_palindrome")
print("="*80)

print("\nProblem Description:")
problem_2_description = """
Find the shortest palindrome that begins with a supplied string.
Algorithm idea is simple:
- Find the longest postfix of supplied string that is a palindrome.
- Append to the end of the string reverse of a string prefix that comes before the palindromic suffix.
>>> make_palindrome('')
''
>>> make_palindrome('cat')
'catac'
>>> make_palindrome('cata')
'catac'
"""
print(problem_2_description)

print("\nMethod Signature:")
print("def make_palindrome(string: str) -> str")

print("\nLLM Prompt for Specifications:")
prompt_2 = """
Problem description: Find the shortest palindrome that begins with a supplied string.
Algorithm idea is simple:
- Find the longest postfix of supplied string that is a palindrome.
- Append to the end of the string reverse of a string prefix that comes before the palindromic suffix.

Method signature: def make_palindrome(string: str) -> str

Please write formal specifications as Python assertions that describe the correct behavior of this method.
Let 'res' denote the expected return value of 'make_palindrome(string)'.
Do not call 'make_palindrome()' in your assertions.
Do not use methods with side effects such as print, file I/O, random number generation, or timing functions.
Express the relationship between 'string' and 'res' using pure string operations and boolean logic only.
Generate about 5 meaningful specifications.
"""
print(prompt_2)

print("\nGenerated Specifications (Before Correction):")
generated_specs_2 = [
    "assert res.startswith(string)  # Result must start with the input string",
    "assert res == res[::-1]  # Result must be a palindrome",
    "assert len(res) >= len(string)  # Result length must be at least input length",
    "assert string == '' or len(res) <= 2 * len(string)  # Result length bounded by twice input length",
    "assert (string == string[::-1]) == (res == string)  # If input is palindrome, result equals input"
]

for i, spec in enumerate(generated_specs_2, 1):
    print(f"{i}. {spec}")

print("\nEvaluation of Generated Specifications:")
evaluations_2 = [
    {"spec_num": 1, "status": "Correct", "explanation": "The result must always start with the input string by definition."},
    {"spec_num": 2, "status": "Correct", "explanation": "The result must be a palindrome by definition."},
    {"spec_num": 3, "status": "Correct", "explanation": "The result cannot be shorter than the input string."},
    {"spec_num": 4, "status": "Correct", "explanation": "Upper bound is reasonable - at most we append the reverse of the entire string."},
    {"spec_num": 5, "status": "Incorrect", "explanation": "This is incorrect based on the actual implementation. Even if input is a palindrome, the implementation may still append characters."}
]

for eval_item in evaluations_2:
    print(f"Spec {eval_item['spec_num']}: {eval_item['status']} - {eval_item['explanation']}")

accuracy_2 = 4 / 5  # 4 correct out of 5
print(f"\nAccuracy Rate: {accuracy_2:.1%} (4/5)")

print("\nCorrected Specifications:")
corrected_specs_2 = [
    "assert res.startswith(string)  # Result must start with the input string",
    "assert res == res[::-1]  # Result must be a palindrome",
    "assert len(res) >= len(string)  # Result length must be at least input length",
    "assert string == '' or len(res) <= 2 * len(string)  # Result length bounded by twice input length",
    "assert string == '' or len(res) == len(string) + len([c for i, c in enumerate(string) if not string[i:] == string[i:][::-1]][:1] if string else [])  # Length relationship based on palindromic suffix"
]

# The last specification is complex, let's simplify it
corrected_specs_2[4] = "assert (string == '') == (res == '')  # Empty input produces empty result"

for i, spec in enumerate(corrected_specs_2, 1):
    print(f"{i}. {spec}")

print("\n" + "="*80)
print("SUMMARY")
print("="*80)
print(f"Problem 1 (same_chars) - Accuracy: {accuracy_1:.1%}")
print(f"Problem 2 (make_palindrome) - Accuracy: {accuracy_2:.1%}")
print(f"Overall Accuracy: {(accuracy_1 + accuracy_2) / 2:.1%}")