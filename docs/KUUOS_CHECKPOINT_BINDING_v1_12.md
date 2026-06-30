# KuuOS Checkpoint Evidence Envelope v1.12

v1.12 combines the v1.10 contract record with the v1.11 validation receipt.

Both input digests must be valid. The candidate digest, repository identifier, checkpoint reference, expected OID, and proposed OID must match exactly.

The contract digest alone is not treated as sufficient. The envelope also checks the local consistency of the v1.10 status, reason, compare-and-swap requirement, observed OID relation, boundary flags, and recorded checks.

This local validation does not repeat the external repository observation or reconstruct the v1.10 policy input. It verifies only the information carried by the contract and the exact binding to the independently replayed v1.11 receipt.

A ready result records consistent evidence. A conflict result preserves a locally coherent observed-OID conflict. Invalid, incoherent, or mismatched evidence is rejected.

The result is descriptive only and performs no repository operation, invokes no Git command, mutates no reference, and grants no update authority.
