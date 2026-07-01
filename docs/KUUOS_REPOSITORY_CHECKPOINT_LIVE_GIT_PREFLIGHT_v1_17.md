# KuuOS Repository Checkpoint Live Git Preflight v1.17

v1.17 follows the merged v1.16 modeled atomic checkpoint CAS transition.

It is the first layer in this checkpoint chain that invokes live Git commands against a repository path.

The public facade accepts only a structurally valid and COMMITTED v1.16 transition whose repository, checkpoint reference, expected OID, proposed OID, and transition digest exactly match the preflight request.

The command set is fixed to seven read-only observations:

- resolve the repository root
- resolve the Git directory
- confirm that the repository is non-bare
- determine whether the checkpoint reference is symbolic
- read the exact checkpoint-reference OID
- confirm that the expected commit object exists
- confirm that the proposed commit object exists

Every command uses an argument array with `shell=False`, `--no-optional-locks`, `GIT_OPTIONAL_LOCKS=0`, a timeout, and bounded captured output. Arbitrary subcommands and arbitrary argument shapes are rejected.

READY requires a direct reference under `refs/kuuos/checkpoints/`, an observed OID equal to the authorized expected OID, and existing expected and proposed commit objects.

This layer deliberately enables `live_git_command_invoked=true` while keeping all mutation capabilities false. It performs no reference update, object write, index write, working-tree write, reflog write, signing operation, or push.

The focused integration tests run against a disposable temporary Git repository. They compare the byte digests of objects, refs, logs, and index before and after preflight to verify that the live command sequence performs no repository write.
