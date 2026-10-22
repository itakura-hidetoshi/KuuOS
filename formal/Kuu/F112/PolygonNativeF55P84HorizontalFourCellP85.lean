import Kuu.F112.PolygonNativeF55P80HorizontalPathCongruenceP84
import Kuu.F112.PolygonNativeF55P80UnitFourVerticalCategoryP81

/-!
# F112-P85 — original source Type-valued horizontal transport four-cells

P82 proves that old P80 source 4-cells are NOT stable under the
ORIGINAL raw F55 horizontal composition. P83 proves that a missing
context comparison is not even sound for the OLD P62 unit-only
free-path relation. P84 instead constructs a distinct, genuinely
source-witness-generated path congruence and its exact Mathlib
quotient, preserving full original shadow.

Here a new, separately labelled Type-valued 4-cell presentation
retains each OLD P80 4-cell certificate, adds genuine left and right
horizontal whiskering of old P80 certificates by arbitrary ORIGINAL
raw F55 proof cells, and closes under vertical unit/associator
comparison, inverses, transitivity and two-sided VERTICAL
whiskering of actual raw proof histories.

The two new horizontal generators are certificates themselves:
they carry their ORIGINAL P80 Type-valued witnesses. Every generated
P85 4-cell is sound for the independently defined NEW P84
typed path congruence (NOT necessarily for the OLD P62 relation),
and separately preserves the selected full (Int × Int) × ZMod 2
shadow. An exact source-witness quotient carries a strict LOCAL
vertical Mathlib Category on the original F54 route objects.

The original horizontal F55 operation now descends BIVARIATELY
from two ORIGINAL P80 four-cell quotient Homs to the NEW P85 Hom,
with actual proof witnesses in both representative changes.
This is a well-defined typed binary map, not a claim of a
bifunctor on all P85 Homs, strict interchange, global strict 3/n
or hyperdescent. The C60 north pentagon P82 counterexample stays
unequal in OLD P80 and becomes equal in NEW P85.

The new P85 source is one selected presentation, not an absolute
empty structure. No Gray, new axioms, sorry/admit, or exclusion of
the 107 historical public proof roots; old P62/P80 remain untouched.
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

