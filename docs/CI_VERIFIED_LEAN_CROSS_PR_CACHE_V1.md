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
