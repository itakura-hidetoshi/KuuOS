import KUOS.DependentOriginationGrayC60OriginalFaceHorizontalThreeHomV5_199

namespace KUOS.DependentOriginationGrayC60OriginalFaceHorizontalCompositionV5_199

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60CyclicGlobalPastingV5_156
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationGrayC60PresentedInterchangerV5_191
open KUOS.DependentOriginationGrayC60ThreeHomCategoriesV5_192
open KUOS.DependentOriginationGrayC60GradedGrayThreeCategoryV5_197
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalPresentationV5_199
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalThreeHomV5_199

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.199 / F59-F51-C — genuine original-source 3-Hom composition functors

F51-A adjoined new correctly globular 3-source constructors for
horizontal and 2-context vertical composition, precisely because
the ORIGINAL F43 raw presentation did not supply them.
F51-B constructed their proof-relevant F42-object local 3-Hom
category through the full Int×Int-plus-ZMod2 target kernel.

Now the ORIGINAL C60 2-cell horizontal operation is promoted to a
genuine MATHLIB FUNCTOR from a product of TWO local 3-Hom
categories into the 3-Hom above the *actual composed C60 1-paths*.
Separately, original vertical composition of 2-cells defines
another genuine Mathlib product 3-Hom functor. In both cases
composition, identities and the complete full-native Gray
evaluation are proved coherent, without identifying distinct
raw original F42 face 2-cell syntax.

The two real original C60 1-path whiskerings also become genuine
functors, preserving the complete original-source higher arrows.
The original F43 source inclusion remains distinct from these
ADJOINED horizontal/vertical 3-source operations.
-/

/-! ## I. Horizontal original-F42 2-cell 3-Hom bifunctor -/

