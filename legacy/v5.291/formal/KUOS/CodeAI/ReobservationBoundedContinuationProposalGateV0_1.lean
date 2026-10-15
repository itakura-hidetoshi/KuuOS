import Mathlib

namespace KUOS.CodeAI.ReobservationBoundedContinuationProposalGateV0_1

inductive ActionKind
  | observeRepository
  | inspectArtifact
  | runReadOnlyCheck
  | runFormalVerification
  deriving DecidableEq, Repr

structure Binding where
  repository : String
  sourceCommit : String
  predecessorManifest : String
  predecessorPack : String
  predecessorReceipt : String
  selectedSpecialist : String
  environmentCapsule : String
  progressTrace : String
  deriving DecidableEq, Repr

structure Query where
  binding : Binding
  continuationRound : Nat
  deriving DecidableEq, Repr

structure Budget where
  totalSteps : Nat
  totalToolCalls : Nat
  totalModelCalls : Nat
  totalTokenUnits : Nat
  totalWallClockMs : Nat
  totalFailedActions : Nat
  deriving DecidableEq, Repr

structure MeasuredUsage where
  steps : Nat
  toolCalls : Nat
  modelCalls : Nat
  tokenUnits : Nat
  wallClockMs : Nat
  failedActions : Nat
  deriving DecidableEq, Repr

structure ContinuationProposal where
  continuationRound : Nat
  actionCount : Nat
  actionKind : ActionKind
  requestedSteps : Nat
  requestedToolCalls : Nat
  requestedModelCalls : Nat
  requestedTokenUnits : Nat
  requestedWallClockMs : Nat
  requestedFailedActions : Nat
  grounded : Bool
  readOnly : Bool
  observableReturn : Bool
  newCheckpoint : Bool
  predecessorGateReentry : Bool
  selfReportOnly : Bool
  continuationAuthority : Bool
  executionAuthority : Bool
  repositoryMutation : Bool
  gitAuthority : Bool
  correctnessClaim : Bool
  deriving DecidableEq, Repr

structure GateEvidence where
  exactBinding : Bool
  predecessorDecisionAdmitted : Bool
  predecessorHintOnly : Bool
  predecessorTraceGrounded : Bool
  predecessorCapsuleReproducible : Bool
  predecessorLivelockFree : Bool
  predecessorEfficient : Bool
  predecessorAuthorityFree : Bool
  deriving DecidableEq, Repr

def PredecessorAdmitted (e : GateEvidence) : Prop :=
  e.predecessorDecisionAdmitted = true ∧
  e.predecessorHintOnly = true ∧
  e.predecessorTraceGrounded = true ∧
  e.predecessorCapsuleReproducible = true ∧
  e.predecessorLivelockFree = true ∧
  e.predecessorEfficient = true ∧
  e.predecessorAuthorityFree = true

def ProposalBounded (q : Query) (p : ContinuationProposal) : Prop :=
  p.continuationRound = q.continuationRound ∧
  p.actionCount = 1 ∧
  p.requestedSteps = 1 ∧
  p.grounded = true ∧
  p.readOnly = true ∧
  p.selfReportOnly = false

def ResidualSufficient (b : Budget) (m : MeasuredUsage) (p : ContinuationProposal) : Prop :=
  m.steps + p.requestedSteps ≤ b.totalSteps ∧
  m.toolCalls + p.requestedToolCalls ≤ b.totalToolCalls ∧
  m.modelCalls + p.requestedModelCalls ≤ b.totalModelCalls ∧
  m.tokenUnits + p.requestedTokenUnits ≤ b.totalTokenUnits ∧
  m.wallClockMs + p.requestedWallClockMs ≤ b.totalWallClockMs ∧
  m.failedActions + p.requestedFailedActions ≤ b.totalFailedActions

def ObservableReturn (p : ContinuationProposal) : Prop :=
  p.observableReturn = true ∧
  p.newCheckpoint = true ∧
  p.predecessorGateReentry = true

def BoundaryPreserved (p : ContinuationProposal) : Prop :=
  p.continuationAuthority = false ∧
  p.executionAuthority = false ∧
  p.repositoryMutation = false ∧
  p.gitAuthority = false ∧
  p.correctnessClaim = false

def GateAdmitted
    (q : Query)
    (expected : Binding)
    (b : Budget)
    (m : MeasuredUsage)
    (e : GateEvidence)
    (p : ContinuationProposal) : Prop :=
  q.binding = expected ∧
  e.exactBinding = true ∧
  PredecessorAdmitted e ∧
  ProposalBounded q p ∧
  ResidualSufficient b m p ∧
  ObservableReturn p ∧
  BoundaryPreserved p

