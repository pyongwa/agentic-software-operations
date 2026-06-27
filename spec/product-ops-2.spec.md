---
okf_version: "0.1"
type: Specification
title: "Product Ops 2.0 — Normative Spec"
description: "An open, vendor-neutral, LLM-agnostic operating-model framework for AI-operated product operations."
status: Draft
version: "1.0"
spec_license: "CC-BY-4.0"
author: "Fred Chong Rutherford"
tags: [product-ops, agentic, operating-model, jira, confluence, rag, okf]
# --- Typed-edge / provenance profile -------------------------------------
# OKF (markdown + YAML frontmatter) deliberately omits typed edges and
# provenance. This document reuses the typed-edge/provenance profile so the
# framework's relationships and authorship are machine-legible.
provenance:
  authored_by: "Fred Chong Rutherford"
  origin: "Author-originated. Designed LLM-agnostic; reference implementations on Claude and Codex."
  note: "This is the author's framework, open-sourced by the author."
relations:
  - type: reference-implementation
    target: "product-ops-2 (Claude Code plugin)"
  - type: evidence
    target: "Knowledge-graph RAG vs document RAG (Xu et al., LinkedIn, SIGIR '24)"
  - type: evidence
    target: "Atlassian Rovo / Teamwork Graph (vendor-native graph traversal)"
---

# Product Ops 2.0 — Normative Spec

An open, vendor-neutral, **LLM-agnostic operating-model framework** for
AI-operated product operations. This document is the normative specification; it
is platform-portable and names no specific employer, tracker, stack, or vendor as
a requirement. A reference implementation (a Claude Code plugin) accompanies it,
but the framework is defined here, not by the implementation.

## Governing principle (the spine)

> **Use agentic tools for utility writing** (reporting, tracking, tracing,
> developing material to act as a RAG) **and save human creativity for
> creativity, judgment, and novel ideation.**

Two structural consequences run through every component:

- **The machine/human line.** Every component either automates *utility writing*
  or *protects/feeds human judgment*. If a proposed component does neither, it is
  out of scope. This is the inclusion test for the whole framework.
- **The generate⇄audit dual.** Every utility-writing component runs in two modes:
  **generate** (draft-first — the machine produces the artifact) and **audit**
  (the machine scores a human- or machine-produced artifact against the minimum
  standard). The dual recurs at every layer.

## Components

### C0 — Operating Model & Hierarchy

- **OpEx vs CapEx split.** Strategy/discovery is **OpEx** — an "Idea": the need,
  the opportunity, the big-picture plan. Execution is **CapEx** —
  Epic → Story → Task → Bug → Subtask. The Idea tier is the only home for "why".
- **Generic hierarchy.** Program → Project → Initiative → Epic → Story / Task /
  Bug → Subtask. The framework is generic; **team specifics live in config**,
  never hard-coded.
- **Membership is label-based, not date-based.** Grouping (PI, OKR, ART, flow) is
  carried by labels; a multi-labeled item appears in every matching rollup.

### C1 — Doc-Minimums Engine (generate + audit)

- Minimum standards for **PRD, SDD, Design Doc, Release Notes, Operational
  Procedure, and Work-Artifact/Iteration records** that an agent can **generate**
  (draft-first) or **audit** (score a human-written doc against the minimum and
  report gaps).
- Living documents carry a **Decisions** table (what was decided, alternatives
  rejected, rationale) and a **Change Log** (what changed and why). Decisions feed
  the retrospective (C6).
- Self-conformance: a framework spec is itself written to this standard.

### C2 — Tracker Operation

- Agentic estimation, ticket formation and **decomposition** (a bundled task →
  one ticket per item), **acceptance-criteria authoring**, hierarchy **audit**
  (stale / duplicate / drift), and import building from consolidated data.
- **Dry-run before apply** for any write; no tracker mutation without explicit
  approval. Persona-driven ticket templates. Acceptance criteria *are* the test
  checklist (handoff to C3).
- **Page every query** (cursor + dedupe by key); never trust a first page or a
  reported total count.

### C3 — AC → Tests Bridge

- Acceptance criteria translate into **working tests** and build-breaking
  **conformance gates**. A conformance gate is a test that keeps the artifact
  honest: validate-by-counts, freshness gates, snapshot/source reconciliation,
  no-raw-literal rules.
- The gate is the mechanism that makes the framework's disciplines durable rather
  than aspirational — without it, standards degrade within a few sessions.

### C4 — Reporting & Cadence

- One-off and recurring (weekly) reports, posted **simultaneously** to the tracker
  (Epic/Idea comment), the knowledge base (a weekly page), and the chat channel —
  plus an **executive variant**.
