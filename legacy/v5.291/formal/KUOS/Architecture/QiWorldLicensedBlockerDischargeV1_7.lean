import Mathlib
import KUOS.Architecture.QiWorldIndraTransportRequestV1_6

/-!
Qi–WORLD licensed blocker discharge v1.7.

The v1.6 Indra request remains request-only and unrealized. A separate,
externally-issued, single-use authority may discharge only the present-cycle
activation and execution-boundary blockers for a strictly later ActOS cycle.
The source blocker certificate, Qi history, WORLD identity, truth separation,
cycle separation, and noncollapse remain invariant.
-/

namespace KUOS.Architecture

def licensedDischargeMask : CrossCycleBlockerVector
  | .presentActivation => true
  | .executionBoundary => true
  | .memoryPreservation => false
  | .worldPreservation => false
  | .truthSeparation => false
  | .cycleSeparation => false
  | .noncollapse => false

def licensedInvariantMask : CrossCycleBlockerVector
  | .presentActivation => false
  | .executionBoundary => false
  | .memoryPreservation => true
  | .worldPreservation => true
  | .truthSeparation => true
  | .cycleSeparation => true
  | .noncollapse => true

theorem licensed_masks_partition (blocker : CrossCycleBlocker) :
    (licensedDischargeMask blocker || licensedInvariantMask blocker) = true := by
  cases blocker <;> rfl

theorem licensed_masks_disjoint (blocker : CrossCycleBlocker) :
    (licensedDischargeMask blocker && licensedInvariantMask blocker) = false := by
  cases blocker <;> rfl

theorem invariant_mask_excludes_discharge
    (blocker : CrossCycleBlocker)
    (hInvariant : licensedInvariantMask blocker = true) :
    licensedDischargeMask blocker = false := by
  have hDisjoint := licensed_masks_disjoint blocker
  simpa [hInvariant] using hDisjoint

structure QiWorldLicensedBlockerDischarge where
  sourceBlocker : CrossCycleBlockerCertificate
  sourceBlockerDigest : Nat
  sourceIndraRequest : QiWorldIndraTransportRequest
  indra_blocker_digest_bound :
    sourceIndraRequest.blockerCertificateDigest = sourceBlockerDigest

  dischargeMask : CrossCycleBlockerVector
  dischargeMask_eq : dischargeMask = licensedDischargeMask
  retainedMask : CrossCycleBlockerVector
  retainedMask_eq :
    retainedMask =
      fun blocker => sourceBlocker.vector blocker && licensedInvariantMask blocker

  externalAuthorityValid : Prop
  externalAuthorityValidProof : externalAuthorityValid
  externalAuthorityNotAnalyticTransportReceipt : Prop
  externalAuthorityNotAnalyticTransportReceiptProof :
    externalAuthorityNotAnalyticTransportReceipt
  humanApprovalValid : Prop
  humanApprovalValidProof : humanApprovalValid
  hostLicenseValid : Prop
  hostLicenseValidProof : hostLicenseValid
  stepAuthorizationBound : Prop
  stepAuthorizationBoundProof : stepAuthorizationBound
  authorityDoesNotWidenLicense : Prop
  authorityDoesNotWidenLicenseProof : authorityDoesNotWidenLicense

  sourceCertificateImmutable : Prop
  sourceCertificateImmutableProof : sourceCertificateImmutable
  sourceCycleImmutable : Prop
  sourceCycleImmutableProof : sourceCycleImmutable
  targetCycleStrictlyLater : Prop
  targetCycleStrictlyLaterProof : targetCycleStrictlyLater
  singleUseRelease : Prop
  singleUseReleaseProof : singleUseRelease
  releaseConsumptionCount : Nat
  release_consumed_once : releaseConsumptionCount = 1

  targetActStarted : Bool
  target_act_started : targetActStarted = true
  effectRecorded : Bool
  effect_recorded : effectRecorded = true
  observationRequired : Bool
  observation_required : observationRequired = true
  verificationRequired : Bool
  verification_required : verificationRequired = true

  indraTransportStillUnrealized : Prop
  indraTransportStillUnrealizedProof : indraTransportStillUnrealized
  memoryOverwritten : Bool
  no_memory_overwrite : memoryOverwritten = false
  exactWorldUpdated : Bool
  no_exact_world_update : exactWorldUpdated = false
  truthPromoted : Bool
  no_truth_promotion : truthPromoted = false
  sameCycleRecursiveInvocation : Bool
  no_same_cycle_recursion : sameCycleRecursiveInvocation = false
  multiWorldCollapsed : Bool
  no_multi_world_collapse : multiWorldCollapsed = false

  releaseGrantsFurtherAuthority : Bool
  no_further_authority_issue : releaseGrantsFurtherAuthority = false
  releaseGrantsPlanCompletion : Bool
  no_plan_completion_authority : releaseGrantsPlanCompletion = false
  releaseGrantsAutomaticRollback : Bool
  no_automatic_rollback_authority : releaseGrantsAutomaticRollback = false

namespace QiWorldLicensedBlockerDischarge
variable (D : QiWorldLicensedBlockerDischarge)

theorem source_certificate_remains_active :
    AllBlockersActive D.sourceBlocker.vector :=
  D.sourceBlocker.all_active

theorem indra_request_bound_to_source_blocker :
    D.sourceIndraRequest.blockerCertificateDigest = D.sourceBlockerDigest :=
  D.indra_blocker_digest_bound

