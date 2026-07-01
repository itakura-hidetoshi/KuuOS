# KuuOS Repository Checkpoint Live Reference CAS v1.18

v1.18 follows the merged v1.17 live Git read-only preflight.

It is the first checkpoint layer permitted to mutate a live repository. The permitted mutation is exactly one atomic compare-and-swap update of one direct reference under `refs/kuuos/checkpoints/`.

The only mutating command shape is:

`git --no-optional-locks -C <repository> -c core.logAllRefUpdates=false update-ref --no-deref <checkpoint-reference> <proposed-oid> <expected-oid>`

The repository path must be explicitly allowlisted by digest. The executor must be allowlisted. A regular non-symbolic sandbox marker file named `kuuos-live-mutation-sandbox-v1_18` must exist directly in the repository Git directory and contain the exact request marker token.

The supplied v1.17 READY receipt is not accepted by digest alone. Immediately before mutation, v1.18 reruns the complete v1.17 live preflight and requires the recomputed receipt to equal the supplied receipt exactly. Any reference or object-state change after the supplied preflight therefore prevents mutation.

The target reference must be direct, the observed OID must equal the authorized expected OID, the proposed commit object must exist, and no target reflog may exist before execution.

A successful update is followed by a fixed read-only `show-ref --verify --hash` command. COMMITTED requires the observed final OID to equal the proposed OID and the target reflog to remain absent.

This stage does not permit force update, deletion, HEAD update, branch update, tag update, remote-reference update, push, signing, object-database write, index write, working-tree write, or reflog write.

Focused tests use disposable Git repositories. They verify a successful single-reference CAS, sandbox-marker rejection, executor rejection, TOCTOU rejection after a supplied preflight, and replay rejection. The successful test confirms that objects, index, working tree, and logs remain byte-identical.
