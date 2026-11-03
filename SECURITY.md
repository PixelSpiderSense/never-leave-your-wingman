# Security policy

## Reporting a vulnerability

Please report security problems privately through GitHub's **Report a vulnerability** option on
the Security tab of this repository (private vulnerability reporting). Do not open a public issue
for anything that could be exploited.

Useful details: what you found, which file or script, how to reproduce it, and which AI tool and
version you used.

## What is in scope

- The scripts in `scripts/` (`scan_untrusted.py`, `check_staged_secrets.py`, `inbox_status.py`).
- The pre-commit hook in `.githooks/`.
- Rules in `AGENTS.md`, `GLOBAL-AGENTS.md` and `07-Prompts/prompt-defense.md` that fail to prevent
  a prompt-injection or secret-leak path they claim to cover.

## What to expect

This is a small personal project. I will acknowledge a report as soon as I can and fix confirmed
issues in a new commit. There is no bounty. The scanner and secret check are screens, not
guarantees; see the safety notes in the README.
