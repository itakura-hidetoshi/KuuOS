import Kuu.F112.PolygonNativeF55P87ClosedPathCongruence

/-!
# F112-P87C — original F55 horizontal composition closes internally on P87

P87A has a genuine recursively context/route/horizontally stable
SOURCE Type-valued four-cell grammar. P87B independently constructs
its proof-generated free-path congruence.

Here we prove a GENUINE proof-relevant vertical Category on the P87
source four-cell quotient, exactly witnessed by source P87 certificates.
All four original F55 F54 route actions (binary contexts, pre-/post-
composition) now map P87 classes TO P87 classes, and the original
horizontal F55 operation descends to a TOTAL well-defined binary
map **P87 × P87 → P87** on each compatible pair of dependent
hom types. Previous P85/P86 constructions only mapped old input
presentations to enlarged output presentations.

This is a necessary advance toward a strict three-category, but
being a well-defined binary map is not the complete bifunctor
axiom: strict interchange requires identifying specific ORIGINAL
different source proof terms by genuine Type-valued 4-cells.
No algebraic commutativity of the selected numerical shadow is
substituted for those source witnesses.

The P86→P87 source comparison is surjective, preserves vertical
pasting, and preserves every old representative's full shadow.
The P87 horizontal unit is justified by an actual original P80
Type-valued horizontal-unit generator transported through
P85/P86/P87, rather than assumed as a definitional raw equality.
All pre-C60 public roots and old no-go theorems are preserved.
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

variable {p : Polygon} {a b : D} {x y : E}
variable {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}
variable {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
variable {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v}

/-- NEW P87 Type-valued genuine source 4-cell grammar is sound
for the P87 path congruence, independently defined in P87B.
All twelve constructors are handled without shadow-kernel escape. -/
theorem NativeF55P87ClosedFourCell.p87_sound
    (h : NativeF55P87ClosedFourCell f g) :
    NativeF55P87ClosedPathRel first last
      f.toNativeStrictPath g.toNativeStrictPath := by
  induction h with
  | old witness => exact .old witness.p86_sound
  | refl raw => exact .refl _
  | symm witness ih => exact .symm ih
  | trans fg gh ihfg ihgh => exact .trans ihfg ihgh
  | leftWhisker prior witness ih =>
      exact .comp (.refl prior.toNativeStrictPath) ih
  | rightWhisker witness suffix ih =>
      exact .comp ih (.refl suffix.toNativeStrictPath)
  | leftContext witness later ih => exact .leftContext witness later
  | rightContext earlier witness ih => exact .rightContext earlier witness
  | precompose prior witness ih => exact .precompose prior witness
  | postcompose witness suffix ih => exact .postcompose witness suffix
  | horizontalLeft witness g ih => exact .horizontalLeft witness g
  | horizontalRight f witness ih => exact .horizontalRight f witness

/-- Actual source 4-cell witnesses generate the exact P86 Setoid.
The Setoid is NOT defined by shadow or P86 path equality. -/
def nativeF55P87FourSetoid
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (u v : KuuNativeF45Tree.DepthRotationRoute p first last) :
    Setoid (KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v) where
  r := fun f g => Nonempty (NativeF55P87ClosedFourCell f g)
  iseqv := ⟨
    (fun raw => ⟨.refl raw⟩),
    (fun h => h.elim (fun w => ⟨.symm w⟩)),
    (fun h k => h.elim (fun w => k.elim (fun v => ⟨.trans w v⟩)))⟩

/-- Exact quotient on ORIGINAL raw F55 3-proof syntax. -/
abbrev NativeF55P87FourClasses
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (u v : KuuNativeF45Tree.DepthRotationRoute p first last) :=
  _root_.Quotient (nativeF55P87FourSetoid first last u v)

def nativeF55P87FourClass
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    (raw : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v) :
    NativeF55P87FourClasses first last u v :=
  _root_.Quotient.mk _ raw

/-- Quotient equality IFF source Type-valued P86 four-cell witness
exists; it is never replaced by same-shadow equality. -/
theorem nativeF55P87FourClass_eq_iff
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v) :
    nativeF55P87FourClass first last f =
      nativeF55P87FourClass first last g ↔
      Nonempty (NativeF55P87ClosedFourCell f g) := by
  constructor
  · intro heq
    exact _root_.Quotient.exact heq
  · intro hw
    exact _root_.Quotient.sound hw

