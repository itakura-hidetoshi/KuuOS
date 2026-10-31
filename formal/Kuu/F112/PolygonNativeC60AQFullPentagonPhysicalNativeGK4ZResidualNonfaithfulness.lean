import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4ZBackwardCountInvariant
import Mathlib.Tactic

/-!
F112-P94D3GK4Z — genuine residual NONFAITHFULNESS even after GK4X charge.

Use the existing REAL original F54 forward/backward two-edge rotation
backtrack GK4F, not a synthetic loop. Each such backtrack has two
physical rotations, exactly one stored backward Type-valued edge,
zero depth casts, Boolean=false, and castCharge=-2. Compose two actual
depth-cast identity proof constructors with one backtrack: the resulting
true F54 self-route has backward count one, signed castCharge zero.
Repeatedly compose this BALANCED proof route with an initial backtrack.

This produces genuine fully dependent F45 original F54 Type-valued
routes R_k with exactly
  backwardCount(R_k) = k+1,
  castCharge(R_k) = -2,
  rotationCount(R_k) = 2*(k+1),
  O_X(R_k) = (false,-2).
GK4Z's ALL-original / ALL-structural comparison soundness of
backwardCount proves the independent GK4E structural quotient classes
[R_k]_S are ALL DISTINCT, although the existing GK4X reinforced
observation and genuine GK4Y S -> SECOND observer-kernel quotient
identifies every one. This proves a concrete nonfaithfulness of the
ENHANCED GK4X/GK4Y comparison at every actual F45 local rotation,
including genuine physical C60 north triple. The residual structural
fiber is countably infinite at physical C60 north by the already
proved countability of S there.

This does NOT assert any original P92B identity/associativity, a
reconstructed original P92B Type-valued comparison cell from numeric
equality, unconditional old 14D Countable, 19D filler, global
strict n, historical complete typed equivalence or hyperdescent.

Strict 空 central; independent Kuu one presentation, no Gray.
Append-only, same-root, 107 public roots, overwrite forbidden.
Lean v4.30.0-rc2, mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Protect validation-only PR #1558 Draft/open/unmerged.
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

section RealBalancedBacktracks
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E} {n m : Nat}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable {before after : KuuNativeF45Tree p n m ma pa mb pb}
variable (rot : KuuNativeF45Tree.LocalRotation p before after)

/-- A real original GK4F forward-then-backward physical loop has
one stored backward rotation certificate, not an external inverse. -/
@[simp] theorem nativeGK4ZBacktrack_backwardCount :
    (nativeGK4FBacktrack rot).gk4zBackwardCount = 1 := by
  rfl

/-- GK4W charge of the actual two-edge original backtrack is -2. -/
@[simp] theorem nativeGK4ZBacktrack_charge :
    (nativeGK4FBacktrack rot).gk4wCastCharge = (-2 : Int) := by
  rfl

/-- Source generator with two ACTUAL F54 castDepths constructors
and one GK4F genuine backtrack. It has nontrivial proof history,
backwardCount=1, rotationCount=2, but castCharge=0. -/
def nativeGK4ZBalancedStep :
    KuuNativeF45Tree.DepthRotationRoute p before before :=
  .trans (nativeGK4WCastRoute before)
    (.trans (nativeGK4WCastRoute before) (nativeGK4FBacktrack rot))

@[simp] theorem nativeGK4ZBalancedStep_backward :
    (nativeGK4ZBalancedStep rot).gk4zBackwardCount = 1 := by
  rfl

@[simp] theorem nativeGK4ZBalancedStep_rotation :
    (nativeGK4ZBalancedStep rot).rotationCount = 2 := by
  rfl

@[simp] theorem nativeGK4ZBalancedStep_charge :
    (nativeGK4ZBalancedStep rot).gk4wCastCharge = (0 : Int) := by
  rw [nativeGK4ZBalancedStep, nativeGK4W_charge_trans,
    nativeGK4W_charge_trans, nativeGK4WCastRoute_charge,
    nativeGK4WCastRoute_charge, nativeGK4ZBacktrack_charge]
  omega

/-- Recursively concatenate ACTUAL balanced F54 proof words to the
original genuine F54 backtrack without identifying distinct proofs. -/
def nativeGK4ZBalancedTower : Nat →
    KuuNativeF45Tree.DepthRotationRoute p before before
  | 0 => nativeGK4FBacktrack rot
  | k + 1 => .trans (nativeGK4ZBalancedStep rot) (nativeGK4ZBalancedTower k)

/-- Every extra balanced F54 word adds ONE actual stored backward
rotation while preserving the fully dependent original endpoints. -/
theorem nativeGK4ZBalancedTower_backward (k : Nat) :
    (nativeGK4ZBalancedTower rot k).gk4zBackwardCount = k + 1 := by
  induction k with
  | zero => rfl
  | succ k ih =>
      change (nativeGK4ZBalancedStep rot).gk4zBackwardCount +
        (nativeGK4ZBalancedTower rot k).gk4zBackwardCount = k + 1 + 1
      rw [nativeGK4ZBalancedStep_backward, ih]
      omega

