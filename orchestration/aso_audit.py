#!/usr/bin/env python3
"""Shared ambient-audit appender (EXEC-456).

One JSONL record per ambient event to the ASO audit log. Best-effort by
construction: it never raises and never writes to stdout, so observability can
never break a session or corrupt a hook's stdout contract. Both the
SessionStart hook (Slice 1) and the lifecycle-write hook (Slice 2) append
through here, so the audit format and its fail-safe guarantees live in one
place (default log survives plugin reinstall: ~/.claude/, not the cache dir).
"""
import json
import os
from datetime import datetime, timezone

DEFAULT_LOG = "~/.claude/aso/ambient-audit.jsonl"


def log_path() -> str:
    """Resolve the audit log path (ASO_AUDIT_LOG override, else the default)."""
    return os.environ.get("ASO_AUDIT_LOG") or os.path.expanduser(DEFAULT_LOG)


def append(record: dict) -> None:
    """Append one JSONL record, stamped with a UTC `ts`, to the audit log.
    Best-effort: a logging failure (unwritable path, full disk) is swallowed —
    it can never break the caller and never touches stdout."""
    try:
        path = log_path()
        os.makedirs(os.path.dirname(path), exist_ok=True)
        record = {"ts": datetime.now(timezone.utc).isoformat(), **record}
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(record) + "\n")
    except Exception:
        pass
