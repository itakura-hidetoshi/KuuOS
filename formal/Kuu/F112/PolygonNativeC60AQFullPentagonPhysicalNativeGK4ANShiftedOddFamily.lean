import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4AMUniformNoncoverage
import Mathlib.Tactic

/-!
F112-P94D3GK4AN — genuine shifted ODD half-backtrack finite family.
Previously GK4AK showed k+1 distinct TRUE F54 paths above q_k;
GK4AM provided one additional odd witness for every k>0.
This stage supplies ALL k complementary odd witnesses over the same
q_k, with certified exact decoder, not untyped abstract matrices.

P=B^6, H=B^3, C=original double Nat cast. For j,d : Nat,
  Odd(j,d) = P^j ; (H ; C ; P^(2d+1) ; C ; H) ; P^j.
Its FULL old GK4AG class equals q_(j+d+1), while its independently
seam-sound new 2x2 matrix has linear decoder -88-192*d.
Existing GK4AK even indices decode to 8-192*d, so all odd points
are distinct from each other and from every even point in q_k.
True original source F55/P92B/seam evidence remains unchanged.
Neither a fixed infinite fiber nor global S->K_AI faithfulness is
claimed. Append-only/tighten-only/same-root107. Strict 空 central,
independent Kuu one presentation, no Gray. Protect draft PR #1558.
Pinned Lean v4.30.0-rc2 / mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
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

section GenuineOddFamily
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E} {n m : Nat}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {before after : KuuNativeF45Tree p n m ma pa mb pb}
variable (rot : KuuNativeF45Tree.LocalRotation p before after)

/-- A FULLY original F54 typed word with P^j wrapped around
the genuine GK4AM odd half-backtrack word. -/
def nativeGK4ANShiftedOddWord (j d : Nat) :
    KuuNativeF45Tree.DepthRotationRoute p before before :=
  .trans (nativeGK4AKTower rot j)
    (.trans (nativeGK4AMOddWord rot d) (nativeGK4AKTower rot j))

theorem nativeGK4ANShiftedOddWord_count (j d : Nat) :
    (nativeGK4ANShiftedOddWord rot j d).rotationCount =
      24 * (j + d + 1) := by
  simp only [nativeGK4ANShiftedOddWord, nativeGK4H_raw_rotationCount_compose,
    nativeGK4AKTower_count, nativeGK4AMOddWord_count]
  omega

theorem nativeGK4ANShiftedOddWord_ad (j d : Nat) :
    (nativeGK4ANShiftedOddWord rot j d).gk4adValue =
      ((2 - 24 * ((j + d + 1 : Nat) : Int), 12 * (j + d + 1)),
        12 * ((j + d + 1 : Nat) : Int) -
          144 * ((j + d + 1 : Nat) : Int) ^ 2) := by
  simp only [nativeGK4ANShiftedOddWord, nativeGK4AD_trans,
    nativeGK4AKTower_ad, nativeGK4AMOddWord_ad]
  apply Prod.ext
  · apply Prod.ext
    · simp [nativeGK4ADCombine] <;> ring
    · simp [nativeGK4ADCombine] <;> omega
  · simp [nativeGK4ADCombine] <;> ring

theorem nativeGK4ANShiftedOddWord_af (j d : Nat) :
    (nativeGK4ANShiftedOddWord rot j d).gk4afMatrix =
      (((1 : Int), (2 : Int)), ((0 : Int), (1 : Int))) := by
  simp only [nativeGK4ANShiftedOddWord, nativeGK4AF_trans,
    nativeGK4AKTower_af, nativeGK4AMOddWord_af]
  norm_num [nativeGK4AFMul, nativeGK4AFOne]

/-- Exact full second-matrix decoder: external P towers disappear
from THIS linear form, but not generally from the whole matrix. -/
theorem nativeGK4ANShiftedOddWord_decoder (j d : Nat) :
    nativeGK4AKDecoder (nativeGK4ANShiftedOddWord rot j d).gk4ahMatrix =
      -88 - 192 * (d : Int) := by
  simp only [nativeGK4ANShiftedOddWord, nativeGK4AMOddWord,
    nativeGK4AH_trans, nativeGK4AKTower_ah, nativeGK4AMHalf_ah,
    nativeGK4AKCast_ah]
  simp [nativeGK4AKDecoder, nativeGK4AHMul,
    nativeGK4AKPowerMatrix, nativeGK4AHCast] <;> ring

theorem nativeGK4ANShiftedOddWord_oldValue (j d : Nat) :
    nativeGK4AGStructural before before
      (nativeGK4EStructuralRouteClass before before
        (nativeGK4ANShiftedOddWord rot j d)) =
      nativeGK4AKOldValue (j + d + 1) := by
  change ((nativeGK4GRawGrade before before
      (nativeGK4ANShiftedOddWord rot j d),
      (nativeGK4ANShiftedOddWord rot j d).gk4adValue),
      (nativeGK4ANShiftedOddWord rot j d).gk4afMatrix) = _
  apply Prod.ext
  · apply Prod.ext
    · simp [nativeGK4GRawGrade, nativeGK4ANShiftedOddWord_count,
        nativeGK4AKOldValue]
    · exact nativeGK4ANShiftedOddWord_ad rot j d
  · exact nativeGK4ANShiftedOddWord_af rot j d

/-- For i : Fin k, the integer d=k-1-i gives exactly k distinct
odd points in the same q_k, including k=0 vacuously. -/
def nativeGK4ANOddClass (k : Nat) (i : Fin k) :
    NativeGK4SKernelClasses (nativeGK4AIP92Family p D E) before before :=
  nativeGK4AIComparison before before
    (nativeGK4EStructuralRouteClass before before
      (nativeGK4ANShiftedOddWord rot i.val (k - 1 - i.val)))

