# KuuOS Repository Certificate Sequence v0.82

v0.82 connects incremental repository validation results across successive revisions.

Each record binds:

- sequence identity
- parent revision identifier
- current revision identifier
- previous record digest
- previous and current snapshot digests
- declared and computed changed paths
- reused scopes
- rechecked scopes and certificate digests

The declared path set must exactly equal the snapshot difference.

A record with a changed parent identifier, changed sequence identity, stale snapshot, repeated revision identifier, or modified digest is rejected.

Unchanged scopes are reused. Contract-local changes are checked locally. Shared-root or contract-set changes use a full normal-form check.

A record that does not preserve score zero can be recorded, but it cannot be extended.

The sequence length is explicitly bounded.

No external approval is required.
