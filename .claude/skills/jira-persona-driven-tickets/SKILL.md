---
name: jira-persona-driven-tickets
description: Persona-driven ticket structure, user stories, and human-readable ticket standards
lifecycle:
  phase: project-start
  cadence: on-demand
  trigger: "authoring any IDEA/EXEC ticket — the persona-driven ticket-content standard"
---

# JIRA Persona-Driven Tickets

## Personas vs. Stakeholders

**Personas** are broad user categories used for market research and testing. They appear in user stories across IDEA, Epic, and Story tickets.

Examples: Writer, Literary Agent, Publisher, Software Engineer, Product Manager

**Stakeholders** are named individuals with vested interest in the work. They may or may not be users. They appear in IDEA tickets for context but NOT in user stories.

Examples: Fred Chong Rutherford, The Client, The Finance Team

---

## IDEA Tickets (Discovery & Validation)

**Purpose:** Articulate a hypothesis, need, or opportunity before committing execution resources.

**Required Sections:**

1. **Title:** Clear, specific hypothesis or question
   - Example: "Knowledge Graph: Queryable Alternative to Flat Extraction"
   - Not: "KG POC"

2. **Problem Statement:** What need or gap does this address?
   - Describe current pain point
   - Which persona(s) experience this pain
   - Business impact if unsolved

