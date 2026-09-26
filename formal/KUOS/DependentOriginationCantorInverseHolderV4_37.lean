import KUOS.DependentOriginationCantorForwardHolderV4_36
import Mathlib.Topology.MetricSpace.HausdorffDimension
import Mathlib.Topology.MetricSpace.Holder
import Mathlib.Analysis.Real.OfDigits
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Analysis.SpecialFunctions.Pow.NNReal
import Mathlib

namespace KUOS.DependentOriginationCantorInverseHolderV4_37

open MeasureTheory
open KUOS.DependentOriginationBinaryCantorHausdorffDimensionV4_33
open KUOS.DependentOriginationCantorCriticalExponentV4_34
open KUOS.DependentOriginationCantorCodingPrefixV4_35
open KUOS.DependentOriginationCantorForwardHolderV4_36

set_option autoImplicit false

noncomputable section

attribute [local instance] PiNat.metricSpace

/-!
# Inverse Hölder transport and Cantor Hausdorff lower bound v4.37

The forward direction is complete in v4.36:

  dimH cantorSet <= logb 3 2.

For the reverse inequality we need genuine separation, not only a common-prefix
upper bound.

If two binary streams agree before index n and have digits false/true at n,
then their ternary 0/2 values satisfy

  3^(-(n+1)) <= F(y) - F(x).

The proof expands both positional series after n+1 digits.  The first differing
digit contributes exactly two units of the scale 3^(-(n+1)); the worst possible
opposing tail can cancel at most one unit of that scale.

This yields, for first difference n,

  3^(-(n+1)) <= dist(F x, F y).

Raising to s = logb 3 2 converts ternary scale to binary scale.  Consequently
the inverse Cantor coding is (2,s)-Hölder.  Hausdorff-dimension transport then
gives

  logb 3 2 <= dimH cantorSet.
-/

/-- If two streams have a common prefix of length n and then digits false/true,
the corresponding ternary Cantor values are separated from below by
3^(-(n+1)). -/
theorem binaryToTernaryCantor_sub_lower_of_prefix_false_true
    {x y : BinaryCantorSpace}
    {n : Nat}
    (hprefix : ∀ i < n, x i = y i)
    (hxn : x n = false)
    (hyn : y n = true) :
    (1 / 3 : ℝ) ^ (n + 1) ≤
      binaryToTernaryCantor y - binaryToTernaryCantor x := by
  let a : Nat → Fin 3 := binaryToTernaryDigits x
  let b : Nat → Fin 3 := binaryToTernaryDigits y
  let p : ℝ := ∑ i ∈ Finset.range n, Real.ofDigitsTerm a i
  let scale : ℝ := ((3 : ℝ) ^ (n + 1))⁻¹
  let tx : ℝ := Real.ofDigits (fun i => a (i + (n + 1)))
  let ty : ℝ := Real.ofDigits (fun i => b (i + (n + 1)))

  have hp :
      (∑ i ∈ Finset.range n, Real.ofDigitsTerm b i) = p := by
    unfold p
    apply Finset.sum_congr rfl
    intro i hi
    have hij : x i = y i := hprefix i (Finset.mem_range.mp hi)
    simp [a, b, Real.ofDigitsTerm, binaryToTernaryDigits, hij]

  have hxdec :
      binaryToTernaryCantor x = p + scale * tx := by
    rw [binaryToTernaryCantor]
    rw [Real.ofDigits_eq_sum_add_ofDigits a (n + 1)]
    rw [Finset.sum_range_succ]
    simp [a, p, scale, tx, Real.ofDigitsTerm, binaryToTernaryDigits, hxn]

  have hydec :
      binaryToTernaryCantor y = p + 2 * scale + scale * ty := by
    rw [binaryToTernaryCantor]
    rw [Real.ofDigits_eq_sum_add_ofDigits b (n + 1)]
    rw [Finset.sum_range_succ, hp]
    simp [b, p, scale, ty, Real.ofDigitsTerm, binaryToTernaryDigits, hyn]
    ring

  have hscale_nonneg : 0 ≤ scale := by
    dsimp [scale]
    positivity
  have htx_le : tx ≤ 1 := by
    exact Real.ofDigits_le_one _
  have hty_nonneg : 0 ≤ ty := by
    exact Real.ofDigits_nonneg _
  have htailx : scale * tx ≤ scale := by
    simpa [mul_one] using
      (mul_le_mul_of_nonneg_left htx_le hscale_nonneg)
  have htailey : 0 ≤ scale * ty := by
    exact mul_nonneg hscale_nonneg hty_nonneg

  have hscale_form :
      (1 / 3 : ℝ) ^ (n + 1) = scale := by
    simp [scale, one_div, inv_pow]

  rw [hscale_form, hxdec, hydec]
  linarith

