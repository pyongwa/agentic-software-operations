---
name: jira-story-points
description: Story point estimation, Fibonacci scale, token cost mapping, retrospectives, and weekly reporting
lifecycle:
  phase: project-start
  cadence: on-demand
  trigger: "estimating story points; weekly status reporting and retrospectives"
---

# JIRA Story Points & Cost Estimation

## Story Point Scale (Fibonacci)

Story points measure relative complexity and effort. Use Fibonacci sequence: **1, 2, 3, 5, 8, 13, 21**

- **SP 1:** Trivial (< 2 hours, 200–500 tokens, ~$0.01)
  - Single-line fix, log statement, variable rename
- **SP 2:** Small (2–4 hours, 800–2,000 tokens, ~$0.02)
  - Simple function, unit test, config update
- **SP 3:** Medium (4–8 hours, 3,000–7,000 tokens, ~$0.05)
  - New class/module, API endpoint, integration test
- **SP 5:** Complex (1–2 days, 10,000–20,000 tokens, ~$0.15)
  - Multi-file refactor, feature with tests, documentation
- **SP 8:** Very Complex (2–4 days, 25,000–50,000 tokens, ~$0.35)
  - New subsystem, complex algorithm, major integration
- **SP 13:** Highly Complex (1–2 weeks, 60,000–100,000 tokens, ~$0.65)
  - Architectural change, large feature set, extensive testing
- **SP 21:** **EPIC** (Multiple weeks, > 100,000 tokens, > $1.00)
  - **MUST DECOMPOSE into smaller stories (SP 1–13)**

**Reference:** Full Story Point & Cost Mapping table available in Confluence: [Story Points & Cost Mapping Reference](https://fredchongrutherford.atlassian.net/wiki/spaces/SD/pages/2555906/)

---

## Token Cost Calculation

**Formula:** (Input Tokens × $0.80/1M) + (Output Tokens × $4.00/1M)

**Assumptions:**
- Input tokens: Documentation, context, code review, planning (40%)
- Output tokens: Code generation, test writing, documentation (60%)

**Example (SP 5):**
- 15,000 total tokens estimated
- Input: 6,000 × $0.80/1M = $0.0048
- Output: 9,000 × $4.00/1M = $0.036
- **Total: ~$0.04 (rounds to ~$0.15 with overhead)**

---

## When Assigning Story Points

1. **Compare to past stories:** "This is like EXEC-70 (SP 5) but simpler" → SP 3–5
2. **Ask: Can I deliver + test in one work session?** → SP 1–3
3. **Ask: Does this span multiple independent components?** → SP 8–13
4. **Ask: Is this still ambiguous after scoping?** → SP 21 (Must decompose)

---

## Red Flags for SP 21 (Must Decompose)

- Story involves 5+ distinct features or components
- Unclear which parts are dependent vs. parallel
- Acceptance criteria have "and" separating major functionality
- Duration estimate exceeds 2–3 weeks
- **Action:** Return to IDEA project for validation, then split into child stories

---

## Epic Tickets: Feature Breakdown with Story Points

Every Epic description must include a subsection listing all child stories with story points:

```markdown
## Feature Breakdown

| Story | Complexity | SP | Tokens | Cost | Notes |
|-------|-----------|-----|---------|------|-------|
| Phase 1.1: File Indexing | Medium | 3 | 3,000–7,000 | $0.05 | Scan source directory, catalog files |
| Phase 1.2: Text Extraction | Complex | 5 | 10,000–20,000 | $0.15 | Extract from PDFs, DOCX, images, etc. |
| Phase 1.3: Entity Extraction | Very Complex | 8 | 25,000–50,000 | $0.35 | Claude API + Pydantic schemas |
| Phase 1.4: Entity Resolution | Complex | 5 | 10,000–20,000 | $0.15 | Local clustering, canonicalization |
| **TOTAL** | | **21** | **48,000–97,000** | **~$0.70** | All phases 1–5 |
```

**Acceptance Criteria must reference total SP:**

```markdown
Acceptance Criteria:
✓ All [X] child stories (total [SP] story points) completed and merged
✓ Total effort aligns with estimates (tolerance: ±20%)
✓ ...rest of acceptance criteria...
```

---

## Story Tickets: Story Point Estimate Section

Every Story description must include:

```markdown
**Story Points:** 5
**Estimated Tokens:** 10,000–20,000 tokens
**Estimated Cost:** ~$0.15

**Rationale:** Multi-file refactor with integration test coverage.
Comparable to EXEC-69 (SP 3, simpler) but less complex than EXEC-75 (SP 8).
```

---

## Ticket Closure & Retrospective Comments

### When Closing a Story/Task/Bug

Claude must add a retrospective comment comparing **estimated story points** (effort) with **actual tokens used** (cost). This feedback loop improves future estimates.

**Retrospective Comment Template:**

```markdown
## Retrospective: Story Point vs. Actual Cost

**Estimated:** SP 5 (10,000–20,000 tokens, ~$0.15)
**Actual:** 16,420 tokens (~$0.13)
**Accuracy:** 106% ✓

**Variance Analysis:** 
Within estimate range. Complexity aligned with SP 5.

**Learning:** 
Entity resolution testing took longer than expected due to edge cases 
(unicode, empty strings). Future SP 5 stories involving clustering should 
add +20% buffer.

**Recommendation:** 
Estimate was good; process was efficient. No changes needed.
```

---

## Estimation Accuracy Scoring

**Formula:** Estimation Accuracy = (Actual Tokens / Estimated Token Midpoint) × 100%

- **80–120%:** ✓ Estimate was accurate
- **50–80%:** ⚠ Overestimated (simpler than expected)
- **120–150%:** ⚠ Underestimated (harder than expected)
- **> 150%:** 🔴 Significantly underestimated (scope creep?)

---

## Weekly Retrospective Automation

These comments are formatted for automated parsing every Friday.

**Weekly Retrospective Report includes:**
- Stories closed this week (count, total SP, total tokens)
- Estimation accuracy (mean, std dev, outliers)
- Trends (SP creep, cost per story point)
- Recommendations for next sprint

**Example Weekly Report:**

```markdown
## Weekly Retrospective (Week of May 22–28, 2026)

**Velocity:** 18 story points closed (5 stories)
**Total Cost:** 74,290 tokens (~$0.58)
**Cost per SP:** 4,127 tokens (~$0.032/SP)

**Estimation Accuracy:**
- EXEC-69: SP 3, 3,240 tokens (108%) ✓
- EXEC-70: SP 5, 15,890 tokens (107%) ✓
- EXEC-71: SP 3, 2,540 tokens (101%) ✓
- EXEC-72: SP 8, 23,100 tokens (92%) ✓ (Overestimated)
- EXEC-73: SP 2, 1,892 tokens (105%) ✓

**Mean Accuracy:** 102.6% (excellent)
**Std Dev:** 6.1% (estimates are consistent)
**Outliers:** None > 150%
**Trend:** Cost per SP stable. No scope creep.

**Recommendation:** Maintain current estimation process.
```

---

## Key Principles

1. **Fibonacci Scale:** Enforces realistic complexity assessment
2. **SP 21 = Epic Trigger:** Automatically identifies work needing decomposition
3. **Token Cost Visibility:** Every estimate shows effort and budget
4. **Retrospective Loop:** Closure comments drive estimation improvement
5. **Velocity Tracking:** Weekly reports identify trends and outliers
