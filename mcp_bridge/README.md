# KuuOS Chat–Work MCP State Bridge

This is a tool-only MCP server that gives Chat and Work a single canonical continuation state.
It does not try to make two agents share hidden runtime memory. Instead, both surfaces read and
write the same explicit state through MCP.

## Invariant

Every write is optimistic compare-and-swap (CAS):

1. call `get_project_state`;
2. retain the returned `version`;
3. call `record_continuation` or `update_project_state` with that value as `expected_version`;
4. if the server reports a conflict, re-read and reconcile.

Therefore a stale Chat or Work session cannot silently overwrite a newer continuation point.
The JSON file is written atomically with `fsync` + `os.replace`; POSIX deployments also serialize
CAS updates with an advisory lock file across worker processes.

## MCP surface

- `get_project_state` — read canonical state and version.
- `record_continuation` — update the common repository/PR/CI/frontier hand-off fields.
- `update_project_state` — general JSON-object patch with CAS.
- `list_next_actions` — lightweight ordered next-action read.
- `kuuos://state/project` — read-only JSON resource for host-side context loading.

## Run locally

Requires Python 3.10+ and the current MCP Python SDK v2.

```bash
python -m venv .venv
. .venv/bin/activate
pip install -e '.[test]'
export KUUOS_MCP_STATE_PATH="$PWD/var/kuuos-mcp-state.json"
kuuos-mcp-bridge
```

The production transport is Streamable HTTP. The MCP Python SDK exposes the server at `/mcp`
when run with `transport="streamable-http"`.

## Deploy

Mount `KUUOS_MCP_STATE_PATH` on durable storage shared by the server workers. The lock file is
created beside it, so the backing filesystem must preserve POSIX advisory locking semantics. Do
**not** expose this write-capable endpoint publicly without authentication. Put it behind an
authenticated gateway (or configure MCP OAuth at deployment time) and TLS before registering it
with ChatGPT.

The SDK enables DNS-rebinding protection for HTTP by default. A public hostname therefore also
requires an explicit deployment allowlist / transport-security configuration appropriate to the
hosting environment; do not disable that protection globally.

## Connect Chat and Work

Register the same authenticated remote MCP URL in both surfaces. Treat this resource as the source
of truth at hand-off boundaries:

```text
Chat ─┐
      ├── remote MCP /mcp ── durable canonical JSON state
Work ─┘
```

Recommended actor values are `chat` and `work`. A continuation write should include the exact
canonical SHA, active PR snapshot, exact-head CI snapshot, mathematical frontier, and ordered next
actions whenever they are available.

## Test

```bash
pytest
```

The state-store tests cover version increments, persistence, stale-writer rejection, and protected
metadata fields.
