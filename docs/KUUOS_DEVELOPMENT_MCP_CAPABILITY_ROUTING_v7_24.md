# KuuOS Development MCP Capability Routing v7.24

## Purpose

KuuOS now has many verified MCP surfaces.

That creates a new failure mode:

```text
more MCPs
-> call everything
-> duplicate evidence
-> larger context
-> confused authority
```

v7.24 solves this by routing each development task to the smallest set of MCP planes needed for the facts being asked.

## Central rule

```text
choose by fact plane
not by MCP popularity
not by maximum tool count
```

The same repository may legitimately require several MCPs because each sees a different conditioned surface.

## Authority planes

### Remote repository and CI

```text
GitHub MCP
```

Use for:

- canonical remote HEAD;
- PR state;
- Actions;
- Issues/reviews;
- code/security/governance state.

### Local revision and diff

```text
Git MCP
```

Use for local HEAD, staged/unstaged changes and local history.

### Working bytes

```text
Filesystem MCP
```

Use for the actual bytes currently being edited.

### Lean semantics

```text
Lean-LSP MCP
```

Use only when bound to the current Filesystem bytes.

### External library/API docs

```text
Context7
```

Use for current version-specific SDK/library documentation.

### MCP specification

```text
Official MCP Docs
```

This outranks Context7 and generic Fetch for current MCP specification claims.

### Generic external content

```text
Fetch MCP
```

Use as a generic public-content fallback, not as KuuOS repository authority.

### Browser functional behavior

```text
Playwright MCP
```

### Browser console/network/performance

```text
Chrome DevTools MCP
```

### Multi-MCP orchestration

```text
Docker MCP Gateway
```

Gateway routing does not transfer authority from downstream servers.

## The normal Lean CI repair route

For the user's recurring KuuOS workflow:

```text
CI RED
-> inspect entire Lean file
-> learn the Lean/API reason
-> repair
-> exact-head CI
```

v7.24 chooses:

```text
1. GitHub MCP
   remote exact-head CI failure

2. Filesystem MCP
   current source bytes

3. Lean-LSP MCP
   goals / diagnostics / hover / theorem search on those bytes

4. Git MCP
   local diff and revision review

5. Context7
   only when current external API/library documentation is actually needed

6. Official MCP Docs
   only when the issue concerns MCP protocol semantics
```

It does not activate browser, database, deployment or orchestration MCPs without a reason.

## Read/write non-collapse

A write-capable MCP is still useful for a read-only task.

Therefore:

```text
write-capable server
+
read task
-> read/inspection mode
```

If a write is requested but authority is absent:

```text
candidate
-> authority_required
```

not:

```text
candidate
-> rejected
```

This follows the same middle-way action principle used elsewhere in KuuOS.

## External documentation

External docs help explain current APIs but do not overwrite local truth.

```text
exact KuuOS behavior
-> repository/local/runtime evidence

current external API behavior
-> Context7 / official provider docs

current MCP specification
-> official MCP Docs
```

## Browser routing

Playwright and Chrome DevTools remain distinct.

```text
functional validation
-> Playwright primary

console/network/performance diagnosis
-> Chrome DevTools primary
```

The other browser MCP may be used as a corroborating plane when needed.

## Deployment and database routing

Provider-specific state stays provider-specific.

```text
Vercel deployment
-> Vercel connector

Supabase database
-> Supabase connector

Neon database
-> Neon connector
```

The router does not infer that two database providers are interchangeable.

## Validation

Focused tests verify:

1. Lean CI repair selects GitHub + Filesystem + Lean-LSP + Git, and no unrelated MCPs;
2. external docs add Context7 only when requested;
3. MCP spec research gives official MCP Docs primary authority;
4. browser functional and diagnostic routes remain distinct;
5. write requests without authority become partial `authority_required`, not rejection;
6. an unavailable required server blocks only the requested task route;
7. provider-specific database and deployment routing does not broaden to unrelated providers;
8. maximal profile is never selected by default.

The central law is:

> **Use the minimum set of MCP presentations needed to answer the actual development question, and preserve which source is authoritative for each fact.**
