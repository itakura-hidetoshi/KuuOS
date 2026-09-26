import KUOS.DependentOriginationStageIIGeometricFractalLimitV4_32
import Mathlib.Topology.MetricSpace.HausdorffAlexandroff
import Mathlib.Topology.MetricSpace.HausdorffDimension
import Mathlib.MeasureTheory.Measure.Hausdorff
import Mathlib.Topology.MetricSpace.PiNat
import Mathlib.Analysis.Real.OfDigits
import Mathlib

namespace KUOS.DependentOriginationBinaryCantorHausdorffDimensionV4_33

open Filter
open MeasureTheory

set_option autoImplicit false

noncomputable section

/-!
# Binary Cantor space has Hausdorff dimension one v4.33

The exact ternary Cantor-set dimension will be transferred from the canonical
binary Cantor space.  This file first fixes the metric normalization.

We use mathlib's PiNat metric on Bool-valued streams:

  d(x,y) = (1/2)^(first differing index).

The lower bound dim_H >= 1 follows from a 1-Lipschitz surjection onto the unit
interval, obtained from binary positional expansion.

The upper bound dim_H <= 1 follows from the canonical length-n cylinder cover:
there are 2^n cylinders and every cylinder has diameter at most 2^(-n).
Consequently the one-dimensional Hausdorff measure is finite.

This produces the exact normalization

  dim_H (Nat -> Bool) = 1,

which will be used in the next unit to transport dimension through ternary
Cantor coding with Hölder exponent log_3 2.
-/

abbrev BinaryCantorSpace : Type := Nat → Bool

attribute [local instance] PiNat.metricSpace

/-- Convert a Bool stream to binary digits in Fin 2. -/
def binaryCantorDigits
    (x : BinaryCantorSpace) : Nat → Fin 2 :=
  fun n => finTwoEquiv.symm (x n)

/-- Real binary value of a Bool stream. -/
noncomputable def binaryCantorValue
    (x : BinaryCantorSpace) : Real :=
  Real.ofDigits (binaryCantorDigits x)

/-- Binary values always lie in the unit interval. -/
theorem binaryCantorValue_mem_Icc
    (x : BinaryCantorSpace) :
    binaryCantorValue x ∈ Set.Icc (0 : Real) 1 := by
  exact ⟨Real.ofDigits_nonneg _, Real.ofDigits_le_one _⟩

/-- Every point of the real unit interval has a binary Bool-stream
representation. -/
theorem binaryCantorValue_surjOn_Icc :
    Set.SurjOn binaryCantorValue Set.univ (Set.Icc (0 : Real) 1) := by
  intro y hy
  rcases (Real.ofDigits_SurjOn (b := 2) (by norm_num)) y hy with
    ⟨d, hd, hdy⟩
  let x : BinaryCantorSpace := fun n => finTwoEquiv (d n)
  refine ⟨x, Set.mem_univ x, ?_⟩
  have hdigits : binaryCantorDigits x = d := by
    funext n
    simp [binaryCantorDigits, x]
  simpa [binaryCantorValue, hdigits] using hdy

/-- The range of the binary value map is exactly [0,1]. -/
theorem range_binaryCantorValue :
    Set.range binaryCantorValue = Set.Icc (0 : Real) 1 := by
  apply Set.Subset.antisymm
  · rintro y ⟨x, rfl⟩
    exact binaryCantorValue_mem_Icc x
  · intro y hy
    rcases binaryCantorValue_surjOn_Icc y hy with ⟨x, _, hx⟩
    exact ⟨x, hx⟩

/-- Agreement on the first n Bool coordinates implies agreement of the
corresponding Fin 2 binary digits. -/
theorem binaryCantorDigits_eq_of_mem_cylinder
    {x y : BinaryCantorSpace}
    {n : Nat}
    (hy : y ∈ PiNat.cylinder x n) :
    ∀ i < n, binaryCantorDigits x i = binaryCantorDigits y i := by
  intro i hi
  have hxy := (PiNat.mem_cylinder_iff.mp hy) i hi
  simp [binaryCantorDigits, hxy]

