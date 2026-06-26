#!/usr/bin/env python3
"""Tests for the lifecycle-write audit hook (EXEC-456 Slice 2).

A PostToolUse hook that fires on the jira-lifecycle WRITE operations
(transition / comment / edit / issue-link) and appends one session-tagged
audit record per write, so "did this session record its work?" becomes a
query over the audit log rather than a guess.

Contract (mirrors Slice 1):
  - a recognized write  -> exactly one "lifecycle_write" record (op + issue +
    session_id), NO stdout, exit 0
  - a read that slips past the matcher -> NO record (silent), exit 0
  - an unparseable payload we were invoked on -> one "error" record (a real
    write we couldn't observe is a miss worth surfacing), NO stdout, exit 0
  - the hook NEVER raises and NEVER writes stdout (PostToolUse stdout is shown
    in the transcript; the audit must stay invisible there)
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

import lifecycle_write_hook as hook  # noqa: E402


class LifecycleWriteHookTest(unittest.TestCase):
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
        """Feed a payload on stdin exactly as Claude Code would, run main()."""
        sys.stdin = io.StringIO(payload if isinstance(payload, str) else json.dumps(payload))
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = hook.main()
        return rc, buf.getvalue()

    def _records(self):
        with open(self._log, encoding="utf-8") as fh:
            return [json.loads(ln) for ln in fh if ln.strip()]

    def test_transition_write_is_audited_with_op_issue_and_session(self):
        rc, out = self._run({
            "session_id": "sess-1",
            "tool_name": "mcp__claude_ai_Atlassian_Rovo__transitionJiraIssue",
            "tool_input": {"cloudId": "x", "issueIdOrKey": "EXEC-456", "transition": {"id": "31"}},
        })
        self.assertEqual(rc, 0)
        self.assertEqual(out, "")  # never pollutes the transcript
        recs = self._records()
        self.assertEqual(len(recs), 1)
        r = recs[0]
        self.assertEqual(r["event"], "lifecycle_write")
        self.assertEqual(r["op"], "transition")
        self.assertEqual(r["issue"], "EXEC-456")
        self.assertEqual(r["session_id"], "sess-1")
        self.assertEqual(r["status"], "ok")
        self.assertIn("ts", r)

    def test_comment_write_op_label(self):
        rc, out = self._run({
            "session_id": "sess-2",
            "tool_name": "mcp__claude_ai_Atlassian_Rovo__addCommentToJiraIssue",
            "tool_input": {"issueIdOrKey": "IDEA-25", "commentBody": "PR: http://x"},
        })
        self.assertEqual(rc, 0)
        recs = self._records()
        self.assertEqual(len(recs), 1)
        self.assertEqual(recs[0]["op"], "comment")
        self.assertEqual(recs[0]["issue"], "IDEA-25")

    def test_edit_write_op_label(self):
        rc, _ = self._run({
            "session_id": "s",
            "tool_name": "mcp__plugin_atlassian_atlassian__editJiraIssue",
            "tool_input": {"issueIdOrKey": "EXEC-1", "fields": {"labels": ["blocked"]}},
        })
        self.assertEqual(rc, 0)
        self.assertEqual(self._records()[0]["op"], "edit")

    def test_issue_link_extracts_key_without_an_issueidorkey_field(self):
        # createIssueLink has no issueIdOrKey — the key lives in the link refs.
        rc, _ = self._run({
            "session_id": "s",
            "tool_name": "mcp__claude_ai_Atlassian_Rovo__createIssueLink",
            "tool_input": {"type": "is child of",
                           "inwardIssue": {"key": "EXEC-456"},
                           "outwardIssue": {"key": "EXEC-444"}},
        })
        self.assertEqual(rc, 0)
        r = self._records()[0]
        self.assertEqual(r["op"], "link")
        self.assertEqual(r["issue"], "EXEC-456")  # first key found

    def test_read_tool_is_silent(self):
        # A read that slips past the matcher must NOT be logged (would pollute
        # the per-ticket correlation Slice 3 depends on).
        rc, out = self._run({
            "session_id": "s",
            "tool_name": "mcp__claude_ai_Atlassian_Rovo__getJiraIssue",
            "tool_input": {"issueIdOrKey": "EXEC-456"},
        })
        self.assertEqual(rc, 0)
        self.assertEqual(out, "")
        self.assertEqual(self._records(), [])

    def test_transitions_read_is_silent(self):
        # getTransitionsForJiraIssue contains "JiraIssue" but is a READ.
        rc, _ = self._run({
            "session_id": "s",
            "tool_name": "mcp__claude_ai_Atlassian_Rovo__getTransitionsForJiraIssue",
            "tool_input": {"issueIdOrKey": "EXEC-456"},
        })
        self.assertEqual(rc, 0)
        self.assertEqual(self._records(), [])

    def test_write_with_missing_issue_key_still_logs(self):
        rc, _ = self._run({
            "session_id": "s",
            "tool_name": "mcp__claude_ai_Atlassian_Rovo__transitionJiraIssue",
            "tool_input": {"transition": {"id": "31"}},  # no key present
        })
        self.assertEqual(rc, 0)
        r = self._records()[0]
        self.assertEqual(r["op"], "transition")
        self.assertIsNone(r["issue"])  # logged as a miss, not dropped

    def test_unparseable_payload_logs_error_record(self):
        rc, out = self._run("}{ not json")
        self.assertEqual(rc, 0)        # never break the session
        self.assertEqual(out, "")      # never pollute the transcript
        recs = self._records()
        self.assertEqual(len(recs), 1)
        self.assertEqual(recs[0]["event"], "lifecycle_write")
        self.assertEqual(recs[0]["status"], "error")

    def test_audit_failure_never_breaks_the_hook(self):
        os.environ["ASO_AUDIT_LOG"] = "/proc/nonexistent/cannot/write.jsonl"
        rc, out = self._run({
            "session_id": "s",
            "tool_name": "mcp__claude_ai_Atlassian_Rovo__transitionJiraIssue",
            "tool_input": {"issueIdOrKey": "EXEC-1"},
        })
        self.assertEqual(rc, 0)
        self.assertEqual(out, "")


if __name__ == "__main__":
    unittest.main()
