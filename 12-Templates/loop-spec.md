---
created: "{{date:YYYY-MM-DD HH:mm}}"
type: loop-spec
status: active
project: 
owner: 
tags: [loop-spec, automation]
related: ["[[agent-pipeline]]", "[[loop-engineering]]", "[[prd]]", "[[frameworks-reharvest-2026-08-10]]"]
---

# <Task name> — Loop Spec

> For an iterative or autonomous task (agent runs the steps itself until the goal is met).
> Write GOAL + VERIFY + STOP-WHEN **before** you hit go. From [[loop-engineering]].

```
GOAL: <measurable end state — e.g. "every test in /tests/X passes, lint clean">

EACH ITERATION:
  1. run the check and read every failure
  2. pick the single highest-impact failure
  3. write the smallest change that fixes it
  4. re-run the check (tests / lint / type-check)

VERIFY: <green tests + zero lint warnings + zero type errors>

STOP WHEN: verify passes, OR <N> iterations reached, OR budget/time ceiling hit,
           OR no-progress (same call + same args twice)
           OR <M> consecutive iterations with no measurable progress
           OR 3 failed fixes on the same failure (architecture breaker)

ON STOP: summarize what changed and what still fails — never discard silently
```

## Run controls

- Mode: bounded execution or explicitly open-ended research
- Completion verifier and pass rule:
- No-progress metric and consecutive threshold:
- Attempt limit and time/cost ceiling for bounded execution:
- Search directions and novelty rule for open-ended research:
- Checkpoint cadence:
- Cancellation and external wait behavior:
- Retryable failures and what changes before retry:
- Protected writes awaiting approval:

## At the cap — adjudicate or block, never discard
When a brake fires, exactly one of these happens, in writing:
- **Adjudicate** — a written ruling: what was attempted, why it is being parked, what would
  unblock it. Park it in `## Resume state` below.
- **BLOCKED** — escalate to a human with the same information.

A completion condition, convergence signal, user stop, permission boundary or budget limit can legitimately stop work. Record which fired. Only the completion verifier establishes completed; convergence reports the investigated scope and remaining frontier. A blocked or partial run must not masquerade as success.

## Data-pipeline loops — hard accounting block
For any loop touching an ETL / import / re-pull, VERIFY must reconcile counts, not just exit 0.
A pipeline that processes zero files exits 0 happily ([[2026-08-03-repull-must-force-reload-or-data-freezes]]).
Report every line, every run:

```
files discovered:      N
files processed:       N        (must equal discovered, or name the skipped ones and why)
rows read (raw):       N
rows written (derived):N
rows rejected:         N        (+ where they went — never silently dropped)
remaining tail:        N        (unprocessed backlog; 0 means caught up)
runtime:               Ns
manifest count == table max timestamp?   yes/no
```

Two separate questions, both required — conflating them hides staleness:
- **Backfill status** — is the historical load complete?
- **Live-tail freshness** — is *today's* data present? A complete backfill with a frozen tail
  looks healthy on row counts alone.

Skip-unchanged work by **content hash** (SHA-256 of the file → `{hash}.json` marker), not by
mtime; treat a corrupt marker as a cache miss, never as a hit. (ECC `data-throughput-accelerator`,
`content-hash-cache-pattern`)

## Ceremony scales to blast radius
Match the loop's overhead to the change's size — full ceremony on a one-line fix is waste, and
skipping research on a schema migration is negligence. State which tier this run is:
- **trivial** (typo, constant) → make the change, verify, done. No PRD, no research pass.
- **small** (one function, no interface change) → verify + review.
- **standard** (multi-file, or any interface change) → full [[agent-pipeline]].
- **large** (schema, migration, security boundary, money/pricing path) → full pipeline + a
  second independent reviewer.
Security review is mandatory regardless of tier when the change touches: auth, user input, DB
queries, filesystem paths, external APIs, crypto, secrets, or **pricing**. (ECC `orch-pipeline`)

## Resume state

- Input and source revisions:
- Completed criteria and evidence paths:
- Candidates processed and per-direction novelty counters:
- Current artifact hashes:
- Pending proposal IDs and approval references:
- Failed approaches and why:
- Deferred work and concrete reopen triggers:
- Next exact step:

Checkpoint task-owned state without committing unless the user asks. Validate the saved state against current files when resuming.

## Run log
- **{{date:YYYY-MM-DD HH:mm}}** — spec created
