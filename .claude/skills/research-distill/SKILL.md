---
name: research-distill
description: Prepare a cited research-note proposal when the user asks to distill sources into the vault. Do not activate for ordinary summaries or source material merely judged worth keeping.
---

# Research Distill

Turn source material into a `10-Research/` note in the vault's established distill style.
This encodes the workflow already used for `loop-engineering`, `evals-for-ai-agents`,
`building-effective-agents`, `agent-loops-vs-dags-sgh`, `claude-skills-curation-critique`,
and `claude-customer-stories` — match those notes, don't invent a new shape.

## Procedure

1. Identify the exact sources and check existing notes for overlap. For repository material, record the revision and file paths. Screen staged third-party files with the vault scanner before bulk reading; explicitly account for files the directory scan omits. Read the source relevant to each claim and record any unread or inaccessible portion.
2. Separate facts, source claims, inferences and unknowns. Verify quantitative claims against primary evidence or label them unverified. Do not substitute marketing, popularity or a generated summary for implementation evidence.
3. Write a complete proposed note in the task's review-artifact location. Include YAML fields type, name, status, date, trust: unreviewed, sources, tags and related; retain the vault's established topic-oriented body and end with Takeaway for this vault. Each actionable takeaway names a target asset and proposed change; otherwise explain why no change is needed.
4. Show the final destination path and entire note, or the exact diff for an existing note. List cross-link or MAP changes separately. Wait for an explicit yes for each protected write. The research request and a prior note's approval do not approve a different note or policy change.
5. Apply only approved content after confirming the source file has not changed. Report the actual written path and verification. If approval is pending, report draft ready rather than saved. Follow-up actions remain proposals.

When conversion is needed, follow [[research-ingestion]] after that protocol is independently approved. Until then, record the converter, settings, source locations, partial results and resource limits directly in the draft evidence record.

## Rules
- One note per coherent topic; two thin sources on the same topic → one note (the existing
  notes merge 2–3 sources each).
- If the material is trivia or duplicates an existing research note, say so and stop —
  update the existing note instead of creating a near-duplicate.
- Follow-up actions discovered while distilling go into the note as a checklist (see
  `loop-engineering.md` "Follow-up — ACTIONED"), not silently executed.
