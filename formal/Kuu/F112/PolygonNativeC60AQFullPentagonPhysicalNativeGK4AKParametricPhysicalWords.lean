import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4AJExactMatrixFiber
import Mathlib.Tactic

/-!
F112-P94D3GK4AK — parametric ORIGINAL F54 typed words with a
common old GK4AG observation and an exact second-matrix decoder.
Let P=B^6, where B is the real two-edge LocalRotation backtrack.
W(j,d)=P^j ; C ; P^(2*d) ; C ; P^j uses only actual F54 constructors.
For j+d=k the old four coordinates and first matrix depend only on k.
The second matrix satisfies 4*b+2*d_entry-2*a-c = 8-192*d.
This is the even-index subfamily of the previous proposed family,
not a new untyped source generator or an assumed source equation.
All earlier Type-valued F55/P92B/seam soundness remains unchanged.
No original Q category axioms, no S->K_AI global faithfulness,
no infinite single-fiber claim, no Gray or hyperdescent.
Append-only/same-root107. Strict 空 central; independent Kuu one
presentation. Protected validation-only #1558 remains unmerged.
Lean v4.30.0-rc2; mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
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

/-- Closed second-matrix value of n genuinely witnessed B^6 blocks. -/
def nativeGK4AKPowerMatrix (n : Nat) : NativeGK4AHMatrix :=
  ((1 + 12 * (n : Int), 6 * (n : Int)),
    (-24 * (n : Int), 1 - 12 * (n : Int)))

/-- A linear integer measurement of the full second matrix.
It is used only AFTER the certified original Type-cell descent. -/
def nativeGK4AKDecoder (M : NativeGK4AHMatrix) : Int :=
  4 * M.1.2 + 2 * M.2.2 - 2 * M.1.1 - M.2.1

/-- Actual old four-observation plus full first matrix, with the
zero-length boundary case retained rather than assuming k>0. -/
def nativeGK4AKOldValue (k : Nat) : NativeGK4AGValue :=
  ((decide (k = 0), ((2 - 24 * (k : Int), 12 * k),
    12 * (k : Int) - 144 * (k : Int) ^ 2)),
    ((1, 2), (0, 1)))

section OriginalTypedPowers
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E} {n m : Nat}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {before after : KuuNativeF45Tree p n m ma pa mb pb}
variable (rot : KuuNativeF45Tree.LocalRotation p before after)

/-- Genuine original F54 power of the SIX physical backtracks.
At zero use the original zero-edge RotationChain, not a Q identity law. -/
def nativeGK4AKTower : Nat → KuuNativeF45Tree.DepthRotationRoute p before before
  | 0 => .chain (.refl before)
  | k + 1 => .trans (nativeGK4AKTower k) (nativeGK4AHBacktrackSix rot)

/-- The fixed six-backtrack block has twelve actual rotation edges. -/
theorem nativeGK4AKSix_count :
    (nativeGK4AHBacktrackSix rot).rotationCount = 12 := by rfl

theorem nativeGK4AKSix_ad :
    (nativeGK4AHBacktrackSix rot).gk4adValue =
      (((-12 : Int), (6 : Nat)), (-36 : Int)) := by rfl

theorem nativeGK4AKSix_af :
    (nativeGK4AHBacktrackSix rot).gk4afMatrix = nativeGK4AFOne := by rfl

theorem nativeGK4AKSix_ah :
    (nativeGK4AHBacktrackSix rot).gk4ahMatrix =
      (((13 : Int), (6 : Int)), ((-24 : Int), (-11 : Int))) := by rfl

theorem nativeGK4AKCast_count
    (tree : KuuNativeF45Tree p n m ma pa mb pb) :
    (nativeGK4WCastRoute tree).rotationCount = 0 := by rfl

theorem nativeGK4AKCast_ad
    (tree : KuuNativeF45Tree p n m ma pa mb pb) :
    (nativeGK4WCastRoute tree).gk4adValue = ((1, 0), 0) := by rfl

