# Execution-aware rollup & reconciliation

## Execution-aware rollup
- Completion **rolls up from child work**, not from a parent's status field. A
  parent marked Done with open children is *not* Done.
- Never silently mix completion models (e.g. child-count completion vs.
  committed-scope completion) — keep them separate and label which is shown.
- **Page every query** and dedupe by key before rolling up; membership is
  **label-based** (an item appears in every matching rollup).

## Reconciliation record (feeds the C6 retrospective — S7 contract)
Before publishing, reconcile the report against the source and emit a
**reconciliation record** so the v0.2 analyzer has its delivery/freshness input
with zero rework. It must satisfy `tools/retro/contract.py` →
`ReconciliationRecord.from_dict`:

```toml
[reconciliation]
as_of    = "2026-06-19"   # when the source was read
scanned  = 100            # items considered
resolved = 98             # items whose status reconciled cleanly
dead     = 2              # items that did not reconcile (flagged, not hidden)
```

- A non-zero `dead` count is **disclosed in the report**, never hidden — a clean
  report must still say how much didn't reconcile.
