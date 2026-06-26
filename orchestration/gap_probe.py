#!/usr/bin/env python3
"""Dogfood-gate gap-probe (EXEC-456 Slice 3).

Deterministic, LLM-free. Reads the ambient-audit log (Slices 1/2/3 records) and
git history over a window, then reports whether the agent actually recorded the
work it did:

  PRIMARY  — worked-but-didn't-record: EXEC/IDEA keys with git commits in the
             window that have NO `lifecycle_write` recording in the audit log.
             A robust set difference (git keys − recorded keys); this is the
             dogfood-gate signal the gate reads.
  SECONDARY — ambient vs prompted classification of the writes that DID happen.
             ambient = a write not preceded by a user prompt (Fred's boundary,
             2026-06-26). A heuristic — see the CAVEAT in format_report.

Design (per the pipeline-monitoring lesson): no external watchdog and no LLM —
the probe is in-tree and reads only the local audit log + `git log`. Success is
a *rate/trend* across real sessions, not a single green check; run it on the
reporting-cadence (weekly) and read the miss list.

The pure functions (parse_records / select / classify_writes / parse_git_keys /
build_report / format_report) take their inputs as arguments so the logic is
unit-tested without touching the filesystem or git; only collect_git_activity
and main() do I/O.
"""
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone

import aso_audit

PREFIXES = ("EXEC", "IDEA")  # the two Jira projects; avoids matching random IDs
_BOUNDARY_EVENTS = ("user_prompt", "lifecycle_write", "session_start")
MAX_EVIDENCE = 3  # commit lines shown per miss key before an explicit "+N more"


def parse_records(lines):
    """Parse JSONL lines into dict records, tolerating blank/garbage lines."""
    out = []
    for ln in lines:
        ln = ln.strip()
        if not ln:
            continue
        try:
            rec = json.loads(ln)
        except Exception:
            continue
        if isinstance(rec, dict):
            out.append(rec)
    return out


def parse_ts(rec):
    """Parse a record's UTC `ts` into an aware datetime, or None if unusable."""
    try:
        return datetime.fromisoformat(rec.get("ts"))
    except (TypeError, ValueError):
        return None


def is_synthetic(rec):
    """Manual proof records (DEPLOY-SMOKE-*) must never pollute real counts."""
    return (rec.get("session_id") or "").startswith("DEPLOY-SMOKE")


def select(records, now, days):
    """Records inside the window [now - days, now], excluding synthetic ones.
    Records without a parseable ts cannot be placed in the window and are dropped."""
    cutoff = now - timedelta(days=days)
    kept = []
    for r in records:
        if is_synthetic(r):
            continue
        ts = parse_ts(r)
        if ts is None or ts < cutoff:
            continue
        kept.append(r)
    return kept


def classify_writes(records):
    """Classify each lifecycle_write as prompted / ambient / unknown.

    Groups by session_id FIRST, then orders by ts within the session — the log
    interleaves concurrent sessions, so a global sort would let one session's
    prompt mislabel another's write. Within a session, a write is `prompted` if
    the most recent preceding boundary event is a user_prompt, else `ambient`
    (the agent is mid self-driven run). A session with NO recorded prompt yields
    `unknown` — its timeline is incomplete (pre-deploy, or a UserPromptSubmit
    gap); guessing would overstate ambient.
    """
    by_session = {}
    for r in records:
        if r.get("event") in _BOUNDARY_EVENTS:
            by_session.setdefault(r.get("session_id"), []).append(r)

    writes = []
    for sid, recs in by_session.items():
        recs_sorted = sorted(recs, key=lambda r: r.get("ts") or "")
        has_prompt = any(r.get("event") == "user_prompt" for r in recs_sorted)
        last = None  # most recent boundary event type within this session
        for r in recs_sorted:
            ev = r.get("event")
            if ev == "user_prompt":
                last = "user_prompt"
            elif ev == "session_start":
                last = "start"
            elif ev == "lifecycle_write":
                if not has_prompt:
                    cls = "unknown"
                elif last == "user_prompt":
                    cls = "prompted"
                else:
                    cls = "ambient"
                writes.append({
                    "session_id": sid,
                    "issue": r.get("issue"),
                    "op": r.get("op"),
                    "ts": r.get("ts"),
                    "classification": cls,
                })
                last = "lifecycle_write"
    return writes


def parse_git_keys(log_text, prefixes=PREFIXES):
    """Map each referenced Jira key -> list of the commit lines that mention it.
    Only the configured project prefixes are matched (no stray uppercase IDs)."""
    key_re = re.compile(r"\b(?:%s)-\d+\b" % "|".join(prefixes))
    activity = {}
    for line in log_text.splitlines():
        for key in key_re.findall(line):
            activity.setdefault(key, []).append(line.strip())
    return activity