/-- Signed castCharge is EXACTLY -2 at EVERY stage, independent of
the infinitely growing original backward evidence and cast count. -/
theorem nativeGK4ZBalancedTower_charge (k : Nat) :
    (nativeGK4ZBalancedTower rot k).gk4wCastCharge = (-2 : Int) := by
  induction k with
  | zero => exact nativeGK4ZBacktrack_charge rot
  | succ k ih =>
      rw [nativeGK4ZBalancedTower, nativeGK4W_charge_trans,
        nativeGK4ZBalancedStep_charge, ih]
      omega

/-- The physical edge count increases exactly by TWO per stage. -/
theorem nativeGK4ZBalancedTower_rotation (k : Nat) :
    (nativeGK4ZBalancedTower rot k).rotationCount = 2 * (k + 1) := by
  induction k with
  | zero => rfl
  | succ k ih =>
      change (nativeGK4ZBalancedStep rot).rotationCount +
        (nativeGK4ZBalancedTower rot k).rotationCount = 2 * (k + 1 + 1)
      rw [nativeGK4ZBalancedStep_rotation, ih]
      omega

/-- ALL original balanced tower classes have the SAME actual enhanced
GK4X value (Boolean=false, castCharge=-2). -/
theorem nativeGK4ZBalancedTower_observation (k : Nat) :
    nativeGK4XEnhancedStructural before before
        (nativeGK4EStructuralRouteClass before before
          (nativeGK4ZBalancedTower rot k)) =
      (false, (-2 : Int)) := by
  apply Prod.ext
  · change decide ((nativeGK4ZBalancedTower rot k).rotationCount = 0) = false
    rw [nativeGK4ZBalancedTower_rotation]
    have hk : 2 * (k + 1) ≠ (0 : Nat) := by omega
    simp only [hk, decide_False]
  · exact nativeGK4ZBalancedTower_charge rot k

/-- These original source proofs are GENUINELY DIFFERENT in the
independently extended STRUCTURAL quotient S: every original P92B
3-cell and separate F54 structural seam preserves backward count. -/
theorem nativeGK4ZBalancedTower_structural_injective :
    Function.Injective
      (fun k : Nat => nativeGK4EStructuralRouteClass before before
        (nativeGK4ZBalancedTower rot k)) := by
  intro i j heq
  have hb := congrArg (nativeGK4ZBackwardStructural before before) heq
  change (nativeGK4ZBalancedTower rot i).gk4zBackwardCount =
    (nativeGK4ZBalancedTower rot j).gk4zBackwardCount at hb
  rw [nativeGK4ZBalancedTower_backward, nativeGK4ZBalancedTower_backward] at hb
  omega

/-- The verified GK4X enhanced comparison map identifies ALL tower
classes, though they are distinct already as original structural
classes; no new original Type-valued 3-cell is inferred. -/
theorem nativeGK4ZBalancedTower_comparison_constant (i j : Nat) :
    nativeGK4XEnhancedComparison before before
      (nativeGK4EStructuralRouteClass before before
        (nativeGK4ZBalancedTower rot i)) =
    nativeGK4XEnhancedComparison before before
      (nativeGK4EStructuralRouteClass before before
        (nativeGK4ZBalancedTower rot j)) := by
  apply (nativeGK4XEnhancedComparison_eq_iff before before _ _).mpr
  rw [nativeGK4ZBalancedTower_observation,
    nativeGK4ZBalancedTower_observation]

/-- MAIN no-go: actual S->K_X comparison is NOT injective at EVERY
original F45 tree with a witnessed TRUE F54 local rotation. -/
theorem nativeGK4ZEnhancedComparison_not_injective :
    ¬ Function.Injective
      (nativeGK4XEnhancedComparison before before) := by
  intro hinj
  have heq := nativeGK4ZBalancedTower_comparison_constant rot 0 1
  have hstruct := hinj heq
  have hidx := nativeGK4ZBalancedTower_structural_injective rot hstruct
  omega

/-- A TRUE residual fiber of genuine independent structural
classes with precisely the SAME GK4X enhanced value (false,-2).
It is not a synthetic raw word equivalence and not the full S Hom. -/
abbrev NativeGK4ZResidualStructuralFiber :=
  {s : NativeGK4EStructuralRouteClasses before before //
    nativeGK4XEnhancedStructural before before s = (false, (-2 : Int))}

