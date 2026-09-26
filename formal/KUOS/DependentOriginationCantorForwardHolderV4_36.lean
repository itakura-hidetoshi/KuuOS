import KUOS.DependentOriginationCantorCodingPrefixV4_35
import Mathlib.Topology.MetricSpace.HausdorffDimension
import Mathlib.Topology.MetricSpace.Holder
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Analysis.SpecialFunctions.Pow.NNReal
import Mathlib

namespace KUOS.DependentOriginationCantorForwardHolderV4_36

open MeasureTheory
open KUOS.DependentOriginationBinaryCantorHausdorffDimensionV4_33
open KUOS.DependentOriginationCantorCriticalExponentV4_34
open KUOS.DependentOriginationCantorCodingPrefixV4_35

set_option autoImplicit false

noncomputable section

attribute [local instance] PiNat.metricSpace

/-!
# Forward Hölder transport from binary Cantor space to the real Cantor set v4.36

v4.35 fixes the canonical binary-to-ternary coding and proves the common-prefix
estimate

  common prefix of length n
    -> dist(F x, F y) <= 3^(-n).

The PiNat metric on binary streams satisfies, for distinct streams whose first
difference is at n,

  dist(x,y) = 2^(-n).

The critical exponent for the forward coding is therefore

  alpha = log_2 3,

because

  (2^(-n))^alpha = 3^(-n).

This unit formalizes that scale identity, proves that the canonical coding is
(1, alpha)-Hölder, and derives the upper Hausdorff-dimension bound for the
classical real Cantor set.
-/

/-- Hölder exponent for the forward binary-to-ternary coding. -/
noncomputable def binaryToTernaryHolderExponent : NNReal :=
  ⟨Real.logb 2 3,
    (le_of_lt
      (lt_trans (by norm_num : (0 : ℝ) < 1)
        one_lt_logb_two_three))⟩

@[simp] theorem binaryToTernaryHolderExponent_coe :
    (binaryToTernaryHolderExponent : ℝ) = Real.logb 2 3 := by
  rfl

theorem binaryToTernaryHolderExponent_pos :
    0 < binaryToTernaryHolderExponent := by
  change (0 : ℝ) < Real.logb 2 3
  exact
    lt_trans (by norm_num : (0 : ℝ) < 1)
      one_lt_logb_two_three

/-- The forward exponent is reciprocal to the Cantor critical exponent. -/
theorem binaryToTernaryHolderExponent_inv :
    binaryToTernaryHolderExponent⁻¹ = cantorCriticalExponent := by
  apply NNReal.eq
  change (Real.logb 2 3)⁻¹ = cantorCriticalExponentReal
  exact inv_logb_two_three_eq_cantorCriticalExponent

/-- The base binary scale raised to the forward Hölder exponent is exactly the
base ternary scale. -/
theorem one_half_rpow_binaryToTernaryHolderExponent :
    (1 / 2 : ℝ) ^ (binaryToTernaryHolderExponent : ℝ) =
      (1 / 3 : ℝ) := by
  change (1 / 2 : ℝ) ^ Real.logb 2 3 = (1 / 3 : ℝ)
  calc
    (1 / 2 : ℝ) ^ Real.logb 2 3 =
        ((2 : ℝ)⁻¹) ^ Real.logb 2 3 := by
      rw [one_div]
    _ = ((2 : ℝ) ^ Real.logb 2 3)⁻¹ := by
      exact
        Real.inv_rpow
          (by norm_num : (0 : ℝ) ≤ 2)
          (Real.logb 2 3)
    _ = (3 : ℝ)⁻¹ := by
      rw [Real.rpow_logb (b := 2) (x := 3)
        (by norm_num : (0 : ℝ) < 2)
        (by norm_num : (2 : ℝ) ≠ 1)
        (by norm_num : (0 : ℝ) < 3)]
    _ = (1 / 3 : ℝ) := by
      rw [one_div]

