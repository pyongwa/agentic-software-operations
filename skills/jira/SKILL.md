---
name: jira
description: Governing skill for Fred's two-project JIRA workflow; routes to jira-workflow, jira-persona-driven-tickets, or jira-story-points
lifecycle:
  phase: project-start
  cadence: on-demand
  trigger: "any JIRA work — routes to jira-workflow / jira-persona-driven-tickets / jira-story-points"
---

# JIRA: Two-Project Workflow Governance

Fred's JIRA uses a **two-project system** separating discovery (IDEA) from execution (EXEC).

```
IDEA Project           EXEC Project
Discovery & Validation → Implementation & Delivery
├─ Idea                ├─ Epic
├─ Opportunity         ├─ Story
├─ Solution            ├─ Task
└─ Feature             ├─ Subtask
                       └─ Bug
```

---

## What Are You Doing?

Choose the relevant skill based on your current task:

### **A) Understanding the workflow and project structure**
→ Use **jira-workflow**

- When: You need to understand IDEA vs. EXEC projects, when to create each ticket type, how work flows from discovery to execution
- You'll learn: Two-project pattern, workflow diagram, key principles, when to create Ideas, Epics, Stories, Tasks, Bugs, when to create Subtasks
- Example: "Should I put this in IDEA or EXEC? When do I create an Epic?"

### **B) Writing a ticket (IDEA, Epic, Story, Task, Subtask, or Bug)**
→ Use **jira-persona-driven-tickets**

- When: You're creating or updating a ticket and need to know what structure, sections, and content it should have
- You'll learn: Persona vs. stakeholder distinction, required sections for each ticket type, user story format, acceptance criteria standards, how personas flow through work
- Example: "How do I write a good story ticket? What should the user story look like?"

**Special: Writing a PRD for an Epic?** → Also use **confluence-prd-writing**
- When: You need to create the detailed specification (PRD) that an Epic links to
- You'll learn: PRD structure, how to incorporate personas, success metrics, phases, acceptance criteria
- PRDs are the source of truth for what an Epic delivers

### **C) Estimating effort or closing work**
→ Use **jira-story-points**

- When: You're assigning story points, estimating tokens/cost, or adding a retrospective comment to a closing ticket
- You'll learn: Fibonacci scale, token cost calculation, when to assign each SP level, how to write retrospective comments, weekly reporting format
- Example: "What's the story point estimate for this? How do I calculate cost? What goes in the retrospective comment?"

---

## Core Principles (Apply to All)

1. **Personas drive user stories.** Define personas once in IDEA; reference them consistently across Epics and Stories.
2. **All tickets must be testable.** Every acceptance criterion must be verifiable; every ticket must have clear closure conditions.
3. **Lineage is traceable.** Every EXEC Epic links to its parent IDEA. Every Story links to its parent Epic. This creates a chain of context.
4. **User stories are first lines.** Epics and Stories start with "As a [persona], I [need/want] [action], so that [benefit]."
5. **Effort is visible.** Stories include story points, token estimates, and cost. Retrospectives compare estimates to actuals.

---

## Quick Reference: When to Create Each Type

| Type | Project | Scope | When | Owner |
|------|---------|-------|------|-------|
| **Idea** | IDEA | Hypothesis, research question | You have a hypothesis but haven't committed resources | Brainstorming phase |
| **Epic** | EXEC | 5+ stories, clear deliverable | Idea is approved and ready to execute | Execution phase |
| **Story** | EXEC | 3–10 days of work | Work can be done independently, testable, assignable to one person | Team member |
| **Task** | EXEC | 1–3 days of work | Small, discrete, not user-facing | Team member |
| **Subtask** | EXEC | Part of a Story | Story is complex, needs smaller trackable units | Team member |
| **Bug** | EXEC | Problem + solution | Unexpected behavior discovered with clear reproduction | Team member |

---

## Governing Principles

**Separation of Concerns:** Ideas in IDEA, execution in EXEC. Prevents scope creep.

**Atomic Work:** Each story is one coherent piece. Each task is small and discrete. No ambiguity about what "done" means.

**Linkage:** Every ticket traces back to its parent and forward to its children. Context is always available.

**Personas:** Work flows from persona needs → Epic delivering value to that persona → Stories implementing pieces of that value.

**Visibility:** Estimates and actuals are captured. Weekly reports show velocity, accuracy, trends.

---

## Next Steps

Pick the skill that matches what you need:

1. **Understanding the system?** → `jira-workflow`
2. **Writing or updating a ticket?** → `jira-persona-driven-tickets`
3. **Estimating or closing work?** → `jira-story-points`

Each focused skill is self-contained and executable on its own.