/-- At the first differing binary digit, the real Cantor images have a uniform
lower separation at the next ternary scale. -/
theorem binaryToTernaryCantor_firstDiff_separation
    {x y : BinaryCantorSpace}
    (hxy : x ≠ y) :
    (1 / 3 : ℝ) ^ (PiNat.firstDiff x y + 1) ≤
      dist (binaryToTernaryCantor x) (binaryToTernaryCantor y) := by
  let n := PiNat.firstDiff x y
  have hprefix : ∀ i < n, x i = y i := by
    intro i hi
    exact PiNat.apply_eq_of_lt_firstDiff hi
  have hne : x n ≠ y n := by
    exact PiNat.apply_firstDiff_ne hxy
  cases hx : x n <;> cases hy : y n
  · exact (hne (by simp [hx, hy])).elim
  · have hsep :=
      binaryToTernaryCantor_sub_lower_of_prefix_false_true
        hprefix hx hy
    calc
      (1 / 3 : ℝ) ^ (n + 1) ≤
          binaryToTernaryCantor y - binaryToTernaryCantor x := hsep
      _ ≤ |binaryToTernaryCantor y - binaryToTernaryCantor x| :=
        le_abs_self _
      _ = dist (binaryToTernaryCantor x) (binaryToTernaryCantor y) := by
        rw [Real.dist_eq, abs_sub_comm]
  · have hprefix' : ∀ i < n, y i = x i := by
      intro i hi
      exact (hprefix i hi).symm
    have hsep :=
      binaryToTernaryCantor_sub_lower_of_prefix_false_true
        hprefix' hy hx
    calc
      (1 / 3 : ℝ) ^ (n + 1) ≤
          binaryToTernaryCantor x - binaryToTernaryCantor y := hsep
      _ ≤ |binaryToTernaryCantor x - binaryToTernaryCantor y| :=
        le_abs_self _
      _ = dist (binaryToTernaryCantor x) (binaryToTernaryCantor y) := by
        rw [Real.dist_eq]
  · exact (hne (by simp [hx, hy])).elim

/-- Ternary scale raised to the critical exponent equals the binary scale. -/
theorem one_third_rpow_cantorCriticalExponent :
    (1 / 3 : ℝ) ^ cantorCriticalExponentReal = (1 / 2 : ℝ) := by
  calc
    (1 / 3 : ℝ) ^ cantorCriticalExponentReal =
        ((3 : ℝ)⁻¹) ^ cantorCriticalExponentReal := by
      rw [one_div]
    _ = ((3 : ℝ) ^ cantorCriticalExponentReal)⁻¹ := by
      exact
        Real.inv_rpow
          (by norm_num : (0 : ℝ) ≤ 3)
          cantorCriticalExponentReal
    _ = (2 : ℝ)⁻¹ := by
      rw [three_rpow_cantorCriticalExponent]
    _ = (1 / 2 : ℝ) := by
      rw [one_div]

