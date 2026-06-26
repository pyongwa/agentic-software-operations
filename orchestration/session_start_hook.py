#!/usr/bin/env python3
"""SessionStart hook (EXEC-431): surface the lifecycle orientation at session start.

Reads the skills' `lifecycle:` frontmatter (via gen_orchestration.load_skills) and
injects a compact orientation — the session-start and project-start skills — into
the model's context so the orchestration model is *executed*, not just documented.

Fail-safe by construction: any error exits 0 with no output. A hook must never
break a session. Wired in .claude/settings.json -> hooks.SessionStart.

Audit (EXEC-456): every fire appends one best-effort JSONL record to the audit
log (ASO_AUDIT_LOG, default ~/.claude/aso/ambient-audit.jsonl) so a hook that
silently fails to fire becomes *detectable*. The audit never writes to stdout
(Claude Code parses stdout as the hook result) and never raises (a logging
failure cannot break the session or suppress the orientation).
"""
import sys, json, os

# Shared appender (EXEC-456 Slice 2 factored the audit out of this hook so the
# lifecycle-write hook reuses one format + one fail-safe guarantee).
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from aso_audit import append as _audit  # noqa: E402


def _session_id():
    """Claude Code passes the hook payload (incl. session_id) on stdin. Read it
    defensively — never block on a TTY, never raise."""
    try:
        if sys.stdin is None or sys.stdin.isatty():
            return None
        raw = sys.stdin.read()
        return (json.loads(raw) or {}).get("session_id") if raw.strip() else None
    except Exception:
        return None


def main() -> int:
    sid = _session_id()
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import gen_orchestration as g
        skills = g.load_skills()
        order = {p: i for i, p in enumerate(g.PHASES)}
        lines = [
            "Skill lifecycle orientation (generated from each skill's `lifecycle` frontmatter; "
            "full map: meta/orchestration/WORKFLOW.md).",
            "Phases run: session-start -> project-start -> execution-loop -> work-close; "
            "on-trigger skills fire on demand.",
        ]
        for phase in ("session-start", "project-start"):
            members = sorted([s for s in skills if s["phase"] == phase], key=lambda s: s["name"])
            if members:
                lines.append(f"\n{phase}:")
                for s in members:
                    lines.append(f"  - {s['name']} ({s['cadence']}): {s['trigger']}")
        nloop = sum(1 for s in skills if s["phase"] == "execution-loop")
        nclose = sum(1 for s in skills if s["phase"] == "work-close")
        lines.append(f"\nThen: {nloop} execution-loop skill(s) per unit of work, "
                     f"{nclose} work-close skill(s) before shipping.")
        context = "\n".join(lines)
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": context,
            }
        }))
        _audit({"event": "session_start", "status": "injected",
                "skills": len(skills), "session_id": sid})
        return 0
    except Exception as e:
        _audit({"event": "session_start", "status": "error",
                "error": repr(e), "session_id": sid})
        return 0  # never break a session

if __name__ == "__main__":
    raise SystemExit(main())
