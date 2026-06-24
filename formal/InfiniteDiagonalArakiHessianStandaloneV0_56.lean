import Mathlib

noncomputable section
open scoped BigOperators

namespace InfiniteDiagonalArakiHessianStandaloneV0_56

variable {ι : Type*} [DecidableEq ι] [Infinite ι]
variable (q : ι → ℝ) (hq : ∀ i, 0 < q i)

def scalarTerm (a p : ℝ) : ℝ := p * Real.log (p / a)
def scalarScore (a p : ℝ) : ℝ := Real.log (p / a) + 1

def firstVariation (s : Finset ι) (u v : ι → ℝ) (r : ℝ) : ℝ :=
  ∑ i in s, v i * scalarScore (q i) (q i + r * u i)

def bkm (s : Finset ι) (u v : ι → ℝ) : ℝ :=
  ∑ i in s, u i * v i / q i

theorem q_ne_zero (i : ι) : q i ≠ 0 := ne_of_gt (hq i)

theorem scalarTerm_hasDerivAt (a : ℝ) (ha : a ≠ 0) :
    HasDerivAt (fun p : ℝ => scalarTerm a p) 1 a := by
  have hlog :
      HasDerivAt (fun p : ℝ => Real.log (p / a))
        ((1 / a) / (a / a)) a :=
    ((hasDerivAt_id a).div_const a).log (div_ne_zero ha ha)
  have hmul := (hasDerivAt_id a).mul hlog
  simpa [scalarTerm, ha] using hmul

theorem scalarScore_hasDerivAt (a : ℝ) (ha : a ≠ 0) :
    HasDerivAt (fun p : ℝ => scalarScore a p) (1 / a) a := by
  have hlog :
      HasDerivAt (fun p : ℝ => Real.log (p / a))
        ((1 / a) / (a / a)) a :=
    ((hasDerivAt_id a).div_const a).log (div_ne_zero ha ha)
  simpa [scalarScore, ha] using hlog.add_const 1

theorem affine_hasDerivAt (a u : ℝ) :
    HasDerivAt (fun t : ℝ => a + t * u) u 0 := by
  simpa using ((hasDerivAt_id (0 : ℝ)).mul_const u).const_add a

theorem scorePath_hasDerivAt (a u : ℝ) (ha : a ≠ 0) :
    HasDerivAt (fun r : ℝ => scalarScore a (a + r * u)) (u / a) 0 := by
  have h := (scalarScore_hasDerivAt a ha).comp 0 (affine_hasDerivAt a u)
  convert h using 1 <;> simp [div_eq_mul_inv, mul_comm]

theorem scalarMixed_hasDerivAt (a u v : ℝ) (ha : a ≠ 0) :
    HasDerivAt
      (fun r : ℝ => v * scalarScore a (a + r * u))
      (u * v / a) 0 := by
  have h := (scorePath_hasDerivAt a u ha).const_mul v
  convert h using 1 <;> ring

theorem firstVariation_hasDerivAt (s : Finset ι) (u v : ι → ℝ) :
    HasDerivAt (firstVariation q s u v) (bkm q s u v) 0 := by
  unfold firstVariation bkm
  apply HasDerivAt.fun_sum
  intro i hi
  exact scalarMixed_hasDerivAt (q i) (u i) (v i) (q_ne_zero q hq i)

end InfiniteDiagonalArakiHessianStandaloneV0_56
