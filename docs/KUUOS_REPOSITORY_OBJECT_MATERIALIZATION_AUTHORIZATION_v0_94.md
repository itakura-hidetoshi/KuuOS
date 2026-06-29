# KuuOS Repository Object Materialization Authorization v0.94

v0.94 authorizes a bounded set of Git objects for later materialization from one valid v0.93 repository commit candidate certificate.

The layer is an authorization step only.

It does not write an object database, create the commit object, update an index, modify a working tree, sign an object, or mutate a reference.

## Candidate object reconstruction

The v0.93 certificate is fully revalidated against its v0.92 application receipt, final repository snapshot, parent-tree inventory, and commit-candidate policy.

v0.94 then reconstructs the exact payload of every candidate object:

```text
new text blobs
all generated subtrees
root tree
candidate commit
```

Blob payloads are taken from the exact UTF-8 text values bound by v0.92.

Tree payloads are reconstructed from the v0.93 entry modes, names, NUL separators, and raw child object identifiers.

The commit payload is reconstructed from the exact root tree, parent commit, author, committer, and canonical message.

Each reconstructed object binds:

```text
Git object kind
traditional Git SHA-1 object identifier
payload byte size
SHA-256 payload digest
one or more deterministic origins
```

Objects with the same object identifier are deduplicated only when kind, payload size, and payload digest are identical.

An object-identifier reuse with different content is rejected.

## Dependency order

The materialization plan uses a deterministic dependency order:

```text
blobs
subtrees from deepest to shallowest
root tree
commit
```

An already-present exact object receives no write order and is reused.

Missing objects receive consecutive write-order values.

This order is a plan value, not an executed write sequence.

## Target object database observation

Authorization requires a bounded observation receipt for the target Git object database.

The receipt binds:

```text
repository identity
Git-directory fingerprint
object format
source parent commit
exact queried object-identifier set
existing object metadata
observation time
```

The queried set must equal the candidate object identifiers together with the source parent commit identifier.

The source parent must already exist as a commit object.

The observation must come from the object database and must not consult the working tree.

For every candidate object already present, kind, size, and SHA-256 payload digest must match exactly.

Exact matches are reused.

A mismatch is treated as an object-identifier collision and causes rejection.

## Bounded single-use authorization

The authorization scope binds one candidate certificate, one target observation, one policy, one repository identity, one Git-directory fingerprint, one parent commit, one candidate commit identifier, and one nonce.

The policy bounds:

```text
allowed repository identities
authorized nonce authorities
authorization lifetime
observation age
nonce-status age
new object count
new payload bytes
allowed object kinds
```

The nonce-status receipt must be fresh, unused, not revoked, and bound to the exact authorization scope.

The authorization is therefore eligible for one later materialization attempt only.

A later execution layer must consume the nonce atomically with the object-database result.

## Effect boundary

A granted v0.94 certificate may state that bounded object-database write authority exists for the exact plan.

It does not state that any object has been written.

The certificate fixes the following boundary:

```text
object_database_write_performed = false
commit_object_written = false
index_write_performed = false
working_tree_write_performed = false
reference_mutation_authority_granted = false
reference_mutated = false
signing_performed = false
```

Writing the candidate commit object does not update a branch, tag, or `HEAD`.

Reference mutation remains a separate later authorization domain.

## Security meaning

The traditional Git SHA-1 identifier is retained because the modeled repository uses the SHA-1 Git object format.

Every candidate payload is also bound by SHA-256.

An existing SHA-1 identifier is reusable only when its independently observed payload metadata matches the reconstructed object exactly.

The certificate is not proof that a filesystem or Git implementation performed the observation correctly.

It proves that the supplied receipts and values satisfy the v0.94 authorization contract.
