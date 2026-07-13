import Mathlib
import KUOS.OpenHorizon.MemoryOSObserverRelativeNonMarkovTemporalRecordV0_40
import KUOS.PlanOS.FinitePhysicalQuantumQiCoherenceKernelPartialDephasingV1_23

namespace KUOS.OpenHorizon.MemoryOSObserverRelativeFiniteWindowQiInfluencePlanOSHandoffV0_41

/-- Exact finite component contraction for one PlanOS history coupling. -/
def componentDot (couplings effects : List ℤ) : ℤ :=
  (List.zipWith (fun coupling effect => coupling * effect) couplings effects).sum

/-- Lag-weighted contraction of a finite observer-relative memory window. -/
def weightedWindow
    (lagWeights : List ℤ)
    (windowEffects : List (List ℤ))
    (couplings : List ℤ) : ℤ :=
  (List.zipWith
    (fun lag effects => lag * componentDot couplings effects)
    lagWeights windowEffects).sum

/-- Full finite-window influence with a visible residue for the discarded tail. -/
def historyInfluence
    (lagWeights : List ℤ)
    (windowEffects : List (List ℤ))
    (couplings tailResidue : List ℤ) : ℤ :=
  weightedWindow lagWeights windowEffects couplings +
    componentDot couplings tailResidue

/-- Action obtained by using only the retained suffix window. -/
def windowOnlyAction
    (baseAction : ℤ)
    (lagWeights : List ℤ)
    (windowEffects : List (List ℤ))
    (couplings : List ℤ) : ℤ :=
  baseAction + weightedWindow lagWeights windowEffects couplings

/-- PlanOS advisory action after finite-window and tail-residue conditioning. -/
def conditionedAction
    (baseAction : ℤ)
    (lagWeights : List ℤ)
    (windowEffects : List (List ℤ))
    (couplings tailResidue : List ℤ) : ℤ :=
  baseAction + historyInfluence lagWeights windowEffects couplings tailResidue

/-- The reference suffix window contributes exactly `34`. -/
theorem reference_weighted_window_influence :
    weightedWindow
      [3, 2]
      [[1, 0, 0, 2, 0, 0, 0, 0, 1],
       [0, 1, -1, 0, 1, 0, 0, 0, 2]]
      [1, 2, 1, 1, 1, -1, 2, 1, 3] = 34 := by
  native_decide

/-- The exact discarded-tail residue contributes `9`; it is not erased. -/
theorem reference_discarded_tail_influence :
    componentDot
      [1, 2, 1, 1, 1, -1, 2, 1, 3]
      [0, 0, 0, 0, 1, 0, 1, 0, 2] = 9 := by
  native_decide

/-- The full influence is `43` and changes the base action `11` to `54`. -/
theorem reference_full_history_influence_and_action :
    historyInfluence
        [3, 2]
        [[1, 0, 0, 2, 0, 0, 0, 0, 1],
         [0, 1, -1, 0, 1, 0, 0, 0, 2]]
        [1, 2, 1, 1, 1, -1, 2, 1, 3]
        [0, 0, 0, 0, 1, 0, 1, 0, 2] = 43 ∧
      conditionedAction
        11
        [3, 2]
        [[1, 0, 0, 2, 0, 0, 0, 0, 1],
         [0, 1, -1, 0, 1, 0, 0, 0, 2]]
        [1, 2, 1, 1, 1, -1, 2, 1, 3]
        [0, 0, 0, 0, 1, 0, 1, 0, 2] = 54 := by
  native_decide

/-- The visible tail contribution is exactly the difference between the full
    history-conditioned action and the window-only action. -/
theorem tail_contribution_is_exact_difference
    (baseAction : ℤ)
    (lagWeights : List ℤ)
    (windowEffects : List (List ℤ))
    (couplings tailResidue : List ℤ) :
    conditionedAction baseAction lagWeights windowEffects couplings tailResidue -
        windowOnlyAction baseAction lagWeights windowEffects couplings =
      componentDot couplings tailResidue := by
  unfold conditionedAction windowOnlyAction historyInfluence
  ring

/-- A nonzero discarded-tail residue prevents the finite suffix window from
    being identified with a Markov replacement of the complete history. -/
theorem nonzero_tail_prevents_markov_reduction
    (baseAction : ℤ)
    (lagWeights : List ℤ)
    (windowEffects : List (List ℤ))
    (couplings tailResidue : List ℤ)
    (htail : componentDot couplings tailResidue ≠ 0) :
    conditionedAction baseAction lagWeights windowEffects couplings tailResidue ≠
      windowOnlyAction baseAction lagWeights windowEffects couplings := by
  intro heq
  have hdiff := tail_contribution_is_exact_difference
    baseAction lagWeights windowEffects couplings tailResidue
  rw [heq] at hdiff
  have hzero : componentDot couplings tailResidue = 0 := by
    simpa using hdiff.symm
  exact htail hzero

