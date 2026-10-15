import Mathlib
import KUOS.Architecture.QiWuxingPhaseProjectionQuotientKernelV2_8

/-!
# Qi Wuxing additive-congruence first isomorphism v2.9

This append-only layer upgrades the v2.8 observational phase quotient from a
set-level quotient to Mathlib's additive-congruence quotient.

The protected shift space remains

`WuxingShift = FivePhase × Nat`.

Because the history coordinate is `Nat`, this is an additive monoid rather than
an additive group.  Accordingly, this layer uses `AddCon.ker phaseProjection`,
the kernel congruence available for additive monoids, rather than introducing
artificial negative history counts.

Mathlib's additive-monoid first isomorphism theorem then identifies the quotient
by equality under phase projection with `FivePhase` as an additive structure.
This is a finite algebraic statement internal to the KuuOS architecture model.
It is not a physical gauge quotient and grants no clinical, execution, WORLD,
truth, or external theorem authority.
-/

namespace KUOS.Architecture

/-- Additive congruence induced by equality after phase projection. -/
def phaseProjectionAddCon : AddCon WuxingShift :=
  AddCon.ker phaseProjection

/-- The Mathlib additive-congruence relation is exactly the v2.8 phase
observational equivalence. -/
@[simp] theorem phaseProjectionAddCon_rel
    (first second : WuxingShift) :
    phaseProjectionAddCon first second ↔ SamePhaseShift first second := by
  simp [phaseProjectionAddCon, SamePhaseShift]

/-- The v2.8 zero-fibre kernel is exactly congruence with the zero protected
shift in the Mathlib additive kernel congruence. -/
@[simp] theorem phaseProjectionKernel_iff_addCon_zero
    (shift : WuxingShift) :
    PhaseProjectionKernel shift ↔ phaseProjectionAddCon shift 0 := by
  simp [PhaseProjectionKernel, phaseProjectionAddCon]

/-- Additive quotient of protected shifts by equality of phase projection. -/
abbrev PhaseAddQuotient := (AddCon.ker phaseProjection).Quotient

/-- Canonical additive quotient map. -/
def phaseAddClass : WuxingShift →+ PhaseAddQuotient :=
  (AddCon.ker phaseProjection).mk'

/-- Every phase has a canonical representative with zero protected-history
count.  This is a section only for the phase projection; it does not erase or
invert actual history counts. -/
def phaseZeroHistorySection (phase : FivePhase) : WuxingShift :=
  (phase, 0)

/-- The zero-history phase representative is a right inverse to phase
projection. -/
theorem phaseZeroHistorySection_rightInverse :
    Function.RightInverse phaseZeroHistorySection phaseProjection := by
  intro phase
  rfl

/-- Additive-monoid first isomorphism theorem for phase observation.

The quotient by the kernel congruence of phase projection is additively
isomorphic to the five-phase displacement space. -/
def phaseAddQuotientEquiv : PhaseAddQuotient ≃+ FivePhase :=
  AddCon.quotientKerEquivOfRightInverse
    phaseProjection phaseZeroHistorySection
    phaseZeroHistorySection_rightInverse

/-- The first-isomorphism map sends a protected shift class to its phase
projection. -/
@[simp] theorem phaseAddQuotientEquiv_class (shift : WuxingShift) :
    phaseAddQuotientEquiv (phaseAddClass shift) = phaseProjection shift := by
  simp [phaseAddQuotientEquiv, phaseAddClass]

/-- Equality in the additive quotient is exactly equality after phase
projection. -/
theorem phaseAddClass_eq_iff
    (first second : WuxingShift) :
    phaseAddClass first = phaseAddClass second ↔
      phaseProjection first = phaseProjection second := by
  constructor
  · intro h
    have hphase := congrArg phaseAddQuotientEquiv h
    simpa using hphase
  · intro hphase
    apply phaseAddQuotientEquiv.injective
    simpa using hphase

/-- Equality with the zero quotient class is exactly the v2.8 zero-fibre
kernel predicate. -/
theorem phaseAddClass_eq_zero_class_iff_kernel (shift : WuxingShift) :
    phaseAddClass shift = phaseAddClass 0 ↔ PhaseProjectionKernel shift := by
  rw [phaseAddClass_eq_iff]
  simp [PhaseProjectionKernel]

/-- Every phase-closed relation word becomes the zero class in the additive
phase quotient. -/
theorem phaseClosedWord_addClass_eq_zero_class
    (word : WuxingRelationWord) (hclosed : PhaseClosedWord word) :
    phaseAddClass (relationWordShift word) = phaseAddClass 0 := by
  apply (phaseAddClass_eq_zero_class_iff_kernel _).2
  exact phaseClosedWord_shift_mem_kernel word hclosed

/-- A nonempty phase-closed word can become the zero observational class while
remaining a nonzero protected shift. -/
theorem nonempty_phaseClosedWord_addQuotient_nonfaithful
    (word : WuxingRelationWord)
    (hclosed : PhaseClosedWord word)
    (hword : word ≠ []) :
    phaseAddClass (relationWordShift word) = phaseAddClass 0 ∧
      relationWordShift word ≠ 0 := by
  exact ⟨phaseClosedWord_addClass_eq_zero_class word hclosed,
    relationWordShift_ne_zero_of_nonempty word hword⟩

/-- The canonical control-insult loop is zero in the additive phase quotient
but nonzero in protected-shift space. -/
theorem control_insult_addQuotient_zero_nonzero_shift :
    phaseAddClass (relationWordShift [.control, .insult]) = phaseAddClass 0 ∧
      relationWordShift [.control, .insult] ≠ 0 := by
  exact nonempty_phaseClosedWord_addQuotient_nonfaithful
    [.control, .insult] control_insult_word_phase_closed (by simp)

/-- The v2.7/v2.8 control-versus-two-generations collision is now equality in
an additive quotient, while the original protected shifts remain distinct. -/
theorem control_two_generations_same_addQuotient_class_distinct_shift :
    phaseAddClass (relationWordShift [.control]) =
        phaseAddClass (relationWordShift [.generation, .generation]) ∧
      relationWordShift [.control] ≠
        relationWordShift [.generation, .generation] := by
  constructor
  · apply (phaseAddClass_eq_iff _ _).2
    exact control_word_two_generations_same_phase_distinct_shift.1
  · exact control_word_two_generations_same_phase_distinct_shift.2

end KUOS.Architecture