theorem admitted_exact_binding
    {q : Query} {expected : Binding} {b : Budget} {m : MeasuredUsage}
    {e : GateEvidence} {p : ContinuationProposal}
    (h : GateAdmitted q expected b m e p) :
    q.binding = expected :=
  h.1

theorem admitted_predecessor
    {q : Query} {expected : Binding} {b : Budget} {m : MeasuredUsage}
    {e : GateEvidence} {p : ContinuationProposal}
    (h : GateAdmitted q expected b m e p) :
    PredecessorAdmitted e :=
  h.2.2.1

theorem admitted_proposal_bounded
    {q : Query} {expected : Binding} {b : Budget} {m : MeasuredUsage}
    {e : GateEvidence} {p : ContinuationProposal}
    (h : GateAdmitted q expected b m e p) :
    ProposalBounded q p :=
  h.2.2.2.1

theorem admitted_residual_sufficient
    {q : Query} {expected : Binding} {b : Budget} {m : MeasuredUsage}
    {e : GateEvidence} {p : ContinuationProposal}
    (h : GateAdmitted q expected b m e p) :
    ResidualSufficient b m p :=
  h.2.2.2.2.1

theorem admitted_observable_return
    {q : Query} {expected : Binding} {b : Budget} {m : MeasuredUsage}
    {e : GateEvidence} {p : ContinuationProposal}
    (h : GateAdmitted q expected b m e p) :
    ObservableReturn p :=
  h.2.2.2.2.2.1

theorem admitted_boundary_preserved
    {q : Query} {expected : Binding} {b : Budget} {m : MeasuredUsage}
    {e : GateEvidence} {p : ContinuationProposal}
    (h : GateAdmitted q expected b m e p) :
    BoundaryPreserved p :=
  h.2.2.2.2.2.2

theorem repository_mismatch_forbids_admission
    {q : Query} {expected : Binding} {b : Budget} {m : MeasuredUsage}
    {e : GateEvidence} {p : ContinuationProposal}
    (h : q.binding ≠ expected) :
    ¬ GateAdmitted q expected b m e p := by
  intro admitted
  exact h admitted.1

theorem held_predecessor_forbids_admission
    {q : Query} {expected : Binding} {b : Budget} {m : MeasuredUsage}
    {e : GateEvidence} {p : ContinuationProposal}
    (h : e.predecessorDecisionAdmitted = false) :
    ¬ GateAdmitted q expected b m e p := by
  simp [GateAdmitted, PredecessorAdmitted, h]

theorem multiple_actions_forbid_admission
    {q : Query} {expected : Binding} {b : Budget} {m : MeasuredUsage}
    {e : GateEvidence} {p : ContinuationProposal}
    (h : p.actionCount ≠ 1) :
    ¬ GateAdmitted q expected b m e p := by
  intro admitted
  exact h (admitted_proposal_bounded admitted).2.1

theorem mutating_action_forbids_admission
    {q : Query} {expected : Binding} {b : Budget} {m : MeasuredUsage}
    {e : GateEvidence} {p : ContinuationProposal}
    (h : p.readOnly = false) :
    ¬ GateAdmitted q expected b m e p := by
  simp [GateAdmitted, ProposalBounded, h]

theorem missing_reobservation_forbids_admission
    {q : Query} {expected : Binding} {b : Budget} {m : MeasuredUsage}
    {e : GateEvidence} {p : ContinuationProposal}
    (h : p.observableReturn = false) :
    ¬ GateAdmitted q expected b m e p := by
  simp [GateAdmitted, ObservableReturn, h]

theorem self_report_only_forbids_admission
    {q : Query} {expected : Binding} {b : Budget} {m : MeasuredUsage}
    {e : GateEvidence} {p : ContinuationProposal}
    (h : p.selfReportOnly = true) :
    ¬ GateAdmitted q expected b m e p := by
  simp [GateAdmitted, ProposalBounded, h]

theorem token_budget_excess_forbids_admission
    {q : Query} {expected : Binding} {b : Budget} {m : MeasuredUsage}
    {e : GateEvidence} {p : ContinuationProposal}
    (h : b.totalTokenUnits < m.tokenUnits + p.requestedTokenUnits) :
    ¬ GateAdmitted q expected b m e p := by
  intro admitted
  exact (Nat.not_le_of_lt h) (admitted_residual_sufficient admitted).2.2.2.1

