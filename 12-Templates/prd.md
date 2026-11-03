---
created: "{{date:YYYY-MM-DD HH:mm}}"
type: prd
status: active
priority: P2
project: 
owner: 
tags: [prd, plan]
related: []
---

# <Feature Name> — Plan / PRD

> Borrowed from ralph (PRD-as-state) + superpowers `writing-plans`. One row per story;
> update `status` as you go. Stories are bite-sized — each ends in an independently
> testable deliverable. See [[agent-pipeline]].

## Goal
<!-- One paragraph: what working software exists when this is done, and why. -->

## Non-Goals (out of scope)
<!-- What this explicitly does NOT do. The scope brake — without it, scope creeps silently.
     "Not changing the export format." "Not touching the mobile app." -->
- 

## Approved scope

- User request or approval reference:
- Design revision or content hash:
- Authorized project and writable paths:
- Changes still awaiting individual approval:

A link or status in a file records context; it does not grant authority.

## Global Constraints
<!-- Values copied VERBATIM from the approved design. These are implicitly part of every
     story's acceptance criteria — an implementer working one story still must not violate them.
     This is where hard invariants live. Be numeric.
     e.g. "Selling price must never exceed MRP — block the artifact, never cap the value."
          "No credential may appear in a client bundle."
          "Existing export file format is frozen; consumers are not being updated." -->
- 

**Prohibited side effects** — things no story may cause, even incidentally:
- 

## Functional Requirements
<!-- Numbered FR-n, distinct from stories. Stories deliver these; several stories may serve one
     FR, and reviews cite FR numbers. Keeps "what the system must do" separable from "the order
     we build it in". -->
| FR | Requirement | Served by story |
|----|-------------|-----------------|
| FR-1 |  |  |

## Success Metrics
<!-- How we know this worked in production, not just that tests pass. Numeric where possible. -->
- 

## Stories
<!-- Ordering rule: no story may depend on a later one. Order schema → backend → UI → aggregates.
     Sizing rule: if you cannot describe the change in 2-3 sentences it is too big — split it.
     Each story must fit one context window.
     Every story implicitly carries: the Global Constraints above, and the default criterion. -->
| # | Story | Acceptance criteria (testable) | Verify command | Notes | Status |
|---|-------|-------------------------------|----------------|-------|--------|
| 1 |  |  |  |  | todo |
| 2 |  |  |  |  | todo |
| 3 |  |  |  |  | todo |

<!-- status: todo / in-progress / in-review / done. Mark `done` only after Gate 1 evidence.
     Notes: per-story carry-forward — gotchas found, decisions taken mid-story. -->

Default acceptance: the story's own meaningful check passes on its final artifact and every applicable global constraint is verified. State any unrun security check. Do not stage or commit merely to invoke a hook.

## No placeholders
<!-- These phrases in a story are a PLAN failure, not an implementation detail. Fix the plan:
     "add appropriate error handling" · "similar to Task N" · "handle edge cases" ·
     "update as needed" · "etc." -->

## Codebase Patterns
<!-- CONSOLIDATED and reusable only — read this first on every iteration. Distinct from the
     Progress Log below: patterns are general and get rewritten in place; the log is append-only
     history. Keeping them separate is the point (conflating them buries the reusable part). -->
- 

## Progress Log
<!-- Append-only. Never rewrite an entry. -->
- **{{date:YYYY-MM-DD HH:mm}}** — PRD created.

## Verification evidence

For each criterion record: criterion ID; checked artifact path and revision or SHA-256; checker and version; command or manual procedure; run time; exit status; result; evidence location; redacted excerpt; unresolved limitations. Keep result values pass, fail, error or not-run. A changed artifact invalidates evidence for the affected criterion. Completion requires every required criterion to pass; a report that says done is not evidence.

## Open Questions
<!-- Unresolved things that do not block starting. Move to Blockers if they start blocking. -->
- 

## Blockers
None