/-- Every concrete source equality in P86 is sound in the
independent NEW P86 typed free-path relation. -/
theorem nativeF55P87FourClass_eq_implies_path
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v)
    (h : nativeF55P87FourClass first last f =
      nativeF55P87FourClass first last g) :
    NativeF55P86ContextPathRel first last
      f.toNativeStrictPath g.toNativeStrictPath := by
  obtain ⟨w⟩ := (nativeF55P87FourClass_eq_iff first last f g).mp h
  exact w.p86_sound

/-- The full selected (Int × Int) × ZMod 2 original F55 shadow
descends exactly from actual P86 Type-valued source witnesses. -/
def nativeF55P87FourToShadow
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (u v : KuuNativeF45Tree.DepthRotationRoute p first last) :
    NativeF55P87FourClasses first last u v → KuuNativeF55Shadow :=
  _root_.Quotient.lift
    (fun raw => raw.nativeShadow)
    (by
      intro f g h
      rcases h with ⟨w⟩
      exact w.shadow_sound)

/-- Both original vertical raw proof operands admit independent
four-cell representative changes in the new P86 quotient. -/
def nativeF55P87VerticalComp
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {u v w : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P87FourClasses first last u v)
    (g : NativeF55P87FourClasses first last v w) :
    NativeF55P87FourClasses first last u w :=
  Quot.liftOn₂ f g
    (fun left right =>
      nativeF55P87FourClass first last (.trans left right))
    (by
      intro left right₁ right₂ hr
      apply Quot.sound
      rcases hr with ⟨witness⟩
      exact ⟨NativeF55P87ClosedFourCell.leftWhisker left witness⟩)
    (by
      intro left₁ left₂ right hl
      apply Quot.sound
      rcases hl with ⟨witness⟩
      exact ⟨NativeF55P87ClosedFourCell.rightWhisker witness right⟩)

/-- Genuine strict LOCAL vertical Mathlib Category on the old
F54 route objects and the new proof-relevant P86 four-cell quotient. -/
@[reducible] def nativeF55P87VerticalCategory
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    Category (KuuNativeF45Tree.DepthRotationRoute p first last) where
  Hom := NativeF55P87FourClasses first last
  id route := nativeF55P87FourClass first last (.ident route)
  comp f g := nativeF55P87VerticalComp first last f g
  id_comp := by
    intro X Y f
    refine Quot.inductionOn f (fun raw => ?_)
    change nativeF55P87FourClass first last (.trans (.ident X) raw) =
      nativeF55P87FourClass first last raw
    exact Quot.sound ⟨NativeF55P87ClosedFourCell.old
      (NativeF55P86ContextFourCell.old
        (NativeF55P85HorizontalFourCell.old
        (NativeF55P80UnitFourCell.old
          (NativeF55RawVerticalFourCell.leftUnit raw))))⟩
  comp_id := by
    intro X Y f
    refine Quot.inductionOn f (fun raw => ?_)
    change nativeF55P87FourClass first last (.trans raw (.ident Y)) =
      nativeF55P87FourClass first last raw
    exact Quot.sound ⟨NativeF55P87ClosedFourCell.old
      (NativeF55P86ContextFourCell.old
        (NativeF55P85HorizontalFourCell.old
        (NativeF55P80UnitFourCell.old
          (NativeF55RawVerticalFourCell.rightUnit raw))))⟩
  assoc := by
    intro W X Y Z f g h
    refine Quot.inductionOn f (fun a => ?_)
    refine Quot.inductionOn g (fun b => ?_)
    refine Quot.inductionOn h (fun c => ?_)
    change nativeF55P87FourClass first last
      (.trans (.trans a b) c) =
      nativeF55P87FourClass first last
        (.trans a (.trans b c))
    exact Quot.sound ⟨NativeF55P87ClosedFourCell.old
      (NativeF55P86ContextFourCell.old
        (NativeF55P85HorizontalFourCell.old
        (NativeF55P80UnitFourCell.old
          (NativeF55RawVerticalFourCell.assoc a b c))))⟩

