#!/usr/bin/env python3
"""Tests for the skill-orchestration generator (EXEC-431). Stdlib unittest, no deps.

Run: python3 meta/orchestration/test_gen_orchestration.py
"""
import unittest, tempfile, os
from pathlib import Path
import gen_orchestration as g


FM_FULL = """---
name: demo-skill
description: A demo skill.
lifecycle:
  phase: execution-loop
  cadence: loop-until-done
  trigger: "open -> close on any ticket"
---
# body
"""

FM_NONE = """---
name: bare-skill
description: No lifecycle here, long description that should be truncated for the trigger fallback so it stays compact.
---
body
"""

FM_BAD = """---
name: bad-skill
description: bad
lifecycle:
  phase: not-a-phase
  cadence: on-demand
---
"""


class ParseTests(unittest.TestCase):
    def test_parses_nested_lifecycle(self):
        fm = g.parse_frontmatter(FM_FULL)
        self.assertEqual(fm["name"], "demo-skill")
        self.assertEqual(fm["lifecycle"]["phase"], "execution-loop")
        self.assertEqual(fm["lifecycle"]["cadence"], "loop-until-done")
        self.assertEqual(fm["lifecycle"]["trigger"], "open -> close on any ticket")

    def test_no_frontmatter_returns_empty(self):
        self.assertEqual(g.parse_frontmatter("# just a heading\n"), {})

    def test_scalar_strips_quotes(self):
        self.assertEqual(g._scalar('"hi"'), "hi")
        self.assertEqual(g._scalar("plain"), "plain")


class LoadValidateTests(unittest.TestCase):
    def _fixture(self, files: dict) -> Path:
        d = Path(tempfile.mkdtemp())
        for name, text in files.items():
            (d / name).mkdir(parents=True, exist_ok=True)
            (d / name / "SKILL.md").write_text(text)
        return d

    def test_load_classifies_and_defaults(self):
        g.SKILLS_DIR = self._fixture({"demo-skill": FM_FULL, "bare-skill": FM_NONE})
        skills = {s["name"]: s for s in g.load_skills()}
        self.assertTrue(skills["demo-skill"]["classified"])
        self.assertEqual(skills["demo-skill"]["phase"], "execution-loop")
        # unclassified defaults to on-trigger / on-demand and borrows description as trigger
        self.assertFalse(skills["bare-skill"]["classified"])
        self.assertEqual(skills["bare-skill"]["phase"], "on-trigger")
        self.assertEqual(skills["bare-skill"]["cadence"], "on-demand")
        self.assertLessEqual(len(skills["bare-skill"]["trigger"]), 120)

    def test_validate_flags_bad_phase(self):
        g.SKILLS_DIR = self._fixture({"bad-skill": FM_BAD})
        errs = g.validate(g.load_skills())
        self.assertTrue(any("invalid phase" in e for e in errs))


class RenderTests(unittest.TestCase):
    SK = [
        {"name": "b", "phase": "project-start", "cadence": "on-demand", "trigger": 'has "quotes"', "classified": True},
        {"name": "a", "phase": "execution-loop", "cadence": "loop-until-done", "trigger": "x", "classified": True},
    ]

    def test_yaml_is_deterministic_and_phase_ordered(self):
        out1 = g.render_yaml(self.SK)
        out2 = g.render_yaml(list(reversed(self.SK)))
        self.assertEqual(out1, out2)  # order-independent of input
        # project-start (index 1) sorts before execution-loop (index 2)
        self.assertLess(out1.index("name: b"), out1.index("name: a"))

    def test_yaml_quotes_are_escaped(self):
        self.assertIn(r'trigger: "has \"quotes\""', g.render_yaml(self.SK))

    def test_workflow_groups_by_phase(self):
        wf = g.render_workflow(self.SK)
        self.assertIn("## Project start", wf)
        self.assertIn("## Execution loop", wf)


class CheckModeTests(unittest.TestCase):
    def test_check_detects_stale(self):
        d = Path(tempfile.mkdtemp())
        (d / "demo" ).mkdir()
        (d / "demo" / "SKILL.md").write_text(FM_FULL)
        g.SKILLS_DIR = d
        g.HERE = Path(tempfile.mkdtemp())  # empty output dir → artifacts missing → stale
        self.assertEqual(g.main(["--check"]), 1)
        self.assertEqual(g.main([]), 0)         # generate
        self.assertEqual(g.main(["--check"]), 0)  # now up to date


if __name__ == "__main__":
    unittest.main(verbosity=2)