def referenceBinding : Binding where
  repository := "itakura-hidetoshi/KuuOS"
  sourceCommit := "2944084ee7d415993f35c2bb8551c4fe83ee443d"
  predecessorManifest := "c24224d427dca0529e9a4aaee1e69da44c95800fc99f763e15500f53f7f0104d"
  predecessorPack := "e0b8aeea1179a999317e1a0092940c3cb062644c366e0a1700219d35f98debb8"
  predecessorReceipt := "51e921bc13bd9a25ae7d7bae34e786e4c4e52d8377a29fe43e60b8b5100ef439"
  selectedSpecialist := "specialist-formal-001"
  environmentCapsule := "60bec0429b6d113e1fffc3f4e7a98eaed0cc650ebf6a3ba884ba574342fb5be0"
  progressTrace := "9ea48de292b513393fa2ef91de33b93eb6c86e315304345f66b88362777f8755"

def referenceQuery : Query where
  binding := referenceBinding
  continuationRound := 1

def referenceBudget : Budget where
  totalSteps := 8
  totalToolCalls := 12
  totalModelCalls := 8
  totalTokenUnits := 60000
  totalWallClockMs := 1800000
  totalFailedActions := 0

def referenceMeasured : MeasuredUsage where
  steps := 6
  toolCalls := 9
  modelCalls := 6
  tokenUnits := 46000
  wallClockMs := 1380000
  failedActions := 0

def referenceEvidence : GateEvidence where
  exactBinding := true
  predecessorDecisionAdmitted := true
  predecessorHintOnly := true
  predecessorTraceGrounded := true
  predecessorCapsuleReproducible := true
  predecessorLivelockFree := true
  predecessorEfficient := true
  predecessorAuthorityFree := true

def referenceProposal : ContinuationProposal where
  continuationRound := 1
  actionCount := 1
  actionKind := .runFormalVerification
  requestedSteps := 1
  requestedToolCalls := 1
  requestedModelCalls := 1
  requestedTokenUnits := 7000
  requestedWallClockMs := 180000
  requestedFailedActions := 0
  grounded := true
  readOnly := true
  observableReturn := true
  newCheckpoint := true
  predecessorGateReentry := true
  selfReportOnly := false
  continuationAuthority := false
  executionAuthority := false
  repositoryMutation := false
  gitAuthority := false
  correctnessClaim := false

def referenceHeldEvidence : GateEvidence :=
  { referenceEvidence with predecessorDecisionAdmitted := false }

def referenceMutatingProposal : ContinuationProposal :=
  { referenceProposal with readOnly := false }

def referenceOverBudgetProposal : ContinuationProposal :=
  { referenceProposal with requestedTokenUnits := 15000 }

def referenceMissingReobservationProposal : ContinuationProposal :=
  { referenceProposal with observableReturn := false }

def referenceSelfReportProposal : ContinuationProposal :=
  { referenceProposal with selfReportOnly := true }

theorem reference_admitted :
    GateAdmitted referenceQuery referenceBinding referenceBudget referenceMeasured
      referenceEvidence referenceProposal := by
  simp [
    GateAdmitted,
    PredecessorAdmitted,
    ProposalBounded,
    ResidualSufficient,
    ObservableReturn,
    BoundaryPreserved,
    referenceQuery,
    referenceBinding,
    referenceBudget,
    referenceMeasured,
    referenceEvidence,
    referenceProposal
  ]

theorem reference_held_predecessor_not_admitted :
    ¬ GateAdmitted referenceQuery referenceBinding referenceBudget referenceMeasured
      referenceHeldEvidence referenceProposal := by
  simp [
    GateAdmitted,
    PredecessorAdmitted,
    referenceHeldEvidence,
    referenceEvidence
  ]

theorem reference_mutating_not_admitted :
    ¬ GateAdmitted referenceQuery referenceBinding referenceBudget referenceMeasured
      referenceEvidence referenceMutatingProposal := by
  simp [
    GateAdmitted,
    ProposalBounded,
    referenceMutatingProposal,
    referenceProposal
  ]

theorem reference_over_budget_not_admitted :
    ¬ GateAdmitted referenceQuery referenceBinding referenceBudget referenceMeasured
      referenceEvidence referenceOverBudgetProposal := by
  simp [
    GateAdmitted,
    ResidualSufficient,
    referenceBudget,
    referenceMeasured,
    referenceOverBudgetProposal,
    referenceProposal
  ]

theorem reference_missing_reobservation_not_admitted :
    ¬ GateAdmitted referenceQuery referenceBinding referenceBudget referenceMeasured
      referenceEvidence referenceMissingReobservationProposal := by
  simp [
    GateAdmitted,
    ObservableReturn,
    referenceMissingReobservationProposal,
    referenceProposal
  ]

theorem reference_self_report_not_admitted :
    ¬ GateAdmitted referenceQuery referenceBinding referenceBudget referenceMeasured
      referenceEvidence referenceSelfReportProposal := by
  simp [
    GateAdmitted,
    ProposalBounded,
    referenceSelfReportProposal,
    referenceProposal
  ]

end KUOS.CodeAI.ReobservationBoundedContinuationProposalGateV0_1
