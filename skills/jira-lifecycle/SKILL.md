---
name: jira-lifecycle
description: Complete JIRA ticket lifecycle — open, progress, comment, PR link, close. Use on any EXEC ticket before starting and after finishing work.
lifecycle:
  phase: execution-loop
  cadence: loop-until-done
  trigger: "open -> progress -> PR -> close on any EXEC ticket, before starting and after finishing"
---

# JIRA Ticket Lifecycle

> **Transport:** the Jira operations here (search, comment, assignee/update, transition) resolve through the [Atlassian transport contract](../../../atlassian-transport/transport-contract.md) — the **Rovo MCP** by default, a **REST** adapter (API token) when no MCP is present. Name the *operation*, not a hardcoded tool.

Every ticket passes through these stages. Execute each stage without being asked.

## Before Starting Work

1. If the ticket does not exist, create it using the `jira` skill.
2. Label anchor tickets (design, architecture, session-tracking) with `session-anchor`.
3. Link child tasks to their parent Epic using createIssueLink:
   - type: "is child of" (inward: child, outward: parent Epic)
4. Confirm the ticket is In To Do status before transitioning.

## When Starting Work

Immediately transition the ticket to In Progress:
```
getTransitionsForJiraIssue(cloudId, issueKey)
  → find the transition ID for "In Progress"
transitionJiraIssue(cloudId, issueKey, transitionId)
```

Write an opening comment:
```
addCommentToJiraIssue(cloudId, issueKey,
  "Starting [YYYY-MM-DD]. Approach: [one sentence describing the plan].")
```

## During Work

Write a working comment for any significant decision or pivot. Not for every
action — only for things that would confuse a future reader of the ticket.

If blocked:
- Add label `blocked` via editJiraIssue
- Write a blocker comment: "Blocked [date]: [description]. Waiting on: [ticket key or person]."

## Completing Work

**Commit format:**
```
[EXEC-NNN] Brief description of what changed
```

**PR title format:**
```
[EXEC-NNN] What this PR delivers
```

After PR is created, add the PR URL as a comment:
```
addCommentToJiraIssue(cloudId, issueKey,
  "PR: [URL]. Ready for review.")
```

Run tests before marking done. Do not close the ticket until tests pass.

## Browser Testing (UI Stories Only)

UI stories require browser testing evidence before closing. Follow this workflow:

### Setup
1. Deploy the code (dev, staging, or test environment as appropriate)
2. Open browser (Chrome DevTools recommended)
3. Log in with appropriate test credentials
4. Open Developer Tools (F12 or right-click → Inspect)
5. Navigate to the feature being tested

### Execute Browser Testing Checklist
- Run through each acceptance criterion from the JIRA story
- For each item:
  - Perform the action described
  - Verify expected result
  - Check for console errors (DevTools Console tab)
  - Check for visual glitches (responsive layout, colors, spacing)
  - Test edge cases mentioned in AC (empty states, maximum length, special characters)

### Capture Evidence
- Take screenshots of key successful states
- Record a video if the feature is interactive (screen recording tools: QuickTime, Loom, etc.)
- Attach evidence to the JIRA ticket
- Add comment: "Browser testing complete: [link to evidence/screenshots]"

### Report Bugs
- If issues found, create a new bug JIRA ticket immediately
- Link to parent story: createIssueLink with "is blocked by" relationship
- Attach evidence (screenshots/videos) to the bug ticket
- Do NOT close the story until bugs are resolved or documented as deferred

### Verify Complete
- All AC items tested and passing
- Evidence attached to story
- No open bugs blocking the story
- Story cannot close without this evidence documented

## Regression Testing (All Stories)

When closing any story, regression tests must be tracked to prevent future regressions.

### Update Test Plan
1. Locate the project's Test Plan document (usually in Confluence under project space)
2. Add new section under "Regression Tests" with the story key (e.g., "EXEC-1234")
3. List the acceptance criteria as regression test items:
   - Include steps to reproduce/verify
   - Include expected result
   - Note any edge cases or boundary conditions

### For Bug Fix Stories
- Ensure AC include explicit regression testing steps
- These steps should verify the related feature still works after the fix
- Example: "Fix pagination bug → AC should include: verify pagination works for both small and large datasets"

### Before Closing
- Add comment: "Test Plan updated: [regression testing items added under EXEC-XXXX]"
- Verify the Test Plan entry is complete and clear enough for future testing

## Closing a Ticket

1. Write the retrospective comment using the template from the JIRA Skill page
   (SD/2523138 — Session Comment Template section). Include references to:
   - Browser testing evidence (for UI stories) or manual testing performed
   - Test Plan updates made (regression testing items added)
2. Transition to Done:
   ```
   getTransitionsForJiraIssue(cloudId, issueKey)
     → find transition ID for "Done"
   transitionJiraIssue(cloudId, issueKey, transitionId)
   ```
3. Update the Confluence Current State page for this project:
   - Update "Current State" section
   - Update "Next Action" section
   - Add entry to "Decisions This Sprint" if any decisions were made
4. If this closes an Epic: update the Epic's `## Current State` section in its description.

## MCP Call Reference

```
Transition ticket:    transitionJiraIssue(cloudId, issueKey, transitionId)
Get transitions:      getTransitionsForJiraIssue(cloudId, issueKey)
Add comment:          addCommentToJiraIssue(cloudId, issueKey, body)
Link issues:          createIssueLink(cloudId, type, inwardIssue, outwardIssue)
Edit ticket fields:   editJiraIssue(cloudId, issueKey, fields)
```

All calls use cloudId: `fredchongrutherford.atlassian.net`

## Anti-Patterns to Avoid

- ❌ Starting code before transitioning ticket to In Progress
- ❌ Closing a ticket without a retrospective comment
- ❌ Expressing blocking relationships as prose ("see EXEC-NNN") instead of JIRA issue links
- ❌ Merging without adding the PR URL as a ticket comment
- ❌ Updating ticket status only when asked — do it proactively
- ❌ Closing a UI story without browser testing evidence
- ❌ Closing any story without updating regression testing documentation
