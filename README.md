# Agentic Software Operations

A **platform for agentic software operations** — the operating model and the deterministic
Atlassian substrate to run a software practice in Jira + Confluence, composed into one install.

It is a **composition, not a fourth codebase.** Two products that also ship independently:

- **[Atlassian Companion](https://github.com/pyongwa/atlassian-companion)** — the *deterministic* Jira + Confluence substrate
  binding (no-LLM, idempotent ticket craft, decomposition, audit, doc types, orchestration).
- **[Product Ops 2.0](https://github.com/pyongwa/product-ops-2)** — the operating-model *intelligence*
  (reporting cadence, persistence/handoff, retrospective, planning logic, and the moments that need
  LLM judgment).

The bundle is where the two **compose into platform features** — value neither delivers alone.

## The platform model

> **Platform feature = Product Ops 2.0 intelligence + Atlassian Companion substrate.**

Product Ops 2.0 owns the judgment and synthesis; the Atlassian Companion owns the deterministic
read/write against Jira and Confluence. That split is also the boundary between the two products.

The headline platform features on the roadmap (see [`ROADMAP.md`](ROADMAP.md)):

| Feature | What it does |
| --- | --- |
| **AutoSprint** | Auto-generate & manage sprints from the backlog by velocity and priority. |
| **AutoRetro** | Slice a sprint, analyze comments, write a retrospective (went-well / needs-improvement / the *one* thing), then measure that outcome next sprint and repeat. |
| **Delivery Dashboard** | A standalone HTML + small `.py` view that organizes Jira data by status into health metrics — shipped both as a download and as instructions an agent can follow to build it. |
| **AutoPI Planning** | Organize the artifacts; from velocity + prioritization, suggest roadmap sequencing and scenarios. |

These are **on the roadmap, not yet shipped** — the bundle today composes the existing operating
model + substrate that they will build on.

## What the bundle ships (the resolved skill set)

The bundle ships the **already-resolved skill set** in `.claude/skills/` — **curated** so there are
no duplicate or competing skills:

- **All** of the Atlassian Companion's production skills + orchestration.
- Product Ops 2.0's **operating-model** skills (`reporting-cadence`, `persistence-handoff`) and spec.
- Product Ops 2.0's two **substrate reference skills** (`doc-minimums`, `tracker-operation`) are
  **curated out** — the Companion's production skills supersede them on the Atlassian substrate.

> This curation is a property of the *pre-composed bundle*. It does **not** contradict the soft,
> no-disabling interop contract that governs the two products as *standalone* installs — see the
> Companion's [`INTEROP.md`](https://github.com/pyongwa/atlassian-companion/blob/main/INTEROP.md).
> Standalone, each product keeps its full skill set; the bundle simply ships the resolved combination.

## Install

The composed skill set ships ready-to-use in `.claude/skills/`. Point your agent at this directory
(Claude Code via the `.claude-plugin/plugin.json` manifest; Codex / Copilot / Gemini via the shared
skills path, with `AGENTS.md` carrying the session-start orientation). The two source products
([Atlassian Companion](https://github.com/pyongwa/atlassian-companion),
[Product Ops 2.0](https://github.com/pyongwa/product-ops-2)) are also installable on their own.

## License

Split-licensed, matching both component products — see [`LICENSE`](LICENSE):
- **Skills & docs**: Creative Commons Attribution 4.0 (**CC-BY-4.0**).
- **Code & plugin**: Apache License 2.0 (**Apache-2.0**) — use, modify, and redistribute freely, commercially or not. The project *name* is reserved (Apache-2.0 §6 + [`NOTICE`](NOTICE)).

"Atlassian", "Jira", and "Confluence" are trademarks of Atlassian Pty Ltd. This is an independent project, not affiliated with or endorsed by Atlassian.

## Prior art & alternatives

This platform is one honest option in an active space. See [`PRIOR-ART.md`](PRIOR-ART.md) and the
Companion's [prior-art map](https://github.com/pyongwa/atlassian-companion/blob/main/PRIOR-ART.md) — including Anthropic's own official
Atlassian plugin and Claude Agent for Jira. Where a tool there fits your need better, use it.

## Provenance

The methods are **Fred Chong Rutherford's own** — 20+ years with Jira/Atlassian and agile frameworks
(Certified Scrum Product Owner, Certified ScrumMaster, SAFe), documented generically so they scale
with a company.