/-- New genuinely Type-valued source 4-cell language, retaining
the ORIGINAL nine-constructor F55 raw proof terms as endpoints.
Horizontal whisker constructors retain P80 witnesses, and
their path soundness is relative to P84 rather than old P62. -/
inductive NativeF55P85HorizontalFourCell
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
  | old

      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v}
      (witness : NativeF55P80UnitFourCell f g) :
      NativeF55P85HorizontalFourCell f g
  | refl

      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
      (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v) :
      NativeF55P85HorizontalFourCell f f
  | symm

      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v}
      (witness : NativeF55P85HorizontalFourCell f g) :
      NativeF55P85HorizontalFourCell g f
  | trans

      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v}
      (fg : NativeF55P85HorizontalFourCell f g)
      (gh : NativeF55P85HorizontalFourCell g h) :
      NativeF55P85HorizontalFourCell f h
  | leftWhisker

      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {u v w : KuuNativeF45Tree.DepthRotationRoute p first last}
      (prior : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v)
      {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p v w}
      (witness : NativeF55P85HorizontalFourCell f g) :
      NativeF55P85HorizontalFourCell (.trans prior f) (.trans prior g)
  | rightWhisker

      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {u v w : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v}
      (witness : NativeF55P85HorizontalFourCell f g)
      (suffix : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p v w) :
      NativeF55P85HorizontalFourCell (.trans f suffix) (.trans g suffix)
  | horizontalLeft

      {n n' m m' k k' l l' : Nat}
      {p₀ p₁ p₂ : KuuNativeBlocks a b}
      {q₀ q₁ q₂ : KuuNativeBlocks x y}
      {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
      {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
      {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
      {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
      {u u' : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter}
      {v v' : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter}
      {f f' : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u u'}
      (witness : NativeF55P80UnitFourCell f f')
      (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p v v') :
      NativeF55P85HorizontalFourCell
        (f.horizontal g) (f'.horizontal g)
  | horizontalRight

      {n n' m m' k k' l l' : Nat}
      {p₀ p₁ p₂ : KuuNativeBlocks a b}
      {q₀ q₁ q₂ : KuuNativeBlocks x y}
      {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
      {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
      {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
      {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
      {u u' : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter}
      {v v' : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter}
      (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u u')
      {g g' : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p v v'}
      (witness : NativeF55P80UnitFourCell g g') :
      NativeF55P85HorizontalFourCell
        (f.horizontal g) (f.horizontal g')

variable {p : Polygon} {a b : D} {x y : E}
variable {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}
variable {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
variable {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v}

/-- Every SOURCE P85 Type-valued 4-cell admits an actual certified
path comparison in the NEW P84 presentation. The induction covers
all eight constructors, not just the two horizontal generators. -/
theorem NativeF55P85HorizontalFourCell.p84_sound
    (h : NativeF55P85HorizontalFourCell f g) :
    NativeF55P84HorizontalPathRel first last
      f.toNativeStrictPath g.toNativeStrictPath := by
  induction h with
  | old w => exact .old w.p62_sound
  | refl raw => exact .refl _
  | symm h ih => exact .symm ih
  | trans hfg hgh ihfg ihgh => exact .trans ihfg ihgh
  | leftWhisker prior h ih =>
      exact .comp (.refl prior.toNativeStrictPath) ih
  | rightWhisker h suffix ih =>
      exact .comp ih (.refl suffix.toNativeStrictPath)
  | horizontalLeft witness g => exact .horizontalLeft witness g
  | horizontalRight f witness => exact .horizontalRight f witness

/-- Independently from P84 path soundness, every P85 source 4-cell
preserves the original complete F55 shadow. In particular no
equality of chosen scalar shadows CREATES a 4-cell witness. -/
theorem NativeF55P85HorizontalFourCell.shadow_sound
    (h : NativeF55P85HorizontalFourCell f g) :
    f.nativeShadow = g.nativeShadow := by
  induction h with
  | old w => exact w.shadow_sound
  | refl raw => rfl
  | symm h ih => exact ih.symm
  | trans hfg hgh ihfg ihgh => exact ihfg.trans ihgh
  | leftWhisker prior h ih =>
      change prior.nativeShadow + _ = prior.nativeShadow + _
      rw [ih]
  | rightWhisker h suffix ih =>
      change _ + suffix.nativeShadow = _ + suffix.nativeShadow
      rw [ih]
  | horizontalLeft witness g =>
      simpa only [KuuNativeF45Tree.DepthRotationRoute.PresentedCell.horizontal_nativeShadow] using
        congrArg (fun z : KuuNativeF55Shadow => z + g.nativeShadow)
          witness.shadow_sound
  | horizontalRight f witness =>
      simpa only [KuuNativeF45Tree.DepthRotationRoute.PresentedCell.horizontal_nativeShadow] using
        congrArg (fun z : KuuNativeF55Shadow => f.nativeShadow + z)
          witness.shadow_sound

/-- Horizontal source transport is already proof-relevant in BOTH
original P80 inputs and produces a single new P85 certificate,
through an actual intermediate horizontal raw proof. -/
def nativeF55P85Horizontal_twoSided
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    {r r' : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter}
    {s s' : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter}
    {f f' : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r r'}
    {g g' : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p s s'}
    (hf : NativeF55P80UnitFourCell f f')
    (hg : NativeF55P80UnitFourCell g g') :
    NativeF55P85HorizontalFourCell
      (f.horizontal g) (f'.horizontal g') :=
  .trans (.horizontalLeft hf g) (.horizontalRight f' hg)

/-- The new source four-cell witnesses generate an EXACT local
Setoid kernel, with mere existence used only at the Prop boundary. -/
def nativeF55P85FourSetoid
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (u v : KuuNativeF45Tree.DepthRotationRoute p first last) :
    Setoid (KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v) where
  r := fun f g => Nonempty (NativeF55P85HorizontalFourCell f g)
  iseqv := ⟨
    (fun raw => ⟨.refl raw⟩),
    (fun h => h.elim (fun w => ⟨.symm w⟩)),
    (fun h k => h.elim (fun w => k.elim (fun v => ⟨.trans w v⟩)))⟩

/-- Quotient on the ORIGINAL F55 raw proof source, with no
information loss concealed in the upstream raw proof grammar. -/
abbrev NativeF55P85FourClasses
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (u v : KuuNativeF45Tree.DepthRotationRoute p first last) :=
  _root_.Quotient (nativeF55P85FourSetoid first last u v)

def nativeF55P85FourClass
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    (raw : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v) :
    NativeF55P85FourClasses first last u v :=
  _root_.Quotient.mk _ raw

/-- Precise quotient kernel: an equality of raw P85 classes is
equivalent to the existence of a genuinely generated P85 4-cell. -/
theorem nativeF55P85FourClass_eq_iff
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v) :
    nativeF55P85FourClass first last f =
      nativeF55P85FourClass first last g ↔
      Nonempty (NativeF55P85HorizontalFourCell f g) := by
  constructor
  · intro eq
    exact _root_.Quotient.exact eq
  · intro hw
    exact _root_.Quotient.sound hw

/-- Class equality at source entails the independently defined P84
path relation, but the converse is NOT forced by an observer. -/
theorem nativeF55P85FourClass_eq_implies_P84
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v)
    (h : nativeF55P85FourClass first last f =
      nativeF55P85FourClass first last g) :
    NativeF55P84HorizontalPathRel first last
      f.toNativeStrictPath g.toNativeStrictPath := by
  obtain ⟨witness⟩ := (nativeF55P85FourClass_eq_iff first last f g).mp h
  exact witness.p84_sound

/-- Full original F55 signed charges and exchange parity descend
through the source P85 proof-relevant 4-cell quotient. -/
def nativeF55P85FourToShadow
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (u v : KuuNativeF45Tree.DepthRotationRoute p first last) :
    NativeF55P85FourClasses first last u v → KuuNativeF55Shadow :=
  _root_.Quotient.lift
    (fun raw => raw.nativeShadow)
    (by
      intro f g h
      rcases h with ⟨w⟩
      exact w.shadow_sound)

/-- Vertical composition survives P85 source four-cell changes in
both operands by ACTUAL two-sided vertical 4-cell whiskering. -/
def nativeF55P85VerticalComp
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {u v w : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P85FourClasses first last u v)
    (g : NativeF55P85FourClasses first last v w) :
    NativeF55P85FourClasses first last u w :=
  Quot.liftOn₂ f g
    (fun left right =>
      nativeF55P85FourClass first last (.trans left right))
    (by
      intro left right₁ right₂ hr
      apply Quot.sound
      rcases hr with ⟨witness⟩
      exact ⟨NativeF55P85HorizontalFourCell.leftWhisker left witness⟩)
    (by
      intro left₁ left₂ right hl
      apply Quot.sound
      rcases hl with ⟨witness⟩
      exact ⟨NativeF55P85HorizontalFourCell.rightWhisker witness right⟩)

/-- An explicit, separately chosen strict LOCAL vertical Mathlib
Category on original F54 raw route objects, with P85 proof quotient
classes as Homs. Old P77 unit/assoc 4-cells supply the laws. -/
@[reducible] def nativeF55P85VerticalCategory
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    Category (KuuNativeF45Tree.DepthRotationRoute p first last) where
  Hom := NativeF55P85FourClasses first last
  id route := nativeF55P85FourClass first last (.ident route)
  comp f g := nativeF55P85VerticalComp first last f g
  id_comp := by
    intro X Y f
    refine Quot.inductionOn f (fun raw => ?_)
    change nativeF55P85FourClass first last (.trans (.ident X) raw) =
      nativeF55P85FourClass first last raw
    exact Quot.sound ⟨NativeF55P85HorizontalFourCell.old
      (NativeF55P80UnitFourCell.old
        (NativeF55RawVerticalFourCell.leftUnit raw))⟩
  comp_id := by
    intro X Y f
    refine Quot.inductionOn f (fun raw => ?_)
    change nativeF55P85FourClass first last (.trans raw (.ident Y)) =
      nativeF55P85FourClass first last raw
    exact Quot.sound ⟨NativeF55P85HorizontalFourCell.old
      (NativeF55P80UnitFourCell.old
        (NativeF55RawVerticalFourCell.rightUnit raw))⟩
  assoc := by
    intro W X Y Z f g h
    refine Quot.inductionOn f (fun left => ?_)
    refine Quot.inductionOn g (fun middle => ?_)
    refine Quot.inductionOn h (fun right => ?_)
    change nativeF55P85FourClass first last
      (.trans (.trans left middle) right) =
      nativeF55P85FourClass first last
      (.trans left (.trans middle right))
    exact Quot.sound ⟨NativeF55P85HorizontalFourCell.old
      (NativeF55P80UnitFourCell.old
        (NativeF55RawVerticalFourCell.assoc left middle right))⟩

/-- Original full selected shadow is additive on the P85 strict
local vertical category; raw F55 syntax has not been equated. -/
theorem nativeF55P85VerticalShadow_comp
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {u v w : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P85FourClasses first last u v)
    (g : NativeF55P85FourClasses first last v w) :
    nativeF55P85FourToShadow first last u w
      (nativeF55P85VerticalComp first last f g) =
        nativeF55P85FourToShadow first last u v f +
          nativeF55P85FourToShadow first last v w g := by
  refine Quot.inductionOn f (fun left => ?_)
  refine Quot.inductionOn g (fun right => ?_)
  rfl

/-- OLD P80 classes map to the NEW P85 quotient through their
identical original raw F55 witnesses; no source history is rewritten. -/
def nativeF55P80ToP85
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P80UnitFourClasses first last u v) :
    NativeF55P85FourClasses first last u v :=
  Quot.liftOn f
    (fun raw => nativeF55P85FourClass first last raw)
    (by
      intro left right h
      apply Quot.sound
      rcases h with ⟨w⟩
      exact ⟨NativeF55P85HorizontalFourCell.old w⟩)

/-- Every P85 class is represented by an original raw F55 proof,
hence by an old P80 class: surjective, NOT injective. -/
theorem nativeF55P80ToP85_surjective
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (u v : KuuNativeF45Tree.DepthRotationRoute p first last) :
    Function.Surjective
      (nativeF55P80ToP85 first last (u := u) (v := v)) := by
  intro z
  refine Quot.inductionOn z (fun raw => ?_)
  exact ⟨nativeF55P80UnitFourClass first last raw, rfl⟩

/-- Genuine TWO-INPUT horizontal action: P80 equivalence in
EITHER original input is respected after passage to P85 output,
with explicit independent Type-valued four-cell witnesses.
No same-shadow quotient is being used as its kernel. -/
def nativeF55P80HorizontalToP85
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    {r r' : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter}
    {s s' : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter}
    (f : NativeF55P80UnitFourClasses leftBefore leftAfter r r')
    (g : NativeF55P80UnitFourClasses rightBefore rightAfter s s') :
    NativeF55P85FourClasses
      (KuuNativeF45Tree.node leftBefore rightBefore)
      (KuuNativeF45Tree.node leftAfter rightAfter)
      (.trans (.leftContext r rightBefore) (.rightContext leftAfter s))
      (.trans (.leftContext r' rightBefore) (.rightContext leftAfter s')) :=
  Quot.liftOn₂ f g
    (fun left right =>
      nativeF55P85FourClass _ _ (left.horizontal right))
    (by
      intro left right₁ right₂ hr
      apply Quot.sound
      rcases hr with ⟨w⟩
      exact ⟨NativeF55P85HorizontalFourCell.horizontalRight left w⟩)
    (by
      intro left₁ left₂ right hl
      apply Quot.sound
      rcases hl with ⟨w⟩
      exact ⟨NativeF55P85HorizontalFourCell.horizontalLeft w right⟩)

/-- The P80×P80→P85 binary map computes on unchanged original
raw F55 proof representatives, with no inferred source equality. -/
@[simp] theorem nativeF55P80HorizontalToP85_raw
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    {r r' : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter}
    {s s' : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r r')
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p s s') :
    nativeF55P80HorizontalToP85
      (nativeF55P80UnitFourClass leftBefore leftAfter f)
      (nativeF55P80UnitFourClass rightBefore rightAfter g) =
    nativeF55P85FourClass _ _ (f.horizontal g) := rfl

/-- The TRUE north C60 pentagon P82 horizontal obstruction:
distinct OLD P80 quotient classes become equal in the NEW P85
Type-valued four-cell quotient, by an ACTUAL source witness.
Nothing is inferred from equal numerical observer readings. -/
theorem northNativeP85_oldP80_ne_newP85_eq :
    nativeF55P80UnitFourClass _ _
      ((KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans
        (.ident northNativeF45PentagonLong)
        northNativeF55PentagonCell).horizontal
        (.ident northNativeP82RightUnitRoute)) ≠
    nativeF55P80UnitFourClass _ _
      (northNativeF55PentagonCell.horizontal
        (.ident northNativeP82RightUnitRoute)) ∧
    nativeF55P85FourClass _ _
      ((KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans
        (.ident northNativeF45PentagonLong)
        northNativeF55PentagonCell).horizontal
        (.ident northNativeP82RightUnitRoute)) =
    nativeF55P85FourClass _ _
      (northNativeF55PentagonCell.horizontal
        (.ident northNativeP82RightUnitRoute)) := by
  constructor
  · exact nativeF55P82_horizontal_oldLeftUnit_class_ne
      northNativeF55PentagonCell northNativeP82RightUnitRoute rfl (by decide)
  · apply Quot.sound
    exact ⟨NativeF55P85HorizontalFourCell.horizontalLeft
      (NativeF55P80UnitFourCell.old
        (NativeF55RawVerticalFourCell.leftUnit northNativeF55PentagonCell))
      (.ident northNativeP82RightUnitRoute)⟩

#print axioms NativeF55P85HorizontalFourCell
#print axioms NativeF55P85HorizontalFourCell.p84_sound
#print axioms NativeF55P85HorizontalFourCell.shadow_sound
#print axioms nativeF55P85Horizontal_twoSided
#print axioms nativeF55P85FourSetoid
#print axioms NativeF55P85FourClasses
#print axioms nativeF55P85FourClass
#print axioms nativeF55P85FourClass_eq_iff
#print axioms nativeF55P85FourClass_eq_implies_P84
#print axioms nativeF55P85FourToShadow
#print axioms nativeF55P85VerticalComp
#print axioms nativeF55P85VerticalCategory
#print axioms nativeF55P85VerticalShadow_comp
#print axioms nativeF55P80ToP85
#print axioms nativeF55P80ToP85_surjective
#print axioms nativeF55P80HorizontalToP85
#print axioms nativeF55P80HorizontalToP85_raw
#print axioms northNativeP85_oldP80_ne_newP85_eq

end
end Kuu.F112.Physical
