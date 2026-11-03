#!/usr/bin/env python3
"""Prep report for scope-creep review: file list + change size, never mutates git."""

import argparse
import subprocess
import sys


def get_numstat(staged: bool) -> str:
    cmd = ["git", "diff", "--numstat"]
    if staged:
        cmd.insert(2, "--cached")
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return result.stdout


def parse_numstat(numstat: str):
    files = []
    for line in numstat.splitlines():
        if not line.strip():
            continue
        added, deleted, path = line.split("\t", 2)
        if added == "-" or deleted == "-":
            files.append((path, None))  # binary file
        else:
            files.append((path, int(added) + int(deleted)))
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--intent", required=True, help="One-line stated intent for this diff")
    parser.add_argument("--staged", action="store_true", help="Use `git diff --cached` instead of unstaged")
    parser.add_argument("--threshold", type=int, default=80, help="Line-count above which a file is flagged (default: 80)")
    args = parser.parse_args()

    try:
        numstat = get_numstat(args.staged)
    except subprocess.CalledProcessError as e:
        print(f"git diff failed: {e}", file=sys.stderr)
        sys.exit(1)

    files = parse_numstat(numstat)
    if not files:
        print("No changes found. Nothing to classify.")
        return

    print(f"Stated intent: {args.intent}")
    print(f"Threshold: {args.threshold} changed lines\n")
    print(f"{'lines':>7}  {'flag':<10}  file")
    for path, lines in files:
        if lines is None:
            print(f"{'binary':>7}  {'justify?':<10}  {path}")
        elif lines > args.threshold:
            print(f"{lines:>7}  {'justify?':<10}  {path}")
        else:
            print(f"{lines:>7}  {'':<10}  {path}")

    print(
        "\nClassify each file against the stated intent: keep (serves it), "
        "split (unrelated, separate commit), or justify (related but flagged above)."
    )


if __name__ == "__main__":
    main()
