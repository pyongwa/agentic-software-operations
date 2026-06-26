#!/usr/bin/env python3
"""Tests for the shared ambient-audit appender (EXEC-456 Slice 2 refactor).

Slice 1's SessionStart hook grew a private `_audit`. Slice 2 adds a second
writer (the lifecycle-write hook), so the append logic is factored into one
module both share. The contract is unchanged: append one JSONL record,
stamp a UTC `ts`, and NEVER raise / NEVER touch stdout — observability must
not be able to break a session.
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

import aso_audit  # noqa: E402


class AsoAuditTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False)
        self._tmp.close()
        self._log = self._tmp.name
        os.environ["ASO_AUDIT_LOG"] = self._log

    def tearDown(self):
        os.environ.pop("ASO_AUDIT_LOG", None)
        try:
            os.unlink(self._log)
        except OSError:
            pass

    def _lines(self):
        with open(self._log, encoding="utf-8") as fh:
            return [json.loads(ln) for ln in fh if ln.strip()]

    def test_append_writes_one_record_with_ts(self):
        aso_audit.append({"event": "x", "status": "ok"})
        recs = self._lines()
        self.assertEqual(len(recs), 1)
        self.assertEqual(recs[0]["event"], "x")
        self.assertEqual(recs[0]["status"], "ok")
        self.assertIn("ts", recs[0])  # appender stamps the timestamp

    def test_append_appends_not_overwrites(self):
        aso_audit.append({"event": "a"})
        aso_audit.append({"event": "b"})
        recs = self._lines()
        self.assertEqual([r["event"] for r in recs], ["a", "b"])

    def test_append_never_raises_on_unwritable_path(self):
        os.environ["ASO_AUDIT_LOG"] = "/proc/nonexistent/cannot/write.jsonl"
        # Must not raise — a logging failure cannot break the caller.
        aso_audit.append({"event": "x"})

    def test_append_never_writes_stdout(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            aso_audit.append({"event": "x"})
        self.assertEqual(buf.getvalue(), "")


if __name__ == "__main__":
    unittest.main()
