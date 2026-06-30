# KuuOS Repository Checkpoint CAS Coherence Receipt v1.13

v1.13 follows the merged v1.12 validated checkpoint CAS intake.

It does not repeat the external repository observation and does not reconstruct the v1.10 policy input. Instead, it independently checks the local coherence of the v1.10 contract, the local coherence of the v1.12 intake, and the exact binding between both artifacts.

The contract check covers its digest, candidate and policy evidence bindings, status and reason pairing, compare-and-swap requirement, observed-versus-expected OID relation, checkpoint-only boundary, forbidden-operation flags, and recorded checks.

The intake check covers its digest, evidence bindings, validated-input claims, status and reason pairing, compare-and-swap requirement, forbidden-operation flags, and recorded checks.

The cross-artifact check requires exact equality of the contract digest, candidate digest, repository, Git-directory fingerprint, checkpoint reference, expected OID, observed OID, proposed OID, status meaning, and compare-and-swap requirement.

A coherent ready receipt preserves that compare-and-swap is required. A coherent conflict receipt preserves that compare-and-swap is not required. Any invalid, incoherent, or mismatched evidence is rejected.

The receipt grants no repository-change authority, performs no operation, invokes no live Git command, and does not update a reference.
