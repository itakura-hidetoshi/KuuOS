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

end InfiniteDiagonalArakiHessianStandaloneV0_56
