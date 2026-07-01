# KuuOS Repository Alternate Index v1.22

v1.22 resumes the staged repository-write roadmap after the interposed v1.21 constructed-commit publication layer.

It loads the exact tree accepted by v1.20 into one dedicated alternate Git index after the exact commit has been published by v1.21.

The alternate index is stored as `.git/kuuos-index-v1_22-<operation>.index`.

The standard `.git/index` is never selected and must remain byte-for-byte unchanged.

The request binds the v1.20 request and result, the v1.21 publication result, repository identity, Git-directory fingerprint, exact tree entries, expected tree object identifier, published commit identifier, executor, marker, and dedicated filename.

The only write command is `git --no-optional-locks -C <repository> read-tree <tree-oid>` with the controlled alternate-index path.

The verification command is `git --no-optional-locks -C <repository> ls-files --stage -z` against the same path.

Inherited `GIT_*` values are removed before the controlled index setting is installed.

An existing exact alternate index is reused without rewriting it.

An existing mismatched index is rejected and is not overwritten.

If creation succeeds but later verification fails, the ERROR result retains the completed alternate-index write in its effect accounting.

This layer performs no current object-database, reference, standard-index, working-tree, reflog, signing, or push write.

The prior v1.20 object-database effect and prior v1.21 checkpoint-reference effect remain separately recorded.

Because v1.21 was used for the publication integration layer, sandbox working-tree reflection moves to v1.23 and checkpoint-only reflog recording moves to v1.24.
