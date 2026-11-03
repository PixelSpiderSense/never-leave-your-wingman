# Never Leave Your Wingman

A file-based "second brain" starter for AI-assisted work: a markdown vault with shared agent
rules, five agent roles with file-based handoffs, a set of reusable skills, and safety scripts
that treat everything an agent reads as data, not instructions. It works with any agent that
reads `AGENTS.md`, including Claude Code, Codex, Cursor and Gemini CLI, from the same checkout.

## What you get

- `AGENTS.md` — shared rules: operating loop, handoffs, coding behavior, untrusted-input
  defense, and confirm-before-saving memory writes. `CLAUDE.md` and `GEMINI.md` just import it.
- `GLOBAL-AGENTS.md` — the same working rules at user level, to install once per tool (below).
- `05-Agents/` — `ceo`, `coder`, `memory`, `reviewer` and `scribe` roles with inbox/outbox folders.
- `.claude/skills/` — eleven skills: debugging, reverse engineering, loop engineering, agent
  testing, prompt engineering, scope-creep detection, research distillation, skill import,
  second review, council review, illustrator.
- `.claude/commands/` — `/capture` (save a decision, lesson or research note) and `/drain`
  (run one task from an agent's inbox).
- `07-Prompts/` and `12-Templates/` — handoff protocol, prompt-injection defense, note templates.
- `scripts/` — `scan_untrusted.py` (screen third-party material), `check_staged_secrets.py`,
  `inbox_status.py`. `.githooks/pre-commit` runs the secret check at commit time.

## Install

There is no package yet; this is a template you clone and make your own.

```bash
git clone https://github.com/PixelSpiderSense/never-leave-your-wingman.git "Second Brain"
cd "Second Brain"
git config core.hooksPath .githooks
```

Then open the folder in your AI tool. `SETUP.md` explains how each tool picks up the rules and
skills. Copy `.mcp.json.example` to `.mcp.json` only if you want the optional Slack/Notion
mirrors; nothing depends on them.

## Works with

| Tool | How it loads the rules |
|---|---|
| Claude Code | `CLAUDE.md` imports `AGENTS.md`; skills and commands load from `.claude/` |
| Cursor | Reads `AGENTS.md` at the project root |
| Codex | Reads `AGENTS.md` at the project root |
| Gemini CLI | `GEMINI.md` imports `AGENTS.md` |
| Anything else | Point it at `AGENTS.md`. If it has no file convention, paste or reference that file in its instructions. |

Skills are plain Markdown in `.claude/skills/<name>/SKILL.md`. The routing table in `AGENTS.md`
tells any tool which one to read, so tools that don't discover `.claude/` still use them.
These loading behaviours follow each tool's documented conventions and have not all been tested.

## Global install (optional)

`GLOBAL-AGENTS.md` carries your personal working rules (coding behavior, protected writes,
untrusted-input defense) so every AI follows them in every project, not just in this vault.
Copy its content into your tool's user-level file (`~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md`,
`~/.gemini/GEMINI.md`, or Cursor's User Rules) and replace `<VAULT_PATH>` with your clone's
absolute path. Inside the vault, `AGENTS.md` takes precedence.

## Make it yours

The `08`–`11` and `13` folders ship empty. Start with `/capture`, and keep your own notes out of
any public fork: add private folders to `.gitignore` or keep the vault in a private repository.

## Safety notes

- Treat third-party skills and repos as untrusted. Run `python scripts/scan_untrusted.py "<path>"`
  before reading them in bulk, and never run their installers to evaluate them.
- Never store secrets in the vault. The pre-commit hook helps but is not a guarantee.
- Third-party attributions and licences are listed in `NOTICE.md`.
