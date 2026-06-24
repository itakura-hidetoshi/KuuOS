import Mathlib
import KUOS.WORLD.KuuVacuumInformationGeometryBridgeV0_55

/-!
WORLD infinite diagonal Araki-Hessian bridge v0.56.

This file closes a genuine infinite-carrier model rather than adding another
analytic receipt.  The index type is infinite, the tangent core is the infinite
type of finitely supported real directions, and the Araki/Umegaki entropy is
realized on the commuting diagonal algebra.  Lean proves the scalar entropy
score, the mixed second variation at the faithful reference state, the BKM /
classical Fisher form, positivity, symmetry, and its standard-form weighted-L2
Gram representation.

The result is an exact theorem on the finite-support core of an infinite
diagonal von Neumann model.  It is not yet the noncommutative type-III local
algebra theorem and is not identified with the interacting four-dimensional
Yang-Mills realization.
-/

namespace KUOS
namespace WORLD

noncomputable section

open scoped BigOperators

/-- A faithful diagonal reference state over an infinite index type. -/
structure WorldInfiniteDiagonalArakiModel
    (ι : Type*) [DecidableEq ι] [Infinite ι] where
  referenceWeight : ι → ℝ
  referenceWeight_pos : ∀ i, 0 < referenceWeight i

namespace WorldInfiniteDiagonalArakiModel

variable {ι : Type*} [DecidableEq ι] [Infinite ι]
variable (A : WorldInfiniteDiagonalArakiModel ι)

/-- The finite-support tangent core remains an infinite carrier. -/
abbrev TangentCore := ι →₀ ℝ

/-- The scalar commuting Araki/Umegaki entropy integrand `p log (p/q)`. -/
def scalarArakiTerm (q p : ℝ) : ℝ :=
  p * Real.log (p / q)

/-- The scalar entropy score with respect to the first argument `p`. -/
def scalarArakiScore (q p : ℝ) : ℝ :=
  Real.log (p / q) + 1

/-- A finite-support diagonal entropy path through the reference state. -/
def diagonalArakiPath
    (s : Finset ι) (v : ι → ℝ) (t : ℝ) : ℝ :=
  ∑ i in s,
    scalarArakiTerm (A.referenceWeight i)
      (A.referenceWeight i + t * v i)

/-- The first variation in direction `v`, evaluated along direction `u`. -/
def diagonalFirstVariation
    (s : Finset ι) (u v : ι → ℝ) (r : ℝ) : ℝ :=
  ∑ i in s,
    v i * scalarArakiScore (A.referenceWeight i)
      (A.referenceWeight i + r * u i)

/-- The diagonal BKM, equivalently classical Fisher, bilinear form. -/
def diagonalBKMMetric
    (s : Finset ι) (u v : ι → ℝ) : ℝ :=
  ∑ i in s, u i * v i / A.referenceWeight i

/-- The weighted standard-form Gram expression for diagonal excitations. -/
def weightedExcitationGram
    (s : Finset ι) (u v : ι → ℝ) : ℝ :=
  ∑ i in s,
    A.referenceWeight i *
      (u i / A.referenceWeight i) *
      (v i / A.referenceWeight i)

/-- Total first-order mass of a tangent direction over the active support. -/
def tangentMass (s : Finset ι) (v : ι → ℝ) : ℝ :=
  ∑ i in s, v i

/-- The finite-support tangent core is an infinite type when the index is infinite. -/
theorem tangent_core_infinite : Infinite (TangentCore (ι := ι)) :=
  inferInstance

/-- Faithfulness gives nonzero reference weights. -/
theorem referenceWeight_ne_zero (i : ι) : A.referenceWeight i ≠ 0 :=
  ne_of_gt (A.referenceWeight_pos i)

/-- At the reference point, the scalar entropy derivative is exactly one. -/
theorem scalar_araki_term_hasDerivAt_reference
    (q : ℝ) (hq : q ≠ 0) :
    HasDerivAt (fun p : ℝ => scalarArakiTerm q p) 1 q := by
  have hlog :
      HasDerivAt (fun p : ℝ => Real.log (p / q))
        ((1 / q) / (q / q)) q :=
    ((hasDerivAt_id q).div_const q).log (div_ne_zero hq hq)
  have hmul := (hasDerivAt_id q).mul hlog
  simpa [scalarArakiTerm, hq] using hmul

/-- The derivative of the scalar score at the faithful reference is `q⁻¹`. -/
theorem scalar_araki_score_hasDerivAt_reference
    (q : ℝ) (hq : q ≠ 0) :
    HasDerivAt (fun p : ℝ => scalarArakiScore q p) (1 / q) q := by
  have hlog :
      HasDerivAt (fun p : ℝ => Real.log (p / q))
        ((1 / q) / (q / q)) q :=
    ((hasDerivAt_id q).div_const q).log (div_ne_zero hq hq)
  simpa [scalarArakiScore, hq] using hlog.add_const 1

/-- The affine perturbation `q + t u` has derivative `u`. -/
theorem affine_perturbation_hasDerivAt (q u : ℝ) :
    HasDerivAt (fun t : ℝ => q + t * u) u 0 := by
  simpa using ((hasDerivAt_id (0 : ℝ)).mul_const u).const_add q

