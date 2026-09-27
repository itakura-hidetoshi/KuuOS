# KuuOS Local Repository MCP Compatibility v7.18

## Purpose

v7.17 verified the Lean-LSP MCP against the pinned KuuOS theorem environment.

v7.18 verifies the other two core local repository surfaces:

```text
Git MCP
Filesystem MCP
```

against the same KuuOS repository root.

The intended four-surface development model is:

```text
GitHub MCP     -> remote repository / PR / Actions truth
Git MCP        -> local worktree / local commit truth
Filesystem MCP -> local repository file surface
Lean-LSP MCP   -> Lean semantic state inside that repository
```

These are related presentations, not interchangeable authorities.

## Upstream pins

The reference repository is pinned for evidence to:

```text
modelcontextprotocol/servers
main SHA: f46d9578190b476b3501923ea8977d899e8db2cb
```

Packages:

```text
mcp-server-git == 0.6.2
  with upstream lock mcp == 1.29.0
@modelcontextprotocol/server-filesystem == 2026.8.31
```

The upstream repository explicitly describes these as reference implementations, not production guarantees. KuuOS therefore verifies interoperability but keeps its own authority and scoping rules.

## Exact-head alignment

The CI checkout is the pull request source head itself.

The probe requires:

```text
git rev-parse HEAD
=
GitHub pull_request.head.sha
```

and then asks Git MCP for:

```text
git_status
git_log(max_count=1)
```

The Git MCP result must refer to that same exact head.

Therefore:

```text
GitHub exact source head
=
local worktree HEAD
=
Git MCP HEAD
```

for the compatibility receipt.

## Filesystem scope

Filesystem MCP is launched with exactly one allowed directory:

```text
<KUUOS_REPOSITORY_ROOT>
```

The probe calls:

```text
list_allowed_directories
read_text_file(lean-toolchain)
search_files(lean-toolchain)
```

and verifies that the visible Lean toolchain is exactly:

```text
leanprover/lean4:v4.30.0-rc2
```

No parent directory, home directory, or machine-wide filesystem root is admitted.

## Write tools

Both reference servers expose write-capable operations.

v7.18 does not hide that capability and does not treat it as a fault.

Instead, this compatibility probe is explicitly read-only.

For Filesystem MCP it discovers write tools and checks their MCP annotations, but calls none of them.

For Git MCP it calls only status/log/show.

Thus:

```text
write-capable server
!= write authority
```

and also:

```text
write-capable server
!= automatic rejection
```

The later KuuOS workspace authority layer decides whether local mutations may be used.

## Why Git MCP and GitHub MCP are both needed

GitHub MCP knows the remote collaboration state:

- PRs;
- Issues;
- Actions;
- remote branches and commits;
- code/security/governance surfaces.

Git MCP knows the local working state:

- unstaged changes;
- staged changes;
- local HEAD;
- local history;
- local branch checkout.

A clean local checkout can correspond to a remote head, but the two surfaces are not identical in general.

v7.18 therefore records alignment rather than collapsing them.

## Why Filesystem MCP remains separate from Git MCP

Git sees version-control semantics.

Filesystem sees files whether or not Git considers them changed, tracked, staged, ignored, or generated.

That distinction matters for:

- generated receipts;
- temporary build artifacts;
- local configuration;
- source files before staging;
- Lean diagnostics before commit.

## Relation to Lean-LSP MCP

After v7.18 the preferred local development chain becomes:

```text
Filesystem MCP
  -> file/read/search surface

Git MCP
  -> local revision/diff surface

Lean-LSP MCP
  -> Lean semantic surface

GitHub MCP
  -> remote PR/CI/repository surface
```

All four can refer to one repository without pretending they are one provider.

## Promotion

A successful exact-head live probe permits:

```text
git_reference:
  recommended_sandboxed -> verified_compatible

filesystem_reference:
  recommended_sandboxed -> verified_compatible
```

This means only that the pinned server versions were shown to interoperate with the KuuOS repository.

It does not make the reference servers theorem authority or GitHub authority.


## Released Git MCP surface note

The current upstream source at `f46d9578...` contains a `git_show` implementation, while the live PyPI `mcp-server-git==0.6.2` tool listing observed by the first v7.18 probe did not expose it.

KuuOS therefore treats the released package's live `tools/list` as the compatibility authority for this probe and uses `git_log(max_count=1)` to bind the exact local HEAD. The discrepancy is preserved as provenance rather than filled by assumption.


## Published Filesystem MCP version note

The current upstream main `src/filesystem/package.json` reports `0.6.3`, but that exact version is not published on npm. The official npm package currently publishes `2026.8.31`.

KuuOS therefore uses the actually installable official release `@modelcontextprotocol/server-filesystem@2026.8.31` for the live compatibility probe and records the source/package-version discrepancy explicitly.