/-- Exact scale conversion at every finite binary prefix depth. -/
theorem binaryScale_rpow_holderExponent
    (n : Nat) :
    ((1 / 2 : ℝ) ^ n) ^ (binaryToTernaryHolderExponent : ℝ) =
      (1 / 3 : ℝ) ^ n := by
  calc
    ((1 / 2 : ℝ) ^ n) ^ (binaryToTernaryHolderExponent : ℝ) =
        (((1 / 2 : ℝ) ^ (binaryToTernaryHolderExponent : ℝ)) ^ n) := by
      exact
        (Real.rpow_pow_comm
          (by norm_num : (0 : ℝ) ≤ 1 / 2)
          (binaryToTernaryHolderExponent : ℝ)
          n).symm
    _ = (1 / 3 : ℝ) ^ n := by
      rw [one_half_rpow_binaryToTernaryHolderExponent]

/-- Real-distance form of the global forward Hölder estimate. -/
theorem binaryToTernaryCantor_dist_le_rpow
    (x y : BinaryCantorSpace) :
    dist (binaryToTernaryCantor x) (binaryToTernaryCantor y) ≤
      dist x y ^ (binaryToTernaryHolderExponent : ℝ) := by
  rcases eq_or_ne x y with hxy | hxy
  · subst y
    simpa only [dist_self] using
      Real.zero_rpow_nonneg (binaryToTernaryHolderExponent : ℝ)
  · let n := PiNat.firstDiff x y
    have hprefix : ∀ i < n, x i = y i := by
      intro i hi
      exact PiNat.apply_eq_of_lt_firstDiff hi
    calc
      dist (binaryToTernaryCantor x) (binaryToTernaryCantor y) ≤
          (1 / 3 : ℝ) ^ n :=
        binaryToTernaryCantor_dist_le_of_prefix hprefix
      _ = ((1 / 2 : ℝ) ^ n) ^
          (binaryToTernaryHolderExponent : ℝ) :=
        (binaryScale_rpow_holderExponent n).symm
      _ = dist x y ^
          (binaryToTernaryHolderExponent : ℝ) := by
        rw [PiNat.dist_eq_of_ne hxy]

/-- The canonical binary-to-ternary coding is Hölder with coefficient one and
exponent log_2 3. -/
theorem binaryToTernaryCantor_holderWith :
    HolderWith 1 binaryToTernaryHolderExponent binaryToTernaryCantor := by
  intro x y
  rw [edist_dist, edist_dist, ENNReal.coe_one, one_mul]
  rw [ENNReal.ofReal_rpow_of_nonneg
    dist_nonneg
    (show (0 : ℝ) ≤ (binaryToTernaryHolderExponent : ℝ) by
      exact binaryToTernaryHolderExponent.2)]
  exact
    ENNReal.ofReal_mono
      (binaryToTernaryCantor_dist_le_rpow x y)

/-- Hölder transport gives the sharp upper Hausdorff-dimension bound for the
classical real Cantor set. -/
theorem dimH_cantorSet_le_cantorCriticalExponent :
    dimH cantorSet ≤ (cantorCriticalExponent : ENNReal) := by
  have h :=
    binaryToTernaryCantor_holderWith.dimH_range_le
      binaryToTernaryHolderExponent_pos
  rw [range_binaryToTernaryCantor, dimH_binaryCantorSpace_eq_one] at h
  have hinv :
      (1 : ENNReal) /
          (binaryToTernaryHolderExponent : ENNReal) =
        (cantorCriticalExponent : ENNReal) := by
    have hne : binaryToTernaryHolderExponent ≠ 0 :=
      binaryToTernaryHolderExponent_pos.ne'
    rw [one_div, ← ENNReal.coe_inv hne]
    exact_mod_cast binaryToTernaryHolderExponent_inv
  exact h.trans_eq hinv

/-!
## Boundary after v4.36

The forward quantitative transport is now complete:

* binary-to-ternary coding has exact range `cantorSet`;
* common-prefix depth gives ternary distance at scale `3^(-n)`;
* PiNat distance is binary scale `2^(-n)`;
* exponent `logb 2 3` converts the scales exactly;
* the coding is `HolderWith 1 (logb 2 3)`;
* therefore

    dimH cantorSet <= logb 3 2.

The remaining hard direction is the inverse estimate.  One must prove that
first disagreement in the allowed ternary 0/2 code forces a Euclidean
separation from below at the same critical scale.  That will yield a Hölder
bound for the inverse coding and hence the lower dimension inequality.
-/

end

end KUOS.DependentOriginationCantorForwardHolderV4_36
