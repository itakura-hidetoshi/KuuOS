import Mathlib
import KUOS.PlanOS.ReplanBoundSynthesisV0_1

namespace KUOS
namespace ActOS

inductive ActPhase where
  | bind
  | select
  | authorize
  | project
  | invoke
  | verify
  | commit
  deriving DecidableEq, Repr


def ActPhase.next : ActPhase → Option ActPhase
  | .bind => some .select
  | .select => some .authorize
  | .authorize => some .project
  | .project => some .invoke
  | .invoke => some .verify
  | .verify => some .commit
  | .commit => none


theorem actPhase_next_deterministic
    (phase left right : ActPhase)
    (hleft : phase.next = some left)
    (hright : phase.next = some right) :
    left = right := by
  rw [hleft] at hright
  exact Option.some.inj hright


theorem actPhase_bind_next :
    ActPhase.bind.next = some ActPhase.select := by
  rfl


theorem actPhase_invoke_next :
    ActPhase.invoke.next = some ActPhase.verify := by
  rfl


structure ActEventIndex where
  current : ℕ


def ActEventIndex.append (index : ActEventIndex) : ActEventIndex where
  current := index.current + 1


theorem actEventIndex_strict
    (index : ActEventIndex) :
    index.current < index.append.current := by
  simp [ActEventIndex.append]


structure FivefoldBinding where
  committedPlanBound : Bool
  exactStepBound : Bool
  actPhaseBound : Bool
  hostLicenseBound : Bool
  projectionReceiptBound : Bool
  planRequired : committedPlanBound = true
  stepRequired : exactStepBound = true
  actPhaseRequired : actPhaseBound = true
  licenseRequired : hostLicenseBound = true
  projectionRequired : projectionReceiptBound = true


theorem invocation_requires_committed_plan
    (binding : FivefoldBinding) :
    binding.committedPlanBound = true := by
  exact binding.planRequired


theorem invocation_requires_exact_step
    (binding : FivefoldBinding) :
    binding.exactStepBound = true := by
  exact binding.stepRequired


theorem invocation_requires_act_phase
    (binding : FivefoldBinding) :
    binding.actPhaseBound = true := by
  exact binding.actPhaseRequired


theorem invocation_requires_host_license
    (binding : FivefoldBinding) :
    binding.hostLicenseBound = true := by
  exact binding.licenseRequired


theorem invocation_requires_projection_receipt_binding
    (binding : FivefoldBinding) :
    binding.projectionReceiptBound = true := by
  exact binding.projectionRequired


structure SelectedActStep where
  isActCandidate : Bool
  effectful : Bool
  stopConditionsPresent : Bool
  observationDigestPresent : Bool
  verificationCriterionPresent : Bool
  candidateRequired : isActCandidate = true
  effectRequired : effectful = true
  stopRequired : stopConditionsPresent = true
  observationRequired : observationDigestPresent = true
  verificationRequired : verificationCriterionPresent = true


theorem selectedStep_is_effectful_actCandidate
    (step : SelectedActStep) :
    step.isActCandidate = true ∧ step.effectful = true := by
  exact ⟨step.candidateRequired, step.effectRequired⟩


theorem selectedStep_has_stop_condition
    (step : SelectedActStep) :
    step.stopConditionsPresent = true := by
  exact step.stopRequired


theorem selectedStep_has_observation_and_verification
    (step : SelectedActStep) :
    step.observationDigestPresent = true ∧
      step.verificationCriterionPresent = true := by
  exact ⟨step.observationRequired, step.verificationRequired⟩


structure AuthorizationBoundary where
  explicitStepAuthorization : Bool
  humanApprovalWhenRequired : Bool
  singleUse : Bool
  doesNotWidenLicense : Bool
  authorizationRequired : explicitStepAuthorization = true
  approvalRequired : humanApprovalWhenRequired = true
  singleUseRequired : singleUse = true
  noWideningRequired : doesNotWidenLicense = true


theorem authorization_is_single_use
    (boundary : AuthorizationBoundary) :
    boundary.singleUse = true := by
  exact boundary.singleUseRequired


theorem authorization_cannot_widen_license
    (boundary : AuthorizationBoundary) :
    boundary.doesNotWidenLicense = true := by
  exact boundary.noWideningRequired


structure BoundedInvocation where
  jobsClaimed : ℕ
  slicesRun : ℕ
  jobsBounded : jobsClaimed ≤ 1
  slicesBounded : slicesRun ≤ 1


theorem invocation_claims_at_most_one_job
    (invocation : BoundedInvocation) :
    invocation.jobsClaimed ≤ 1 := by
  exact invocation.jobsBounded


theorem invocation_runs_at_most_one_slice
    (invocation : BoundedInvocation) :
    invocation.slicesRun ≤ 1 := by
  exact invocation.slicesBounded


inductive HostRoute where
  | effectRecorded
  | blocked
  | replayed
  deriving DecidableEq, Repr


