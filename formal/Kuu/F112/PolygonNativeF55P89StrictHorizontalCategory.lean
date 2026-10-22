import Kuu.F112.PolygonNativeF55P89InterchangeFourCell

/-!
# F112-P89B — exact strict interchange in a distinct genuine 4-cell quotient

P89A extends original P87 Type-valued source 4-cell presentation by
a new explicitly typed F55 interchange generator; P88 proves that
the OLD P87 presentation cannot identify nonunit-middle histories.

P89B constructs a real local strict vertical Mathlib Category,
a self-contained well-defined original horizontal binary operation,
and proves strict interchange on arbitrary FOUR P89 quotient classes.
Old P87 and P88 mathematics remain untouched. The original full
integer charge and odd square phase are preserved.

Local globular strict 3-category, all horizontal associativity,
F54 route-object comparison and full higher coherence are not
automatically established by this theorem.
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

def nativeF55P89VerticalComp
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {u v w : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P89FourClasses first last u v)
    (g : NativeF55P89FourClasses first last v w) :
    NativeF55P89FourClasses first last u w :=
  Quot.liftOn₂ f g
    (fun left right =>
      nativeF55P89FourClass first last (.trans left right))
    (by
      intro left right₁ right₂ hr
      apply Quot.sound
      rcases hr with ⟨witness⟩
      exact ⟨NativeF55P89InterchangeFourCell.leftWhisker left witness⟩)
    (by
      intro left₁ left₂ right hl
      apply Quot.sound
      rcases hl with ⟨witness⟩
      exact ⟨NativeF55P89InterchangeFourCell.rightWhisker witness right⟩)

/-- Genuine strict LOCAL vertical Mathlib Category on the old
F54 route objects and the new proof-relevant P86 four-cell quotient. -/
@[reducible] def nativeF55P89VerticalCategory
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    Category (KuuNativeF45Tree.DepthRotationRoute p first last) where
  Hom := NativeF55P89FourClasses first last
  id route := nativeF55P89FourClass first last (.ident route)
  comp f g := nativeF55P89VerticalComp first last f g
  id_comp := by
    intro X Y f
    refine Quot.inductionOn f (fun raw => ?_)
    change nativeF55P89FourClass first last (.trans (.ident X) raw) =
      nativeF55P89FourClass first last raw
    exact Quot.sound ⟨NativeF55P89InterchangeFourCell.old
      (NativeF55P87ClosedFourCell.old
      (NativeF55P86ContextFourCell.old
        (NativeF55P85HorizontalFourCell.old
        (NativeF55P80UnitFourCell.old
          (NativeF55RawVerticalFourCell.leftUnit raw)))))⟩
  comp_id := by
    intro X Y f
    refine Quot.inductionOn f (fun raw => ?_)
    change nativeF55P89FourClass first last (.trans raw (.ident Y)) =
      nativeF55P89FourClass first last raw
    exact Quot.sound ⟨NativeF55P89InterchangeFourCell.old
      (NativeF55P87ClosedFourCell.old
      (NativeF55P86ContextFourCell.old
        (NativeF55P85HorizontalFourCell.old
        (NativeF55P80UnitFourCell.old
          (NativeF55RawVerticalFourCell.rightUnit raw)))))⟩
  assoc := by
    intro W X Y Z f g h
    refine Quot.inductionOn f (fun a => ?_)
    refine Quot.inductionOn g (fun b => ?_)
    refine Quot.inductionOn h (fun c => ?_)
    change nativeF55P89FourClass first last
      (.trans (.trans a b) c) =
      nativeF55P89FourClass first last
        (.trans a (.trans b c))
    exact Quot.sound ⟨NativeF55P89InterchangeFourCell.old
      (NativeF55P87ClosedFourCell.old
      (NativeF55P86ContextFourCell.old
        (NativeF55P85HorizontalFourCell.old
        (NativeF55P80UnitFourCell.old
          (NativeF55RawVerticalFourCell.assoc a b c)))))⟩

