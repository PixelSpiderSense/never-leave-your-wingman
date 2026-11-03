---
name: skill-import
description: Evaluate an external skill, plugin, or agent framework and prepare a bounded adoption or borrowing proposal. Evaluation does not authorize installation, execution, registration, or protected writes.
---

# Skill Import

Run a candidate third-party skill/framework through the vault's import gate. This encodes
the workflow already applied 9 times (see the table in `06-Skills/README.md`). The default
verdict is **borrow, don't adopt** — most candidates should end as a study note, not a clone.

## Procedure

1. Check the skill index, previous evaluation notes and harvest ledger. Record overlap and a specific reason to reopen an existing candidate. Prefer improving an existing vault asset to importing a competing agent fleet.
2. Stage a no-execution inspection copy in a clone staging folder outside the vault. Record the repository URL and commit SHA before extracting files. Do not execute installers, setup scripts, hooks, package lifecycle scripts or candidate tests during evaluation. Do not delete existing clones or strip their provenance as part of a study.
3. Inventory execution surfaces: skill instructions, referenced scripts, plugin manifests, convention-loaded hooks and agents, MCP definitions and startup files. Screen every file selected for reading with the vault scanner, including extensions omitted by its directory filter. Preserve scan receipts and manually adjudicate findings.
4. Apply EVALUATION_CHECKLIST to the proposed activation surface. Use pass, fail or unknown per item; unknown is not a pass. State the inspected scope and runtime tests not performed. A score never overrides a security veto, missing license permission or user approval.
5. Draft one evaluation note in the previous format with source revision, read files and lines, scanner findings, checklist, verdict, what to borrow, what not to borrow and concrete follow-up. Re-express ideas; copy no source code. For a full application, compare data boundaries, execution, dependencies, export path and actual vault need instead of pretending it is a skill.
6. Draft exact proposed skill content and any index changes as separately reviewable items. Wait for each required yes before activation, configuration changes or durable-memory writes. Borrow-only means no installation and no live registration. Report pending approvals separately from completed research.
