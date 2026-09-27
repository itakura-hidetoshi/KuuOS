# KuuOS Fetch + Official MCP Docs Compatibility v7.23

## Purpose

KuuOS development now has verified repository, semantic, documentation, browser, and orchestration MCP surfaces.

v7.23 adds two more read-only planes:

```text
MCP Fetch
-> generic external web content retrieval

Official MCP Docs
-> current Model Context Protocol specification search
```

These are useful for different reasons and are not collapsed into one source.

## Fetch MCP

The pinned target is:

```text
reference source metadata: mcp-server-fetch 0.6.3
published package: discovered from the live package index, then pinned after the first GREEN
mcp SDK: exact upstream lock 1.29.0
reference servers SHA f46d9578...
```

The exact SDK pin follows the upstream `src/fetch/uv.lock`, not only the looser `mcp>=1.29,<2` package constraint.

The live probe:

```text
initialize
-> tools/list
-> fetch(https://example.com/)
```

and requires the deterministic `Example Domain` marker.

### Fetch network boundary

The reference Fetch server explicitly warns that it can access local/internal IP addresses.

KuuOS therefore records:

```text
fetch_server_can_access_internal_networks_in_general = true
```

but the compatibility probe itself uses only a public external URL and does not grant internal-network authority.

## Official MCP Docs

The current MCP specification repository explicitly configures:

```text
https://modelcontextprotocol.io/mcp
```

as its `mcp-docs` server and identifies:

```text
SearchModelContextProtocol
```

as the preferred authoritative tool for current specification content.

The pinned reference repository head is:

```text
modelcontextprotocol/modelcontextprotocol
ab3a39c13bd23be691c2760e1c6c5c15a64582e1
```

## Modern protocol path

The current MCP specification is `2026-07-28`.

That version is stateless:

- no initialize/initialized handshake;
- no MCP session ID;
- protocol metadata is carried per request;
- HTTP requests carry `MCP-Protocol-Version`;
- method/tool routing is mirrored in `Mcp-Method` / `Mcp-Name`.

v7.23 therefore tests the official docs server using that modern request model rather than forcing it through the older v1 SDK/session model used by the reference Fetch server.

This is an important compatibility distinction:

```text
Fetch reference server
-> MCP SDK 1.x / legacy initialization

Official docs endpoint
-> MCP 2026-07-28 stateless HTTP
```

Both remain valid conditioned surfaces.

## Live docs probe

The probe performs:

```text
tools/list
-> require SearchModelContextProtocol
-> tools/call(SearchModelContextProtocol)
```

with the required per-request metadata and modern HTTP headers.

The search asks for current `tools/list` protocol metadata.

A non-empty result is required.

## Authority

The official MCP Docs server is authoritative for current MCP specification content.

It is not authoritative for:

- KuuOS repository state;
- KuuOS Lean theorems;
- exact KuuOS GitHub HEAD;
- local KuuOS working bytes.

Likewise, generic Fetch content is only external evidence.

The authority relationship is:

```text
for MCP specification:
  official MCP Docs > generic external pages

for exact KuuOS behavior:
  repository-local evidence > external docs/fetch
```

## Promotion

If the final exact-head CI is GREEN:

```text
mcp_fetch:
  recommended_read_only -> verified_compatible

mcp_docs:
  recommended_read_only -> verified_compatible
```

Neither promotion grants write or source authority.


## Fetch release/source discrepancy

The first v7.23 run found that the current reference-tree version `0.6.3` is not published as `mcp-server-fetch==0.6.3`.

KuuOS therefore does not pretend the source-tree version is installable. The probe first resolves the actually published package version with the upstream SDK lock, records it, and then starts that exact release. After the first complete GREEN run, that observed release is pinned in the registry evidence.
