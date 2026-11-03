---
description: Capture a decision, lesson, or research note into the SecondBrain vault
argument-hint: <what happened, in plain language>
---

Resolve the SecondBrain vault from the active project context or an explicitly configured vault root. Confirm that the resolved directory contains its AGENTS.md and MAP.md before drafting a destination; do not use another user's hard-coded home path.
This works from any project — the vault is the cross-project memory.

The raw capture is: **$ARGUMENTS**

(If `$ARGUMENTS` is empty, ask the user one line: "What do you want to capture?" then proceed.)

## Step 1 — Triage: is this worth keeping?
Only **durable decisions, lessons, and research** belong in the vault. If what they described
is trivia, a routine edit, or something obvious from git history or the code itself, say so and
ask whether to skip it. Don't auto-write noise.

**The test:** would this change a future decision? If not, don't write it.

**Dedup BEFORE writing.** Grep `08-Decisions/`, `09-Lessons/`, and `10-Research/` for the topic
first. If a note already covers it, **update that note** — add the new evidence, bump the date,
note what changed. A near-duplicate is worse than nothing: it splits the record, so future
searches find the weaker copy. Say which existing note you checked.

**Capture the pattern, not the diary.** A note that says "X broke on Tuesday and I fixed it" is
useless in six months. A reusable note names three things:
- **Trigger** — the recognizable condition under which this recurs
- **Mechanism** — why it happened, not just what happened
- **Rule** — what to do differently, stated so it can be followed without this note's context

If you can't state the trigger, it's probably a diary entry — ask whether to skip it.

## Step 2 — Classify
Pick exactly one type. If genuinely ambiguous, ask one quick question; otherwise just decide and proceed.

- **decision** — a choice was made (X over Y, with reasons). → `08-Decisions/`
- **lesson** — something went wrong + the fix / how to avoid it next time. → `09-Lessons/`
- **research** — findings worth keeping from investigation/reading. → `10-Research/`

## Step 3 — Gather context
- **Date:** today's date as `YYYY-MM-DD` (from the environment).
- **Project:** infer from the current working directory / git repo name. Add it as a tag and,
  if a matching note exists under `01-Projects/`, link it in `related`.
- **Filename slug:** short kebab-case from the title.
  - decision → `08-Decisions/YYYY-MM-DD-<slug>.md`
  - lesson   → `09-Lessons/YYYY-MM-DD-<slug>.md`
  - research → `10-Research/<slug>.md`  *(no date prefix — matches existing research notes)*

## Step 4 — Propose the note

Synthesize the entire note in the existing format. For an existing note, show the exact diff instead. Show its final vault path and any separately proposed cross-link or superseding edit. Wait for the user's explicit yes to each protected change before writing. A capture request starts drafting; it does not approve unseen wording.

**decision:**
```
---
type: decision
status: decided
date: "YYYY-MM-DD"
decision: "<one-line summary of the choice>"
tags: [decision, <project>, <topic>]
related: []
---

# Decision: <title>

## Context
## Options considered
<!-- REQUIRED: every option that was genuinely on the table, each with why it was rejected.
     A decision without its rejected alternatives can't be re-litigated later — only repeated.
     If only one option was considered, say so explicitly; that's itself worth knowing. -->
## Decision
## Rationale
## Revisit if
```

`status` lifecycle: `decided` → `deprecated` | `superseded`. When a later decision replaces this
one, **edit the old note** to add `superseded_by: "[[new-note]]"` and set `status: superseded` —
never leave two live notes disagreeing. Check for a note this one supersedes before writing.

**lesson:**
```
---
type: lesson
status: captured
date: "YYYY-MM-DD"
lesson: "<one-line summary of what to remember>"
tags: [lesson, <project>, <topic>]
related: []
---

# Lesson: <title>

## What happened
## Root cause
## Fix
## How to avoid next time
```

**research:**
```
---
type: research
name: <Title Case name>
status: active
date: "YYYY-MM-DD"
sources: []
tags: [research, <topic>]
related: []
---

# <title>

<distilled findings>
```

After approval, check that the target still matches the reviewed baseline, then apply only the approved content. If it changed, show the revised diff for a fresh approval. Report saved only after the write succeeds; otherwise report draft awaiting approval. Do not commit or modify the user's global installed copy as a side effect.
