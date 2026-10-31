import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4VBooleanFunctorSectionCriterion
import Mathlib.Tactic

/-!
F112-P94D3GK4W — genuinely conserved cast-depth minus rotation charge.

The frozen independent F54 route grammar remembers BOTH explicit
F19/F28 Nat casts and actual primitive F54 local-rotation edges.
The original P92B pentagon changes three rotations to two, but
each actual associator uses one explicit cast and one real rotation.
The SIGNED integer (#castDepths - #physical rotations) therefore
survives the original full P92B relation, including its naturality
generator, AND the independently extended F54 structural seams.

This is a new explicitly checked invariant of TRUE original Type-valued
route data, not a 3-cell created by numerical agreement. It will
separate distinct zero-physical-rotation STRUCTURAL route classes and
identify a true obstruction to GK4U Boolean observation faithfulness.

No original P92B associativity/units, historical complete typed equivalence,
unconditional genuine 14D Countable, 19D filler, global strict n,
hyperdescent or Gray. Append-only, same-root, 107 roots.
Pinned Lean v4.30.0-rc2/mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Protect PR #1558 Draft/open/unmerged.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE

section ActualCastCharge
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}

/-- Count the ACTUAL castDepths constructors on true F54 proofs.
Original chain edges contribute zero; dependent contexts transport
the precise count and vertical trans adds it. -/
def KuuNativeF45Tree.DepthRotationRoute.gk4wCastCount
    {n n' m m' : Nat}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) : Nat := by
  induction route with
  | chain _ => exact 0
  | castDepths _ _ _ => exact 1
  | trans _ _ ihLeft ihRight => exact ihLeft + ihRight
  | leftContext _ _ ih => exact ih
  | rightContext _ _ ih => exact ih

/-- Genuine signed charge, not original physical rotation count
and not a quotient of unsupported external proof syntax. -/
def KuuNativeF45Tree.DepthRotationRoute.gk4wCastCharge
    {n n' m m' : Nat}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) : Int :=
  (route.gk4wCastCount : Int) - (route.rotationCount : Int)

/-- This signed original F54 invariant is additive under genuine
vertical route composition on full dependent D/E F45 endpoints. -/
theorem nativeGK4W_charge_trans
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {first : KuuNativeF45Tree p n₁ m₁ ma pa mb pb}
    {middle : KuuNativeF45Tree p n₂ m₂ ma pa mb pb}
    {last : KuuNativeF45Tree p n₃ m₃ ma pa mb pb}
    (u : KuuNativeF45Tree.DepthRotationRoute p first middle)
    (v : KuuNativeF45Tree.DepthRotationRoute p middle last) :
    (KuuNativeF45Tree.DepthRotationRoute.trans u v).gk4wCastCharge =
      u.gk4wCastCharge + v.gk4wCastCharge := by
  change (((u.gk4wCastCount + v.gk4wCastCount : Nat) : Int) -
      ((u.rotationCount + v.rotationCount : Nat) : Int)) =
    ((u.gk4wCastCount : Int) - (u.rotationCount : Int)) +
      ((v.gk4wCastCount : Int) - (v.rotationCount : Int))
  omega

@[simp] theorem nativeGK4W_charge_leftContext
    {n n' m m' k l : Nat}
    {mc : KuuNativeBlocks a b} {pc : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (route : KuuNativeF45Tree.DepthRotationRoute p first last)
    (later : KuuNativeF45Tree p k l mb pb mc pc) :
    (KuuNativeF45Tree.DepthRotationRoute.leftContext route later).gk4wCastCharge =
      route.gk4wCastCharge := by
  rfl

@[simp] theorem nativeGK4W_charge_rightContext
    {k l n n' m m' : Nat}
    {mc : KuuNativeBlocks a b} {pc : KuuNativeBlocks x y}
    (earlier : KuuNativeF45Tree p k l ma pa mb pb)
    {first : KuuNativeF45Tree p n m mb pb mc pc}
    {last : KuuNativeF45Tree p n' m' mb pb mc pc}
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) :
    (KuuNativeF45Tree.DepthRotationRoute.rightContext earlier route).gk4wCastCharge =
      route.gk4wCastCharge := by
  rfl

