import KUOS.DependentOriginationCantorCriticalExponentV4_34
import Mathlib.Topology.Instances.CantorSet
import Mathlib.Topology.MetricSpace.PiNat
import Mathlib.Analysis.Real.OfDigits
import Mathlib

namespace KUOS.DependentOriginationCantorCodingPrefixV4_35

open KUOS.DependentOriginationBinaryCantorHausdorffDimensionV4_33

set_option autoImplicit false

noncomputable section

attribute [local instance] PiNat.metricSpace

/-!
# Canonical binary-to-ternary Cantor coding and prefix estimate v4.35

v4.33 fixes the normalized binary Cantor source `Nat → Bool` and proves its
Hausdorff dimension is exactly one.  v4.34 isolates the critical exponent
`logb 3 2`.

This unit keeps the next step as close as possible to mathlib's existing
Cantor API.

We define the canonical ternary 0/2 coding

  Bool stream ↦ Real.ofDigits (0/2 ternary digits),

identify it with the inverse of mathlib's canonical equivalence
`cantorSetEquivNatToBool`, prove that its range is exactly `cantorSet`, and
record the quantitative common-prefix estimate

  common prefix of length n
    -> distance of real Cantor images <= 3^(-n).

No Hölder exponent algebra is used yet.  That conversion belongs to the next
unit.
-/

/-- Ternary digits 0/2 associated to a binary stream. -/
def binaryToTernaryDigits
    (x : BinaryCantorSpace) : Nat → Fin 3 :=
  fun n => cond (x n) 2 0

/-- Canonical real Cantor point associated to a binary stream. -/
noncomputable def binaryToTernaryCantor
    (x : BinaryCantorSpace) : ℝ :=
  Real.ofDigits (binaryToTernaryDigits x)

/-- Every canonical binary-to-ternary code lands in the classical Cantor set. -/
theorem binaryToTernaryCantor_mem_cantorSet
    (x : BinaryCantorSpace) :
    binaryToTernaryCantor x ∈ cantorSet := by
  simpa [binaryToTernaryCantor, binaryToTernaryDigits] using
    ofDigits_bool_to_fin_three_mem_cantorSet x

/-- The canonical equivalence from binary streams to the Cantor-set subtype. -/
noncomputable def binaryCantorEquivCantorSet :
    BinaryCantorSpace ≃ cantorSet :=
  cantorSetEquivNatToBool.symm

/-- The subtype value of the canonical equivalence is exactly the explicit
0/2-digit real coding. -/
@[simp] theorem binaryCantorEquivCantorSet_val
    (x : BinaryCantorSpace) :
    ((binaryCantorEquivCantorSet x : cantorSet) : ℝ) =
      binaryToTernaryCantor x := by
  rfl

/-- The explicit real coding is injective. -/
theorem binaryToTernaryCantor_injective :
    Function.Injective binaryToTernaryCantor := by
  intro x y hxy
  apply binaryCantorEquivCantorSet.injective
  apply Subtype.ext
  simpa using hxy

/-- Applying the inverse code to a Cantor point and returning to the real line
recovers the original point. -/
@[simp] theorem binaryToTernaryCantor_inverse_value
    (z : cantorSet) :
    binaryToTernaryCantor (binaryCantorEquivCantorSet.symm z) = (z : ℝ) := by
  have h :
      binaryCantorEquivCantorSet (binaryCantorEquivCantorSet.symm z) = z :=
    binaryCantorEquivCantorSet.apply_symm_apply z
  have hval := congrArg (fun q : cantorSet => (q : ℝ)) h
  simpa using hval

/-- The range of the explicit coding is exactly the classical ternary Cantor
set. -/
theorem range_binaryToTernaryCantor :
    Set.range binaryToTernaryCantor = cantorSet := by
  apply Set.Subset.antisymm
  · rintro y ⟨x, rfl⟩
    exact binaryToTernaryCantor_mem_cantorSet x
  · intro y hy
    let z : cantorSet := ⟨y, hy⟩
    refine ⟨binaryCantorEquivCantorSet.symm z, ?_⟩
    simpa [z] using binaryToTernaryCantor_inverse_value z

/-- Equal binary prefixes induce equal ternary 0/2 prefixes. -/
theorem binaryToTernaryDigits_eq_of_prefix
    {x y : BinaryCantorSpace}
    {n : Nat}
    (hxy : ∀ i < n, x i = y i) :
    ∀ i < n, binaryToTernaryDigits x i = binaryToTernaryDigits y i := by
  intro i hi
  simp [binaryToTernaryDigits, hxy i hi]

/-- Common binary prefix of length `n` gives the sharp elementary ternary
upper bound `3^(-n)` on the Euclidean distance of the coded Cantor points. -/
theorem binaryToTernaryCantor_dist_le_of_prefix
    {x y : BinaryCantorSpace}
    {n : Nat}
    (hxy : ∀ i < n, x i = y i) :
    dist (binaryToTernaryCantor x) (binaryToTernaryCantor y) ≤
      (1 / 3 : ℝ) ^ n := by
  rw [Real.dist_eq]
  calc
    |binaryToTernaryCantor x - binaryToTernaryCantor y| ≤
        ((3 : ℝ) ^ n)⁻¹ := by
      exact
        Real.abs_ofDigits_sub_ofDigits_le
          (binaryToTernaryDigits_eq_of_prefix hxy)
    _ = (1 / 3 : ℝ) ^ n := by
      simp [one_div, inv_pow]

/-- Cylinder membership is the PiNat metric form of the same common-prefix
estimate. -/
theorem binaryToTernaryCantor_dist_le_of_mem_cylinder
    {x y : BinaryCantorSpace}
    {n : Nat}
    (hy : y ∈ PiNat.cylinder x n) :
    dist (binaryToTernaryCantor x) (binaryToTernaryCantor y) ≤
      (1 / 3 : ℝ) ^ n := by
  apply binaryToTernaryCantor_dist_le_of_prefix
  intro i hi
  exact ((PiNat.mem_cylinder_iff.mp hy) i hi).symm

/-!
## Boundary after v4.35

The source/target coding is now fixed canonically and quantitatively:

* `binaryToTernaryCantor` is injective;
* its range is exactly `cantorSet`;
* it is definitionally the inverse side of mathlib's canonical Cantor
  equivalence;
* agreement through depth `n` forces real distance at most `3^(-n)`.

The next theorem unit should convert this prefix estimate into a global
HölderWith estimate with exponent `Real.logb 2 3`, using PiNat's exact
first-difference metric and the v4.34 scale identities.  That gives the upper
dimension inequality

  dimH cantorSet <= logb 3 2.

The inverse/separation estimate should remain a separate theorem unit because
it requires a genuine lower bound on ternary separation at the first differing
digit.
-/

end

end KUOS.DependentOriginationCantorCodingPrefixV4_35