theorem nativeGK4AKCast_af
    (tree : KuuNativeF45Tree p n m ma pa mb pb) :
    (nativeGK4WCastRoute tree).gk4afMatrix = nativeGK4AFCast := by rfl

theorem nativeGK4AKCast_ah
    (tree : KuuNativeF45Tree p n m ma pa mb pb) :
    (nativeGK4WCastRoute tree).gk4ahMatrix = nativeGK4AHCast := by rfl

/-- True original physical count, by induction on constructed source. -/
theorem nativeGK4AKTower_count (k : Nat) :
    (nativeGK4AKTower rot k).rotationCount = 12 * k := by
  induction k with
  | zero => rfl
  | succ k ih =>
      change (nativeGK4AKTower rot k).rotationCount +
        (nativeGK4AHBacktrackSix rot).rotationCount = 12 * (k + 1)
      rw [ih, nativeGK4AKSix_count]
      omega

/-- Noncommutative ordered moment of B^(6k), not just a count. -/
theorem nativeGK4AKTower_ad (k : Nat) :
    (nativeGK4AKTower rot k).gk4adValue =
      ((-12 * (k : Int), 6 * k), -36 * (k : Int) ^ 2) := by
  induction k with
  | zero => rfl
  | succ k ih =>
      change nativeGK4ADCombine (nativeGK4AKTower rot k).gk4adValue
        (nativeGK4AHBacktrackSix rot).gk4adValue = _
      rw [ih, nativeGK4AKSix_ad]
      apply Prod.ext
      · apply Prod.ext
        · simp [nativeGK4ADCombine] <;> ring
        · simp [nativeGK4ADCombine] <;> omega
      · simp [nativeGK4ADCombine] <;> ring

/-- The old matrix erases every whole six-backtrack block. -/
theorem nativeGK4AKTower_af (k : Nat) :
    (nativeGK4AKTower rot k).gk4afMatrix = nativeGK4AFOne := by
  induction k with
  | zero => rfl
  | succ k ih =>
      change nativeGK4AFMul (nativeGK4AKTower rot k).gk4afMatrix
        (nativeGK4AHBacktrackSix rot).gk4afMatrix = nativeGK4AFOne
      rw [ih, nativeGK4AKSix_af, nativeGK4AFMul_leftUnit]

/-- The second representation retains the exact unbounded power. -/
theorem nativeGK4AKTower_ah (k : Nat) :
    (nativeGK4AKTower rot k).gk4ahMatrix = nativeGK4AKPowerMatrix k := by
  induction k with
  | zero => rfl
  | succ k ih =>
      change nativeGK4AHMul (nativeGK4AKTower rot k).gk4ahMatrix
        (nativeGK4AHBacktrackSix rot).gk4ahMatrix = nativeGK4AKPowerMatrix (k + 1)
      rw [ih, nativeGK4AKSix_ah]
      apply Prod.ext
      · apply Prod.ext <;> simp [nativeGK4AHMul, nativeGK4AKPowerMatrix] <;> ring
      · apply Prod.ext <;> simp [nativeGK4AHMul, nativeGK4AKPowerMatrix] <;> ring

/-- W(j,d)=B^(6j) C B^(12d) C B^(6j), a genuine original F54
self-route with all true LocalRotation and dependent tree witnesses. -/
def nativeGK4AKWord (j d : Nat) :
    KuuNativeF45Tree.DepthRotationRoute p before before :=
  .trans (nativeGK4AKTower rot j)
    (.trans (nativeGK4WCastRoute before)
      (.trans (nativeGK4AKTower rot (2 * d))
        (.trans (nativeGK4WCastRoute before) (nativeGK4AKTower rot j))))

theorem nativeGK4AKWord_count (j d : Nat) :
    (nativeGK4AKWord rot j d).rotationCount = 24 * (j + d) := by
  simp only [nativeGK4AKWord, nativeGK4H_raw_rotationCount_compose,
    nativeGK4AKTower_count, nativeGK4AKCast_count]
  omega

