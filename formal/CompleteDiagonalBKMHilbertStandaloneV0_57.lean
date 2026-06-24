import Mathlib.Analysis.InnerProductSpace.l2Space

noncomputable section
open scoped BigOperators

namespace CompleteDiagonalBKMHilbertStandaloneV0_57

variable {ι : Type*} [DecidableEq ι] [Infinite ι]
variable (q : ι → ℝ) (hq : ∀ i, 0 < q i)

abbrev H := lp (fun _ : ι => ℝ) 2

def metric (x y : H (ι := ι)) : ℝ := inner ℝ x y

def coordinate (i : ι) (u : ℝ) : H (ι := ι) :=
  lp.single 2 i (u / Real.sqrt (q i))

end CompleteDiagonalBKMHilbertStandaloneV0_57
