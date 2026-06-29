# KuuOS Repository Reference Update Authorization v0.96

v0.96 constructs a bounded, single-use certificate for one exact local branch reference transition.

It starts from a valid v0.95 object materialization receipt and revalidates the complete upstream certificate chain.

It verifies that the exact candidate commit is present in the post-operation object database.

It does not change any Git reference.

A granted certificate binds the repository identity, Git-directory fingerprint, complete `refs/heads/...` name, expected old commit OID, proposed candidate commit OID, policy, observations, ancestry evidence, scope, nonce, and evaluation time.

Only a direct local branch is eligible.

`HEAD`, symbolic references, tags, remote-tracking references, notes, replace references, ambiguous names, zero OIDs, deletion, and force updates are rejected.

The expected old OID must equal both reference observations and the source parent preserved by v0.95.

The proposed new OID must equal the materialized candidate commit.

The ancestry certificate must prove a bounded fast-forward path from the exact old OID to the exact new OID using object-database-derived evidence.

The later execution layer must use compare-and-swap semantics and must independently confirm that the reference still has the expected old OID.

The authorization always records all mutation and execution effects as false.

Focused validation is provided by `tests/test_kuuos_repository_reference_update_authorization_v0_96.py`.

The cumulative runtime root and strict Lean aggregate root include this frontier.
