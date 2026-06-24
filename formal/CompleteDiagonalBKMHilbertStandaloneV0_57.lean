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

theorem complete : CompleteSpace (H (ι := ι)) := inferInstance

theorem coordinateSeries (x : H (ι := ι)) :
    HasSum (fun i : ι => lp.single 2 i (x i)) x := by
  exact lp.hasSum_single (by norm_num) x

theorem coordinateInner (i : ι) (u v : ℝ) :
    metric (coordinate q i u) (coordinate q i v) = u * v / q i := by
  unfold metric coordinate
  rw [lp.inner_single_left, lp.single_apply_self]
  change
    (u / Real.sqrt (q i)) * (v / Real.sqrt (q i)) = u * v / q i
  calc
    (u / Real.sqrt (q i)) * (v / Real.sqrt (q i)) =
      (u * v) / (Real.sqrt (q i) * Real.sqrt (q i)) := by ring
    _ = u * v / q i := by
      rw [Real.mul_self_sqrt (le_of_lt (hq i))]

end CompleteDiagonalBKMHilbertStandaloneV0_57