theorem nativeGK4ANOddClass_forget (k : Nat) (i : Fin k) :
    nativeGK4AIForgetMatrix before before (nativeGK4ANOddClass rot k i) =
      nativeGK4AKOldTarget rot k := by
  change nativeGK4AIForgetMatrix before before
    (nativeGK4AIComparison before before
      (nativeGK4EStructuralRouteClass before before
        (nativeGK4ANShiftedOddWord rot i.val (k - 1 - i.val)))) =
    nativeGK4AGComparison before before
      (nativeGK4EStructuralRouteClass before before (nativeGK4AKWord rot 0 k))
  rw [nativeGK4AIForgetMatrix_comparison]
  apply (nativeGK4AGComparison_eq_iff before before _ _).mpr
  rw [nativeGK4ANShiftedOddWord_oldValue, nativeGK4AKWord_oldValue]
  have hi := i.isLt
  have hsum : i.val + (k - 1 - i.val) + 1 = k := by omega
  simpa only [Nat.zero_add, hsum]

def nativeGK4ANOddFiberPoint (k : Nat) (i : Fin k) :
    nativeGK4AJOldFiber before before (nativeGK4AKOldTarget rot k) :=
  ⟨nativeGK4ANOddClass rot k i, nativeGK4ANOddClass_forget rot k i⟩

theorem nativeGK4ANOddFiberPoint_decoder (k : Nat) (i : Fin k) :
    nativeGK4AKDecoder
      (nativeGK4AJFiberMatrix before before
        (nativeGK4AKOldTarget rot k) (nativeGK4ANOddFiberPoint rot k i)) =
      -88 - 192 * ((k - 1 - i.val : Nat) : Int) := by
  change nativeGK4AKDecoder
    (nativeGK4ANShiftedOddWord rot i.val (k - 1 - i.val)).gk4ahMatrix = _
  exact nativeGK4ANShiftedOddWord_decoder rot i.val (k - 1 - i.val)

/-- ALL k shifted odd members are pairwise distinct in the same
actual dependent fiber, using the genuine second-matrix decoder. -/
theorem nativeGK4ANOddFiberPoint_injective (k : Nat) :
    Function.Injective (nativeGK4ANOddFiberPoint rot k) := by
  intro i j h
  have hd := congrArg
    (fun z : nativeGK4AJOldFiber before before (nativeGK4AKOldTarget rot k) =>
      nativeGK4AKDecoder
        (nativeGK4AJFiberMatrix before before (nativeGK4AKOldTarget rot k) z)) h
  change nativeGK4AKDecoder
      (nativeGK4AJFiberMatrix before before
        (nativeGK4AKOldTarget rot k) (nativeGK4ANOddFiberPoint rot k i)) =
    nativeGK4AKDecoder
      (nativeGK4AJFiberMatrix before before
        (nativeGK4AKOldTarget rot k) (nativeGK4ANOddFiberPoint rot k j)) at hd
  rw [nativeGK4ANOddFiberPoint_decoder rot k i,
      nativeGK4ANOddFiberPoint_decoder rot k j] at hd
  apply Fin.ext
  have hi := i.isLt
  have hj := j.isLt
  omega

/-- No odd source can equal any original GK4AK even source in q_k.
The decoders are 96 apart modulo 192, not merely numerically checked. -/
theorem nativeGK4ANOdd_ne_even (k : Nat) (i : Fin k) (j : Fin (k + 1)) :
    nativeGK4ANOddFiberPoint rot k i ≠ nativeGK4AKFiberPoint rot k j := by
  intro h
  have hd := congrArg
    (fun z : nativeGK4AJOldFiber before before (nativeGK4AKOldTarget rot k) =>
      nativeGK4AKDecoder
        (nativeGK4AJFiberMatrix before before (nativeGK4AKOldTarget rot k) z)) h
  change nativeGK4AKDecoder
      (nativeGK4AJFiberMatrix before before
        (nativeGK4AKOldTarget rot k) (nativeGK4ANOddFiberPoint rot k i)) =
    nativeGK4AKDecoder
      (nativeGK4AJFiberMatrix before before
        (nativeGK4AKOldTarget rot k) (nativeGK4AKFiberPoint rot k j)) at hd
  rw [nativeGK4ANOddFiberPoint_decoder rot k i] at hd
  change (-88 - 192 * ((k - 1 - i.val : Nat) : Int)) =
    nativeGK4AKDecoder
      (nativeGK4AIKernelValue before before (nativeGK4AKClass rot k j)).2 at hd
  rw [nativeGK4AKClass_decoder rot k j] at hd
  have hi := i.isLt
  have hj := j.isLt
  omega

#print axioms nativeGK4ANShiftedOddWord
#print axioms nativeGK4ANShiftedOddWord_count
#print axioms nativeGK4ANShiftedOddWord_ad
#print axioms nativeGK4ANShiftedOddWord_af
#print axioms nativeGK4ANShiftedOddWord_decoder
#print axioms nativeGK4ANShiftedOddWord_oldValue
#print axioms nativeGK4ANOddClass
#print axioms nativeGK4ANOddClass_forget
#print axioms nativeGK4ANOddFiberPoint
#print axioms nativeGK4ANOddFiberPoint_decoder
#print axioms nativeGK4ANOddFiberPoint_injective
#print axioms nativeGK4ANOdd_ne_even

end GenuineOddFamily
end
end Kuu.F112.Physical
