# Atlassian transport (EXEC-442)

Makes the **Atlassian Rovo MCP a soft default, not a hard requirement** for the Atlassian Companion. The skills name *operations* (search / get / create / update / transition / page CRUD) and resolve them through a small **contract** with two interchangeable adapters:

- **MCP adapter** (default) — the Rovo MCP tools; zero setup in an interactive Claude/Codex session.
- **REST adapter** — [`atlassian_rest.py`](atlassian_rest.py), stdlib `urllib`, API-token auth; runs with **no MCP** (CI, cron, non-Claude runtimes), and is cleaner for bulk.

## Files
- **`transport-contract.md`** — the operation → MCP-tool → REST-endpoint mapping. Skill authors point here instead of hardcoding a tool name.
- **`atlassian_rest.py`** — the REST adapter (`Config.from_env()` + `Transport`). All egress funnels through `_send`, so it's fully mockable.
- **`test_atlassian_rest.py`** — 12 stdlib tests, **zero live calls** (fake sender).

## REST quick start
```bash
export ATLASSIAN_SITE=your-site.atlassian.net ATLASSIAN_EMAIL=you@example.com ATLASSIAN_API_TOKEN=...
python3 -c "from atlassian_rest import Config, Transport; print(Transport(Config.from_env()).jira_get('EXEC-1', ['summary']))"
```

The deterministic helpers (`decompose.py`, `audit.py`, `gen_orchestration.py`) stay transport-free — they parse/analyze fetched data and make no calls.

## No-MCP smoke
The REST path is exercised **offline** by the test suite (fake sender — `python3 test_atlassian_rest.py`), proving every contract operation builds the right request with no MCP and no network. The live smoke is the quick-start above (needs a token).
