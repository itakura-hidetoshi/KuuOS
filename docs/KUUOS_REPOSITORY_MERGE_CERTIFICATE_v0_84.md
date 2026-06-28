# KuuOS Repository Merge Certificate v0.84

v0.84 extends the linear certificate sequence to a two-parent merge revision.

A valid merge certificate requires:

- two valid preserved parent records
- one shared chain identity and root revision
- a nonempty common history prefix
- disjoint branch histories after the fork
- exact Git parent order
- exact parent record revision and snapshot bindings
- no overlapping changed paths
- no changed path outside the explicit inventory
- a score-zero normal-form merge tree

The merge observation reads committed objects and ignores the working tree.

Overlapping path changes are not resolved by v0.84. They are rejected for a later conflict-resolution certificate.

A branch whose current normal form is not preserved cannot enter a merge certificate.

The certificate binds both parent record digests, both parent revisions, the merge revision, the merge observation digest, and the merge normal-form certificate digest.

No repository write or external approval is used.
