#!/usr/bin/env python3
"""PostToolUse hook (EXEC-456 Slice 2): tag jira-lifecycle writes.

Fires after a jira-lifecycle WRITE operation (transition / comment / edit /
issue-link) and appends one session-tagged audit record, so "did this session
record its work?" becomes a query over the audit log instead of a guess —
closing the open loop Slice 1 opened (we know the orientation fired; now we
know whether the session acted on it).

Wired as a plugin PostToolUse hook (hooks/hooks.json), matched to the four
Jira write verbs across any Atlassian MCP server prefix. The matcher narrows
to writes; this script independently re-checks the op so a read that slips
through (getJiraIssue, getTransitionsForJiraIssue, searchJiraIssuesUsingJql)
is never logged — logging reads would pollute the per-ticket correlation the
Slice 3 gap-probe depends on.

Fail-safe like Slice 1: never raises (a hook must not break a session) and
never writes to stdout (Claude Code shows PostToolUse stdout in the transcript;
the audit must stay invisible there). Reads go silent; a write we were invoked
on but could not parse is recorded as an `error` — a real miss must be loud.
"""
import json
import re
import sys

import aso_audit

# Tool-name suffix -> short op label. WRITES ONLY. Reads are deliberately
# absent so a loose matcher can never turn a read into an audit record.
_WRITE_OPS = {
    "transitionJiraIssue": "transition",   # start / close (status change)
    "addCommentToJiraIssue": "comment",    # working notes, PR link, retro
    "editJiraIssue": "edit",               # field/label edits (e.g. blocked)
    "createIssueLink": "link",             # parent/child + blocker links
}
_KEY_RE = re.compile(r"\b[A-Z][A-Z0-9]+-\d+\b")  # JIRA key, e.g. EXEC-456


def _op(tool_name: str):
    """The write op for a tool name, or None if it is not a lifecycle write."""
    for verb, op in _WRITE_OPS.items():
        if tool_name.endswith(verb):
            return op
    return None


def _issue_key(tool_input: dict):
    """Best-effort issue key. Most writes carry `issueIdOrKey`; createIssueLink
    carries the key in nested link refs, so fall back to a key-pattern scan."""
    for k in ("issueIdOrKey", "issueKey", "key"):
        v = tool_input.get(k)
        if isinstance(v, str) and v:
            return v
    m = _KEY_RE.search(json.dumps(tool_input))
    return m.group(0) if m else None


def main() -> int:
    try:
        raw = "" if sys.stdin is None or sys.stdin.isatty() else sys.stdin.read()
        payload = json.loads(raw) if raw.strip() else {}
    except Exception:
        # Invoked on a write but the payload was unreadable: a real miss.
        aso_audit.append({"event": "lifecycle_write", "status": "error",
                          "error": "unparseable hook payload"})
        return 0
    try:
        op = _op(payload.get("tool_name") or "")
        if op is None:
            return 0  # a read slipped past the matcher — stay silent
        tool_input = payload.get("tool_input") or {}
        aso_audit.append({
            "event": "lifecycle_write",
            "op": op,
            "issue": _issue_key(tool_input),
            "tool": payload.get("tool_name"),
            "status": "ok",
            "session_id": payload.get("session_id"),
        })
    except Exception as e:
        aso_audit.append({"event": "lifecycle_write", "status": "error",
                          "error": repr(e), "session_id": payload.get("session_id")})
    return 0  # never break a session


if __name__ == "__main__":
    raise SystemExit(main())
