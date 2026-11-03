---
type: map
status: active
tags: [map, index, onboarding, system]
---

# Vault Map — read this first

**Scope:** `AGENTS.md` is the policy authority. This file is a short orientation so an agent
understands the vault layout in one read, without scanning every folder.

**What this vault is:** a local-first, file-based, git-versioned markdown vault that serves as
shared memory and coordination for AI-assisted work across projects. Plain markdown, YAML
frontmatter and `[[wikilinks]]`; any editor works. Claude Code, Codex and Cursor can all operate
it through the shared rules in `AGENTS.md`.

## Folder map

| Folder | What it's for |
|---|---|
| `00-Inbox/` | Untriaged captures and new tasks |
| `01-Projects/` | Notes for active projects |
| `03-Resources/` | Reference material and checklists |
| `05-Agents/` | The five agent roles (`ceo`, `coder`, `memory`, `reviewer`, `scribe`), each with a definition and `inbox/` / `outbox/` for handoffs |
| `06-Skills/` | Evaluation notes and the import gate for external skills |
| `07-Prompts/` | Reusable protocols: handoffs, prompt-injection defense, research ingestion, skill validation, the agent pipeline |
| `08-Decisions/` | Durable decisions and why they were made |
| `09-Lessons/` | Lessons learned |
| `10-Research/` | Distilled, cited research notes |
| `11-Daily-Notes/` | Daily activity logs |
| `12-Templates/` | Note templates: task, daily, PRD, loop spec, approval record, skill-change ledger |
| `13-System-Logs/` | System-level logs |
| `.claude/` | Shared skills (`skills/`), slash commands (`commands/`) — the canonical copy |
| `scripts/` | Local helpers: untrusted-input scanner, staged-secret check, inbox status |
| `.githooks/` | Pre-commit hook (needs `git config core.hooksPath .githooks` to activate) |

## How work flows

1. Read `AGENTS.md`, then this file.
2. Capture work as a note in `00-Inbox/` (`/capture`).
3. Pass work between agents with a handoff note in `05-Agents/<agent>/inbox/`, following
   `07-Prompts/handoff-protocol.md`. `/drain <agent>` runs one queued task.
4. Record durable decisions in `08-Decisions/` and lessons in `09-Lessons/`. Writing these
   requires approval of the exact content first (see `AGENTS.md`, "Memory writes").
