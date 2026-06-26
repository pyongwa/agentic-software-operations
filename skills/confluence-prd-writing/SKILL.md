---
name: confluence-prd-writing
description: PRD structure, personas, success metrics, and templates for Product Requirements Documents
lifecycle:
  phase: project-start
  cadence: once-per-project
  trigger: "writing the PRD for an EXEC Epic (structure, personas, success metrics)"
---

# Confluence: PRD Writing for JIRA Epics

## Overview

A **Product Requirements Document (PRD)** is the detailed specification for an EXEC Epic. Every Epic in JIRA links to its PRD in Confluence.

**Relationship:**
```
JIRA IDEA (high-level hypothesis)
  ↓
JIRA EXEC Epic (initiative with user story)
  ↓
Confluence PRD (detailed specification)
  ↓
JIRA Stories (implementation tasks)
```

The PRD is the **source of truth** for:
- How the epic solves the problem stated in the IDEA
- Which personas benefit and what value they receive
- Success metrics for the epic
- Architecture and technical approach
- Phases and decomposition
- Acceptance criteria

---

## PRD Structure

Every PRD must include these sections:

### 1. **Problem & Personas** (from parent IDEA)

Reference the personas from the parent IDEA ticket. Describe:
- What problem each persona faces
- Why it matters to them
- Current pain points

Example:
```
## Problem & Personas

**Writer Persona:**
Writers manually search 40,000+ files to find which manuscripts have been submitted 
where. They have no systematic way to query: "Which publishers accepted my work?" 
"What's my success rate by genre?" This manual tracking costs 20+ hours/month.

**Literary Agent Persona:**
Literary agents need to understand their clients' publishing records to advise on 
genre positioning and publisher targeting. Currently, they rely on clients to 
provide this information—no aggregated view exists.
```

### 2. **Success Metrics** (testable, tied to Epic acceptance criteria)

