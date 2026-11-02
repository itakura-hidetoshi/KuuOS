import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5AKInterchangeFourCellBoundary
import Kuu.F112.PolygonNativeF55P86ContextFourCell
import Kuu.F112.PolygonNativeF55P84HorizontalFourCellP85
import Kuu.F112.PolygonNativeF55P62RelativeUnitFourCellP80
import Mathlib.Tactic

/-!
F112-P94D3GK5AL — the EXACT old P87 structural obstruction reduces to
the THREE genuinely adjoined source P80 primitive unit 4-cells.

GK5AK proved that all thirteen original P89 4-cell constructors
admit a selected P93 structural lift exactly if all old P87 4-cells
do. We now analyze the actual historical base chain
P87 -> P86 -> P85 -> P80 -> original P77 (not a shadow proxy).

The old P77 four-cells have an unconditional structural P93 image
by GK5AJ. Every recursive P80/P85/P86/P87 closure rule has a
corresponding genuine P93 four-cell constructor. Consequently the
ONLY additional structural compatibility DATA are the three
original P80 primitive source-generator families:
  horizontalUnit, leftContextUnit, rightContextUnit.
These were genuinely adjoined to the old F55 proof syntax at P80;
they cannot be erased by identifying .original(f) with the
distinct GK5AI structural image phi(f).

Prove, constructively and with complete source proof histories,
  Nonempty(P89 structural lift)
     <-> Nonempty(P87 structural lift)
     <-> Nonempty(three primitive P80 structural lifts).
Also give the exact local obstruction implication: a single
primitive P80 source generator WITHOUT a target P93 four-cell
rules out a global P87/P89 structural lift. This is conditional:
we do NOT assert the existence of such a counterexample.

The two Nat depth indices, original F54/F55 proof types, original
three-coordinate C60 shadow and strict 空 authority are retained.
No fabricated unit 4-cell, P92B associator naturality backport,
unconditional descent, Gray, sorry, native_decide or new axioms.
Append-only/tighten-only; root107; protect draft PR #1558.
Pinned Lean v4.30.0-rc2, mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
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

