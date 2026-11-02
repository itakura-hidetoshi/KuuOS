import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5AJFourCellComparisonReflection
import Kuu.F112.PolygonNativeF55P89InterchangeFourCell
import Kuu.F112.PolygonNativeF55P93AssocFourCellCoherence
import Mathlib.Tactic

/-!
F112-P94D3GK5AK — exact proof-relevant original P89 horizontal
interchange preservation boundary against selected P93 four-cells.

GK5AI structurally mapped all nine ORIGINAL F55 Type-valued 3-cell
constructors into selected P92B comparison proofs; GK5AJ mapped
all eight ACTUAL P77 vertical four-cell constructors to P93.

The original P89 four-cell presentation has THIRTEEN constructors:
one imported P87 source four-cell, one new genuine horizontal
interchange, and eleven further genuine proof closure rules.
The P93 selected presentation has the matching INTERCHANGE and
closure constructors, but its .old generator only relates
.original(f) to .original(g), NOT automatically the distinct
structural images phi(f) and phi(g). It would be unsound to
promote this last compatibility without a typed witness.

GK5AK therefore proves:
(1) P89's actual interchange generator ALWAYS maps to a true
    P93 Type-valued four-cell between the STRUCTURAL phi images,
    using no P87 compatibility assumption.
(2) All P89 source four-cells admit such a structural typed
    four-cell lift iff the inherited P87 base four-cells do.
    Necessity is restriction; sufficiency is a complete recursion
    over ALL 13 source constructors.
(3) Conditional on exactly this explicit P87 typed boundary,
    the true P89 witness quotient maps into the true P93 witness
    quotient; injectivity holds IFF it REFLECTS all actual
    selected P93 four-cells between translated original 3-cells.
(4) The entire signed/odd-ZMod2 F55 shadow commutes with that
    quotient map, without upgrading shadow equalities to cells.

No unconditional P87-to-structural-phi four-cell bridge is
invented, and the separate P92B assocNaturality is not claimed
to originate in the old nine-constructor F55. No Gray,
global pseudo-functor/higher filler or hyperdescent.

Append-only/tighten-only, independent Kuu, public root107,
strict 空 authority boundary, no protected #1558 changes.
Pinned Lean v4.30.0-rc2 / mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
No sorry, native_decide or new axioms.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
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
variable {a b : D} {x y : E}
variable (p : Polygon)

/-- The EXACT missing source authority boundary: for every
actual P87 four-cell, a P93C Type-valued four-cell between
its two GK5AI STRUCTURAL original F55→P92B images must be
supplied. This is data, not an assumed global axiom or a theorem
silently derived from P93's separately chosen .old generator. -/
abbrev NativeGK5AKP87StructuralBoundary :=
  ∀ {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s},
      NativeF55P87ClosedFourCell f g →
      NativeF55P93AssocFourCell
        (nativeGK5AIOriginalToP92Structural f)
        (nativeGK5AIOriginalToP92Structural g)

/-- The desired COMPLETE structural four-cell map for every one
of the thirteen genuine original P89 higher-comparison rules. -/
abbrev NativeGK5AKP89StructuralBoundary :=
  ∀ {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s},
      NativeF55P89InterchangeFourCell f g →
      NativeF55P93AssocFourCell
        (nativeGK5AIOriginalToP92Structural f)
        (nativeGK5AIOriginalToP92Structural g)

/-- The genuine newly added P89 INTERCHANGE itself has an
UNCONDITIONAL P93 structural image. The two 4-cell endpoints
are the exact original F54 route horizontal composites,
not their zero-dimensional shadow or their existence quotient. -/
def nativeGK5AKInterchangeStructural
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    {u₀ u₁ u₂ : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter}
    {v₀ v₁ v₂ : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter}
    (f₁ : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u₀ u₁)
    (f₂ : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u₁ u₂)
    (g₁ : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p v₀ v₁)
    (g₂ : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p v₁ v₂) :
    NativeF55P93AssocFourCell
      (nativeGK5AIOriginalToP92Structural
        ((KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans f₁ f₂).horizontal
          (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans g₁ g₂)))
      (nativeGK5AIOriginalToP92Structural
        (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans
          (f₁.horizontal g₁) (f₂.horizontal g₂))) :=
  .interchange
    (nativeGK5AIOriginalToP92Structural f₁)
    (nativeGK5AIOriginalToP92Structural f₂)
    (nativeGK5AIOriginalToP92Structural g₁)
    (nativeGK5AIOriginalToP92Structural g₂)

