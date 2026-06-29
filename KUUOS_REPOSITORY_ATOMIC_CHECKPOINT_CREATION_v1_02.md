# KuuOS Repository Atomic Checkpoint Creation v1.02

v1.02 defines a pure deterministic state transition for one authorized local checkpoint-reference creation.

It consumes a valid v1.01 checkpoint authorization, an explicit checkpoint-reference state, and an explicit nonce registry.

It does not invoke Git and does not mutate a live repository.

External execution and post-execution observation remain later layers.

## Source states

The transition receives two immutable source values.

`RepositoryCheckpointState` represents one direct local checkpoint reference.

Its current OID may be the Git zero OID, which represents absence, or a nonzero OID, which represents an already existing reference.

`RepositoryCheckpointNonceRegistry` represents consumed and revoked checkpoint-authorization nonces at one explicit registry snapshot.

Both source values carry sequence numbers, observation times, and canonical digests.

## Complete v1.01 revalidation

The transition revalidates the complete v1.01 checkpoint authorization from all original inputs.

It binds:

- authorization certificate digest
- authorization scope digest
- repository identity
- Git-directory fingerprint
- checkpoint reference
- expected zero OID
- proposed final-tip OID
- authorization nonce
- finality transaction ID
- execution request
- authorized executor

A recomputed outer digest cannot conceal an invalid v1.01 certificate or mismatched v1.01 input chain.

## Atomic compare-and-swap

The only committable source checkpoint state is:

```text
current_oid = 0000000000000000000000000000000000000000
```

The request and v1.01 authorization must bind the same zero expected-old OID.

A nonzero source OID is a valid modeled source state, but compare-and-swap fails.

The transition then aborts without overwriting the existing checkpoint reference and without consuming the nonce.

## Atomic nonce consumption

A commit performs one logical state transition containing both changes:

1. the checkpoint reference moves from the zero OID to the exact v1.01 proposed OID;
2. the authorization nonce is added to the consumed-nonce set.

Both sequence numbers increase by exactly one.

The final nonce registry records the source registry digest as its upstream snapshot digest.

There is no state in which only one half of the transition commits.

## Abort preservation

Every abort returns the exact source checkpoint state and exact source nonce registry.

Abort causes include:

- checkpoint reference already exists
- authorization not granted
- authorization or request binding mismatch
- unauthorized executor
- stale checkpoint state
- symbolic or indirect checkpoint reference
- working-tree, reflog, or remote evidence source
- nonce authority mismatch
- nonce snapshot mismatch
- consumed or revoked nonce
- stale nonce registry
- expired authorization
- excessive execution duration
- future-dated evidence
- overwrite, delete, force, tag, or push request

No abort consumes a nonce.

## Modeled transition and live Git

A committed result may report:

```text
checkpoint_creation_transition_committed = true
checkpoint_created = true
checkpoint_state_mutated = true
nonce_consumed = true
```

These fields describe the explicit modeled state transition returned by the pure function.

They do not prove that a live Git reference changed.

The following always remain false:

```text
checkpoint_overwrite_performed
force_update_performed
reference_delete_performed
branch_updated
tag_updated
remote_reference_updated
push_performed
index_write_performed
working_tree_write_performed
object_database_write_performed
reflog_write_performed
signing_performed
live_git_command_invoked
live_repository_mutated
```

## Validation

Focused validation:

```bash
python3 -m unittest -v tests.test_kuuos_repository_atomic_checkpoint_creation_v1_02
```

Cumulative validation:

```bash
python3 runtime/kuuos_v102_check.py
```
