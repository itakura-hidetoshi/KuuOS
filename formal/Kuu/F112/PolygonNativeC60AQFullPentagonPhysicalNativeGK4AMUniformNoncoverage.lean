import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4AMNoncoverage
import Mathlib.Tactic

/-!
F112-P94D3GK4AM — UNIFORM failure of GK4AL FamilyCovers(k) for
EVERY positive k, with a concrete new true F54 typed witness.
Let B be the original physical forward/backward LocalRotation
backtrack, H=B^3 and P=B^6. The genuine source word
  V_d = H; C; P^(2*d+1); C; H
has the SAME old GK4AG value as GK4AK's q_(d+1):
  (false, (2-24(d+1),12(d+1),12(d+1)-144(d+1)^2), C^2).
This relies on the OLD matrix H=-I, P=I, not a spurious Type-cell.
The NEW, independently seam-sound matrix decodes to -88-192*d;
all GK4AK family points decode to 8-192*((d+1)-i).
Parity prevents equality for EVERY i : Fin(d+2).
Thus the old conditional finite family is NEVER exhaustive for
any positive k, while all actual fibers remain countable. No single
fixed infinite fiber or exact finite total cardinality is asserted.
No global S faithfulness, Q category axioms, Gray, hyperdescent.
Append-only/tighten-only/same-root107; strict 空 central, independent
Kuu one presentation. Protected #1558 remains Draft/open/unmerged.
Lean v4.30.0-rc2, mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe uD vD uE vE

section UniformTypedNoncoverage
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E} {n m : Nat}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {before after : KuuNativeF45Tree p n m ma pa mb pb}
variable (rot : KuuNativeF45Tree.LocalRotation p before after)

/-- H=B^3 is six actual original F54 rotation edges. -/
theorem nativeGK4AMHalf_count :
    (nativeGK4AHBacktrackTriple rot).rotationCount = 6 := by rfl

theorem nativeGK4AMHalf_ad :
    (nativeGK4AHBacktrackTriple rot).gk4adValue =
      (((-6 : Int), (3 : Nat)), (-9 : Int)) := by rfl

/-- H=-I in the OLD GK4AF observation, rather than H=I. -/
theorem nativeGK4AMHalf_af :
    (nativeGK4AHBacktrackTriple rot).gk4afMatrix =
      (((-1 : Int), (0 : Int)), ((0 : Int), (-1 : Int))) := by rfl

/-- H is NOT scalar in the independent NEW GK4AH representation. -/
theorem nativeGK4AMHalf_ah :
    (nativeGK4AHBacktrackTriple rot).gk4ahMatrix =
      (((-7 : Int), (-3 : Int)), ((12 : Int), (5 : Int))) := by rfl

/-- NEW genuine original F54 self-route at q_(d+1).
The odd number of P blocks is essential for half-step obstruction. -/
def nativeGK4AMOddWord (d : Nat) :
    KuuNativeF45Tree.DepthRotationRoute p before before :=
  .trans (nativeGK4AHBacktrackTriple rot)
    (.trans (nativeGK4WCastRoute before)
      (.trans (nativeGK4AKTower rot (2 * d + 1))
        (.trans (nativeGK4WCastRoute before)
          (nativeGK4AHBacktrackTriple rot))))

theorem nativeGK4AMOddWord_count (d : Nat) :
    (nativeGK4AMOddWord rot d).rotationCount = 24 * (d + 1) := by
  simp only [nativeGK4AMOddWord, nativeGK4H_raw_rotationCount_compose,
    nativeGK4AMHalf_count, nativeGK4AKTower_count, nativeGK4AKCast_count]
  omega

theorem nativeGK4AMOddWord_ad (d : Nat) :
    (nativeGK4AMOddWord rot d).gk4adValue =
      ((2 - 24 * ((d + 1 : Nat) : Int), 12 * (d + 1)),
        12 * ((d + 1 : Nat) : Int) - 144 * ((d + 1 : Nat) : Int) ^ 2) := by
  simp only [nativeGK4AMOddWord, nativeGK4AD_trans,
    nativeGK4AMHalf_ad, nativeGK4AKCast_ad, nativeGK4AKTower_ad]
  apply Prod.ext
  · apply Prod.ext
    · simp [nativeGK4ADCombine] <;> ring
    · simp [nativeGK4ADCombine] <;> omega
  · simp [nativeGK4ADCombine] <;> ring