/-- Given only the genuinely OLD P87 typed boundary, recursion
over ALL THIRTEEN source P89 higher-cell constructors produces a
selected P93 Type-valued 4-cell, preserving actual typed
F54 source/target and both independent Nat depth indices. -/
def nativeGK5AKP89Structural_of_P87
    (base : NativeGK5AKP87StructuralBoundary (a := a) (b := b) (x := x) (y := y) p) :
    NativeGK5AKP89StructuralBoundary (a := a) (b := b) (x := x) (y := y) p := by
  intro n n' m m' ma mb pa pb first last r s f g w
  induction w with
  | old witness => exact base witness
  | interchange f₁ f₂ g₁ g₂ =>
      exact nativeGK5AKInterchangeStructural p f₁ f₂ g₁ g₂
  | refl raw => exact .refl _
  | symm witness ih => exact .symm ih
  | trans fg gh ihfg ihgh => exact .trans ihfg ihgh
  | leftWhisker prior witness ih =>
      exact .leftWhisker (nativeGK5AIOriginalToP92Structural prior) ih
  | rightWhisker witness suffix ih =>
      exact .rightWhisker ih (nativeGK5AIOriginalToP92Structural suffix)
  | leftContext witness later ih => exact .leftContext ih later
  | rightContext earlier witness ih => exact .rightContext earlier ih
  | precompose prior witness ih => exact .precompose prior ih
  | postcompose witness suffix ih => exact .postcompose ih suffix
  | horizontalLeft witness other ih =>
      exact .horizontalLeft ih (nativeGK5AIOriginalToP92Structural other)
  | horizontalRight other witness ih =>
      exact .horizontalRight (nativeGK5AIOriginalToP92Structural other) ih

/-- Restrict a complete structural P89 comparison to its ACTUAL
P87 original-source generator; this establishes necessity. -/
def nativeGK5AKP87Structural_of_P89
    (whole : NativeGK5AKP89StructuralBoundary (a := a) (b := b) (x := x) (y := y) p) :
    NativeGK5AKP87StructuralBoundary (a := a) (b := b) (x := x) (y := y) p := by
  intro n n' m m' ma mb pa pb first last r s f g w
  exact whole (.old w)

/-- Precise Type-valued lifting EXISTENCE iff: all P89 horizontal,
context and vertical four-cell coherence is structurally
transportable exactly when the genuinely old P87 base generator
is. No unproved choice of original 4-cell evidence is added. -/
theorem nativeGK5AKP89Structural_nonempty_iff_P87 :
    Nonempty (NativeGK5AKP89StructuralBoundary
      (a := a) (b := b) (x := x) (y := y) p) ↔
    Nonempty (NativeGK5AKP87StructuralBoundary
      (a := a) (b := b) (x := x) (y := y) p) := by
  constructor
  · rintro ⟨whole⟩
    exact ⟨nativeGK5AKP87Structural_of_P89 p whole⟩
  · rintro ⟨base⟩
    exact ⟨nativeGK5AKP89Structural_of_P87 p base⟩

variable {p}

/-- The selected P93C witness quotient RECEIVES the genuine
original P89 horizontal-interchange quotient if the exact
prior P87 structural 4-cell boundary is provided. No numerical
shadow is promoted to a fabricated four-cell. -/
def nativeGK5AKFourClassMap
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last)
    (base : NativeGK5AKP87StructuralBoundary (a := a) (b := b) (x := x) (y := y) p) :
    NativeF55P89FourClasses first last r s →
      NativeF55P93AssocFourClasses first last r s :=
  _root_.Quotient.lift
    (fun f => nativeF55P93AssocFourClass first last
      (nativeGK5AIOriginalToP92Structural f))
    (by
      intro f g h
      rcases h with ⟨w⟩
      exact _root_.Quotient.sound
        ⟨nativeGK5AKP89Structural_of_P87 p base w⟩)

