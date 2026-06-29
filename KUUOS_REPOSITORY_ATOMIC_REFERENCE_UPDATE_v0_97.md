# KuuOS Repository Atomic Reference Update v0.97

v0.97 defines the deterministic execution transition immediately after a valid v0.96 reference update authorization.

The transition operates on an explicit repository reference state and an explicit single-use nonce registry.

It does not invoke Git, mutate a live repository, update a remote reference, or push.

A later receipt layer may compare an external bounded executor with this transition.

## Commit condition

A transition commits only when all of the following remain exact at execution time:

- the complete v0.96 authorization chain revalidates
- the authorization is granted and unexpired
- the repository identity and Git-directory fingerprint match
- the complete direct local branch reference matches
- the request binds the authorization certificate, scope, nonce, old OID, and new OID
- the executor is allowlisted
- the reference state comes from the reference store and not the working tree
- the current reference OID equals the expected old OID
- the nonce registry is fresh, authority-bound, snapshot-bound, unused, and not revoked
- force, delete, and push requests are absent
- execution duration and evidence times remain within policy

The committed transition updates the modeled reference state from the exact old OID to the exact candidate commit OID and consumes the exact nonce in the same transaction.

## Abort condition

Any failed condition aborts the transition.

A compare-and-swap mismatch may be attempted, but it cannot consume the nonce.

Every aborted transition preserves both the source reference state and the source nonce registry exactly.

No partial transition is represented.

## Authority boundary

A committed v0.97 result is an abstract repository-state transition.

It is not evidence that a Git command ran or that a live branch changed.

The following remain false:

```text
force_update_performed
reference_delete_performed
head_updated
tag_updated
remote_reference_updated
push_performed
index_write_performed
working_tree_write_performed
object_database_write_performed
signing_performed
live_git_command_invoked
live_repository_mutated
```

Authorization, modeled execution, external execution, and receipt remain separate layers.

## Validation

Focused validation:

```bash
python3 -m unittest -v tests.test_kuuos_repository_atomic_reference_update_v0_97
```

Cumulative validation:

```bash
python3 runtime/kuuos_v097_validation.py
```
