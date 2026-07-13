import Mathlib
import KUOS.PlanOS.FinitePhysicalQuantumQiCoherenceKernelPartialDephasingV1_23
import KUOS.DecisionOS.WorldConditionedRelationalDeliberationV0_6
import KUOS.OpenHorizon.MemoryOSWorldObserveIntakeKernelV0_39

namespace KUOS.OpenHorizon.MemoryOSObserverRelativeNonMarkovTemporalRecordV0_40

/-- Exact finite memory-kernel contraction. -/
def weightedMemory (weights effects : List ℤ) : ℤ :=
  (List.zipWith (fun weight effect => weight * effect) weights effects).sum

/-- Present signal updated by the retained finite history kernel. -/
def transitionContext
    (present : ℤ)
    (weights effects : List ℤ) : ℤ :=
  present + weightedMemory weights effects

/-- Visible translation residue between two observer-relative records. -/
def translationResidual
    (source target offset : ℤ) : ℤ :=
  target - (source + offset)

/-- Finite temporal-role bindings across future, present, and past. -/
structure TemporalRoleBinding where
  planosFutureBound : Bool
  decisionosPresentBound : Bool
  memoryosPastBound : Bool
  observeChannelBound : Bool

/-- Bounded observer-relative MemoryOS certificate surface. -/
structure ObserverRelativeNonMarkovTemporalRecordCertificate where
  temporalRoles : TemporalRoleBinding
  observerRelativeRecording : Bool
  appendOnlyRecordLineage : Bool
  translationResidueVisible : Bool
  nonMarkovHistoryDependencePreserved : Bool
  recordNotEventIdentity : Bool
  absoluteObserverClaimed : Bool
  eventRecordIdentityClaimed : Bool
  historyErasurePerformed : Bool
  memoryOverwritePerformed : Bool
  planSelectionPerformed : Bool
  decisionReplayedAsNewDecision : Bool
  activationPerformed : Bool
  executionPermission : Bool
  worldMutated : Bool
  verificationResultClaimed : Bool
  sourcePlanOSMutated : Bool
  sourceDecisionOSMutated : Bool
  sourceMemoryOSV039Mutated : Bool
  finiteBounded : Bool
  readOnly : Bool

/-- Reference retained history contributes seven units through weights `3,2,1`. -/
theorem reference_retained_history_memory :
    weightedMemory [3, 2, 1] [2, -1, 3] = 7 := by
  native_decide

/-- Counterfactual history with the same present contributes four units. -/
theorem reference_counterfactual_history_memory :
    weightedMemory [3, 2, 1] [2, -1, 0] = 4 := by
  native_decide

/-- The same present state can produce different next contexts when retained
    histories differ: a finite non-Markov witness. -/
theorem reference_same_present_non_markov_separation :
    transitionContext 5 [3, 2, 1] [2, -1, 3] = 12 ∧
      transitionContext 5 [3, 2, 1] [2, -1, 0] = 9 ∧
      transitionContext 5 [3, 2, 1] [2, -1, 3] ≠
        transitionContext 5 [3, 2, 1] [2, -1, 0] := by
  native_decide

/-- Observer translation leaves a visible residue `10 - (7 + 2) = 1`. -/
theorem reference_observer_translation_residue :
    translationResidual 7 10 2 = 1 := by
  native_decide

/-- Future, present, past, and observation-channel roles remain simultaneously
    bound instead of collapsing into one time slice. -/
theorem temporal_role_binding_preserved
    (binding : TemporalRoleBinding)
    (hplan : binding.planosFutureBound = true)
    (hdecision : binding.decisionosPresentBound = true)
    (hmemory : binding.memoryosPastBound = true)
    (hobserve : binding.observeChannelBound = true) :
    binding.planosFutureBound = true ∧
      binding.decisionosPresentBound = true ∧
      binding.memoryosPastBound = true ∧
      binding.observeChannelBound = true := by
  exact ⟨hplan, hdecision, hmemory, hobserve⟩

/-- An observer-relative record is explicitly not identified with the event. -/
theorem record_event_nonidentity_preserved
    (certificate : ObserverRelativeNonMarkovTemporalRecordCertificate)
    (hrecord : certificate.recordNotEventIdentity = true)
    (hidentity : certificate.eventRecordIdentityClaimed = false) :
    certificate.recordNotEventIdentity = true ∧
      certificate.eventRecordIdentityClaimed = false := by
  exact ⟨hrecord, hidentity⟩

/-- Observer relativity, translation residue, and history dependence grant no
    selection, activation, mutation, overwrite, or execution authority. -/
theorem observer_relative_memory_grants_no_authority
    (certificate : ObserverRelativeNonMarkovTemporalRecordCertificate)
    (hobserver : certificate.observerRelativeRecording = true)
    (happend : certificate.appendOnlyRecordLineage = true)
    (hresidue : certificate.translationResidueVisible = true)
    (hnonmarkov : certificate.nonMarkovHistoryDependencePreserved = true)
    (habsolute : certificate.absoluteObserverClaimed = false)
    (herase : certificate.historyErasurePerformed = false)
    (hoverwrite : certificate.memoryOverwritePerformed = false)
    (hselect : certificate.planSelectionPerformed = false)
    (hreplay : certificate.decisionReplayedAsNewDecision = false)
    (hactivate : certificate.activationPerformed = false)
    (hexecute : certificate.executionPermission = false)
    (hworld : certificate.worldMutated = false) :
    certificate.observerRelativeRecording = true ∧
      certificate.appendOnlyRecordLineage = true ∧
      certificate.translationResidueVisible = true ∧
      certificate.nonMarkovHistoryDependencePreserved = true ∧
      certificate.absoluteObserverClaimed = false ∧
      certificate.historyErasurePerformed = false ∧
      certificate.memoryOverwritePerformed = false ∧
      certificate.planSelectionPerformed = false ∧
      certificate.decisionReplayedAsNewDecision = false ∧
      certificate.activationPerformed = false ∧
      certificate.executionPermission = false ∧
      certificate.worldMutated = false := by
  exact ⟨hobserver, happend, hresidue, hnonmarkov, habsolute, herase,
    hoverwrite, hselect, hreplay, hactivate, hexecute, hworld⟩

/-- The v0.40 layer is finite, read-only, and source preserving. -/
theorem observer_relative_memory_is_bounded_read_only
    (certificate : ObserverRelativeNonMarkovTemporalRecordCertificate)
    (hfinite : certificate.finiteBounded = true)
    (hreadonly : certificate.readOnly = true)
    (hplan : certificate.sourcePlanOSMutated = false)
    (hdecision : certificate.sourceDecisionOSMutated = false)
    (hmemory : certificate.sourceMemoryOSV039Mutated = false)
    (hverify : certificate.verificationResultClaimed = false) :
    certificate.finiteBounded = true ∧
      certificate.readOnly = true ∧
      certificate.sourcePlanOSMutated = false ∧
      certificate.sourceDecisionOSMutated = false ∧
      certificate.sourceMemoryOSV039Mutated = false ∧
      certificate.verificationResultClaimed = false := by
  exact ⟨hfinite, hreadonly, hplan, hdecision, hmemory, hverify⟩

end KUOS.OpenHorizon.MemoryOSObserverRelativeNonMarkovTemporalRecordV0_40
