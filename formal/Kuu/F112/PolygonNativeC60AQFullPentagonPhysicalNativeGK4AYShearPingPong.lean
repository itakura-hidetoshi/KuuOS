import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4AXFiniteEvaluationDeterminacy
import Mathlib.GroupTheory.CoprodI
import Mathlib.Tactic

/-!
F112-P94D3GK4AY — exact integer shear geometry for the Sanov
single-evaluation problem of original F54 polynomial histories.

Genuine polynomial generators at t=4 are
  C = [[1,1],[0,1]], F=C⁻¹, R = [[1,0],[4,1]].
Under the integer coordinate rescaling (u,v) ↦ (2u,v)
their actions become upper and lower shear maps
  U(n)(x,y)=(x+2*n*y,y)
  L(n)(x,y)=(x,y+2*n*x).
Both are genuine invertible integer bijections and are additive
one-parameter actions. For all NONZERO n, U(n) sends the vertical
strict cone |y|>|x| into the horizontal cone |x|>|y|, and L(n)
sends the horizontal cone into the vertical cone. This is the
arithmetic ping-pong inequality needed for the pinned mathlib
`Monoid.CoprodI.lift_injective_of_ping_pong` theorem.

No free-subgroup injectivity, single-point polynomial determinacy,
or full original F54 Type-valued equivalence is claimed before the
corresponding Lean theorem actually exists. None of the old true
Type-valued comparison cells or quotient assumptions is weakened.

Append-only, root107 unchanged; Lean 4.30.0-rc2 and pinned mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6. Protected PR #1558
Draft/OPEN/unmerged. No Gray. Copyright © 2026 Hidetoshi Itakura /
板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

/-- The horizontal cone is STRICT, intentionally excluding the boundary. -/
def nativeGK4AYHorizontal (z : Int × Int) : Prop := |z.2| < |z.1|

/-- The vertical cone is STRICT, intentionally excluding the boundary. -/
def nativeGK4AYVertical (z : Int × Int) : Prop := |z.1| < |z.2|

theorem nativeGK4AYCones_disjoint (z : Int × Int)
    (hh : nativeGK4AYHorizontal z) (hv : nativeGK4AYVertical z) : False := by
  dsimp [nativeGK4AYHorizontal, nativeGK4AYVertical] at *
  omega

theorem nativeGK4AYHorizontal_nonempty :
    ∃ z : Int × Int, nativeGK4AYHorizontal z := by
  refine ⟨(2, 1), ?_⟩
  norm_num [nativeGK4AYHorizontal]

theorem nativeGK4AYVertical_nonempty :
    ∃ z : Int × Int, nativeGK4AYVertical z := by
  refine ⟨(1, 2), ?_⟩
  norm_num [nativeGK4AYVertical]

/-- Upper integer transvection, parameterized by arbitrary exponent n. -/
def nativeGK4AYUpperShear (n : Int) (z : Int × Int) : Int × Int :=
  (z.1 + 2 * n * z.2, z.2)

/-- Lower integer transvection, parameterized by arbitrary exponent n. -/
def nativeGK4AYLowerShear (n : Int) (z : Int × Int) : Int × Int :=
  (z.1, z.2 + 2 * n * z.1)

theorem nativeGK4AYUpperShear_add (m n : Int) (z : Int × Int) :
    nativeGK4AYUpperShear m (nativeGK4AYUpperShear n z) =
      nativeGK4AYUpperShear (m + n) z := by
  rcases z with ⟨x, y⟩
  simp only [nativeGK4AYUpperShear, Prod.fst, Prod.snd, Prod.mk.injEq, and_true]
  ring

theorem nativeGK4AYLowerShear_add (m n : Int) (z : Int × Int) :
    nativeGK4AYLowerShear m (nativeGK4AYLowerShear n z) =
      nativeGK4AYLowerShear (m + n) z := by
  rcases z with ⟨x, y⟩
  simp only [nativeGK4AYLowerShear, Prod.fst, Prod.snd, Prod.mk.injEq, true_and]
  ring

theorem nativeGK4AYUpperShear_zero (z : Int × Int) :
    nativeGK4AYUpperShear 0 z = z := by
  rcases z with ⟨x, y⟩
  simp [nativeGK4AYUpperShear]

theorem nativeGK4AYLowerShear_zero (z : Int × Int) :
    nativeGK4AYLowerShear 0 z = z := by
  rcases z with ⟨x, y⟩
  simp [nativeGK4AYLowerShear]

/-- A closed invertible permutation; negative exponent is an actual inverse. -/
def nativeGK4AYUpperPerm (n : Int) : Equiv.Perm (Int × Int) where
  toFun := nativeGK4AYUpperShear n
  invFun := nativeGK4AYUpperShear (-n)
  left_inv z := by
    rw [nativeGK4AYUpperShear_add, neg_add_cancel]
    exact nativeGK4AYUpperShear_zero z
  right_inv z := by
    rw [nativeGK4AYUpperShear_add, add_neg_cancel]
    exact nativeGK4AYUpperShear_zero z

