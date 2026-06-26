#!/usr/bin/env python3
"""Tests for the user-prompt audit hook (EXEC-456 Slice 3).

A UserPromptSubmit hook that fires when the user submits a prompt and appends
one session-tagged `user_prompt` record. This is the prompt timeline the Slice 3
gap-probe needs to classify each lifecycle write as ambient (not preceded by a
user prompt) vs prompted.

Contract (mirrors Slices 1/2):
  - a prompt submission   -> exactly one "user_prompt" record (session_id),
    NO stdout, exit 0
  - an unparseable payload -> one "error" record (a missed prompt leaves a gap
    in the timeline that would mislabel a later write as ambient), NO stdout
  - the prompt TEXT is never logged (privacy + noise; only that a prompt fired)
  - the hook NEVER raises and NEVER writes stdout (UserPromptSubmit stdout is
    injected into the model context; the audit must stay invisible there)
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

import user_prompt_hook as hook  # noqa: E402


class UserPromptHookTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False)
        self._tmp.close()
        self._log = self._tmp.name
        os.environ["ASO_AUDIT_LOG"] = self._log
        self._stdin = sys.stdin

    def tearDown(self):
        sys.stdin = self._stdin
        os.environ.pop("ASO_AUDIT_LOG", None)
        try:
            os.unlink(self._log)
        except OSError:
            pass

    def _run(self, payload):
        sys.stdin = io.StringIO(payload if isinstance(payload, str) else json.dumps(payload))
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = hook.main()
        return rc, buf.getvalue()

    def _records(self):
        with open(self._log, encoding="utf-8") as fh:
            return [json.loads(ln) for ln in fh if ln.strip()]

    def test_prompt_is_audited_with_session_and_no_stdout(self):
        rc, out = self._run({
            "session_id": "sess-1",
            "hook_event_name": "UserPromptSubmit",
            "prompt": "continue the ASO launch work",
        })
        self.assertEqual(rc, 0)
        self.assertEqual(out, "")  # UserPromptSubmit stdout would enter context
        recs = self._records()
        self.assertEqual(len(recs), 1)
        r = recs[0]
        self.assertEqual(r["event"], "user_prompt")
        self.assertEqual(r["session_id"], "sess-1")
        self.assertEqual(r["status"], "ok")
        self.assertIn("ts", r)

    def test_prompt_text_is_never_logged(self):
        secret = "my password is hunter2 and SSN 123-45-6789"
        rc, _ = self._run({"session_id": "s", "prompt": secret})
        self.assertEqual(rc, 0)
        blob = json.dumps(self._records())
        self.assertNotIn("hunter2", blob)
        self.assertNotIn("123-45-6789", blob)

    def test_missing_session_id_still_logs(self):
        rc, _ = self._run({"prompt": "hi"})  # no session_id
        self.assertEqual(rc, 0)
        r = self._records()[0]
        self.assertEqual(r["event"], "user_prompt")
        self.assertIsNone(r["session_id"])  # logged as a gap, not dropped

    def test_unparseable_payload_logs_error_record(self):
        rc, out = self._run("}{ not json")
        self.assertEqual(rc, 0)
        self.assertEqual(out, "")
        recs = self._records()
        self.assertEqual(len(recs), 1)
        self.assertEqual(recs[0]["event"], "user_prompt")
        self.assertEqual(recs[0]["status"], "error")

    def test_audit_failure_never_breaks_the_hook(self):
        os.environ["ASO_AUDIT_LOG"] = "/proc/nonexistent/cannot/write.jsonl"
        rc, out = self._run({"session_id": "s", "prompt": "x"})
        self.assertEqual(rc, 0)
        self.assertEqual(out, "")


if __name__ == "__main__":
    unittest.main()
