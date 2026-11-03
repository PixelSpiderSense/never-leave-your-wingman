---
type: index
name: Skill Library
status: active
tags: [skill, index]
---

# 06-Skills — Skill Library Index

Evaluation notes for external skills, plugins and agent frameworks. Evaluation and activation
are distinct states: evaluating a skill never authorizes installing or running it.

- Canonical authored skills live in `.claude/skills/` (see the routing table in `AGENTS.md`).
- Clone candidate source into a staging folder outside the vault, record the repository URL and
  commit SHA, and screen it with `scripts/scan_untrusted.py` before reading it in bulk.
- Score candidates against [[EVALUATION_CHECKLIST]]. Write one evaluation note per candidate in
  this folder, with a verdict: adopt, adopt-with-modifications, borrow-only, or reject.
- Use the `skill-import` skill to prepare an adoption or borrowing proposal.
