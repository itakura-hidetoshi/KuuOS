# KuuOS Lean CI — pinned cache topology and incremental compilation

**2026-10-20 / build infrastructure only.** This optimization changes no Lean theorem,
no 107 publicly retained roots, no pinned Lean/mathlib/Batteries dependency and
does not merge the independent F112 or Qi v3.3 lines.

## Observed bottleneck (PR #2371, original workflows)

- CodeAI independent workflows ran `lake update`, `lake exe cache get`,
  a strict subsystem Lean build, **and** a second strict `lake build KuuOSFormal`.
- Example: `CodeAI Bounded Autonomous Git Lifecycle Loop Orchestration`
  on the tested exact head downloaded 8297 mathlib cache files and ran the
  full root around 09:12:49–09:26:21 UTC, over 13 minutes.
- In contrast, PR Governance restored trusted `kuuos-lake-*` from main and
  its own PR-local build overlay, then validated the changed root incrementally.
- A successful original Qi v3.3 focused build restored the immutable
  `kuuos-current-lean-v2-*` archive; it could not update that primary key.

## New paths and responsibilities

1. **Trusted main cache owner:** `.github/workflows/lean-formal-validation.yml`
   remains the sole writer of the `kuuos-lake-*` snapshot containing `.lake`.
   On a cache hit with an actual package/build tree it invokes
   `scripts/build_lean4.sh --no-update --no-cache` to avoid unnecessary
   `lake update` and mathlib cache unpacking. Cold misses preserve the
   original update/cache/full compile path. Main also warms the newest DO frontier.
2. **CodeAI scoped check consumers (49 workflows):** each restores `.lake`
   from trusted main with `actions/cache/restore@v5`, then optionally restores
   a same-PR `.lake/build` overlay previously saved by Governance. No CodeAI
   workflow writes these caches. Pinned Lean setup is unchanged.
3. **Cold fallback:** only when the main cache is absent, update dependencies,
   verify the committed manifest and download the pinned Mathlib cache.
   Cached dependencies are still verified against the committed manifest.
4. **Scope-aware routing:** a small fail-closed path observer compares the exact PR
   Lean targets are preserved; the *redundant* full `KuuOSFormal` build is
   skipped in each of the 49 jobs. The existing PR Governance Strict Lean
   job remains the canonical integrated build and publishes exact-head receipts.
   `workflow_dispatch` continues to run full `KuuOSFormal` in each subsystem
   for explicit independent regression testing.

## Cache compatibility and safety

- Main key = `kuuos-lake-{runner.os}-{runner.arch}-{hash(lean-toolchain)}-{hash(lake-manifest)}-{main SHA}`.
  The restore-only consumers reuse exactly the same **path** (`.lake`),
  avoiding incompatible cache archive versions.
- PR build key = `kuuos-pr-build-{os}-{arch}-{toolchain}-{manifest}-pr{number}-{head SHA}`.
  PR build overlays are constrained to the same PR and are read-only in
  subsystem workflows. No PR cache may overwrite the trusted main namespace.
- Lake still compares source/dependency timestamps and manifests and rebuilds
  changed modules. **Cache reuse never constitutes proof verification.**
- `warningAsError`, `sorryAsError` and `#print axioms` policies are unchanged.
- A cache miss does not silently pass: dependencies are downloaded, checks
  remain strict, and a failed build fails the owning workflow.

## Regression

`python3 -m unittest -v tests.test_ci_lean_cache_topology`

The changed-source exact-head CI is required before merge. The measured
13-minute root build is an observed example, **not** a guaranteed speedup;
real latency depends on cache restore time, CI queueing, and changed imports.


## Why scope-aware routing matters

The main `.lake` GitHub Actions archive measured about **2714 MB compressed**
on an exact-head PR validation run. Loading that archive for 49 CodeAI jobs
triggered solely by `lakefile.toml` would unnecessarily transfer over 100 GB.
Each individual workflow still reports its Python/runtime checks; only its
unrelated Lean cache and subsystem target can be omitted. The globally
authoritative PR Governance lean job remains required.
