# Changelog — Agentic Software Operations

All notable changes to the bundle distribution. The roadmap (forward) lives in
[`ROADMAP.md`](ROADMAP.md); this file records what actually shipped.

Format loosely follows [Keep a Changelog](https://keepachangelog.com/); dates are intentionally
omitted in favor of versioned milestones.

## [0.1.0] — initial bundle

### Added
- The bundle distribution: a composition of the Atlassian Companion (deterministic Jira/Confluence
  substrate) and Product Ops 2.0 (operating model), assembled by `build.sh` from the canonical
  sources.
- Composition curation: the Companion's production skills supersede Product Ops 2.0's two substrate
  reference skills (`doc-minimums`, `tracker-operation`), which are curated out of the bundle; Product
  Ops 2.0's operating-model skills (`reporting-cadence`, `persistence-handoff`) and spec are included.
- Split license (CC-BY-4.0 docs / Apache-2.0 code), reconciled across both component products; the project name is reserved (Apache-2.0 §6 + `NOTICE`).
- `README.md` (platform model + the four platform features), `ROADMAP.md`, `PRIOR-ART.md`,
  plugin manifest with optional `worksWith` declarations.

### Notes
- Publish-**ready** in the monorepo; a separate public repository is a planned roadmap item.
- The four platform features (AutoSprint, AutoRetro, Delivery Dashboard, AutoPI Planning) are on the
  roadmap as `exploratory` — not yet shipped.
