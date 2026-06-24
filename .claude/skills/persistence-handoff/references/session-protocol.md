# Session Protocol (persistence & handoff)

## Session Start (≤ 5 calls)
1. Find the active **anchor** record (tracker query: `session-anchor`, not Done,
   most recently updated).
2. Read the anchor — scope, strategy, link to the current-state page.
3. Read the **current-state page** — Current State, Decisions This Sprint, Active
   Blockers, and the **Next Action**.
4. (New phase / architectural decision only) read the governing PRD/SDD.
5. **Do the Next Action.** Do not replan from scratch — trust the handoff.

## Session End
1. Write a closing/status record on the anchor (what happened; estimate-vs-actual
   for the retrospective contract).
2. Update the current-state page: Current State, Decisions This Sprint, Active
   Blockers, and a single concrete **Next Action**.
3. Transition the ticket if the work is done.

## Decisions vs status (the rule)
**Decisions go to the knowledge base; status goes to the tracker.**
- Knowledge base: why an architectural choice was made; what was tried and
  rejected; current operational state; reusable patterns.
- Tracker: completion notes, links, blockers, retrospective/estimate data.

## Backfill
When reconstructing past work into the record:
- **Search the tracker first** — never create duplicate records.
- Separate **delivery progress** from **admin / cleanup**.
- Label backfilled work clearly; mark **verified vs. inferred**.
- One record per unit of work; never merge periods.
