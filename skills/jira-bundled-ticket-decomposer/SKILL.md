---
name: jira-bundled-ticket-decomposer
description: Decompose a bundled Jira ticket — one ticket whose description is a table or list of N items — into one child ticket per item, preserving the original. Triggers on "decompose a bundled ticket", "split this ticket into one per item", "bundled task", or any ticket whose body is really a checklist of separate work units that each deserve their own ticket. Dry-run first, then explicit apply.
lifecycle:
  phase: project-start
  cadence: on-demand
  trigger: "split a bundled Jira ticket (table/list of items) into one child ticket per item — dry-run then apply"
---

# JIRA Bundled-Ticket Decomposer

> **Transport:** the parser (`decompose.py`) is transport-free. The **apply** step's Jira operations (search-by-key, create) resolve through the [Atlassian transport contract](../../../atlassian-transport/transport-contract.md) — **Rovo MCP** default, **REST** adapter (API token) when no MCP. Name the *operation*, not a hardcoded tool.

A **bundled ticket** is one Jira issue whose description is really a table or a
bullet/numbered list of N distinct work items — each of which should be its own
ticket so it can be assigned, scored, estimated, and closed independently. This
skill splits it into **one child ticket per item**, keeps the original as the
parent, and does it under a **dry-run-first / explicit-apply** contract.

The live Jira writes go through the Atlassian MCP (session-mediated). This skill
is a precise **process** plus a deterministic stdlib **parser**
(`decompose.py`) that turns the bundled description into a structured item list.
The parser never calls Jira; it produces the *plan* the apply step executes.

For the underlying ticket lifecycle (open → progress → PR → close) load
`jira-lifecycle`. For project/ticket structure load `jira-workflow`. This skill
sits at `project-start`: you reach for it when framing the bundled work, before
execution.

---

## Shared design discipline (do not skip any of these)

1. **Dry-run before apply, always.** Never write to Jira on the first pass. Run
   the parser, show the human the proposed children, get an explicit go-ahead,
   then apply. The dry-run plan and the apply input are the **same item list** —
   the human reviews exactly what apply will create.
2. **Never hardcode transition ids.** Always resolve them live via
   `getTransitionsForJiraIssue` (per `jira-lifecycle`). Transition ids vary by
   project/workflow and drift.
3. **Validate by counts.** After apply, `created == planned`. If they differ,
   stop and report the mismatch — do not silently proceed.
4. **Idempotent — resolve by a stable per-item key.** Each item has a stable
   key (slug + hash of the full normalized row). Apply **writes that key onto
   the child** and **searches for it before creating**, so re-apply never
   duplicates. The key is the load-bearing mechanism, not decoration.
5. **Original ticket preserved.** The bundled ticket becomes the parent. It is
   **never deleted** and its description is **never destroyed** — at most
   annotated with a comment noting it was decomposed.
6. **Assignee shape:** `fields: { "assignee": { "accountId": "<id>" } }`. New
   EXEC children are assigned to the executor (Pyongwa), not Fred, unless the
   item is decision/requirement work (which stays with Fred per the
   assignment-ownership rule).
7. **Large N → reuse the Bulk-operations method** from `jira-workflow`
   (self-paginate batches of ~20, hand each batch to a subagent context-firewall
   that returns counts + failures, back off on HTTP 429, `jq`-on-saved-file for
   oversized searches).

---

## The parser (`decompose.py`)

Stdlib only (`re`, `hashlib`, `argparse`). No deps, no Jira calls.

```bash
# Dry-run plan (human-readable) from a saved description:
python3 decompose.py bundled.txt --parent EXEC-500

# Or pipe it in:
pbpaste | python3 decompose.py --parent EXEC-500

# Machine-readable item list for the apply step:
python3 decompose.py bundled.txt --json
```

Each item carries:

| field | meaning |
| --- | --- |
| `title` | first table column / the list line text (markers stripped) |
| `source` | the raw row/line, preserved verbatim for traceability |
| `key` | stable key = `slug(title)` + 8-char sha1 digest of the normalized row |
| `columns` | extra table columns (owner, notes, …), if present |

**Parser behavior (the design decisions):**

- **Auto-detect.** If the body has ≥2 pipe rows and a separator row
  (`|---|---|`), parse as a **table**; the separator and header rows are dropped,
  data rows become items. Leading/trailing pipes are handled. Otherwise parse as
  a **list** (lines starting with `-`, `*`, `+`, `1.`, or `1)`).
- **Title heuristic:** table → first column; list → the line minus its marker.
- **Empty / malformed input → empty item list** (never raises). Prose with no
  table and no list markers yields zero items — surface that to the human rather
  than inventing children.

Run the tests before trusting it: `python3 -m unittest test_decompose -v`
(22 cases: table, list, idempotency, empty/malformed, plan formatter).

---

## Process

### 1. Read the bundled ticket
`getJiraIssue(cloudId, parentKey)` → take the description. Confirm with the
human that this ticket really is a bundle (a table/list of separable items) and
not a single coherent unit.

### 2. Dry-run
Save the description to a file and run the parser to produce the plan:
```bash
python3 decompose.py bundled.txt --parent <PARENT>
```
Show the plan to the human: N proposed children, each with title, source row,
and stable key. **Stop here.** Do not write to Jira until the human explicitly
approves. If the parser returned zero items, report that — the body is not a
recognizable bundle.

### 3. Apply (only on explicit approval)
For each item, idempotently:

1. **Check for an existing child by key.** Search the parent's children for the
   item's key (it is written into each child — see below). If found, **skip**
   (already created). This is what makes re-apply safe.
   ```
   searchJiraIssuesUsingJql(cloudId,
     'parent = <PARENT> AND description ~ "decomp-key:<key>"')
   ```
2. **Create the child** (`createJiraIssue`) with:
   - summary = `item.title`
   - description = the item's `source` row + a marker line the search above
     keys on, e.g. a final line `decomp-key:<key>` (also add a `decomposed`
     label). The marker is how step 1 finds it next time.
   - `fields: { "assignee": { "accountId": "<id>" } }` — executor for execution
     work, Fred for decision/requirement items.
3. **Link the child to the parent:** `createIssueLink` with type `"is child of"`
   (inward: child, outward: parent) — never express the relationship as prose.
4. **Transition** the child into its starting status only via
   `getTransitionsForJiraIssue` → `transitionJiraIssue` (no hardcoded ids).

For large N, drive steps 1–4 through the `jira-workflow` **Bulk operations**
method (batches of ~20, subagent firewall, 429 back-off).

### 4. Validate by counts
`created == planned`. Re-query the parent's children (the index lags — verify
against fresh ground truth) and confirm the live child count matches the plan.
Report any mismatch instead of proceeding.

### 5. Preserve & annotate the original
Leave the parent's description intact. Add one comment:
`addCommentToJiraIssue(cloudId, parentKey, "Decomposed into N children: [keys]. Original preserved as parent.")`.
The parent is **never deleted**.

---

## Anti-patterns

- ❌ Writing to Jira on the first pass (skipping the dry-run).
- ❌ Hardcoding a transition id instead of resolving it live.
- ❌ Deleting or overwriting the original bundled ticket.
- ❌ "Idempotent" in name only — creating children without writing/searching the
  per-item key, so a re-run duplicates everything.
- ❌ Declaring success without checking `created == planned` against a fresh
  re-query.
- ❌ Expressing the child↔parent relationship as prose instead of an issue link.
- ❌ Treating a 100-item bundle as one big sweep instead of the `jira-workflow`
  batched/subagent method.