3. **Personas:** Which user categories will benefit?
   - List broad persona names (e.g., "Writer," "Literary Agent," "Publisher")
   - For each persona: goals, motivations, and key constraints
   - Do NOT name individuals here (that's the stakeholder section)

4. **Stakeholders (optional):** Who has vested interest?
   - Named individuals interested in this work
   - Their role and specific interest in the outcome
   - Reporting requirements (what value needs to be demonstrated to them?)

5. **Business Goals & Value:** Why solve this?
   - Strategic value (cost savings, new capability, risk reduction)
   - Success metrics (what would prove this works?)
   - Estimated impact (qualitative or quantitative)
   - Which persona(s) get primary value?

6. **Solution Hypothesis:** Proposed approach (optional)
   - What pattern or technology might work
   - Why this approach
   - Unknowns to validate

7. **Acceptance Criteria (for IDEA closure):**
   - [ ] Problem statement validated with stakeholders
   - [ ] Personas identified and documented
   - [ ] Business value articulated and agreed
   - [ ] Solution approach tested or prototyped
   - [ ] Decision: Approved for execution (→ EXEC) or defer/abandon

**Example IDEA-20: Literary Manager KG Initiative**
```
Problem: Writers manually search 40,000+ files to track submissions, rejections, 
publishing history. No unified view of what sold, where, and why.

Personas: 
- Writer: Tracks submission history, analyzes success rates by publisher/genre,
  identifies patterns in rejections and acceptances. Constraints: overwhelmed by
  unstructured notes; no systematic way to query across documents.
- Literary Agent: Needs to understand client's publishing record, pitch success
  rates, advise on genre positioning. Constraints: relies on client to provide
  information; no aggregated view of outcomes.

Business Goal: Autonomous content discovery from unstructured documents. Enable
both personas to query: "Which publishers accept this genre?" "What's my success rate?"

Value: 
- Writers: Save 20 hours/month manual tracking; enable data-driven submission strategy.
- Literary Agents: Provide better client advising; win more client trust through analysis.

Stakeholders: Fred Chong Rutherford (validating KG patterns for Literary Manager product suite)

Acceptance: POC validates KG pattern on 200+ sample documents; cost < $10.
```

---

## Epic Tickets (Execution: Multi-Story Initiative)

**Purpose:** Large initiative spanning multiple stories; has clear deliverable and outcome.

**Required Sections:**

1. **Title:** Feature or capability being delivered
   - Example: "Literary Manager KG Foundation"
   - Not: "Build stuff"

2. **User Story (FIRST LINE — from parent IDEA's persona):**
   
   This MUST be the first line of the description:
   ```
   As a [persona from IDEA], I want [capability], so that [value/outcome].
   ```
   - **Persona** must come from the parent IDEA ticket
   - **Capability** is the epic's scope
   - **Value** connects directly to the IDEA's business goal
   - This line establishes who benefits and why
   
   Example:
   ```
   As a writer, I want a queryable knowledge graph of my submissions and outcomes,
   so that I can identify successful publishers and optimize my submission strategy.
   ```

3. **Objective & Business Value:** Follow the user story with:
   - What problem this epic solves
   - Outcomes stakeholders should expect
   - Metrics for success

4. **Link to PRD:** Reference product requirements document
   - Confluence link or wiki URL
   - PRD must include personas that benefit from this epic
   - PRD contains: architecture, tech stack, phases, success metrics
   - **Need to write a PRD?** Use the **confluence-prd-writing** skill for structure, personas, and templates

5. **Child Stories:** List the stories this epic contains
   - EXEC-69: Phase 1.1 File Indexing
   - EXEC-70: Phase 1.2 Text Extraction
   - etc.

6. **Acceptance Criteria (all testable):**
   - [ ] All child stories completed and merged
   - [ ] Code passes lint and type checks
   - [ ] Unit test coverage > 80%
   - [ ] Integration tests pass (end-to-end)
   - [ ] Documentation complete (README, API docs)
   - [ ] Validation against success criteria from PRD
   - [ ] Performance benchmarks met
   - [ ] Security review complete (if applicable)

**Example EXEC-68: Literary Manager KG Foundation**
```
As a writer, I want to extract and query character/manuscript data from my notes,
so that I can track which stories have been submitted where and see my success patterns.

**Objective:** Build a complete knowledge graph infrastructure that catalogs literary
entities (characters, manuscripts, submissions, publishers, outcomes) from unstructured
notes and documents. Enable interactive exploration and reporting for writing/submission
strategy.

**Business Value:** Writers gain a queryable view of their body of work and submission
outcomes, enabling data-driven decisions about genre, publisher targets, and revisions.

PRD: https://wiki.atlassian.net/.../Literary-Manager-KG-PRD
(PRD includes: Writer and Literary Agent personas, success metrics, architecture phases)

Child Stories: EXEC-69 through EXEC-78 (5 phases, total 54 story points)

Acceptance Criteria:
✓ All 5 phases implemented (extraction through visualization)
✓ 500+ entities extracted from 200+ source documents
✓ 95%+ entity resolution accuracy
✓ Interactive KG explorer with zoom and cluster navigation
✓ Character profile reports with proper formatting
✓ All modules documented with setup/usage guides
✓ Total cost < $50 for full extraction + synthesis
```

---

## Story Tickets (Execution: Single Feature or Component)

**Purpose:** User-facing functionality or single coherent piece of work; scoped to 3–10 days.

**Required Sections:**

1. **Title:** Feature/component being delivered
   - Example: "Text Extraction (PDFs, DOCX, XLSX, Images)"
   - Not: "Extract stuff"

2. **User Story (FIRST LINE):**
   
   This MUST be the first line of the description:
   ```
   As a [persona], I need [action], so that I can [get a benefit].
   ```
   - **Persona** is a user category (from parent IDEA), not a person's name
   - Keep it concrete and testable
   - Value statement shows why this story matters to that persona
   - For technical stories, the persona may be a system or component that serves end users
   
   Examples:
   ```
   As a writer, I need to extract text from my manuscript files,
   so that I can build a searchable index of my work.
   ```
   
   ```
   As a KG extraction pipeline, I need to extract text from diverse formats,
   so that I can process all source materials regardless of format.
   ```

3. **Objective & Technical Context (optional):**
   - Implementation approach if non-obvious
   - Links to related stories or epics
   - Tech dependencies

4. **Acceptance Criteria (all testable):**
   - [ ] PDFs extract text correctly (including embedded images)
   - [ ] DOCX files preserve formatting structure
   - [ ] XLSX/CSV cells parse correctly
   - [ ] Images with text trigger OCR (pytesseract)
   - [ ] Error handling: missing/corrupt files logged, pipeline continues
   - [ ] Performance: extract 100 files < 2 minutes
   - [ ] Unit tests cover: 8 file types, 3 error scenarios
   - [ ] Code review approved
   - [ ] Documentation: how to run, how to extend

5. **Subtasks (optional):**
   - Break complex stories into subtasks if helpful
   - Each subtask has clear acceptance criteria

**Example EXEC-70: Phase 1.2 Text Extraction Pipeline**
```
As a KG extraction pipeline, I need to extract text from PDFs, DOCX, XLSX, and images,
so that I can process all Literary Manager source materials without format barriers.

**Technical Context:** Reuse Media Engine KG pattern (EXEC-57); test on Literary Manager
documents. Part of EXEC-68 (Literary Manager KG Foundation), Phase 1.2. Feeds into
EXEC-71 (Entity Extraction).

Story Points: 5 | Estimated Tokens: 10,000–20,000 | Cost: ~$0.15
(Comparable to EXEC-58 Media Engine text extraction)

Acceptance Criteria:
✓ Extract text from PDFs (pypdf)
✓ Extract text from DOCX (python-docx)
✓ Extract cells from XLSX (openpyxl)
✓ OCR images (pytesseract)
✓ Handle corrupt files gracefully
✓ Performance: 100 files < 2 min
✓ Unit tests: 8 format types + 3 error scenarios
✓ Code review + merge
✓ PHASE_1_2_IMPLEMENTATION.md created
```

---

## Task Tickets (Execution: Small, Discrete Work)

**Purpose:** Small, distinct pieces of work; scoped to 1–3 days; not user-facing.

**Required Sections:**

1. **Title:** What needs doing?
   - Example: "Add Levenshtein distance function to entity resolver"
   - Not: "Code cleanup"

2. **Description:** Context and approach
   - Why this task (dependency for what story?)
   - How to approach it
   - Any gotchas or constraints

3. **Acceptance Criteria (testable):**
   - [ ] Function implemented and callable
   - [ ] Handles edge cases (empty strings, unicode, etc.)
   - [ ] Unit tests pass (> 5 test cases)
   - [ ] Code review approved
   - [ ] Merged to main branch

**Example Task:**
```
Title: Implement Levenshtein distance function for entity clustering

Description: EXEC-72 needs a local clustering algorithm to consolidate entity variants.
Implement Levenshtein distance with 2-gram windowing for performance.

Acceptance Criteria:
✓ levenshtein_distance(s1, s2) → float [0, 1]
✓ Handles: empty strings, unicode, special chars
✓ Performance: compute distance for 1000 pairs < 100ms
✓ Unit tests: 8 cases (matching, non-matching, edge cases)
✓ Code review passed
✓ Merged to main
```

---

## Subtask Tickets (Execution: Part of a Story)

**Purpose:** Break complex stories into smaller, trackable units.

**Required Sections:**

1. **Title:** What part of the story?
   - Example: "Implement PDF text extraction using pypdf"
   - Not: "PDF stuff"

2. **Description:** Scope and approach
   - Exactly what's included/excluded
   - Any dependencies on other subtasks

3. **Acceptance Criteria (testable):**
   - [ ] Function/module working and callable
   - [ ] Handles errors gracefully (corrupt PDFs, permissions)
   - [ ] Unit tests pass
   - [ ] Code review approved
   - [ ] Merged

**Example Subtask (child of EXEC-70):**
```
Title: Implement PDF text extraction (pypdf)

Description: Part of EXEC-70 (Text Extraction). Extract text and metadata from PDFs.
Depends on: index_files.py (EXEC-69).

Acceptance Criteria:
✓ extract_pdf_text(filepath) → str
✓ extract_pdf_metadata(filepath) → dict {pages, creation_date, author, etc.}
✓ Handles: corrupt PDFs, password-protected, missing files
✓ Performance: 100 PDFs < 60sec
✓ Unit tests: 6 cases (valid, corrupt, metadata, etc.)
✓ Code review + merge
```

---

## Bug Tickets (Issue Tracking)

**Purpose:** Report and track problems or errors.

**Required Sections:**

1. **Title:** What's broken?
   - Example: "v10 appendices truncated to 500 characters"
   - Not: "Bug in report"

2. **Description:** What should happen vs. what happens
   - Expected behavior
   - Actual behavior
   - Impact (critical, high, medium, low)

3. **Reproduction Steps:**
   - [ ] Step 1: ...
   - [ ] Step 2: ...
   - [ ] Step 3: Observe [actual behavior]
   
   Example:
   ```
   Steps to Reproduce:
   1. Run: python3 rebuild_v10.py
   2. Open outputs/media_engine_report_v10.docx
   3. Navigate to Appendix B
   4. Observe: Only first 500 characters of content appear (should be full 3KB)
   ```

4. **Environment:**
   - Python version, OS, dependencies if relevant

5. **Comments Section (for solutions):**
   - How was problem identified? (logs, user report, testing)
   - Root cause analysis (what was wrong)
   - Solution applied (what fixed it)
   - Validation (how was fix tested)
   
   Example:
   ```
   **Identified:** Integration test failure on v10 rebuild (EXEC-59).
   
   **Root Cause:** rebuild_v10.py extracted text via XML, losing formatting.
   Paragraph text is limited to 200–300 chars in Word XML element serialization.
   
   **Solution:** Switch to element-level copying instead of text extraction.
   Deepcopy source XML elements directly into target document.
   
   **Validation:** v11 rebuild preserves 46 tables, 919 paragraphs, all formatting.
   Compare v10 (truncated) vs v11 (full) in appendices B–E.
   ```

**Example Bug (Closed with Solution):**
```
Title: Report v10 appendices truncated to 500 characters

Description:
- Expected: Appendices B–E contain full content from source documents
- Actual: Only first 500 characters appear; tables and formatting lost
- Impact: High (v10 unusable for delivery)

Reproduction:
1. Run: python3 rebuild_v10.py
2. Open outputs/media_engine_report_v10.docx
3. Check Appendix B (should be 3,688 chars, shows ~500)

Environment: Python 3.9, python-docx 0.8.11, Windows/Mac

---

**Comment: Solution**

Identified: Integration test showed v10 appendices truncated. (Test: 
compare_content_length in EXEC-59)

Root Cause: rebuild_v10.py extracted text to XML, but Word XML element 
serialization limits string content to 200–300 chars. Text extraction 
also loses tables, styles, list structure.

Solution: Implemented element-level copying in rebuild_v11.py:
- Import formatted elements (paragraphs, tables, runs) as XML from source
- Deepcopy into target document instead of extracting text
- Result: 100% formatting preservation (tables, fonts, colors, spacing)

Validation: 
- v11 rebuild shows 46 tables (vs 8 in v5 baseline, 0 in v10)
- 919 paragraphs with full content (vs 150 in v10)
- All visual hierarchy and styles preserved
- Diff: v10 Appendix B (500 chars) vs v11 (3,688 chars, tables intact)

Commit: 62051ac
```

---

## Test Strategy

**Purpose:** Establish a testing approach that shapes scope estimation and execution planning.

Testing strategy determines how thoroughly code is validated before merge and affects story point estimation through a multiplier applied to raw complexity-based estimates.

**Options & Multipliers:**

1. **TDD (Test-Driven Development) — ×1.3 multiplier**
   - Tests are written BEFORE implementation (red-green-refactor cycle)
   - Use when: Requirements are stable and well-defined, high-risk component, high-reuse potential
   - Multiplier accounts for upfront test design and iterative refinement
   - Example: Core entity resolution algorithm, where correctness is non-negotiable

2. **Testing-After — ×1.1 multiplier**
   - Code is written first; tests are written after (or light validation only)
   - Use when: Requirements are fluid, exploratory work, low-risk or one-off code
   - Multiplier is minimal because implementation speed is prioritized
   - Example: Prototype extraction method for a new format, investigating feasibility

3. **Mixed — ×1.2 multiplier**
   - Combination of both: critical paths use TDD; exploratory parts tested after
   - Use when: Complex story with both mature and uncertain components
   - Multiplier balances upfront design rigor with pragmatic iteration
   - Example: Full text extraction pipeline (core modules TDD, format handlers tested-after)

**How to Apply:**

1. **Choose a strategy** during story estimation (Story, Subtask, or Task ticket)
2. **List it explicitly** in the story description or a comment (e.g., "Test Strategy: Mixed")
3. **Multiply the raw estimate** by the strategy multiplier:
   - Base estimate (5 points) + TDD strategy (×1.3) = 7 points (rounded)
   - Base estimate (5 points) + Testing-After (×1.1) = 5–6 points (minimal overhead)
4. **Acceptance Criteria** must reflect the chosen strategy (see section below)

**Example Story with Test Strategy:**
```
Title: Text Extraction (PDFs, DOCX, XLSX, Images)

User Story: As a KG extraction pipeline, I need to extract text from diverse formats,
so that I can process all source materials regardless of format.

Test Strategy: Mixed
- Core module (text extraction, error handling): TDD
- Format-specific handlers (PDF, DOCX, XLSX): Testing-After

Acceptance Criteria:
✓ Core extraction module has unit tests (red-green-refactor, >80% coverage)
✓ PDF handler: extract_pdf_text(filepath) → str (callable, basic format tests)
✓ DOCX handler: extract_docx_text(filepath) → str (callable, formatting preserved)
✓ XLSX handler: extract_xlsx_cells(filepath) → list (callable, all cells extracted)
✓ OCR handler: extract_ocr_text(image_path) → str (callable, pytesseract integration)
✓ Error handling (corrupt files, missing paths): logs and continues pipeline
✓ Performance: 100 files extracted < 2 minutes
✓ Integration tests pass (end-to-end with sample documents)
✓ Code review approved
```

---

## Acceptance Criteria = Test Checklist

**Key Principle:** Acceptance Criteria ARE the test checklist. They are not separate from testing — they define what must be tested and what constitutes "done."

**Why This Matters:**

Every story, task, or subtask in this workflow has acceptance criteria. Each criterion is a testable condition that must pass before the work is considered complete. When you run tests, code review, or UAT (user acceptance testing), you are validating that each acceptance criterion is met. They are the bridge between requirements and testing.

**Pattern Across Ticket Types:**

Look at the examples throughout this document:

- **Story (EXEC-70):** "Extract text from PDFs (pypdf)" ← this is a test: does the PDF extraction function work?
- **Subtask:** "Handle corrupt PDFs gracefully" ← this is a test: does the code handle errors?
- **Task:** "Unit tests: 8 cases (matching, non-matching, edge cases)" ← this IS the testing criterion
- **Epic (EXEC-68):** "95%+ entity resolution accuracy" ← this is a validation metric that must be tested

Each criterion is phrased as testable: "verify X", "ensure Y", "code passes Z", "performance < time T".

**How to Write Strong Acceptance Criteria:**

1. **Make them testable:** Each one must have a clear pass/fail outcome
   - Good: "Extract text from PDFs using pypdf (>95% accuracy on sample set)"
   - Bad: "PDF extraction works well"

2. **Include multiple types:**
   - Functional tests (does it work?)
   - Error handling (does it fail gracefully?)
   - Performance tests (is it fast enough?)
   - Quality gates (code review, lint, coverage)

3. **Reference the chosen Test Strategy:** If you chose TDD, criteria emphasize unit test completeness. If Testing-After, criteria are still testable but may focus on integration or functional validation.

4. **Make them part of Definition of Done:** No work is merged until all criteria are validated.

**Example: What Strong Criteria Look Like**

From EXEC-70 (Phase 1.2 Text Extraction Pipeline):
```
Acceptance Criteria:
✓ Extract text from PDFs (pypdf)                      ← Functional test
✓ Extract text from DOCX (python-docx)                ← Functional test
✓ Extract cells from XLSX (openpyxl)                  ← Functional test
✓ OCR images (pytesseract)                            ← Functional test
✓ Handle corrupt files gracefully                     ← Error handling test
✓ Performance: 100 files < 2 min                      ← Performance test
✓ Unit tests: 8 format types + 3 error scenarios     ← Quality gate (test coverage)
✓ Code review + merge                                 ← Quality gate (peer review)
✓ PHASE_1_2_IMPLEMENTATION.md created                ← Documentation test
```

Each one is directly testable and collectively they define what it means for this story to be "done."

**When You Test:**

When you run the code, write tests, or review a PR, you are checking acceptance criteria. If a criterion fails, the work is not done — go back to the developer, ask for fixes, re-test. If all criteria pass, the work is ready to merge.

---

## Personas Throughout the Workflow

Personas are defined once in an IDEA and flow through all related Epics and Stories. This ensures all work stays focused on actual user needs.

**Persona Flow:**

```
IDEA-20: Literary Manager KG Initiative
├─ Personas:
│   ├─ Writer (track submissions, analyze outcomes)
│   └─ Literary Agent (advise clients, understand publishing record)
│
└─ EXEC-68: Literary Manager KG Foundation [Epic]
    ├─ User Story: "As a writer, I want to extract and query character/manuscript data..."
    │
    ├─ EXEC-69: File Indexing [Story]
    │   └─ User Story: "As a writer, I need to catalog my unstructured documents..."
    │
    ├─ EXEC-70: Text Extraction [Story]
    │   └─ User Story: "As a KG pipeline, I need to extract text from all document types..."
    │
    └─ EXEC-71: Entity Extraction [Story]
        └─ User Story: "As a writer, I need to identify key literary entities..."
```

**Rules for Personas:**

1. **Define once in IDEA:** When creating an IDEA ticket, list all personas that will benefit
2. **Reference in Epic:** The Epic's user story uses one of the IDEA's personas
3. **Inherit in Stories:** Each child Story references the same persona(s) or a related one
4. **Validate in PRD:** The Product Requirements Document links personas to success metrics and acceptance criteria
5. **Not individuals:** Personas are user categories (Writer, Literary Agent, Publisher), never named people (Fred, Alice, Bob)

**Stakeholder Distinction:**

Stakeholders are listed in IDEAs for context but do NOT appear in user stories:
```
IDEA-20 Lists:
- Personas: Writer, Literary Agent (these go into user stories)
- Stakeholders: Fred Chong Rutherford (interested in validating KG pattern)
              | The Client (needs reports for their use case)
```

Stakeholders may be notified of epic completion and progress, but the user story always reflects the persona's needs, not the stakeholder's.