def nativeGK4AYLowerPerm (n : Int) : Equiv.Perm (Int × Int) where
  toFun := nativeGK4AYLowerShear n
  invFun := nativeGK4AYLowerShear (-n)
  left_inv z := by
    rw [nativeGK4AYLowerShear_add, neg_add_cancel]
    exact nativeGK4AYLowerShear_zero z
  right_inv z := by
    rw [nativeGK4AYLowerShear_add, add_neg_cancel]
    exact nativeGK4AYLowerShear_zero z

/-- Strict two-cone inequality, in integral arithmetic, for EVERY
nontrivial upper shear exponent (positive or negative). -/
theorem nativeGK4AYAbs_upper (x y n : Int)
    (hn : n ≠ 0) (hxy : |x| < |y|) :
    |y| < |x + 2 * n * y| := by
  have hnpos : 0 < |n| := abs_pos.mpr hn
  have hn1 : (1 : Int) ≤ |n| := by omega
  have ht := abs_add_le (x + 2 * n * y) (-x)
  have hcancel : x + 2 * n * y + -x = 2 * n * y := by ring
  rw [hcancel, abs_neg] at ht
  have habs : |(2 : Int) * n * y| = 2 * |n| * |y| := by
    simp [abs_mul]
  rw [habs] at ht
  have hprod : 0 ≤ (|n| - 1) * |y| :=
    mul_nonneg (by omega) (abs_nonneg _)
  nlinarith

/-- Strict cone transport for lower integer shear, via the same
actual triangle-inequality calculation and reversed coordinates. -/
theorem nativeGK4AYAbs_lower (x y n : Int)
    (hn : n ≠ 0) (hyx : |y| < |x|) :
    |x| < |y + 2 * n * x| :=
  nativeGK4AYAbs_upper y x n hn hyx

/-- First ping-pong inclusion, exact pointwise form. -/
theorem nativeGK4AYUpper_maps_vertical (n : Int) (hn : n ≠ 0)
    (z : Int × Int) (hz : nativeGK4AYVertical z) :
    nativeGK4AYHorizontal (nativeGK4AYUpperShear n z) := by
  rcases z with ⟨x, y⟩
  exact nativeGK4AYAbs_upper x y n hn hz

/-- Second ping-pong inclusion, exact pointwise form. -/
theorem nativeGK4AYLower_maps_horizontal (n : Int) (hn : n ≠ 0)
    (z : Int × Int) (hz : nativeGK4AYHorizontal z) :
    nativeGK4AYVertical (nativeGK4AYLowerShear n z) := by
  rcases z with ⟨x, y⟩
  exact nativeGK4AYAbs_lower x y n hn hz

/-- Original integer-coordinate rescaling makes TRUE C at t=4
act by U(1) on (2u,v); no real square root or change of ring. -/
theorem nativeGK4AYCast_rescaled (u v : Int) :
    nativeGK4AYUpperShear 1 (2 * u, v) = (2 * (u + v), v) := by
  simp [nativeGK4AYUpperShear]
  ring

/-- Original R(4) acts by L(1) under the SAME rescaling. -/
theorem nativeGK4AYBackward_rescaled (u v : Int) :
    nativeGK4AYLowerShear 1 (2 * u, v) = (2 * u, 4 * u + v) := by
  simp [nativeGK4AYLowerShear]
  ring

/-- The true original F54 cast and backward generator matrices at 4,
extracted from the same previously verified GK4AV polynomial family. -/
theorem nativeGK4AYGenuineGenerators_eval_four :
    nativeGK4AVPolyEval 4 nativeGK4AVCast =
        (((1 : Int), 1), (0, 1)) ∧
    nativeGK4AVPolyEval 4 nativeGK4AVBackward =
        (((1 : Int), 0), (4, 1)) := by
  constructor <;>
    simp [nativeGK4AVPolyEval, nativeGK4AVCast,
      nativeGK4AVBackward]

#print axioms nativeGK4AYHorizontal
#print axioms nativeGK4AYVertical
#print axioms nativeGK4AYCones_disjoint
#print axioms nativeGK4AYHorizontal_nonempty
#print axioms nativeGK4AYVertical_nonempty
#print axioms nativeGK4AYUpperShear
#print axioms nativeGK4AYLowerShear
#print axioms nativeGK4AYUpperShear_add
#print axioms nativeGK4AYLowerShear_add
#print axioms nativeGK4AYUpperShear_zero
#print axioms nativeGK4AYLowerShear_zero
#print axioms nativeGK4AYUpperPerm
#print axioms nativeGK4AYLowerPerm
#print axioms nativeGK4AYAbs_upper
#print axioms nativeGK4AYAbs_lower
#print axioms nativeGK4AYUpper_maps_vertical
#print axioms nativeGK4AYLower_maps_horizontal
#print axioms nativeGK4AYCast_rescaled
#print axioms nativeGK4AYBackward_rescaled
#print axioms nativeGK4AYGenuineGenerators_eval_four

end
end Kuu.F112.Physical