/-- Real source horizontal 3-arrow between the actual F42
left-first horizontal pasting of two pairs of original 2-cells. -/
def c60F51HorizontalMap
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    {X X' : C60F51OriginalTwo p q}
    {Y Y' : C60F51OriginalTwo r s}
    (f : X ⟶ X') (g : Y ⟶ Y') :
    c60F51OriginalTwoHorizontal X Y ⟶
      c60F51OriginalTwoHorizontal X' Y' :=
  Quot.liftOn₂ f g
    (fun rf rg => c60F51Of (.horizontal rf rg))
    (by
      intro rf rg₁ rg₂ heq
      apply Quot.sound
      change rf.toNative + rg₁.toNative =
        rf.toNative + rg₂.toNative
      rw [heq])
    (by
      intro rf₁ rf₂ rg heq
      apply Quot.sound
      change rf₁.toNative + rg.toNative =
        rf₂.toNative + rg.toNative
      rw [heq])

theorem c60F51HorizontalMap_eval
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    {X X' : C60F51OriginalTwo p q}
    {Y Y' : C60F51OriginalTwo r s}
    (f : X ⟶ X') (g : Y ⟶ Y') :
    c60F51Eval (c60F51HorizontalMap f g) =
      c60F51Eval f + c60F51Eval g := by
  refine Quot.inductionOn f (fun rf => ?_)
  refine Quot.inductionOn g (fun rg => ?_)
  rfl

/-- A true ORIGINAL C60 horizontal 2-cell Mathlib FUNCTOR
acting on genuinely typed original F42 proof witnesses
and new F51 3-morphism words. This is not the grade-only F49
tensor functor: its source and target are original proof terms. -/
def c60F51HorizontalThreeHomFunctor
    {a b c : IcosahedralDart}
    (p q : Quiver.Path a b) (r s : Quiver.Path b c) :
    (C60F51OriginalTwo p q × C60F51OriginalTwo r s) ⥤
      C60F51OriginalTwo (p.comp r) (q.comp s) where
  obj z := c60F51OriginalTwoHorizontal z.1 z.2
  map := fun {_ _} f => c60F51HorizontalMap f.1 f.2
  map_id := by
    intro ⟨X, Y⟩
    apply Quot.sound
    change (0 : GradedThreeCell 0 0) + 0 = 0
    exact add_zero _
  map_comp := by
    intro ⟨X, Y⟩ ⟨X', Y'⟩ ⟨X'', Y''⟩ f g
    obtain ⟨f₁, f₂⟩ := f
    obtain ⟨g₁, g₂⟩ := g
    refine Quot.inductionOn f₁ (fun rf₁ => ?_)
    refine Quot.inductionOn f₂ (fun rf₂ => ?_)
    refine Quot.inductionOn g₁ (fun rg₁ => ?_)
    refine Quot.inductionOn g₂ (fun rg₂ => ?_)
    apply Quot.sound
    change (rf₁.toNative + rg₁.toNative) +
        (rf₂.toNative + rg₂.toNative) =
      (rf₁.toNative + rf₂.toNative) +
        (rg₁.toNative + rg₂.toNative)
    abel

/-! ## II. Vertical original-F42 2-cell 3-Hom bifunctor -/

/-- Vertical original 2-context comp of two genuinely
original-source F51 3-cell arrows, preserving the raw F42
source and target face 2-cells separately. -/
def c60F51VerticalTwoMap
    {a b : IcosahedralDart}
    {p q r : Quiver.Path a b}
    {X X' : C60F51OriginalTwo p q}
    {Y Y' : C60F51OriginalTwo q r}
    (f : X ⟶ X') (g : Y ⟶ Y') :
    c60F51OriginalTwoVertical X Y ⟶
      c60F51OriginalTwoVertical X' Y' :=
  Quot.liftOn₂ f g
    (fun rf rg => c60F51Of (.vertical rf rg))
    (by
      intro rf rg₁ rg₂ heq
      apply Quot.sound
      change rf.toNative + rg₁.toNative =
        rf.toNative + rg₂.toNative
      rw [heq])
    (by
      intro rf₁ rf₂ rg heq
      apply Quot.sound
      change rf₁.toNative + rg.toNative =
        rf₂.toNative + rg.toNative
      rw [heq])

theorem c60F51VerticalTwoMap_eval
    {a b : IcosahedralDart}
    {p q r : Quiver.Path a b}
    {X X' : C60F51OriginalTwo p q}
    {Y Y' : C60F51OriginalTwo q r}
    (f : X ⟶ X') (g : Y ⟶ Y') :
    c60F51Eval (c60F51VerticalTwoMap f g) =
      c60F51Eval f + c60F51Eval g := by
  refine Quot.inductionOn f (fun rf => ?_)
  refine Quot.inductionOn g (fun rg => ?_)
  rfl

/-- Every ACTUAL composable triple of original C60 1-paths
has a vertical original-F42 2-cell composition Mathlib
FUNCTOR on full original proof-relevant 3-Homs. -/
def c60F51VerticalTwoThreeHomFunctor
    {a b : IcosahedralDart}
    (p q r : Quiver.Path a b) :
    (C60F51OriginalTwo p q × C60F51OriginalTwo q r) ⥤
      C60F51OriginalTwo p r where
  obj z := c60F51OriginalTwoVertical z.1 z.2
  map := fun {_ _} f => c60F51VerticalTwoMap f.1 f.2
  map_id := by
    intro ⟨X, Y⟩
    apply Quot.sound
    change (0 : GradedThreeCell 0 0) + 0 = 0
    exact add_zero _
  map_comp := by
    intro ⟨X, Y⟩ ⟨X', Y'⟩ ⟨X'', Y''⟩ f g
    obtain ⟨f₁, f₂⟩ := f
    obtain ⟨g₁, g₂⟩ := g
    refine Quot.inductionOn f₁ (fun rf₁ => ?_)
    refine Quot.inductionOn f₂ (fun rf₂ => ?_)
    refine Quot.inductionOn g₁ (fun rg₁ => ?_)
    refine Quot.inductionOn g₂ (fun rg₂ => ?_)
    apply Quot.sound
    change (rf₁.toNative + rg₁.toNative) +
        (rf₂.toNative + rg₂.toNative) =
      (rf₁.toNative + rf₂.toNative) +
        (rg₁.toNative + rg₂.toNative)
    abel

/-! ## III. Original real C60 1-path whiskering functors -/

/-- Genuine original C60 prior path acts on complete F51
source 2-cell objects AND all native 3-cell constructors. -/
def c60F51LeftWhiskerFunctor
    {a b c : IcosahedralDart}
    (prior : Quiver.Path a b)
    {p q : Quiver.Path b c} :
    C60F51OriginalTwo p q ⥤
      C60F51OriginalTwo (prior.comp p) (prior.comp q) where
  obj X := ⟨.whiskerLeft prior X.original⟩
  map := fun {_ _} f =>
    Quot.liftOn f
      (fun raw => c60F51Of (.whiskerLeft prior raw))
      (by
        intro f g h
        apply Quot.sound
        exact h)
  map_id := by
    intro X
    apply Quot.sound
    rfl
  map_comp := by
    intro X Y Z f g
    refine Quot.inductionOn f (fun f => ?_)
    refine Quot.inductionOn g (fun g => ?_)
    apply Quot.sound
    rfl

def c60F51RightWhiskerFunctor
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b}
    (suffix : Quiver.Path b c) :
    C60F51OriginalTwo p q ⥤
      C60F51OriginalTwo (p.comp suffix) (q.comp suffix) where
  obj X := ⟨.whiskerRight X.original suffix⟩
  map := fun {_ _} f =>
    Quot.liftOn f
      (fun raw => c60F51Of (.whiskerRight raw suffix))
      (by
        intro f g h
        apply Quot.sound
        exact h)
  map_id := by
    intro X
    apply Quot.sound
    rfl
  map_comp := by
    intro X Y Z f g
    refine Quot.inductionOn f (fun f => ?_)
    refine Quot.inductionOn g (fun g => ?_)
    apply Quot.sound
    rfl

theorem c60F51LeftWhisker_eval
    {a b c : IcosahedralDart}
    (prior : Quiver.Path a b)
    {p q : Quiver.Path b c}
    {X Y : C60F51OriginalTwo p q}
    (f : X ⟶ Y) :
    c60F51Eval ((c60F51LeftWhiskerFunctor prior).map f) =
      c60F51Eval f := by
  refine Quot.inductionOn f (fun raw => ?_)
  rfl

theorem c60F51RightWhisker_eval
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b}
    (suffix : Quiver.Path b c)
    {X Y : C60F51OriginalTwo p q}
    (f : X ⟶ Y) :
    c60F51Eval ((c60F51RightWhiskerFunctor suffix).map f) =
      c60F51Eval f := by
  refine Quot.inductionOn f (fun raw => ?_)
  rfl

theorem c60F51LeftWhisker_faithful
    {a b c : IcosahedralDart}
    (prior : Quiver.Path a b)
    {p q : Quiver.Path b c}
    {X Y : C60F51OriginalTwo p q}
    {f g : X ⟶ Y}
    (h : (c60F51LeftWhiskerFunctor prior).map f =
      (c60F51LeftWhiskerFunctor prior).map g) :
    f = g := by
  have hh :
      c60F51Eval ((c60F51LeftWhiskerFunctor prior).map f) =
      c60F51Eval ((c60F51LeftWhiskerFunctor prior).map g) :=
    congrArg (fun z => c60F51Eval z) h
  rw [c60F51LeftWhisker_eval, c60F51LeftWhisker_eval] at hh
  exact c60F51GrayFunctor_faithful _ _ (by
    apply GradedThreeCell.ext
    · change (c60F51Eval f).charge = (c60F51Eval g).charge
      exact congrArg GradedThreeCell.charge hh
    · change (c60F51Eval f).phase = (c60F51Eval g).phase
      exact congrArg GradedThreeCell.phase hh)

theorem c60F51RightWhisker_faithful
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b}
    (suffix : Quiver.Path b c)
    {X Y : C60F51OriginalTwo p q}
    {f g : X ⟶ Y}
    (h : (c60F51RightWhiskerFunctor suffix).map f =
      (c60F51RightWhiskerFunctor suffix).map g) :
    f = g := by
  have hh :
      c60F51Eval ((c60F51RightWhiskerFunctor suffix).map f) =
      c60F51Eval ((c60F51RightWhiskerFunctor suffix).map g) :=
    congrArg (fun z => c60F51Eval z) h
  rw [c60F51RightWhisker_eval, c60F51RightWhisker_eval] at hh
  exact c60F51GrayFunctor_faithful _ _ (by
    apply GradedThreeCell.ext
    · change (c60F51Eval f).charge = (c60F51Eval g).charge
      exact congrArg GradedThreeCell.charge hh
    · change (c60F51Eval f).phase = (c60F51Eval g).phase
      exact congrArg GradedThreeCell.phase hh)

#print axioms c60F51HorizontalThreeHomFunctor
#print axioms c60F51HorizontalMap_eval
#print axioms c60F51VerticalTwoThreeHomFunctor
#print axioms c60F51VerticalTwoMap_eval
#print axioms c60F51LeftWhiskerFunctor
#print axioms c60F51RightWhiskerFunctor
#print axioms c60F51LeftWhisker_faithful
#print axioms c60F51RightWhisker_faithful

end
end KUOS.DependentOriginationGrayC60OriginalFaceHorizontalCompositionV5_199
