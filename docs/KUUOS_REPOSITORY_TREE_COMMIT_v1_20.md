# KuuOS Repository Tree and Commit Objects v1.20

v1.20 follows the merged v1.19 bounded-blob object-database layer.

It permits one exactly bound flat Git tree object and one exactly bound Git commit object to be constructed without updating any reference.

The tree is limited to a canonical, duplicate-free sequence of regular-file or executable-file entries.

Every entry binds a safe single-component path, an allowed mode, and an existing blob object identifier.

At least one entry must reference the exact blob accepted by the supplied v1.19 result.

The commit binds the tree identifier, one existing parent commit, author and committer identities, a UTC timestamp, and the normalized commit message bytes.

The runtime computes the expected SHA-1 tree and commit identifiers before invoking Git.

The only mutating command shapes are:

`git --no-optional-locks -C <repository> mktree`

`git --no-optional-locks -C <repository> hash-object -t commit -w --stdin`

The public facade and core route execution through the strict path.

The strict path accepts only the literal executable name `git` and removes every inherited `GIT_*` environment variable within the adapter scope.

Before either write, the runtime verifies the repository binding, executor allowlist, dedicated sandbox marker, accepted v1.19 result, SHA-1 object format, referenced blob types, parent commit type, canonical tree payload, canonical commit payload, and both expected object identifiers.

An exact existing tree or commit is reused without rewriting it.

After construction, the runtime verifies object presence, type, and exact raw object content.

If one object is written and a later command or postcondition fails, the ERROR result preserves the object-database effect that already occurred.

This layer does not permit reference, index, working-tree, reflog, signing, or push writes.

Focused disposable-repository tests verify new tree and commit construction, exact reuse, message-mismatch rejection, marker and executor rejection, literal-executable enforcement, Git environment isolation, non-target repository-state preservation, and postcondition effect accounting.
