import Mathlib
import KUOS.OpenHorizon.MissionContractKernelV0_20
import KUOS.OpenHorizon.ObservationBeliefStateKernelV0_21

namespace KUOS.OpenHorizon

inductive SemanticPlanStatus where
  | ready
  | blockedUnknown
  | blockedContradiction
  | blockedStale
  | capabilityGap
  | resourceBlocked
  deriving DecidableEq, Repr

inductive OutcomeVerificationStatus where
  | verifiedSuccess
  | partialSuccess
  | inconclusive
  | contradicted
  | regressionDetected
  | verificationRequiresHuman
  deriving DecidableEq, Repr

structure SemanticPlanBoundary where
  proposalOnly : Bool
  lowerEffectLicenseRequired : Bool
  grantsExecutionAuthority : Bool
  grantsToolAuthority : Bool
  grantsTruthAuthority : Bool
  grantsMemoryOverwriteAuthority : Bool
  exactMissionBinding : Bool
  exactBeliefBinding : Bool
  finiteResourceEnvelope : Bool

structure OutcomeVerificationBoundary where
  plannerId : Nat
  verifierId : Nat
  executionSucceeded : Bool
  independentMissionEvidence : Bool
  grantsExecutionAuthority : Bool
  grantsMissionTransitionAuthority : Bool
  contradictionVisible : Bool

namespace SemanticPlannerVerifier

def missionSuccessEligible (v : OutcomeVerificationBoundary) : Bool :=
  v.executionSucceeded && v.independentMissionEvidence

theorem execution_success_alone_not_mission_success
    (v : OutcomeVerificationBoundary)
    (hIndependent : v.independentMissionEvidence = false) :
    missionSuccessEligible v = false := by
  simp [missionSuccessEligible, hIndependent]

theorem planner_verifier_separation
    (v : OutcomeVerificationBoundary)
    (hSeparate : v.plannerId ≠ v.verifierId) :
    v.plannerId ≠ v.verifierId := by
  exact hSeparate

theorem semantic_plan_nonAuthority
    (p : SemanticPlanBoundary)
    (hExecution : p.grantsExecutionAuthority = false)
    (hTool : p.grantsToolAuthority = false)
    (hTruth : p.grantsTruthAuthority = false)
    (hMemory : p.grantsMemoryOverwriteAuthority = false) :
    p.grantsExecutionAuthority = false ∧
      p.grantsToolAuthority = false ∧
      p.grantsTruthAuthority = false ∧
      p.grantsMemoryOverwriteAuthority = false := by
  exact ⟨hExecution, hTool, hTruth, hMemory⟩

theorem semantic_planner_verifier_boundary
    (p : SemanticPlanBoundary)
    (v : OutcomeVerificationBoundary)
    (hProposal : p.proposalOnly = true)
    (hLicense : p.lowerEffectLicenseRequired = true)
    (hPlanExecution : p.grantsExecutionAuthority = false)
    (hPlanTool : p.grantsToolAuthority = false)
    (hPlanTruth : p.grantsTruthAuthority = false)
    (hPlanMemory : p.grantsMemoryOverwriteAuthority = false)
    (hMission : p.exactMissionBinding = true)
    (hBelief : p.exactBeliefBinding = true)
    (hFinite : p.finiteResourceEnvelope = true)
    (hSeparate : v.plannerId ≠ v.verifierId)
    (hVerifyExecution : v.grantsExecutionAuthority = false)
    (hTransition : v.grantsMissionTransitionAuthority = false)
    (hContradiction : v.contradictionVisible = true) :
    p.proposalOnly = true ∧
      p.lowerEffectLicenseRequired = true ∧
      p.grantsExecutionAuthority = false ∧
      p.grantsToolAuthority = false ∧
      p.grantsTruthAuthority = false ∧
      p.grantsMemoryOverwriteAuthority = false ∧
      p.exactMissionBinding = true ∧
      p.exactBeliefBinding = true ∧
      p.finiteResourceEnvelope = true ∧
      v.plannerId ≠ v.verifierId ∧
      v.grantsExecutionAuthority = false ∧
      v.grantsMissionTransitionAuthority = false ∧
      v.contradictionVisible = true := by
  exact ⟨hProposal, hLicense, hPlanExecution, hPlanTool, hPlanTruth,
    hPlanMemory, hMission, hBelief, hFinite, hSeparate,
    hVerifyExecution, hTransition, hContradiction⟩

end SemanticPlannerVerifier

end KUOS.OpenHorizon
