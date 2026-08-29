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

Always available when the HTTP request satisfies the configured read authorization policy:

- `get_project_state`
- `list_next_actions`
- read-only resource `kuuos://state/project`

Write tools are registered only when `KUUOS_MCP_WRITE_ENABLED=true`:

- `record_continuation`
- `update_project_state`

Write enablement is fail-closed. Startup aborts unless all of the following hold:

1. the selected backend is PostgreSQL;
2. `KUUOS_MCP_OAUTH_ENABLED=true`;
3. the OAuth resource-server configuration is complete;
4. each write request carries the configured write scope (default `kuuos:write`).

## Storage backends

The server selects storage in this order:

1. `KUUOS_MCP_DATABASE_URL` or `DATABASE_URL` → PostgreSQL CAS backend.
2. `KUUOS_MCP_GITHUB_ISSUE_API_URL`, or the default public KuuOS continuation issue when running on Vercel → durable read-only GitHub Issue backend.
3. local JSON at `KUUOS_MCP_STATE_PATH` (default `./var/kuuos-mcp-state.json`) → local/single-host backend.

When a database URL is present the server uses PostgreSQL and creates its single CAS state table idempotently. This is the only backend accepted for remote write mode.

When no database URL is available on Vercel, the bridge reads the canonical fenced JSON state from public Issue #1548 through `GitHubIssueStateStore`. This provides a durable, auditable read path shared by Chat and Work immediately, while keeping writes fail-closed.

## OAuth 2.1 resource-server mode

The MCP server can operate as an OAuth 2.1 protected resource using the MCP Python SDK authorization surface. It verifies bearer tokens through an external RFC 7662 introspection endpoint and publishes RFC 9728 protected-resource metadata automatically.

Enable it with:

```bash
export KUUOS_MCP_OAUTH_ENABLED=true
export KUUOS_MCP_OAUTH_ISSUER='https://auth.example.com'
export KUUOS_MCP_OAUTH_RESOURCE_URL='https://kuuos-chat-work-mcp.vercel.app/api/mcp'
export KUUOS_MCP_OAUTH_INTROSPECTION_URL='https://auth.example.com/oauth2/introspect'
export KUUOS_MCP_OAUTH_INTROSPECTION_CLIENT_ID='...'
export KUUOS_MCP_OAUTH_INTROSPECTION_CLIENT_SECRET='...'
```

Optional policy variables:

```bash
export KUUOS_MCP_OAUTH_READ_SCOPE='kuuos:read'
export KUUOS_MCP_OAUTH_WRITE_SCOPE='kuuos:write'
export KUUOS_MCP_OAUTH_AUDIENCE='https://kuuos-chat-work-mcp.vercel.app/api/mcp'
```

The read scope is enforced by the MCP SDK at the HTTP resource-server boundary. Write tools additionally require the write scope inside each tool handler.

The authorization server remains external: this bridge validates tokens; it does not mint them. For ChatGPT OAuth connectivity, use an authorization server whose discovery metadata supports the required flow and refresh tokens. OIDC deployments intended for persistent ChatGPT connectivity should advertise and issue `offline_access`.

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

The remote endpoint is:

```text
https://<deployment-host>/api/mcp
```

Safe read-only sequence:

1. deploy with `KUUOS_MCP_WRITE_ENABLED` unset;
2. verify `/healthz`;
3. verify MCP initialize, tool discovery, `get_project_state`, and `list_next_actions`.

Safe writable sequence:

1. attach PostgreSQL as `DATABASE_URL` or `KUUOS_MCP_DATABASE_URL`;
2. configure the OAuth variables above with an HTTPS issuer and introspection endpoint;
3. keep `KUUOS_MCP_WRITE_ENABLED` unset and verify authenticated reads first;
4. verify the authorization server issues the read scope, write scope, audience/resource binding, and refresh tokens needed by the ChatGPT OAuth flow;
5. set `KUUOS_MCP_WRITE_ENABLED=true`;
6. confirm tool discovery now includes the two write tools;
7. execute a CAS write with the current version and verify the version increments once;
8. replay the old version and verify stale-writer rejection;
9. keep Issue #1548 as audit/recovery after PostgreSQL becomes primary.

Until PostgreSQL credentials and OAuth provider credentials are actually injected and verified, the production MCP must remain read-only.
