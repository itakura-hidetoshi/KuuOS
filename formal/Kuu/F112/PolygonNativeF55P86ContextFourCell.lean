import Kuu.F112.PolygonNativeF55P86ContextPathCongruence

/-!
# F112-P86B — source Type-valued four-cell transport under F55 contexts

P85's selected Type-valued horizontal four-cell presentation
cannot be silently assumed stable under every context and F54
pre/postcompose operation. The new P86A path congruence explicitly
adds source-witness comparisons for those contexts, retaining the old
P84 relation and source proof histories without altering P62/P80/P85.

P86B now constructs a SEPARATE Type-valued 4-cell language on original
nine-generator F55 3-proofs. Its 12 constructors consist of all P85
source evidence, equivalence and two-sided vertical whiskers, and
left/right binary contexts, pre/post F54 routes, and left/right
horizontal pastes of ANY original P85 Type-valued four-cell witness.
Each constructor has genuine dependent F54 endpoints and carries
actual old source certificates rather than a scalar shadow.

Every new 4-cell is sound for the exactly selected P86A path relation,
and separately preserves both signed integer charges and the ZMod 2
phase. We build its exact Setoid/Quotient, a strict local vertical
Mathlib Category, surjective old P85-to-P86 comparison, and explicit
representative-independent context/route operations.

As a positive frontier, the ORIGINAL F55 horizontal pasting now
descends bivariately from P85×P85 to the NEW P86 four-cell quotient,
with genuine two-sided 4-cell change witnesses. This is NOT the
still unproved P86×P86 horizontal bifunctor or strict interchange.

The actual north C60 pentagon supplies a new source 4-cell obtained
by applying an original F45 binary context to the existing physical
P85 witness. Its prior P82/P83 negative facts remain true.

No Gray, sorry, admit, new axioms or excluded legacy public roots.
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

