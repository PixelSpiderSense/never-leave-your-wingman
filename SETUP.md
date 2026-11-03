---
type: reference
status: active
tags: [setup, system, codex, cursor]
created: "2026-06-24"
---

# Working in this vault

Open the cloned vault root as the project folder in Cursor, or start Codex from that root. The tools must already be installed and authenticated, and their normal workspace trust requirements still apply. The repository provides the project instructions and shared skill content; there is no vault-specific installation, persona-pasting or global skill-copy step for these two tools.

## Project instructions and skills

`AGENTS.md` is the shared entry point. It directs the agent to `MAP.md`, the handoff protocol, relevant assignments and the shared skill files. Codex's persona is read by Codex as directed there. Preserve the actual identity of an agent using Cursor.

Keep `.claude/skills/` as the single source for the eight authored skills. The task routing table in `AGENTS.md` tells any agent which complete `SKILL.md` to read with its normal file tools. A skill's script may need an interpreter for the particular task; reading Markdown does not require running that script or installing its dependencies.

Current official Cursor documentation describes automatic loading of root `AGENTS.md` and compatibility discovery of `.claude/skills/`. Current Codex documentation describes native repository discovery under `.agents/skills/`; this vault uses the explicit `AGENTS.md` routing table for its existing location. File-based consultation does not promise that these skills appear in Codex's native skill selector.

No `.cursor/rules/` pointer is required by the documented root-file convention. Do not mirror the complete shared rules or skill bodies into `.mdc` files. Add a narrowly scoped adapter only after a reproducible loading failure shows that one is needed and the user approves its exact content.

These loading claims concern agent work. They do not establish equivalent rule handling in Cursor Tab completion, Inline Edit, Bugbot, remote workspaces or every product version.

## Compatibility checks for maintainers

These are acceptance checks after a loader change or tool upgrade, not setup steps for every user or every session.

- Verify the root entry files and all routed skill paths exist in the checkout and in the tracked Git tree. An untracked local file cannot satisfy a fresh-clone requirement.
- Inspect Codex's assembled prompt using its supported diagnostic when available. Confirm the complete root `AGENTS.md` is present. Check both the ordinary profile and an isolated profile without custom global instructions; do not retain private prompt contents.
- In a fresh Cursor Agent chat with this vault as the opened root, inspect the applied rule sources for `AGENTS.md` and the skill inventory for the eight project skills. Then use a task-shaped debugging request without naming a skill, and verify that the debugging body is consulted before work proceeds. A model's unsupported claim that it loaded a file is not proof.
- For Codex, use the same task-shaped request after the routing change and observe the read of `.claude/skills/debugging/SKILL.md`. Its absence from the native selector is not a failure of file-based routing.
- Record tool version, checkout revision, root, profile conditions, actual observations and remaining limitations. Test a trivial question as well: it should not load all eight skills.

The 2026-09-06 audit verified root instruction assembly in Codex CLI 0.153.4 with both current and isolated profiles. Cursor 3.19.7 was installed and the repository layout matched the official convention; live Cursor rule and skill activation remained unverified. Behavior after any proposed routing change requires a new check.

## Git and security checks

`AGENTS.md` requires explicit user authorization for commits. Opening this vault does not authorize automatic commits, pushes, hook installation or Git configuration changes.

The versioned `.githooks/pre-commit` file is present, but a fresh clone does not inherit another checkout's local `core.hooksPath` setting. Hook activation is a separate, explicitly approved Git configuration action; platforms that enforce executable bits also need a usable executable hook. Never report a hook as active from file presence alone.

Before bulk reading third-party material, run the vault's `scripts/scan_untrusted.py` through an available Python interpreter, using the resolved vault root and an explicit target. A hook only checks commit-time inputs and cannot replace this read-time screen. If the interpreter or check is unavailable, report the limitation and do not treat it as a clean result.

## Optional integrations and interface features

The following are not prerequisites for Cursor or Codex to consult the vault:

- Obsidian Templater: select `12-Templates` as the template folder. If desired, map `11-Daily-Notes` to `12-Templates/daily-note.md` and `00-Inbox` to `12-Templates/task-note.md`, then verify a new note uses the intended template.
- Obsidian Dataview: enable inline queries if useful; leave JavaScript queries off unless deliberately needed and reviewed.
- Obsidian QuickAdd: an optional Inbox Task capture can create `00-Inbox/{{DATE:YYYYMMDD-HHmmss}}-{{VALUE}}.md` from `12-Templates/task-note.md`.
- Obsidian Git: configure backup behavior only after the user explicitly chooses it. Do not assume automatic commits or remote synchronization are authorized.
- Slack and Notion: the example configuration files document optional mirrors. File-based work succeeds without connected accounts or credentials.
- Claude Code commands: canonical project copies live under `.claude/commands/`. A user-level copy is an optional convenience for other projects, not a requirement for this vault or a bootstrap mechanism for Cursor or Codex.
- Claude Desktop project instructions: manual persona setup belongs to that separate product workflow; it is not a prerequisite for the tools above.

Use an available interpreter for scripts and report missing prerequisites for the specific operation. Do not assume another machine's Python alias or home directory.
