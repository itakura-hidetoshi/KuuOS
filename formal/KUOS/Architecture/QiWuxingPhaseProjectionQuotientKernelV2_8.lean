import Mathlib
import KUOS.Architecture.QiWuxingRelationWordProtectedHistoryV2_7

/-!
# Qi Wuxing phase-projection quotient/kernel v2.8

This append-only layer makes precise the information loss already exhibited in
v2.7.  The protected shift space is

`WuxingShift = FivePhase × Nat`.

Projection to the phase coordinate is an additive homomorphism.  Its kernel
contains nonzero protected-history shifts, so the phase projection is not
injective.  Equality after phase projection therefore defines a genuine
observational quotient of the richer protected shift space.

The quotient is equivalent, as a type, to `FivePhase`: it remembers exactly the
phase coordinate and forgets the protected-history coordinate.  This is a
finite algebraic statement inside the KuuOS architecture model.  It is not a
physical gauge quotient, does not identify history with a substance, and grants
no clinical, execution, WORLD, truth, or external theorem authority.
-/

namespace KUOS.Architecture

/-- Forget protected history and retain only the five-phase displacement. -/
def phaseProjection : WuxingShift →+ FivePhase where
  toFun shift := shift.1
  map_zero' := rfl
  map_add' _ _ := rfl

@[simp] theorem phaseProjection_apply (shift : WuxingShift) :
    phaseProjection shift = shift.1 := rfl

/-- The phase projection is onto: every phase displacement has a protected
shift representative with zero history count. -/
theorem phaseProjection_surjective : Function.Surjective phaseProjection := by
  intro phase
  exact ⟨(phase, 0), rfl⟩

/-- Kernel membership is exactly vanishing phase displacement. -/
@[simp] theorem mem_phaseProjection_ker_iff (shift : WuxingShift) :
    shift ∈ phaseProjection.ker ↔ shift.1 = 0 := by
  rfl

/-- Every phase-closed relation word lands in the kernel of phase projection. -/
theorem phaseClosedWord_shift_mem_kernel
    (word : WuxingRelationWord) (hclosed : PhaseClosedWord word) :
    relationWordShift word ∈ phaseProjection.ker := by
  simpa [PhaseClosedWord] using hclosed

/-- A nonempty phase-closed word gives a nonzero kernel element: phase closure
is not protected-history erasure. -/
theorem nonempty_phaseClosedWord_nonzero_kernel
    (word : WuxingRelationWord)
    (hclosed : PhaseClosedWord word)
    (hword : word ≠ []) :
    relationWordShift word ∈ phaseProjection.ker ∧
      relationWordShift word ≠ 0 := by
  exact ⟨phaseClosedWord_shift_mem_kernel word hclosed,
    relationWordShift_ne_zero_of_nonempty word hword⟩

/-- The canonical control-insult loop is a concrete nonzero kernel element. -/
theorem control_insult_nonzero_kernel :
    relationWordShift [.control, .insult] ∈ phaseProjection.ker ∧
      relationWordShift [.control, .insult] ≠ 0 := by
  exact nonempty_phaseClosedWord_nonzero_kernel
    [.control, .insult] control_insult_word_phase_closed (by simp)

/-- Phase projection is non-faithful on protected shifts. -/
theorem phaseProjection_not_injective :
    ¬ Function.Injective phaseProjection := by
  intro hinjective
  have hsame :
      phaseProjection (relationWordShift [.control, .insult]) =
        phaseProjection 0 := by
    simpa [PhaseClosedWord] using control_insult_word_phase_closed
  exact control_insult_word_shift_ne_zero (hinjective hsame)

/-- Two protected shifts are phase-equivalent when phase projection cannot
distinguish them. -/
def SamePhaseShift (first second : WuxingShift) : Prop :=
  phaseProjection first = phaseProjection second

