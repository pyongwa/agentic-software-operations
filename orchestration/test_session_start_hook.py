#!/usr/bin/env python3
"""Tests for the SessionStart hook audit (EXEC-456 Slice 1).

The audit must make every hook fire observable WITHOUT changing the hook's
stdout contract and WITHOUT ever breaking the session:
  - success  -> stdout has the orientation JSON AND one "injected" audit line
  - failure  -> exit 0, NO stdout, AND one "error" audit line
"""
import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import session_start_hook as hook  # noqa: E402
import gen_orchestration as g  # noqa: E402


class HookAuditTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False)
        self._tmp.close()
        self._log = self._tmp.name
        os.environ["ASO_AUDIT_LOG"] = self._log
        self._stdin = sys.stdin
        sys.stdin = io.StringIO("")  # no payload; non-tty, read() -> ""

    def tearDown(self):
        sys.stdin = self._stdin
        os.environ.pop("ASO_AUDIT_LOG", None)
        try:
            os.unlink(self._log)
        except OSError:
            pass

    def _audit_lines(self):
        with open(self._log, encoding="utf-8") as fh:
            return [json.loads(ln) for ln in fh if ln.strip()]

    def test_success_emits_orientation_and_injected_audit(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = hook.main()
        self.assertEqual(rc, 0)
        # stdout contract unchanged: the orientation JSON is still emitted.
        self.assertIn("hookSpecificOutput", buf.getvalue())
        # exactly one audit record, marking a successful injection.
        recs = self._audit_lines()
        self.assertEqual(len(recs), 1)
        self.assertEqual(recs[0]["event"], "session_start")
        self.assertEqual(recs[0]["status"], "injected")
        self.assertIsInstance(recs[0]["skills"], int)
        self.assertGreater(recs[0]["skills"], 0)
        self.assertIn("ts", recs[0])

    def test_failure_is_silent_on_stdout_but_audited(self):
        orig = g.load_skills
        g.load_skills = lambda: (_ for _ in ()).throw(RuntimeError("boom"))
        try:
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = hook.main()
        finally:
            g.load_skills = orig
        self.assertEqual(rc, 0)  # never break the session
        self.assertEqual(buf.getvalue().strip(), "")  # no stdout on failure
        recs = self._audit_lines()
        self.assertEqual(len(recs), 1)
        self.assertEqual(recs[0]["status"], "error")
        self.assertIn("boom", recs[0]["error"])

    def test_audit_failure_never_breaks_the_hook(self):
        # Point the audit at an unwritable path; the hook must still succeed.
        os.environ["ASO_AUDIT_LOG"] = "/proc/nonexistent/cannot/write.jsonl"
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = hook.main()
        self.assertEqual(rc, 0)
        self.assertIn("hookSpecificOutput", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
