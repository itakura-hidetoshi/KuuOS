import KUOS.WORLD.KuuOSRepositoryEvolutionAdmissionV0_89

namespace KUOS.WORLD.KuuOSRepositoryExternalApprovalV0_90

open KUOS.WORLD.KuuOSRepositoryEvolutionAdmissionV0_89


structure ApprovalTimeline where
  admissionEvaluatedAt : Nat
  approvalIssuedAt : Nat
  signatureVerifiedAt : Nat
  revocationCheckedAt : Nat
  evaluatedAt : Nat
  approvalExpiresAt : Nat
  maxAdmissionAge : Nat
  maxApprovalLifetime : Nat
  maxVerificationAge : Nat
  maxRevocationStatusAge : Nat


structure ApprovalTimeline.Valid (timeline : ApprovalTimeline) : Prop where
  admissionBeforeApproval :
    timeline.admissionEvaluatedAt ≤ timeline.approvalIssuedAt
  approvalBeforeVerification :
    timeline.approvalIssuedAt ≤ timeline.signatureVerifiedAt
  verificationBeforeRevocationCheck :
    timeline.signatureVerifiedAt ≤ timeline.revocationCheckedAt
  revocationCheckBeforeEvaluation :
    timeline.revocationCheckedAt ≤ timeline.evaluatedAt
  approvalNotExpired :
    timeline.evaluatedAt < timeline.approvalExpiresAt
  admissionFresh :
    timeline.evaluatedAt - timeline.admissionEvaluatedAt ≤
      timeline.maxAdmissionAge
  approvalLifetimeBounded :
    timeline.approvalExpiresAt - timeline.approvalIssuedAt ≤
      timeline.maxApprovalLifetime
  verificationFresh :
    timeline.evaluatedAt - timeline.signatureVerifiedAt ≤
      timeline.maxVerificationAge
  revocationStatusFresh :
    timeline.evaluatedAt - timeline.revocationCheckedAt ≤
      timeline.maxRevocationStatusAge


structure ExternalApprovalWitness where
  admissionProposalBound : Prop
  approvalPolicyBound : Prop
  attestationBound : Prop
  decisionApprove : Prop
  approverAuthorized : Prop
  approverKeyAuthorized : Prop
  verifierAuthorized : Prop
  revocationAuthorityAuthorized : Prop
  signatureAlgorithmAllowed : Prop
  distinctApprovalRoles : Prop
  signedPayloadBound : Prop
  signatureMetadataBound : Prop
  signatureVerified : Prop
  timeline : ApprovalTimeline
  revocationStatusValid : Prop
  notRevoked : Prop
  externalApprovalGranted : Bool
  applicationAuthorizationEligible : Bool
  patchApplicationAuthority : Bool
  commitAuthority : Bool
  referenceMutationAuthority : Bool


structure ExternalApprovalWitness.Valid
    (witness : ExternalApprovalWitness) : Prop where
  admissionProposalBound : witness.admissionProposalBound
  approvalPolicyBound : witness.approvalPolicyBound
  attestationBound : witness.attestationBound
  decisionApprove : witness.decisionApprove
  approverAuthorized : witness.approverAuthorized
  approverKeyAuthorized : witness.approverKeyAuthorized
  verifierAuthorized : witness.verifierAuthorized
  revocationAuthorityAuthorized : witness.revocationAuthorityAuthorized
  signatureAlgorithmAllowed : witness.signatureAlgorithmAllowed
  distinctApprovalRoles : witness.distinctApprovalRoles
  signedPayloadBound : witness.signedPayloadBound
  signatureMetadataBound : witness.signatureMetadataBound
  signatureVerified : witness.signatureVerified
  timeline : witness.timeline.Valid
  revocationStatusValid : witness.revocationStatusValid
  notRevoked : witness.notRevoked
  externalApprovalGranted : witness.externalApprovalGranted = true
  applicationAuthorizationEligible :
    witness.applicationAuthorizationEligible = true
  patchApplicationAuthority : witness.patchApplicationAuthority = false
  commitAuthority : witness.commitAuthority = false
  referenceMutationAuthority : witness.referenceMutationAuthority = false


