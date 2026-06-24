import Mathlib.Analysis.InnerProductSpace.l2Space
import KUOS.WORLD.InfiniteDiagonalArakiHessianBridgeV0_56

namespace KUOS
namespace WORLD

noncomputable section

open scoped BigOperators

namespace WorldInfiniteDiagonalArakiModel

variable {ι : Type*} [DecidableEq ι] [Infinite ι]
variable (A : WorldInfiniteDiagonalArakiModel ι)

abbrev CompleteTangent := lp (fun _ : ι => ℝ) 2

def completeBKMMetric (x y : A.CompleteTangent) : ℝ :=
  inner ℝ x y

def coordinateExcitation (i : ι) (u : ℝ) : A.CompleteTangent :=
  lp.single 2 i (u / Real.sqrt (A.referenceWeight i))

theorem completeTangent_complete : CompleteSpace A.CompleteTangent :=
  inferInstance

theorem completeBKMMetric_symmetric (x y : A.CompleteTangent) :
    A.completeBKMMetric x y = A.completeBKMMetric y x := by
  unfold completeBKMMetric
  exact real_inner_comm x y

theorem completeBKMMetric_nonnegative (x : A.CompleteTangent) :
    0 ≤ A.completeBKMMetric x x := by
  unfold completeBKMMetric
  exact real_inner_self_nonneg

theorem completeBKMMetric_eq_zero_iff (x : A.CompleteTangent) :
    A.completeBKMMetric x x = 0 ↔ x = 0 := by
  unfold completeBKMMetric
  rw [real_inner_self_eq_norm_sq]
  constructor
  · intro h
    exact norm_eq_zero.mp (sq_eq_zero_iff.mp h)
  · intro h
    simp [h]

theorem completeBKMMetric_eq_tsum (x y : A.CompleteTangent) :
    A.completeBKMMetric x y =
      ∑' i : ι, inner ℝ (x i) (y i) := by
  unfold completeBKMMetric
  exact lp.inner_eq_tsum x y

theorem completeTangent_hasSum_coordinates (x : A.CompleteTangent) :
    HasSum (fun i : ι => lp.single 2 i (x i)) x := by
  exact lp.hasSum_single (by norm_num) x

theorem coordinateExcitation_inner (i : ι) (u v : ℝ) :
    A.completeBKMMetric
        (A.coordinateExcitation i u)
        (A.coordinateExcitation i v) =
      u * v / A.referenceWeight i := by
  unfold completeBKMMetric coordinateExcitation
  rw [lp.inner_single_left, lp.single_apply_self]
  change
    (u / Real.sqrt (A.referenceWeight i)) *
        (v / Real.sqrt (A.referenceWeight i)) =
      u * v / A.referenceWeight i
  calc
    (u / Real.sqrt (A.referenceWeight i)) *
        (v / Real.sqrt (A.referenceWeight i)) =
      (u * v) /
        (Real.sqrt (A.referenceWeight i) *
          Real.sqrt (A.referenceWeight i)) := by ring
    _ = u * v / A.referenceWeight i := by
      rw [Real.mul_self_sqrt (le_of_lt (A.referenceWeight_pos i))]

theorem diagonalBKMMetric_eq_coordinateGramSum
    (s : Finset ι) (u v : ι → ℝ) :
    A.diagonalBKMMetric s u v =
      ∑ i in s,
        A.completeBKMMetric
          (A.coordinateExcitation i (u i))
          (A.coordinateExcitation i (v i)) := by
  unfold diagonalBKMMetric
  apply Finset.sum_congr rfl
  intro i hi
  exact (A.coordinateExcitation_inner i (u i) (v i)).symm

theorem diagonal_firstVariation_hasDerivAt_completeBKM
    (s : Finset ι) (u v : ι → ℝ) :
    HasDerivAt (A.diagonalFirstVariation s u v)
      (∑ i in s,
        A.completeBKMMetric
          (A.coordinateExcitation i (u i))
          (A.coordinateExcitation i (v i))) 0 := by
  rw [← A.diagonalBKMMetric_eq_coordinateGramSum s u v]
  exact A.diagonal_firstVariation_hasDerivAt_reference s u v

theorem complete_diagonal_bkm_hilbert_package
    (s : Finset ι) (u v : ι → ℝ) (x : A.CompleteTangent) :
    HasSum (fun i : ι => lp.single 2 i (x i)) x ∧
    0 ≤ A.completeBKMMetric x x ∧
    A.diagonalBKMMetric s u v =
      ∑ i in s,
        A.completeBKMMetric
          (A.coordinateExcitation i (u i))
          (A.coordinateExcitation i (v i)) ∧
    HasDerivAt (A.diagonalFirstVariation s u v)
      (∑ i in s,
        A.completeBKMMetric
          (A.coordinateExcitation i (u i))
          (A.coordinateExcitation i (v i))) 0 :=
  ⟨A.completeTangent_hasSum_coordinates x,
    A.completeBKMMetric_nonnegative x,
    A.diagonalBKMMetric_eq_coordinateGramSum s u v,
    A.diagonal_firstVariation_hasDerivAt_completeBKM s u v⟩

end WorldInfiniteDiagonalArakiModel
end
end WORLD
end KUOS
