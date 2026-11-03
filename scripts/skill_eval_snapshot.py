#!/usr/bin/env python
"""Side-effect check for skill evals: did a test run change files or start processes?

Encodes the manual check used while testing the user-level skills (2026-09-23/24):
snapshot a target folder and a watch-list of processes, run the eval, snapshot again, compare.

Fail-closed: an unreadable path, a failed process listing, or a missing snapshot is an ERROR,
never "unchanged". A clean result is evidence about the watched folder and processes only.

Usage:
    python scripts/skill_eval_snapshot.py snapshot <dir> <out.json> [--strict]
    python scripts/skill_eval_snapshot.py compare <before.json> <after.json> [--allow GLOB ...]
    python scripts/skill_eval_snapshot.py --self-test

--strict skips no directories and adds a SHA-256 of every file, so a rewrite that keeps size and
mtime is still caught. Links (symlinks, junctions) are never followed; their target is recorded,
so retargeting one shows as CHANGED, and a link whose target cannot be read is an ERROR. A link
whose target resolves outside the snapshot root is listed in "links_outside_root": writes through
it land in that target, which this snapshot does not watch. Browser automation flags are read
when each snapshot is taken, so a compare can be re-run later with the same result.

Exit: 0 unchanged · 1 changed · 2 error or bad usage.
"""

import csv
import fnmatch
import hashlib
import io
import json
import os
import subprocess
import sys
import time
from pathlib import Path

SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "vendor", ".next", ".wrangler"}  # __pycache__ is kept: new .pyc = code was imported
WATCH = {
    "python.exe", "pythonw.exe", "chrome.exe", "chromedriver.exe", "msedge.exe", "msedgedriver.exe",
    "php.exe", "node.exe", "docker.exe", "workerd.exe", "dwg2dxf.exe", "excel.exe", "outlook.exe",
    "psql.exe", "supabase.exe",
}
BROWSERS = {"chrome.exe", "msedge.exe"}
AUTOMATION_FLAGS = ("--enable-automation", "--remote-debugging", "--test-type", "--headless")


def is_link(path):
    """True for symlinks and Windows junctions; they are recorded, never followed."""
    if os.path.islink(path):
        return True
    isjunction = getattr(os.path, "isjunction", None)
    return bool(isjunction and isjunction(path))


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def snapshot_files(root, strict=False):
    files, errors, outside = {}, [], {}
    if not os.path.isdir(root):
        return files, [f"not a directory: {root}"], outside
    base = os.path.normcase(os.path.realpath(root)) + os.sep

    def record_link(full):
        rel = os.path.relpath(full, root)
        try:
            target = os.readlink(full)
        except OSError as exc:
            errors.append(f"unresolved link: {full} ({exc.strerror})")
            return
        files[rel] = ["link", target]
        resolved = os.path.realpath(full)
        if not os.path.normcase(resolved).startswith(base):
            outside[rel] = resolved

    def onerror(exc):
        errors.append(f"unreadable: {exc.filename}")

    for parent, dirs, names in os.walk(root, onerror=onerror, followlinks=False):
        keep = []
        for d in dirs:
            full = os.path.join(parent, d)
            if d in SKIP_DIRS and not strict:
                continue
            if is_link(full):
                record_link(full)
            else:
                keep.append(d)
        dirs[:] = keep
        for n in names:
            full = os.path.join(parent, n)
            try:
                if is_link(full):
                    record_link(full)
                    continue
                st = os.stat(full, follow_symlinks=False)
                entry = [st.st_size, st.st_mtime_ns]
                if strict:
                    entry.append(sha256(full))
                files[os.path.relpath(full, root)] = entry
            except OSError as exc:
                errors.append(f"unreadable: {full} ({exc.strerror})")
    return files, errors, outside


def snapshot_processes():
    """Return ({"name|pid": name}, error-or-None) for watched process names."""
    try:
        out = subprocess.run(["tasklist", "/FO", "CSV", "/NH"], capture_output=True,
                             text=True, timeout=60, check=True).stdout
    except (OSError, subprocess.SubprocessError) as exc:
        return {}, f"process listing failed: {exc}"
    procs = {}
    own = {str(os.getpid()), str(os.getppid())}  # this tool's own interpreter is not a side effect
    for row in csv.reader(io.StringIO(out)):
        if len(row) >= 2 and row[0].lower() in WATCH and row[1] not in own:
            procs[f"{row[0].lower()}|{row[1]}"] = row[0].lower()
    return procs, None


