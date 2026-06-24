# [Product] — SDD

> **Software Design Document.** Status: [planned / building / built — + validation state]. Code: `[path]`. Governing PRD: [link]. Story/Epic: [EXEC-XX]. Test/QA Plan: [link]. This page is canonical; repo mirror at `docs/[name]-sdd.md`.

> ⚠️ **Living document — see the Change Log at the bottom.** Authoritative sources (the doc defers to code where code owns the truth): schema = `[module].py` docstring; routing = `app/main.py` + `app/routers/`; [other].

## 1. Overview
[What this is, in 2–4 sentences, for a reader unfamiliar with the IDEA/PRD.]

## 2. Architecture
[Layering / component diagram. Transport, boundaries, where the work happens.]
```
[ASCII diagram — layers or data flow]
```

## 3. Data Model
[Entities / tables / key fields. Point to the authoritative source in code.]

## 4. Interfaces / API Routing
[Endpoints or CLI surface — a table where it helps. Omit if not applicable.]

## 5. Services / Business-logic layer
[The modules that do the work, and what each owns.]

## 6. Design philosophy — using the landed toolkit (not changing it)
The question for any new build: *am I **using** what's landed, **adding** to it, or **changing** it?* State which, with a reuse table.

| Landed pattern (where it landed) | How this build uses it |
|---|---|
| Idempotent resolve-or-create by stable key | [how] |
| Backup-first before destructive writes | [how] |
| Single-writer for canonical state | [how] |
| Dry-run / draft-first safety gate | [how] |
| Stdlib-only, local-first; runs without Claude | [how] |

**The addition (if any):** [what is genuinely new and why prior tools didn't cover it — additive, alters no existing pattern].

## 7. Key Design Decisions
| Decision | Rationale | Rejected / Alternatives |
|---|---|---|
| [decision] | [why] | [what else was considered] |

## 8. Integration / environment deep-dives
[Anything non-obvious about the environment, integrations, or dev-parity. Omit if none.]

## 9. Tech Stack
| Layer | Phase 1 | Phase 2 | Phase 3 |
|---|---|---|---|
| Backend / Frontend / Data / Integrations | … | … | … |

## 10. Phase Breakdown
- **Phase 1 — [name] (status):** [scope]
- **Phase 2 — [name] (status):** [scope]

## 11. Validation / Testing & Quality (honest)
| Path | Status |
|---|---|
| [path] | VERIFIED / partial / not yet |

State what the release gate **does** and **does not** cover (migrations, external integrations, real-credential paths often aren't exercised by the gate — say so).

## 12. Cross-product / cornerstone relevance
[How this seeds or relates to other initiatives — the transferable core + the seam to extract. Omit if standalone.]

## 13. Usage & safety
```
[invocation examples]
```
[Destructive-operation warnings; backups; what must be true before an unattended run.]

## 14. Future work
- [optional / deferred items, each with a one-line rationale]

## 15. Change Log
| Date | Change | Reason |
|---|---|---|
| YYYY-MM-DD | Initial | — |
