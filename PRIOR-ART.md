# Prior art, alternatives & related work

Agentic Software Operations is **one honest option in an active space**, not the only one. This page
points to the broader landscape so you can find what fits your need — and use it if it fits better.

The bundle's specific stance: a **deterministic** Atlassian substrate (no-LLM, idempotent ticket
craft, decomposition, audit, status/metrics) under an **operating model** that reserves the LLM for
judgment (retrospective synthesis, planning suggestions). Most of the landscape below is either
LLM-driven throughout or a point GUI/SaaS product.

## Component-level prior art
The Ops4Atlassian's [`PRIOR-ART.md`](../ops4atlassian/PRIOR-ART.md) maps the Atlassian
agent-tooling landscape in detail — **start there**. It covers, among others:

- **Anthropic's official [Atlassian plugin](https://claude.com/plugins/atlassian)** and hosted
  **[Claude Agent for Jira](https://www.atlassian.com/blog/company-news/claude-agent-for-jira)** —
  first-party, zero-setup natural-language Jira/Confluence. If that's what you want, start there.
- Community skill packs (e.g. [langpingxue/atlassian-skills](https://github.com/langpingxue/atlassian-skills)).
- Paid GUI bulk-edit apps (e.g. codefortynine) and the terminal `atlassian-cli`.
- Native Jira features (split issue, automation-rule dedup) and the documented gaps they leave
  (no idempotent-create endpoint).

## Operating-model / platform landscape
- **SAFe® and other scaled-agile frameworks** — the methodology lineage this operating model draws
  on. Agentic Software Operations is a generic, agent-operated take on those public practices, not a
  replacement for the frameworks themselves.
- **Atlassian Rovo / native Jira reporting & dashboards** — for in-product dashboards and reporting.
  The bundle's Delivery Dashboard is a deliberately lightweight, portable, agent-buildable alternative,
  not a competitor to the in-product analytics suite.
- **Research** — e.g. *"Closed-Loop Autonomous Software Development via Jira-Integrated Backlog
  Orchestration: Deterministic Control and Safety-Constrained Automation"* (arXiv) — adjacent work on
  deterministic, Jira-integrated automation; worth reading if the deterministic-orchestration idea
  interests you.

## How to choose
- Want **natural-language Jira/Confluence actions, zero setup, first-party**? → Anthropic's Atlassian
  plugin / Claude Agent for Jira.
- Want **in-product dashboards and analytics**? → native Jira / Rovo.
- Want a **deterministic, scriptable, version-controlled operating model + substrate** you can run and
  extend yourself? → this bundle.

*This list reflects what we found during evaluation (2026); it isn't exhaustive, and "not listed"
doesn't mean "doesn't exist." Additions welcome.*