/-- Exact critical scale conversion at every depth. -/
theorem ternaryScale_rpow_cantorCriticalExponent
    (n : Nat) :
    ((1 / 3 : ℝ) ^ n) ^ cantorCriticalExponentReal =
      (1 / 2 : ℝ) ^ n := by
  calc
    ((1 / 3 : ℝ) ^ n) ^ cantorCriticalExponentReal =
        (((1 / 3 : ℝ) ^ cantorCriticalExponentReal) ^ n) := by
      exact
        (Real.rpow_pow_comm
          (by norm_num : (0 : ℝ) ≤ 1 / 3)
          cantorCriticalExponentReal
          n).symm
    _ = (1 / 2 : ℝ) ^ n := by
      rw [one_third_rpow_cantorCriticalExponent]

/-- Canonical inverse map from the Cantor-set subtype to the normalized binary
Cantor space. -/
noncomputable def cantorSetToBinary :
    cantorSet → BinaryCantorSpace :=
  binaryCantorEquivCantorSet.symm

/-- The inverse map is surjective onto the full binary Cantor space. -/
theorem range_cantorSetToBinary :
    Set.range cantorSetToBinary =
      (Set.univ : Set BinaryCantorSpace) := by
  apply Set.range_eq_univ.mpr
  exact binaryCantorEquivCantorSet.symm.surjective

/-- Real-distance inverse Hölder estimate with coefficient two and critical
exponent s = logb 3 2. -/
theorem cantorSetToBinary_dist_le
    (z w : cantorSet) :
    dist (cantorSetToBinary z) (cantorSetToBinary w) ≤
      2 * dist z w ^ cantorCriticalExponentReal := by
  rcases eq_or_ne z w with hzw | hzw
  · subst w
    have hs_nonneg : 0 ≤ cantorCriticalExponentReal :=
      cantorCriticalExponentReal_pos.le
    have hrpow_nonneg :
        0 ≤ (0 : ℝ) ^ cantorCriticalExponentReal :=
      Real.rpow_nonneg (by norm_num) cantorCriticalExponentReal
    simpa only [dist_self, zero_mul] using
      (mul_nonneg (by norm_num : (0 : ℝ) ≤ 2) hrpow_nonneg)
  · let x : BinaryCantorSpace := cantorSetToBinary z
    let y : BinaryCantorSpace := cantorSetToBinary w
    have hxy : x ≠ y := by
      intro h
      apply hzw
      apply binaryCantorEquivCantorSet.symm.injective
      exact h
    let n := PiNat.firstDiff x y
    have hsep :
        (1 / 3 : ℝ) ^ (n + 1) ≤ dist z w := by
      have h0 :=
        binaryToTernaryCantor_firstDiff_separation hxy
      have hz :
          binaryToTernaryCantor x = (z : ℝ) := by
        exact binaryToTernaryCantor_inverse_value z
      have hw :
          binaryToTernaryCantor y = (w : ℝ) := by
        exact binaryToTernaryCantor_inverse_value w
      simpa [x, y, n, hz, hw] using h0
    have hrpow :
        ((1 / 3 : ℝ) ^ (n + 1)) ^ cantorCriticalExponentReal ≤
          dist z w ^ cantorCriticalExponentReal := by
      exact
        Real.rpow_le_rpow
          (by positivity)
          hsep
          cantorCriticalExponentReal_pos.le
    have hscale :
        (1 / 2 : ℝ) ^ n =
          2 * ((1 / 2 : ℝ) ^ (n + 1)) := by
      rw [pow_succ]
      ring
    calc
      dist (cantorSetToBinary z) (cantorSetToBinary w) =
          (1 / 2 : ℝ) ^ n := by
        change dist x y = (1 / 2 : ℝ) ^ n
        exact PiNat.dist_eq_of_ne hxy
      _ = 2 * ((1 / 2 : ℝ) ^ (n + 1)) := hscale
      _ = 2 *
          (((1 / 3 : ℝ) ^ (n + 1)) ^ cantorCriticalExponentReal) := by
        rw [ternaryScale_rpow_cantorCriticalExponent]
      _ ≤ 2 * dist z w ^ cantorCriticalExponentReal := by
        exact mul_le_mul_of_nonneg_left hrpow (by norm_num)

