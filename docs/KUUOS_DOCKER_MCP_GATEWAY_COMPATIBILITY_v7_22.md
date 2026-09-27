# KuuOS Docker MCP Gateway Compatibility v7.22

## Purpose

KuuOS now has several individually verified MCP surfaces:

- GitHub;
- Git;
- Filesystem;
- Lean-LSP;
- Context7;
- Playwright;
- Chrome DevTools.

v7.22 verifies whether those kinds of servers can be placed behind one containerized orchestration surface without changing their authority semantics.

The target is Docker MCP Gateway.

## Exact upstream target

```text
docker/mcp-gateway
main SHA: a34df45d4ec0e941a9853ad768c4f6cd818966b3
Go: 1.25.12
MCP Go SDK: 1.4.1
```

The plugin is built directly from that exact source SHA in CI.

## Why a real Gateway probe is required

A CLI help check would prove only that the binary starts.

v7.22 instead exercises the actual forwarding path:

```text
KuuOS MCP client
-> Docker MCP Gateway
-> profile
-> isolated containerized MCP server
-> read-only tool
-> response
-> Gateway
-> KuuOS client
```

## Deterministic fixture

The probe server is intentionally tiny.

It exposes one tool:

```text
kuuos_probe_echo
```

and returns:

```text
KUUOS_GATEWAY_PROBE:<message>
```

The container entry declares:

```text
disableNetwork: true
```

so this test does not require external service access from the downstream MCP server.

## Local profile

The profile is created from a trusted local `file://` server entry under the Docker MCP catalog directory.

No external Docker MCP catalog is required.

This matters because the compatibility result should test the Gateway itself rather than availability of a third-party catalog service.

## Docker CE mode

The upstream documentation explicitly supports non-Desktop Docker environments by using:

```text
DOCKER_MCP_IN_CONTAINER=1
```

v7.22 also declares Docker CE mode for the CI environment.

Profiles are enabled before the live probe.

## Live protocol path

The test performs:

```text
docker mcp gateway run --profile kuuos_gateway_probe
-> initialize
-> tools/list
-> discover KuuOS probe tool
-> tools/call
-> observe deterministic marker
```

A successful profile listing alone is not sufficient.

## Authority boundary

Docker Gateway provides:

- lifecycle;
- container isolation;
- aggregation;
- tool discovery;
- routing;
- profile selection.

It does not create downstream authority.

Therefore:

```text
server in profile
!=
tool authorized for every use
```

and:

```text
Gateway can route a write-capable tool
!=
Gateway grants permission to write
```

Provider-specific and KuuOS-specific authority remain separate.

## Relation to KuuOS non-collapse

The Gateway is another presentation of the MCP capability surface.

A tool may appear:

- directly from its original MCP server;
- through Docker Gateway;
- through a host connector.

These presentations may be operationally equivalent for a particular tool call, but they are not assumed to be the same authority source.

## Promotion

If the exact-head live probe is GREEN, the development registry may promote:

```text
docker_mcp_gateway:
  recommended_orchestration
->
  verified_compatible
```

That status means Docker Gateway has demonstrated real tool discovery and forwarding in the KuuOS development environment.

It does not mean every downstream server is automatically verified or authorized.