theorem nativeGK4AMOddWord_af (d : Nat) :
    (nativeGK4AMOddWord rot d).gk4afMatrix =
      (((1 : Int), (2 : Int)), ((0 : Int), (1 : Int))) := by
  simp only [nativeGK4AMOddWord, nativeGK4AF_trans,
    nativeGK4AMHalf_af, nativeGK4AKTower_af, nativeGK4AKCast_af]
  norm_num [nativeGK4AFMul, nativeGK4AFOne, nativeGK4AFCast]

theorem nativeGK4AMOddWord_decoder (d : Nat) :
    nativeGK4AKDecoder (nativeGK4AMOddWord rot d).gk4ahMatrix =
      -88 - 192 * (d : Int) := by
  simp only [nativeGK4AMOddWord, nativeGK4AH_trans,
    nativeGK4AMHalf_ah, nativeGK4AKTower_ah, nativeGK4AKCast_ah]
  simp [nativeGK4AKDecoder, nativeGK4AHMul,
    nativeGK4AKPowerMatrix, nativeGK4AHCast] <;> ring

/-- The SAME old full observation q_(d+1), including the original
four-component Heisenberg value AND first complete 2x2 matrix. -/
theorem nativeGK4AMOddWord_oldValue (d : Nat) :
    nativeGK4AGStructural before before
      (nativeGK4EStructuralRouteClass before before (nativeGK4AMOddWord rot d)) =
      nativeGK4AKOldValue (d + 1) := by
  change ((nativeGK4GRawGrade before before (nativeGK4AMOddWord rot d),
      (nativeGK4AMOddWord rot d).gk4adValue),
      (nativeGK4AMOddWord rot d).gk4afMatrix) = _
  apply Prod.ext
  · apply Prod.ext
    · simp [nativeGK4GRawGrade, nativeGK4AMOddWord_count,
        nativeGK4AKOldValue]
    · exact nativeGK4AMOddWord_ad rot d
  · exact nativeGK4AMOddWord_af rot d

/-- Actual K_AI class, not an arbitrary observed matrix code. -/
def nativeGK4AMOddClass (d : Nat) :
    NativeGK4SKernelClasses (nativeGK4AIP92Family p D E) before before :=
  nativeGK4AIComparison before before
    (nativeGK4EStructuralRouteClass before before (nativeGK4AMOddWord rot d))

theorem nativeGK4AMOddClass_forget (d : Nat) :
    nativeGK4AIForgetMatrix before before (nativeGK4AMOddClass rot d) =
      nativeGK4AKOldTarget rot (d + 1) := by
  change nativeGK4AIForgetMatrix before before
    (nativeGK4AIComparison before before
      (nativeGK4EStructuralRouteClass before before
        (nativeGK4AMOddWord rot d))) =
    nativeGK4AGComparison before before
      (nativeGK4EStructuralRouteClass before before
        (nativeGK4AKWord rot 0 (d + 1)))
  rw [nativeGK4AIForgetMatrix_comparison]
  apply (nativeGK4AGComparison_eq_iff before before _ _).mpr
  rw [nativeGK4AMOddWord_oldValue, nativeGK4AKWord_oldValue]
  rfl

/-- Truly attained new point over the same old q_(d+1). -/
def nativeGK4AMOddFiberPoint (d : Nat) :
    nativeGK4AJOldFiber before before (nativeGK4AKOldTarget rot (d + 1)) :=
  ⟨nativeGK4AMOddClass rot d, nativeGK4AMOddClass_forget rot d⟩

theorem nativeGK4AMOddFiberPoint_decoder (d : Nat) :
    nativeGK4AKDecoder
      (nativeGK4AJFiberMatrix before before
        (nativeGK4AKOldTarget rot (d + 1))
        (nativeGK4AMOddFiberPoint rot d)) =
      -88 - 192 * (d : Int) := by
  change nativeGK4AKDecoder (nativeGK4AMOddWord rot d).gk4ahMatrix = _
  exact nativeGK4AMOddWord_decoder rot d