/-- Precisely the THREE primitive P80 generator families that are
not original P77 4-cells. This is an indexed Type-valued subpresentation
of P80, not a Prop quotient or numerical shadow. -/
inductive NativeGK5ALPrimitiveUnitFourCell
    {p : Polygon} {a b : D} {x y : E} :
    ∀ {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {u v : KuuNativeF45Tree.DepthRotationRoute p first last},
      KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v →
      KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v →
      Type (max (max uD uE) (max vD vE)) where
  | horizontalUnit
      {n n' m m' k k' l l' : Nat}
      {p₀ p₁ p₂ : KuuNativeBlocks a b}
      {q₀ q₁ q₂ : KuuNativeBlocks x y}
      {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
      {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
      {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
      {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
      (u : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter)
      (v : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter) :
      NativeGK5ALPrimitiveUnitFourCell
        ((KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident u).horizontal
          (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident v))
        (.ident (nativeF55HorizontalUnitRoute u v))
  | leftContextUnit
      {n n' m m' k l : Nat}
      {ma mb mc : KuuNativeBlocks a b}
      {pa pb pc : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      (u : KuuNativeF45Tree.DepthRotationRoute p first last)
      (later : KuuNativeF45Tree p k l mb pb mc pc) :
      NativeGK5ALPrimitiveUnitFourCell
        (.leftContext (.ident u) later)
        (.ident (.leftContext u later))
  | rightContextUnit
      {k l n n' m m' : Nat}
      {ma mb mc : KuuNativeBlocks a b}
      {pa pb pc : KuuNativeBlocks x y}
      (earlier : KuuNativeF45Tree p k l ma pa mb pb)
      {first : KuuNativeF45Tree p n m mb pb mc pc}
      {last : KuuNativeF45Tree p n' m' mb pb mc pc}
      (u : KuuNativeF45Tree.DepthRotationRoute p first last) :
      NativeGK5ALPrimitiveUnitFourCell
        (.rightContext earlier (.ident u))
        (.ident (.rightContext earlier u))

/-- Each named primitive has the corresponding ACTUAL original
P80 source 4-cell, embedded successively in P85, P86 and P87.
There is no use of a scalar shadow to fabricate this source cell. -/
def NativeGK5ALPrimitiveUnitFourCell.toP87
    {p : Polygon} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
    (w : NativeGK5ALPrimitiveUnitFourCell f g) :
    NativeF55P87ClosedFourCell f g := by
  cases w with
  | horizontalUnit u v => exact .old (.old (.old (.horizontalUnit u v)))
  | leftContextUnit u later => exact .old (.old (.old (.leftContextUnit u later)))
  | rightContextUnit earlier u => exact .old (.old (.old (.rightContextUnit earlier u)))

/-- Exactly the selected P93 structural four-cell obligation on
each of the three primitive P80 generator families (no other data). -/
abbrev NativeGK5ALPrimitiveBoundary (p : Polygon) :=
  ∀ {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s},
      NativeGK5ALPrimitiveUnitFourCell f g →
      NativeF55P93AssocFourCell
        (nativeGK5AIOriginalToP92Structural f)
        (nativeGK5AIOriginalToP92Structural g)

abbrev NativeGK5ALP80Boundary (p : Polygon) :=
  ∀ {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s},
      NativeF55P80UnitFourCell f g →
      NativeF55P93AssocFourCell
        (nativeGK5AIOriginalToP92Structural f)
        (nativeGK5AIOriginalToP92Structural g)

abbrev NativeGK5ALP85Boundary (p : Polygon) :=
  ∀ {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s},
      NativeF55P85HorizontalFourCell f g →
      NativeF55P93AssocFourCell
        (nativeGK5AIOriginalToP92Structural f)
        (nativeGK5AIOriginalToP92Structural g)

abbrev NativeGK5ALP86Boundary (p : Polygon) :=
  ∀ {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s},
      NativeF55P86ContextFourCell f g →
      NativeF55P93AssocFourCell
        (nativeGK5AIOriginalToP92Structural f)
        (nativeGK5AIOriginalToP92Structural g)

/-- All NINE P80 4-cell constructors are lifted given ONLY its
three genuine new primitive units. The old P77 case is already
unconditionally provided by the proven GK5AJ structural map. -/
def nativeGK5ALP80_of_primitive (p : Polygon)
    (base : NativeGK5ALPrimitiveBoundary (a := a) (b := b) (x := x) (y := y) p) :
    NativeGK5ALP80Boundary (a := a) (b := b) (x := x) (y := y) p := by
  intro n n' m m' ma mb pa pb first last r s f g w
  induction w with
  | old witness => exact nativeGK5AJOriginalFourToP93 _ _ witness
  | refl raw => exact .refl _
  | symm witness ih => exact .symm ih
  | trans fg gh ihfg ihgh => exact .trans ihfg ihgh
  | leftWhisker prior witness ih =>
      exact .leftWhisker (nativeGK5AIOriginalToP92Structural prior) ih
  | rightWhisker witness suffix ih =>
      exact .rightWhisker ih (nativeGK5AIOriginalToP92Structural suffix)
  | horizontalUnit u v => exact base (.horizontalUnit u v)
  | leftContextUnit u later => exact base (.leftContextUnit u later)
  | rightContextUnit earlier u => exact base (.rightContextUnit earlier u)

/-- Complete P85 eight-constructor horizontal closure. Its two
horizontal generators come from P80 rather than recursively from
P85, so they are mapped using the exact P80 lift. -/
def nativeGK5ALP85_of_P80 (p : Polygon)
    (base : NativeGK5ALP80Boundary (a := a) (b := b) (x := x) (y := y) p) :
    NativeGK5ALP85Boundary (a := a) (b := b) (x := x) (y := y) p := by
  intro n n' m m' ma mb pa pb first last r s f g w
  induction w with
  | old witness => exact base witness
  | refl raw => exact .refl _
  | symm witness ih => exact .symm ih
  | trans fg gh ihfg ihgh => exact .trans ihfg ihgh
  | leftWhisker prior witness ih =>
      exact .leftWhisker (nativeGK5AIOriginalToP92Structural prior) ih
  | rightWhisker witness suffix ih =>
      exact .rightWhisker ih (nativeGK5AIOriginalToP92Structural suffix)
  | horizontalLeft witness other =>
      exact .horizontalLeft (base witness)
        (nativeGK5AIOriginalToP92Structural other)
  | horizontalRight other witness =>
      exact .horizontalRight (nativeGK5AIOriginalToP92Structural other)
        (base witness)

/-- Complete P86 twelve-constructor context/route closure,
respecting that its six new non-recursive actions take P85
witnesses, whereas vertical operations recurse through P86. -/
def nativeGK5ALP86_of_P85 (p : Polygon)
    (base : NativeGK5ALP85Boundary (a := a) (b := b) (x := x) (y := y) p) :
    NativeGK5ALP86Boundary (a := a) (b := b) (x := x) (y := y) p := by
  intro n n' m m' ma mb pa pb first last r s f g w
  induction w with
  | old witness => exact base witness
  | refl raw => exact .refl _
  | symm witness ih => exact .symm ih
  | trans fg gh ihfg ihgh => exact .trans ihfg ihgh
  | leftWhisker prior witness ih =>
      exact .leftWhisker (nativeGK5AIOriginalToP92Structural prior) ih
  | rightWhisker witness suffix ih =>
      exact .rightWhisker ih (nativeGK5AIOriginalToP92Structural suffix)
  | leftContext witness later => exact .leftContext (base witness) later
  | rightContext earlier witness => exact .rightContext earlier (base witness)
  | precompose prior witness => exact .precompose prior (base witness)
  | postcompose witness suffix => exact .postcompose (base witness) suffix
  | horizontalLeft witness other =>
      exact .horizontalLeft (base witness)
        (nativeGK5AIOriginalToP92Structural other)
  | horizontalRight other witness =>
      exact .horizontalRight (nativeGK5AIOriginalToP92Structural other)
        (base witness)

/-- Full P87 TWELVE-constructor self-recursive closure. Unlike
P86, its six actions recurse on actual P87 certificates. -/
def nativeGK5ALP87_of_P86 (p : Polygon)
    (base : NativeGK5ALP86Boundary (a := a) (b := b) (x := x) (y := y) p) :
    NativeGK5AKP87StructuralBoundary (a := a) (b := b) (x := x) (y := y) p := by
  intro n n' m m' ma mb pa pb first last r s f g w
  induction w with
  | old witness => exact base witness
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

/-- Construct the full old P87 lift from *only* the three P80
primitive unit families, through every intermediate typed layer. -/
def nativeGK5ALP87_of_primitive (p : Polygon)
    (base : NativeGK5ALPrimitiveBoundary (a := a) (b := b) (x := x) (y := y) p) :
    NativeGK5AKP87StructuralBoundary (a := a) (b := b) (x := x) (y := y) p :=
  nativeGK5ALP87_of_P86 p
    (nativeGK5ALP86_of_P85 p
      (nativeGK5ALP85_of_P80 p (nativeGK5ALP80_of_primitive p base)))

/-- Necessity: every primitive P80 unit witness embeds through
genuine P85/P86/P87 typed old constructors, so a P87 structural
lift restricts to exactly the three required P93 generator maps. -/
def nativeGK5ALPrimitive_of_P87 (p : Polygon)
    (whole : NativeGK5AKP87StructuralBoundary (a := a) (b := b) (x := x) (y := y) p) :
    NativeGK5ALPrimitiveBoundary (a := a) (b := b) (x := x) (y := y) p := by
  intro n n' m m' ma mb pa pb first last r s f g w
  exact whole w.toP87

/-- GK5AL CENTRAL THEOREM: the full original P87 structural
compatibility exists iff all THREE primitive P80 unit generators
admit their true selected P93 structural Type-valued images. -/
theorem nativeGK5ALP87Structural_nonempty_iff_primitive (p : Polygon) :
    Nonempty (NativeGK5AKP87StructuralBoundary
      (a := a) (b := b) (x := x) (y := y) p) ↔
    Nonempty (NativeGK5ALPrimitiveBoundary
      (a := a) (b := b) (x := x) (y := y) p) := by
  constructor
  · rintro ⟨whole⟩
    exact ⟨nativeGK5ALPrimitive_of_P87 p whole⟩
  · rintro ⟨base⟩
    exact ⟨nativeGK5ALP87_of_primitive p base⟩

/-- Combine GK5AK with this exact three-generator decomposition:
ALL THIRTEEN original P89 constructors lift iff the three
primitive P80 source units lift. No hidden P87 assumption. -/
theorem nativeGK5ALP89Structural_nonempty_iff_primitive (p : Polygon) :
    Nonempty (NativeGK5AKP89StructuralBoundary
      (a := a) (b := b) (x := x) (y := y) p) ↔
    Nonempty (NativeGK5ALPrimitiveBoundary
      (a := a) (b := b) (x := x) (y := y) p) :=
  (nativeGK5AKP89Structural_nonempty_iff_P87
    (a := a) (b := b) (x := x) (y := y) p).trans
    (nativeGK5ALP87Structural_nonempty_iff_primitive p)

/-- Construct the actual P89 full structural lifting function from
just the primitive P80 unit certificates; the interchange 4-cell
itself remains unconditional as in GK5AK. -/
def nativeGK5ALP89_of_primitive (p : Polygon)
    (base : NativeGK5ALPrimitiveBoundary (a := a) (b := b) (x := x) (y := y) p) :
    NativeGK5AKP89StructuralBoundary (a := a) (b := b) (x := x) (y := y) p :=
  nativeGK5AKP89Structural_of_P87 p (nativeGK5ALP87_of_primitive p base)

/-- An independently established missing selected P93 four-cell
for just ONE genuine primitive P80 generator obstructs the
complete old P87 structural lift. This does not assert that any
such missing certificate actually exists. -/
theorem nativeGK5ALP87_obstruction_of_primitive_missing
    {p : Polygon} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
    (w : NativeGK5ALPrimitiveUnitFourCell f g)
    (missing : ¬ Nonempty (NativeF55P93AssocFourCell
      (nativeGK5AIOriginalToP92Structural f)
      (nativeGK5AIOriginalToP92Structural g))) :
    ¬ Nonempty (NativeGK5AKP87StructuralBoundary
      (a := a) (b := b) (x := x) (y := y) p) := by
  rintro ⟨whole⟩
  exact missing ⟨whole w.toP87⟩

/-- The same typed, LOCAL primitive obstruction excludes a
global P89 structural transport by the exact GK5AK reduction. -/
theorem nativeGK5ALP89_obstruction_of_primitive_missing
    {p : Polygon} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
    (w : NativeGK5ALPrimitiveUnitFourCell f g)
    (missing : ¬ Nonempty (NativeF55P93AssocFourCell
      (nativeGK5AIOriginalToP92Structural f)
      (nativeGK5AIOriginalToP92Structural g))) :
    ¬ Nonempty (NativeGK5AKP89StructuralBoundary
      (a := a) (b := b) (x := x) (y := y) p) := by
  intro whole
  apply nativeGK5ALP87_obstruction_of_primitive_missing w missing
  exact (nativeGK5AKP89Structural_nonempty_iff_P87 p).mp whole

#print axioms NativeGK5ALPrimitiveUnitFourCell.toP87
#print axioms nativeGK5ALP80_of_primitive
#print axioms nativeGK5ALP85_of_P80
#print axioms nativeGK5ALP86_of_P85
#print axioms nativeGK5ALP87_of_P86
#print axioms nativeGK5ALP87Structural_nonempty_iff_primitive
#print axioms nativeGK5ALP89Structural_nonempty_iff_primitive
#print axioms nativeGK5ALP89_of_primitive
#print axioms nativeGK5ALP87_obstruction_of_primitive_missing
#print axioms nativeGK5ALP89_obstruction_of_primitive_missing

end
end Kuu.F112.Physical