/-- First derivative of the scalar entropy along a reference tangent. -/
theorem scalar_araki_path_hasDerivAt_reference
    (q u : ℝ) (hq : q ≠ 0) :
    HasDerivAt
      (fun t : ℝ => scalarArakiTerm q (q + t * u)) u 0 := by
  exact (scalar_araki_term_hasDerivAt_reference q hq).comp 0
    (affine_perturbation_hasDerivAt q u)

/-- The score along `q + r u` has derivative `u/q` at the reference. -/
theorem scalar_score_path_hasDerivAt_reference
    (q u : ℝ) (hq : q ≠ 0) :
    HasDerivAt
      (fun r : ℝ => scalarArakiScore q (q + r * u)) (u / q) 0 := by
  have h := (scalar_araki_score_hasDerivAt_reference q hq).comp 0
    (affine_perturbation_hasDerivAt q u)
  convert h using 1 <;> simp [div_eq_mul_inv, mul_comm]

/-- The mixed scalar Hessian is `u v / q`. -/
theorem scalar_mixed_hessian_hasDerivAt_reference
    (q u v : ℝ) (hq : q ≠ 0) :
    HasDerivAt
      (fun r : ℝ => v * scalarArakiScore q (q + r * u))
      (u * v / q) 0 := by
  have h := (scalar_score_path_hasDerivAt_reference q u hq).const_mul v
  convert h using 1 <;> ring

/-- The first entropy variation of a finite-support path is its total tangent mass. -/
theorem diagonal_araki_path_hasDerivAt_reference
    (s : Finset ι) (v : ι → ℝ) :
    HasDerivAt (A.diagonalArakiPath s v) (A.tangentMass s v) 0 := by
  unfold diagonalArakiPath tangentMass
  apply HasDerivAt.fun_sum
  intro i hi
  exact scalar_araki_path_hasDerivAt_reference
    (A.referenceWeight i) (v i) (A.referenceWeight_ne_zero i)

/-- Normalized tangent directions have vanishing first entropy variation. -/
theorem diagonal_araki_path_stationary_of_tangentMass_zero
    (s : Finset ι) (v : ι → ℝ)
    (hv : A.tangentMass s v = 0) :
    HasDerivAt (A.diagonalArakiPath s v) 0 0 := by
  simpa [hv] using A.diagonal_araki_path_hasDerivAt_reference s v

/-- Exact mixed second variation of diagonal Araki entropy on the infinite carrier. -/
theorem diagonal_firstVariation_hasDerivAt_reference
    (s : Finset ι) (u v : ι → ℝ) :
    HasDerivAt (A.diagonalFirstVariation s u v)
      (A.diagonalBKMMetric s u v) 0 := by
  unfold diagonalFirstVariation diagonalBKMMetric
  apply HasDerivAt.fun_sum
  intro i hi
  exact scalar_mixed_hessian_hasDerivAt_reference
    (A.referenceWeight i) (u i) (v i) (A.referenceWeight_ne_zero i)

/-- The diagonal BKM form is symmetric. -/
theorem diagonalBKMMetric_symmetric
    (s : Finset ι) (u v : ι → ℝ) :
    A.diagonalBKMMetric s u v = A.diagonalBKMMetric s v u := by
  unfold diagonalBKMMetric
  apply Finset.sum_congr rfl
  intro i hi
  ring

/-- The diagonal BKM quadratic form is nonnegative. -/
theorem diagonalBKMMetric_nonnegative
    (s : Finset ι) (u : ι → ℝ) :
    0 ≤ A.diagonalBKMMetric s u u := by
  unfold diagonalBKMMetric
  apply Finset.sum_nonneg
  intro i hi
  exact div_nonneg (mul_self_nonneg (u i))
    (le_of_lt (A.referenceWeight_pos i))

/-- The weighted standard-form excitation Gram form equals the BKM Hessian. -/
theorem weightedExcitationGram_eq_diagonalBKMMetric
    (s : Finset ι) (u v : ι → ℝ) :
    A.weightedExcitationGram s u v = A.diagonalBKMMetric s u v := by
  unfold weightedExcitationGram diagonalBKMMetric
  apply Finset.sum_congr rfl
  intro i hi
  field_simp [A.referenceWeight_ne_zero i]
  <;> ring

/-- The exact infinite diagonal package proved without analytic receipts. -/
theorem infinite_diagonal_araki_hessian_package
    (s : Finset ι) (u v : ι → ℝ) :
    HasDerivAt (A.diagonalFirstVariation s u v)
      (A.diagonalBKMMetric s u v) 0 ∧
    A.diagonalBKMMetric s u v = A.diagonalBKMMetric s v u ∧
    0 ≤ A.diagonalBKMMetric s u u ∧
    A.weightedExcitationGram s u v = A.diagonalBKMMetric s u v :=
  ⟨A.diagonal_firstVariation_hasDerivAt_reference s u v,
    A.diagonalBKMMetric_symmetric s u v,
    A.diagonalBKMMetric_nonnegative s u,
    A.weightedExcitationGram_eq_diagonalBKMMetric s u v⟩

end WorldInfiniteDiagonalArakiModel
end
end WORLD
end KUOS
