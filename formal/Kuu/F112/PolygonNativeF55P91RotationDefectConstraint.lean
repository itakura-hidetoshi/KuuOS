import Kuu.F112.PolygonNativeF55P90TripleRouteNaturalityBoundary
import Mathlib.Tactic

/-!
# F112-P91A — rotation-count coboundary for genuine original F55 cells

Every one of the NINE truly typed native F55 3-cell constructors
conserves an exact integer relation:
  source F54 primitive rotation count - target F54 primitive count
    = signed PENTAGON integer component of original F55 shadow.

The real 3-vs-2 F54 pentagon generator has defect +1; the actual
disjoint F54 square has defect 0. Symmetry, vertical composition,
all four context / pre-post route transports preserve this identity.

P90B proves its two naturality source routes have the SAME actual
primitive rotation count but DIFFERENT raw histories. Therefore
any inhabitant of the genuinely typed ORIGINAL nine-constructor
NativeF55P90AssocNaturalityCell must have ZERO net pentagon charge.
Combining this result with the previously verified original square
charge parity forces the COMPLETE NECESSARY shadow shape:
    ((0, signed-square-charge), odd phase = square charge mod 2).
It is NOT a proof that the slot is inhabited, an assertion that
the original histories are equal, nor a construction of new source
cells or 4-cell coherence. In particular the actual C60 odd square
phase is not erased. Existing P87/P88 obstruction and P89 strict
interchange remain unchanged.

No Gray, new axioms, sorry/admit or removal of the 107 public roots.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- For EVERY original nine-constructor native F55 Type-valued
3-cell, the signed pentagon shadow is EXACTLY the integer rotation
count defect between its actual ORIGINAL F54 route endpoints. -/
theorem KuuNativeF45Tree.DepthRotationRoute.PresentedCell.p91_pentagonCharge_eq_countDefect
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    (r.rotationCount : Int) - (s.rotationCount : Int) =
      cell.nativeShadow.1.1 := by
  induction cell with
  | ident route =>
      change (route.rotationCount : Int) - (route.rotationCount : Int) = 0
      omega
  | pentagon a b c d =>
      change (3 : Int) - 2 = 1
      omega
  | disjointSquare left right =>
      change (2 : Int) - 2 = 0
      omega
  | symm c ih =>
      change _ = -c.nativeShadow.1.1
      omega
  | trans c d ihc ihd =>
      change _ = c.nativeShadow.1.1 + d.nativeShadow.1.1
      omega
  | leftContext c later ih => exact ih
  | rightContext earlier c ih => exact ih
  | precompose prior c ih =>
      change ((prior.rotationCount + _ : Nat) : Int) -
        ((prior.rotationCount + _ : Nat) : Int) = c.nativeShadow.1.1
      omega
  | postcompose c suffix ih =>
      change ((_ + suffix.rotationCount : Nat) : Int) -
        ((_ + suffix.rotationCount : Nat) : Int) = c.nativeShadow.1.1
      omega

/-- This is an exact necessary constraint on an actual ORIGINAL
nine-constructor certificate in the previously UNFILLED P90
associator-naturality slot. We do NOT assert that such a cell exists. -/
theorem nativeF55P91_assocNaturalityCell_pentagonCharge_zero

    {p : Polygon} {a b : D} {x y : E}
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
    (w : KuuNativeF45Tree.DepthRotationRoute p thirdBefore thirdAfter)
    (cell : NativeF55P90AssocNaturalityCell u v w) :
    cell.nativeShadow.1.1 = (0 : Int) := by
  have hcount := nativeF54P90AssocNaturality_rotationCount_eq u v w
  have hdef := cell.p91_pentagonCharge_eq_countDefect
  change ((nativeF54P90AssocNaturalityLeftRoute u v w).rotationCount : Int) -
    ((nativeF54P90AssocNaturalityRightRoute u v w).rotationCount : Int) =
      cell.nativeShadow.1.1 at hdef
  rw [hcount, sub_self] at hdef
  exact hdef.symm

/-- The complete original signed-charge/odd-phase shadow of ANY
P90 associator naturality witness has this NECESSARY shape. The
middle signed exchange-square integer remains genuinely free: this
does NOT fabricate or require zero odd phase. -/
theorem nativeF55P91_assocNaturalityCell_shadow_shape

    {p : Polygon} {a b : D} {x y : E}
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
    (w : KuuNativeF45Tree.DepthRotationRoute p thirdBefore thirdAfter)
    (cell : NativeF55P90AssocNaturalityCell u v w) :
    cell.nativeShadow =
      (((0 : Int), cell.nativeShadow.1.2),
        ((cell.nativeShadow.1.2 : Int) : ZMod 2)) := by
  apply Prod.ext
  · apply Prod.ext
    · exact nativeF55P91_assocNaturalityCell_pentagonCharge_zero u v w cell
    · rfl
  · exact cell.phase_squareParity.symm

/-- A SINGLE original positively oriented pentagon (or any
certificate with nonzero net pentagon shadow) cannot be the desired
P90 naturality filler. This is an obstruction by genuine original
rotation counts, not by numerical shadow coincidence. -/
theorem nativeF55P91_assocNaturalityCell_no_primitive_pentagon_grade

    {p : Polygon} {a b : D} {x y : E}
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
    (w : KuuNativeF45Tree.DepthRotationRoute p thirdBefore thirdAfter)
    (cell : NativeF55P90AssocNaturalityCell u v w) :
    cell.nativeShadow.1.1 ≠ (1 : Int) := by
  rw [nativeF55P91_assocNaturalityCell_pentagonCharge_zero u v w cell]
  omega

#print axioms KuuNativeF45Tree.DepthRotationRoute.PresentedCell.p91_pentagonCharge_eq_countDefect
#print axioms nativeF55P91_assocNaturalityCell_pentagonCharge_zero
#print axioms nativeF55P91_assocNaturalityCell_shadow_shape
#print axioms nativeF55P91_assocNaturalityCell_no_primitive_pentagon_grade

end
end Kuu.F112.Physical
