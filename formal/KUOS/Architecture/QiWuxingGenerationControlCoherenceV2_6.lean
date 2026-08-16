import Mathlib
import KUOS.Architecture.QiYinYangWuxingFibonacciHistoryGeometryV2_5

/-!
# Qi Wuxing generation-control coherence v2.6

This additive architecture layer keeps the v2.5 five-phase/Fibonacci-history
separation and adds relational Wuxing generation/control directions, a
nonnegative interaction-strength boundary, and an explicit composition
coherence law.

The mathematical reading is deliberately structural:

* generation is phase shift `+1` on `ZMod 5`;
* control is phase shift `+2`;
* insult/counter-control is the inverse phase direction `-2`;
* mother/child directions are `-1`/`+1`;
* every canonical relation is one interaction event in the protected
  Fibonacci history fibre;
* overacting is control direction plus excessive strength, not a distinct
  phase direction;
* equal phase endpoints do not imply equal protected histories;
* "middle" is represented by composition coherence, not by identifying a
  privileged Earth substance.

No historical identity between classical Wuxing and a physical gauge theory,
no physical anyon realization, no clinical threshold, and no treatment or
WORLD authority is claimed.
-/

namespace KUOS.Architecture

/-- Nonnegative interaction strength.  It classifies a relation but does not
supply an unvalidated physical or clinical dynamical law. -/
abbrev InteractionStrength := ℝ≥0

/-- A history-aware shift consists of a `Z5` phase displacement and a number of
protected Fibonacci-history interaction events. -/
abbrev WuxingShift := FivePhase × Nat

/-- Generation (`相生`) advances one phase. -/
def generationPhase (phase : FivePhase) : FivePhase := phase + 1

/-- Control (`相克`) advances two phases in the canonical five-phase order. -/
def controlPhase (phase : FivePhase) : FivePhase := phase + 2

/-- Insult/counter-control (`相侮`) is the inverse control direction. -/
def insultPhase (phase : FivePhase) : FivePhase := phase - 2

/-- Mother direction is one phase backward. -/
def motherPhase (phase : FivePhase) : FivePhase := phase - 1

/-- Child direction is one phase forward. -/
def childPhase (phase : FivePhase) : FivePhase := phase + 1

/-- Control and two generation steps have the same phase endpoint. -/
theorem generation_twice_phase_eq_control (phase : FivePhase) :
    generationPhase (generationPhase phase) = controlPhase phase := by
  simp [generationPhase, controlPhase]
  ring

/-- The insult direction is the inverse of control at the phase level. -/
@[simp] theorem insult_after_control_phase (phase : FivePhase) :
    insultPhase (controlPhase phase) = phase := by
  simp [insultPhase, controlPhase]

/-- Control is also the inverse of insult at the phase level. -/
@[simp] theorem control_after_insult_phase (phase : FivePhase) :
    controlPhase (insultPhase phase) = phase := by
  simp [insultPhase, controlPhase]

/-- Mother and child are inverse phase directions. -/
@[simp] theorem mother_after_child_phase (phase : FivePhase) :
    motherPhase (childPhase phase) = phase := by
  simp [motherPhase, childPhase]

/-- Child and mother are inverse phase directions. -/
@[simp] theorem child_after_mother_phase (phase : FivePhase) :
    childPhase (motherPhase phase) = phase := by
  simp [motherPhase, childPhase]

/-- Canonical relation labels.  Overacting is intentionally not a constructor:
it is control together with excessive strength. -/
inductive WuxingRelation where
  | generation
  | control
  | insult
  | mother
  | child
  deriving DecidableEq, Repr

/-- Each canonical relation is one protected-history interaction event.
The phase displacement and event count are intentionally separate. -/
def relationShift : WuxingRelation → WuxingShift
  | .generation => (1, 1)
  | .control => (2, 1)
  | .insult => (-2, 1)
  | .mother => (-1, 1)
  | .child => (1, 1)

/-- A weighted relation records classification strength without pretending that
strength alone supplies a validated physical or clinical dynamics. -/
structure WuxingInteraction where
  relation : WuxingRelation
  strength : InteractionStrength
  deriving Repr

/-- Apply a phase/history shift to the v2.5 state. -/
def applyShift (shift : WuxingShift)
    (state : WuxingFibonacciState) : WuxingFibonacciState :=
  ⟨state.phase + shift.1, advanceHistoryN shift.2 state.history⟩

/-- Apply a weighted relation.  Strength is preserved as classification
metadata; the state update is determined by the relation shift only. -/
def applyInteraction (interaction : WuxingInteraction)
    (state : WuxingFibonacciState) : WuxingFibonacciState :=
  applyShift (relationShift interaction.relation) state

