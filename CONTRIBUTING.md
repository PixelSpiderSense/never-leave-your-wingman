# Contributing

Thanks for helping. Small, focused pull requests are easiest to review.

- **Open an issue first** for anything that changes `AGENTS.md`, the handoff protocol or a
  skill's behaviour, so the direction can be agreed before you write it.
- **Keep it generic.** Don't add company names, personal paths, credentials or client data.
  Run `python scripts/check_staged_secrets.py` and, for third-party material,
  `python scripts/scan_untrusted.py "<path>"` before you push.
- **Match the style.** Markdown with YAML frontmatter, kebab-case filenames, `[[wikilinks]]`
  between notes, DD-MM-YYYY for human-readable dates.
- **Attribute borrowed ideas.** If you adapt text from another project, add it to `NOTICE.md`
  with its licence.
- **Say what you tested.** State which tool you used (Claude Code, Cursor, Codex, Gemini CLI)
  and what you actually verified.

By contributing you agree your work is released under the MIT licence in `LICENSE`.
