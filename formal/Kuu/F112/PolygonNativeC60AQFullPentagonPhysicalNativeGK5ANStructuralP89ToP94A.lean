import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5AMContextParityNoStructuralLift
import Kuu.F112.PolygonNativeF55P94UnitFourCellPresentation
import Mathlib.Tactic

/-!
F112-P94D3GK5AN — unconditional full original P89 structural
four-cell transport into the pre-existing, HONEST P94A extension.

Source chronology is preserved: original Type-valued F55 three-cells
with nine constructors, P77 eight source four-cells, P80 three
adjoined primitive unit four-cells, P85 horizontal closure, P86
context/route closure, P87 recursive closure and P89 full thirteen
four-cell rules. GK5AI's exact structural phi preserves ALL source
F55 constructors; GK5AM proved P93C alone cannot lift left/right
P80 context-unit generators because of the ZMod2 context-parity
invariant. Qi v4.6 exhibited that no-lift on real north C60 stages.

Crucially P94A already exists in the canonical repository!
NativeF55P94UnitFourCell is an independently declared higher
presentation which embeds P93C, explicitly adjoins precisely the
three P80 primitive units, and closes under all P93 operations.
Do not invent a duplicate new 4-cell source or alter the original
P93C declarations. This GK5AN module proves the previously missing
STRUCTURAL map from the entire P89 original source through the
GK5AI constructor-recursive phi, with actual typed four-cells as
results, not merely numeric shadows or quotient equalities.

Construct the three P80 primitive lifts, all P80/P85/P86/P87
closure recursors, all thirteen P89 generators, a genuine
unconditional P89 four-witness quotient → P94A quotient map and
its precise injectivity iff selected P94A comparisons REFLECT
to real original P89 four-cells. Retain all signed pentagon/square
and odd C60 phase information. Distinguish the old P93 no-go from
the new P94A positive repair; show the canonical P93→P94A
four-class map is non-injective on genuine typed contexts.

No unconditional faithfulness, no P92B assocNaturality
backport into original F55, no conflation .original(f)=phi(f),
no physical Edge=whole-NatIso, unrestricted descent, gluing,
higher filler or Gray restoration. Independent Kuu only; Qi
may import Kuu, never converse. strict 空 authority, append-only,
same public root107, protected PR #1558 Draft/open/unmerged.
Pinned Lean v4.30.0-rc2/mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
No sorry, native_decide or added axioms.
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

/-- P94A-target lift data for P87 and P89, keeping every original
F54 doubly Nat-indexed source history and every F55 proof term.
Unlike the historical P93C boundary, these interfaces DO have
unconditionally constructed inhabitants below. -/
abbrev NativeGK5ANP94P87Boundary :=
  ∀ {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s},
      NativeF55P87ClosedFourCell f g →
      NativeF55P94UnitFourCell
        (nativeGK5AIOriginalToP92Structural f)
        (nativeGK5AIOriginalToP92Structural g)

/-- The desired COMPLETE structural four-cell map for every one
of the thirteen genuine original P89 higher-comparison rules. -/
abbrev NativeGK5ANP94P89Boundary :=
  ∀ {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s},
      NativeF55P89InterchangeFourCell f g →
      NativeF55P94UnitFourCell
        (nativeGK5AIOriginalToP92Structural f)
        (nativeGK5AIOriginalToP92Structural g)



/-- P94A-targeted three-generator boundary: proof-relevant,
independently typed, rather than a shadow-level inference. -/
abbrev NativeGK5ANP94PrimitiveBoundary (p : Polygon) :=
  ∀ {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s},
      NativeGK5ALPrimitiveUnitFourCell f g →
      NativeF55P94UnitFourCell
        (nativeGK5AIOriginalToP92Structural f)
        (nativeGK5AIOriginalToP92Structural g)

abbrev NativeGK5ANP94P80Boundary (p : Polygon) :=
  ∀ {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s},
      NativeF55P80UnitFourCell f g →
      NativeF55P94UnitFourCell
        (nativeGK5AIOriginalToP92Structural f)
        (nativeGK5AIOriginalToP92Structural g)

