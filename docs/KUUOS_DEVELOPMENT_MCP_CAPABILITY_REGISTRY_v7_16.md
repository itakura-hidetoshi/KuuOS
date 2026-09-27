# KuuOS Repository-Development MCP Capability Registry v7.16

## Purpose

KuuOS already had a verified GitHub MCP bridge, write canaries, workflow dispatch, live CI observation, and an observability MCP multiplexer for GitHub/Vercel/Supabase/Neon.

v7.16 expands the repository-development surface instead of creating another GitHub-specific bridge.

The architecture is:

```text
KuuOS development task
        |
        v
development MCP capability registry
        |
        +-- remote repository state      -> GitHub MCP
        +-- local worktree state         -> Git MCP
        +-- local files                  -> Filesystem MCP
        +-- Lean semantic state          -> Lean-LSP MCP
        +-- current library docs         -> Context7
        +-- functional browser testing   -> Playwright MCP
        +-- browser debugging/perf       -> Chrome DevTools MCP
        +-- MCP isolation/orchestration  -> Docker MCP Gateway
        +-- deployed error diagnosis     -> Sentry MCP
        +-- generic document retrieval   -> MCP Fetch
        +-- MCP protocol docs            -> official MCP docs server
        +-- cloud deployment/data        -> existing Vercel/Supabase/Neon
```

The registry does not auto-start servers and does not create write authority.

## Why this is useful for the current KuuOS repository

The current development pattern repeatedly needs:

1. exact GitHub branch/PR/CI state;
2. local Git diffs and repository history;
3. file-level search and edits;
4. Lean diagnostics and theorem search;
5. current external API documentation;
6. browser verification for runtime/web surfaces;
7. deployment and database observations.

Previously these capabilities were split between GitHub-specific bridges and provider-specific tools.

v7.16 gives them one host-neutral capability map.

## GitHub MCP: widen the existing integration

KuuOS already has real GitHub MCP write and re-observation paths.

Therefore v7.16 does not replace them.

It registers the official GitHub MCP Server and recommends the development toolsets:

```text
context
repos
git
issues
labels
pull_requests
actions
code_quality
code_security
dependabot
secret_protection
security_advisories
notifications
discussions
governance
```

The important rule is:

```text
registry support
!=
GitHub write authority
```

All GitHub mutations continue through the existing exact-head / authority / receipt discipline.

## Lean-LSP MCP: highest-value new capability

KuuOS is Lean-heavy, so the largest practical gain is a Lean-aware MCP.

The selected candidate is:

```text
oOo0oOo/lean-lsp-mcp
```

It provides agent-facing access to:

- Lean diagnostics;
- current goals;
- hover and symbol information;
- local Lean source search;
- proof verification;
- LeanSearch;
- Loogle;
- Lean Finder;
- Lean Hammer premise search.

This can move error discovery earlier than GitHub CI.

However, KuuOS pins:

```text
Lean v4.30.0-rc2
mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6
```

v7.17 has now demonstrated exact compatibility with that pinned environment. The registry therefore marks Lean-LSP MCP:

```text
verified_compatible
```

The compatibility evidence is a live MCP handshake plus `lean_file_outline` and `lean_diagnostic_messages` on an existing KuuOS Lean file under the pinned Lean/mathlib pair. Explicit project opt-in remains required.

The server should use the KuuOS repository root as `LEAN_PROJECT_PATH` so `lake serve` uses the project toolchain rather than a global Lean installation.

## Git MCP

The MCP reference Git server complements GitHub MCP. v7.18 has live-verified `mcp-server-git 0.6.2` against the exact KuuOS source head, with the upstream-locked `mcp==1.29.0`; its registry status is now `verified_compatible`.

Use GitHub MCP for:

```text
remote repository truth
PRs
issues
GitHub Actions
GitHub security/governance
```

Use Git MCP for:

```text
local worktree status
unstaged/staged diffs
local history
local repository manipulation
```

These are different presentations and neither replaces the other.

## Filesystem MCP

The MCP reference filesystem server gives project-local file access. v7.18 has live-verified the published `@modelcontextprotocol/server-filesystem@2026.8.31` release against the exact KuuOS repository root; its registry status is now `verified_compatible`.

For KuuOS it must be rooted explicitly at:

```text
<KUUOS_REPOSITORY_ROOT>
```

Do not configure a home-directory or filesystem-wide root.

This makes local file search/edit capabilities available without turning Filesystem MCP into a machine-wide authority.

## Context7

Context7 supplies current library/framework/API documentation. v7.20 has live-verified `@upstash/context7-mcp 4.1.1` through `resolve-library-id` and `query-docs` without an API key, so its registry status is now `verified_compatible`.

It is useful when KuuOS development depends on changing external interfaces, especially:

- Python libraries;
- GitHub/MCP SDK changes;
- Vercel/Supabase/Neon SDKs;
- browser automation APIs.

Repository-local code and pinned toolchain files still outrank fetched documentation for exact KuuOS behavior.

## Playwright MCP

Playwright MCP is registered for deterministic functional browser verification. v7.21 has live-verified `@playwright/mcp 0.0.82` against a deterministic localhost fixture, so its registry status is now `verified_compatible`.

