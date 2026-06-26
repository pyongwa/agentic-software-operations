#!/usr/bin/env python3
"""Tests for the dogfood-gate gap-probe (EXEC-456 Slice 3).

The probe is deterministic and LLM-free (per the pipeline-monitoring lesson: no
external watchdog, instrumentation lives in-tree). It reads the ambient-audit
log + git history over a window and reports:

  PRIMARY  — worked-but-didn't-record: EXEC/IDEA keys with git commits in the
             window that have NO lifecycle_write recording. A robust set
             difference; this is the dogfood-gate signal.
  SECONDARY — ambient vs prompted classification of the writes that DID happen.
             ambient = a write not preceded by a user prompt (Fred's boundary,
             2026-06-26). A heuristic, labeled as such (see the boundary caveat
             in gap_probe.format_report).

Correctness this suite pins down:
  - records are grouped by session_id BEFORE ordering by ts (the log interleaves
    concurrent sessions — a global sort cross-contaminates the timeline)
  - synthetic DEPLOY-SMOKE records are excluded
  - a session with writes but zero prompts -> writes are 'unknown', not 'ambient'
    (the prompt timeline is incomplete; guessing would overstate ambient)
  - the miss list is keyed by EXEC-NNN, not by session (commits carry no session)
"""
import json
import os
import sys
import unittest
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import gap_probe  # noqa: E402

NOW = datetime(2026, 6, 26, 20, 0, 0, tzinfo=timezone.utc)


def _ts(h, m=0, s=0, day=26):
    return datetime(2026, 6, day, h, m, s, tzinfo=timezone.utc).isoformat()


def _rec(event, sid, h, m=0, s=0, day=26, **extra):
    return {"ts": _ts(h, m, s, day), "event": event, "session_id": sid, **extra}


class ClassifyWritesTest(unittest.TestCase):
    def _by_key(self, writes):
        return {(w["session_id"], w["issue"]): w["classification"] for w in writes}

    def test_first_write_after_prompt_is_prompted(self):
        recs = [
            _rec("user_prompt", "A", 10),
            _rec("lifecycle_write", "A", 10, 1, issue="EXEC-1", op="transition"),
        ]
        writes = gap_probe.classify_writes(recs)
        self.assertEqual(writes[0]["classification"], "prompted")

    def test_subsequent_write_in_same_run_is_ambient(self):
        recs = [
            _rec("user_prompt", "A", 10),
            _rec("lifecycle_write", "A", 10, 1, issue="EXEC-1", op="transition"),
            _rec("lifecycle_write", "A", 10, 2, issue="EXEC-1", op="comment"),
        ]
        cls = [w["classification"] for w in gap_probe.classify_writes(recs)]
        self.assertEqual(cls, ["prompted", "ambient"])

    def test_new_prompt_makes_the_next_write_prompted_again(self):
        recs = [
            _rec("user_prompt", "A", 10),
            _rec("lifecycle_write", "A", 10, 1, issue="EXEC-1", op="comment"),
            _rec("user_prompt", "A", 11),
            _rec("lifecycle_write", "A", 11, 1, issue="EXEC-2", op="transition"),
        ]
        cls = [w["classification"] for w in gap_probe.classify_writes(recs)]
        self.assertEqual(cls, ["prompted", "prompted"])

    def test_write_with_no_prompts_in_session_is_unknown(self):
        # Pre-deploy session (no UserPromptSubmit hook) -> cannot classify.
        recs = [
            _rec("session_start", "A", 9, status="injected"),
            _rec("lifecycle_write", "A", 10, issue="EXEC-1", op="comment"),
        ]
        writes = gap_probe.classify_writes(recs)
        self.assertEqual(writes[0]["classification"], "unknown")

    def test_sessions_grouped_not_globally_ordered(self):
        # Interleaved: A.prompt, B.write, A.write (global order).
        # A global sort would see A.prompt immediately before B.write and wrongly
        # mark B's write 'prompted'. Grouped: B has no prompt -> unknown; A's
        # write is preceded (in A) by A.prompt -> prompted.
        recs = [
            _rec("user_prompt", "A", 10, 0),
            _rec("lifecycle_write", "B", 10, 1, issue="EXEC-9", op="comment"),
            _rec("lifecycle_write", "A", 10, 2, issue="EXEC-1", op="comment"),
        ]
        cls = self._by_key(gap_probe.classify_writes(recs))
        self.assertEqual(cls[("B", "EXEC-9")], "unknown")
        self.assertEqual(cls[("A", "EXEC-1")], "prompted")


class SelectWindowTest(unittest.TestCase):
    def test_synthetic_deploy_smoke_excluded(self):
        recs = [
            _rec("lifecycle_write", "DEPLOY-SMOKE-2026-06-26", 19, issue="EXEC-456", op="transition"),
            _rec("lifecycle_write", "real", 19, 30, issue="EXEC-456", op="comment"),
        ]
        kept = gap_probe.select(recs, NOW, days=7)
        self.assertEqual([r["session_id"] for r in kept], ["real"])

    def test_old_records_outside_window_filtered(self):
        recs = [
            _rec("lifecycle_write", "old", 12, issue="EXEC-1", op="comment", day=10),  # 16 days back
            _rec("lifecycle_write", "new", 12, issue="EXEC-2", op="comment", day=25),  # 1 day back
        ]
        kept = gap_probe.select(recs, NOW, days=7)
        self.assertEqual([r["session_id"] for r in kept], ["new"])


