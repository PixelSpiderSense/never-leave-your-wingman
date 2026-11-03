---
name: second-review
description: Provide an additional evidence-based review of code, documents, or plans when a second opinion or independent review is requested.
---

# Second Review

Use the existing reviewer role. Review the artifact before seeing
earlier reviewers' conclusions, to reduce anchoring.

1. Identify the artifact or revision, intended behavior, acceptance
   criteria, and authorized inspection scope.
2. Use one separate reviewer context when delegation is available
   and authorized. Honor the user's model choice; otherwise inherit
   the host default. Give it the artifact, requirements, and relevant
   context without the maker's or previous reviewer's conclusions.
3. Request findings with severity, exact location, supporting evidence,
   likely consequence, and a suggested correction or verification.
   Review correctness, omissions, boundaries, and regressions.
4. Compare the returned findings with earlier reviews. Verify material
   disagreements against the artifact rather than counting votes.
5. Return confirmed findings, unresolved concerns, checks performed,
   and a verdict: ready, changes required, or unverified.

Use read-only tools or sandboxing where supported. A review request
does not authorize edits, installations, commits, or external messages.
Run checks only within the existing authorization.

If delegation is unavailable, report that limitation and provide a
clearly labeled self-review; never claim independent review occurred.
A separate context using the same model does not establish model diversity.

Complete one review pass. Do not automatically launch repeated reviews
or additional workers. Return findings in chat; saved records follow
the vault's existing approval rules.
