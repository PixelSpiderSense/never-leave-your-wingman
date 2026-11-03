#!/usr/bin/env python
"""SessionStart reminder: surface pending agent-inbox handoffs.

Why this exists: `/drain` is deliberately manual (human-in-the-loop, per
the swarm-orchestration decision note — no daemon, no scheduler). But a manual
command with no reminder gets forgotten: a reviewer handoff sat pending for 5 weeks because
nothing surfaced it. This does not automate execution — it only makes the queue visible.

**Silent when every inbox is empty**, so it adds nothing to the ~95% of sessions with no pending
work. Only speaks when there is something to drain.

Never fails a session: errors produce a bounded diagnostic and exit 0.

    python scripts/inbox_status.py            # the hook entry point
    python scripts/inbox_status.py --self-test
"""

from __future__ import annotations

import os
import re
import sys
from datetime import date, datetime
from pathlib import Path

DEFAULT_VAULT = Path(__file__).resolve().parents[1]
AGENTS = ("ceo", "coder", "reviewer", "scribe", "memory")
STALE_DAYS = 7
DATE_RE = re.compile(r"(20\d{2}-\d{2}-\d{2})")


def note_date(path: Path, today: date) -> int:
    """Age in days, from frontmatter `date:` if present, else filename, else mtime."""
    try:
        head = path.read_text(encoding="utf-8", errors="replace")[:400]
        m = re.search(r"^date:\s*\"?(20\d{2}-\d{2}-\d{2})", head, re.M)
        if not m:
            m = DATE_RE.search(path.name)
        if m:
            return (today - date.fromisoformat(m.group(1))).days
    except (OSError, ValueError):
        pass
    try:
        return (today - datetime.fromtimestamp(path.stat().st_mtime).date()).days
    except OSError:
        return 0


def note_status(path: Path) -> str:
    """Read a bounded scalar status from frontmatter, never from note content."""
    if path.is_symlink():
        return "invalid"
    try:
        with path.open("rb") as source:
            raw = source.read(16385)
        lines = raw.replace(b"\r\n", b"\n").split(b"\n")
        if lines[0].removeprefix(b"\xef\xbb\xbf") != b"---":
            return "invalid"
        end = lines.index(b"---", 1)
        header = b"\n".join(lines[1:end]).decode("utf-8")
        statuses = re.findall(r"^status:([^\n]*)$", header, re.M)
        if len(statuses) != 1:
            return "invalid"
        value = statuses[0].split("#", 1)[0].strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        return value if value in {"pending", "in-progress", "blocked", "done"} else "invalid"
    except (OSError, UnicodeError, ValueError):
        return "invalid"


def scan(vault: Path, today: date | None = None, notices: list[str] | None = None) -> list[tuple[str, int, int, str]]:
    """Return pending rows; report other actionable statuses separately."""
    today = today or date.today()
    notices = notices if notices is not None else []
    out = []
    for agent in AGENTS:
        inbox = vault / "05-Agents" / agent / "inbox"
        if not inbox.is_dir() or inbox.is_symlink() or inbox.is_junction():
            print(f"[vault] {agent} inbox unavailable", file=sys.stderr)
            continue
        pending = []
        counts = {"blocked": 0, "in-progress": 0, "invalid": 0}
        for path in sorted(inbox.glob("*.md")):
            if not path.is_file():
                continue
            status = note_status(path)
            if status == "pending":
                pending.append(path)
            elif status in counts:
                counts[status] += 1
        summaries = [f"{count} {status}" for status, count in counts.items() if count]
        if summaries:
            notices.append(f"{agent}: " + ", ".join(summaries))
        if pending:
            aged = sorted(((note_date(p, today), p.stem) for p in pending), reverse=True)
            out.append((agent, len(pending), aged[0][0], aged[0][1]))
    return out