/-- Bounded bridge surface from MemoryOS v0.40 to the future-only PlanOS intake. -/
structure ObserverRelativeFiniteWindowQiInfluencePlanOSHandoffCertificate where
  sourceMemoryOSV040Bound : Bool
  sourcePlanOSV123Bound : Bool
  observerRelativeRecordsPreserved : Bool
  finiteWindowProjection : Bool
  discardedTailResidueVisible : Bool
  nonMarkovRootReplaced : Bool
  allPlanOSHistoriesRetained : Bool
  historyPruningPerformed : Bool
  historyRankingPerformed : Bool
  representativeHistorySelected : Bool
  planSelectionPerformed : Bool
  decisionCommitPerformed : Bool
  activationPerformed : Bool
  executionPermission : Bool
  sourceMemoryOSV040Mutated : Bool
  sourcePlanOSV123Mutated : Bool
  persistentWorldStateMutated : Bool
  verificationResultClaimed : Bool
  truthAuthorityGranted : Bool
  futureOnlyAdvisoryHandoff : Bool
  readOnly : Bool

/-- The handoff preserves the MemoryOS source, the complete PlanOS support, and
    the visible discarded tail without selecting or pruning a history. -/
theorem handoff_preserves_history_and_planos_support
    (certificate : ObserverRelativeFiniteWindowQiInfluencePlanOSHandoffCertificate)
    (hmemory : certificate.sourceMemoryOSV040Bound = true)
    (hplan : certificate.sourcePlanOSV123Bound = true)
    (hobserver : certificate.observerRelativeRecordsPreserved = true)
    (hwindow : certificate.finiteWindowProjection = true)
    (htail : certificate.discardedTailResidueVisible = true)
    (hreplace : certificate.nonMarkovRootReplaced = false)
    (hall : certificate.allPlanOSHistoriesRetained = true)
    (hprune : certificate.historyPruningPerformed = false)
    (hrank : certificate.historyRankingPerformed = false)
    (hrepresentative : certificate.representativeHistorySelected = false) :
    certificate.sourceMemoryOSV040Bound = true ∧
      certificate.sourcePlanOSV123Bound = true ∧
      certificate.observerRelativeRecordsPreserved = true ∧
      certificate.finiteWindowProjection = true ∧
      certificate.discardedTailResidueVisible = true ∧
      certificate.nonMarkovRootReplaced = false ∧
      certificate.allPlanOSHistoriesRetained = true ∧
      certificate.historyPruningPerformed = false ∧
      certificate.historyRankingPerformed = false ∧
      certificate.representativeHistorySelected = false := by
  exact ⟨hmemory, hplan, hobserver, hwindow, htail, hreplace, hall, hprune,
    hrank, hrepresentative⟩

/-- Influence calculation grants no selection, commit, activation, execution,
    mutation, verification, or truth authority. -/
theorem handoff_grants_no_authority
    (certificate : ObserverRelativeFiniteWindowQiInfluencePlanOSHandoffCertificate)
    (hselect : certificate.planSelectionPerformed = false)
    (hdecision : certificate.decisionCommitPerformed = false)
    (hactivate : certificate.activationPerformed = false)
    (hexecute : certificate.executionPermission = false)
    (hmemory : certificate.sourceMemoryOSV040Mutated = false)
    (hplan : certificate.sourcePlanOSV123Mutated = false)
    (hworld : certificate.persistentWorldStateMutated = false)
    (hverify : certificate.verificationResultClaimed = false)
    (htruth : certificate.truthAuthorityGranted = false)
    (hfuture : certificate.futureOnlyAdvisoryHandoff = true)
    (hreadonly : certificate.readOnly = true) :
    certificate.planSelectionPerformed = false ∧
      certificate.decisionCommitPerformed = false ∧
      certificate.activationPerformed = false ∧
      certificate.executionPermission = false ∧
      certificate.sourceMemoryOSV040Mutated = false ∧
      certificate.sourcePlanOSV123Mutated = false ∧
      certificate.persistentWorldStateMutated = false ∧
      certificate.verificationResultClaimed = false ∧
      certificate.truthAuthorityGranted = false ∧
      certificate.futureOnlyAdvisoryHandoff = true ∧
      certificate.readOnly = true := by
  exact ⟨hselect, hdecision, hactivate, hexecute, hmemory, hplan, hworld,
    hverify, htruth, hfuture, hreadonly⟩

end KUOS.OpenHorizon.MemoryOSObserverRelativeFiniteWindowQiInfluencePlanOSHandoffV0_41
