# Atlassian transport contract

The Ops4Atlassian skills talk to Jira/Confluence through this small **contract**, not through hardcoded tool names. That makes the **Atlassian Rovo MCP a soft default, not a hard requirement** — the same skills run via the **REST API** (an API token) when no MCP is present.

> **Rule for skill authors:** in a skill's operative steps, name the **operation** (e.g. "*update* the issue's assignee"), then point here. Do **not** bake a specific MCP tool name into the instruction as the only path.

## Operations → adapters

| Operation | MCP adapter (default) | REST adapter (`atlassian_rest.py`) | REST endpoint |
| --- | --- | --- | --- |
| Jira **search** | `searchJiraIssuesUsingJql` | `Transport.jira_search(jql, fields)` | `POST /rest/api/3/search` |
| Jira **get** | `getJiraIssue` | `Transport.jira_get(key, fields)` | `GET /rest/api/3/issue/{key}` |
| Jira **create** | `createJiraIssue` | `Transport.jira_create(project, type, fields)` | `POST /rest/api/3/issue` |
| Jira **update** | `editJiraIssue` | `Transport.jira_update(key, fields)` | `PUT /rest/api/3/issue/{key}` |
| Jira **transition** | `transitionJiraIssue` | `Transport.jira_transition(key, id)` | `POST /rest/api/3/issue/{key}/transitions` |
| Confluence **get page** | `getConfluencePage` | `Transport.cf_get_page(id)` | `GET /wiki/api/v2/pages/{id}` |
| Confluence **create page** | `createConfluencePage` | `Transport.cf_create_page(...)` | `POST /wiki/api/v2/pages` |
| Confluence **update page** | `updateConfluencePage` | `Transport.cf_update_page(...)` | `PUT /wiki/api/v2/pages/{id}` |

Field shapes are identical across adapters (e.g. assignee = `{"accountId": "<id>"}`); the transport only changes *how* the call is delivered.

## Bulk operations — the adapter changes the math

The `jira-mcp-bulk-operations` method (self-paginate into batches of ~20, subagent context-firewall, `jq`-on-saved-file) exists to work **around** the MCP returning the full issue (~5KB) per call. Over **REST** you control `fields`, so payloads are small and Jira's own bulk/pagination applies — most of that mitigation is unnecessary. So:
- **MCP adapter:** use the batch-of-20 / subagent-firewall method.
- **REST adapter:** request minimal `fields`, page with `startAt`/`maxResults`; no jq-on-saved-file needed.

Same operation, transport-appropriate execution.

## Choosing an adapter

- **MCP** (default): zero setup if the Atlassian Rovo MCP is connected. Best for interactive Claude/Codex sessions.
- **REST**: set `ATLASSIAN_SITE`, `ATLASSIAN_EMAIL`, `ATLASSIAN_API_TOKEN`; `from atlassian_transport.atlassian_rest import Config, Transport`. Best for runs-without-an-MCP, CI, cron, and any non-Claude runtime. Cleaner for bulk.

The deterministic helpers (`decompose.py`, `audit.py`, `gen_orchestration.py`) are **transport-free** — they parse/analyze data the transport fetched; they make no calls themselves.
