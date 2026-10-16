import Mathlib
import KUOS.Architecture.QiWuxingAddConFirstIsomorphismV2_9

/-!
# Qi Wuxing phase-observation universal property v3.0

This append-only layer upgrades the v2.9 additive first-isomorphism statement
to a universal property.

The protected shift space remains

`WuxingShift = FivePhase × Nat`,

with additive phase projection

`phaseProjection : WuxingShift →+ FivePhase`.

An additive observation is phase-compatible when equality under
`phaseProjection` forces equality under the observation. Mathlib's `AddCon.lift`
and `AddCon.lift_unique` then give a unique additive map out of the quotient.
Using the canonical zero-history section, the same observation also factors
uniquely through `FivePhase` itself.

No negative history counts are introduced. The theorem concerns only a finite
architecture-level additive quotient and does not assert a physical gauge
quotient, causal hidden variable, biological dynamics, clinical validity, or
external theorem authority.
-/

namespace KUOS.Architecture

/-- An additive observation is phase-compatible when it identifies every pair
of protected shifts identified by phase projection. -/
def PhaseCompatibleAdditiveObservation
    {P : Type*} [AddZeroClass P]
    (obs : WuxingShift →+ P) : Prop :=
  AddCon.ker phaseProjection ≤ AddCon.ker obs

/-- Phase compatibility says exactly that the observation has equal values on
protected shifts with the same phase projection. -/
theorem phaseCompatibleAdditiveObservation_iff
    {P : Type*} [AddZeroClass P]
    (obs : WuxingShift →+ P) :
    PhaseCompatibleAdditiveObservation obs ↔
      ∀ first second : WuxingShift,
        SamePhaseShift first second → obs first = obs second := by
  constructor
  · intro h first second hsame
    have hphase : AddCon.ker phaseProjection first second :=
      (AddCon.ker_rel phaseProjection).2 hsame
    exact (AddCon.ker_rel obs).1 (h hphase)
  · intro h first second hphase
    apply (AddCon.ker_rel obs).2
    apply h first second
    exact (AddCon.ker_rel phaseProjection).1 hphase

/-- Canonical additive factor of a phase-compatible observation through the
v2.9 additive quotient. -/
def phaseObservationLift
    {P : Type*} [AddZeroClass P]
    (obs : WuxingShift →+ P)
    (h : PhaseCompatibleAdditiveObservation obs) :
    PhaseAddQuotient →+ P :=
  (AddCon.ker phaseProjection).lift obs h

