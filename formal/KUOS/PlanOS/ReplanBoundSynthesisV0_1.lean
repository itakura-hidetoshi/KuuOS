import Mathlib
import KUOS.DecisionOS.WaRelationalHarmonyV0_3

namespace KUOS
namespace PlanOS

inductive PlanPhase where
  | bind
  | decompose
  | order
  | resource
  | guard
  | checkpoint
  | verify
  | commit
  deriving DecidableEq, Repr


def PlanPhase.next : PlanPhase → Option PlanPhase
  | .bind => some .decompose
  | .decompose => some .order
  | .order => some .resource
  | .resource => some .guard
  | .guard => some .checkpoint
  | .checkpoint => some .verify
  | .verify => some .commit
  | .commit => none


theorem planPhase_next_deterministic
    (phase left right : PlanPhase)
    (hleft : phase.next = some left)
    (hright : phase.next = some right) :
    left = right := by
  rw [hleft] at hright
  exact Option.some.inj hright


theorem planPhase_no_bind_skip :
    PlanPhase.bind.next = some PlanPhase.decompose := by
  rfl


theorem planPhase_no_verify_skip :
    PlanPhase.verify.next = some PlanPhase.commit := by
  rfl


structure PlanEventIndex where
  current : ℕ


def PlanEventIndex.append (index : PlanEventIndex) : PlanEventIndex where
  current := index.current + 1


theorem planEventIndex_strict
    (index : PlanEventIndex) :
    index.current < index.append.current := by
  simp [PlanEventIndex.append]


structure DependencyCertificate (Step : Type) where
  rank : Step → ℕ
  dependsOn : Step → Step → Prop
  dependencyLowerRank : ∀ step dependency,
    dependsOn step dependency → rank dependency < rank step


theorem dependency_no_self
    {Step : Type}
    (certificate : DependencyCertificate Step)
    (step : Step) :
    ¬ certificate.dependsOn step step := by
  intro dependency
  have lower := certificate.dependencyLowerRank step step dependency
  exact (Nat.lt_irrefl _ lower)


theorem dependency_no_two_cycle
    {Step : Type}
    (certificate : DependencyCertificate Step)
    (left right : Step) :
    ¬ (certificate.dependsOn left right ∧
      certificate.dependsOn right left) := by
  intro cycle
  have hright := certificate.dependencyLowerRank left right cycle.1
  have hleft := certificate.dependencyLowerRank right left cycle.2
  exact (Nat.not_lt_of_ge (Nat.le_of_lt hright)) hleft


structure ResourceBoundary where
  totalCost : ℝ
  planBudget : ℝ
  peakStepRisk : ℝ
  maximumStepRisk : ℝ
  totalCostNonnegative : 0 ≤ totalCost
  peakRiskNonnegative : 0 ≤ peakStepRisk
  costBounded : totalCost ≤ planBudget
  riskBounded : peakStepRisk ≤ maximumStepRisk


theorem plan_total_cost_bounded
    (boundary : ResourceBoundary) :
    boundary.totalCost ≤ boundary.planBudget := by
  exact boundary.costBounded


theorem plan_peak_risk_bounded
    (boundary : ResourceBoundary) :
    boundary.peakStepRisk ≤ boundary.maximumStepRisk := by
  exact boundary.riskBounded


structure EffectGuard where
  effectful : Bool
  rollbackPresent : Bool
  humanReviewRequired : Bool
  externalLicenseRequired : Bool
  stopConditionPresent : Bool
  checkpointPresent : Bool
  guarded :
    effectful = true →
      ((rollbackPresent = true) ∨
        (humanReviewRequired = true ∧ externalLicenseRequired = true)) ∧
      stopConditionPresent = true ∧
      checkpointPresent = true


theorem effectfulStep_has_rollback_or_escalation
    (guard : EffectGuard)
    (effectful : guard.effectful = true) :
    guard.rollbackPresent = true ∨
      (guard.humanReviewRequired = true ∧
        guard.externalLicenseRequired = true) := by
  exact (guard.guarded effectful).1


theorem effectfulStep_has_stop_condition
    (guard : EffectGuard)
    (effectful : guard.effectful = true) :
    guard.stopConditionPresent = true := by
  exact (guard.guarded effectful).2.1


theorem effectfulStep_has_checkpoint
    (guard : EffectGuard)
    (effectful : guard.effectful = true) :
    guard.checkpointPresent = true := by
  exact (guard.guarded effectful).2.2


structure SourceIdentityBoundary where
  sourceOptionIdentityPreserved : Bool
  stakeholderSectionsPreserved : Bool
  vetoAppealHistoryPreserved : Bool
  identityRequired : sourceOptionIdentityPreserved = true
  stakeholderRequired : stakeholderSectionsPreserved = true
  historyRequired : vetoAppealHistoryPreserved = true