/-- Vertical original full F55 shadow remains additive on
P86's chosen proof-relevant strict local vertical category. -/
theorem nativeF55P89VerticalShadow_comp
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {u v w : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P89FourClasses first last u v)
    (g : NativeF55P89FourClasses first last v w) :
    nativeF55P89FourToShadow first last u w
      (nativeF55P89VerticalComp first last f g) =
        nativeF55P89FourToShadow first last u v f +
          nativeF55P89FourToShadow first last v w g := by
  refine Quot.inductionOn f (fun left => ?_)
  refine Quot.inductionOn g (fun right => ?_)
  rfl


def nativeF55P89LeftContext
    {k l : Nat}
    {mc : KuuNativeBlocks a b}
    {pc : KuuNativeBlocks x y}
    (later : KuuNativeF45Tree p k l mb pb mc pc)
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P89FourClasses first last u v) :
    NativeF55P89FourClasses
      (KuuNativeF45Tree.node first later)
      (KuuNativeF45Tree.node last later)
      (.leftContext u later) (.leftContext v later) :=
  Quot.liftOn f
    (fun raw => nativeF55P89FourClass _ _ (.leftContext raw later))
    (by
      intro raw₁ raw₂ heq
      apply Quot.sound
      rcases heq with ⟨w⟩
      exact ⟨NativeF55P89InterchangeFourCell.leftContext w later⟩)

/-- Genuine original F54 right binary context on each P85 class,
descending into the new P86 quotient by Type-valued evidence. -/
def nativeF55P89RightContext
    {k l n n' m m' : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    (earlier : KuuNativeF45Tree p k l ma pa mb pb)
    (first : KuuNativeF45Tree p n m mb pb mc pc)
    (last : KuuNativeF45Tree p n' m' mb pb mc pc)
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P89FourClasses first last u v) :
    NativeF55P89FourClasses
      (KuuNativeF45Tree.node earlier first)
      (KuuNativeF45Tree.node earlier last)
      (.rightContext earlier u) (.rightContext earlier v) :=
  Quot.liftOn f
    (fun raw => nativeF55P89FourClass _ _ (.rightContext earlier raw))
    (by
      intro raw₁ raw₂ heq
      apply Quot.sound
      rcases heq with ⟨w⟩
      exact ⟨NativeF55P89InterchangeFourCell.rightContext earlier w⟩)

/-- True F54 precomposition with a typed prior route now
descends from P85 proof quotient to the new P86 proof quotient. -/
def nativeF55P89Precompose
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n₁ m₁ ma pa mb pb)
    (middle : KuuNativeF45Tree p n₂ m₂ ma pa mb pb)
    (last : KuuNativeF45Tree p n₃ m₃ ma pa mb pb)
    (prior : KuuNativeF45Tree.DepthRotationRoute p first middle)
    {u v : KuuNativeF45Tree.DepthRotationRoute p middle last}
    (f : NativeF55P89FourClasses middle last u v) :
    NativeF55P89FourClasses first last
      (.trans prior u) (.trans prior v) :=
  Quot.liftOn f
    (fun raw => nativeF55P89FourClass first last (.precompose prior raw))
    (by
      intro raw₁ raw₂ heq
      apply Quot.sound
      rcases heq with ⟨w⟩
      exact ⟨NativeF55P89InterchangeFourCell.precompose prior w⟩)

/-- True F54 postcomposition with a typed suffix now
descends to the new P86 quotient through actual P85 witnesses. -/
def nativeF55P89Postcompose
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n₁ m₁ ma pa mb pb)
    (middle : KuuNativeF45Tree p n₂ m₂ ma pa mb pb)
    (last : KuuNativeF45Tree p n₃ m₃ ma pa mb pb)
    {u v : KuuNativeF45Tree.DepthRotationRoute p first middle}
    (f : NativeF55P89FourClasses first middle u v)
    (suffix : KuuNativeF45Tree.DepthRotationRoute p middle last) :
    NativeF55P89FourClasses first last
      (.trans u suffix) (.trans v suffix) :=
  Quot.liftOn f
    (fun raw => nativeF55P89FourClass first last (.postcompose raw suffix))
    (by
      intro raw₁ raw₂ heq
      apply Quot.sound
      rcases heq with ⟨w⟩
      exact ⟨NativeF55P89InterchangeFourCell.postcompose w suffix⟩)