/-- Each positive-k fiber has a genuinely attained point OUTSIDE
GK4AK's k+1-member finite family. Parity, not cardinality speculation. -/
theorem nativeGK4AMOdd_not_family (d : Nat) (i : Fin ((d + 1) + 1)) :
    nativeGK4AMOddFiberPoint rot d ≠
      nativeGK4AKFiberPoint rot (d + 1) i := by
  intro h
  have hd := congrArg
    (fun z : nativeGK4AJOldFiber before before (nativeGK4AKOldTarget rot (d + 1)) =>
      nativeGK4AKDecoder
        (nativeGK4AJFiberMatrix before before
          (nativeGK4AKOldTarget rot (d + 1)) z)) h
  change nativeGK4AKDecoder
      (nativeGK4AJFiberMatrix before before
        (nativeGK4AKOldTarget rot (d + 1)) (nativeGK4AMOddFiberPoint rot d)) =
    nativeGK4AKDecoder
      (nativeGK4AJFiberMatrix before before
        (nativeGK4AKOldTarget rot (d + 1))
        (nativeGK4AKFiberPoint rot (d + 1) i)) at hd
  rw [nativeGK4AMOddFiberPoint_decoder rot d] at hd
  change (-88 - 192 * (d : Int)) =
    nativeGK4AKDecoder
      (nativeGK4AIKernelValue before before
        (nativeGK4AKClass rot (d + 1) i)).2 at hd
  rw [nativeGK4AKClass_decoder rot (d + 1) i] at hd
  have hi := i.isLt
  omega

/-- Main UNIFORM NEGATIVE RESULT: the conditional GK4AL finite
normal-form family fails to cover at EVERY positive k. -/
theorem nativeGK4AMFamilyCovers_succ_false (d : Nat) :
    ¬ nativeGK4ALFamilyCovers rot (d + 1) := by
  intro h
  obtain ⟨i, hi⟩ := h (nativeGK4AMOddFiberPoint rot d)
  exact nativeGK4AMOdd_not_family rot d i hi.symm

theorem nativeGK4AMFamilyCovers_positive_false (k : Nat) (hk : 0 < k) :
    ¬ nativeGK4ALFamilyCovers rot k := by
  cases k with
  | zero => omega
  | succ d =>
      simpa only [Nat.succ_eq_add_one] using
        (nativeGK4AMFamilyCovers_succ_false rot d)

end UniformTypedNoncoverage

/-- Genuine C60 north: ALL positive-k finite families miss an
additional full Type-valued F54 path in their same old fibers. -/
theorem nativeGK4AMPhysicalNorth_positive_family_noncoverage
    (k : Nat) (hk : 0 < k) :
    ¬ nativeGK4ALFamilyCovers northHexagonNativeLeftRotation k :=
  nativeGK4AMFamilyCovers_positive_false northHexagonNativeLeftRotation k hk

#print axioms nativeGK4AMHalf_count
#print axioms nativeGK4AMHalf_ad
#print axioms nativeGK4AMHalf_af
#print axioms nativeGK4AMHalf_ah
#print axioms nativeGK4AMOddWord
#print axioms nativeGK4AMOddWord_count
#print axioms nativeGK4AMOddWord_ad
#print axioms nativeGK4AMOddWord_af
#print axioms nativeGK4AMOddWord_decoder
#print axioms nativeGK4AMOddWord_oldValue
#print axioms nativeGK4AMOddClass
#print axioms nativeGK4AMOddClass_forget
#print axioms nativeGK4AMOddFiberPoint
#print axioms nativeGK4AMOddFiberPoint_decoder
#print axioms nativeGK4AMOdd_not_family
#print axioms nativeGK4AMFamilyCovers_succ_false
#print axioms nativeGK4AMFamilyCovers_positive_false
#print axioms nativeGK4AMPhysicalNorth_positive_family_noncoverage

end
end Kuu.F112.Physical