/-- Actual F54 balanced towers land in the SAME original structural
enhanced-observation fiber with original complete Type-valued proofs. -/
def nativeGK4ZResidualTowerFiber (k : Nat) :
    NativeGK4ZResidualStructuralFiber rot :=
  ⟨nativeGK4EStructuralRouteClass before before
      (nativeGK4ZBalancedTower rot k),
    nativeGK4ZBalancedTower_observation rot k⟩

/-- This residual fiber is infinite for ANY TRUE local rotation. -/
theorem nativeGK4ZResidualTowerFiber_injective :
    Function.Injective (nativeGK4ZResidualTowerFiber rot) := by
  intro i j hij
  exact nativeGK4ZBalancedTower_structural_injective rot
    (congrArg Subtype.val hij)

end RealBalancedBacktracks

section RealPhysicalNorth

/-- The genuine physical C60 north F45 triple has an actual
assoc LocalRotation and the above original source proof tower;
enhanced structural->K_X comparison is nonfaithful unconditionally. -/
theorem nativeGK4Z_physical_north_enhanced_nonfaithful :
    ¬ Function.Injective
      (nativeGK4XEnhancedComparison
        nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple) := by
  exact nativeGK4ZEnhancedComparison_not_injective northHexagonNativeLeftRotation

/-- The residual enhanced-observation fiber itself has cardinal
aleph-null at the ACTUAL physical C60 north triple, from a genuine
Nat-injective original F54 tower and the separately proved
physical original S Hom countability. No generic D/E countability
hypothesis is silently dropped. -/
theorem nativeGK4Z_physical_north_residual_fiber_aleph0 :
    Cardinal.mk (NativeGK4ZResidualStructuralFiber
      northHexagonNativeLeftRotation) = Cardinal.aleph0 := by
  letI : Countable (NativeGK4EStructuralRouteClasses
      nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple) :=
    (nativeGK4G_physical_north_structural_countable_and_graded).1
  letI : Countable (NativeGK4ZResidualStructuralFiber
      northHexagonNativeLeftRotation) := inferInstance
  letI : Infinite (NativeGK4ZResidualStructuralFiber
      northHexagonNativeLeftRotation) :=
    Infinite.of_injective (nativeGK4ZResidualTowerFiber
      northHexagonNativeLeftRotation)
      (nativeGK4ZResidualTowerFiber_injective northHexagonNativeLeftRotation)
  exact Cardinal.mk_eq_aleph0 _

/-- The exact single enhanced K_X value class at physical north
has infinitely many distinct structural preimages: this is a
NONTRIVIAL concrete loss of information in a genuine second
observer-kernel quotient, not merely an ambient Bool×Int map. -/
theorem nativeGK4Z_physical_north_same_kernel_infinite :
    ∃ z : NativeGK4SKernelClasses
        (nativeGK4XEnhancedP92Family _ _ _)
        nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple,
      ∃ tower : Nat → NativeGK4EStructuralRouteClasses
          nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple,
        Function.Injective tower ∧
        ∀ k, nativeGK4XEnhancedComparison
            nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple
              (tower k) = z := by
  let tower : Nat → NativeGK4EStructuralRouteClasses
      nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple :=
    fun k => nativeGK4EStructuralRouteClass
      nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple
      (nativeGK4ZBalancedTower northHexagonNativeLeftRotation k)
  refine ⟨nativeGK4XEnhancedComparison
    nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple (tower 0),
      tower, ?_, ?_⟩
  · exact nativeGK4ZBalancedTower_structural_injective
      northHexagonNativeLeftRotation
  · intro k
    exact nativeGK4ZBalancedTower_comparison_constant
      northHexagonNativeLeftRotation k 0

end RealPhysicalNorth

#print axioms nativeGK4ZBacktrack_backwardCount
#print axioms nativeGK4ZBacktrack_charge
#print axioms nativeGK4ZBalancedStep
#print axioms nativeGK4ZBalancedStep_backward
#print axioms nativeGK4ZBalancedStep_rotation
#print axioms nativeGK4ZBalancedStep_charge
#print axioms nativeGK4ZBalancedTower
#print axioms nativeGK4ZBalancedTower_backward
#print axioms nativeGK4ZBalancedTower_charge
#print axioms nativeGK4ZBalancedTower_rotation
#print axioms nativeGK4ZBalancedTower_observation
#print axioms nativeGK4ZBalancedTower_structural_injective
#print axioms nativeGK4ZBalancedTower_comparison_constant
#print axioms nativeGK4ZEnhancedComparison_not_injective
#print axioms NativeGK4ZResidualStructuralFiber
#print axioms nativeGK4ZResidualTowerFiber
#print axioms nativeGK4ZResidualTowerFiber_injective
#print axioms nativeGK4Z_physical_north_enhanced_nonfaithful
#print axioms nativeGK4Z_physical_north_residual_fiber_aleph0
#print axioms nativeGK4Z_physical_north_same_kernel_infinite

end
end Kuu.F112.Physical