/-- Exactly 12 original-shape SOURCE proof constructors; new
context and horizontal generators retain actual Type-valued
old-P85 certificates on ORIGINAL raw 3-proof boundaries. -/
inductive NativeF55P86ContextFourCell
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
      (witness : NativeF55P85HorizontalFourCell f g) :
      NativeF55P86ContextFourCell f g
  | refl

      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
      (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v) :
      NativeF55P86ContextFourCell f f
  | symm

      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v}
      (h : NativeF55P86ContextFourCell f g) :
      NativeF55P86ContextFourCell g f
  | trans

      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v}
      (fg : NativeF55P86ContextFourCell f g)
      (gh : NativeF55P86ContextFourCell g h) :
      NativeF55P86ContextFourCell f h
  | leftWhisker

      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {u v w : KuuNativeF45Tree.DepthRotationRoute p first last}
      (prior : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v)
      {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p v w}
      (h : NativeF55P86ContextFourCell f g) :
      NativeF55P86ContextFourCell (.trans prior f) (.trans prior g)
  | rightWhisker

      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {u v w : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v}
      (h : NativeF55P86ContextFourCell f g)
      (suffix : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p v w) :
      NativeF55P86ContextFourCell (.trans f suffix) (.trans g suffix)
  | leftContext

      {n n' m m' k l : Nat}
      {ma mb mc : KuuNativeBlocks a b}
      {pa pb pc : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v}
      (h : NativeF55P85HorizontalFourCell f g)
      (later : KuuNativeF45Tree p k l mb pb mc pc) :
      NativeF55P86ContextFourCell
        (.leftContext f later) (.leftContext g later)
  | rightContext

      {k l n n' m m' : Nat}
      {ma mb mc : KuuNativeBlocks a b}
      {pa pb pc : KuuNativeBlocks x y}
      (earlier : KuuNativeF45Tree p k l ma pa mb pb)
      {first : KuuNativeF45Tree p n m mb pb mc pc}
      {last : KuuNativeF45Tree p n' m' mb pb mc pc}
      {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v}
      (h : NativeF55P85HorizontalFourCell f g) :
      NativeF55P86ContextFourCell
        (.rightContext earlier f) (.rightContext earlier g)
  | precompose

      {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n₁ m₁ ma pa mb pb}
      {middle : KuuNativeF45Tree p n₂ m₂ ma pa mb pb}
      {last : KuuNativeF45Tree p n₃ m₃ ma pa mb pb}
      (prior : KuuNativeF45Tree.DepthRotationRoute p first middle)
      {r s : KuuNativeF45Tree.DepthRotationRoute p middle last}
      {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
      (h : NativeF55P85HorizontalFourCell f g) :
      NativeF55P86ContextFourCell
        (.precompose prior f) (.precompose prior g)
  | postcompose

      {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n₁ m₁ ma pa mb pb}
      {middle : KuuNativeF45Tree p n₂ m₂ ma pa mb pb}
      {last : KuuNativeF45Tree p n₃ m₃ ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first middle}
      {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
      (h : NativeF55P85HorizontalFourCell f g)
      (suffix : KuuNativeF45Tree.DepthRotationRoute p middle last) :
      NativeF55P86ContextFourCell
        (.postcompose f suffix) (.postcompose g suffix)
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
      (h : NativeF55P85HorizontalFourCell f f')
      (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p v v') :
      NativeF55P86ContextFourCell
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
      (h : NativeF55P85HorizontalFourCell g g') :
      NativeF55P86ContextFourCell
        (f.horizontal g) (f.horizontal g')

variable {p : Polygon} {a b : D} {x y : E}
variable {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}
variable {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
variable {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v}

/-- Genuine Type-valued P86 source evidence is sound for EXACTLY
the chosen P86 path relation, not for P84/P62 by assertion.
All twelve constructors have a separate actual witness branch. -/
theorem NativeF55P86ContextFourCell.p86_sound
    (h : NativeF55P86ContextFourCell f g) :
    NativeF55P86ContextPathRel first last
      f.toNativeStrictPath g.toNativeStrictPath := by
  induction h with
  | old witness => exact .old witness.p84_sound
  | refl raw => exact .refl _
  | symm witness ih => exact .symm ih
  | trans fg gh ihfg ihgh => exact .trans ihfg ihgh
  | leftWhisker prior witness ih =>
      exact .comp (.refl prior.toNativeStrictPath) ih
  | rightWhisker witness suffix ih =>
      exact .comp ih (.refl suffix.toNativeStrictPath)
  | leftContext witness later => exact .leftContext witness later
  | rightContext earlier witness => exact .rightContext earlier witness
  | precompose prior witness => exact .precompose prior witness
  | postcompose witness suffix => exact .postcompose witness suffix
  | horizontalLeft witness g => exact .horizontalLeft witness g
  | horizontalRight f witness => exact .horizontalRight f witness

/-- Independent ORIGINAL full F55 shadow soundness over every P86
source four-cell constructor, separately from path presentation. -/
theorem NativeF55P86ContextFourCell.shadow_sound
    (h : NativeF55P86ContextFourCell f g) :
    f.nativeShadow = g.nativeShadow := by
  induction h with
  | old witness => exact witness.shadow_sound
  | refl raw => rfl
  | symm witness ih => exact ih.symm
  | trans fg gh ihfg ihgh => exact ihfg.trans ihgh
  | leftWhisker prior witness ih =>
      change prior.nativeShadow + _ = prior.nativeShadow + _
      rw [ih]
  | rightWhisker witness suffix ih =>
      change _ + suffix.nativeShadow = _ + suffix.nativeShadow
      rw [ih]
  | leftContext witness later => exact witness.shadow_sound
  | rightContext earlier witness => exact witness.shadow_sound
  | precompose prior witness => exact witness.shadow_sound
  | postcompose witness suffix => exact witness.shadow_sound
  | horizontalLeft witness g =>
      simpa only [KuuNativeF45Tree.DepthRotationRoute.PresentedCell.horizontal_nativeShadow] using
        congrArg (fun z : KuuNativeF55Shadow => z + g.nativeShadow)
          witness.shadow_sound
  | horizontalRight f witness =>
      simpa only [KuuNativeF45Tree.DepthRotationRoute.PresentedCell.horizontal_nativeShadow] using
        congrArg (fun z : KuuNativeF55Shadow => f.nativeShadow + z)
          witness.shadow_sound

/-- Two actual independent P85 four-cell changes yield a
typed original horizontal comparison in the NEW P86 source. -/
def nativeF55P86Horizontal_twoSided
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
    (hf : NativeF55P85HorizontalFourCell f f')
    (hg : NativeF55P85HorizontalFourCell g g') :
    NativeF55P86ContextFourCell (f.horizontal g) (f'.horizontal g') :=
  .trans (.horizontalLeft hf g) (.horizontalRight f' hg)

/-- Actual source 4-cell witnesses generate the exact P86 Setoid.
The Setoid is NOT defined by shadow or P86 path equality. -/
def nativeF55P86FourSetoid
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (u v : KuuNativeF45Tree.DepthRotationRoute p first last) :
    Setoid (KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v) where
  r := fun f g => Nonempty (NativeF55P86ContextFourCell f g)
  iseqv := ⟨
    (fun raw => ⟨.refl raw⟩),
    (fun h => h.elim (fun w => ⟨.symm w⟩)),
    (fun h k => h.elim (fun w => k.elim (fun v => ⟨.trans w v⟩)))⟩

/-- Exact quotient on ORIGINAL raw F55 3-proof syntax. -/
abbrev NativeF55P86FourClasses
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (u v : KuuNativeF45Tree.DepthRotationRoute p first last) :=
  _root_.Quotient (nativeF55P86FourSetoid first last u v)

def nativeF55P86FourClass
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    (raw : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v) :
    NativeF55P86FourClasses first last u v :=
  _root_.Quotient.mk _ raw

/-- Quotient equality IFF source Type-valued P86 four-cell witness
exists; it is never replaced by same-shadow equality. -/
theorem nativeF55P86FourClass_eq_iff
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v) :
    nativeF55P86FourClass first last f =
      nativeF55P86FourClass first last g ↔
      Nonempty (NativeF55P86ContextFourCell f g) := by
  constructor
  · intro heq
    exact _root_.Quotient.exact heq
  · intro hw
    exact _root_.Quotient.sound hw

/-- Every concrete source equality in P86 is sound in the
independent NEW P86 typed free-path relation. -/
theorem nativeF55P86FourClass_eq_implies_path
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v)
    (h : nativeF55P86FourClass first last f =
      nativeF55P86FourClass first last g) :
    NativeF55P86ContextPathRel first last
      f.toNativeStrictPath g.toNativeStrictPath := by
  obtain ⟨w⟩ := (nativeF55P86FourClass_eq_iff first last f g).mp h
  exact w.p86_sound

/-- The full selected (Int × Int) × ZMod 2 original F55 shadow
descends exactly from actual P86 Type-valued source witnesses. -/
def nativeF55P86FourToShadow
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (u v : KuuNativeF45Tree.DepthRotationRoute p first last) :
    NativeF55P86FourClasses first last u v → KuuNativeF55Shadow :=
  _root_.Quotient.lift
    (fun raw => raw.nativeShadow)
    (by
      intro f g h
      rcases h with ⟨w⟩
      exact w.shadow_sound)

/-- Both original vertical raw proof operands admit independent
four-cell representative changes in the new P86 quotient. -/
def nativeF55P86VerticalComp
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {u v w : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P86FourClasses first last u v)
    (g : NativeF55P86FourClasses first last v w) :
    NativeF55P86FourClasses first last u w :=
  Quot.liftOn₂ f g
    (fun left right =>
      nativeF55P86FourClass first last (.trans left right))
    (by
      intro left right₁ right₂ hr
      apply Quot.sound
      rcases hr with ⟨witness⟩
      exact ⟨NativeF55P86ContextFourCell.leftWhisker left witness⟩)
    (by
      intro left₁ left₂ right hl
      apply Quot.sound
      rcases hl with ⟨witness⟩
      exact ⟨NativeF55P86ContextFourCell.rightWhisker witness right⟩)

/-- Genuine strict LOCAL vertical Mathlib Category on the old
F54 route objects and the new proof-relevant P86 four-cell quotient. -/
@[reducible] def nativeF55P86VerticalCategory
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    Category (KuuNativeF45Tree.DepthRotationRoute p first last) where
  Hom := NativeF55P86FourClasses first last
  id route := nativeF55P86FourClass first last (.ident route)
  comp f g := nativeF55P86VerticalComp first last f g
  id_comp := by
    intro X Y f
    refine Quot.inductionOn f (fun raw => ?_)
    change nativeF55P86FourClass first last (.trans (.ident X) raw) =
      nativeF55P86FourClass first last raw
    exact Quot.sound ⟨NativeF55P86ContextFourCell.old
      (NativeF55P85HorizontalFourCell.old
        (NativeF55P80UnitFourCell.old
          (NativeF55RawVerticalFourCell.leftUnit raw)))⟩
  comp_id := by
    intro X Y f
    refine Quot.inductionOn f (fun raw => ?_)
    change nativeF55P86FourClass first last (.trans raw (.ident Y)) =
      nativeF55P86FourClass first last raw
    exact Quot.sound ⟨NativeF55P86ContextFourCell.old
      (NativeF55P85HorizontalFourCell.old
        (NativeF55P80UnitFourCell.old
          (NativeF55RawVerticalFourCell.rightUnit raw)))⟩
  assoc := by
    intro W X Y Z f g h
    refine Quot.inductionOn f (fun a => ?_)
    refine Quot.inductionOn g (fun b => ?_)
    refine Quot.inductionOn h (fun c => ?_)
    change nativeF55P86FourClass first last
      (.trans (.trans a b) c) =
      nativeF55P86FourClass first last
        (.trans a (.trans b c))
    exact Quot.sound ⟨NativeF55P86ContextFourCell.old
      (NativeF55P85HorizontalFourCell.old
        (NativeF55P80UnitFourCell.old
          (NativeF55RawVerticalFourCell.assoc a b c)))⟩

/-- Vertical original full F55 shadow remains additive on
P86's chosen proof-relevant strict local vertical category. -/
theorem nativeF55P86VerticalShadow_comp
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {u v w : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P86FourClasses first last u v)
    (g : NativeF55P86FourClasses first last v w) :
    nativeF55P86FourToShadow first last u w
      (nativeF55P86VerticalComp first last f g) =
        nativeF55P86FourToShadow first last u v f +
          nativeF55P86FourToShadow first last v w g := by
  refine Quot.inductionOn f (fun left => ?_)
  refine Quot.inductionOn g (fun right => ?_)
  rfl

/-- The OLD P85 class maps to the NEW P86 class of EXACTLY the
same original raw F55 3-proof representative. -/
def nativeF55P85ToP86
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P85FourClasses first last u v) :
    NativeF55P86FourClasses first last u v :=
  Quot.liftOn f
    (fun raw => nativeF55P86FourClass first last raw)
    (by
      intro left right h
      apply Quot.sound
      rcases h with ⟨w⟩
      exact ⟨NativeF55P86ContextFourCell.old w⟩)

/-- Every P86 class has an original raw representative and
therefore comes from an OLD P85 class; no injectivity claim. -/
theorem nativeF55P85ToP86_surjective
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (u v : KuuNativeF45Tree.DepthRotationRoute p first last) :
    Function.Surjective
      (nativeF55P85ToP86 first last (u := u) (v := v)) := by
  intro z
  refine Quot.inductionOn z (fun raw => ?_)
  exact ⟨nativeF55P85FourClass first last raw, rfl⟩

/-- Compatible exact source P85→P86 map preserves every true
raw vertical composite (no observer equality used). -/
theorem nativeF55P85ToP86_comp
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {u v w : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P85FourClasses first last u v)
    (g : NativeF55P85FourClasses first last v w) :
    nativeF55P85ToP86 first last
      (nativeF55P85VerticalComp first last f g) =
    nativeF55P86VerticalComp first last
      (nativeF55P85ToP86 first last f)
      (nativeF55P85ToP86 first last g) := by
  refine Quot.inductionOn f (fun left => ?_)
  refine Quot.inductionOn g (fun right => ?_)
  rfl

/-- Original source left binary context is now a well-defined
P85 quotient → NEW P86 quotient operation, proved by actual
Type-valued P85 witness transport, not by full-shadow equality. -/
def nativeF55P85LeftContextToP86
    {k l : Nat}
    {mc : KuuNativeBlocks a b}
    {pc : KuuNativeBlocks x y}
    (later : KuuNativeF45Tree p k l mb pb mc pc)
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P85FourClasses first last u v) :
    NativeF55P86FourClasses
      (KuuNativeF45Tree.node first later)
      (KuuNativeF45Tree.node last later)
      (.leftContext u later) (.leftContext v later) :=
  Quot.liftOn f
    (fun raw => nativeF55P86FourClass _ _ (.leftContext raw later))
    (by
      intro raw₁ raw₂ heq
      apply Quot.sound
      rcases heq with ⟨w⟩
      exact ⟨NativeF55P86ContextFourCell.leftContext w later⟩)

/-- Genuine original F54 right binary context on each P85 class,
descending into the new P86 quotient by Type-valued evidence. -/
def nativeF55P85RightContextToP86
    {k l n n' m m' : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    (earlier : KuuNativeF45Tree p k l ma pa mb pb)
    (first : KuuNativeF45Tree p n m mb pb mc pc)
    (last : KuuNativeF45Tree p n' m' mb pb mc pc)
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P85FourClasses first last u v) :
    NativeF55P86FourClasses
      (KuuNativeF45Tree.node earlier first)
      (KuuNativeF45Tree.node earlier last)
      (.rightContext earlier u) (.rightContext earlier v) :=
  Quot.liftOn f
    (fun raw => nativeF55P86FourClass _ _ (.rightContext earlier raw))
    (by
      intro raw₁ raw₂ heq
      apply Quot.sound
      rcases heq with ⟨w⟩
      exact ⟨NativeF55P86ContextFourCell.rightContext earlier w⟩)

/-- True F54 precomposition with a typed prior route now
descends from P85 proof quotient to the new P86 proof quotient. -/
def nativeF55P85PrecomposeToP86
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n₁ m₁ ma pa mb pb)
    (middle : KuuNativeF45Tree p n₂ m₂ ma pa mb pb)
    (last : KuuNativeF45Tree p n₃ m₃ ma pa mb pb)
    (prior : KuuNativeF45Tree.DepthRotationRoute p first middle)
    {u v : KuuNativeF45Tree.DepthRotationRoute p middle last}
    (f : NativeF55P85FourClasses middle last u v) :
    NativeF55P86FourClasses first last
      (.trans prior u) (.trans prior v) :=
  Quot.liftOn f
    (fun raw => nativeF55P86FourClass first last (.precompose prior raw))
    (by
      intro raw₁ raw₂ heq
      apply Quot.sound
      rcases heq with ⟨w⟩
      exact ⟨NativeF55P86ContextFourCell.precompose prior w⟩)

/-- True F54 postcomposition with a typed suffix now
descends to the new P86 quotient through actual P85 witnesses. -/
def nativeF55P85PostcomposeToP86
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n₁ m₁ ma pa mb pb)
    (middle : KuuNativeF45Tree p n₂ m₂ ma pa mb pb)
    (last : KuuNativeF45Tree p n₃ m₃ ma pa mb pb)
    {u v : KuuNativeF45Tree.DepthRotationRoute p first middle}
    (f : NativeF55P85FourClasses first middle u v)
    (suffix : KuuNativeF45Tree.DepthRotationRoute p middle last) :
    NativeF55P86FourClasses first last
      (.trans u suffix) (.trans v suffix) :=
  Quot.liftOn f
    (fun raw => nativeF55P86FourClass first last (.postcompose raw suffix))
    (by
      intro raw₁ raw₂ heq
      apply Quot.sound
      rcases heq with ⟨w⟩
      exact ⟨NativeF55P86ContextFourCell.postcompose w suffix⟩)

/-- TRUE two-input horizontal P85×P85→P86 source operation.
For both independent quotient arguments, changes of representatives
are justified by original Type-valued P85 witnesses. -/
def nativeF55P85HorizontalToP86
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    {r r' : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter}
    {s s' : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter}
    (f : NativeF55P85FourClasses leftBefore leftAfter r r')
    (g : NativeF55P85FourClasses rightBefore rightAfter s s') :
    NativeF55P86FourClasses
      (KuuNativeF45Tree.node leftBefore rightBefore)
      (KuuNativeF45Tree.node leftAfter rightAfter)
      (.trans (.leftContext r rightBefore) (.rightContext leftAfter s))
      (.trans (.leftContext r' rightBefore) (.rightContext leftAfter s')) :=
  Quot.liftOn₂ f g
    (fun left right =>
      nativeF55P86FourClass _ _ (left.horizontal right))
    (by
      intro left right₁ right₂ hr
      apply Quot.sound
      rcases hr with ⟨w⟩
      exact ⟨NativeF55P86ContextFourCell.horizontalRight left w⟩)
    (by
      intro left₁ left₂ right hl
      apply Quot.sound
      rcases hl with ⟨w⟩
      exact ⟨NativeF55P86ContextFourCell.horizontalLeft w right⟩)

/-- P85×P85→P86 binary operation computes on the SAME original
source raw F55 proofs, never an invented replacement proof label. -/
@[simp] theorem nativeF55P85HorizontalToP86_raw
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
    nativeF55P85HorizontalToP86
      (nativeF55P85FourClass leftBefore leftAfter f)
      (nativeF55P85FourClass rightBefore rightAfter g) =
    nativeF55P86FourClass _ _ (f.horizontal g) := rfl

/-- A TRUE physical C60 north-pentagon source witness can now
be placed in an additional original F45 binary context, retaining
the original old-P85 witness at its exact raw endpoints. -/
theorem northNativeP86LeftContext_fourWitness :
    Nonempty (NativeF55P86ContextFourCell
      (.leftContext
        ((KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans
          (.ident northNativeF45PentagonLong)
          northNativeF55PentagonCell).horizontal
            (.ident northNativeP82RightUnitRoute))
        northNativeP82RightUnitTree)
      (.leftContext
        (northNativeF55PentagonCell.horizontal
          (.ident northNativeP82RightUnitRoute))
        northNativeP82RightUnitTree)) := by
  exact ⟨.leftContext
    (NativeF55P85HorizontalFourCell.horizontalLeft
      (NativeF55P80UnitFourCell.old
        (NativeF55RawVerticalFourCell.leftUnit northNativeF55PentagonCell))
      (.ident northNativeP82RightUnitRoute))
    northNativeP82RightUnitTree⟩

/-- The physical source context witness yields equality in the
NEW P86 quotient while all old P82/P83 obstruction facts remain. -/
theorem northNativeP86LeftContext_class_eq :
    nativeF55P86FourClass _ _
      (.leftContext
        ((KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans
          (.ident northNativeF45PentagonLong)
          northNativeF55PentagonCell).horizontal
            (.ident northNativeP82RightUnitRoute))
        northNativeP82RightUnitTree) =
    nativeF55P86FourClass _ _
      (.leftContext
        (northNativeF55PentagonCell.horizontal
          (.ident northNativeP82RightUnitRoute))
        northNativeP82RightUnitTree) := by
  exact (nativeF55P86FourClass_eq_iff _ _ _ _).2
    northNativeP86LeftContext_fourWitness

#print axioms NativeF55P86ContextFourCell
#print axioms NativeF55P86ContextFourCell.p86_sound
#print axioms NativeF55P86ContextFourCell.shadow_sound
#print axioms nativeF55P86Horizontal_twoSided
#print axioms nativeF55P86FourSetoid
#print axioms NativeF55P86FourClasses
#print axioms nativeF55P86FourClass
#print axioms nativeF55P86FourClass_eq_iff
#print axioms nativeF55P86FourClass_eq_implies_path
#print axioms nativeF55P86FourToShadow
#print axioms nativeF55P86VerticalComp
#print axioms nativeF55P86VerticalCategory
#print axioms nativeF55P86VerticalShadow_comp
#print axioms nativeF55P85ToP86
#print axioms nativeF55P85ToP86_surjective
#print axioms nativeF55P85ToP86_comp
#print axioms nativeF55P85LeftContextToP86
#print axioms nativeF55P85RightContextToP86
#print axioms nativeF55P85PrecomposeToP86
#print axioms nativeF55P85PostcomposeToP86
#print axioms nativeF55P85HorizontalToP86
#print axioms nativeF55P85HorizontalToP86_raw
#print axioms northNativeP86LeftContext_fourWitness
#print axioms northNativeP86LeftContext_class_eq

end
end Kuu.F112.Physical