Define how you'll know the PRD was successfully delivered. Include:
- Quantitative metrics (# of entities extracted, accuracy %, performance benchmarks)
- Qualitative metrics (user satisfaction, feature completeness)
- Acceptance criteria (tied to Epic acceptance criteria)

Example:
```
## Success Metrics

**Extraction & Quality:**
- ✓ Extract 500+ entities from 200+ sample documents (Writer use case)
- ✓ 95%+ entity resolution accuracy (Literary Agent can trust the data)
- ✓ Process documents in < 2 sec per page (acceptable performance for interactive use)

**User Value:**
- ✓ Writer can query: "Which publishers accepted my work?" in < 1 second
- ✓ Writer can see success rates by genre/publisher with confidence scores
- ✓ Literary Agent can generate client analysis report in < 5 minutes
- ✓ All entities have source citations (users can verify data)

**Acceptance Criteria (from Epic):**
- ✓ All 5 phases implemented (extraction through visualization)
- ✓ Interactive KG explorer with zoom and cluster navigation
- ✓ Character profile reports with proper formatting
- ✓ Total cost < $50 for full extraction + synthesis
```

### 3. **Architecture & Approach**

High-level design of how the epic solves the problem. Include:
- Major components
- Data flow
- Technology choices and why
- Constraints and assumptions

Example:
```
## Architecture

**Components:**
1. File Indexer: Catalogs source documents (PDFs, DOCX, emails, spreadsheets)
2. Text Extractor: Extracts text from diverse formats
3. Entity Extractor: Identifies literary entities (characters, manuscripts, publishers, submissions)
4. Entity Resolver: Clusters name variants to canonical names
5. Graph Builder: Constructs relationship graph
6. Query Engine: Traverses graph for multi-hop queries
7. Report Generator: Synthesizes character profiles and analytics
8. Interactive Explorer: Web-based visualization with zoom and filtering

**Data Flow:**
Source Documents → Indexing → Text Extraction → Entity Extraction → 
Resolution → Graph Building → Storage → Query & Reporting

**Technology:**
- Python 3.9+ for extraction pipeline
- Claude API for entity identification (Pydantic schemas)
- NetworkX for graph structure
- python-docx for report synthesis
- vis-network for interactive visualization
- SQLite for persistence (or cloud option)

**Assumptions:**
- Source documents remain on-premises (no cloud upload)
- Cost must stay below $50 for full pipeline
- Performance acceptable up to 500K entities
```

### 4. **Phases & Decomposition** (linked to child Stories)

Break the epic into phases. For each phase, list:
- What it delivers
- Why it matters (which persona needs it)
- Child stories (link to JIRA story keys)
- Estimated complexity (story points)

Example:
```
## Phases & Decomposition

**Phase 1: File Cataloging & Text Extraction (Writer value: foundation)**
- EXEC-69: File Indexing (SP 3) — Discover all source documents
- EXEC-70: Text Extraction (SP 5) — Extract text from all formats
- Deliverable: Complete indexed text corpus ready for analysis

**Phase 2: Entity Extraction & Resolution (Literary Agent value: data quality)**
- EXEC-71: Entity Extraction (SP 8) — Identify manuscripts, publishers, outcomes
- EXEC-72: Entity Resolution (SP 5) — Consolidate name variants
- Deliverable: Canonical entity list with confidence scores

**Phase 3: Graph Building & Querying (Writer value: analysis)**
- EXEC-73: Graph Building (SP 8) — Construct relationship graph
- EXEC-74: Graph Queries (SP 5) — Enable multi-hop traversal
- EXEC-75: Document Registry (SP 5) — Track provenance and sources
- Deliverable: Queryable knowledge graph with source citations

**Phase 4: Reporting & Visualization (Both personas: actionable insights)**
- EXEC-76: Character Profile Reports (SP 5) — Narrative profiles
- EXEC-77: DOCX Formatting (SP 5) — Publication-ready documents
- EXEC-78: Interactive Explorer (SP 5) — Zoomable KG visualization
- Deliverable: Multiple report types and interactive interface

**Total Effort:** 54 story points, 112K–217K tokens, ~$1.60
```

### 5. **Acceptance Criteria** (must match Epic acceptance criteria)

Testable conditions for PRD completion. These should align exactly with Epic AC:

Example:
```
## Acceptance Criteria

✓ All 5 phases implemented and integrated (EXEC-69 through EXEC-78 completed)
✓ File indexing correctly catalogs all document formats
✓ Entity extraction achieves 95%+ accuracy on test set
✓ Graph queries complete in < 1 second for 500+ entity networks
✓ Character profile reports export to DOCX with formatting preserved
✓ Interactive explorer renders 500+ entities with zoom and filtering
✓ All source data has citations (trace back to original documents)
✓ Performance benchmarks met (extraction, queries, report generation)
✓ Code review approved, tests > 80% coverage, documentation complete
✓ Total token cost < $50 for full pipeline
```

### 6. **Timeline & Resources** (optional, for planning)

If relevant:
- Estimated completion date
- Dependencies on other work
- Resources or access needed

Example:
```
## Timeline & Resources

**Estimated Duration:** 4–6 weeks (54 SP, depends on parallelization)
**Dependencies:** 
- Access to Literary Manager sample documents (200+ files)
- Claude API access with sufficient quota (~$2K capacity)

**Parallelization:**
- Phase 1 (indexing/extraction) can run independent of others
- Phase 2 (resolution) depends on Phase 1 output
- Phases 3 & 4 can run in parallel once Phase 2 completes
```

---

## How to Write for Personas

When describing problem, metrics, and architecture:

1. **Problem Statement:** Describe the pain point from each persona's perspective
   ```
   Writer: "I need to find which publishers accepted my short stories quickly"
   Literary Agent: "I need aggregated publishing data to advise clients"
   ```

2. **Success Metrics:** Include persona-specific metrics
   ```
   Writer metric: "Query returns results in < 1 second"
   Literary Agent metric: "Report can be generated in < 5 minutes"
   ```

3. **Architecture Explanation:** Reference which components serve which persona
   ```
   "The Interactive Explorer serves the Writer by enabling visual browsing"
   "The Report Generator serves the Literary Agent by creating client-facing analysis"
   ```

---

## PRD Template (Confluence Page)

When creating a PRD in Confluence:

```markdown
# [Epic Title] - Product Requirements Document

**JIRA Epic:** [Link to EXEC-##]
**Parent IDEA:** [Link to IDEA-##]
**Last Updated:** [Date]

## Problem & Personas

[Copy from IDEA, describe each persona and their problem]

## Success Metrics

[Quantitative and qualitative metrics, tied to Epic AC]

## Architecture & Approach

[Components, data flow, technology, assumptions]

## Phases & Decomposition

[Phases with story links and story points]

## Acceptance Criteria

[Must match Epic acceptance criteria]

## Timeline & Resources

[If applicable]

---

## References

**JIRA Epic:** [Link to EXEC-##]
**Child Stories:** [Link to EXEC-##, EXEC-##, ...]
**Confluence Related:** [Links to architecture docs, design docs, etc.]
```

---

## Examples

### Literary Manager KG PRD

**JIRA:** EXEC-68 (Literary Manager KG Foundation)
**Parent IDEA:** IDEA-20
**Location:** https://fredchongrutherford.atlassian.net/wiki/spaces/SD/pages/[ID]

Key sections:
- Problem: Writers can't query their submissions; Literary Agents lack client publishing data
- Personas: Writer (needs analytics), Literary Agent (needs data for advising)
- Success: 500+ entities extracted, 95%+ accuracy, < 1 sec queries
- Architecture: File → Extract → Entity → Resolve → Graph → Query → Report
- Phases: 4 phases (4 weeks, 54 SP)
- Metrics: Cost < $50, performance benchmarks, report generation < 5 min

---

## When to Create a PRD

Create a PRD when:
- Epic is approved in EXEC and ready for detailed specification
- Epic spans 5+ stories and needs clear decomposition
- Success metrics need to be explicit (not just implicit in Epic AC)
- Multiple personas benefit and need clear messaging
- Team needs architecture overview before implementation

---

## How This Connects to JIRA

**JIRA Epic:**
```
Title: Literary Manager KG Foundation
User Story: "As a writer, I want to extract and query character/manuscript data..."
Link to PRD: https://wiki.atlassian.net/.../Literary-Manager-KG-PRD
Child Stories: EXEC-69 through EXEC-78
```

**PRD:**
```
Problem & Personas: [From parent IDEA]
Success Metrics: [Tied to Epic AC]
Phases: [References each child story]
Acceptance Criteria: [Match Epic AC exactly]
```

The PRD is the **detailed how**, the Epic is the **summary what**.

---

## References

- **JIRA Skill (Governing):** Use when understanding the overall workflow
- **JIRA Persona-Driven Tickets:** Use when creating/updating the Epic
- **JIRA Story Points:** Use for phase decomposition and cost estimation
- **Confluence Story Points & Cost Mapping:** Reference for estimation accuracy
