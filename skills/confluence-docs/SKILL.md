---
name: confluence-docs
description: Use when creating, updating, or referencing any Confluence page — PRDs, work artifacts, iteration records, release notes, or operational procedures. Loads the five Confluence document types, PRD structure and full chain (IDEA → PRD → Epic → Story), bidirectional linking rules, PRD as living document (Change Log and Decisions log), work artifact iteration history format, release note structure, and operational procedure structure.
lifecycle:
  phase: project-start
  cadence: on-demand
  trigger: "authoring/updating Confluence docs across the lifecycle — PRD & design docs (project-start), work-artifact/iteration records (execution), release notes (work-close), operational procedures (governing); owns the IDEA->PRD->Epic->Story chain"
---

# Confluence Documentation

> **Transport:** the Confluence operations here (get / create / update page) resolve through the [Atlassian transport contract](../../../atlassian-transport/transport-contract.md) — the **Rovo MCP** by default, a **REST** adapter (API token) when no MCP is present. Name the *operation*, not a hardcoded tool.

## Document Types

Confluence serves seven document purposes. Each has a distinct trigger, structure, and relationship to the sprint retrospective. **Templates for each live in [`references/`](references/)** — generated docs should start from the template, not from scratch.

| Type | Purpose | Feeds retrospective? | Template |
|---|---|---|---|
| PRD | Governs Epic execution. Living document. The *product requirements*. | Yes — Change Log | [prd-template.md](references/prd-template.md) |
| SDD (Software Design Document) | The *technical design* that implements a PRD, where software design is non-trivial. Living document. | Yes — Change Log | [sdd-template.md](references/sdd-template.md) |
| Design Doc (Design Research) | Design *rationale + evidence* — maps decisions to PRD personas + cited research with confidence levels. | Yes — Change Log | [design-doc-template.md](references/design-doc-template.md) |
| Work Artifact / Iteration Record | Documents work products and their versions as they evolve. | Yes — iteration history | [work-artifact-template.md](references/work-artifact-template.md) |
| General Reference | Stable reference material for ongoing systems. | No — informational | — |
| Release Notes | Records what changed when a skill, pipeline, or system was updated. | Yes — per release | [release-notes-template.md](references/release-notes-template.md) |
| Operational Procedure | Governs how work is conducted. Includes SDLC, session protocols, error handling. | No — governing layer | [operational-procedure-template.md](references/operational-procedure-template.md) |

**Naming + location convention:** title every doc `<Product> — <DocType>` (e.g. `Graph Life (GL) — Career KG — SDD`), and keep all of a product's design docs in the **SD (Software Development)** space. Operational/PII working data stays in the operational space. (Inconsistent titles make an SDD undiscoverable by title; split spaces make hand-offs harder.)

**PRD vs SDD vs Design Doc** — the three are distinct and complementary:
- **PRD** = *what* and *why* (requirements, personas, success metrics). Governs the Epic.
- **SDD** = *how, technically* (architecture, data model, key decisions, validation). Implements the PRD; one per buildable product where the design is non-trivial.
- **Design Doc** = *why this design* (rationale + cited evidence, mapped to PRD personas). Often UX/research-led. Not every product needs one; reach for it when design choices need an evidence trail.

## PRDs — Product Requirements Documents

PRDs are created when an IDEA requires software development. They are the governing document for the Epic that executes the IDEA.

**Trigger:** An IDEA in the IDEA project that requires software to be built → creates a PRD in Confluence → creates an Epic in EXEC that links to that PRD.

**The chain:**
```
IDEA (IDEA project)
  └── PRD (Confluence)        ← governs the Epic; links to it
        └── Epic (EXEC)       ← links back to PRD and to IDEA
              ├── Story        ← links back to PRD (Confluence page)
              ├── Task
              └── Bug
```

Every link in this chain is bidirectional:
- The PRD references the Epic key and embeds a Jira story chart (standard Confluence feature — shows all Stories under the Epic, live status)
- Every Story and Task in the Epic links back to the PRD Confluence page
- The Epic links to both the IDEA ticket and the PRD

## PRD Structure