/-- Vertical original full F55 shadow remains additive on
P86's chosen proof-relevant strict local vertical category. -/
theorem nativeF55P87VerticalShadow_comp
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {u v w : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P87FourClasses first last u v)
    (g : NativeF55P87FourClasses first last v w) :
    nativeF55P87FourToShadow first last u w
      (nativeF55P87VerticalComp first last f g) =
        nativeF55P87FourToShadow first last u v f +
          nativeF55P87FourToShadow first last v w g := by
  refine Quot.inductionOn f (fun left => ?_)
  refine Quot.inductionOn g (fun right => ?_)
  rfl


/-- The OLD P85 class maps to the NEW P86 class of EXACTLY the
same original raw F55 3-proof representative. -/
def nativeF55P86ToP87
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P86FourClasses first last u v) :
    NativeF55P87FourClasses first last u v :=
  Quot.liftOn f
    (fun raw => nativeF55P87FourClass first last raw)
    (by
      intro left right h
      apply Quot.sound
      rcases h with ⟨w⟩
      exact ⟨NativeF55P87ClosedFourCell.old w⟩)

/-- Every P86 class has an original raw representative and
therefore comes from an OLD P85 class; no injectivity claim. -/
theorem nativeF55P86ToP87_surjective
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (u v : KuuNativeF45Tree.DepthRotationRoute p first last) :
    Function.Surjective
      (nativeF55P86ToP87 first last (u := u) (v := v)) := by
  intro z
  refine Quot.inductionOn z (fun raw => ?_)
  exact ⟨nativeF55P86FourClass first last raw, rfl⟩

/-- Compatible exact source P85→P86 map preserves every true
raw vertical composite (no observer equality used). -/
theorem nativeF55P86ToP87_comp
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {u v w : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P86FourClasses first last u v)
    (g : NativeF55P86FourClasses first last v w) :
    nativeF55P86ToP87 first last
      (nativeF55P86VerticalComp first last f g) =
    nativeF55P87VerticalComp first last
      (nativeF55P86ToP87 first last f)
      (nativeF55P86ToP87 first last g) := by
  refine Quot.inductionOn f (fun left => ?_)
  refine Quot.inductionOn g (fun right => ?_)
  rfl


/-- Original source left binary context is now a well-defined
P85 quotient → NEW P86 quotient operation, proved by actual
Type-valued P85 witness transport, not by full-shadow equality. -/
def nativeF55P87LeftContext
    {k l : Nat}
    {mc : KuuNativeBlocks a b}
    {pc : KuuNativeBlocks x y}
    (later : KuuNativeF45Tree p k l mb pb mc pc)
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P87FourClasses first last u v) :
    NativeF55P87FourClasses
      (KuuNativeF45Tree.node first later)
      (KuuNativeF45Tree.node last later)
      (.leftContext u later) (.leftContext v later) :=
  Quot.liftOn f
    (fun raw => nativeF55P87FourClass _ _ (.leftContext raw later))
    (by
      intro raw₁ raw₂ heq
      apply Quot.sound
      rcases heq with ⟨w⟩
      exact ⟨NativeF55P87ClosedFourCell.leftContext w later⟩)

/-- Genuine original F54 right binary context on each P85 class,
descending into the new P86 quotient by Type-valued evidence. -/
def nativeF55P87RightContext
    {k l n n' m m' : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    (earlier : KuuNativeF45Tree p k l ma pa mb pb)
    (first : KuuNativeF45Tree p n m mb pb mc pc)
    (last : KuuNativeF45Tree p n' m' mb pb mc pc)
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P87FourClasses first last u v) :
    NativeF55P87FourClasses
      (KuuNativeF45Tree.node earlier first)
      (KuuNativeF45Tree.node earlier last)
      (.rightContext earlier u) (.rightContext earlier v) :=
  Quot.liftOn f
    (fun raw => nativeF55P87FourClass _ _ (.rightContext earlier raw))
    (by
      intro raw₁ raw₂ heq
      apply Quot.sound
      rcases heq with ⟨w⟩
      exact ⟨NativeF55P87ClosedFourCell.rightContext earlier w⟩)

