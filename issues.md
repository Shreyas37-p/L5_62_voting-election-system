# Lab 5: Static Code Analysis — Issue Log

**Program:** `election_system.py`  
**Scope:** Issues identified in the original version before fixes. Line numbers refer to that original version and may shift if the source is edited.

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---:|---|---|
| Hidden bidirectional Unicode character in role check | Security — High | 21–22 | The `isOfficer()` condition contains a bidirectional Unicode control character. This makes the displayed condition misleading and can cause the role check to behave differently from what a reader expects. Pylint reported `bidirectional-unicode` (E2502). | Remove the hidden control character and compare the role directly with a clear, explicit officer-role constant. The corrected function returns `False` for a normal `"voter"` role. |
| Unsafe XML parsing for postal ballots | Security — High | 7, 74–83 | Postal-ballot XML is parsed from input with `xml.dom.pulldom`. Parsing untrusted XML without hardened protections can expose the program to XML-related attacks, and the import path does not adequately validate ballot fields. | Replace the parser with `defusedxml.ElementTree`, catch specific parsing/input exceptions, and validate voter IDs and candidate names before accepting a ballot. |
| Hard-coded administrative password | Security — High | 8 | A password is stored directly in the source code. Anyone who can read the code can discover it; changing the password also requires editing the program. | Do not embed real credentials in source control. Load secrets from a protected configuration or environment variable and use an appropriate authentication design. Remove the unused hard-coded password if admin authentication is not implemented by this program. |
| MD5 used to hash voter IDs | Security — Medium | 16 | MD5 is a weak cryptographic hash and hashing a voter ID this way does not provide authentication or meaningful protection for the identifier. | Remove the unnecessary hash field. If the application needs authentication or protected identifiers, use a design suitable for that purpose rather than MD5. |
| A voter can vote more than once | Logic — High | 26–37 | `castVote()` checks whether the voter exists but does not reject a voter whose `voted` flag is already true. The demo therefore accepts Ben's second vote. | Check the voter's `voted` flag before recording a ballot. Mark the voter as having voted only after a valid ballot is accepted. |
| Poll-closing check permits votes after 18:00 | Logic — High | 26–37 | The original code checks only `when.hour > POLLS_CLOSE_HOUR`, so a time such as 18:30 passes when the closing hour is 18. | Compare the full time with a defined closing time using `>=`, so a vote at or after 18:00 is rejected. |
| Vote percentage can divide by zero | Reliability — Medium | 51–52 | `votePercent()` divides by the number of ballots without checking whether any ballots exist. Calling it before the first vote raises `ZeroDivisionError`. | Return `0.0` when there are no ballots; otherwise calculate the percentage using floating-point division. |
| Turnout percentage can exceed 100% | Logic — High | 54–55 | Turnout is calculated using the number of ballots divided by the number of registered voters. Duplicate or otherwise invalid ballots can make turnout inaccurate or greater than 100%. | Calculate turnout from the number of registered voters marked as having voted, divided by the number of registered voters. Handle an empty voter list. |
| Announcements all show the same candidate | Logic — Medium | 65–69 | The original code stores lambdas inside a loop. Each lambda uses the loop variable after the loop has finished, so the messages can all refer to the last candidate. | Build announcement strings directly in the loop/list comprehension, or bind the current candidate when creating each callback. |
| Bare `except` hides import errors | Reliability / Maintainability — Medium | 74–83 | The postal-import code catches every exception and silently passes. This can hide malformed input and programming errors, making failures difficult to diagnose. | Catch specific exceptions, reject invalid ballot records explicitly, and return an import count only for validated ballots. |
| Candidate names are not normalized consistently | Logic — Medium | 26–37, 74–83 | Candidate matching is case-sensitive in the original flow, so values such as `"bob"` and `"Bob"` can be treated as different candidates. | Validate candidates against the official candidate list using case-insensitive lookup, then store the canonical candidate name. |
| Minimum-age boundary rejects an eligible 18-year-old | Logic — Medium | 16–18 | The original condition uses `age > 18`, which rejects someone who is exactly 18 even though the demonstration and usual minimum-age rule treat 18 as eligible. | Accept the minimum age by rejecting only ages below 18, and add a boundary test for age 18. |
| Code-style and maintainability findings | Code Quality — Low | Multiple lines | Pylint and Flake8 reported unused imports/variables, missing docstrings, non-snake-case function names, trailing whitespace, long lines, and spacing violations. | Remove unused imports and variables, use snake_case names, add docstrings, remove trailing whitespace, and follow standard Python spacing and line-length conventions. |

## Verification after fixes

The corrected `election_system.py` was run successfully with the test cases in `main()`. The observed output showed that the age-18 voter could register, a plain `voter` role was not treated as an officer, duplicate voting was rejected, `bob` was normalized to `Bob`, a vote at 18:30 was rejected, turnout was 75.0%, and announcements were generated for each candidate.

| Tool | Final result |
|---|---|
| Pylint | **10.00/10** |
| Bandit | **No issues identified** (0 low, 0 medium, 0 high) |
| Flake8 | **No violations reported** (no output) |

*Note: a clean static-analysis report reduces known risks but does not prove that a program has no bugs or security vulnerabilities.*