```
# [Product Name] — PRD

## Overview
[What this product or feature is, in 2–4 sentences. Written for a reader unfamiliar with the IDEA.]

## Problem / Opportunity
[The IDEA this PRD executes on. Link to the IDEA ticket. Why this matters.]

## Jira References
- Epic: [EXEC-XX link]
- IDEA: [IDEA-XX link]

## Jira Stories
[Embed Confluence Jira chart macro here — filters to Epic key, shows Story status live]

## Requirements
[What the system must do. Functional and non-functional. Written as requirements, not as tasks.]

## Out of Scope
[Explicit list of what this PRD does not cover. Prevents scope creep.]

## Decisions
| Date | Decision | Alternatives considered | Rationale |
|---|---|---|---|
| YYYY-MM-DD | [what was decided] | [what else was considered] | [why this choice] |

## Acceptance Criteria (PRD-level)
[High-level criteria that, when all Stories pass, mean the Epic is complete. These are the rollup of Story-level AC, not a replacement.]

## Change Log
| Date | Change | Reason |
|---|---|---|
| YYYY-MM-DD | [what changed] | [why] |
```

**Decisions vs. Change Log:** The Decisions table records significant choices made during development — architecture, scope trade-offs, approach selection, evaluated-and-rejected alternatives. The Change Log records when the PRD itself was updated and why. A decision that causes a PRD update generates an entry in both: Decisions captures the reasoning, Change Log captures the document change.

## PRDs as Living Documents

PRDs update as the Epic evolves. They are not frozen at creation.

**When to update a PRD:**
- A Story's scope changes materially
- A requirement is added, removed, or revised
- The Epic's acceptance criteria shift based on new information
- A Bug reveals a requirement that was underspecified

**Every update requires a Change Log entry** — date, what changed, why. The Change Log is not optional and is not a narrative summary. It is a structured record for automated retrospective processing alongside ticket closing comments.

The Change Log feeds the sprint retrospective alongside ticket Actuals blocks. Together they give a complete picture: what was estimated, what actually happened at the ticket level, and how the governing document evolved in response.

**PRDs are also reference documents for retrospectives.** The retrospective script reads:
1. Closing comments (Actuals blocks) from tickets closed during the sprint
2. Change Log entries from PRDs updated during the sprint

This allows retrospectives to surface not just estimation accuracy but requirement drift — cases where the PRD changed because the original requirements were incomplete or wrong.

## SDDs — Software Design Documents

An **SDD** is the technical design that implements a PRD. It is created when an Epic involves non-trivial software design — architecture, a data model, integration mechanics, design trade-offs worth recording. It is a **living document** with a Change Log, canonical in Confluence with a repo mirror (`docs/<name>-sdd.md`).

**Trigger:** an Epic whose build is more than a thin feature → write an SDD that the Epic's Stories implement against. (A small Story may not need its own SDD; a product/subsystem does.)

**The chain — the SDD slots between PRD and Epic:**
```
IDEA (IDEA project)
  └── PRD (Confluence)            ← product requirements; governs the Epic
        └── SDD (Confluence)      ← technical design that implements the PRD  [where design is non-trivial]
              └── Epic (EXEC)     ← links back to the PRD and the SDD
                    ├── Story      ← implements the SDD; links back to PRD + SDD
                    ├── Task
                    └── Bug
```

**Bidirectional linking:** the SDD's header links to its **governing PRD** and its **Epic/Story**; the Epic and its Stories link back to the SDD. The SDD also names the **code as authoritative** for anything the code owns (schema, routing) — e.g. *"authoritative schema = `app/models.py` docstring"* — so the doc never silently drifts from the implementation.

**Structure:** start from [`references/sdd-template.md`](references/sdd-template.md). The spine (derived from the real JDG and Life Planner SDDs): header (related docs, status, code path, governing Story/Epic, living-doc banner + authoritative-source pointers) → Overview → Architecture → Data Model → Interfaces/API → Services → **Design philosophy / toolkit-reuse** (using vs adding vs changing the landed patterns) → **Key Design Decisions** (`Decision | Rationale | Rejected`) → Integration deep-dives → Tech Stack (by phase) → Phase Breakdown → **Validation (honest)** → Cross-product relevance → Usage & safety → Future work → **Change Log**.

