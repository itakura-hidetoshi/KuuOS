# KuuOS Repository Bounded Tree Commit v1.20

v1.20 follows the merged v1.19 bounded blob layer.

It permits exact Git tree objects and one exact Git commit object to be materialized from an already certified v0.93 commit candidate.

The candidate is revalidated against its atomic-application receipt, final snapshot, parent-tree inventory, and candidate policy.

Every changed blob candidate must be covered by a valid v1.19 materialization result bound to the same repository.

Every retained leaf object and gitlink is observed in the object database before tree construction.

The parent commit must exist and have Git object type `commit`.

Tree payloads are reconstructed from the certified entry names, modes, and object identifiers.

The runtime writes child trees before parent trees and writes the commit object only after the complete tree set has been verified.

The permitted mutating command shapes are:

`git --no-optional-locks -C <repository> hash-object -t tree -w --stdin`

`git --no-optional-locks -C <repository> hash-object -t commit -w --stdin`

The literal executable name `git` is required.

All inherited `GIT_*` environment variables are removed from the subprocess environment.

Existing tree or commit objects are reused only after exact type, size, and content verification.

If a write succeeds and a later postcondition fails, the ERROR result retains the completed object-database write count.

This layer does not update references.

It does not write the index, working tree, reflog, signatures, or remotes.

Focused disposable-repository tests cover new tree and commit materialization, exact reuse, unauthorized-executor rejection, v1.19 coverage rejection, executable restriction, Git object-directory isolation, and non-target repository-state preservation.
