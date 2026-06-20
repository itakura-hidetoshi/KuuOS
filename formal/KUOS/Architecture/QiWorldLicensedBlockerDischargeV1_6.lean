import Mathlib
import KUOS.Architecture.QiWorldCrossCycleBlockerTheoryV1_5

/-!
Qi–WORLD licensed blocker discharge v1.6.

The source v1.5 blocker certificate is not deleted or rewritten.  A separate,
single-use, externally-authorized handoff may discharge only the present-cycle
activation and execution-boundary blockers for a strictly later cycle.  Memory,
WORLD identity, truth separation, cycle separation, and noncollapse remain
invariant.
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
    licensedDischargeMask blocker || licensedInvariantMask blocker = true := by
  cases blocker <;> rfl


theorem licensed_masks_disjoint (blocker : CrossCycleBlocker) :
    licensedDischargeMask blocker && licensedInvariantMask blocker = false := by
  cases blocker <;> rfl


theorem invariant_mask_excludes_discharge
    (blocker : CrossCycleBlocker)
    (hInvariant : licensedInvariantMask blocker = true) :
    licensedDischargeMask blocker = false := by
  cases blocker <;> simp [licensedInvariantMask, licensedDischargeMask] at hInvariant ⊢


structure QiWorldLicensedBlockerDischarge where
  source : CrossCycleBlockerCertificate
  dischargeMask : CrossCycleBlockerVector
  dischargeMask_eq : dischargeMask = licensedDischargeMask
  retainedMask : CrossCycleBlockerVector
  retainedMask_eq :
    retainedMask = fun blocker => source.vector blocker && licensedInvariantMask blocker

  externalAuthorityValid : Prop
  externalAuthorityValidProof : externalAuthorityValid
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
    AllBlockersActive D.source.vector :=
  D.source.all_active


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
  simp [D.source.all_active blocker, hInvariant]


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


theorem release_requires_external_bounded_authority :
    D.externalAuthorityValid ∧
    D.humanApprovalValid ∧
    D.hostLicenseValid ∧
    D.stepAuthorizationBound ∧
    D.authorityDoesNotWidenLicense ∧
    D.targetCycleStrictlyLater ∧
    D.singleUseRelease ∧
    D.releaseConsumptionCount = 1 :=
  ⟨D.externalAuthorityValidProof,
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
    D.externalAuthorityValid ∧
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
  ⟨D.externalAuthorityValidProof,
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