def browser_flags(pids):
    """Map pid -> list of automation flags seen on its command line (None if unknown)."""
    if not pids:
        return {}
    ids = ",".join(str(int(p)) for p in pids)
    ps = ("Get-CimInstance Win32_Process | Where-Object { @(" + ids + ") -contains $_.ProcessId } | "
          "ForEach-Object { \"$($_.ProcessId)`t$($_.CommandLine)\" }")
    try:
        out = subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True,
                             text=True, timeout=60, check=True).stdout
    except (OSError, subprocess.SubprocessError):
        return {p: None for p in pids}
    seen = {}
    for line in out.splitlines():
        pid, _, cmd = line.partition("\t")
        if pid.strip().isdigit():
            seen[pid.strip()] = [f for f in AUTOMATION_FLAGS if f in cmd]
    return {p: seen.get(str(p)) for p in pids}


def cmd_snapshot(root, out, strict=False):
    files, errors, outside = snapshot_files(root, strict)
    procs, perr = snapshot_processes()
    if perr:
        errors.append(perr)
    flags = browser_flags([k.split("|")[1] for k in procs if k.split("|")[0] in BROWSERS])
    data = {"schema": "skill-eval-snapshot/2", "root": os.path.abspath(root), "strict": strict,
            "taken": time.strftime("%Y-%m-%dT%H:%M:%S"), "files": files,
            "processes": procs, "browser_flags": flags, "links_outside_root": outside,
            "errors": errors}
    Path(out).write_text(json.dumps(data, indent=1), encoding="utf-8")
    for rel, target in sorted(outside.items()):
        print(f"link outside root: {rel} -> {target}")
    print(f"snapshot: {len(files)} files, {len(procs)} watched processes, {len(outside)} links outside "
          f"root, {len(errors)} errors -> {out}")
    return 2 if errors else 0


def load(path):
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return None, f"cannot read snapshot {path}: {exc}"
    if data.get("schema") != "skill-eval-snapshot/2":
        return None, f"not a skill-eval snapshot: {path}"
    return data, None


def cmd_compare(before_path, after_path, allow):
    before, e1 = load(before_path)
    after, e2 = load(after_path)
    errors = [e for e in (e1, e2) if e]
    if not errors:
        errors += [f"before: {e}" for e in before["errors"]] + [f"after: {e}" for e in after["errors"]]
        if before["root"] != after["root"]:
            errors.append("snapshots are of different folders")
        if before["strict"] != after["strict"]:
            errors.append("one snapshot is --strict and the other is not")
    if errors:
        for e in errors:
            print(f"ERROR {e}")
        print("RESULT: ERROR (not a clean result)")
        return 2

    allowed = lambda rel: any(fnmatch.fnmatch(rel.replace("\\", "/"), g) for g in allow)
    bf, af = before["files"], after["files"]
    added = sorted(p for p in af.keys() - bf.keys() if not allowed(p))
    removed = sorted(p for p in bf.keys() - af.keys() if not allowed(p))
    changed = sorted(p for p in af.keys() & bf.keys() if af[p] != bf[p] and not allowed(p))
    new_procs = sorted(af_k for af_k in after["processes"].keys() - before["processes"].keys())

    flags = after["browser_flags"]  # read at snapshot time, not now
    suspicious, benign = [], []
    for k in new_procs:
        name, pid = k.split("|")
        if name in BROWSERS and flags.get(pid) == []:
            benign.append(k)
        else:
            suspicious.append(k if name not in BROWSERS else f"{k} flags={flags.get(pid)}")

    for label, items in (("ADDED", added), ("REMOVED", removed), ("CHANGED", changed),
                         ("NEW PROCESS", suspicious)):
        for item in items:
            print(f"{label} {item}")
    if benign:
        print(f"note: {len(benign)} new browser process(es) with no automation flags (ordinary tabs)")
    dirty = added or removed or changed or suspicious
    print(f"RESULT: {'CHANGED' if dirty else 'UNCHANGED'} ({len(af)} files compared)")
    return 1 if dirty else 0