/-- Iterated protected history respects addition of event counts. -/
theorem advanceHistoryN_add_v2_6
    (first second : Nat) (history : FibonacciHistory) :
    advanceHistoryN (first + second) history =
      advanceHistoryN second (advanceHistoryN first history) := by
  induction first generalizing history with
  | zero =>
      simp
  | succ first ih =>
      rw [Nat.succ_add]
      change
        advanceHistoryN (first + second) (advanceHistory history) =
          advanceHistoryN second
            (advanceHistoryN first (advanceHistory history))
      exact ih (history := advanceHistory history)

/-- The phase/history state action is coherent with addition of shifts. -/
theorem applyShift_add
    (first second : WuxingShift) (state : WuxingFibonacciState) :
    applyShift (first + second) state =
      applyShift second (applyShift first state) := by
  rcases first with ⟨firstPhase, firstHistory⟩
  rcases second with ⟨secondPhase, secondHistory⟩
  ext
  · simp [applyShift, add_assoc]
  · simp [applyShift, advanceHistoryN_add_v2_6]

/-- Coherence is a property of the relational action, not a sixth phase. -/
def WuxingCoherent (state : WuxingFibonacciState) : Prop :=
  ∀ first second : WuxingShift,
    applyShift (first + second) state =
      applyShift second (applyShift first state)

/-- Every v2.5 phase/history state satisfies the v2.6 composition coherence. -/
theorem wuxing_coherence (state : WuxingFibonacciState) :
    WuxingCoherent state := by
  intro first second
  exact applyShift_add first second state

/-- Pure phase projection cannot distinguish one control event from two
successive generation events. -/
theorem control_phase_projection_eq_two_generations :
    (relationShift .control).1 =
      (relationShift .generation + relationShift .generation).1 := by
  norm_num [relationShift]

/-- The protected-history shift does distinguish one control event from two
successive generation events. -/
theorem control_shift_ne_two_generation_shifts :
    relationShift .control ≠
      relationShift .generation + relationShift .generation := by
  intro h
  have hhistory := congrArg Prod.snd h
  norm_num [relationShift] at hhistory

/-- Control followed by insult returns the phase coordinate. -/
theorem control_then_insult_phase_returns (state : WuxingFibonacciState) :
    (applyShift (relationShift .insult)
      (applyShift (relationShift .control) state)).phase = state.phase := by
  simp [applyShift, relationShift]

/-- Phase cancellation does not erase history: control then insult records two
interaction events. -/
theorem control_then_insult_history_advances_twice
    (state : WuxingFibonacciState) :
    (applyShift (relationShift .insult)
      (applyShift (relationShift .control) state)).history =
        advanceHistoryN 2 state.history := by
  rfl

/-- The same non-erasure principle holds for child followed by mother. -/
theorem child_then_mother_phase_returns (state : WuxingFibonacciState) :
    (applyShift (relationShift .mother)
      (applyShift (relationShift .child) state)).phase = state.phase := by
  simp [applyShift, relationShift]

/-- Actual strength lies below the nominal relation strength. -/
def IsUnderStrength
    (nominal actual : InteractionStrength) : Prop := actual < nominal

/-- Actual strength equals the nominal relation strength. -/
def IsBalancedStrength
    (nominal actual : InteractionStrength) : Prop := actual = nominal

/-- Actual strength exceeds the nominal relation strength. -/
def IsOverStrength
    (nominal actual : InteractionStrength) : Prop := nominal < actual

/-- Linear order gives an exhaustive under/balanced/over classification. -/
theorem strength_trichotomy
    (nominal actual : InteractionStrength) :
    IsUnderStrength nominal actual ∨
      IsBalancedStrength nominal actual ∨
      IsOverStrength nominal actual := by
  simpa [IsUnderStrength, IsBalancedStrength, IsOverStrength] using
    (lt_trichotomy actual nominal)

/-- Canonical weighted control interaction. -/
def controlInteraction (strength : InteractionStrength) : WuxingInteraction :=
  ⟨.control, strength⟩

/-- Canonical weighted insult interaction. -/
def insultInteraction (strength : InteractionStrength) : WuxingInteraction :=
  ⟨.insult, strength⟩

/-- `相乗` is represented structurally as control direction with excessive
strength relative to an explicitly supplied nominal value. -/
def IsOveractingControl
    (nominal : InteractionStrength) (interaction : WuxingInteraction) : Prop :=
  interaction.relation = .control ∧
    IsOverStrength nominal interaction.strength

/-- A control interaction is overacting exactly when its strength is above the
supplied nominal value. -/
@[simp] theorem controlInteraction_overacting_iff
    (nominal actual : InteractionStrength) :
    IsOveractingControl nominal (controlInteraction actual) ↔ nominal < actual := by
  rfl

/-- `相侮` is a distinct inverse phase direction and is not encoded as negative
or excessive control strength. -/
theorem insultInteraction_not_overacting_control
    (nominal actual : InteractionStrength) :
    ¬ IsOveractingControl nominal (insultInteraction actual) := by
  simp [IsOveractingControl, insultInteraction]