abbrev NativeGK5ANP94P85Boundary (p : Polygon) :=
  ∀ {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s},
      NativeF55P85HorizontalFourCell f g →
      NativeF55P94UnitFourCell
        (nativeGK5AIOriginalToP92Structural f)
        (nativeGK5AIOriginalToP92Structural g)

abbrev NativeGK5ANP94P86Boundary (p : Polygon) :=
  ∀ {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s},
      NativeF55P86ContextFourCell f g →
      NativeF55P94UnitFourCell
        (nativeGK5AIOriginalToP92Structural f)
        (nativeGK5AIOriginalToP92Structural g)


def nativeGK5ANP80P94_of_primitive (p : Polygon)
    (base : NativeGK5ANP94PrimitiveBoundary (a := a) (b := b) (x := x) (y := y) p) :
    NativeGK5ANP94P80Boundary (a := a) (b := b) (x := x) (y := y) p := by
  intro n n' m m' ma mb pa pb first last r s f g w
  induction w with
  | old witness => exact .old (nativeGK5AJOriginalFourToP93 _ _ witness)
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
def nativeGK5ANP85P94_of_P80 (p : Polygon)
    (base : NativeGK5ANP94P80Boundary (a := a) (b := b) (x := x) (y := y) p) :
    NativeGK5ANP94P85Boundary (a := a) (b := b) (x := x) (y := y) p := by
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
def nativeGK5ANP86P94_of_P85 (p : Polygon)
    (base : NativeGK5ANP94P85Boundary (a := a) (b := b) (x := x) (y := y) p) :
    NativeGK5ANP94P86Boundary (a := a) (b := b) (x := x) (y := y) p := by
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
def nativeGK5ANP87P94_of_P86 (p : Polygon)
    (base : NativeGK5ANP94P86Boundary (a := a) (b := b) (x := x) (y := y) p) :
    NativeGK5ANP94P87Boundary (a := a) (b := b) (x := x) (y := y) p := by
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


/-- Every one of the three TRUE ORIGINAL P80 primitive unit
four-cells receives a genuine, separately declared P94A four-cell.
These are explicit P94A presentation generators, NOT theorems
inside P93C. -/
def nativeGK5ANPrimitiveToP94 (p : Polygon) :
    NativeGK5ANP94PrimitiveBoundary (a := a) (b := b) (x := x) (y := y) p := by
  intro n n' m m' ma mb pa pb first last r s f g w
  cases w with
  | horizontalUnit u v => exact .horizontalUnit u v
  | leftContextUnit u later => exact .leftContextUnit u later
  | rightContextUnit earlier u => exact .rightContextUnit earlier u

/-- Unconditional full P87 structural typed source lift: all P80
units and all P85/P86/P87 recursive closures are preserved in
the *existing* independent P94A four-cell presentation. -/
def nativeGK5ANP87ToP94 (p : Polygon) :
    NativeGK5ANP94P87Boundary (a := a) (b := b) (x := x) (y := y) p :=
  nativeGK5ANP87P94_of_P86 p
    (nativeGK5ANP86P94_of_P85 p
      (nativeGK5ANP85P94_of_P80 p
        (nativeGK5ANP80P94_of_primitive p (nativeGK5ANPrimitiveToP94 p))))

/-- All THIRTEEN source P89 four-cell constructors transport into
P94A, including TRUE P89 horizontal interchange, without a
missing P87 premise or conversion to numeric C60 shadows. -/
def nativeGK5ANP89ToP94 (p : Polygon) :
    NativeGK5ANP94P89Boundary (a := a) (b := b) (x := x) (y := y) p := by
  intro n n' m m' ma mb pa pb first last r s f g w
  induction w with
  | old witness => exact nativeGK5ANP87ToP94 p witness
  | interchange f₁ f₂ g₁ g₂ =>
      exact .old (nativeGK5AKInterchangeStructural p f₁ f₂ g₁ g₂)
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