class GitKeyParseTest(unittest.TestCase):
    def test_parses_exec_and_idea_keys_with_subjects(self):
        log = (
            "a1b2c3d [EXEC-463] unify Trajectory into Career History (#274)\n"
            "e4f5a6b [EXEC-462] Promote Double R\n"
            "0011223 chore: tidy build script\n"
            "9988776 [IDEA-25] capture observability gap\n"
        )
        keys = gap_probe.parse_git_keys(log)
        self.assertIn("EXEC-463", keys)
        self.assertIn("EXEC-462", keys)
        self.assertIn("IDEA-25", keys)
        self.assertNotIn("0011223", keys)
        # subjects are retained as evidence
        self.assertTrue(any("Trajectory" in s for s in keys["EXEC-463"]))

    def test_ignores_unknown_prefixes(self):
        keys = gap_probe.parse_git_keys("abc123 [JIRA-9] not one of our projects\n")
        self.assertEqual(keys, {})


class BuildReportTest(unittest.TestCase):
    def test_miss_list_is_git_keys_minus_recorded(self):
        recs = [
            _rec("user_prompt", "A", 10),
            _rec("lifecycle_write", "A", 10, 1, issue="EXEC-1", op="transition"),
        ]
        git = {"EXEC-1": ["a1 did x"], "EXEC-2": ["b2 did y"]}
        report = gap_probe.build_report(recs, git, NOW, days=7)
        self.assertEqual(set(report["misses"]), {"EXEC-2"})
        self.assertIn("EXEC-1", report["recorded_keys"])

    def test_recorded_without_git_reported_separately(self):
        recs = [
            _rec("user_prompt", "A", 10),
            _rec("lifecycle_write", "A", 10, 1, issue="EXEC-3", op="comment"),
        ]
        report = gap_probe.build_report(recs, {}, NOW, days=7)
        self.assertEqual(set(report["recorded_no_git"]), {"EXEC-3"})
        self.assertEqual(report["misses"], {})

    def test_classification_counts_present(self):
        recs = [
            _rec("user_prompt", "A", 10),
            _rec("lifecycle_write", "A", 10, 1, issue="EXEC-1", op="transition"),
            _rec("lifecycle_write", "A", 10, 2, issue="EXEC-1", op="comment"),
            _rec("lifecycle_write", "B", 11, issue="EXEC-5", op="comment"),  # no prompt -> unknown
        ]
        report = gap_probe.build_report(recs, {}, NOW, days=7)
        self.assertEqual(report["classification"]["prompted"], 1)
        self.assertEqual(report["classification"]["ambient"], 1)
        self.assertEqual(report["classification"]["unknown"], 1)

    def test_empty_inputs_do_not_crash(self):
        report = gap_probe.build_report([], {}, NOW, days=7)
        self.assertEqual(report["misses"], {})
        self.assertEqual(report["total_writes"], 0)
        out = gap_probe.format_report(report)
        self.assertIsInstance(out, str)

    def test_format_report_leads_with_misses_and_flags_heuristic(self):
        recs = [_rec("lifecycle_write", "A", 10, issue="EXEC-1", op="comment")]
        report = gap_probe.build_report(recs, {"EXEC-2": ["x missed work"]}, NOW, days=7)
        out = gap_probe.format_report(report)
        # the robust signal (misses) appears before the heuristic section
        self.assertLess(out.index("EXEC-2"), out.lower().index("heuristic"))

    def test_format_caps_evidence_with_explicit_overflow(self):
        many = ["c%d did work on it" % i for i in range(gap_probe.MAX_EVIDENCE + 4)]
        report = gap_probe.build_report([], {"EXEC-9": many}, NOW, days=7)
        out = gap_probe.format_report(report)
        # not a silent cap: the dropped count is stated
        self.assertIn("+4 more commit(s)", out)
        self.assertIn("(%d commit(s))" % len(many), out)


class RealShapedLogTest(unittest.TestCase):
    """The live log today has session_start + lifecycle_write but NO user_prompt
    events (pre-deploy) — so every write must classify 'unknown', and the probe
    must not crash on it (validate-parsers-against-real-files)."""

    REAL = [
        {"ts": "2026-06-26T18:25:41.912250+00:00", "event": "session_start", "status": "injected", "skills": 11, "session_id": "DEPLOY-SMOKE-2026-06-26"},
        {"ts": "2026-06-26T18:25:41.930871+00:00", "event": "lifecycle_write", "op": "transition", "issue": "EXEC-456", "status": "ok", "session_id": "DEPLOY-SMOKE-2026-06-26"},
        {"ts": "2026-06-26T19:15:07.511782+00:00", "event": "session_start", "status": "injected", "skills": 11, "session_id": "6e047dcc"},
        {"ts": "2026-06-26T19:19:17.652212+00:00", "event": "lifecycle_write", "op": "comment", "issue": "EXEC-456", "status": "ok", "session_id": "6e047dcc"},
    ]

    def test_real_log_classifies_unknown_and_excludes_synthetic(self):
        report = gap_probe.build_report(self.REAL, {}, NOW, days=7)
        # the DEPLOY-SMOKE write is dropped; only the real-session write counts
        self.assertEqual(report["total_writes"], 1)
        self.assertEqual(report["classification"]["unknown"], 1)
        self.assertEqual(set(report["recorded_keys"]), {"EXEC-456"})

    def test_parse_records_tolerates_blank_and_bad_lines(self):
        lines = ['{"event":"user_prompt","session_id":"A","ts":"%s"}' % _ts(10),
                 "", "   ", "}{ not json", "not even close"]
        recs = gap_probe.parse_records(lines)
        self.assertEqual(len(recs), 1)


if __name__ == "__main__":
    unittest.main()