def render(rows: list[tuple[str, int, int, str]], notices: list[str] | None = None) -> str:
    """Offer drain only for pending notes; escape source-controlled filenames."""
    parts = []
    for agent, count, age, name in rows:
        stale = " !STALE" if age >= STALE_DAYS else ""
        parts.append(f"{agent}: {count} pending, oldest {age}d{stale} ({ascii(name)})")
    parts.extend(notices or [])
    if not parts:
        return ""
    result = "[vault] Agent inbox: " + " | ".join(parts)
    if rows:
        result += "\n         Run: " + " ".join(f"/drain {a}" for a, *_ in rows)
    return result


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass
    try:
        vault = Path(os.environ.get("SECONDBRAIN_VAULT", DEFAULT_VAULT))
        if not vault.is_dir():
            print("[vault] configured vault unavailable; check SECONDBRAIN_VAULT", file=sys.stderr)
            return 0
        notices = []
        line = render(scan(vault, notices=notices), notices)
        if line:
            print(line)
    except Exception as exc:  # noqa: BLE001 - a reminder must never break a session
        # Report to stderr rather than vanishing. Swallowing this silently is what made the
        # hook mute for its first run; the session still proceeds because we exit 0.
        print(f"[vault] inbox reminder failed: {type(exc).__name__}: {exc}", file=sys.stderr)
    return 0


def self_test() -> int:
    import tempfile

    assert render([]) == "", "must be silent when nothing is pending"

    with tempfile.TemporaryDirectory() as d:
        v = Path(d)
        for a in AGENTS:
            (v / "05-Agents" / a / "inbox").mkdir(parents=True)
        assert scan(v) == [], "empty inboxes yield no rows"
        assert render(scan(v)) == ""

        today = date(2026, 8, 12)
        rv = v / "05-Agents" / "reviewer" / "inbox"
        (rv / "20260704-review-thing.md").write_text(
            '---\ntype: handoff\ndate: "2026-07-04"\nstatus: pending\n---\n# Review\n',
            encoding="utf-8")
        (rv / "20260810-newer.md").write_text(
            '---\ntype: handoff\ndate: "2026-08-10"\nstatus: pending\n---\n# Newer\n', encoding="utf-8")
        # non-markdown must be ignored (mirrors /drain's own rule)
        (rv / ".gitkeep").write_text("", encoding="utf-8")

        rows = scan(v, today)
        assert len(rows) == 1, rows
        agent, count, age, name = rows[0]
        assert agent == "reviewer" and count == 2, rows
        assert age == 39, f"expected 39d from frontmatter date, got {age}"
        assert name == "20260704-review-thing", name

        line = render(rows)
        assert "reviewer: 2 pending" in line and "39d" in line and "STALE" in line, line
        assert "/drain reviewer" in line, line
        # REGRESSION: output must survive a legacy Windows console. An emoji here previously
        # raised UnicodeEncodeError under cp1252 and the caller swallowed it into silence.
        line.encode("cp1252")
        line.encode("ascii")

        # a fresh note must NOT be flagged stale
        fresh = v / "05-Agents" / "coder" / "inbox" / "x.md"
        fresh.write_text('---\ndate: "2026-08-12"\nstatus: pending\n---\n# x\n', encoding="utf-8")
        crow = [r for r in scan(v, today) if r[0] == "coder"][0]
        assert crow[2] == 0 and "STALE" not in render([crow]), crow

        # filename-date fallback when frontmatter has no date
        nf = v / "05-Agents" / "scribe" / "inbox" / "2026-08-05-nofm.md"
        nf.write_text("---\nstatus: pending\n---\n# no frontmatter date\n", encoding="utf-8")
        srow = [r for r in scan(v, today) if r[0] == "scribe"][0]
        assert srow[2] == 7, srow

    # a missing vault emits a diagnostic without failing the session
    os.environ["SECONDBRAIN_VAULT"] = str(Path(tempfile.gettempdir()) / "_no_such_vault_xyz")
    assert main() == 0
    os.environ.pop("SECONDBRAIN_VAULT", None)

    print("self-test: all assertions passed")
    return 0


if __name__ == "__main__":
    sys.exit(self_test() if "--self-test" in sys.argv[1:] else main())