theorem nativeGK5ANP87P89ToP94_unconditional :
    Nonempty (NativeGK5ANP94P87Boundary
      (a := a) (b := b) (x := x) (y := y) p) ∧
    Nonempty (NativeGK5ANP94P89Boundary
      (a := a) (b := b) (x := x) (y := y) p) :=
  ⟨⟨nativeGK5ANP87ToP94 p⟩, ⟨nativeGK5ANP89ToP94 p⟩⟩

variable {p}

/-- Genuine quotient factor map on ACTUAL source-P89 four-cell
witness classes. Well-definedness is obtained from the complete
typed 13-constructor P89 lift, not from scalar shadow equality. -/
def nativeGK5ANP89ToP94FourClassMap
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last) :
    NativeF55P89FourClasses first last r s →
      NativeF55P94UnitFourClasses first last r s :=
  _root_.Quotient.lift
    (fun f => nativeF55P94UnitFourClass first last
      (nativeGK5AIOriginalToP92Structural f))
    (by
      intro f g h
      rcases h with ⟨w⟩
      exact _root_.Quotient.sound ⟨nativeGK5ANP89ToP94 p w⟩)

/-- Exact representative formula for the new UNCONDITIONAL
original-source P89→selected-extension P94A quotient map. -/
theorem nativeGK5ANP89ToP94FourClassMap_spec
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    nativeGK5ANP89ToP94FourClassMap first last r s
      (nativeF55P89FourClass first last f) =
    nativeF55P94UnitFourClass first last
      (nativeGK5AIOriginalToP92Structural f) := rfl

/-- No unproved source faithfulness: the new P89→P94A quotient
map is injective PRECISELY when every actual selected P94A
four-cell between phi-images reflects back to an actual
original P89 Type-valued four-cell. -/
theorem nativeGK5ANP89ToP94_injective_iff_reflect
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last) :
    Function.Injective (nativeGK5ANP89ToP94FourClassMap first last r s) ↔
      (∀ f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s,
        Nonempty (NativeF55P94UnitFourCell
          (nativeGK5AIOriginalToP92Structural f)
          (nativeGK5AIOriginalToP92Structural g)) →
        Nonempty (NativeF55P89InterchangeFourCell f g)) := by
  constructor
  · intro hinj f g h
    have htarget :
        nativeF55P94UnitFourClass first last
            (nativeGK5AIOriginalToP92Structural f) =
          nativeF55P94UnitFourClass first last
            (nativeGK5AIOriginalToP92Structural g) :=
      (nativeF55P94UnitFourClass_eq_iff first last
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
    exact (nativeF55P94UnitFourClass_eq_iff first last
      (nativeGK5AIOriginalToP92Structural f)
      (nativeGK5AIOriginalToP92Structural g)).1 heq

/-- Full signed pentagon/square/odd-ZMod2 C60 observer factors
through the true unconditional P89→P94A witness quotient map. -/
theorem nativeGK5ANP89ToP94Shadow_commutes
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last)
    (q : NativeF55P89FourClasses first last r s) :
    nativeF55P94UnitFourToShadow first last r s
      (nativeGK5ANP89ToP94FourClassMap first last r s q) =
    nativeF55P89FourToShadow first last r s q := by
  refine _root_.Quotient.inductionOn q ?_
  intro f
  exact nativeGK5AJStructuralShadow first last f

