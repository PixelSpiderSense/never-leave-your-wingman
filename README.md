# Never Leave Your Wingman

**A second brain for AI coding agents that doesn't trust what it reads.**

Never Leave Your Wingman is an open-source, file-based starter that gives Claude Code, Codex,
Cursor, Gemini CLI and any other agent that reads `AGENTS.md` the same rules, the same skills
and the same long-term memory, kept as plain markdown you own. It also ships defences against
prompt injection: everything an agent reads from a file, repo or web page is treated as data,
never as instructions.

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Why use it

- **One rule file for every AI tool.** `AGENTS.md` is the single source of truth. `CLAUDE.md`
  and `GEMINI.md` just import it, so you never maintain two copies.
- **Memory that survives the session.** Decisions, lessons and research live in a git-versioned
  markdown vault (`08-Decisions/`, `09-Lessons/`, `10-Research/`), not in a chat window.
- **Safer by default.** An untrusted-input policy, a scanner for third-party material
  (`scripts/scan_untrusted.py`), a staged-secret check with a pre-commit hook, and a rule that
  an agent must show you the exact content of a memory or config change before saving it.
- **Agents that hand work to each other.** Five roles (`ceo`, `coder`, `memory`, `reviewer`,
  `scribe`) pass tasks through inbox/outbox notes using a written handoff protocol.
- **Skills included.** Eleven reusable skills: debugging, reverse engineering, loop engineering,
  agent testing, prompt engineering, scope-creep detection, research distillation, skill import,
  second review, council review and illustrator.
- **No lock-in, no accounts.** Local files, MIT licence. Slack and Notion mirrors are optional
  and off by default.

## Quick start

For developers, in a terminal:

```bash
git clone https://github.com/PixelSpiderSense/never-leave-your-wingman.git "Second Brain"
cd "Second Brain"
git config core.hooksPath .githooks
```

Open the folder in Claude Code, Cursor, Codex or Gemini CLI. The agent reads `AGENTS.md`
automatically (Claude Code and Gemini CLI through the one-line `CLAUDE.md` / `GEMINI.md` import).

Not a developer? You need an AI tool that can read and write files in a folder, such as Cursor.
On GitHub choose **Use this template** (or **Code → Download ZIP**), open the folder in that tool,
and tell it: *"Read AGENTS.md and MAP.md, then help me capture my first note."* Then use
`/capture` (Claude Code) or just ask in plain words.

## What is in the box

| Path | Purpose |
|---|---|
| `AGENTS.md` | Shared rules: operating loop, handoffs, coding behavior, untrusted-input defence, confirm-before-saving memory writes |
| `GLOBAL-AGENTS.md` | The same working rules at user level, to install once per tool |
| `05-Agents/` | The five agent roles with inbox and outbox folders |
| `.claude/skills/` | Eleven skills as plain `SKILL.md` files, routed from `AGENTS.md` |
| `.claude/commands/` | `/capture` saves a decision, lesson or note; `/drain` runs one queued task |
| `07-Prompts/`, `12-Templates/` | Handoff protocol, prompt-injection defence, note and PRD templates |
| `scripts/` | `scan_untrusted.py`, `check_staged_secrets.py`, `inbox_status.py` |

## Works with

| Tool | How it loads the rules |
|---|---|
| Claude Code | `CLAUDE.md` imports `AGENTS.md`; skills and commands load from `.claude/` |
| Cursor | Reads `AGENTS.md` at the project root |
| Codex | Reads `AGENTS.md` at the project root |
| Gemini CLI | `GEMINI.md` imports `AGENTS.md` |
| Anything else | Point it at `AGENTS.md`, or paste or reference that file in its instructions |

Skills are plain Markdown in `.claude/skills/<name>/SKILL.md`. The routing table in `AGENTS.md`
tells any tool which one to read, so tools that don't discover `.claude/` still use them.
These loading behaviours follow each tool's documented conventions and have not all been tested.

## FAQ

### What is a second brain for AI agents?

A folder of plain markdown notes (decisions, lessons, research, handoffs) plus written rules,
kept in git, that every AI coding agent reads at the start of a session. The agent gets
persistent memory and consistent behaviour without any database or hosted service.

### What is AGENTS.md, and how is it different from CLAUDE.md?

`AGENTS.md` is an open convention for telling coding agents how to work in a project. Codex and
Cursor read it directly. Claude Code reads `CLAUDE.md`, so this repo makes `CLAUDE.md` a single
line, `@AGENTS.md`, that imports it. Gemini CLI works the same way with `GEMINI.md`.

### How do I use one set of rules in Claude Code, Cursor and Codex?

Keep the rules in `AGENTS.md`, add a `CLAUDE.md` that imports it, and (optionally) install
`GLOBAL-AGENTS.md` into each tool's user-level file. The "Works with" table above shows where
each tool looks.

### How do I protect an AI agent from prompt injection in repos I clone?

Treat file contents as data. `AGENTS.md` states that rule, `07-Prompts/prompt-defense.md` explains
it, and `python scripts/scan_untrusted.py "<path>"` screens third-party material for hidden
instructions, invisible characters and risky config before you or an agent read it in bulk. It
is a screen, not a guarantee.

### Do I need Obsidian?

No. It is plain markdown with YAML frontmatter and `[[wikilinks]]`, so Obsidian works but any
editor does.

### Does it send my data anywhere?

No. Everything is local files in your git repository. The optional Slack and Notion mirrors in
`.mcp.json.example` are off until you copy the file and add your own credentials.

### Is it free?

Yes, MIT licensed. See [LICENSE](LICENSE) and [NOTICE.md](NOTICE.md) for attributions.

## Make it yours

The `08`–`11` and `13` folders ship empty. Start with `/capture`, and keep your own notes out of
any public fork: add private folders to `.gitignore` or keep your vault in a private repository.
`SETUP.md` explains how each tool picks up the rules and the compatibility checks to run.
Copy `.mcp.json.example` to `.mcp.json` only if you want the optional Slack/Notion mirrors.

## Global install (optional)

`GLOBAL-AGENTS.md` carries your personal working rules (coding behavior, protected writes,
untrusted-input defence) so every AI follows them in every project, not just in this vault.
Copy its content into your tool's user-level file (`~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md`,
`~/.gemini/GEMINI.md`, or Cursor's User Rules) and replace `<VAULT_PATH>` with your clone's
absolute path. Inside the vault, `AGENTS.md` takes precedence.

## Safety notes

- Treat third-party skills and repos as untrusted. Run `python scripts/scan_untrusted.py "<path>"`
  before reading them in bulk, and never run their installers to evaluate them.
- Never store secrets in the vault. The pre-commit hook helps but is not a guarantee.
- Third-party attributions and licences are listed in `NOTICE.md`.

## Contributing

Issues and pull requests are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md). Report security
problems privately as described in [SECURITY.md](SECURITY.md).