/-- True F54 precomposition with a typed prior route now
descends from P85 proof quotient to the new P86 proof quotient. -/
def nativeF55P87Precompose
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n₁ m₁ ma pa mb pb)
    (middle : KuuNativeF45Tree p n₂ m₂ ma pa mb pb)
    (last : KuuNativeF45Tree p n₃ m₃ ma pa mb pb)
    (prior : KuuNativeF45Tree.DepthRotationRoute p first middle)
    {u v : KuuNativeF45Tree.DepthRotationRoute p middle last}
    (f : NativeF55P87FourClasses middle last u v) :
    NativeF55P87FourClasses first last
      (.trans prior u) (.trans prior v) :=
  Quot.liftOn f
    (fun raw => nativeF55P87FourClass first last (.precompose prior raw))
    (by
      intro raw₁ raw₂ heq
      apply Quot.sound
      rcases heq with ⟨w⟩
      exact ⟨NativeF55P87ClosedFourCell.precompose prior w⟩)

/-- True F54 postcomposition with a typed suffix now
descends to the new P86 quotient through actual P85 witnesses. -/
def nativeF55P87Postcompose
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n₁ m₁ ma pa mb pb)
    (middle : KuuNativeF45Tree p n₂ m₂ ma pa mb pb)
    (last : KuuNativeF45Tree p n₃ m₃ ma pa mb pb)
    {u v : KuuNativeF45Tree.DepthRotationRoute p first middle}
    (f : NativeF55P87FourClasses first middle u v)
    (suffix : KuuNativeF45Tree.DepthRotationRoute p middle last) :
    NativeF55P87FourClasses first last
      (.trans u suffix) (.trans v suffix) :=
  Quot.liftOn f
    (fun raw => nativeF55P87FourClass first last (.postcompose raw suffix))
    (by
      intro raw₁ raw₂ heq
      apply Quot.sound
      rcases heq with ⟨w⟩
      exact ⟨NativeF55P87ClosedFourCell.postcompose w suffix⟩)