structure HostReceiptSemantics where
  route : HostRoute
  effectRecordCount : ℕ
  truthAuthority : Bool
  finalCommitmentAuthority : Bool
  memoryOverwriteAuthority : Bool
  readyBoundedSliceOnly :
    route = .effectRecorded → effectRecordCount = 1
  blockedNoEffect :
    route = .blocked → effectRecordCount = 0
  replayNoDuplicate :
    route = .replayed → effectRecordCount ≤ 1
  truthForbidden : truthAuthority = false
  finalForbidden : finalCommitmentAuthority = false
  overwriteForbidden : memoryOverwriteAuthority = false


theorem effectRecorded_means_one_record
    (receipt : HostReceiptSemantics)
    (ready : receipt.route = .effectRecorded) :
    receipt.effectRecordCount = 1 := by
  exact receipt.readyBoundedSliceOnly ready


theorem blocked_records_no_effect
    (receipt : HostReceiptSemantics)
    (blocked : receipt.route = .blocked) :
    receipt.effectRecordCount = 0 := by
  exact receipt.blockedNoEffect blocked


theorem replay_does_not_duplicate_effect
    (receipt : HostReceiptSemantics)
    (replayed : receipt.route = .replayed) :
    receipt.effectRecordCount ≤ 1 := by
  exact receipt.replayNoDuplicate replayed


theorem successfulReceipt_is_not_truth_authority
    (receipt : HostReceiptSemantics) :
    receipt.truthAuthority = false := by
  exact receipt.truthForbidden


theorem successfulReceipt_is_not_final_commitment
    (receipt : HostReceiptSemantics) :
    receipt.finalCommitmentAuthority = false := by
  exact receipt.finalForbidden


structure PostEffectDebt where
  effectRecorded : Bool
  observationRequired : Bool
  verificationRequired : Bool
  automaticTruthPromotion : Bool
  automaticPlanCompletion : Bool
  automaticRollback : Bool
  debtRequired :
    effectRecorded = true →
      observationRequired = true ∧ verificationRequired = true
  truthPromotionForbidden : automaticTruthPromotion = false
  planCompletionForbidden : automaticPlanCompletion = false
  rollbackForbidden : automaticRollback = false


theorem effect_preserves_observation_debt
    (debt : PostEffectDebt)
    (recorded : debt.effectRecorded = true) :
    debt.observationRequired = true := by
  exact (debt.debtRequired recorded).1


theorem effect_preserves_verification_debt
    (debt : PostEffectDebt)
    (recorded : debt.effectRecorded = true) :
    debt.verificationRequired = true := by
  exact (debt.debtRequired recorded).2


theorem effect_does_not_promote_truth
    (debt : PostEffectDebt) :
    debt.automaticTruthPromotion = false := by
  exact debt.truthPromotionForbidden


theorem effect_does_not_complete_plan
    (debt : PostEffectDebt) :
    debt.automaticPlanCompletion = false := by
  exact debt.planCompletionForbidden


theorem effect_does_not_automatically_rollback
    (debt : PostEffectDebt) :
    debt.automaticRollback = false := by
  exact debt.rollbackForbidden


structure LowerAuthorityBoundary where
  lowerHostReceiptCanonical : Bool
  lowerAuthorityPreserved : Bool
  clinicalAuthority : Bool
  legalAuthority : Bool
  institutionalAuthority : Bool
  theoremAuthority : Bool
  canonicalRequired : lowerHostReceiptCanonical = true
  lowerRequired : lowerAuthorityPreserved = true
  clinicalForbidden : clinicalAuthority = false
  legalForbidden : legalAuthority = false
  institutionalForbidden : institutionalAuthority = false
  theoremForbidden : theoremAuthority = false


theorem lowerHostReceipt_remains_canonical
    (boundary : LowerAuthorityBoundary) :
    boundary.lowerHostReceiptCanonical = true := by
  exact boundary.canonicalRequired


theorem actOS_preserves_lower_authority
    (boundary : LowerAuthorityBoundary) :
    boundary.lowerAuthorityPreserved = true := by
  exact boundary.lowerRequired


theorem actOS_grants_no_clinical_or_legal_authority
    (boundary : LowerAuthorityBoundary) :
    boundary.clinicalAuthority = false ∧ boundary.legalAuthority = false := by
  exact ⟨boundary.clinicalForbidden, boundary.legalForbidden⟩


structure ActHistory where
  committedRecords : ℕ
  recoveredRecords : ℕ
  snapshotRecords : ℕ
  recoveryExact : recoveredRecords = committedRecords
  snapshotDerived : snapshotRecords = recoveredRecords


theorem actHistory_snapshot_matches_commits
    (history : ActHistory) :
    history.snapshotRecords = history.committedRecords := by
  rw [history.snapshotDerived, history.recoveryExact]

end ActOS
end KUOS
