# KuuOS Repository External Approval v0.90

v0.90 binds a v0.89 admission proposal to externally supplied approval evidence.

The runtime does not implement or claim cryptographic signature verification. It validates an external signature-verification receipt and binds that receipt to the exact signed payload, signature digest, signing key, algorithm, approver, admission certificate, and approval policy.

The approval policy fixes the authorized approvers, approver-to-key bindings, authorized signature verifiers, authorized revocation-status authorities, allowed signature algorithms, evidence-age limits, approval lifetime limit, and role-separation requirement.

A valid approval requires an admission certificate with `REPOSITORY_EVOLUTION_ADMISSION_PROPOSED`. Rejected or stable admissions cannot be approved through this layer.

The signed approval attestation binds the admission certificate digest, approval policy digest, approver identity, approval decision, issuance time, expiry time, signature algorithm, signing key, signed-payload digest, and signature digest.

The external signature-verification receipt must reproduce all signature metadata exactly and must report successful verification.

The revocation-status receipt binds the approval attestation and policy to an authorized registry authority and registry snapshot. A revoked approval is rejected.

Operational failures such as an explicit reject decision, unauthorized roles, unapproved signing key, unsupported signature algorithm, failed signature verification, stale evidence, excessive approval lifetime, expiration, or revocation produce `REPOSITORY_EVOLUTION_EXTERNAL_APPROVAL_REJECTED`.

Digest corruption and mismatched admission, policy, attestation, signature metadata, or revocation targets fail closed.

A successful assessment produces `REPOSITORY_EVOLUTION_EXTERNAL_APPROVAL_ACCEPTED` and marks the evidence as eligible for a later application-authorization stage.

Acceptance does not apply a patch, create a commit, or mutate a reference. Those authority fields remain false.
