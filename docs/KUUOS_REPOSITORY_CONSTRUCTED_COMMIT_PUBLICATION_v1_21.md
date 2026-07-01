# KuuOS Repository Constructed Commit Publication v1.21

v1.21 follows the merged v1.20 limited tree and commit object-construction layer.

It publishes the exact commit object accepted by v1.20 to one checkpoint reference through the existing v1.17 read-only preflight and v1.18 atomic live reference compare-and-swap path.

The publication request binds the v1.20 result digest, v1.18 live-reference request digest, repository identity, Git-directory fingerprint, checkpoint reference, expected current object identifier, constructed commit identifier, executor identity, and request time.

The constructed commit identifier must equal both the verified v1.20 commit identifier and the v1.18 proposed checkpoint identifier.

The layer does not reimplement reference mutation.

It delegates the live operation to the existing v1.18 strict CAS implementation after every v1.21 binding and authorization check succeeds.

The delegated CAS recomputes the v1.17 preflight against the current repository state before mutation.

The strict path accepts only the literal executable name `git`.

It removes inherited `GIT_*` variables from both the delegated preflight and live-reference execution scopes.

A successful publication changes only the selected checkpoint reference.

The tree and commit objects may have been created by v1.20, but v1.21 performs no new object-database write.

The result therefore records prior object-database mutation separately from current publication effects.

Replay, stale current-reference state, commit-binding mismatch, unauthorized executor, repository mismatch, marker mismatch, and preflight mismatch fail closed.

If the delegated reference command succeeds but a later postcondition fails, the publication result remains ERROR while preserving the completed reference-write accounting.

This layer does not permit object-database, index, working-tree, reflog, force, delete, HEAD, branch, tag, remote-reference, signing, or push writes beyond the one selected checkpoint-reference CAS.