theorem indra_request_remains_unrealized_and_non_authoritative :
    D.sourceIndraRequest.requestOnly = true ∧
    D.sourceIndraRequest.transportRealized = false ∧
    D.sourceIndraRequest.worldUpdated = false ∧
    D.sourceIndraRequest.requestGrantsExecution = false ∧
    D.sourceIndraRequest.requestGrantsTruth = false ∧
    D.sourceIndraRequest.requestIssuesAuthority = false ∧
    D.indraTransportStillUnrealized :=
  ⟨D.sourceIndraRequest.request_only,
    D.sourceIndraRequest.transport_not_realized,
    D.sourceIndraRequest.no_world_update,
    D.sourceIndraRequest.no_execution_authority,
    D.sourceIndraRequest.no_truth_authority,
    D.sourceIndraRequest.no_authority_issue,
    D.indraTransportStillUnrealizedProof⟩

theorem discharged_only_when_releasable
    (blocker : CrossCycleBlocker)
    (h : D.dischargeMask blocker = true) :
    licensedDischargeMask blocker = true := by
  rw [D.dischargeMask_eq] at h
  exact h

theorem all_invariant_blockers_retained
    (blocker : CrossCycleBlocker)
    (hInvariant : licensedInvariantMask blocker = true) :
    D.retainedMask blocker = true := by
  rw [D.retainedMask_eq]
  change (D.sourceBlocker.vector blocker && licensedInvariantMask blocker) = true
  rw [D.sourceBlocker.all_active blocker, hInvariant]
  rfl

theorem memory_world_truth_cycle_noncollapse_retained :
    D.retainedMask .memoryPreservation = true ∧
    D.retainedMask .worldPreservation = true ∧
    D.retainedMask .truthSeparation = true ∧
    D.retainedMask .cycleSeparation = true ∧
    D.retainedMask .noncollapse = true := by
  exact
    ⟨all_invariant_blockers_retained D .memoryPreservation rfl,
      all_invariant_blockers_retained D .worldPreservation rfl,
      all_invariant_blockers_retained D .truthSeparation rfl,
      all_invariant_blockers_retained D .cycleSeparation rfl,
      all_invariant_blockers_retained D .noncollapse rfl⟩

theorem release_requires_separate_external_bounded_authority :
    D.externalAuthorityValid ∧
    D.externalAuthorityNotAnalyticTransportReceipt ∧
    D.humanApprovalValid ∧
    D.hostLicenseValid ∧
    D.stepAuthorizationBound ∧
    D.authorityDoesNotWidenLicense ∧
    D.targetCycleStrictlyLater ∧
    D.singleUseRelease ∧
    D.releaseConsumptionCount = 1 :=
  ⟨D.externalAuthorityValidProof,
    D.externalAuthorityNotAnalyticTransportReceiptProof,
    D.humanApprovalValidProof,
    D.hostLicenseValidProof,
    D.stepAuthorizationBoundProof,
    D.authorityDoesNotWidenLicenseProof,
    D.targetCycleStrictlyLaterProof,
    D.singleUseReleaseProof,
    D.release_consumed_once⟩

theorem source_is_immutable_during_release :
    D.sourceCertificateImmutable ∧ D.sourceCycleImmutable :=
  ⟨D.sourceCertificateImmutableProof, D.sourceCycleImmutableProof⟩

theorem licensed_handoff_creates_evidence_debt :
    D.targetActStarted = true ∧
    D.effectRecorded = true ∧
    D.observationRequired = true ∧
    D.verificationRequired = true :=
  ⟨D.target_act_started,
    D.effect_recorded,
    D.observation_required,
    D.verification_required⟩

theorem invariant_safety_is_not_discharged :
    D.memoryOverwritten = false ∧
    D.exactWorldUpdated = false ∧
    D.truthPromoted = false ∧
    D.sameCycleRecursiveInvocation = false ∧
    D.multiWorldCollapsed = false :=
  ⟨D.no_memory_overwrite,
    D.no_exact_world_update,
    D.no_truth_promotion,
    D.no_same_cycle_recursion,
    D.no_multi_world_collapse⟩

theorem release_has_no_secondary_authority :
    D.releaseGrantsFurtherAuthority = false ∧
    D.releaseGrantsPlanCompletion = false ∧
    D.releaseGrantsAutomaticRollback = false :=
  ⟨D.no_further_authority_issue,
    D.no_plan_completion_authority,
    D.no_automatic_rollback_authority⟩

theorem licensed_discharge_boundary :
    D.sourceIndraRequest.transportRealized = false ∧
    D.externalAuthorityValid ∧
    D.externalAuthorityNotAnalyticTransportReceipt ∧
    D.singleUseRelease ∧
    D.releaseConsumptionCount = 1 ∧
    D.sourceCertificateImmutable ∧
    D.targetCycleStrictlyLater ∧
    D.effectRecorded = true ∧
    D.observationRequired = true ∧
    D.verificationRequired = true ∧
    D.memoryOverwritten = false ∧
    D.exactWorldUpdated = false ∧
    D.truthPromoted = false :=
  ⟨D.sourceIndraRequest.transport_not_realized,
    D.externalAuthorityValidProof,
    D.externalAuthorityNotAnalyticTransportReceiptProof,
    D.singleUseReleaseProof,
    D.release_consumed_once,
    D.sourceCertificateImmutableProof,
    D.targetCycleStrictlyLaterProof,
    D.effect_recorded,
    D.observation_required,
    D.verification_required,
    D.no_memory_overwrite,
    D.no_exact_world_update,
    D.no_truth_promotion⟩

end QiWorldLicensedBlockerDischarge
end KUOS.Architecture
