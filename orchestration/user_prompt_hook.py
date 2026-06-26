#!/usr/bin/env python3
"""UserPromptSubmit hook (EXEC-456 Slice 3): record the prompt timeline.

Fires when the user submits a prompt and appends one session-tagged
`user_prompt` record to the audit log. This is the timeline the Slice 3
gap-probe reads to classify each jira-lifecycle write as **ambient** (not
preceded by a user prompt) vs **prompted** (per Fred's boundary, 2026-06-26).

Only the FACT that a prompt fired is recorded (event + session_id + ts) — never
the prompt text, which would leak content and bloat the log.

Fail-safe like Slices 1/2: never raises (a hook must not break a session) and
never writes to stdout (Claude Code injects UserPromptSubmit stdout into the
model context; the audit must stay invisible there). A payload we were invoked
on but could not parse is recorded as an `error` — a gap in the prompt timeline
would mislabel a later write as ambient, so it must be surfaced, not dropped.

Wired as a plugin UserPromptSubmit hook (hooks/hooks.json); no matcher (prompt
events are not tool calls).
"""
import json
import sys

import aso_audit


def main() -> int:
    try:
        raw = "" if sys.stdin is None or sys.stdin.isatty() else sys.stdin.read()
        payload = json.loads(raw) if raw.strip() else {}
    except Exception:
        # Invoked on a prompt but the payload was unreadable: a timeline gap.
        aso_audit.append({"event": "user_prompt", "status": "error",
                          "error": "unparseable hook payload"})
        return 0
    try:
        aso_audit.append({
            "event": "user_prompt",
            "status": "ok",
            "session_id": payload.get("session_id"),
        })
    except Exception as e:
        aso_audit.append({"event": "user_prompt", "status": "error",
                          "error": repr(e), "session_id": payload.get("session_id")})
    return 0  # never break a session


if __name__ == "__main__":
    raise SystemExit(main())