/-- The inverse coding is Hölder with coefficient two and critical exponent. -/
theorem cantorSetToBinary_holderWith :
    HolderWith 2 cantorCriticalExponent cantorSetToBinary := by
  intro z w
  rw [edist_dist, edist_dist]
  calc
    ENNReal.ofReal (dist (cantorSetToBinary z) (cantorSetToBinary w)) ≤
        ENNReal.ofReal
          (2 * dist z w ^ cantorCriticalExponentReal) :=
      ENNReal.ofReal_mono (cantorSetToBinary_dist_le z w)
    _ =
        (2 : ENNReal) *
          ENNReal.ofReal (dist z w) ^
            (cantorCriticalExponent : ℝ) := by
      rw [ENNReal.ofReal_mul (by norm_num : (0 : ℝ) ≤ 2)]
      norm_num
      change
        ENNReal.ofReal 2 *
            ENNReal.ofReal (dist z w ^ cantorCriticalExponentReal) =
          (2 : ENNReal) *
            ENNReal.ofReal (dist z w) ^ cantorCriticalExponentReal
      rw [← ENNReal.ofReal_rpow_of_nonneg
        dist_nonneg
        cantorCriticalExponentReal_pos.le]
      norm_num

/-- The real Cantor set and its subtype carry the same Hausdorff dimension. -/
theorem dimH_univ_cantorSetSubtype :
    dimH (Set.univ : Set cantorSet) = dimH cantorSet := by
  have h :=
    isometry_subtype_coe.dimH_image
      (Set.univ : Set cantorSet)
  have himage :
      ((fun z : cantorSet => (z : ℝ)) '' Set.univ) = cantorSet := by
    ext x
    constructor
    · rintro ⟨z, _, rfl⟩
      exact z.property
    · intro hx
      exact ⟨⟨x, hx⟩, Set.mem_univ _, rfl⟩
  rw [himage] at h
  exact h.symm

/-- Inverse Hölder transport gives the sharp Hausdorff-dimension lower bound. -/
theorem cantorCriticalExponent_le_dimH_cantorSet :
    (cantorCriticalExponent : ENNReal) ≤ dimH cantorSet := by
  have h :=
    cantorSetToBinary_holderWith.dimH_range_le
      cantorCriticalExponent_pos
  rw [range_cantorSetToBinary, dimH_binaryCantorSpace_eq_one,
    dimH_univ_cantorSetSubtype] at h
  have hs0 :
      (cantorCriticalExponent : ENNReal) ≠ 0 := by
    exact_mod_cast cantorCriticalExponent_pos.ne'
  have hst :
      (cantorCriticalExponent : ENNReal) ≠ ⊤ :=
    ENNReal.coe_ne_top
  have hmul :
      (1 : ENNReal) * (cantorCriticalExponent : ENNReal) ≤
        dimH cantorSet := by
    exact
      (ENNReal.le_div_iff_mul_le
        (Or.inl hs0)
        (Or.inl hst)).1 h
  simpa using hmul

/-!
## Boundary after v4.37

The inverse quantitative transport is now complete:

* first disagreement at binary depth n forces real ternary separation at least
  3^(-(n+1));
* the critical exponent converts that scale to 2^(-(n+1));
* the inverse Cantor coding is Hölder with coefficient two and exponent
  s = logb 3 2;
* therefore

    logb 3 2 <= dimH cantorSet.

Together with the v4.36 upper bound, the next unit can close the exact equality

  dimH cantorSet = logb 3 2 = log 2 / log 3

without introducing any new geometric assumption.
-/

end

end KUOS.DependentOriginationCantorInverseHolderV4_37
