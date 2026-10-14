# Lab 5: Static Code Analysis — Reflection

> **Note:** The separate handout containing the instructor's exact four reflection questions was not included with the lab instructions shared here. The following are four relevant reflection responses for this exercise. If the separate handout uses different questions, update these headings to match it before submitting.

## 1. What problems did you find in the original program, and how did you fix them?

The original program had both code-quality issues and functional bugs. An invisible bidirectional Unicode character made the officer-role condition misleading. The program accepted a second vote from the same voter, allowed a vote at 18:30 even though polls closed at 18:00, and could calculate an incorrect turnout percentage. Candidate names were handled inconsistently by case, and the announcement lambdas could all display the same candidate. There were also unsafe XML-import practices, a hard-coded password, an unnecessary MD5 hash, a possible division-by-zero error, a bare `except`, unused imports and variables, missing docstrings, and style violations.

I corrected the role check, added duplicate-vote prevention, compared against the full poll-closing time, normalized candidate names, corrected turnout calculation, guarded percentage calculations when no votes exist, generated announcement strings without the loop-closure bug, hardened XML parsing with `defusedxml`, and improved exception handling and code style.

## 2. What is the difference between Pylint, Flake8, and Bandit?

Pylint checks general code quality, including naming, documentation, unused variables, and common programming problems. In this run, it gave the corrected code a score of **10.00/10**. Flake8 checks style and common errors such as unused imports, whitespace, indentation, and line length; it reported no violations after the fixes. Bandit looks for common security-related coding patterns. It reported **no issues identified** in the corrected file. The tools overlap in some areas, but each has a different emphasis, so using all three provides broader feedback than using only one.

## 3. Did the tools identify every bug? Why or why not?

No. Static-analysis tools inspect source code for patterns and potential problems, but they do not automatically understand every intended business rule. For example, whether a voter aged exactly 18 should be accepted, whether 18:30 is after the closing time, whether duplicate voting is rejected, whether case variants should represent the same candidate, and whether turnout can exceed 100% are best confirmed by running the program with meaningful test cases. This lab showed why tool reports should be combined with manual code review and execution-based testing.

## 4. What did you learn from this exercise?

I learned that a program can run without crashing and still produce incorrect or misleading results. I also learned to treat warnings as useful evidence rather than merely trying to silence them: hidden Unicode can obscure logic, poor input validation can affect security, and a small condition or closure bug can change election results. Running the program first helped expose behavior problems, while Pylint, Bandit, and Flake8 helped identify maintainability and security concerns. Finally, rerunning the tools after making changes provided a repeatable way to check whether the reported issues had been addressed.