/-- The binary value map is 1-Lipschitz for the PiNat metric. -/
theorem binaryCantorValue_lipschitz :
    LipschitzWith 1 binaryCantorValue := by
  apply LipschitzWith.mk_one
  refine
    (PiNat.lipschitz_with_one_iff_forall_dist_image_le_of_mem_cylinder).2 ?_
  intro x y n hy
  rw [Real.dist_eq]
  calc
    |binaryCantorValue x - binaryCantorValue y| ≤
        ((2 : Real) ^ n)⁻¹ := by
      exact
        Real.abs_ofDigits_sub_ofDigits_le
          (binaryCantorDigits_eq_of_mem_cylinder hy)
    _ = (1 / 2 : Real) ^ n := by
      simp [one_div, inv_pow]

/-- Hence the binary Cantor space has Hausdorff dimension at least one. -/
theorem one_le_dimH_binaryCantorSpace :
    (1 : ENNReal) ≤
      dimH (Set.univ : Set BinaryCantorSpace) := by
  have hrange :
      dimH (Set.range binaryCantorValue) = 1 := by
    rw [range_binaryCantorValue]
    rw [← segment_eq_Icc (by norm_num : (0 : Real) ≤ 1)]
    exact Real.dimH_segment (by norm_num)
  calc
    (1 : ENNReal) = dimH (Set.range binaryCantorValue) := hrange.symm
    _ ≤ dimH (Set.univ : Set BinaryCantorSpace) :=
      binaryCantorValue_lipschitz.dimH_range_le

/-- Extend a finite Bool word by zeros to an infinite Bool stream. -/
def binaryPrefixExtend
    {n : Nat}
    (w : Fin n → Bool) :
    BinaryCantorSpace :=
  fun i => if h : i < n then w ⟨i, h⟩ else false

/-- The canonical cylinder corresponding to a finite Bool word. -/
def binaryCylinder
    (n : Nat)
    (w : Fin n → Bool) :
    Set BinaryCantorSpace :=
  PiNat.cylinder (binaryPrefixExtend w) n

/-- The length-n binary cylinders cover the entire binary Cantor space. -/
theorem univ_subset_iUnion_binaryCylinder
    (n : Nat) :
    (Set.univ : Set BinaryCantorSpace) ⊆
      ⋃ w : Fin n → Bool, binaryCylinder n w := by
  intro x hx
  let w : Fin n → Bool := fun i => x i
  rw [Set.mem_iUnion]
  refine ⟨w, ?_⟩
  rw [PiNat.mem_cylinder_iff]
  intro i hi
  simp [binaryCylinder, binaryPrefixExtend, w, hi]

/-- Every length-n cylinder has extended diameter at most 2^(-n). -/
theorem binaryCylinder_ediam_le
    (n : Nat)
    (w : Fin n → Bool) :
    Metric.ediam (binaryCylinder n w) ≤
      (2 : ENNReal)⁻¹ ^ n := by
  apply Metric.ediam_le
  intro x hx y hy
  rw [edist_dist]
  have hx' :
      dist x (binaryPrefixExtend w) ≤ (1 / 2 : Real) ^ n :=
    PiNat.mem_cylinder_iff_dist_le.mp hx
  have hy' :
      dist (binaryPrefixExtend w) y ≤ (1 / 2 : Real) ^ n := by
    rw [dist_comm]
    exact PiNat.mem_cylinder_iff_dist_le.mp hy
  have hxy :
      dist x y ≤ (1 / 2 : Real) ^ n := by
    exact
      (PiNat.dist_triangle_nonarch x (binaryPrefixExtend w) y).trans
        (max_le hx' hy')
  calc
    ENNReal.ofReal (dist x y) ≤
        ENNReal.ofReal ((1 / 2 : Real) ^ n) :=
      ENNReal.ofReal_mono hxy
    _ = (2 : ENNReal)⁻¹ ^ n := by
      rw [ENNReal.ofReal_pow (by positivity : 0 ≤ (1 / 2 : Real))]
      norm_num

/-- The canonical cylinder diameter scale tends to zero. -/
theorem binaryCylinderScale_tendsto_zero :
    Tendsto
      (fun n : Nat => (2 : ENNReal)⁻¹ ^ n)
      atTop
      (nhds 0) := by
  exact ENNReal.tendsto_pow_atTop_nhds_zero_of_lt_one (by norm_num)