/-- The exact quotient-kernel computation is the original
structural three-cell map on source representatives. -/
theorem nativeGK5AKFourClassMap_spec
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (base : NativeGK5AKP87StructuralBoundary (a := a) (b := b) (x := x) (y := y) p)
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    nativeGK5AKFourClassMap first last r s base
        (nativeF55P89FourClass first last f) =
      nativeF55P93AssocFourClass first last
        (nativeGK5AIOriginalToP92Structural f) := rfl

/-- Conditional selected four-cell quotient FAITHFULNESS is
equivalent to reflection of each actually present P93 Type-valued
four-cell between mapped original P89 three-cells back to an
actual P89 source four-cell. This is an iff, not a claim of
unconditional global comparison reflection. -/
theorem nativeGK5AKFourClassInjective_iff_reflect
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last)
    (base : NativeGK5AKP87StructuralBoundary (a := a) (b := b) (x := x) (y := y) p) :
    Function.Injective (nativeGK5AKFourClassMap first last r s base) ↔
      (∀ f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s,
        Nonempty (NativeF55P93AssocFourCell
          (nativeGK5AIOriginalToP92Structural f)
          (nativeGK5AIOriginalToP92Structural g)) →
        Nonempty (NativeF55P89InterchangeFourCell f g)) := by
  constructor
  · intro hinj f g h
    have htarget :
        nativeF55P93AssocFourClass first last
            (nativeGK5AIOriginalToP92Structural f) =
          nativeF55P93AssocFourClass first last
            (nativeGK5AIOriginalToP92Structural g) :=
      (nativeF55P93AssocFourClass_eq_iff first last
        (nativeGK5AIOriginalToP92Structural f)
        (nativeGK5AIOriginalToP92Structural g)).2 h
    have hsource :
        nativeF55P89FourClass first last f =
          nativeF55P89FourClass first last g := by
      apply hinj
      exact htarget
    exact (nativeF55P89FourClass_eq_iff first last f g).1 hsource
  · intro href q₁ q₂
    refine _root_.Quotient.inductionOn₂ q₁ q₂ ?_
    intro f g heq
    apply (nativeF55P89FourClass_eq_iff first last f g).2
    apply href f g
    exact (nativeF55P93AssocFourClass_eq_iff first last
      (nativeGK5AIOriginalToP92Structural f)
      (nativeGK5AIOriginalToP92Structural g)).1 heq

/-- Independently established full signed pentagon/square/odd
C60 shadow descends along this CONDITIONAL genuine 4-cell
quotient map; this does not add the missing old P87 witness. -/
theorem nativeGK5AKFourClassShadow_commutes
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last)
    (base : NativeGK5AKP87StructuralBoundary (a := a) (b := b) (x := x) (y := y) p)
    (q : NativeF55P89FourClasses first last r s) :
    nativeF55P93AssocFourToShadow first last r s
      (nativeGK5AKFourClassMap first last r s base q) =
    nativeF55P89FourToShadow first last r s q := by
  refine _root_.Quotient.inductionOn q ?_
  intro f
  exact nativeGK5AJStructuralShadow first last f

#print axioms nativeGK5AKInterchangeStructural
#print axioms nativeGK5AKP89Structural_of_P87
#print axioms nativeGK5AKP87Structural_of_P89
#print axioms nativeGK5AKP89Structural_nonempty_iff_P87
#print axioms nativeGK5AKFourClassMap
#print axioms nativeGK5AKFourClassMap_spec
#print axioms nativeGK5AKFourClassInjective_iff_reflect
#print axioms nativeGK5AKFourClassShadow_commutes

end
end Kuu.F112.Physical