/-- Receipt surface for the additive v2.6 architecture boundary. -/
structure WuxingGenerationControlCoherenceReceipt where
  v2_5DependencyVisible : Bool
  z5GenerationVisible : Bool
  z5ControlVisible : Bool
  insultInverseDirectionVisible : Bool
  motherChildDirectionsVisible : Bool
  nonnegativeStrengthVisible : Bool
  strengthTrichotomyVisible : Bool
  overactingIsExcessControlVisible : Bool
  fibonacciHistoryFibreVisible : Bool
  phaseHistorySeparationVisible : Bool
  compositionCoherenceVisible : Bool
  protectedHistoryPreserved : Bool
  twoTruthsGapPreserved : Bool
  centerIsCoherenceNotEarthSubstance : Bool
  strengthUsedAsClinicalThreshold : Bool
  overactingUsedAsClinicalDiagnosis : Bool
  classicalWuxingIdentifiedWithPhysicalGaugeTheory : Bool
  physicalAnyonRealizationClaimed : Bool
  grantsExecution : Bool
  grantsTruth : Bool
  grantsClinicalAuthority : Bool
  grantsTheoremAuthority : Bool
  overwritesMemory : Bool
  updatesExactWorld : Bool

/-- Valid receipts expose the mathematical structure and keep all authority and
reification boundaries closed. -/
structure WuxingGenerationControlCoherenceReceipt.Valid
    (receipt : WuxingGenerationControlCoherenceReceipt) : Prop where
  v2_5Dependency : receipt.v2_5DependencyVisible = true
  generation : receipt.z5GenerationVisible = true
  control : receipt.z5ControlVisible = true
  insultInverse : receipt.insultInverseDirectionVisible = true
  motherChild : receipt.motherChildDirectionsVisible = true
  nonnegativeStrength : receipt.nonnegativeStrengthVisible = true
  strengthTrichotomy : receipt.strengthTrichotomyVisible = true
  overactingBoundary : receipt.overactingIsExcessControlVisible = true
  fibonacciHistory : receipt.fibonacciHistoryFibreVisible = true
  phaseHistorySeparation : receipt.phaseHistorySeparationVisible = true
  coherence : receipt.compositionCoherenceVisible = true
  protectedHistory : receipt.protectedHistoryPreserved = true
  twoTruthsGap : receipt.twoTruthsGapPreserved = true
  middleAsCoherence : receipt.centerIsCoherenceNotEarthSubstance = true
  noClinicalThreshold : receipt.strengthUsedAsClinicalThreshold = false
  noClinicalDiagnosis : receipt.overactingUsedAsClinicalDiagnosis = false
  noGaugeIdentity : receipt.classicalWuxingIdentifiedWithPhysicalGaugeTheory = false
  noPhysicalAnyonClaim : receipt.physicalAnyonRealizationClaimed = false
  noExecutionAuthority : receipt.grantsExecution = false
  noTruthAuthority : receipt.grantsTruth = false
  noClinicalAuthority : receipt.grantsClinicalAuthority = false
  noTheoremAuthority : receipt.grantsTheoremAuthority = false
  noMemoryOverwrite : receipt.overwritesMemory = false
  noExactWorldUpdate : receipt.updatesExactWorld = false

namespace WuxingGenerationControlCoherenceReceipt

variable (receipt : WuxingGenerationControlCoherenceReceipt)

/-- A valid receipt preserves the positive mathematical surface. -/
theorem valid_preserves_structure
    (h : receipt.Valid) :
    receipt.z5GenerationVisible = true ∧
      receipt.z5ControlVisible = true ∧
      receipt.nonnegativeStrengthVisible = true ∧
      receipt.overactingIsExcessControlVisible = true ∧
      receipt.fibonacciHistoryFibreVisible = true ∧
      receipt.compositionCoherenceVisible = true ∧
      receipt.centerIsCoherenceNotEarthSubstance = true := by
  exact ⟨h.generation, h.control, h.nonnegativeStrength,
    h.overactingBoundary, h.fibonacciHistory, h.coherence,
    h.middleAsCoherence⟩

/-- A valid receipt grants no clinical, theorem, execution, truth, memory, or
WORLD authority. -/
theorem valid_grants_no_authority
    (h : receipt.Valid) :
    receipt.strengthUsedAsClinicalThreshold = false ∧
      receipt.overactingUsedAsClinicalDiagnosis = false ∧
      receipt.grantsExecution = false ∧
      receipt.grantsTruth = false ∧
      receipt.grantsClinicalAuthority = false ∧
      receipt.grantsTheoremAuthority = false ∧
      receipt.overwritesMemory = false ∧
      receipt.updatesExactWorld = false := by
  exact ⟨h.noClinicalThreshold, h.noClinicalDiagnosis,
    h.noExecutionAuthority, h.noTruthAuthority, h.noClinicalAuthority,
    h.noTheoremAuthority, h.noMemoryOverwrite, h.noExactWorldUpdate⟩

end WuxingGenerationControlCoherenceReceipt

end KUOS.Architecture
