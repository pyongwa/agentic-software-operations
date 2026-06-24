---
name: jira-hierarchy-audit
description: Audit a Jira Initiative/Epic hierarchy for outstanding, stale, and duplicate children and drift. Read-only. Use on "audit this epic/initiative", "stale tickets", "duplicate tickets", "hierarchy hygiene", or before a cleanup pass.
lifecycle:
  phase: on-trigger
  cadence: on-demand
  trigger: "audit a Jira Initiative/Epic hierarchy for outstanding / stale / duplicate / drift (read-only)"
---

# JIRA Hierarchy Audit

> **Transport:** the analysis (`audit.py`) is transport-free. The read (search the hierarchy) resolves through the [Atlassian transport contract](../../../atlassian-transport/transport-contract.md) — **Rovo MCP** default, **REST** adapter (API token) when no MCP. Over REST, request minimal `fields` and page directly; the `jq`-on-saved-file step is an MCP-adapter mitigation. Read-only either way.

Read-only audit of a Jira **Initiative/Epic hierarchy** — surfaces outstanding work, stale items, duplicate candidates, and drift, then proposes a cleanup. **This skill never writes to Jira.** It is the read-side companion to `jira-bundled-ticket-decomposer` (write) and automates the manual audit work (cf. EXEC-81).

## Input → Output

- **Input:** a Jira key (Initiative or Epic) + a depth (children, or children + grandchildren).
- **Output:** an **inventory** (counts by type / status / assignee), **outstanding** (open children), **stale** candidates, **duplicate** candidates, and **cleanup recommendations** — as a report. No mutations.

## Method — compact inventory first, then focused reads

The whole point is staying within context on large hierarchies. Follow the **Bulk operations (MCP)** discipline from `jira-workflow` (the EXEC-425 method):

1. **One JQL search for the whole hierarchy**, e.g. `parent = <KEY>` (or `"Epic Link" = <KEY>` / `parent in (<child epics>)` for two levels). Request minimal fields. When the result is large it auto-saves to a file.
2. **Build the compact inventory with `jq`** — pull only the projection the analysis needs, NOT the fat issue bodies:
   ```
   jq -r '.issues.nodes[] | {key, summary, type: .fields.issuetype.name,
     status: .fields.status.name, statusCategory: .fields.status.statusCategory.name,
     assignee: (.fields.assignee.displayName // "Unassigned"),
     updated: .fields.updated}' <saved-file>
   ```
3. **Focused reads only where needed** — fetch a full issue (description/comments) only for a specific candidate you're investigating, never for every child.

## Analysis — `audit.py` (deterministic, stdlib, no live calls)

Feed the compact list (list of dicts: `key, summary, type, status, statusCategory, assignee, updated`) to `audit.py`:

- **`inventory(issues)`** — counts by type, by workflow status (read from the data — statuses are never hardcoded), and by assignee.
- **`outstanding(issues)`** — open issues (those whose `statusCategory` is not `Done`; `statusCategory` is a Jira *system* field with fixed values To Do / In Progress / Done, so it's safe to compare — that is not a hardcoded-status violation).
- **`stale(issues, cutoff)`** — open issues not updated since `cutoff`. The caller owns "now" (pass a `YYYY-MM-DD` cutoff, e.g. 30/60/90 days back) — the helper makes no real-time call, so results are reproducible. Missing `updated` ⇒ treated as stale.
- **`duplicates(issues, threshold=0.7)`** — near-identical pairs by normalized summary token overlap (Jaccard); each unordered pair reported once.

`audit.py` is pure and Claude-independent — it can run in any session or a cron with the saved JQL projection as input. `test_audit.py` covers inventory grouping, the outstanding filter, stale (fixed cutoff), duplicate detection, and empty input.

## Reporting

Present, in this order: **Inventory** (the counts) → **Outstanding** (with ages) → **Stale candidates** (key + last-updated + age) → **Duplicate candidates** (the pairs + similarity) → **Cleanup recommendations** (what to close / merge / re-home / decompose).

## Discipline (shared across the Atlassian companion)

- **Read-only.** This skill proposes; it never closes, merges, or edits. Hand any resulting write to the appropriate write skill (`jira-lifecycle`, `jira-bundled-ticket-decomposer`) or to the user.
- **Context-safe by construction** — compact inventory first; never pull every full issue.
- **Never hardcode workflow status names** — read them from the data; only the `statusCategory` *system* field is treated as fixed.
- **Honest output** — a "duplicate candidate" is a candidate for human judgment, not an assertion; a "stale" item is stale relative to the cutoff you chose, stated explicitly.

## Run the helper / tests

```
python3 meta/.claude/skills/jira-hierarchy-audit/audit.py        # import as a module from your analysis step
python3 meta/.claude/skills/jira-hierarchy-audit/test_audit.py   # stdlib unittest
```
