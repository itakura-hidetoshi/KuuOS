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

## 2026-10-24 — C60 gauge / modular CI speed repair

### Observed bottleneck

The prior Gauge-field v0.60, OS-Associated Gauge Fields v0.61, and
Modular Evolution Mesh dedicated workflows separately executed
`lake update`, `lake exe cache get`, a strict subsystem Lean build,
and a *second* `lake build KuuOSFormal`. This occurred even when a
pull request changed only the canonical `formal/KuuOSFormal.lean`
import aggregate. Observed representative PR runs lasted roughly
67–78 minutes; by comparison the validated main Lean CI completed
its aggregate in roughly 3.5 minutes. These are observations,
not predictions or guarantees about all future runner/cache conditions.

### Repair and exact-head responsibilities

- The three dedicated workflows retain their existing check contexts,
  runtime/unit/manifest validation and strict subsystem Lake targets.
  They now run on the same Ubuntu 24.04 image as the main/governance
  cache publisher.
- A fail-closed source-path classifier reuses the tested
  `scripts/ci_subsystem_lean_scope.py` implementation (which reuses the
  unchanged CodeAI parser and diff helper) and excludes
  only paths whose Lean proof obligations belong to the central
  `pr-governance-gate.yml`: `formal/KuuOSFormal.lean`,
  `formal/KUOS.lean`, global Lake inputs, and the respective
  documentation file. A genuine subsystem change, workflow edit,
  missing diff, or classifier failure still runs the dedicated
  strict Lean check. The workflows continue running the runtime
  validation even on a Lean-scope skip.
- If subsystem Lean is required, the workflow restores only the
  trusted main/base `kuuos-lake-*` workspace, **read-only**,
  using the exact publisher key prefix, pinned toolchain hash,
  manifest hash and base SHA. Only a verified absence of Mathlib
  checkout or compiled `Mathlib.olean` triggers the corresponding
  `lake update` or `lake exe cache get`. Every run checks that
  `lake-manifest.json` and `lean-toolchain` remain unchanged.
- The automatic second aggregate build is delegated to the existing
  exact-head Governance Strict Lean job on PRs and the main-push
  `lean-formal-validation.yml` job. It is NOT dropped from the
  mathematics: a manually dispatched dedicated workflow still
  builds `KuuOSFormal` independently.
- No PR modifies or writes a trusted default-branch Lake archive.
  Cached oleans are never treated as proof; Lake rebuilds changed
  modules and the strict `warningAsError` / `sorryAsError`
  options remain on all executed Lean targets. No root/module,
  pinned dependency, historical no-go or theorem changes.

These steps preserve required-check names: we do not remove the
`pull_request` workflow trigger with a path filter, which can
otherwise leave a required check permanently pending. The
subsystem's source-scoped Lean *steps* are conditionally omitted,
with the required runtime check still completing.

Regression: `python3 -m unittest -v tests.test_ci_lean_cache_topology`.

Post-change times must be read from the new exact-head workflow runs;
the historical 67–78 minute durations are not a guaranteed ratio.


## 2026-10-25 — Qi v3.1–v3.3 and CapabilityOS v0.60 source routing

### Observed redundant work

On F112-P94D3AN PR #2543, modifying
`formal/KuuOSFormal.lean` solely to expose a newly proved F112 module
triggered four unrelated dedicated proof jobs in parallel with the canonical
exact-head Governance strict build: Qi v3.1, Qi v3.2, Qi v3.3 and CapabilityOS
v0.60. The dedicated Qi jobs used one frozen
`kuuos-current-lean-v2-...` archive keyed only by toolchain/manifest; those
checks could not publish a fresh verified main cache to the same immutable
key. The CapabilityOS workflow redundantly compiled
`lake build KuuOSFormal` even though Governance already owns that proof check.

### New route and cache authority

- Each of the four dedicated workflows now uses the existing
  `scripts/ci_subsystem_lean_scope.py` classifier with an exact-PR-base to
  checked-out-merge-HEAD diff. Failures, missing/unknown diffs, workflow
  changes and genuine subsystem module changes select the dedicated Lean
  path **fail closed**. Manual dispatch also retains its Lean checks.
- The canonical public `formal/KuuOSFormal.lean` import aggregate, pinned
  Lake inputs and the corresponding documentation changes are delegated to
  the exact-head Governance Lean check. **Static import/root preservation
  assertions are never skipped**; CapabilityOS runtime/unit/manifest checks
  continue for all triggering PRs.
- The selected dedicated Lean path restores the verified **main** `.lake`
  workspace with the same `kuuos-lake-{os}-{arch}-{toolchain}-{manifest}`
  namespace and archive **path** as the publisher
  (`.github/workflows/lean-formal-validation.yml`). On an actual cache
  miss, it runs `lake update` and/or `lake exe cache get` only for missing
  pinned dependencies. It rechecks manifest/toolchain integrity.
- Dedicated Qi and CapabilityOS workflows become **read-only** cache
  consumers; only main and Governance publish their respective main/PR
  artifacts. CapabilityOS no longer builds the full aggregate a second time
  on PRs or normal main pushes; explicit manual dispatch still does.
- Qi workflows now explicitly pass the repository's pinned strict
  `warningAsError` and `sorryAsError` options to the original two
  buildable `:olean` module targets, retaining the v3.2/v3.3 `sorryAx`
  log checks. No theorem, mathlib/Lean pin, C60 gauge data, public-root set
  or Gray policy is changed.

### Regression and expected effect

`python3 -m unittest -v tests.test_ci_lean_cache_topology` tests the
source-only/aggregate-only cases, unknown-diff fail-closed behavior,
workflow-edit revalidation, cache compatibility and preserved strict flags.
Four dedicated Lean downloads/compilations are avoided on an F112-only
import PR, while the central full library check remains required. Actual
elapsed time and restored-cache keys must be measured from subsequent
GitHub Actions runs; these are not assumed speedup percentages.

The current change deliberately does **not** weaken the expensive
`KuuOSFormal` build in PR Governance: it remains the authority-bearing
exact-HEAD strict Lean gate, with all 107 public proof roots retained.