/-- The ACTUAL F54 associator has ONE explicit Nat cast and ONE
physical rotation, so its signed charge is zero at every boundary. -/
@[simp] theorem nativeGK4W_charge_assoc
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {p₀ p₁ p₂ p₃ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
    (second : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
    (third : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃) :
    (KuuNativeF45Tree.DepthRotationRoute.assoc first second third).gk4wCastCharge =
      0 := by
  rfl

/-- The genuine F54 horizontal composition transports the same
signed charge, using both originally dependent binary contexts. -/
theorem nativeGK4W_charge_horizontal
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    (u : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter)
    (v : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter) :
    (nativeF54P90HorizontalRoute u v).gk4wCastCharge =
      u.gk4wCastCharge + v.gk4wCastCharge := by
  simp only [nativeF54P90HorizontalRoute, nativeGK4W_charge_trans,
    nativeGK4W_charge_leftContext, nativeGK4W_charge_rightContext]

/-- Actual P92B associator naturality has EQUAL signed cast-rotation
charges on its original two genuinely different F54 routes. -/
theorem nativeGK4W_charge_assocNaturality
    {n₁ n₁' n₂ n₂' n₃ n₃' m₁ m₁' m₂ m₂' m₃ m₃' : Nat}
    {p₀ p₁ p₂ p₃ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ : KuuNativeBlocks x y}
    {firstBefore : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁}
    {firstAfter : KuuNativeF45Tree p n₁' m₁' p₀ q₀ p₁ q₁}
    {secondBefore : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂}
    {secondAfter : KuuNativeF45Tree p n₂' m₂' p₁ q₁ p₂ q₂}
    {thirdBefore : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃}
    {thirdAfter : KuuNativeF45Tree p n₃' m₃' p₂ q₂ p₃ q₃}
    (u : KuuNativeF45Tree.DepthRotationRoute p firstBefore firstAfter)
    (v : KuuNativeF45Tree.DepthRotationRoute p secondBefore secondAfter)
    (w : KuuNativeF45Tree.DepthRotationRoute p thirdBefore thirdAfter) :
    (nativeF54P90AssocNaturalityLeftRoute u v w).gk4wCastCharge =
      (nativeF54P90AssocNaturalityRightRoute u v w).gk4wCastCharge := by
  simp only [nativeF54P90AssocNaturalityLeftRoute,
    nativeF54P90AssocNaturalityRightRoute,
    nativeGK4W_charge_trans, nativeGK4W_charge_horizontal,
    nativeGK4W_charge_assoc, add_zero, zero_add]
  omega

end ActualCastCharge

section FullOriginalProofPreservation
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable {n n' m m' : Nat}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}
variable {r s : KuuNativeF45Tree.DepthRotationRoute p first last}

/-- Original F55 ALL nine Type-valued comparison constructors
preserve the signed original cast/physical-rotation charge.
Crucially the 3-vs-2 original pentagon has 3-vs-2 casts as well. -/
theorem nativeGK4W_original_charge_sound
    (cell : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    r.gk4wCastCharge = s.gk4wCastCharge := by
  induction cell with
  | ident route => rfl
  | pentagon a b c d =>
      change (0 : Int) = 0
      rfl
  | disjointSquare left right =>
      change (-2 : Int) = -2
      rfl
  | symm cell ih => exact ih.symm
  | trans left right ihLeft ihRight => exact ihLeft.trans ihRight
  | leftContext cell later ih => exact ih
  | rightContext earlier cell ih => exact ih
  | precompose prior cell ih =>
      simp only [nativeGK4W_charge_trans]
      omega
  | postcompose cell suffix ih =>
      simp only [nativeGK4W_charge_trans]
      omega

/-- The independently added original P92B associator-naturality
generator is also sound; no unproved original 3-cell is manufactured. -/
theorem nativeGK4W_p92_charge_sound
    (cell : NativeF55P92AssocComparison p r s) :
    r.gk4wCastCharge = s.gk4wCastCharge := by
  induction cell with
  | original old => exact nativeGK4W_original_charge_sound old
  | assocNaturality u v w => exact nativeGK4W_charge_assocNaturality u v w
  | refl route => rfl
  | symm cell ih => exact ih.symm
  | trans left right ihLeft ihRight => exact ihLeft.trans ihRight
  | leftContext cell later ih => exact ih
  | rightContext earlier cell ih => exact ih
  | precompose prior cell ih =>
      simp only [nativeGK4W_charge_trans]
      omega
  | postcompose cell suffix ih =>
      simp only [nativeGK4W_charge_trans]
      omega

/-- Original genuine F54 structural seams preserve this charge too.
All FOUR context/compose congruences are checked on true source proofs. -/
theorem nativeGK4W_seam_charge_sound
    (seam : NativeF54StructuralSeam p r s) :
    r.gk4wCastCharge = s.gk4wCastCharge := by
  induction seam with
  | refl route => rfl
  | symm seam ih => exact ih.symm
  | trans left right ihLeft ihRight => exact ihLeft.trans ihRight
  | reassoc u v w =>
      simp only [nativeGK4W_charge_trans]
      omega
  | leftUnit route =>
      simp only [nativeGK4W_charge_trans]
      change (0 : Int) + route.gk4wCastCharge = route.gk4wCastCharge
      omega
  | rightUnit route =>
      simp only [nativeGK4W_charge_trans]
      change route.gk4wCastCharge + (0 : Int) = route.gk4wCastCharge
      omega
  | precompose prior seam ih =>
      simp only [nativeGK4W_charge_trans]
      omega
  | postcompose seam suffix ih =>
      simp only [nativeGK4W_charge_trans]
      omega
  | leftContextTrans u v later =>
      simp only [nativeGK4W_charge_leftContext, nativeGK4W_charge_trans]
  | rightContextTrans earlier u v =>
      simp only [nativeGK4W_charge_rightContext, nativeGK4W_charge_trans]
  | leftContextUnit earlier later => rfl
  | rightContextUnit earlier later => rfl
  | leftContextCongruence seam later ih => exact ih
  | rightContextCongruence earlier seam ih => exact ih

/-- The ACTUAL three-constructor extended structural comparison
is sound for cast-minus-rotation signed charge. This is a theorem
about Type-valued proof history, not a numerical shadow shortcut. -/
theorem nativeGK4W_structural_charge_sound
    (cell : NativeF55StructuralComparison p r s) :
    r.gk4wCastCharge = s.gk4wCastCharge := by
  induction cell with
  | original old => exact nativeGK4W_p92_charge_sound old
  | structural seam => exact nativeGK4W_seam_charge_sound seam
  | trans left right ihLeft ihRight => exact ihLeft.trans ihRight

end FullOriginalProofPreservation

#print axioms KuuNativeF45Tree.DepthRotationRoute.gk4wCastCount
#print axioms KuuNativeF45Tree.DepthRotationRoute.gk4wCastCharge
#print axioms nativeGK4W_charge_trans
#print axioms nativeGK4W_charge_leftContext
#print axioms nativeGK4W_charge_rightContext
#print axioms nativeGK4W_charge_assoc
#print axioms nativeGK4W_charge_horizontal
#print axioms nativeGK4W_charge_assocNaturality
#print axioms nativeGK4W_original_charge_sound
#print axioms nativeGK4W_p92_charge_sound
#print axioms nativeGK4W_seam_charge_sound
#print axioms nativeGK4W_structural_charge_sound

end
end Kuu.F112.Physical