/-- Phase equivalence is preserved by addition of protected shifts. -/
theorem samePhaseShift_add
    {first₁ first₂ second₁ second₂ : WuxingShift}
    (hfirst : SamePhaseShift first₁ first₂)
    (hsecond : SamePhaseShift second₁ second₂) :
    SamePhaseShift (first₁ + second₁) (first₂ + second₂) := by
  change phaseProjection (first₁ + second₁) =
    phaseProjection (first₂ + second₂)
  simp only [map_add]
  rw [hfirst, hsecond]

/-- Setoid induced by equality after phase projection. -/
def phaseShiftSetoid : Setoid WuxingShift where
  r := SamePhaseShift
  iseqv := by
    constructor
    · intro shift
      rfl
    · intro first second h
      exact h.symm
    · intro first second third h₁ h₂
      exact h₁.trans h₂

/-- Observational quotient obtained by forgetting protected history. -/
def PhaseShiftQuotient := Quotient phaseShiftSetoid

/-- Quotient class of a protected shift. -/
def phaseClass (shift : WuxingShift) : PhaseShiftQuotient :=
  Quotient.mk phaseShiftSetoid shift

/-- The phase coordinate descends to the observational quotient. -/
def quotientPhase : PhaseShiftQuotient → FivePhase :=
  Quotient.lift
    (fun shift : WuxingShift => phaseProjection shift)
    (by
      intro first second h
      simpa [phaseShiftSetoid, SamePhaseShift] using h)

@[simp] theorem quotientPhase_phaseClass (shift : WuxingShift) :
    quotientPhase (phaseClass shift) = phaseProjection shift := rfl

/-- Two protected shifts have the same quotient class exactly when their phase
projections agree. -/
theorem phaseClass_eq_iff
    (first second : WuxingShift) :
    phaseClass first = phaseClass second ↔
      phaseProjection first = phaseProjection second := by
  constructor
  · intro h
    have hphase := congrArg quotientPhase h
    simpa using hphase
  · intro h
    apply Quotient.sound
    change phaseProjection first = phaseProjection second
    exact h

/-- The phase quotient remembers exactly `FivePhase` and no protected-history
coordinate. -/
def phaseQuotientEquiv : PhaseShiftQuotient ≃ FivePhase where
  toFun := quotientPhase
  invFun phase := phaseClass (phase, 0)
  left_inv := by
    intro quotient
    refine Quotient.inductionOn quotient ?_
    intro shift
    apply Quotient.sound
    change phaseProjection ((phaseProjection shift, 0) : WuxingShift) =
      phaseProjection shift
    rfl
  right_inv := by
    intro phase
    rfl

/-- Kernel membership is exactly equality with the zero class in the phase
quotient. -/
theorem phaseClass_eq_zero_iff_mem_kernel (shift : WuxingShift) :
    phaseClass shift = phaseClass 0 ↔ shift ∈ phaseProjection.ker := by
  rw [phaseClass_eq_iff]
  rfl

/-- Equal phase endpoints of relation words are precisely equality of their
protected shifts after quotienting by phase observation. -/
theorem relationWords_same_phase_same_class
    (first second : WuxingRelationWord)
    (hphase :
      (relationWordShift first).1 = (relationWordShift second).1) :
    phaseClass (relationWordShift first) =
      phaseClass (relationWordShift second) := by
  apply (phaseClass_eq_iff _ _).2
  exact hphase

/-- The v2.7 control-versus-two-generations example is an explicit quotient
collision: equal phase class, distinct protected shifts. -/
theorem control_two_generations_quotient_collision :
    phaseClass (relationWordShift [.control]) =
        phaseClass (relationWordShift [.generation, .generation]) ∧
      relationWordShift [.control] ≠
        relationWordShift [.generation, .generation] := by
  constructor
  · exact relationWords_same_phase_same_class
      [.control] [.generation, .generation]
      control_word_two_generations_same_phase_distinct_shift.1
  · exact control_word_two_generations_same_phase_distinct_shift.2

end KUOS.Architecture
