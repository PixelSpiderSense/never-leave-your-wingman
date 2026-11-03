---
type: readme
status: active
tags: [prompts, system]
created: "2026-06-24"
---

# 07-Prompts

This folder holds **reusable prompts, protocols, and workflows** — the parameterized
instructions the OS runs again and again. Each file is a stable procedure referenced
from across the vault (e.g. `CLAUDE.md` points here for cross-agent handoffs).

## What goes here
- Reusable protocols and named-stage workflows (e.g. `handoff-protocol.md`, `agent-pipeline.md`)
- Prompts meant to be parameterized and invoked repeatedly, not run once

## What does not
- One-off task notes → `00-Inbox/`
- Fill-in note structures (PRD, loop-spec) → `12-Templates/`

## Naming
Use kebab-case `.md` filenames named for the protocol, e.g. `handoff-protocol.md`.
