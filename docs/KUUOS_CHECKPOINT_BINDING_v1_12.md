# KuuOS Checkpoint Binding v1.12

v1.12 combines the v1.10 contract record with the v1.11 validation receipt.

Both digests must be valid. The candidate digest, repository identifier, checkpoint reference, expected OID, and proposed OID must match exactly.

A ready result records consistent evidence. A conflict result preserves an observed-OID conflict. Invalid or mismatched evidence is rejected.

The result is descriptive only and performs no repository operation.
