# KuuOS Chat–Work MCP State Bridge

This is a tool-only MCP server that gives Chat and Work one explicit canonical continuation state. It does not attempt to share hidden runtime memory between agents. Both surfaces instead read and, when explicitly enabled behind authentication, write the same versioned state through MCP.

## Invariant

Every write is optimistic compare-and-swap (CAS):

1. call `get_project_state`;
2. retain the returned `version`;
3. call `record_continuation` or `update_project_state` with that value as `expected_version`;
4. if the server reports a conflict, re-read and reconcile.

A stale Chat or Work session therefore cannot silently overwrite a newer continuation point. The local JSON backend writes atomically with `fsync` + `os.replace`; the PostgreSQL backend serializes each transition with a row lock and keeps the payload version synchronized with the indexed version column.

## MCP surface

Always available:

- `get_project_state`
- `list_next_actions`
- read-only resource `kuuos://state/project`

Write tools are registered only when `KUUOS_MCP_WRITE_ENABLED=true`:

- `record_continuation`
- `update_project_state`

Read-only is the default deployment mode. Do not enable write tools on a public endpoint until an authenticated gateway or MCP OAuth layer is in place.

## Storage backends

The server selects storage in this order:

1. `KUUOS_MCP_DATABASE_URL` or `DATABASE_URL` → PostgreSQL CAS backend.
2. `KUUOS_MCP_GITHUB_ISSUE_API_URL`, or the default public KuuOS continuation issue when running on Vercel → durable read-only GitHub Issue backend.
3. local JSON at `KUUOS_MCP_STATE_PATH` (default `./var/kuuos-mcp-state.json`) → local/single-host backend.

When a database URL is present the server uses PostgreSQL and creates its single CAS state table idempotently. This remains the intended writable production backend for replicated/serverless deployments.

When no database URL is available on Vercel, the bridge reads the canonical fenced JSON state from public Issue #1548 through `GitHubIssueStateStore`. This provides a durable, auditable read path shared by Chat and Work immediately, while keeping writes fail-closed. Setting `KUUOS_MCP_WRITE_ENABLED=true` with the GitHub Issue backend aborts startup rather than exposing write tools against a read-only store.

The local JSON backend remains useful for local development and single-host recovery.

## HTTP security

Streamable HTTP uses MCP SDK v2 with JSON responses and stateless HTTP mode. DNS-rebinding protection remains enabled.

Configure comma-separated allowlists with:

- `KUUOS_MCP_ALLOWED_HOSTS`
- `KUUOS_MCP_ALLOWED_ORIGINS`

On Vercel the deployment, branch, and production hostnames exposed through standard Vercel environment variables are added automatically. Local development falls back to localhost/loopback hosts only.

## Run locally

Requires Python 3.10+.

```bash
python -m venv .venv
. .venv/bin/activate
pip install -e '.[test]'
kuuos-mcp-bridge
```

For PostgreSQL:

```bash
pip install -e '.[test,postgres]'
export KUUOS_MCP_DATABASE_URL='postgresql://...'
kuuos-mcp-bridge
```

To test the durable GitHub Issue backend locally without Vercel, set:

```bash
export KUUOS_MCP_GITHUB_ISSUE_API_URL='https://api.github.com/repos/itakura-hidetoshi/KuuOS/issues/1548'
kuuos-mcp-bridge
```

The local MCP endpoint is `/mcp`.

## Vercel deployment

Use `mcp_bridge/` as the Vercel project root. `requirements.txt` installs the MCP SDK and PostgreSQL driver. `api/mcp.py` exports an ASGI function and normalizes the Vercel function route to the server's canonical `/mcp` transport path. `pyproject.toml` declares Vercel's explicit Python entrypoint.

The remote endpoint is therefore:

```text
https://<deployment-host>/api/mcp
```

Safe deployment sequence:

1. deploy with `KUUOS_MCP_WRITE_ENABLED` unset;
2. verify `/healthz` reports `read-only` and the intended backend;
3. verify MCP initialize, tool discovery, `get_project_state`, and `list_next_actions`;
4. add authenticated MCP OAuth or a compatible authenticated gateway;
5. attach PostgreSQL as `DATABASE_URL` or `KUUOS_MCP_DATABASE_URL` for writable canonical state;
6. only then set `KUUOS_MCP_WRITE_ENABLED=true` and verify stale-writer rejection remotely.

Until PostgreSQL and authenticated writes are verified, public Issue #1548 is the durable read/audit control plane and the remote MCP must remain read-only.
