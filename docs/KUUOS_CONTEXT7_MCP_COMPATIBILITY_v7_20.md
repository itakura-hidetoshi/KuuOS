# KuuOS Context7 MCP Compatibility v7.20

## Purpose

The development federation now has four verified local/remote repository surfaces:

- GitHub MCP;
- Git MCP;
- Filesystem MCP;
- Lean-LSP MCP.

v7.20 adds a fifth surface:

```text
Context7 MCP
-> current external library / SDK / API documentation
```

This surface is deliberately advisory.

It can inform code repair and API adaptation, but it does not replace exact local evidence.

## Exact compatibility target

```text
upstash/context7
master SHA: e275a848a420e0d11c2822f61201ee005bfd1133
@upstash/context7-mcp: 4.1.1
Node: >=20.18.1
```

The package currently depends on MCP 2.0 packages.

## Live probe

CI starts the exact package over stdio without an API key.

The probe performs:

```text
MCP initialize
-> tools/list
-> resolve-library-id
-> query-docs
```

The query deliberately targets the current Model Context Protocol documentation, because MCP APIs themselves are changing and directly affect KuuOS development bridges.

## No credential dependency

Context7 recommends an API key for higher rate limits and private repositories, but documents basic unauthenticated usage.

The compatibility probe therefore uses no credential and persists none.

A later private-repository use case may supply host-managed credentials, but that is not part of the compatibility receipt.

## Authority order

Context7 is not allowed to override KuuOS-local truth.

For exact KuuOS behavior:

```text
repository-local source / exact Git state
>
external Context7 documentation
```

For exact Lean behavior:

```text
pinned Lean + pinned Mathlib + actual Lean-LSP/CI result
>
generic external documentation
```

Context7 is valuable precisely for the parts that are external and change over time.

Examples:

- MCP SDK APIs;
- GitHub MCP changes;
- Vercel/Supabase/Neon SDKs;
- Playwright/Chrome automation APIs;
- Python/TypeScript dependency changes.

## Non-collapse

The same API may have:

- local KuuOS adapter assumptions;
- Context7 current documentation;
- upstream GitHub source;
- installed package behavior.

These can disagree.

v7.20 treats disagreement as a reason to inspect the versions and bindings, not to assume the latest external docs automatically win.

## Promotion

A successful final exact-head run promotes:

```text
context7:
  recommended_read_only
->
  verified_compatible
```

This means the pinned Context7 package demonstrated live interoperability with the KuuOS development environment.

It does not transfer source authority.