theorem plan_preserves_source_option_identity
    (boundary : SourceIdentityBoundary) :
    boundary.sourceOptionIdentityPreserved = true := by
  exact boundary.identityRequired


theorem plan_preserves_stakeholder_sections
    (boundary : SourceIdentityBoundary) :
    boundary.stakeholderSectionsPreserved = true := by
  exact boundary.stakeholderRequired


theorem plan_preserves_veto_appeal_history
    (boundary : SourceIdentityBoundary) :
    boundary.vetoAppealHistoryPreserved = true := by
  exact boundary.historyRequired


structure RestrictedPlanRoute where
  observationPlan : Bool
  repairPlan : Bool
  handoverPlan : Bool
  containsEffectfulLocalAction : Bool
  restricted :
    observationPlan = true ∨ repairPlan = true ∨ handoverPlan = true →
      containsEffectfulLocalAction = false


theorem restrictedPlan_has_no_effectful_local_action
    (route : RestrictedPlanRoute)
    (restrictedRoute :
      route.observationPlan = true ∨
      route.repairPlan = true ∨
      route.handoverPlan = true) :
    route.containsEffectfulLocalAction = false := by
  exact route.restricted restrictedRoute


structure PlanAuthorityBoundary where
  planIsDecision : Bool
  planIsExecution : Bool
  grantsHostLicense : Bool
  grantsClinicalAuthority : Bool
  grantsToolAuthority : Bool
  decisionSeparation : planIsDecision = false
  executionForbidden : planIsExecution = false
  hostLicenseForbidden : grantsHostLicense = false
  clinicalForbidden : grantsClinicalAuthority = false
  toolForbidden : grantsToolAuthority = false


theorem plan_is_not_decision
    (boundary : PlanAuthorityBoundary) :
    boundary.planIsDecision = false := by
  exact boundary.decisionSeparation


theorem plan_does_not_execute
    (boundary : PlanAuthorityBoundary) :
    boundary.planIsExecution = false := by
  exact boundary.executionForbidden


theorem plan_does_not_grant_host_license
    (boundary : PlanAuthorityBoundary) :
    boundary.grantsHostLicense = false := by
  exact boundary.hostLicenseForbidden


structure PlanCommitBoundary where
  futureOnly : Bool
  memoryOverwrite : Bool
  planNotExecution : Bool
  planNotHostLicense : Bool
  sourceIdentityPreserved : Bool
  futureRequired : futureOnly = true
  overwriteForbidden : memoryOverwrite = false
  nonExecutionRequired : planNotExecution = true
  nonLicenseRequired : planNotHostLicense = true
  identityRequired : sourceIdentityPreserved = true


theorem planCommit_is_future_only
    (boundary : PlanCommitBoundary) :
    boundary.futureOnly = true := by
  exact boundary.futureRequired


theorem planCommit_does_not_overwrite
    (boundary : PlanCommitBoundary) :
    boundary.memoryOverwrite = false := by
  exact boundary.overwriteForbidden


theorem planCommit_is_not_execution
    (boundary : PlanCommitBoundary) :
    boundary.planNotExecution = true := by
  exact boundary.nonExecutionRequired


structure PlanHistory where
  committedPlans : ℕ
  recoveredPlans : ℕ
  snapshotPlans : ℕ
  recoveryExact : recoveredPlans = committedPlans
  snapshotDerived : snapshotPlans = recoveredPlans


theorem planHistory_snapshot_matches_commits
    (history : PlanHistory) :
    history.snapshotPlans = history.committedPlans := by
  rw [history.snapshotDerived, history.recoveryExact]


structure PlanPhaseActivation where
  missionPhaseIsPlan : Bool
  replanReceiptPresent : Bool
  nextPlanBasisPresent : Bool
  futureOnly : Bool
  memoryOverwrite : Bool
  planNotExecution : Bool
  hostLicenseGranted : Bool
  planPhaseRequired : missionPhaseIsPlan = true
  replanRequired : replanReceiptPresent = true
  basisRequired : nextPlanBasisPresent = true
  futureRequired : futureOnly = true
  overwriteForbidden : memoryOverwrite = false
  nonExecutionRequired : planNotExecution = true
  hostLicenseForbidden : hostLicenseGranted = false


theorem planActivation_requires_plan_phase
    (receipt : PlanPhaseActivation) :
    receipt.missionPhaseIsPlan = true := by
  exact receipt.planPhaseRequired


theorem planActivation_requires_replan_receipt
    (receipt : PlanPhaseActivation) :
    receipt.replanReceiptPresent = true := by
  exact receipt.replanRequired


theorem planActivation_does_not_execute
    (receipt : PlanPhaseActivation) :
    receipt.planNotExecution = true := by
  exact receipt.nonExecutionRequired


theorem planActivation_does_not_grant_host_license
    (receipt : PlanPhaseActivation) :
    receipt.hostLicenseGranted = false := by
  exact receipt.hostLicenseForbidden

end PlanOS
end KUOS
