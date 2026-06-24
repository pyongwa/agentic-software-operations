---
name: persistence-handoff
description: Use the tracker + knowledge base as extended memory across sessions. Maintain an anchor record, a current-state page, and exactly one concrete Next Action so the next session resumes in <=5 calls. Enforces decisions->knowledge-base / status->tracker, and explicit backfill. Use at session start (to load context) and session end (to hand off).
---

# Persistence & Handoff (C5)

The tracker + knowledge base are an **off-the-shelf RAG / extended memory** for
both human and agent. This skill keeps them coherent across sessions.

## The handoff loop

**anchor record → current-state page → exactly one concrete Next Action.**
The next session reads the anchor, the current-state page, and does the Next
Action — it trusts the handoff rather than replanning from scratch. Target: full
context in **≤ 5 calls**.

## The rule

**Decisions go to the knowledge base; status goes to the tracker.** If another
session needs it to understand *why*, it's a decision → knowledge base. If it
records *that something happened*, it's status → tracker.

## References

- `references/session-protocol.md` — the ≤5-call **Session Start**, the
  **Session End** handoff, the decisions/status rule, and **Backfill** rules.
- `references/current-state-page.md` — one per active project; its **Next Action**
  is the single source of "what to do next".
- `references/anchor-ticket.md` — the design/architecture/session-tracking ticket
  (label `session-anchor`).

## Principles

- **Exactly one Next Action** — concrete, not a list.
- **Generic** — no employer space keys / page IDs; read targets from the config.
- **Backfill is explicit** — search the tracker first, never duplicate records,
  separate delivery progress from admin/cleanup, label backfilled work clearly.

## Three-layer knowledge architecture (pattern; full build is later)

For large source corpora: *vector* (retrieve entry points) → *graph* (traverse
relationships, the system of record) → *wiki* (human-readable record / RAG
source). Index everything cheaply; spend the LLM budget on a content-aware
sample. v0.1 references this pattern; a full corpus KG is out of scope.
