---
name: jira-workflow
description: IDEA and EXEC projects, discovery→execution pipeline, when to create each ticket type
lifecycle:
  phase: project-start
  cadence: on-demand
  trigger: "structuring an initiative: when to create IDEA / Epic / Story / Task / Subtask / Bug"
---

# JIRA Workflow: Discovery to Execution

## Overview

Fred's JIRA uses a **two-project system** that separates ideation (discovery, validation) from execution (implementation, delivery).

```
IDEA Project (Discovery)           EXEC Project (Execution)
├─ Idea                            ├─ Epic (5+ stories)
├─ Opportunity                     ├─ Story (3–10 days each)
├─ Solution                        ├─ Task (1–3 days)
└─ Feature                         ├─ Subtask (part of story)
                                   └─ Bug (problems + solutions)
```

**Key Principle:** Ideas stay in IDEA until approved for execution. This prevents scope creep and ensures only validated work enters EXEC.

## Ticket Structure Standard

All tickets follow the persona-driven standard defined in `jira-persona-driven-tickets`.
That skill is the project convention and overrides generic templates from other sources
(e.g., the Atlassian `spec-to-backlog` plugin uses a Context/Requirements format with
no persona mandate — that format does not meet this project's standard).

For ticket lifecycle (open → progress → PR → close), load `jira-lifecycle`.

---

## Projects

### IDEA Project (Product Discovery)
- **Key:** IDEA
- **Purpose:** Early-stage concepts, exploration, validation of fit
- **Issue Types:** Idea, Opportunity, Solution, Feature
- **Workflow:** Stays in IDEA until approved; then links to EXEC Epic

**Examples:**
- IDEA-19: Knowledge Graph: Queryable Alternative to Flat Extraction
- IDEA-20: Literary Manager KG Initiative

### EXEC Project (Execution)
- **Key:** EXEC
- **Purpose:** Implementation, delivery, operations
- **Issue Types:** Epic, Story, Task, Bug, Subtask
- **Workflow:** Each Epic links back to parent IDEA for context

**Examples:**
- EXEC-68: Literary Manager KG Foundation [Epic]
- EXEC-69: Phase 1.1 File Indexing [Story]

---

## Workflow: Idea → Epic → Stories

**Pattern:**

```
IDEA Project (Discovery)
  └─ IDEA-#: [Concept] Hypothesis or research question

  ↓ (Approved for execution)

EXEC Project (Execution)
  └─ EXEC-#: [Epic] Initiative decomposition
       ├─ EXEC-#: [Story] Component 1
       ├─ EXEC-#: [Story] Component 2
       └─ EXEC-#: [Story] Component N
```

**Example: Media Engine KG**

```
IDEA-19: Knowledge Graph: Queryable Alternative to Flat Extraction
  ↓ (Approved for execution)
EXEC-56: Career KG Infrastructure Build (Media Engine POC) [Epic]
  ├─ EXEC-57: File Indexing & Filtering Pipeline [Story]
  ├─ EXEC-58: Text Extraction (PDFs, DOCX, Images) [Story]
  ├─ EXEC-59: Entity Extraction (Pydantic + Claude) [Story]
  ├─ EXEC-60: Entity Resolution (Clustering) [Story]
  ├─ EXEC-61: Graph Building (NetworkX) [Story]
  ├─ EXEC-62: Graph Queries (Multi-hop Traversal) [Story]
  ├─ EXEC-63: Report Synthesis Generation [Story]
  ├─ EXEC-64: SQLite Persistence & Schema [Story]
  ├─ EXEC-65: Testing & Integration [Story]
  ├─ EXEC-66: Media Engine Report & Deliverables [Story]
  └─ EXEC-67: Documentation & Code Cleanup [Story]
```

---

## Key Principles

1. **Separation of Concerns:** Discovery (IDEA) is separate from execution (EXEC), preventing premature scope commitment
2. **Clear Lineage:** Every EXEC Epic links back to its originating IDEA for context
3. **Atomic Stories:** Each EXEC Story represents one coherent piece of work (feature, component, or deliverable)
4. **Structured Decomposition:** Epics break into Stories; Stories can have Subtasks for fine-grained tracking
5. **Linkage:** Link related issues across IDEA and EXEC to maintain traceability

---

## When to Create Each Type

### When to Create in IDEA

- You have a hypothesis or question
- You're exploring a new direction
- You want to validate fit before committing resources
- You're brainstorming with stakeholders
- You need to document a need or opportunity before solving it

### When to Create in EXEC

- Idea is approved and ready for execution
- Work can be decomposed into trackable stories
- Team is ready to commit to milestones
- You need to coordinate with implementation

### When to Create an Epic

- Work spans 5+ stories
- Work has a clear deliverable or outcome
- Work can run in parallel (multiple stories)
- Work has phases or release milestones

### When to Create a Story

- Work is scoped to a few days/weeks
- Work has clear acceptance criteria
- Work can be tested/reviewed independently
- Work is assignable to one person

### When to Create a Task

- Work is small (1–3 days)
- Work is not user-facing
- Work supports a story or epic
- Clear, discrete acceptance criteria

### When to Create a Subtask

- Story is complex and benefits from tracking smaller units
- Each subtask is independently testable
- Clear dependencies between subtasks

### When to Create a Bug

- Unexpected behavior discovered
- Reproduction steps are clear
- Impact and severity can be assessed
- Solution includes root cause + validation

---

## Persistence & Integration

### Git Integration

- Reference ticket keys in commit messages (e.g., `EXEC-56: build KG`)
- Link PRs to tickets via GitHub/Jira integration
- Close tickets via PR merge comments (`Closes EXEC-56`)
- Update tickets with PR URLs for cross-repository traceability

### MCP Integration

- Use Atlassian MCP tools to create, update, link issues
- Comment on tickets with implementation notes and PR references
- Add worklogs to track time spent
- Link related IDEA ↔ EXEC tickets for traceability

### Bulk operations — large edits & queries

> **Transport:** these operations resolve through the [Atlassian transport contract](../../../atlassian-transport/transport-contract.md). The **Rovo MCP** is the default adapter; a **REST** adapter (`atlassian-transport/atlassian_rest.py`, API token) runs the same operations with no MCP. The method below is the **MCP-adapter** technique (it works around the MCP's per-call payload). **Over REST you control `fields`, so payloads are small and most of this mitigation is unnecessary** — request minimal fields and page with `startAt`/`maxResults`.

The Atlassian MCP has **no bulk-edit endpoint**, and both `editJiraIssue` and `searchJiraIssuesUsingJql` return the **full issue object (~5KB+) per call**. So a naive sweep of 100–200+ tickets either blows the session context or times out. Reach for this method **before** declaring a >~20-issue task "human-only" or "needs an API token" — it doesn't.

**1. Self-paginate into batches of ~20.** Split the work list into chunks of ~20 (N = the largest you can run before the MCP times out; prior sessions landed on 20). Process each batch one issue at a time, then move to the next batch.

**2. Or hand each batch to a subagent (context firewall).** A subagent absorbs the fat per-call responses in *its own* context and returns a compact summary (counts + failures) — the ~1MB never touches your thread. Use **one sequential worker per batch**: parallel workers share the account's ~200-call rate ceiling; have the worker back off and retry on HTTP 429 rather than abort.

**3. Read oversized searches with `jq`-on-saved-file.** When a `searchJiraIssuesUsingJql` result is too large, the MCP saves it to a file. `jq -r '.issues.nodes[].key'` it to pull just the keys cheaply, instead of loading the fat objects. Page via `nextPageToken` / `pageInfo.endCursor`.

**4. Exclude-by-nature, not by one named key.** A reassign/transition sweep must exclude **every** genuinely-owner ticket, identified by *nature* — decisions/requirements stay with Fred; human-only UI tickets (e.g. Release-Manager Jira-version creation, repo-admin toggles) stay with their owner. Build the exclusion set up front from [the assignment-ownership rule], don't hardcode a single exception.

**5. Verify against fresh ground truth — the index lags.** JQL search is eventually-consistent: a just-completed bulk operation can lag the index by seconds-to-minutes. Re-query and confirm the live count is real before acting on it, and **when the user says "I did it myself," verify and defer** — don't race a stale read to "help."

**Field shapes that work:** reassign → `fields: { "assignee": { "accountId": "<id>" } }`. New EXEC tickets are assigned to the executor (Pyongwa), not Fred.

> Origin: this method existed in practice but wasn't documented, so it failed to trigger by default during the 2026-06-24 EXEC Fred→Pyongwa reassignment (a stale-index sweep briefly moved two Release-Manager tickets). It is skill #7 (`jira-mcp-bulk-operations`) in the IDEA-23 / SD-15728701 Jira-skills decomposition.

---

## Release Milestones

Use EXEC milestones to organize releases:
- **v1.0 (MVP):** Core functionality, basic features
- **v1.x (Iterations):** Refinements, bug fixes, performance
- **v2.0 (Major):** New features, architectural changes

Map EXEC stories to milestones to track release readiness.

---

## Examples from Pyongwa Repo

**Get-A-Job Pipeline (Current):**
- IDEA-17/IDEA-18: Job search automation concepts
- EXEC-42: Hybrid Job Search Automation System [Epic]
- EXEC-43:46: Phase 1-4 stories

**Get-A-Job Infrastructure:**
- EXEC-41: Multi-peer observation network [Epic]
- EXEC-50:55: Infrastructure fixes and automation

**Media Engine KG POC (Completed):**
- IDEA-19: KG concept discovery
- EXEC-56: KG infrastructure build [Epic]
- EXEC-57:67: Component stories (all completed)

**Literary Manager KG (Current):**
- IDEA-20: Literary Manager KG Initiative
- EXEC-68: Literary Manager KG Foundation [Epic]
- EXEC-69:78: 5 phases (file indexing through visualization)
