# Roadmap — Agentic Software Operations

*Direction, not dated commitments.* Items move **exploratory → planned → shipped**. "History"
describes how each product was composed (milestones, no dates). The canonical, always-current copy
of this roadmap is maintained alongside the project; this file mirrors it for the repo.

## The line, and the platform model

Three products that ship independently and compose:

- **Product Ops 2.0** — the operating-model *intelligence*.
- **Atlassian Companion** — the *deterministic* Jira + Confluence substrate binding.
- **Agentic Software Operations** — the **platform**: each headline capability is a
  **Platform feature = Product Ops 2.0 intelligence + Atlassian Companion substrate**.

## Platform features (the forward roadmap)

The split of work shows the boundary: the deterministic substrate work is the Companion's, the
judgment/synthesis is Product Ops 2.0's.

| Feature | What it does | Product Ops 2.0 part | Atlassian Companion part | Status |
| --- | --- | --- | --- | --- |
| **AutoSprint** | Auto-generate & manage sprints from the backlog by velocity & priority. | Decide what to pull in, by velocity + prioritization. | Sprint-operation skill (seed/fill to capacity; dry-run→apply; idempotent). *May* need the Jira board/sprint API — to confirm. | `exploratory` |
| **AutoRetro** | Slice a sprint, analyze comments, write a retro (went-well / needs-improvement / the *one* thing), then measure next sprint and repeat. | The analysis + the "one thing" synthesis; the measure-and-repeat loop. | Sprint-scoped reader (issues + comments + changelog) + a Confluence Retrospective doc type + the deterministic outcome-compare. | `exploratory` |
| **Delivery Dashboard** | Organize work into health metrics — a standalone HTML page driven by a small `.py` bundle that organizes Jira data by status. Ships as a download *and* as instructions an agent can follow to build it. | Define the health metrics. | The `.py` status reader + the standalone renderer. Built from existing status data — no new API surface. | `exploratory` |
| **AutoPI Planning** | Organize the artifacts; from velocity + prioritization, suggest roadmap sequencing & scenarios. | The sequencing suggestions + scenario generation. | Dependency/issue-link reader + velocity history + a draft-plan writer; reuses the decomposer + audit. | `exploratory` |

**Division of labor:** deterministic substrate (Companion) = sprint seeding, status/metrics
extraction, velocity computation, dependency reading, all dry-run/apply writes. LLM judgment
(Product Ops 2.0) = the retro "one thing," the planning suggestions.

## Go-to-market

- **GTM plan** — positioning, channels, launch sequence, and the honest-landscape framing for the
  public releases. *(placeholder — in active discussion; an operational artifact, captured here so the
  roadmap reflects it.)* `exploratory`

## Shipped foundations (composition history)

**Product Ops 2.0** — component model (operating model, doc-minimums, tracker-operation,
AC→tests bridge, reporting & cadence, persistence/RAG & handoff, retrospective) → four reference
skills + public spec + config schema + retro contract → split license + IP-hygiene gate → optional
soft interop with the Companion.

**Atlassian Companion** — Jira ticket-craft method → deterministic bundled-ticket decomposer +
read-only hierarchy audit → Confluence seven doc types + the Idea → PRD → [SDD] → Epic → Story chain
→ skill-lifecycle orchestration + session-start orientation → plugin packaging, cross-runtime → QA
gate → transport seam (soft MCP) → OSS-readiness (IP-clean, evaluation, split license, prior-art doc,
positive provenance) → soft-interop contract.

**Agentic Software Operations** — composition model decided (the Companion supersedes the two
substrate reference skills; Product Ops 2.0's operating-model layer wraps it) → soft-interop contract
→ this bundle distribution.

## Other near-term roadmap

- `planned` Product Ops 2.0 v0.1 provenance release published.
- `planned` Product Ops 2.0 doc-minimums **audit-mode** (score a human doc vs the minimum).
- `planned` Standalone **deterministic Jira-ops CLI** (extract the decomposer + audit).
- `planned` Atlassian Companion public publish; CHANGELOG + status section.
- `planned` Bundle published to a public repository / marketplace.

## Cross-cutting principles

- **Honest-landscape OSS** — name prior art / alternatives / competitors; route readers elsewhere
  when a competitor fits better. Novel + useful + honest about lineage, never "the only solution."
- **Deterministic where it counts** — the substrate is no-LLM and idempotent; the LLM is reserved for
  synthesis and suggestion.
- **Dual-delivery artifacts** — runnable bundle *and* agent-buildable instructions.
- **Roadmap = direction, not dates** — items move exploratory → planned → shipped; the CHANGELOG
  records what actually landed.