theorem nativeGK4AKWord_grade (j d : Nat) :
    nativeGK4GRawGrade before before (nativeGK4AKWord rot j d) =
      decide (j + d = 0) := by
  simp [nativeGK4GRawGrade, nativeGK4AKWord_count]

/-- The old ordered four-observation is independent of the internal
split j,d once their sum is fixed. -/
theorem nativeGK4AKWord_ad (j d : Nat) :
    (nativeGK4AKWord rot j d).gk4adValue =
      ((2 - 24 * ((j + d : Nat) : Int), 12 * (j + d)),
        12 * ((j + d : Nat) : Int) - 144 * ((j + d : Nat) : Int) ^ 2) := by
  simp only [nativeGK4AKWord, nativeGK4AD_trans,
    nativeGK4AKTower_ad, nativeGK4AKCast_ad]
  apply Prod.ext
  · apply Prod.ext
    · simp [nativeGK4ADCombine] <;> ring
    · simp [nativeGK4ADCombine] <;> omega
  · simp [nativeGK4ADCombine] <;> ring

theorem nativeGK4AKWord_af (j d : Nat) :
    (nativeGK4AKWord rot j d).gk4afMatrix = ((1, 2), (0, 1)) := by
  simp [nativeGK4AKWord, nativeGK4AF_trans, nativeGK4AKTower_af,
    nativeGK4AKCast_af, nativeGK4AFMul, nativeGK4AFOne, nativeGK4AFCast]

/-- Exact linear decoder on the second matrix. The cubic entries
cancel, leaving the genuine middle-block parameter d. -/
theorem nativeGK4AKWord_decoder (j d : Nat) :
    nativeGK4AKDecoder (nativeGK4AKWord rot j d).gk4ahMatrix =
      8 - 192 * (d : Int) := by
  simp only [nativeGK4AKWord, nativeGK4AH_trans,
    nativeGK4AKTower_ah, nativeGK4AKCast_ah]
  simp [nativeGK4AKDecoder, nativeGK4AHMul,
    nativeGK4AKPowerMatrix, nativeGK4AHCast] <;> ring

/-- SAME old AG value on genuine original S classes whenever j+d=k.
No equality of original S routes or P92B Type-cells is inferred. -/
theorem nativeGK4AKWord_oldValue (j d : Nat) :
    nativeGK4AGStructural before before
      (nativeGK4EStructuralRouteClass before before (nativeGK4AKWord rot j d)) =
      nativeGK4AKOldValue (j + d) := by
  change ((nativeGK4GRawGrade before before (nativeGK4AKWord rot j d),
      (nativeGK4AKWord rot j d).gk4adValue),
      (nativeGK4AKWord rot j d).gk4afMatrix) = nativeGK4AKOldValue (j + d)
  apply Prod.ext
  · apply Prod.ext
    · exact nativeGK4AKWord_grade rot j d
    · exact nativeGK4AKWord_ad rot j d
  · exact nativeGK4AKWord_af rot j d

end OriginalTypedPowers

#print axioms nativeGK4AKPowerMatrix
#print axioms nativeGK4AKDecoder
#print axioms nativeGK4AKOldValue
#print axioms nativeGK4AKTower
#print axioms nativeGK4AKSix_count
#print axioms nativeGK4AKSix_ad
#print axioms nativeGK4AKSix_af
#print axioms nativeGK4AKSix_ah
#print axioms nativeGK4AKCast_count
#print axioms nativeGK4AKCast_ad
#print axioms nativeGK4AKCast_af
#print axioms nativeGK4AKCast_ah
#print axioms nativeGK4AKTower_count
#print axioms nativeGK4AKTower_ad
#print axioms nativeGK4AKTower_af
#print axioms nativeGK4AKTower_ah
#print axioms nativeGK4AKWord
#print axioms nativeGK4AKWord_count
#print axioms nativeGK4AKWord_grade
#print axioms nativeGK4AKWord_ad
#print axioms nativeGK4AKWord_af
#print axioms nativeGK4AKWord_decoder
#print axioms nativeGK4AKWord_oldValue

end
end Kuu.F112.Physical
