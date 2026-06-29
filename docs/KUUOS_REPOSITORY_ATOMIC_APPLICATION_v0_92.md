# KuuOS Repository Atomic Application v0.92

v0.92 consumes one valid v0.91 application authorization in a pure, isolated repository-snapshot transaction.

The transaction revalidates the authorization certificate, exact application scope, source commit, source snapshot, object-database observation, patch bundle, expected changed paths, executor policy, authorization lifetime, and nonce-registry entry.

The patch bundle is applied only to an in-memory `RepositorySnapshot`. The runtime does not write the working tree, index, object database, branch, tag, or remote reference.

The candidate result must change exactly the authorized paths and must already be a repository alignment normal form. Its observation must bind to the candidate snapshot exactly.

The transaction also constructs inverse patches and verifies that they restore the exact authorized source snapshot. The rollback material is retained as a receipt artifact; rollback is not executed on the live repository.

One nonce-registry entry must bind the exact authorization nonce and application-scope digest. The nonce must be unused and unrevoked before the transaction.

Success commits two pure output values together:

```text
candidate repository snapshot
+
nonce registry with the exact nonce marked used
```

Failure returns both original input values unchanged:

```text
source repository snapshot
+
original nonce registry
```

This excludes partial states in which the patch result exists without nonce use, or the nonce is used without the patch result.

Operational failures produce `REPOSITORY_ATOMIC_APPLICATION_ABORTED`. These include source drift, expired authorization, unauthorized executor, excessive duration, patch before-digest mismatch, path mismatch, used or revoked nonce, non-object-database source, working-tree dependence, and a candidate result that is not a normal form.

Digest corruption in the authorization, scope, source revision, patch bundle, policy, nonce registry, receipt, or rollback material fails closed.

A successful result is `REPOSITORY_ATOMIC_APPLICATION_APPLIED`.

Even on success:

```text
isolated_snapshot_only = true
live_repository_write_performed = false
commit_created = false
reference_mutated = false
```

Git commit construction and reference mutation remain separate later stages with fresh authority requirements.
