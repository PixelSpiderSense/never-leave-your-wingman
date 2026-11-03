"""Regression cases for the read-only inbox reminder."""
import contextlib
import importlib.util
import io
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location('inbox_status', Path(__file__).with_name('inbox_status.py'))
reminder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(reminder)


class InboxTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for role in reminder.AGENTS:
            (self.root / '05-Agents' / role / 'inbox').mkdir(parents=True)

    def note(self, name, status):
        path = self.root / '05-Agents/coder/inbox' / name
        path.write_text(f'---\nstatus: {status}\ndate: "2026-09-01"\n---\n# Test\n', encoding='utf-8')
        return path

    def run_main(self):
        out, err = io.StringIO(), io.StringIO()
        with patch.dict(os.environ, {'SECONDBRAIN_VAULT': str(self.root)}), contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            result = reminder.main()
        return result, out.getvalue(), err.getvalue()

    def test_default_is_script_checkout(self):
        self.assertEqual(reminder.DEFAULT_VAULT, Path(reminder.__file__).resolve().parents[1])

    def test_empty_is_silent(self):
        self.assertEqual(self.run_main(), (0, '', ''))

    def test_only_pending_is_drainable(self):
        for name, status in [('a.md', 'pending'), ('b.md', 'blocked'), ('c.md', 'done'), ('d.md', 'in-progress')]:
            self.note(name, status)
        result, out, err = self.run_main()
        self.assertEqual(result, 0)
        self.assertIn('1 pending', out)
        self.assertIn('1 blocked', out)
        self.assertIn('1 in-progress', out)
        self.assertNotIn('4 pending', out)
        self.assertIn('/drain coder', out)
        self.assertEqual(err, '')

    def test_blocked_only_does_not_offer_drain(self):
        self.note('blocked.md', 'blocked')
        _, out, _ = self.run_main()
        self.assertIn('1 blocked', out)
        self.assertNotIn('/drain', out)

    def test_done_only_is_silent(self):
        self.note('done.md', 'done')
        self.assertEqual(self.run_main(), (0, '', ''))

    def test_missing_and_duplicate_status_are_invalid(self):
        self.note('missing.md', 'unknown')
        path = self.note('duplicate.md', 'pending')
        path.write_text('---\nstatus: pending\nstatus: done\n---\n', encoding='utf-8')
        _, out, _ = self.run_main()
        self.assertIn('2 invalid', out)
        self.assertNotIn('/drain', out)

    def test_body_status_cannot_activate_note(self):
        self.note('body.md', 'done').write_text('---\ntype: handoff\n---\nstatus: pending\n', encoding='utf-8')
        _, out, _ = self.run_main()
        self.assertIn('1 invalid', out)
        self.assertNotIn('/drain', out)

    def test_quoted_status_with_comment(self):
        self.note('quoted.md', '"pending" # reviewed header')
        self.assertIn('1 pending', self.run_main()[1])

    def test_bad_encoding_is_invalid_without_content_dump(self):
        self.note('bad.md', 'pending').write_bytes(b'---\nstatus: pending\nprivate: \xff\n---\n')
        _, out, err = self.run_main()
        self.assertIn('1 invalid', out)
        self.assertNotIn('private:', out + err)

    def test_missing_root_is_diagnostic_not_empty(self):
        self.root = self.root / 'absent'
        result, out, err = self.run_main()
        self.assertEqual(result, 0)
        self.assertEqual(out, '')
        self.assertIn('unavailable', err)

    def test_missing_inbox_is_reported(self):
        (self.root / '05-Agents/memory/inbox').rmdir()
        self.assertIn('unavailable', self.run_main()[2])

    def test_scan_does_not_modify_notes(self):
        path = self.note('keep.md', 'pending')
        before = path.read_bytes()
        self.run_main()
        self.assertEqual(path.read_bytes(), before)

    def test_display_escapes_non_ascii_name(self):
        self.note('task-\u202e.md', 'pending')
        out = self.run_main()[1]
        out.encode('ascii')
        self.assertNotIn('\u202e', out)


if __name__ == '__main__':
    unittest.main()
