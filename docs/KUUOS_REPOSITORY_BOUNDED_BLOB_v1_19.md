# KuuOS Repository Bounded Blob v1.19

v1.19 follows the merged v1.18 checkpoint-reference CAS layer.

It permits one bounded Git blob object to be materialized from an exactly bound byte payload.

The request binds the repository path, repository identity, Git-directory fingerprint, committed v1.18 result, executor identity, sandbox marker token, payload SHA-256 digest, payload size, and expected Git blob identifier.

The only mutating command shape is:

`git --no-optional-locks -C <repository> hash-object -w --stdin`

Before mutation, the runtime verifies the repository and executor allowlists, the dedicated sandbox marker, the committed v1.18 result, the payload bindings, the SHA-1 object format, and the candidate blob identifier.

The public facade and core route execution through the strict path.

The strict path accepts only the literal executable name `git`.

It removes Git environment variables that could redirect the Git directory, work tree, index, common directory, object directory, or alternate object directories.

A missing-object probe is normalized only when its diagnostic is recognized as an unavailable object.

Other probe failures remain errors.

After a new object is written, the runtime verifies object presence, type, size, and content digest.

An exact existing blob is reused without a second write.

If the write succeeds but a later postcondition fails, the result remains ERROR while preserving the recorded object-database mutation.

This layer does not permit reference, index, working-tree, reflog, signing, or push writes.

Focused disposable-repository tests verify new-object materialization, exact reuse, payload-mismatch rejection, non-target repository-state preservation, fail-closed probe normalization, marker rejection, executor rejection, literal-executable enforcement, and Git object-directory environment isolation.
