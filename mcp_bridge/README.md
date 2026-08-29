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
3. the OAuth configuration is complete;
4. each write request carries the configured write scope (default `kuuos:write`).

## Storage backends

The server selects storage in this order:

1. `KUUOS_MCP_DATABASE_URL` or `DATABASE_URL` → PostgreSQL CAS backend.
2. `KUUOS_MCP_GITHUB_ISSUE_API_URL`, or the default public KuuOS continuation issue when running on Vercel → durable read-only GitHub Issue backend.
3. local JSON at `KUUOS_MCP_STATE_PATH` (default `./var/kuuos-mcp-state.json`) → local/single-host backend.

When a database URL is present the server uses PostgreSQL and creates its single CAS state table idempotently. This is the only backend accepted for remote write mode.

When no database URL is available on Vercel, the bridge reads the canonical fenced JSON state from public Issue #1548 through `GitHubIssueStateStore`. This provides a durable, auditable read path shared by Chat and Work immediately, while keeping writes fail-closed.

## OAuth 2.1 modes

Set the common protected-resource configuration first:

```bash
export KUUOS_MCP_OAUTH_ENABLED=true
export KUUOS_MCP_OAUTH_ISSUER='https://auth.example.com'
export KUUOS_MCP_OAUTH_RESOURCE_URL='https://mcp.example.com/mcp'
export KUUOS_MCP_OAUTH_READ_SCOPE='kuuos:read'
export KUUOS_MCP_OAUTH_WRITE_SCOPE='kuuos:write'
```

`KUUOS_MCP_OAUTH_TOKEN_MODE` selects one of three fail-closed modes.

### External RFC 7662 introspection

This remains the default and preferred production architecture when a dedicated authorization server is available.

```bash
export KUUOS_MCP_OAUTH_TOKEN_MODE='introspection'
export KUUOS_MCP_OAUTH_INTROSPECTION_URL='https://auth.example.com/oauth2/introspect'
export KUUOS_MCP_OAUTH_INTROSPECTION_CLIENT_ID='...'
export KUUOS_MCP_OAUTH_INTROSPECTION_CLIENT_SECRET='...'
```

### External OIDC/JWKS access-token verification

Use this when the authorization server issues signed JWT access tokens.

```bash
export KUUOS_MCP_OAUTH_TOKEN_MODE='jwks'
export KUUOS_MCP_OAUTH_JWKS_URL='https://auth.example.com/.well-known/jwks.json'
```

The verifier checks signature, issuer, expiry, audience/resource binding, and scopes. Unsigned tokens and verification errors fail closed.

### Embedded PostgreSQL-backed authorization server

`embedded` is an explicit single-owner fallback for deployments where a separate authorization server cannot be provisioned. It co-hosts the MCP SDK OAuth 2.1 authorization endpoints with the resource server and keeps OAuth clients, authorization state, codes, access tokens, and rotating refresh tokens in PostgreSQL so replicated HTTP workers do not depend on process memory.

```bash
export KUUOS_MCP_DATABASE_URL='postgresql://...'
export KUUOS_MCP_OAUTH_TOKEN_MODE='embedded'
export KUUOS_MCP_OAUTH_ISSUER='https://mcp.example.com'
export KUUOS_MCP_OAUTH_RESOURCE_URL='https://mcp.example.com/mcp'
export KUUOS_MCP_EMBEDDED_AUTH_SECRET='use-a-long-random-deployment-secret'
```

The owner secret must be at least 24 characters and must be injected through the hosting platform's encrypted secret mechanism; never commit it. The embedded flow uses MCP SDK dynamic client registration and PKCE, presents a small HTTPS login gate at `/login`, issues one-time authorization codes, one-hour opaque access tokens, and rotating refresh tokens. OAuth state is durable in PostgreSQL. A failed owner-secret attempt consumes the pending authorization state rather than permitting repeated guesses against the same flow.

The embedded mode is intentionally opt-in and does not replace the external `introspection` or `jwks` modes. It is useful for a tightly controlled single-owner bridge, but a dedicated authorization service remains preferable when organizational identity, MFA, account lifecycle, or centralized audit policy is required.

The read scope is enforced by the MCP SDK at the HTTP protected-resource boundary. Write tools additionally require the write scope inside each tool handler. If `KUUOS_MCP_WRITE_ENABLED=true`, embedded dynamic registrations default to both read and write scopes; otherwise they default to read only.

## Health receipt

`/healthz` is deliberately non-secret and returns the selected mode/backend, state version, OAuth enablement and token mode, write readiness, and the canonical SHA when available from `KUUOS_MCP_CANONICAL_SHA` or the durable state. It never returns credentials or tokens.

## HTTP security

Streamable HTTP uses MCP SDK v2 with JSON responses and stateless HTTP mode. DNS-rebinding protection remains enabled.

Configure comma-separated allowlists with:

- `KUUOS_MCP_ALLOWED_HOSTS`
- `KUUOS_MCP_ALLOWED_ORIGINS`

On Vercel the deployment, branch, and production hostnames exposed through standard Vercel environment variables are added automatically. Other hosting platforms should set the allowlists explicitly. Local development falls back to localhost/loopback hosts only.

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

## Deployment sequence

Use `mcp_bridge/` as the deployment project root. `requirements.txt` installs the MCP SDK and PostgreSQL driver. `api/mcp.py` exports an ASGI function for Vercel; other Python ASGI hosts can run the same package entrypoint.

Safe read-only sequence:

1. deploy with `KUUOS_MCP_WRITE_ENABLED` unset;
2. set `KUUOS_MCP_CANONICAL_SHA` to the exact deployed repository SHA;
3. configure host/origin allowlists for the deployment hostname;
4. verify `/healthz`;
5. verify MCP initialize, tool discovery, `get_project_state`, and `list_next_actions`.

Safe writable sequence:

1. attach PostgreSQL as `DATABASE_URL` or `KUUOS_MCP_DATABASE_URL`;
2. configure one OAuth mode above;
3. keep `KUUOS_MCP_WRITE_ENABLED` unset and verify authenticated reads first;
4. verify the authorization flow issues the read scope, expected audience/resource binding, and a refresh path suitable for persistent ChatGPT connectivity;
5. set `KUUOS_MCP_WRITE_ENABLED=true`;
6. confirm tool discovery now includes the two write tools;
7. execute one CAS write with the current version and verify the version increments once;
8. replay the old version and verify stale-writer rejection;
9. keep Issue #1548 as audit/recovery after PostgreSQL becomes primary.

Until PostgreSQL and OAuth are actually injected and verified, the production MCP must remain read-only.
