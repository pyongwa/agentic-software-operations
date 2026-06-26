---
name: reporting-cadence
description: Generate one-off and weekly status reports and post them simultaneously to the tracker, the knowledge base, and the chat channel (one comment / one message per period), plus an executive variant. Draft-first, config-driven, verified-vs-inferred, execution-aware rollup. Use for weekly status or any one-off report.
lifecycle:
  phase: work-close
  cadence: on-demand
  trigger: "weekly status report, retrospective rollup, or any one-off / executive status report"
---

# Reporting & Cadence (C4)

Turns status reporting into automated utility-writing with a durable audit trail.
Config-driven — reads targets (tracker keys, KB space, chat channels) from
`productops.toml`; no hard-coded keys, channels, or identity openers.

## What it does (see `references/`)

- **Weekly + one-off report** — `weekly-report.md`. The structure, **one comment /
  one message per period**, verified-vs-inferred, **draft-first**.
- **Three-surface simultaneous post** — `three-surface-post.md`. Tracker + knowledge
  base + chat; tracker = system of record, chat = supporting evidence.
- **Executive variant** — `executive-variant.md`.
- **Execution-aware rollup + reconciliation** — `rollup-and-reconciliation.md`.
  Completion rolls up from child work; the reconciliation record feeds the C6
  retrospective (S7).

## Non-negotiables

- **Draft-first** — produce the full report; post nothing without explicit approval.
- **One unit = one comment / one message per period** — never merge periods.
- **Verified vs. inferred** — label every claim; never present reconstructed
  history as verified.
- **Config-driven** — example values use Nampung; no real channels/keys.
