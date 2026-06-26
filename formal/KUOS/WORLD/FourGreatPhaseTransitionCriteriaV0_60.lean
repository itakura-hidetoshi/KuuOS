import Mathlib
import KUOS.WORLD.FourGreatPhaseDynamicsCoreV0_59

/-!
WORLD v0.60 phase-transition criteria.

This module separates the v0.59 four-great diagnostic from three independent
phase-transition witnesses: free-energy nonanalyticity, spectral-gap closure, and
fixed-point-algebra change. Stronger continuity and isolated-gap witnesses are
available separately and are not required by the basic declaration.
-/

namespace KUOS.WORLD

noncomputable section

structure WorldFourGreatCoordinateSnapshot where
  earth : ℝ
  water : ℝ
  fire : ℝ
  air : ℝ

namespace WorldFourGreatCoordinateSnapshot

def ofDiagnostic
    (d : WorldFourGreatCoreDiagnostic) : WorldFourGreatCoordinateSnapshot where
  earth := d.earth
  water := d.water
  fire := d.fire
  air := d.air

end WorldFourGreatCoordinateSnapshot

inductive WorldPhaseTransitionChannel where
  | freeEnergyNonanalyticity
  | spectralGapClosure
  | fixedPointAlgebraChange
  deriving DecidableEq, Repr

variable (𝕜 A : Type*)
variable [CommSemiring 𝕜] [Semiring A] [Algebra 𝕜 A]

/-- Order-theoretic classification of a fixed-point-subalgebra change. -/
inductive WorldFixedPointAlgebraChangeWitness
    (left right : Subalgebra 𝕜 A) : Prop where
  | enlargement (h : left < right)
  | reduction (h : right < left)
  | incomparable (hLR : ¬ left ≤ right) (hRL : ¬ right ≤ left)

namespace WorldFixedPointAlgebraChangeWitness

variable {𝕜 A}
variable {left right : Subalgebra 𝕜 A}

theorem ne (h : WorldFixedPointAlgebraChangeWitness 𝕜 A left right) :
    left ≠ right := by
  cases h with
  | enlargement hlt => exact ne_of_lt hlt
  | reduction hlt => exact ne_of_gt hlt
  | incomparable hLR _ =>
      intro hEq
      apply hLR
      simpa [hEq]

end WorldFixedPointAlgebraChangeWitness

structure WorldFourGreatPhaseTransitionSystem where
  fourGreatDiagnostic : ℝ → WorldFourGreatCoreDiagnostic
  freeEnergy : ℝ → ℝ
  spectralGap : ℝ → ℝ
  spectralGap_nonnegative : ∀ t, 0 ≤ spectralGap t
  fixedPointAlgebra : ℝ → Subalgebra 𝕜 A
  criterionIndependenceRequired : Prop
  criterionIndependenceRequiredProof : criterionIndependenceRequired
  declarationIsReadOnly : Prop
  declarationIsReadOnlyProof : declarationIsReadOnly
  declarationGrantsNoExecutionAuthority : Prop
  declarationGrantsNoExecutionAuthorityProof :
    declarationGrantsNoExecutionAuthority
  fourGreatChangeIsNotMaterialOntology : Prop
  fourGreatChangeIsNotMaterialOntologyProof :
    fourGreatChangeIsNotMaterialOntology

namespace WorldFourGreatPhaseTransitionSystem

variable {𝕜 A : Type*}
variable [CommSemiring 𝕜] [Semiring A] [Algebra 𝕜 A]
variable (System : WorldFourGreatPhaseTransitionSystem 𝕜 A)

/-- Basic thermodynamic witness: loss of real analyticity. -/
def freeEnergyNonanalyticAt (critical : ℝ) : Prop :=
  ¬ AnalyticAt ℝ System.freeEnergy critical

/-- Strengthened thermodynamic witness retaining continuity at the critical point. -/
def continuousFreeEnergyNonanalyticAt (critical : ℝ) : Prop :=
  ContinuousAt System.freeEnergy critical ∧
    System.freeEnergyNonanalyticAt critical

/-- Basic spectral witness: a continuous nonnegative gap vanishes at the critical point. -/
def spectralGapClosesAt (critical : ℝ) : Prop :=
  ContinuousAt System.spectralGap critical ∧
    System.spectralGap critical = 0

/-- Strengthened isolated closure: positive gap values occur arbitrarily nearby. -/
def isolatedSpectralGapClosesAt (critical : ℝ) : Prop :=
  System.spectralGapClosesAt critical ∧
    ∀ ε : ℝ, 0 < ε →
      ∃ t : ℝ,
        0 < |t - critical| ∧
        |t - critical| < ε ∧
        0 < System.spectralGap t

/-- The fixed-point subalgebra changes locally by enlargement, reduction, or incomparability. -/
def fixedPointAlgebraChangesAt (critical : ℝ) : Prop :=
  ∀ ε : ℝ, 0 < ε →
    ∃ left right : ℝ,
      critical - ε < left ∧
      left < critical ∧
      critical < right ∧
      right < critical + ε ∧
      WorldFixedPointAlgebraChangeWitness 𝕜 A
        (System.fixedPointAlgebra left)
        (System.fixedPointAlgebra right)

/-- The v0.59 diagnostic coordinates change across every critical neighbourhood. -/
def fourGreatCoordinatesChangeAt (critical : ℝ) : Prop :=
  ∀ ε : ℝ, 0 < ε →
    ∃ left right : ℝ,
      critical - ε < left ∧
      left < critical ∧
      critical < right ∧
      right < critical + ε ∧
      WorldFourGreatCoordinateSnapshot.ofDiagnostic
          (System.fourGreatDiagnostic left) ≠
        WorldFourGreatCoordinateSnapshot.ofDiagnostic
          (System.fourGreatDiagnostic right)

@[simp] theorem spectralGap_at_critical_eq_zero
    {critical : ℝ}
    (h : System.spectralGapClosesAt critical) :
    System.spectralGap critical = 0 :=
  h.2

theorem continuous_nonanalytic_implies_nonanalytic
    {critical : ℝ}
    (h : System.continuousFreeEnergyNonanalyticAt critical) :
    System.freeEnergyNonanalyticAt critical :=
  h.2

theorem isolated_gap_closure_implies_gap_closure
    {critical : ℝ}
    (h : System.isolatedSpectralGapClosesAt critical) :
    System.spectralGapClosesAt critical :=
  h.1

theorem spectralGap_nonnegative_at (t : ℝ) :
    0 ≤ System.spectralGap t :=
  System.spectralGap_nonnegative t

theorem boundary_package :
    System.criterionIndependenceRequired ∧
    System.declarationIsReadOnly ∧
    System.declarationGrantsNoExecutionAuthority ∧
    System.fourGreatChangeIsNotMaterialOntology :=
  ⟨System.criterionIndependenceRequiredProof,
    System.declarationIsReadOnlyProof,
    System.declarationGrantsNoExecutionAuthorityProof,
    System.fourGreatChangeIsNotMaterialOntologyProof⟩

end WorldFourGreatPhaseTransitionSystem

end
end KUOS.WORLD