Recommended KuuOS mode:

```text
--isolated
--headless
```

Use it for:

- navigation;
- accessibility-tree inspection;
- forms;
- end-to-end browser flows;
- functional verification.

## Chrome DevTools MCP

Chrome DevTools MCP overlaps with Playwright but has a different role. v7.21 has live-verified `chrome-devtools-mcp 1.10.1` against the same localhost fixture, including snapshot and console diagnostics, so its registry status is now `verified_compatible`.

Use it mainly for:

- console inspection;
- network-request debugging;
- Chrome performance traces;
- live-browser diagnosis.

Thus:

```text
Playwright     -> functional behavior
Chrome DevTools -> diagnosis/performance
```

rather than treating one as the canonical browser server.

## Docker MCP Gateway

As the number of local MCP servers grows, directly launching each server from every host becomes brittle.

Docker MCP Gateway is therefore registered as the preferred orchestration/isolation surface when multiple local servers are enabled. v7.22 has live-verified the exact upstream plugin through a real profile, network-disabled containerized MCP server, Gateway tool discovery, and forwarded tool call; its registry status is now `verified_compatible`.

Its role is:

- MCP server lifecycle;
- container isolation;
- credential routing;
- server profiles;
- centralized routing.

It does not grant the capabilities of the downstream servers by itself.

## Sentry MCP

Sentry MCP is registered but not made a hard dependency.

Status:

```text
optional_when_instrumented
```

Once a deployed KuuOS service is actually instrumented with Sentry, it becomes useful for:

- error triage;
- issue analysis;
- traces;
- performance debugging.

Until then, its absence is local unavailability, not a KuuOS failure.

## Reference Fetch and MCP docs servers

The official MCP reference Fetch server is useful for agents without native web retrieval. v7.23 has live-verified the published `mcp-server-fetch 2026.8.18` release with the upstream-locked `mcp==1.29.0`, while preserving the current source-tree metadata version `0.6.3` as a distinct upstream presentation.

The official MCP documentation server at `https://modelcontextprotocol.io/mcp` is useful while maintaining the KuuOS MCP bridge itself. v7.23 has live-verified the current `2026-07-28` stateless HTTP surface and its `search_model_context_protocol` tool.

Both registry entries are now `verified_compatible`. The official docs plane may be authoritative for current MCP specification content, but neither surface is KuuOS repository or theorem authority.

## Existing cloud connectors

The registry reuses rather than duplicates:

```text
Vercel
Supabase
Neon
```

already present in the v7.1 observability layer and host connector environment.

Datadog remains intentionally absent from the required profile because its runtime connection/region compatibility is not reliable in this environment.

## Profiles

### Core repository development

```text
GitHub
Git
Filesystem
Lean-LSP
Context7
```

This should be the normal KuuOS formalization profile.

### CI and release debugging

Adds:

```text
Vercel
Supabase
Neon
Sentry when configured
```

### Browser validation

```text
Playwright
Chrome DevTools
Context7
```

### Maximal repository development

Combines all registered development servers.

This profile is a capability inventory, not an instruction to auto-start every server.

## Runtime activation states

The v7.16 planner maps each selected server into:

```text
ready
experimental_ready
authority_required
environment_missing
optional_unconfigured
```

This lets KuuOS degrade locally instead of collapsing the whole development environment because one MCP server is missing.

## Write capability

Mixed read/write MCPs are not rejected merely for being powerful.

Instead:

```text
write requested
+
independent authority present
-> write_candidate

write requested
+
authority missing
-> authority_required
```

This follows the same design developed in v7.12 action lifting: capability does not equal authority, but capability is not treated as a fault.

## Selection policy

The registry prefers:

```text
GitHub official  -> remote repository state
Git reference    -> local worktree state
Lean-LSP         -> Lean semantic state
Context7         -> current external docs
Playwright       -> functional browser verification
Chrome DevTools  -> console/network/performance diagnosis
Docker Gateway   -> multi-MCP local orchestration
```

Provider overlap is allowed.

It is another presentation choice, not automatic semantic identity.

## Validation

The focused checker verifies:

1. at least 14 repository-development MCP surfaces are registered;
2. the maximal profile contains all high-value servers;
3. core development resolves GitHub/Git/Filesystem/Context7 and exposes Lean-LSP as experimental-ready;
4. write requests route to independent authorities instead of becoming blanket rejection;
5. one optional provider can be absent without disabling the others;
6. GitHub toolsets cover current KuuOS repository development;
7. Lean-LSP carries exact v7.17 pinned-toolchain compatibility evidence;
8. browser MCPs remain isolated and role-separated;
9. plaintext credential material is rejected from the registry;
10. an unknown profile produces no activation plan.

## Next

The most useful next step is not adding another long list of MCP names.

It is an **exact compatibility probe** for the high-value new servers:

```text
Lean-LSP MCP
Git MCP
Filesystem MCP
Context7
Playwright
Chrome DevTools
Docker MCP Gateway
```

against the current KuuOS environment, with Lean-LSP compatibility against the pinned Lean/mathlib pair checked first.