## Design Docs (Design Research)

A **Design Doc** captures design *rationale and evidence* — distinct from an SDD's technical design. It maps each significant design decision to a **PRD persona** and backs it with **cited research** (e.g. eye-tracking, user studies) at a stated **confidence level**. It is the right home for UX/interaction decisions and any design choice that needs an evidence trail rather than just an assertion.

**Trigger:** a design (often UI/UX or research-led) whose choices should be justified against personas + evidence, not just decided. Not every product needs one.

**Structure:** start from [`references/design-doc-template.md`](references/design-doc-template.md): Purpose → Persona(s) addressed (from the PRD) → Decisions mapped to evidence (each decision → the persona it serves → the cited research + confidence) → Open questions → Relationship to the PRD/SDD. Living document with a Change Log.

## Work Artifacts and Iteration Records

Some work produces artifacts that go through multiple iterations before reaching a final state — and the iterations themselves are meaningful. The taxonomy derivation is the concrete example: the taxonomy went through several versions before approval, and the archive outputs feed downstream into the Get A Job system. The session record page in Confluence documents both the methodology and the final state.

**What belongs here:**
- Any artifact that went through meaningful iteration before reaching its current form
- Outputs from pipelines or analysis sessions that serve as inputs to other systems
- Session records that document how a significant piece of work was conducted and what it produced

**Structure:**
```
# [Artifact Name]

## Current Version
[The current state of the artifact, or a link to it.]

## Purpose
[What this artifact does and what system or workflow it feeds into.]

## Iteration History
| Version | Date | What changed | Why |
|---|---|---|---|
| v1 | YYYY-MM-DD | Initial | — |
| v2 | YYYY-MM-DD | [what changed] | [why] |

## Source / Provenance
[Where this artifact came from — which pipeline, session, or process produced it.]

## Downstream consumers
[What uses this artifact. Links to tickets or other Confluence pages that depend on it.]
```

The Iteration History feeds sprint retrospectives when an artifact is updated during a sprint.

## Release Notes

Release Notes document changes to skills, pipelines, agents, or any operational system when a version is promoted.

**Trigger:** Any time a skill is modified, a pipeline phase is updated, an agent is amended, or a new capability is deployed.

**Structure:**
```
# Release Notes — [System Name]

## [Version or Date] — [One-line summary]

### What changed
- [Change 1]
- [Change 2]

### Why
[The reason — error correction, new requirement, capability extension. Reference the originating ticket or error (e.g., EXEC-18, E26).]

### Impact
[What this affects downstream — skills that load this system, tickets that depend on it, retrospective scripts that parse its output.]

### Rollback
[How to revert if needed. If git-tracked, the commit reference. If not reversible, state that explicitly.]
```

Release Notes feed sprint retrospectives as a record of what changed in the operational layer during the sprint.

## Operational Procedures

Operational procedures govern how work is conducted. They are the governing layer — not project-specific, but system-wide. They document the SDLC and ways of working between Fred and Claude.

**What belongs here:**
- The SDLC workflow itself (IDEA → PRD → Epic → Story → Task → close)
- Sprint cadence and retrospective process
- Session start protocol (error log first, pipeline tracker second)
- Environment routing rules (Code vs. Cowork)
- Error logging protocol (proactive, not reactive)
- Skill and agent modification rules (fenced files, out-of-band amendment process)
- Single-writer principle for canonical files

**Structure:**
```
# [Procedure Name]

## Purpose
[What this procedure governs and why it exists.]

## Applies to
[Which environments, projects, or roles this covers.]

## Procedure
[Step-by-step. Numbered. Each step is a discrete action.]

## Rationale
[Why this procedure exists — often references an error (e.g., E28) or an incident that made the need visible.]

## Change history
| Date | Change | Reason |
|---|---|---|
```

Operational procedures do not feed sprint retrospectives directly — they are the governing layer that retrospectives check against. A retrospective that finds systematic deviation from an operational procedure is a signal that the procedure needs updating or the deviation needs correcting.
