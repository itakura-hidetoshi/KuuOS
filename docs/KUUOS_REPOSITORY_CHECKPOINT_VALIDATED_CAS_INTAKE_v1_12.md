# KuuOS Repository Checkpoint Validated CAS Intake v1.12

v1.12 binds the v1.11 candidate-validation receipt to the v1.10 checkpoint CAS contract.

The intake verifies both artifact digests and requires exact agreement on the candidate digest, repository, checkpoint reference, expected current OID, and proposed checkpoint OID.

A ready intake means that the upstream candidate chain was revalidated and that the separately observed current OID still matches the expected OID recorded by the contract.

A conflict intake preserves the validated binding but records that the observed current OID changed. It does not request compare-and-swap.

A rejected intake indicates invalid evidence or a binding mismatch.

The intake grants no repository-change authority, performs no operation, invokes no live Git command, and does not update a reference.
