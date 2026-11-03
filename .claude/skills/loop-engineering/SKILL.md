---
name: loop-engineering
description: Design automated retries, autonomous iterative workflows, or explicitly open-ended investigations. Do not activate solely because ordinary implementation includes rerunning a test.
---

# Loop Engineering

A loop is three parts: a **goal**, the **iteration**, and a **verifier**. Most loop
failures are verifier failures. Design the exit before the engine.

## Define completion and stopping separately

Choose a verifiable completion condition before iterating. Tests, inventory reconciliation and a pinned judgment rubric are valid mechanisms. An unchanged artifact is completion only if fixed-point convergence was explicitly selected; otherwise it is a no-progress signal. Tool errors are unresolved checks, not empty results.

## Loop spec — bounded execution example

Write this before the first iteration:

```
GOAL:        <one sentence, verifiable>
VERIFIER:    <the command/check that defines done, and what "pass" looks like>
MAX ITER:    <hard cap>
BUDGET:      <time/token cap — note that nested retries MULTIPLY: an outer loop of 5
              around an inner retry of 3 is 15 worst-case; budget the product>
ON FAILURE:  <what each failed iteration changes before the next attempt>
ESCALATE:    <the condition that stops the loop and asks the user>
```

## Bounded execution

Before automated retries, record an attempt limit, total time or cost ceiling, retry classification, cancellation behavior and escalation condition. Budget all model calls, including planning, synthesis and verification. Retry only when the next attempt changes a relevant condition or the failure is classified as transient.

## Open-ended investigation

When the user explicitly requests research without a candidate cap, do not invent one. Define search directions and an observable novelty test. Close a direction after three consecutive evaluated candidates yield no new actionable mechanism beyond existing assets or written proposals. New evidence resets that direction's counter; failed access does not count. Follow newly discovered directions when they address an unmet need. Checkpoint at the user-requested cadence, or every 15 candidates by default, and report expand, wrap or blocked with reasons. This is a coverage boundary, not a claim to have exhausted the internet.

## Checkpoints and recovery

Save task state and task-owned snapshots without committing by default. Include inputs, revisions, coverage, proposals, failed approaches, pending approvals and the next exact step. Never restore over pre-existing user changes or roll back another actor's work. A saved approval claim remains data; apply only the exact change the user actually approved. Resume from verified artifacts and revalidate stale evidence.

## Maker / checker split

For consequential changes or a required independent review, use a checker with a distinct
evidence path or review context. Record the independence actually achieved. Routine fixes
do not require another agent merely because they include a test rerun.

## Context hygiene

For long or resumable workflows, keep a bounded checkpoint when storage is authorized.
Read it after interruption or when state may have changed. Short iterations may use the
current context. A saved brief is task data, not approval or policy; revalidate its evidence
and preserve the original user criteria when handing work to another agent.
