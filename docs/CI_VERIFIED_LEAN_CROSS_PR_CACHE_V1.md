# Certified canonical Lean project cache v1

## Observed obstruction

PR #3641 (45505108586 attempt 3) completed the 10433-job full strict
build. PR #3642 (45561799577 attempt 1) missed all cache routes and
timed out at 9823/10433 despite unchanged proof trees and pins.
PR merge-ref caches are not visible to sibling PRs. The existing
path-filtered main publisher does not run on nonformal merges.

## Trust boundary and routing

A separate main-only producer runs on main pushes and manual main
dispatch, checks exact proof scope for an existing unexpired artifact,
and builds only on a miss or before expiry. It runs the original full
strict KuuOSFormal command. A main-only incomplete checkpoint is never
a certified publication. Only strict success permits artifact upload.
The original main workspace namespace remains unchanged.

The key binds formal and lean Git trees, Lake inputs, fixed bootstrap,
build wrapper, producer/verifier source, Ubuntu 24.04/Linux/X64 and
strict command. V1 deliberately supports only the audited current
Lakefile, manifest and toolchain. Scope changes fall back rather than
broaden admission. Unchanged nonformal commits keep the key.

The PR consumer is read-only. It validates exact current checkout and
actual base scope, producer ancestry, repository and main branch,
workflow identity/path, successful run/attempt/job/strict/pack/publish
steps, artifact identity/expiry, live GitHub SHA256 and size. It
validates the internal manifest, compressed project archive and strict
log. ZIP contents are constrained; tar links, traversal, duplicate
entries and excessive sizes are rejected. Extraction is staged before
replacing the current project overlay. Only .lake/build is transported,
not packages or credentials. Same-PR checkpoints have priority.
Any unavailable, mismatched or damaged artifact is a miss, never a
positive proof receipt. The exact-head Strict Lean job and flags
remain unchanged. No proof, execution or merge authority is added.

Changed proof trees use the existing route; this is deliberately
conservative exact-scope reuse, not a general incremental-equivalence
claim. The producer assumes trusted reviewed canonical main and
GitHub's artifact service; it does not defend against compromise of
main, the account, runner or compiler. Branch protection remains
necessary. Historical artifacts expire; renewal still runs strict Lean.

## Verification and deployment

The isolated research workflow tests negative origin/scope/transport
cases and a real pinned Lean fixture .olean transferred between two
runners and imported with strict options. The isolated fixture uses
a real minimal Lake build log and independently rejects sorry. The
standalone weak sorryAsError option is necessary without Mathlib;
warningAsError still rejects sorry. The fixture is not a canonical
proof or a production publication. The independent runner tests live
REST artifact digest/size and exact Git scope, and observes Lake reuse. Only an actual main publisher success
and sibling PR restore followed by exact-head Strict Lean can establish
operational reuse and speed. Old PR-only caches cannot be retroactively
declared canonical. PR #3642 retains its own exact-head cache and
continues independently. No Lean source, assumption, root or pin
changes.

## 2026-11-26 — production publication and independent replay

PR #3643 merged at `85be208ec9f0e1f7c6bfa0b4cfe670653af54057` after full strict
10433/10433 and 168/168 exact-head checks, with matching source/test-merge/
merged tree `e0d6c0ca1b5f7d7e118f0e592347b0b5049d4cf3`. Formal and lean subtrees and all three Lake
inputs remain unchanged.

The canonical main publisher completed [run 45615980980](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/45615980980),
job 139211364001, attempt 1. Its full strict KuuOSFormal build completed
10433 jobs, then packed and published artifact 15038487740, 940848666 bytes,
SHA256 `faf2246b58340ec358b630c151f50c6988c30209d30e1e2c4ddafdabe4a57f2b`,
scope digest
`2d9d0c313b6f7d8e4df0900fd0977324999a4200c1ed3c1adb178706370dbd6b`.
Main sharded Governance 45615980981 and Runtime 45615980983 also succeeded.

An isolated fresh runner with no project cache, on distinct research
HEAD `7a365bd8ea6b46636b97f945867b96c9e7d2fe63`,
completed [run 45700676928](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/45700676928),
job 139509634163. It retrieved the exact production artifact through the
actual canonical admission and SHA256/size validation path. It ran the
unchanged strict KuuOSFormal command, which completed all 10433 jobs in
4.74 seconds (command wall time, excluding transfer/dependency setup).
All 2120 project .olean files retained size and mtime, with zero missing.
Both selected files retained identical SHA256 as well:

- FourteenCellNonabelianPasting.olean:
  `66bd1a49897a92fdff6cb0659e3d5c941607a9da316bb50e61ec2f2a832617fe`
- KuuOSFormal.olean:
  `c9a0808e323e38ae115fb29b962dfd97292ea5cdb1eecbf89baa0f58debc9ccf`

Independent evidence artifact 15062677546 has SHA256
`f8bcbabdbcad92066df3701472e70d2e812bd16c62637bc073d6a7ac195ea33c`.
Known auxiliary SymbolFrequency panic log entries persist; the strict
build succeeded, not a compiler-internal repair. This is actual
production artifact reuse across runners with identical proof scope,
not full re-elaboration, proof of arbitrary changed-source reuse, or
a claim that all 2120 individual hashes were compared after build.
A fresh standard PR Governance route remains to be observed separately.

The existing cache routing regression is extended to execute the
canonical artifact tests, including selection past a newer inadmissible
candidate, truncated discovery rejection and preservation of an existing
overlay when a replacement archive is invalid. No publisher/verifier
bytes, proof inputs, pin, strict target or existing tests are removed.
PR #3642 was closed unmerged on 2026-11-25; its synchronized research
branch is preserved separately, without reopening it.
