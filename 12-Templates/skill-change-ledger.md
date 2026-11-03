---
type: template
name: Skill change ledger
status: active
tags: [template, skills, evals, self-improvement]
related: ["[[self-improvement-evidence-ledger]]", "[[approval-record]]", "[[agent-testing]]"]
---

# Skill change ledger — <skill>

One row per proposed change to a user-level skill (`~/.agents/skills/<skill>/SKILL.md`).
The versioned copy lives in `06-Skills/authored/<skill>/SKILL.md`; its git history is the rollback.
This ledger is an index of evidence, not an authorization source (see [[approval-record]]).

## <proposal-id> — <one-line hypothesis>

| Field | Value |
|---|---|
| Baseline | path + SHA-256 of the live skill |
| Candidate | scratch path + SHA-256 (never live until approved) |
| Hypothesis | the specific behavior the change should produce |
| Lessons addressed | inbox lines (`00-Inbox/skill-lessons/<skill>.md`, date + summary) |
| Cases | case IDs from `06-Skills/evals/<skill>.md`, marked dev / held-out |
| Evaluator | `scripts/skill_eval_snapshot.py` + the suite's graders |
| Evidence | per case: result line, bounded excerpt, snapshot RESULT line |
| Baseline vs candidate | per-case pass/fail for both; missing runs listed as missing |
| Independent verification | who/what checked it (not the author), and the result |
| Decision | promote / revise / reject / hold |
| Authority | reference to the user's exact-content yes |
| Rollback | previous version's git commit or file hash |
| Outcome | later observations: new lessons, regressions, or no signal (recorded, not assumed good) |
| Limitations | what was not tested |

Rules: a missing, failed or skipped required check blocks promotion; a safety-case failure blocks
promotion regardless of other results; a candidate never edits its own suite, the eval tool,
the scanner, or any rules file.

Records: save each independent review verbatim as `06-Skills/ledger/<skill>-review-<n>.md` and
link it from its row; put per-case evidence (compare RESULT lines, adjudicated processes, bounded
TEST TRACE excerpts) in `06-Skills/ledger/evidence/<proposal-id>.md`. A result without a
matching evidence entry counts as missing.