- **One unit = one comment / one message per period** — a discrete audit trail;
  periods are never merged.
- Tracker = system of record; chat = supporting evidence. Every claim labeled
  **verified vs. inferred**; reconstructed history is never represented as
  verified fact.
- **Execution-aware rollup**: completion rolls up from child work, never trusting
  a parent's status alone; distinct completion models are never silently mixed.

### C5 — Persistence / RAG Substrate & Handoff

- The tracker + knowledge base act as an **off-the-shelf RAG / extended memory**
  for both human and agent. Rule: **decisions go to the knowledge base; status
  goes to the tracker.**
- **Session-handoff loop**: an anchor record → a current-state page → exactly one
  concrete **Next Action**. The next session trusts the handoff rather than
  replanning from scratch.
- **Three-layer knowledge architecture** for source corpora: *vector* (semantic
  retrieval — find entry points) → *graph* (relationship traversal, the system of
  record) → *wiki* (human-readable record/projection, RAG source). Index
  everything cheaply; spend the expensive LLM budget only on a content-aware
  sample.
- **Backfill is explicit**: search the tracker first, never duplicate records,
  separate delivery progress from admin/cleanup, label backfilled work clearly.
- **Evidence base.** Traversing the structured graph rather than chunk-and-embed
  prose is independently supported: Atlassian's Rovo / Teamwork-Graph position
  argues graph traversal over structured work data is cheaper and more accurate
  than document-RAG, and Xu et al. (LinkedIn, SIGIR '24) report a large MRR gain
  and reduced resolution time for knowledge-graph RAG vs. plain-text RAG in
  production. Bidirectional linking + typed cross-references are the lightweight
  expression of that result.

### C6 — Retrospective / Self-Audit

- Reads **estimate-vs-actual**, **requirement drift**, and **delivery/freshness
  reconciliation**, then proposes concrete SDLC refinements. The only component
  whose subject is the framework's own operation.
- **Inputs (hooks):** doc *Change Log* entries (requirement drift) + tracker
  *closing/Actuals* records (estimate-vs-actual) + reporting
  *reconciliation/freshness* gates (delivery truth).

## Cross-cutting operating principles

1. **LLM-independent at runtime** — local-default intelligence; the LLM is an
   opt-in accelerator, never a required runtime dependency.
2. **Draft-first / explicit-apply** — generate a draft; never write to an external
   system without approval.
3. **Generate⇄audit dual** — every component runs in both modes.
4. **Verified vs. inferred** — label the provenance of every claim.
5. **Validate by counts** — reconcile before publish/handoff.
6. **Decisions in the knowledge base; status in the tracker.**
7. **Generic framework; specifics in config.**
8. **Local-first** — keep generated operational data local; commit converters /
   docs / fixtures, not raw exports.
9. **A conformance gate keeps the system honest.**
10. **Bidirectional linking everywhere** — coherence is the product.

## Required platform bindings

The framework binds to existing substrates; it does not re-build them.

- **An agentic tracker / knowledge-base substrate**, bound via **MCP *or*
  CLI-over-API**. The substrate is a requirement; the *binding style* is a
  deployment choice. Use MCP for interactive, exploratory work; prefer a
  **skill-over-CLI** bundle for recurring owned operations — it loads **zero tool
  descriptions until invoked**, the token-economy default consistent with
  local-first and LLM-independence.
- **A chat-channel binding** for the cadence's third post target.
- **A browser / automation binding** for fuller regression testing of UI
  artifacts.
- **Packaging** aligned to the **Agent Skills open standard** and the
  `AGENTS.md` / `CLAUDE.md` convention files.

## What this spec deliberately does NOT do

- It does not mandate a stack — language, web framework, and database are a
  *deployment* choice, not a framework requirement.
- It does not name an employer, tracker keys, space keys, channels, or rosters —
  those are config or out of scope.
- It does not re-build the substrate — it requires it as a binding.

## Authorship & provenance

This framework and this specification are authored by **Fred Chong Rutherford**.
It is designed to be LLM- and platform-independent: the reference implementation
runs on Claude, and the operating model has also been exercised under OpenAI
Codex — the cross-vendor portability is the evidence that this is an operating
model, not a tool feature. The specification is the author's to open-source.

## References

- Open Knowledge Format (OKF) — markdown + YAML frontmatter; the carrier format
  for this spec. This document extends it with a typed-edge / provenance profile.
- Xu et al., *Retrieval-Augmented Generation with Knowledge Graphs for Customer
  Service Question Answering*, SIGIR '24 — evidence base for C5 (graph traversal
  over document-RAG).
- Atlassian Rovo / Teamwork Graph — vendor-native graph traversal over structured
  work data.
