import Mathlib
import KUOS.WORLD.FourGreatPhaseDynamicsCoreV0_59

/-!
WORLD v0.60 phase-transition criteria.

This module separates the v0.59 four-great diagnostic from three independent
phase-transition witnesses: free-energy nonanalyticity, spectral-gap closure, and
fixed-point-algebra change.
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

/-- The free energy is continuous but not analytic at the critical parameter. -/
def freeEnergyNonanalyticAt (critical : ℝ) : Prop :=
  ContinuousAt System.freeEnergy critical ∧
    ¬ AnalyticAt ℝ System.freeEnergy critical

/-- The nonnegative gap continuously closes and is positive arbitrarily nearby. -/
def spectralGapClosesAt (critical : ℝ) : Prop :=
  ContinuousAt System.spectralGap critical ∧
    System.spectralGap critical = 0 ∧
      ∀ ε : ℝ, 0 < ε →
        ∃ t : ℝ,
          0 < |t - critical| ∧
          |t - critical| < ε ∧
          0 < System.spectralGap t

/-- The supplied fixed-point subalgebra changes across every critical neighbourhood. -/
def fixedPointAlgebraChangesAt (critical : ℝ) : Prop :=
  ∀ ε : ℝ, 0 < ε →
    ∃ left right : ℝ,
      critical - ε < left ∧
      left < critical ∧
      critical < right ∧
      right < critical + ε ∧
      System.fixedPointAlgebra left ≠ System.fixedPointAlgebra right

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
  h.2.1

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