/-- The quotient lift agrees with the original observation on every protected
shift representative. -/
@[simp] theorem phaseObservationLift_class
    {P : Type*} [AddZeroClass P]
    (obs : WuxingShift →+ P)
    (h : PhaseCompatibleAdditiveObservation obs)
    (shift : WuxingShift) :
    phaseObservationLift obs h (phaseAddClass shift) = obs shift := by
  change ((AddCon.ker phaseProjection).lift obs h)
      ((AddCon.ker phaseProjection).mk' shift) = obs shift
  exact AddCon.lift_mk' h shift

/-- The quotient lift composes with the canonical quotient map to recover the
original observation. -/
theorem phaseObservationLift_comp_class
    {P : Type*} [AddZeroClass P]
    (obs : WuxingShift →+ P)
    (h : PhaseCompatibleAdditiveObservation obs) :
    (phaseObservationLift obs h).comp phaseAddClass = obs := by
  change (((AddCon.ker phaseProjection).lift obs h).comp
      (AddCon.ker phaseProjection).mk') = obs
  exact AddCon.lift_comp_mk' h

/-- Uniqueness of the additive factor through the phase quotient. -/
theorem phaseObservationLift_unique
    {P : Type*} [AddZeroClass P]
    (obs : WuxingShift →+ P)
    (h : PhaseCompatibleAdditiveObservation obs)
    (lift : PhaseAddQuotient →+ P)
    (hlift : lift.comp phaseAddClass = obs) :
    lift = phaseObservationLift obs h := by
  change lift = (AddCon.ker phaseProjection).lift obs h
  apply AddCon.lift_unique h lift
  change lift.comp (AddCon.ker phaseProjection).mk' = obs at hlift
  exact hlift

/-- Universal property of the additive phase quotient: every phase-compatible
additive observation factors through the quotient in one and only one way. -/
theorem phaseAddQuotient_universal
    {P : Type*} [AddZeroClass P]
    (obs : WuxingShift →+ P)
    (h : PhaseCompatibleAdditiveObservation obs) :
    ∃! lift : PhaseAddQuotient →+ P,
      lift.comp phaseAddClass = obs := by
  refine ⟨phaseObservationLift obs h,
    phaseObservationLift_comp_class obs h, ?_⟩
  intro lift hlift
  exact phaseObservationLift_unique obs h lift hlift

/-- The canonical zero-history section is itself an additive homomorphism. It
serves only as a representative selector for the phase projection. -/
def phaseZeroHistorySectionHom : FivePhase →+ WuxingShift where
  toFun := phaseZeroHistorySection
  map_zero' := rfl
  map_add' _ _ := rfl

@[simp] theorem phaseZeroHistorySectionHom_apply (phase : FivePhase) :
    phaseZeroHistorySectionHom phase = (phase, 0) := rfl

/-- The additive zero-history section remains a right inverse of phase
projection. -/
@[simp] theorem phaseProjection_sectionHom (phase : FivePhase) :
    phaseProjection (phaseZeroHistorySectionHom phase) = phase := rfl

/-- Candidate phase-level factor obtained by evaluating an additive observation
on the canonical zero-history representative. -/
def phaseObservationFactor
    {P : Type*} [AddZeroClass P]
    (obs : WuxingShift →+ P) :
    FivePhase →+ P :=
  obs.comp phaseZeroHistorySectionHom

@[simp] theorem phaseObservationFactor_apply
    {P : Type*} [AddZeroClass P]
    (obs : WuxingShift →+ P)
    (phase : FivePhase) :
    phaseObservationFactor obs phase = obs (phase, 0) := rfl

/-- A phase-compatible additive observation is recovered by composing its
canonical phase-level factor with phase projection. -/
theorem phaseObservationFactor_comp_projection
    {P : Type*} [AddZeroClass P]
    (obs : WuxingShift →+ P)
    (h : PhaseCompatibleAdditiveObservation obs) :
    (phaseObservationFactor obs).comp phaseProjection = obs := by
  ext shift
  change obs ((phaseProjection shift, 0) : WuxingShift) = obs shift
  have hphase :
      AddCon.ker phaseProjection
        ((phaseProjection shift, 0) : WuxingShift) shift :=
    (AddCon.ker_rel phaseProjection).2 rfl
  exact (AddCon.ker_rel obs).1 (h hphase)

/-- Any additive factor through phase projection equals the canonical factor. -/
theorem phaseObservationFactor_unique
    {P : Type*} [AddZeroClass P]
    (obs : WuxingShift →+ P)
    (factor : FivePhase →+ P)
    (hfactor : factor.comp phaseProjection = obs) :
    factor = phaseObservationFactor obs := by
  ext phase
  have hpoint := DFunLike.congr_fun hfactor ((phase, 0) : WuxingShift)
  change factor phase = obs ((phase, 0) : WuxingShift) at hpoint
  change factor phase = obs ((phase, 0) : WuxingShift)
  exact hpoint

/-- Universal property in phase-space form: every phase-compatible additive
observation factors uniquely through `phaseProjection`. -/
theorem phaseProjection_universal
    {P : Type*} [AddZeroClass P]
    (obs : WuxingShift →+ P)
    (h : PhaseCompatibleAdditiveObservation obs) :
    ∃! factor : FivePhase →+ P,
      factor.comp phaseProjection = obs := by
  refine ⟨phaseObservationFactor obs,
    phaseObservationFactor_comp_projection obs h, ?_⟩
  intro factor hfactor
  exact phaseObservationFactor_unique obs factor hfactor

/-- Phase compatibility is equivalent to existence of an additive factor
through phase projection. -/
theorem phaseCompatibleAdditiveObservation_iff_exists_factor
    {P : Type*} [AddZeroClass P]
    (obs : WuxingShift →+ P) :
    PhaseCompatibleAdditiveObservation obs ↔
      ∃ factor : FivePhase →+ P,
        factor.comp phaseProjection = obs := by
  constructor
  · intro h
    exact ⟨phaseObservationFactor obs,
      phaseObservationFactor_comp_projection obs h⟩
  · rintro ⟨factor, hfactor⟩
    intro first second hphase
    apply (AddCon.ker_rel obs).2
    have hphaseEq : phaseProjection first = phaseProjection second :=
      (AddCon.ker_rel phaseProjection).1 hphase
    have hfirst := DFunLike.congr_fun hfactor first
    have hsecond := DFunLike.congr_fun hfactor second
    calc
      obs first = factor (phaseProjection first) := hfirst.symm
      _ = factor (phaseProjection second) := congrArg factor hphaseEq
      _ = obs second := hsecond

/-- Every phase-compatible additive observation identifies a phase-closed word
with the zero shift, even when the protected shift itself is nonzero. -/
theorem phaseCompatibleObservation_phaseClosedWord_eq_zero
    {P : Type*} [AddZeroClass P]
    (obs : WuxingShift →+ P)
    (h : PhaseCompatibleAdditiveObservation obs)
    (word : WuxingRelationWord)
    (hclosed : PhaseClosedWord word) :
    obs (relationWordShift word) = obs 0 := by
  have hclass := phaseClosedWord_addClass_eq_zero_class word hclosed
  calc
    obs (relationWordShift word) =
        phaseObservationLift obs h (phaseAddClass (relationWordShift word)) :=
      (phaseObservationLift_class obs h _).symm
    _ = phaseObservationLift obs h (phaseAddClass 0) :=
      congrArg (phaseObservationLift obs h) hclass
    _ = obs 0 := phaseObservationLift_class obs h 0

/-- Nonempty phase closure exhibits the universal observational information
loss while preserving the richer protected shift as nonzero. -/
theorem nonempty_phaseClosedWord_phaseCompatible_nonfaithful
    {P : Type*} [AddZeroClass P]
    (obs : WuxingShift →+ P)
    (h : PhaseCompatibleAdditiveObservation obs)
    (word : WuxingRelationWord)
    (hclosed : PhaseClosedWord word)
    (hword : word ≠ []) :
    obs (relationWordShift word) = obs 0 ∧
      relationWordShift word ≠ 0 := by
  exact ⟨phaseCompatibleObservation_phaseClosedWord_eq_zero
      obs h word hclosed,
    relationWordShift_ne_zero_of_nonempty word hword⟩

/-- The control-insult loop is invisible to every phase-compatible additive
observation while remaining a nonzero protected shift. -/
theorem control_insult_phaseCompatible_nonfaithful
    {P : Type*} [AddZeroClass P]
    (obs : WuxingShift →+ P)
    (h : PhaseCompatibleAdditiveObservation obs) :
    obs (relationWordShift [.control, .insult]) = obs 0 ∧
      relationWordShift [.control, .insult] ≠ 0 := by
  exact nonempty_phaseClosedWord_phaseCompatible_nonfaithful
    obs h [.control, .insult] control_insult_word_phase_closed (by simp)

/-- Every phase-compatible additive observation identifies control with two
generations, although their protected shifts remain distinct. -/
theorem control_two_generations_phaseCompatible_collision
    {P : Type*} [AddZeroClass P]
    (obs : WuxingShift →+ P)
    (h : PhaseCompatibleAdditiveObservation obs) :
    obs (relationWordShift [.control]) =
        obs (relationWordShift [.generation, .generation]) ∧
      relationWordShift [.control] ≠
        relationWordShift [.generation, .generation] := by
  constructor
  · have hclass :=
      control_two_generations_same_addQuotient_class_distinct_shift.1
    calc
      obs (relationWordShift [.control]) =
          phaseObservationLift obs h (phaseAddClass (relationWordShift [.control])) :=
        (phaseObservationLift_class obs h _).symm
      _ = phaseObservationLift obs h
          (phaseAddClass (relationWordShift [.generation, .generation])) :=
        congrArg (phaseObservationLift obs h) hclass
      _ = obs (relationWordShift [.generation, .generation]) :=
        phaseObservationLift_class obs h _
  · exact control_two_generations_same_addQuotient_class_distinct_shift.2

end KUOS.Architecture