def collect_git_activity(repo, since, prefixes=PREFIXES):
    """Run `git log --since` in `repo` and extract Jira-key references.
    Best-effort: a missing/!git repo returns {} rather than raising."""
    try:
        res = subprocess.run(
            ["git", "-C", repo, "log", "--since=%s" % since, "--pretty=format:%h %s"],
            capture_output=True, text=True, timeout=30,
        )
    except Exception:
        return {}
    if res.returncode != 0:
        return {}
    return parse_git_keys(res.stdout, prefixes)


def build_report(records, git_activity, now, days):
    """Assemble the report dict from raw audit records + git activity."""
    sel = select(records, now, days)
    writes = classify_writes(sel)
    recorded_keys = sorted({w["issue"] for w in writes if w["issue"]})
    git_keys = set(git_activity)
    misses = {k: git_activity[k] for k in git_activity if k not in recorded_keys}
    recorded_no_git = sorted(set(recorded_keys) - git_keys)

    counts = {"prompted": 0, "ambient": 0, "unknown": 0}
    for w in writes:
        counts[w["classification"]] = counts.get(w["classification"], 0) + 1

    return {
        "window_days": days,
        "generated_for": now.isoformat(),
        "total_writes": len(writes),
        "writes": writes,
        "recorded_keys": recorded_keys,
        "misses": misses,
        "recorded_no_git": recorded_no_git,
        "git_keys": sorted(git_keys),
        "classification": counts,
    }


def format_report(report):
    """Human-readable report. The robust miss list leads; the heuristic ambient
    rate is clearly secondary and carries its boundary caveat."""
    L = [
        "ASO dogfood-gate gap-probe — last %sd (as of %s)"
        % (report["window_days"], report["generated_for"]),
        "",
    ]

    misses = report["misses"]
    L.append("## Worked-but-didn't-record  (%d key(s))  [PRIMARY SIGNAL]" % len(misses))
    if not misses:
        L.append("  none — every EXEC/IDEA key with git activity in the window has a recorded Jira write.")
    else:
        L.append("  git commits reference these keys, but NO lifecycle_write was logged for them.")
        L.append("  (Commits predating the audit-hook deploy will appear here until the window rolls past it.)")
        for k in sorted(misses):
            evidence = misses[k]
            L.append("  - %s  (%d commit(s))" % (k, len(evidence)))
            for ev in evidence[:MAX_EVIDENCE]:
                L.append("      %s" % ev)
            if len(evidence) > MAX_EVIDENCE:
                L.append("      ... +%d more commit(s)" % (len(evidence) - MAX_EVIDENCE))
    L.append("")

    c = report["classification"]
    L.append("## Ambient vs prompted  [SECONDARY — heuristic]")
    L.append("  writes recorded in window: %d  (ambient=%d, prompted=%d, unknown=%d)"
             % (report["total_writes"], c["ambient"], c["prompted"], c["unknown"]))
    L.append("  Boundary (Fred 2026-06-26): ambient = a write not preceded by a user prompt.")
    L.append("  CAVEAT: read literally this labels the first write right after a prompt 'prompted'")
    L.append("  even when it is an unprompted lifecycle action (e.g. auto transition -> In Progress),")
    L.append("  so the rate UNDERCOUNTS ambient. Treat per-write detail as truth, not the headline rate.")
    L.append("  'unknown' = the session recorded no prompt (pre-deploy, or a UserPromptSubmit gap).")
    L.append("")

    rng = report["recorded_no_git"]
    L.append("## Recorded-without-git  (%d key(s))  [informational]" % len(rng))
    if rng:
        L.append("  Jira writes for keys with no git commit in the window (often comment-only/admin work):")
        L.append("  " + ", ".join(rng))
    else:
        L.append("  none.")
    return "\n".join(L)


def main(argv=None):
    import argparse
    p = argparse.ArgumentParser(description="ASO dogfood-gate gap-probe (EXEC-456 Slice 3)")
    p.add_argument("--days", type=int, default=7, help="window size in days (default 7)")
    p.add_argument("--repo", default=".", help="git repo to scan for EXEC/IDEA refs (default cwd)")
    p.add_argument("--log", default=None, help="audit log path (default: ASO_AUDIT_LOG or ~/.claude/aso/...)")
    p.add_argument("--json", action="store_true", help="emit the raw report as JSON")
    args = p.parse_args(argv)

    log_path = args.log or aso_audit.log_path()
    try:
        with open(log_path, encoding="utf-8") as fh:
            records = parse_records(fh)
    except FileNotFoundError:
        records = []

    now = datetime.now(timezone.utc)
    since = (now - timedelta(days=args.days)).date().isoformat()
    git_activity = collect_git_activity(args.repo, since)
    report = build_report(records, git_activity, now, args.days)

    print(json.dumps(report, indent=2) if args.json else format_report(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
