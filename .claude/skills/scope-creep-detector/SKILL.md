---
name: scope-creep-detector
description: Compare a diff against its stated one-line intent before committing or opening a PR. Use before any commit/PR that touches more than one file, or whenever a change feels bigger than what was asked.
---

# Scope Creep Detector

A diff either serves its stated intent, or it doesn't — every changed file falls into one
of three buckets: **keep** (clearly serves the intent), **split** (unrelated, belongs in
its own commit/PR), or **justify** (borderline — needs one line explaining why it's here).
Silently letting "while I was in there" changes ride along is how small PRs become
unreviewable ones.

## Workflow

1. **State the intent in one sentence** before running the diff — "fix the null check in
   the pricing calculator," not "various fixes." If you can't state it in one sentence,
   the work itself may need splitting first.
2. Record the baseline status and the intended comparison: unstaged, staged or a named revision. Inventory tracked changes and untracked paths separately. The current helper reports aggregate changed lines per file; it does not inspect hunks, classify intent or cover untracked files. Report those limits until its replacement is approved.
3. Inspect and classify every changed file against the intent, not just large files. Use keep, split or justify. A file can contain both relevant and unrelated hunks; record their boundaries. Inspect binary files with a suitable artifact viewer or mark them unverified. Never infer ownership from being present in the working tree.
4. Propose a split when needed. Do not stash, move, reset or discard pre-existing or another actor's changes without specific permission. After an authorized split or a change to scope, repeat the comparison and reconcile the inventory.

## Rules of thumb

- The threshold is total additions plus deletions per file. Crossing it prompts a size explanation; it is not a hunk-size measurement or a correctness result.
- "I was already in the file" is not an intent — if the file's real change doesn't serve
  the stated one-liner, it's a split candidate regardless of proximity.
- This is a pre-commit discipline, not a blocking gate — per `AGENTS.md`'s Coding
  behavior → Surgical changes, every changed line should trace to the request; this
  script just makes that traceable mechanically instead of by memory.
