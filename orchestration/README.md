# Skill orchestration (EXEC-431)

Turns the skills from a pile of independently-triggered capabilities into a coherent
**workflow** by declaring *when in the work lifecycle* each skill fires and at what
*cadence* — in a form that is both human-readable and machine-executable.

## Source of truth: `lifecycle:` frontmatter

Each skill declares its slot in its own `SKILL.md` frontmatter. That is the **only**
hand-maintained input; everything else is generated.

```yaml
---
name: jira-lifecycle
description: ...
lifecycle:
  phase: execution-loop
  cadence: loop-until-done
  trigger: "open -> progress -> PR -> close on any EXEC ticket"
---
```

### Taxonomy (small on purpose)

| `phase` | meaning |
| --- | --- |
| `session-start` | orient before any work |
| `project-start` | frame & structure a new initiative |
| `execution-loop` | repeat until a unit of work closes |
| `work-close` | QA, simplify, ship |
| `on-trigger` | fired on demand by keyword/event (the default) |

| `cadence` | meaning |
| --- | --- |
| `once-per-session` · `once-per-project` · `loop-until-done` · `on-demand` | how often it fires within its phase |

A skill with no `lifecycle` block defaults to `on-trigger` / `on-demand` and is marked
`classified: false` in the registry (so coverage gaps are visible, not silent).

## Generated artifacts (never hand-edit)

`python3 meta/orchestration/gen_orchestration.py` reads every `meta/.claude/skills/*/SKILL.md`
and writes:

- **`skill-orchestration.yaml`** — machine-readable registry (validated; deterministic order).
- **`WORKFLOW.md`** — human-readable end-to-end workflow, grouped by phase.

`gen_orchestration.py --check` exits non-zero if either artifact is stale — wire it into CI
so the generated files can't drift from the frontmatter.

## Executable: the SessionStart hook

`.claude/settings.json` registers a `SessionStart` hook that runs
`session_start_hook.py`, which surfaces the `session-start` + `project-start` skills as
session context — so the orchestration is *acted on*, not just documented. The hook is
**fail-safe**: any error exits 0 with no output (a hook must never break a session).

> The hook fires on the next session started in this repo (or after opening `/hooks` to
> reload config) — SessionStart can't be proven mid-session.

## Tests

`python3 meta/orchestration/test_gen_orchestration.py` — stdlib `unittest`, no deps:
frontmatter parsing, default/classification, validation, deterministic + escaped YAML,
and `--check` staleness detection.

## Scope & extension

Classified now: the Jira pack (`jira`, `jira-workflow`, `jira-persona-driven-tickets`,
`jira-story-points`, `jira-lifecycle`) plus the `work-close` gate
`evaluate-skills-for-open-source`. The generator already scans **all** skills, so a
pyongwa-wide rollout is just adding `lifecycle` blocks to the remaining skills — no tooling
change. Future skills #4 `jira-bundled-ticket-decomposer` (EXEC-427) and #5
`jira-hierarchy-audit` (EXEC-428) get their `lifecycle` block when built; the EXEC-430 QA
gate is the canonical `work-close` sequence.
