import KUOS.WORLD.KuuOSRepositoryExternalApprovalV0_90

namespace KUOS.WORLD.KuuOSRepositoryApplicationAuthorizationV0_91


structure ApplicationAuthorizationTimeline where
  approvalEvaluatedAt : Nat
  authorizationIssuedAt : Nat
  sourceObservedAt : Nat
  nonceCheckedAt : Nat
  evaluatedAt : Nat
  authorizationExpiresAt : Nat
  maxAuthorizationLifetime : Nat
  maxSourceObservationAge : Nat
  maxNonceStatusAge : Nat


structure ApplicationAuthorizationTimeline.Valid
    (timeline : ApplicationAuthorizationTimeline) : Prop where
  approvalBeforeAuthorization :
    timeline.approvalEvaluatedAt ≤ timeline.authorizationIssuedAt
  authorizationBeforeSourceObservation :
    timeline.authorizationIssuedAt ≤ timeline.sourceObservedAt
  sourceObservationBeforeNonceCheck :
    timeline.sourceObservedAt ≤ timeline.nonceCheckedAt
  nonceCheckBeforeEvaluation :
    timeline.nonceCheckedAt ≤ timeline.evaluatedAt
  authorizationNotExpired :
    timeline.evaluatedAt < timeline.authorizationExpiresAt
  authorizationLifetimeBounded :
    timeline.authorizationExpiresAt - timeline.authorizationIssuedAt ≤
      timeline.maxAuthorizationLifetime
  sourceObservationFresh :
    timeline.evaluatedAt - timeline.sourceObservedAt ≤
      timeline.maxSourceObservationAge
  nonceStatusFresh :
    timeline.evaluatedAt - timeline.nonceCheckedAt ≤ timeline.maxNonceStatusAge


structure ApplicationAuthorizationWitness where
  externalApprovalBound : Prop
  admissionBound : Prop
  authorizationPolicyBound : Prop
  applicationScopeBound : Prop
  patchBundleBound : Prop
  pathsCanonical : Prop
  expectedPathsNonempty : Prop
  expectedPathsWithinAllowedScope : Prop
  protectedPathsExcluded : Prop
  pathCountWithinPolicy : Prop
  patchCountWithinPolicy : Prop
  sourceCommitUnchanged : Prop
  sourceSnapshotUnchanged : Prop
  objectDatabaseSource : Prop
  workingTreeIgnored : Prop
  nonceAuthorityAuthorized : Prop
  nonceUnused : Prop
  nonceNotRevoked : Prop
  timeline : ApplicationAuthorizationTimeline
  applicationAuthorizationGranted : Bool
  singleUseApplicationEligible : Bool
  patchApplicationExecuted : Bool
  commitAuthority : Bool
  referenceMutationAuthority : Bool


structure ApplicationAuthorizationWitness.Valid
    (witness : ApplicationAuthorizationWitness) : Prop where
  externalApprovalBound : witness.externalApprovalBound
  admissionBound : witness.admissionBound
  authorizationPolicyBound : witness.authorizationPolicyBound
  applicationScopeBound : witness.applicationScopeBound
  patchBundleBound : witness.patchBundleBound
  pathsCanonical : witness.pathsCanonical
  expectedPathsNonempty : witness.expectedPathsNonempty
  expectedPathsWithinAllowedScope : witness.expectedPathsWithinAllowedScope
  protectedPathsExcluded : witness.protectedPathsExcluded
  pathCountWithinPolicy : witness.pathCountWithinPolicy
  patchCountWithinPolicy : witness.patchCountWithinPolicy
  sourceCommitUnchanged : witness.sourceCommitUnchanged
  sourceSnapshotUnchanged : witness.sourceSnapshotUnchanged
  objectDatabaseSource : witness.objectDatabaseSource
  workingTreeIgnored : witness.workingTreeIgnored
  nonceAuthorityAuthorized : witness.nonceAuthorityAuthorized
  nonceUnused : witness.nonceUnused
  nonceNotRevoked : witness.nonceNotRevoked
  timeline : witness.timeline.Valid
  applicationAuthorizationGranted :
    witness.applicationAuthorizationGranted = true
  singleUseApplicationEligible : witness.singleUseApplicationEligible = true
  patchApplicationExecuted : witness.patchApplicationExecuted = false
  commitAuthority : witness.commitAuthority = false
  referenceMutationAuthority : witness.referenceMutationAuthority = false


