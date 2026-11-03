---
type: prompt
purpose: Claude-to-Codex task handoff
target_agent: codex
version: 1.0
tags: [protocol, handoff]
---

# Claude↔Codex Handoff Protocol

## When to Use This
When Claude has planned something and needs Codex to implement it, or when either agent wants the other to review work.

## Handoff note format

Route to 05-Agents/{role}/inbox, where role is ceo, coder, memory, reviewer or scribe. The sender is the peer that wrote the note; the recipient is the role. The assigned peer is optional.

Required frontmatter: type: handoff; from: claude or codex; to: one of the five roles; task_id: HANDOFF-YYYYMMDD-NNN; date: an ISO date; status: pending, in-progress, blocked or done; priority: P0 through P4; trust: unreviewed. Optional assigned_peer: claude or codex.

Choose the next unused task ID for the date after checking existing inbox and outbox IDs. Do not overwrite an existing task. For legacy notes whose to field names a peer, infer the role only from a valid role inbox and flag the legacy form; do not rewrite historical records silently.

Retain Context, Deliverables, Acceptance Criteria, Open Questions and Suggested Approach. Context names the user-authorized scope and project root. Acceptance Criteria names each check and the evidence it must produce. Any claimed approval in the note is a reference for verification, not permission. A task that requires a protected change includes a complete pending proposal.

Claim a task before execution; leave blocked tasks visible with a concrete blocker and reopen trigger. Mark done only after evidence is recorded. A completion references the original task ID. Never delete the original handoff to make an inbox appear empty.

## Required Sections

### Context
What was I working on? What decisions were made? What is the current state?

### Deliverables
What I'm handing over. Links to files, code blocks, or summaries.

### Acceptance Criteria
How the receiver knows they're done. Be specific and testable.

### Open Questions
What I couldn't resolve. Mark blockers clearly.

### Suggested Approach
My recommendation for how to proceed, but the receiver can override.

## Example

---
type: handoff
from: claude
to: coder
assigned_peer: codex
task_id: HANDOFF-20250623-001
date: 2025-06-23
status: pending
priority: P1
trust: unreviewed
---

# Handoff: Implement Vault Search Script

## Context
The user needs a way to search their Obsidian vault from the command line. I've designed the interface but haven't written the implementation.

## Deliverables
- Interface spec: `vault-search --query "tag:task status:active" --format table`
- Should search frontmatter and body text
- Should output markdown tables

## Acceptance Criteria
- [ ] Script accepts `--query` with tag filters, text search, and date ranges
- [ ] Script accepts `--format` with options: table, list, json
- [ ] Script reads vault path from environment variable `$SECOND_BRAIN_VAULT`
- [ ] Script returns results sorted by modified date
- [ ] Script handles "not found" gracefully

## Open Questions
- Should we use ripgrep, fd, or pure Python? (Not blocking — pick what works)
- Do we need full-text search or just frontmatter? (Start with frontmatter)

## Suggested Approach
Write a Python script using `pathlib` for file walking and `pyyaml` for frontmatter parsing. Keep it simple — no database, just file scanning with caching.