/-- TRUE two-input horizontal P85×P85→P86 source operation.
For both independent quotient arguments, changes of representatives
are justified by original Type-valued P85 witnesses. -/
def nativeF55P89Horizontal
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    {r r' : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter}
    {s s' : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter}
    (f : NativeF55P89FourClasses leftBefore leftAfter r r')
    (g : NativeF55P89FourClasses rightBefore rightAfter s s') :
    NativeF55P89FourClasses
      (KuuNativeF45Tree.node leftBefore rightBefore)
      (KuuNativeF45Tree.node leftAfter rightAfter)
      (.trans (.leftContext r rightBefore) (.rightContext leftAfter s))
      (.trans (.leftContext r' rightBefore) (.rightContext leftAfter s')) :=
  Quot.liftOn₂ f g
    (fun left right =>
      nativeF55P89FourClass _ _ (left.horizontal right))
    (by
      intro left right₁ right₂ hr
      apply Quot.sound
      rcases hr with ⟨w⟩
      exact ⟨NativeF55P89InterchangeFourCell.horizontalRight left w⟩)
    (by
      intro left₁ left₂ right hl
      apply Quot.sound
      rcases hl with ⟨w⟩
      exact ⟨NativeF55P89InterchangeFourCell.horizontalLeft w right⟩)

/-- P85×P85→P86 binary operation computes on the SAME original
source raw F55 proofs, never an invented replacement proof label. -/
@[simp] theorem nativeF55P89Horizontal_raw
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
    nativeF55P89Horizontal
      (nativeF55P89FourClass leftBefore leftAfter f)
      (nativeF55P89FourClass rightBefore rightAfter g) =
    nativeF55P89FourClass _ _ (f.horizontal g) := rfl



/-- The original horizontal unit has a GENUINE P80 source
four-cell generator. Its image is exactly the horizontal unit
equation in the recursively closed P87 source quotient,
not an equation fabricated from shadow equality. -/
theorem nativeF55P89_horizontal_id
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    (r : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter)
    (s : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter) :
    nativeF55P89Horizontal
        (nativeF55P89FourClass leftBefore leftAfter
          (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident r))
        (nativeF55P89FourClass rightBefore rightAfter
          (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident s)) =
      nativeF55P89FourClass _ _
        (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident
          (nativeF55HorizontalUnitRoute r s)) := by
  change nativeF55P89FourClass _ _
      ((KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident r).horizontal
        (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident s)) =
    nativeF55P89FourClass _ _
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident
        (nativeF55HorizontalUnitRoute r s))
  apply Quot.sound
  exact ⟨NativeF55P89InterchangeFourCell.old
      (NativeF55P87ClosedFourCell.old
    (NativeF55P86ContextFourCell.old
      (NativeF55P85HorizontalFourCell.old
        (NativeF55P80UnitFourCell.horizontalUnit r s))))⟩

/-- The complete ORIGINAL full shadow of a two-sided horizontal
pasting computes additively on arbitrary P87 quotient classes.
This is a preservation theorem, not proof of interchange. -/
theorem nativeF55P89Horizontal_shadow
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    {r r' : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter}
    {s s' : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter}
    (f : NativeF55P89FourClasses leftBefore leftAfter r r')
    (g : NativeF55P89FourClasses rightBefore rightAfter s s') :
    nativeF55P89FourToShadow _ _ _ _
      (nativeF55P89Horizontal f g) =
      nativeF55P89FourToShadow _ _ _ _ f +
        nativeF55P89FourToShadow _ _ _ _ g := by
  refine Quot.inductionOn f (fun left => ?_)
  refine Quot.inductionOn g (fun right => ?_)
  rfl

/-- Strict interchange for FOUR ARBITRARY typed P89 quotient classes:
horizontal preserves vertical pasting as equality in the SAME P89
quotient. This is the strict bifunctoriality part of the local
higher structure, not yet the entire globular strict 3-category. -/
theorem nativeF55P89_interchange
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    {u₀ u₁ u₂ : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter}
    {v₀ v₁ v₂ : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter}
    (f₁ : NativeF55P89FourClasses leftBefore leftAfter u₀ u₁)
    (f₂ : NativeF55P89FourClasses leftBefore leftAfter u₁ u₂)
    (g₁ : NativeF55P89FourClasses rightBefore rightAfter v₀ v₁)
    (g₂ : NativeF55P89FourClasses rightBefore rightAfter v₁ v₂) :
    nativeF55P89Horizontal
      (nativeF55P89VerticalComp leftBefore leftAfter f₁ f₂)
      (nativeF55P89VerticalComp rightBefore rightAfter g₁ g₂) =
    nativeF55P89VerticalComp
      (KuuNativeF45Tree.node leftBefore rightBefore)
      (KuuNativeF45Tree.node leftAfter rightAfter)
      (nativeF55P89Horizontal f₁ g₁)
      (nativeF55P89Horizontal f₂ g₂) := by
  refine Quot.inductionOn f₁ (fun a => ?_)
  refine Quot.inductionOn f₂ (fun b => ?_)
  refine Quot.inductionOn g₁ (fun c => ?_)
  refine Quot.inductionOn g₂ (fun d => ?_)
  change nativeF55P89FourClass _ _
      ((KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans a b).horizontal
        (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans c d)) =
    nativeF55P89FourClass _ _
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans
        (a.horizontal c) (b.horizontal d))
  exact nativeF55P89_interchange_quotient_eq a b c d

/-- Witnessed information-loss comparison between the unchanged OLD
P87 quotient and new P89 quotient, under exactly the existing P88
nonempty-middle-factor hypotheses. The old no-go is preserved. -/
theorem nativeF55P89_strict_enlargement_of_nonempty
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
    (g₂ : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p v₁ v₂)
    (hf : f₂.p88InterchangeWord ≠ [])
    (hg : g₁.p88InterchangeWord ≠ []) :
    nativeF55P87FourClass
      (KuuNativeF45Tree.node leftBefore rightBefore)
      (KuuNativeF45Tree.node leftAfter rightAfter)
      ((KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans f₁ f₂).horizontal
        (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans g₁ g₂)) ≠
    nativeF55P87FourClass
      (KuuNativeF45Tree.node leftBefore rightBefore)
      (KuuNativeF45Tree.node leftAfter rightAfter)
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans
        (f₁.horizontal g₁) (f₂.horizontal g₂)) ∧
    nativeF55P89FourClass
      (KuuNativeF45Tree.node leftBefore rightBefore)
      (KuuNativeF45Tree.node leftAfter rightAfter)
      ((KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans f₁ f₂).horizontal
        (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans g₁ g₂)) =
    nativeF55P89FourClass
      (KuuNativeF45Tree.node leftBefore rightBefore)
      (KuuNativeF45Tree.node leftAfter rightAfter)
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans
        (f₁.horizontal g₁) (f₂.horizontal g₂)) := by
  exact ⟨nativeF55P88_interchange_quotient_ne f₁ f₂ g₁ g₂ hf hg,
    nativeF55P89_interchange_quotient_eq f₁ f₂ g₁ g₂⟩

#print axioms nativeF55P89VerticalComp
#print axioms nativeF55P89VerticalCategory
#print axioms nativeF55P89VerticalShadow_comp
#print axioms nativeF55P89LeftContext
#print axioms nativeF55P89RightContext
#print axioms nativeF55P89Precompose
#print axioms nativeF55P89Postcompose
#print axioms nativeF55P89Horizontal
#print axioms nativeF55P89Horizontal_raw
#print axioms nativeF55P89_horizontal_id
#print axioms nativeF55P89Horizontal_shadow
#print axioms nativeF55P89_interchange
#print axioms nativeF55P89_strict_enlargement_of_nonempty

end
end Kuu.F112.Physical
