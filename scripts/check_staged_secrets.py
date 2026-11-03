#!/usr/bin/env python3
"""Inspect staged blobs without printing secret values or mutating Git."""
import re
import subprocess
import sys
from pathlib import PurePosixPath

RULES = [
    ("aws", rb"AKIA[A-Z0-9]{16}"),
    ("github", rb"(?:gh[pousr]_[A-Za-z0-9]{36}|github_pat_[A-Za-z0-9_]{22,})"),
    ("slack", rb"xox[baprs]-[A-Za-z0-9-]+"),
    ("google", rb"AIza[0-9A-Za-z_-]{35}"),
    ("private-key", rb"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    ("provider-key", rb"(?:sk-ant-[A-Za-z0-9_-]{20,}|sk_(?:live|test)_[A-Za-z0-9]{16,}|rzp_(?:live|test)_[A-Za-z0-9]{10,})"),
    ("generic-key", rb"sk-[A-Za-z0-9_-]{32,}"),
    ("jwt", rb"eyJ[A-Za-z0-9_-]{20,}\.eyJ[A-Za-z0-9_-]{20,}"),
    ("assignment", rb"(?:api[_-]?key|secret|password|passwd|token)\s*[:=]\s*[\"']*[A-Za-z0-9_/+-]{16,}"),
]

def git_bytes(*args):
    completed = subprocess.run(
        ["git", "--no-pager", *args], capture_output=True, check=True)
    return completed.stdout

def main():
    blocked = []
    try:
        names = git_bytes("diff", "--cached", "--name-only", "-z",
                          "--no-renames", "--diff-filter=ACMT")
        for raw in filter(None, names.split(b"\0")):
            path = raw.decode("utf-8", "surrogateescape")
            name = PurePosixPath(path).name.lower()
            if (name == ".env" or name.startswith(".env.") or name.endswith(".env")) and name not in {".env.example", ".env.sample"}:
                blocked.append((path, "environment-file"))
            blob = git_bytes("show", ":" + path)
            for category, expression in RULES:
                for match in re.finditer(expression, blob, re.IGNORECASE if category == "assignment" else 0):
                    blocked.append((path, category))
                    break
    except (OSError, subprocess.CalledProcessError) as exc:
        print("Secret check could not inspect the staged input:", type(exc).__name__, file=sys.stderr)
        return 2
    for path, category in sorted(set(blocked)):
        print("BLOCKED", ascii(path), category)
    if blocked:
        print("Review the indicated staged files locally. Remove secrets; do not paste values into notes.")
        return 1
    print("Staged secret screen completed. Pattern screening is not proof that no secret exists.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