theorem valid_authorization_has_ordered_evidence
    (witness : ApplicationAuthorizationWitness)
    (h : witness.Valid) :
    witness.timeline.approvalEvaluatedAt ≤
        witness.timeline.authorizationIssuedAt ∧
      witness.timeline.authorizationIssuedAt ≤
        witness.timeline.sourceObservedAt ∧
      witness.timeline.sourceObservedAt ≤ witness.timeline.nonceCheckedAt ∧
      witness.timeline.nonceCheckedAt ≤ witness.timeline.evaluatedAt := by
  exact ⟨h.timeline.approvalBeforeAuthorization,
    h.timeline.authorizationBeforeSourceObservation,
    h.timeline.sourceObservationBeforeNonceCheck,
    h.timeline.nonceCheckBeforeEvaluation⟩


theorem valid_authorization_is_fresh_and_unexpired
    (witness : ApplicationAuthorizationWitness)
    (h : witness.Valid) :
    witness.timeline.evaluatedAt < witness.timeline.authorizationExpiresAt ∧
      witness.timeline.authorizationExpiresAt -
          witness.timeline.authorizationIssuedAt ≤
        witness.timeline.maxAuthorizationLifetime ∧
      witness.timeline.evaluatedAt - witness.timeline.sourceObservedAt ≤
        witness.timeline.maxSourceObservationAge ∧
      witness.timeline.evaluatedAt - witness.timeline.nonceCheckedAt ≤
        witness.timeline.maxNonceStatusAge := by
  exact ⟨h.timeline.authorizationNotExpired,
    h.timeline.authorizationLifetimeBounded,
    h.timeline.sourceObservationFresh,
    h.timeline.nonceStatusFresh⟩


theorem valid_authorization_preserves_exact_source
    (witness : ApplicationAuthorizationWitness)
    (h : witness.Valid) :
    witness.sourceCommitUnchanged ∧ witness.sourceSnapshotUnchanged ∧
      witness.objectDatabaseSource ∧ witness.workingTreeIgnored := by
  exact ⟨h.sourceCommitUnchanged, h.sourceSnapshotUnchanged,
    h.objectDatabaseSource, h.workingTreeIgnored⟩


theorem valid_authorization_preserves_path_scope
    (witness : ApplicationAuthorizationWitness)
    (h : witness.Valid) :
    witness.pathsCanonical ∧ witness.expectedPathsNonempty ∧
      witness.expectedPathsWithinAllowedScope ∧ witness.protectedPathsExcluded ∧
      witness.pathCountWithinPolicy ∧ witness.patchCountWithinPolicy := by
  exact ⟨h.pathsCanonical, h.expectedPathsNonempty,
    h.expectedPathsWithinAllowedScope, h.protectedPathsExcluded,
    h.pathCountWithinPolicy, h.patchCountWithinPolicy⟩


theorem valid_authorization_requires_unused_unrevoked_nonce
    (witness : ApplicationAuthorizationWitness)
    (h : witness.Valid) :
    witness.nonceAuthorityAuthorized ∧ witness.nonceUnused ∧
      witness.nonceNotRevoked := by
  exact ⟨h.nonceAuthorityAuthorized, h.nonceUnused, h.nonceNotRevoked⟩


theorem valid_authorization_is_single_use_but_not_executed
    (witness : ApplicationAuthorizationWitness)
    (h : witness.Valid) :
    witness.applicationAuthorizationGranted = true ∧
      witness.singleUseApplicationEligible = true ∧
      witness.patchApplicationExecuted = false ∧
      witness.commitAuthority = false ∧
      witness.referenceMutationAuthority = false := by
  exact ⟨h.applicationAuthorizationGranted,
    h.singleUseApplicationEligible,
    h.patchApplicationExecuted,
    h.commitAuthority,
    h.referenceMutationAuthority⟩


theorem valid_authorization_grants_no_commit_or_reference_authority
    (witness : ApplicationAuthorizationWitness)
    (h : witness.Valid) :
    witness.patchApplicationExecuted = false ∧
      witness.commitAuthority = false ∧
      witness.referenceMutationAuthority = false := by
  exact ⟨h.patchApplicationExecuted, h.commitAuthority,
    h.referenceMutationAuthority⟩

end KUOS.WORLD.KuuOSRepositoryApplicationAuthorizationV0_91