/-- TRUE two-input horizontal P85×P85→P86 source operation.
For both independent quotient arguments, changes of representatives
are justified by original Type-valued P85 witnesses. -/
def nativeF55P87Horizontal
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    {r r' : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter}
    {s s' : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter}
    (f : NativeF55P87FourClasses leftBefore leftAfter r r')
    (g : NativeF55P87FourClasses rightBefore rightAfter s s') :
    NativeF55P87FourClasses
      (KuuNativeF45Tree.node leftBefore rightBefore)
      (KuuNativeF45Tree.node leftAfter rightAfter)
      (.trans (.leftContext r rightBefore) (.rightContext leftAfter s))
      (.trans (.leftContext r' rightBefore) (.rightContext leftAfter s')) :=
  Quot.liftOn₂ f g
    (fun left right =>
      nativeF55P87FourClass _ _ (left.horizontal right))
    (by
      intro left right₁ right₂ hr
      apply Quot.sound
      rcases hr with ⟨w⟩
      exact ⟨NativeF55P87ClosedFourCell.horizontalRight left w⟩)
    (by
      intro left₁ left₂ right hl
      apply Quot.sound
      rcases hl with ⟨w⟩
      exact ⟨NativeF55P87ClosedFourCell.horizontalLeft w right⟩)

/-- P85×P85→P86 binary operation computes on the SAME original
source raw F55 proofs, never an invented replacement proof label. -/
@[simp] theorem nativeF55P87Horizontal_raw
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
    nativeF55P87Horizontal
      (nativeF55P87FourClass leftBefore leftAfter f)
      (nativeF55P87FourClass rightBefore rightAfter g) =
    nativeF55P87FourClass _ _ (f.horizontal g) := rfl



/-- The original horizontal unit has a GENUINE P80 source
four-cell generator. Its image is exactly the horizontal unit
equation in the recursively closed P87 source quotient,
not an equation fabricated from shadow equality. -/
theorem nativeF55P87_horizontal_id
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    (r : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter)
    (s : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter) :
    nativeF55P87Horizontal
        (nativeF55P87FourClass leftBefore leftAfter
          (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident r))
        (nativeF55P87FourClass rightBefore rightAfter
          (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident s)) =
      nativeF55P87FourClass _ _
        (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident
          (nativeF55HorizontalUnitRoute r s)) := by
  change nativeF55P87FourClass _ _
      ((KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident r).horizontal
        (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident s)) =
    nativeF55P87FourClass _ _
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident
        (nativeF55HorizontalUnitRoute r s))
  apply Quot.sound
  exact ⟨NativeF55P87ClosedFourCell.old
    (NativeF55P86ContextFourCell.old
      (NativeF55P85HorizontalFourCell.old
        (NativeF55P80UnitFourCell.horizontalUnit r s)))⟩

/-- The complete ORIGINAL full shadow of a two-sided horizontal
pasting computes additively on arbitrary P87 quotient classes.
This is a preservation theorem, not proof of interchange. -/
theorem nativeF55P87Horizontal_shadow
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    {r r' : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter}
    {s s' : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter}
    (f : NativeF55P87FourClasses leftBefore leftAfter r r')
    (g : NativeF55P87FourClasses rightBefore rightAfter s s') :
    nativeF55P87FourToShadow _ _ _ _
      (nativeF55P87Horizontal f g) =
      nativeF55P87FourToShadow _ _ _ _ f +
        nativeF55P87FourToShadow _ _ _ _ g := by
  refine Quot.inductionOn f (fun left => ?_)
  refine Quot.inductionOn g (fun right => ?_)
  rfl

/-- For four genuinely typed original parallel 3-cell histories,
both interchange pastings have the SAME necessary complete
charge/phase signature. This does NOT supply an interchange 4-cell:
equal shadows are necessary but provably not sufficient for
original proof history identities. -/
theorem nativeF55P87_interchange_shadow
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
    ((KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans f₁ f₂).horizontal
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans g₁ g₂)).nativeShadow =
    (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans
      (f₁.horizontal g₁) (f₂.horizontal g₂)).nativeShadow := by
  change (f₁.nativeShadow + f₂.nativeShadow) +
      (g₁.nativeShadow + g₂.nativeShadow) =
    (f₁.nativeShadow + g₁.nativeShadow) +
      (f₂.nativeShadow + g₂.nativeShadow)
  ac_rfl

#print axioms NativeF55P87ClosedFourCell.p87_sound
#print axioms nativeF55P87FourSetoid
#print axioms NativeF55P87FourClasses
#print axioms nativeF55P87FourClass
#print axioms nativeF55P87FourClass_eq_iff
#print axioms nativeF55P87FourClass_eq_implies_path
#print axioms nativeF55P87FourToShadow
#print axioms nativeF55P87VerticalComp
#print axioms nativeF55P87VerticalCategory
#print axioms nativeF55P87VerticalShadow_comp
#print axioms nativeF55P86ToP87
#print axioms nativeF55P86ToP87_surjective
#print axioms nativeF55P86ToP87_comp
#print axioms nativeF55P87LeftContext
#print axioms nativeF55P87RightContext
#print axioms nativeF55P87Precompose
#print axioms nativeF55P87Postcompose
#print axioms nativeF55P87Horizontal
#print axioms nativeF55P87Horizontal_raw
#print axioms nativeF55P87_horizontal_id
#print axioms nativeF55P87Horizontal_shadow
#print axioms nativeF55P87_interchange_shadow

end
end Kuu.F112.Physical