def self_test():
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        root = Path(d) / "proj"
        (root / "sub").mkdir(parents=True)
        (root / "a.txt").write_text("one", encoding="utf-8")
        (root / "node_modules").mkdir()
        (root / "node_modules" / "x.js").write_text("skip", encoding="utf-8")
        b, a = Path(d) / "b.json", Path(d) / "a.json"
        assert cmd_snapshot(str(root), str(b)) in (0, 2)
        data = json.loads(b.read_text(encoding="utf-8"))
        assert "a.txt" in data["files"] and not any("node_modules" in k for k in data["files"])
        # unchanged run compares clean (processes may differ on a live machine, so strip them)
        cmd_snapshot(str(root), str(a))
        for p in (a, b):
            j = json.loads(p.read_text(encoding="utf-8")); j["processes"] = {}; j["errors"] = []
            p.write_text(json.dumps(j), encoding="utf-8")
        assert cmd_compare(str(b), str(a), []) == 0
        # a new file is detected, and --allow excuses it
        (root / "sub" / "new.json").write_text("{}", encoding="utf-8")
        cmd_snapshot(str(root), str(a))
        j = json.loads(a.read_text(encoding="utf-8")); j["processes"] = {}; j["errors"] = []
        a.write_text(json.dumps(j), encoding="utf-8")
        assert cmd_compare(str(b), str(a), []) == 1
        assert cmd_compare(str(b), str(a), ["sub/*.json"]) == 0
        # --strict sees skipped dirs, and catches a same-size rewrite with mtime restored
        sb, sa = Path(d) / "sb.json", Path(d) / "sa.json"
        cmd_snapshot(str(root), str(sb), strict=True)
        assert any("node_modules" in k for k in json.loads(sb.read_text(encoding="utf-8"))["files"])
        st = os.stat(root / "a.txt")
        (root / "a.txt").write_text("two", encoding="utf-8")
        os.utime(root / "a.txt", ns=(st.st_atime_ns, st.st_mtime_ns))
        cmd_snapshot(str(root), str(sa), strict=True)
        for p in (sb, sa):
            j2 = json.loads(p.read_text(encoding="utf-8")); j2["processes"] = {}; j2["errors"] = []
            p.write_text(json.dumps(j2), encoding="utf-8")
        assert cmd_compare(str(sb), str(sa), ["sub/*.json"]) == 1
        assert cmd_compare(str(b), str(sa), []) == 2  # strict vs non-strict is refused
        # browser flags come from the snapshot: an ordinary tab stays benign after it closes
        j2 = json.loads(sa.read_text(encoding="utf-8"))
        j3 = dict(j2, processes={"chrome.exe|999999": "chrome.exe"}, browser_flags={"999999": []})
        sa.write_text(json.dumps(j3), encoding="utf-8"); sb.write_text(json.dumps(j2), encoding="utf-8")
        assert cmd_compare(str(sb), str(sa), []) == 0
        j3["browser_flags"] = {"999999": ["--remote-debugging"]}
        sa.write_text(json.dumps(j3), encoding="utf-8")
        assert cmd_compare(str(sb), str(sa), []) == 1
        # a link out of the root is recorded with its target and listed (skipped if links need admin)
        try:
            os.symlink(str(Path(d)), str(root / "out"), target_is_directory=True)
        except OSError:
            pass
        else:
            cmd_snapshot(str(root), str(sb))
            j2 = json.loads(sb.read_text(encoding="utf-8"))
            assert j2["files"]["out"][0] == "link" and "out" in j2["links_outside_root"]
            # a link whose target cannot be read fails closed
            real_readlink = os.readlink
            def broken(path):
                raise OSError(5, "Access is denied")
            os.readlink = broken
            try:
                assert cmd_snapshot(str(root), str(sa)) == 2
            finally:
                os.readlink = real_readlink
            assert any("unresolved link" in e for e in json.loads(sa.read_text(encoding="utf-8"))["errors"])
            assert cmd_compare(str(sb), str(sa), []) == 2
            os.rmdir(root / "out")
        # fail-closed: missing folder, missing snapshot, recorded errors
        assert cmd_snapshot(str(Path(d) / "nope"), str(Path(d) / "n.json")) == 2
        assert cmd_compare(str(b), str(Path(d) / "missing.json"), []) == 2
        j["errors"] = ["unreadable: x"]; a.write_text(json.dumps(j), encoding="utf-8")
        assert cmd_compare(str(b), str(a), []) == 2
    print("self-test: all assertions passed")
    return 0


def main(argv):
    if argv == ["--self-test"]:
        return self_test()
    if argv[:1] == ["snapshot"] and len(argv) in (3, 4) and argv[3:] in ([], ["--strict"]):
        return cmd_snapshot(argv[1], argv[2], strict=len(argv) == 4)
    if len(argv) >= 3 and argv[0] == "compare":
        allow, rest = [], argv[3:]
        while rest:
            if rest[0] == "--allow" and len(rest) > 1:
                allow.append(rest[1]); rest = rest[2:]
            else:
                print(__doc__); return 2
        return cmd_compare(argv[1], argv[2], allow)
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