/-- The EXACT previously proven P93 parity obstruction is
REPAIRED by an actual P94A left-context-unit four-cell on
every genuine original typed F54 context; it is not a change
to the P93C presentation itself. -/
theorem nativeGK5ANP93NoButP94Yes_leftContext
    {n n' m m' k l : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (u : KuuNativeF45Tree.DepthRotationRoute p first last)
    (later : KuuNativeF45Tree p k l mb pb mc pc) :
    (¬ Nonempty (NativeF55P93AssocFourCell
      (nativeGK5AIOriginalToP92Structural
        (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.leftContext
          (.ident u) later))
      (nativeGK5AIOriginalToP92Structural
        (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident
          (.leftContext u later))))) ∧
    Nonempty (NativeF55P94UnitFourCell
      (nativeGK5AIOriginalToP92Structural
        (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.leftContext
          (.ident u) later))
      (nativeGK5AIOriginalToP92Structural
        (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident
          (.leftContext u later)))) := by
  exact ⟨nativeGK5AMLeftContextUnit_no_P93 u later,
    ⟨NativeF55P94UnitFourCell.leftContextUnit u later⟩⟩

/-- The independent right-context source unit has the same
genuine non-lift at P93 and genuine proof-relevant lift at P94A. -/
theorem nativeGK5ANP93NoButP94Yes_rightContext
    {k l n n' m m' : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    (earlier : KuuNativeF45Tree p k l ma pa mb pb)
    {first : KuuNativeF45Tree p n m mb pb mc pc}
    {last : KuuNativeF45Tree p n' m' mb pb mc pc}
    (u : KuuNativeF45Tree.DepthRotationRoute p first last) :
    (¬ Nonempty (NativeF55P93AssocFourCell
      (nativeGK5AIOriginalToP92Structural
        (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.rightContext
          earlier (.ident u)))
      (nativeGK5AIOriginalToP92Structural
        (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident
          (.rightContext earlier u))))) ∧
    Nonempty (NativeF55P94UnitFourCell
      (nativeGK5AIOriginalToP92Structural
        (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.rightContext
          earlier (.ident u)))
      (nativeGK5AIOriginalToP92Structural
        (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident
          (.rightContext earlier u)))) :=
  ⟨nativeGK5AMRightContextUnit_no_P93 earlier u,
    ⟨NativeF55P94UnitFourCell.rightContextUnit earlier u⟩⟩

/-- The canonical existing P93→P94A four-class quotient map
STRICTLY collapses old selected-P93 context-proof classes: this
is why the new presentation removes the old parity obstruction.
P94A extends P93, but the induced *quotient* is not faithful
on genuine typed F54 left-context sources. -/
theorem nativeGK5ANP93ToP94Class_not_injective
    {n n' m m' k l : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (u : KuuNativeF45Tree.DepthRotationRoute p first last)
    (later : KuuNativeF45Tree p k l mb pb mc pc) :
    ¬ Function.Injective
      (nativeF55P93ToP94UnitFour
        (KuuNativeF45Tree.node first later)
        (KuuNativeF45Tree.node last later)
        (r := .leftContext u later) (s := .leftContext u later)) := by
  intro hinj
  have hOld :
      nativeF55P93AssocFourClass _ _
          (NativeF55P92AssocComparison.leftContext (.refl u) later) =
        nativeF55P93AssocFourClass _ _
          (NativeF55P92AssocComparison.refl (.leftContext u later)) := by
    apply hinj
    exact _root_.Quotient.sound
      ⟨NativeF55P94UnitFourCell.leftContextUnit u later⟩
  have hWitness :=
    (nativeF55P93AssocFourClass_eq_iff _ _
      (NativeF55P92AssocComparison.leftContext (.refl u) later)
      (NativeF55P92AssocComparison.refl (.leftContext u later))).mp hOld
  exact nativeGK5AMLeftContextUnit_no_P93 u later hWitness

#print axioms nativeGK5ANPrimitiveToP94
#print axioms nativeGK5ANP80P94_of_primitive
#print axioms nativeGK5ANP85P94_of_P80
#print axioms nativeGK5ANP86P94_of_P85
#print axioms nativeGK5ANP87P94_of_P86
#print axioms nativeGK5ANP87ToP94
#print axioms nativeGK5ANP89ToP94
#print axioms nativeGK5ANP87P89ToP94_unconditional
#print axioms nativeGK5ANP89ToP94FourClassMap
#print axioms nativeGK5ANP89ToP94FourClassMap_spec
#print axioms nativeGK5ANP89ToP94_injective_iff_reflect
#print axioms nativeGK5ANP89ToP94Shadow_commutes
#print axioms nativeGK5ANP93NoButP94Yes_leftContext
#print axioms nativeGK5ANP93NoButP94Yes_rightContext
#print axioms nativeGK5ANP93ToP94Class_not_injective

end
end Kuu.F112.Physical
