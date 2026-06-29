# KuuOS Repository Local Frontier Checkpoint Authorization v1.01

v1.01 authorizes one bounded local checkpoint-reference creation attempt for the exact final tip confirmed by a valid committed v1.00 local frontier finality certificate.

It does not create the checkpoint reference.

Execution and receipt confirmation remain separate later layers.

## Checkpoint namespace

An authorized checkpoint reference must be a normalized ASCII direct reference below:

```text
refs/kuuos/checkpoints/
```

The suffix must be nonempty and must not contain ambiguous Git reference syntax.

The authorization rejects:

- `HEAD`
- local branch references under `refs/heads/`
- tags under `refs/tags/`
- remote-tracking references
- notes references
- replace references
- hidden components
- `.lock` suffixes
- repeated separators
- `..` and `@{` syntax
- non-ASCII names

This namespace separation prevents a checkpoint authorization from being interpreted as branch or tag authority.

## v1.00 binding

A granted authorization completely revalidates the supplied v1.00 certificate and binds:

- repository identity
- Git-directory fingerprint
- local frontier history digest
- exact final history sample
- exact final tip OID
- transaction ID
- bounded local finality status
- continuous candidate reachability
- monotone frontier history

The proposed checkpoint target OID must equal the v1.00 final tip exactly.

The final tip must remain present in the final sample's commit-object inventory.

## Compare-and-swap nonexistence

The checkpoint reference must be absent at both observation and immediate recheck.

Absence is represented by the Git zero OID:

```text
0000000000000000000000000000000000000000
```

The observation value, rechecked value, and scope expected-old OID must all equal the zero OID.

This is a compare-and-swap precondition for new-reference creation.

An existing checkpoint reference is never treated as an update target by v1.01.

A change between observation and recheck rejects the authorization.

## Evidence boundary

The checkpoint-reference value comes from the local reference store.

The authorization rejects working-tree, reflog, and remote-reference observations as evidence sources.

The authorization does not inspect or modify a remote repository.

## Single-use scope

The authorization scope binds:

- v1.00 finality certificate digest
- policy digest
- checkpoint observation digest
- repository identity
- Git-directory fingerprint
- exact checkpoint reference
- expected zero OID
- exact final tip OID
- transaction ID
- authorization nonce
- issue and expiry times
- requested operation flags

The strict validator requires the scope policy digest to equal the supplied policy digest before evaluating the authorization.

A fresh authority-issued nonce-status receipt must prove that the nonce is unused and not revoked.

The authorization is invalid after expiry or when its configured lifetime is exceeded.

## Authorized operation

Only a new checkpoint-reference creation attempt may be authorized.

The following requests are rejected:

```text
overwrite_requested
delete_requested
force_update_requested
tag_creation_requested
push_requested
```

## Separation of authorization and effect

A granted v1.01 certificate may set:

```text
checkpoint_creation_authorized = true
```

It does not assert that the reference was created.

The following remain false:

```text
checkpoint_overwrite_authorized
force_update_authorized
reference_delete_authorized
tag_creation_authorized
push_authorized
checkpoint_created
checkpoint_reference_mutated
branch_updated
tag_updated
remote_reference_updated
push_performed
index_write_performed
working_tree_write_performed
object_database_write_performed
reflog_write_performed
signing_performed
```

## Validation

Focused validation:

```bash
python3 -m unittest -v tests.test_kuuos_repository_local_frontier_checkpoint_authorization_v1_01
```

Cumulative validation:

```bash
python3 runtime/kuuos_v101_check.py
```