theorem valid_approval_has_ordered_evidence
    (witness : ExternalApprovalWitness)
    (h : witness.Valid) :
    witness.timeline.admissionEvaluatedAt ≤ witness.timeline.approvalIssuedAt ∧
      witness.timeline.approvalIssuedAt ≤ witness.timeline.signatureVerifiedAt ∧
      witness.timeline.signatureVerifiedAt ≤ witness.timeline.revocationCheckedAt ∧
      witness.timeline.revocationCheckedAt ≤ witness.timeline.evaluatedAt := by
  exact ⟨h.timeline.admissionBeforeApproval,
    h.timeline.approvalBeforeVerification,
    h.timeline.verificationBeforeRevocationCheck,
    h.timeline.revocationCheckBeforeEvaluation⟩


theorem valid_approval_is_fresh_and_unexpired
    (witness : ExternalApprovalWitness)
    (h : witness.Valid) :
    witness.timeline.evaluatedAt < witness.timeline.approvalExpiresAt ∧
      witness.timeline.evaluatedAt - witness.timeline.admissionEvaluatedAt ≤
        witness.timeline.maxAdmissionAge ∧
      witness.timeline.evaluatedAt - witness.timeline.signatureVerifiedAt ≤
        witness.timeline.maxVerificationAge ∧
      witness.timeline.evaluatedAt - witness.timeline.revocationCheckedAt ≤
        witness.timeline.maxRevocationStatusAge := by
  exact ⟨h.timeline.approvalNotExpired,
    h.timeline.admissionFresh,
    h.timeline.verificationFresh,
    h.timeline.revocationStatusFresh⟩


theorem valid_approval_has_verified_signature
    (witness : ExternalApprovalWitness)
    (h : witness.Valid) :
    witness.signedPayloadBound ∧
      witness.signatureMetadataBound ∧
      witness.signatureVerified := by
  exact ⟨h.signedPayloadBound, h.signatureMetadataBound,
    h.signatureVerified⟩


theorem valid_approval_is_not_revoked
    (witness : ExternalApprovalWitness)
    (h : witness.Valid) :
    witness.revocationStatusValid ∧ witness.notRevoked := by
  exact ⟨h.revocationStatusValid, h.notRevoked⟩


theorem valid_approval_requires_distinct_authorized_roles
    (witness : ExternalApprovalWitness)
    (h : witness.Valid) :
    witness.approverAuthorized ∧
      witness.approverKeyAuthorized ∧
      witness.verifierAuthorized ∧
      witness.revocationAuthorityAuthorized ∧
      witness.distinctApprovalRoles := by
  exact ⟨h.approverAuthorized, h.approverKeyAuthorized,
    h.verifierAuthorized, h.revocationAuthorityAuthorized,
    h.distinctApprovalRoles⟩


theorem valid_approval_is_only_application_authorization_eligible
    (witness : ExternalApprovalWitness)
    (h : witness.Valid) :
    witness.externalApprovalGranted = true ∧
      witness.applicationAuthorizationEligible = true ∧
      witness.patchApplicationAuthority = false ∧
      witness.commitAuthority = false ∧
      witness.referenceMutationAuthority = false := by
  exact ⟨h.externalApprovalGranted, h.applicationAuthorizationEligible,
    h.patchApplicationAuthority, h.commitAuthority,
    h.referenceMutationAuthority⟩


theorem valid_approval_grants_no_repository_mutation_authority
    (witness : ExternalApprovalWitness)
    (h : witness.Valid) :
    witness.patchApplicationAuthority = false ∧
      witness.commitAuthority = false ∧
      witness.referenceMutationAuthority = false := by
  exact ⟨h.patchApplicationAuthority, h.commitAuthority,
    h.referenceMutationAuthority⟩

end KUOS.WORLD.KuuOSRepositoryExternalApprovalV0_90
