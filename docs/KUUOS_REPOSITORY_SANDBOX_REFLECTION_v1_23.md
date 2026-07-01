# KuuOS Repository Sandbox Reflection v1.23

v1.23 reflects the exact alternate index accepted by v1.22 into one dedicated sandbox working tree.

The sandbox directory is restricted to `.kuuos-worktree-v1_23-<operation>` directly below the repository root.

The standard repository working tree remains unchanged.

The request binds the v1.22 request and result, repository identity, Git-directory fingerprint, alternate-index filename, exact tree entries, expected tree object identifier, published commit identifier, executor, marker, and sandbox directory.

The only write command is `git --no-optional-locks -C <repository> checkout-index --all --force --prefix=<sandbox>/`.

The command receives the v1.22 alternate index through the controlled `GIT_INDEX_FILE` setting.

Inherited `GIT_*` variables are removed before the controlled setting is installed.

The tree-entry grammar inherited from v1.20 allows only regular files with modes `100644` and `100755` and single-component safe paths.

The postcondition recomputes each Git blob object identifier from the materialized bytes, verifies executable-mode classification, and rejects missing or extra entries.

The alternate index, standard index, repository-root working tree, object database, references, reflog, signing surface, and push surface must remain unchanged.

An existing exact sandbox is reused without running Git.

An existing mismatched sandbox is rejected and is not overwritten.

If checkout creates a partial sandbox and later validation fails, the ERROR result retains the completed sandbox write in its effect accounting.

The prior object-database, checkpoint-reference, and alternate-index effects remain separately recorded.

The next intended stage is checkpoint-only reflog recording in v1.24.
