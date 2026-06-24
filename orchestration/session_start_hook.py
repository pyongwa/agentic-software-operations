#!/usr/bin/env python3
"""SessionStart hook (EXEC-431): surface the lifecycle orientation at session start.

Reads the skills' `lifecycle:` frontmatter (via gen_orchestration.load_skills) and
injects a compact orientation — the session-start and project-start skills — into
the model's context so the orchestration model is *executed*, not just documented.

Fail-safe by construction: any error exits 0 with no output. A hook must never
break a session. Wired in .claude/settings.json -> hooks.SessionStart.
"""
import sys, json, os

def main() -> int:
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
        return 0
    except Exception:
        return 0  # never break a session

if __name__ == "__main__":
    raise SystemExit(main())