/-- At dimension one, the total diameter of the level-n binary cylinder cover
is at most one. -/
theorem binaryCylinderCover_sum_le_one
    (n : Nat) :
    (∑ w : Fin n → Bool,
      Metric.ediam (binaryCylinder n w) ^ (1 : Real)) ≤
      (1 : ENNReal) := by
  calc
    (∑ w : Fin n → Bool,
      Metric.ediam (binaryCylinder n w) ^ (1 : Real)) ≤
        ∑ _w : Fin n → Bool, (2 : ENNReal)⁻¹ ^ n := by
      apply Finset.sum_le_sum
      intro w hw
      simpa using binaryCylinder_ediam_le n w
    _ = 1 := by
      simp [Fintype.card_fun, ← mul_pow]

/-- The liminf of the one-dimensional cylinder-cover costs is at most one. -/
theorem binaryCylinderCover_liminf_le_one :
    Filter.liminf
        (fun n : Nat =>
          ∑ w : Fin n → Bool,
            Metric.ediam (binaryCylinder n w) ^ (1 : Real))
        atTop ≤
      (1 : ENNReal) := by
  refine Filter.liminf_le_of_le (a := (1 : ENNReal)) (h := ?_)
  intro b hb
  rcases hb.exists with ⟨n, hn⟩
  exact hn.trans (binaryCylinderCover_sum_le_one n)

/-- The one-dimensional Hausdorff measure of the binary Cantor space is finite. -/
theorem hausdorffMeasure_one_binaryCantorSpace_le_one :
    (MeasureTheory.Measure.hausdorffMeasure 1)
        (Set.univ : Set BinaryCantorSpace) ≤
      (1 : ENNReal) := by
  letI : MeasurableSpace BinaryCantorSpace := borel BinaryCantorSpace
  letI : BorelSpace BinaryCantorSpace := ⟨rfl⟩
  calc
    (MeasureTheory.Measure.hausdorffMeasure 1)
        (Set.univ : Set BinaryCantorSpace) ≤
        Filter.liminf
          (fun n : Nat =>
            ∑ w : Fin n → Bool,
              Metric.ediam (binaryCylinder n w) ^ (1 : Real))
          atTop := by
      exact
        MeasureTheory.Measure.hausdorffMeasure_le_liminf_sum
          1
          (Set.univ : Set BinaryCantorSpace)
          (fun n : Nat => (2 : ENNReal)⁻¹ ^ n)
          binaryCylinderScale_tendsto_zero
          binaryCylinder
          (Filter.Eventually.of_forall
            (fun n w => binaryCylinder_ediam_le n w))
          (Filter.Eventually.of_forall
            (fun n => univ_subset_iUnion_binaryCylinder n))
    _ ≤ 1 := binaryCylinderCover_liminf_le_one

/-- Therefore the binary Cantor space has Hausdorff dimension at most one. -/
theorem dimH_binaryCantorSpace_le_one :
    dimH (Set.univ : Set BinaryCantorSpace) ≤
      (1 : ENNReal) := by
  letI : MeasurableSpace BinaryCantorSpace := borel BinaryCantorSpace
  letI : BorelSpace BinaryCantorSpace := ⟨rfl⟩
  apply dimH_le_of_hausdorffMeasure_ne_top (d := (1 : NNReal))
  intro htop
  have hle := hausdorffMeasure_one_binaryCantorSpace_le_one
  rw [htop] at hle
  exact not_top_le_one hle

/-- Exact Hausdorff dimension of the normalized binary Cantor space. -/
theorem dimH_binaryCantorSpace_eq_one :
    dimH (Set.univ : Set BinaryCantorSpace) = 1 := by
  exact le_antisymm dimH_binaryCantorSpace_le_one one_le_dimH_binaryCantorSpace

/-!
## Boundary after v4.33

The canonical binary Cantor space now has exact Hausdorff dimension one for
mathlib's PiNat metric.

The next step is quantitative transport to the ternary Cantor set.  If two
ternary Cantor points first differ at digit n, their Euclidean distance is
bounded below at scale 3^(-(n+1)), while their binary codes are separated at
scale 2^(-n).  With s = log_3 2, this gives the critical Holder exponent.

Combining that lower-bound transport with the standard 2^n ternary-cylinder
cover will identify the real Cantor-set Hausdorff dimension exactly with

  logb 3 2 = log 2 / log 3.
-/

end

end KUOS.DependentOriginationBinaryCantorHausdorffDimensionV4_33
