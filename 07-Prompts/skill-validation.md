---
type: protocol
status: proposed
tags: [skills, evaluation, verification]
related: ["[[EVALUATION_CHECKLIST]]", "[[harness-evals]]"]
---

# Skill validation

Use this protocol when proposing a skill change. It describes checks, not permission to edit or execute a candidate.

## Static checks

Read the complete SKILL.md and enumerate its referenced files. Check that name and description are present, the name matches its kebab-case directory, and local references resolve inside the intended skill tree. Report missing files, invalid frontmatter, unknown fields and read errors separately. Compare the eight local skill directories with the index; an unexplained mismatch is a finding.

Inspect optional scripts, manifests, hooks and tool permissions before enabling them. Metadata correctness is not a safety verdict. Do not fetch remote links as part of routine local validation. Record files inspected and omissions.

## Behavioral cases

Use the following initial positive and negative cases. Keep every available skill, including the target, in both candidate catalogs.

| Target | Positive case | Negative case |
|---|---|---|
| debugging | Checkout fails only after a specific state transition; investigate cause | Rename a heading with no reported defect |
| reverse-engineering | Explain why a branch exists using implementation and history | Implement an already specified branch |
| loop-engineering | Define success and convergence for a repeated repair task | Answer a single stable factual question |
| agent-testing | Compare an agent change against a frozen baseline | Run a deterministic formatter on one file |
| prompt-engineering | Revise a prompt and test its output contract | Edit ordinary report prose |
| scope-creep-detector | Review all tracked and untracked changes against the stated task | Summarize a clean repository with no change review requested |
| research-distill | Turn screened source evidence into a cited proposal | Apply a fully approved local typo correction |
| skill-import | Evaluate a candidate skill and its activation risks | Use an already approved local skill on its normal task |

These are seed cases, not measured results. Add realistic paraphrases and near-neighbor tasks before grading routing. Unknown labels and malformed responses are errors, not correct negatives.

## Comparison record

Freeze the case set, source revisions and scoring rules before running a comparison. Run the same cases with and without the proposed skill under comparable model and tool conditions. Reserve held-out cases. Separate run errors, missing outputs and skipped cases from failures and passes. Zero completed cases is an error. Report paired denominators, task quality, forbidden-action attempts, latency and cost when available. A safety-critical failure blocks activation regardless of average quality.

For subjective outputs, use a rubric with examples and a reviewer who has not seen the candidate's self-assessment. Record disagreement instead of silently averaging it away. Repeat stochastic cases enough to expose variability; do not infer a universal benefit from one successful trace.

## Decision record

Record proposal ID and version, baseline and candidate hashes, runtime and model, cases attempted/completed, raw evidence locations, limitations and verdict. A passing record makes the change reviewable; only the user's separate approval authorizes applying the specified change.
