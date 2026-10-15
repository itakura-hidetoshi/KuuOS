import KUOS.DependentOriginationGrayC60OriginalFaceAssociatorPresentationV5_200

namespace KUOS.DependentOriginationGrayC60OriginalFaceAssociatorThreeHomV5_200

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60CyclicGlobalPastingV5_156
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationGrayC60PresentedInterchangerV5_191
open KUOS.DependentOriginationGrayC60GradedGrayThreeCategoryV5_197
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalPresentationV5_199
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalThreeHomV5_199
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalCompositionV5_199
open KUOS.DependentOriginationGrayC60OriginalFaceAssociatorPresentationV5_200

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.200 / F59-F52-B: source F42 associator in a genuine Mathlib 3-Hom

The F52 category keeps the EXACT original F42 proof witnesses as
objects, and admits old F51/F43 cells plus specifically ADJOINED
source associators/unitors. Quotienting is ONLY between existing
parallel source 3-arrows with identical FULL native F59 values.
This never identifies distinct 2-cell proof terms, nor invents
an F43 or F55 source constructor that was not present originally.

The nontrivial original F43 Gray exchange remains a sourced
morphism through the faithful F51 inclusion. Associator and
unitor are zero-native but nontrivially TYPED as source comparisons.
-/

structure C60F52OriginalTwo {a b : IcosahedralDart}
    (p q : Quiver.Path a b) where
  original : C60F42PresentedFaceCell p q

variable {a b : IcosahedralDart}
variable {p q : Quiver.Path a b}

def c60F52NativeRel
    {α β : C60F42PresentedFaceCell p q}
    (f g : C60F52PresentedThreeCell α β) : Prop :=
  f.toNative = g.toNative

abbrev C60F52Hom
    (X Y : C60F52OriginalTwo p q) : Type :=
  Quot (c60F52NativeRel (α := X.original) (β := Y.original))

def c60F52Of
    {X Y : C60F52OriginalTwo p q}
    (f : C60F52PresentedThreeCell X.original Y.original) :
    C60F52Hom X Y := Quot.mk _ f

def c60F52Eval
    {X Y : C60F52OriginalTwo p q}
    (f : C60F52Hom X Y) : GradedThreeCell 0 0 :=
  Quot.liftOn f (fun raw => raw.toNative)
    (by intro f g heq; exact heq)

@[simp] theorem c60F52Eval_of
    {X Y : C60F52OriginalTwo p q}
    (f : C60F52PresentedThreeCell X.original Y.original) :
    c60F52Eval (c60F52Of f) = f.toNative := rfl

def c60F52Comp
    {X Y Z : C60F52OriginalTwo p q}
    (f : C60F52Hom X Y) (g : C60F52Hom Y Z) :
    C60F52Hom X Z :=
  Quot.liftOn₂ f g
    (fun x y => c60F52Of (.trans x y))
    (by
      intro x y₁ y₂ heq
      apply Quot.sound
      change x.toNative + y₁.toNative =
        x.toNative + y₂.toNative
      rw [heq])
    (by
      intro x₁ x₂ y heq
      apply Quot.sound
      change x₁.toNative + y.toNative =
        x₂.toNative + y.toNative
      rw [heq])

theorem c60F52Eval_comp
    {X Y Z : C60F52OriginalTwo p q}
    (f : C60F52Hom X Y) (g : C60F52Hom Y Z) :
    c60F52Eval (c60F52Comp f g) =
      c60F52Eval f + c60F52Eval g := by
  refine Quot.inductionOn f (fun f => ?_)
  refine Quot.inductionOn g (fun g => ?_)
  rfl

instance c60F52ThreeCategory : Category (C60F52OriginalTwo p q) where
  Hom := C60F52Hom
  id X := c60F52Of (.ident X.original)
  comp := c60F52Comp
  id_comp := by
    intro X Y f
    refine Quot.inductionOn f (fun raw => ?_)
    apply Quot.sound
    change (0 : GradedThreeCell 0 0) + raw.toNative = raw.toNative
    exact zero_add _
  comp_id := by
    intro X Y f
    refine Quot.inductionOn f (fun raw => ?_)
    apply Quot.sound
    change raw.toNative + (0 : GradedThreeCell 0 0) = raw.toNative
    exact add_zero _
  assoc := by
    intro W X Y Z f g h
    refine Quot.inductionOn f (fun f => ?_)
    refine Quot.inductionOn g (fun g => ?_)
    refine Quot.inductionOn h (fun h => ?_)
    apply Quot.sound
    change (f.toNative + g.toNative) + h.toNative =
      f.toNative + (g.toNative + h.toNative)
    exact add_assoc _ _ _

theorem c60F52Hom_ext
    {X Y : C60F52OriginalTwo p q}
    {f g : X ⟶ Y}
    (heq : c60F52Eval f = c60F52Eval g) : f = g := by
  revert heq
  refine Quot.inductionOn f (fun f => ?_)
  refine Quot.inductionOn g (fun g h => ?_)
  apply Quot.sound
  exact h

@[simp] theorem c60F52Eval_id
    (X : C60F52OriginalTwo p q) :
    c60F52Eval (𝟙 X) = (0 : GradedThreeCell 0 0) := rfl

theorem c60F52Hom_degreeEq
    {X Y : C60F52OriginalTwo p q}
    (f : X ⟶ Y) :
    c60F43FaceDegree X.original =
      c60F43FaceDegree Y.original := by
  refine Quot.inductionOn f (fun raw => ?_)
  exact raw.preservesFaceDegree

/-- Typed original F42 source into the genuine graded Gray target.
The full native Int×Int and independent exchange phase are kept. -/
def c60F52Lift
    {X Y : C60F52OriginalTwo p q} (f : X ⟶ Y) :
    C60F49Three
      (c60F49OriginalFaceTwo X.original)
      (c60F49OriginalFaceTwo Y.original) :=
  ⟨c60F52Hom_degreeEq f,
    (c60F52Eval f).charge, (c60F52Eval f).phase⟩

def c60F52GrayFunctor (p q : Quiver.Path a b) :
    C60F52OriginalTwo p q ⥤ C60F49Two p q where
  obj X := c60F49OriginalFaceTwo X.original
  map := fun {_ _} f => c60F52Lift f
  map_id := by
    intro X
    apply GradedThreeCell.ext <;> rfl
  map_comp := by
    intro X Y Z f g
    apply GradedThreeCell.ext
    · change (c60F52Eval (c60F52Comp f g)).charge =
        (c60F52Eval f).charge + (c60F52Eval g).charge
      rw [c60F52Eval_comp]
      exact grayNeutral_add_charge _ _
    · change (c60F52Eval (c60F52Comp f g)).phase =
        (c60F52Eval f).phase + (c60F52Eval g).phase
      rw [c60F52Eval_comp]
      exact grayNeutral_add_phase _ _

/-- Faithful embedding of every old F51/F43 cell in the
NEW F52 category; no old source generator is redefined. -/
def c60F52Inclusion (p q : Quiver.Path a b) :
    C60F51OriginalTwo p q ⥤ C60F52OriginalTwo p q where
  obj X := ⟨X.original⟩
  map := fun {X Y} f =>
    Quot.liftOn f
      (fun raw => c60F52Of
        (X := ⟨X.original⟩) (Y := ⟨Y.original⟩) (.ofF51 raw))
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

theorem c60F52Inclusion_eval
    (p q : Quiver.Path a b)
    {X Y : C60F51OriginalTwo p q}
    (f : X ⟶ Y) :
    c60F52Eval ((c60F52Inclusion p q).map f) =
      c60F51Eval f := by
  refine Quot.inductionOn f (fun f => ?_)
  rfl

theorem c60F52Inclusion_faithful
    (p q : Quiver.Path a b)
    {X Y : C60F51OriginalTwo p q}
    {f g : X ⟶ Y}
    (heq : (c60F52Inclusion p q).map f =
      (c60F52Inclusion p q).map g) : f = g := by
  have hh :
      c60F52Eval ((c60F52Inclusion p q).map f) =
      c60F52Eval ((c60F52Inclusion p q).map g) :=
    congrArg (fun z => c60F52Eval z) heq
  rw [c60F52Inclusion_eval, c60F52Inclusion_eval] at hh
  apply c60F51GrayFunctor_faithful p q
  apply GradedThreeCell.ext
  · change (c60F51Eval f).charge = (c60F51Eval g).charge
    exact congrArg GradedThreeCell.charge hh
  · change (c60F51Eval f).phase = (c60F51Eval g).phase
    exact congrArg GradedThreeCell.phase hh

def c60F52OriginalTwoHorizontal
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    (X : C60F52OriginalTwo p q)
    (Y : C60F52OriginalTwo r s) :
    C60F52OriginalTwo (p.comp r) (q.comp s) :=
  ⟨X.original.horizontalLeftFirst Y.original⟩

def c60F52OriginalTwoHorizontalRight
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    (X : C60F52OriginalTwo p q)
    (Y : C60F52OriginalTwo r s) :
    C60F52OriginalTwo (p.comp r) (q.comp s) :=
  ⟨X.original.horizontalRightFirst Y.original⟩

def c60F52AssocRightTwo
    {a b c d : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    {t u : Quiver.Path c d}
    (X : C60F52OriginalTwo p q)
    (Y : C60F52OriginalTwo r s)
    (Z : C60F52OriginalTwo t u) :
    C60F52OriginalTwo ((p.comp r).comp t) ((q.comp s).comp u) :=
  ⟨c60F52AssocRight X.original Y.original Z.original⟩

/-- SOURCE typed associator: its target is a TRANSPORT of the
right-associated ORIGINAL proof term, not an equality of terms. -/
def c60F52Associator
    {a b c d : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    {t u : Quiver.Path c d}
    (X : C60F52OriginalTwo p q)
    (Y : C60F52OriginalTwo r s)
    (Z : C60F52OriginalTwo t u) :
    c60F52OriginalTwoHorizontal (c60F52OriginalTwoHorizontal X Y) Z ⟶
      c60F52AssocRightTwo X Y Z :=
  c60F52Of (.associator X.original Y.original Z.original)

theorem c60F52Associator_eval
    {a b c d : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    {t u : Quiver.Path c d}
    (X : C60F52OriginalTwo p q)
    (Y : C60F52OriginalTwo r s)
    (Z : C60F52OriginalTwo t u) :
    c60F52Eval (c60F52Associator X Y Z) =
      (0 : GradedThreeCell 0 0) := rfl

def c60F52LeftUnitTwo
    {a b : IcosahedralDart} {p q : Quiver.Path a b}
    (X : C60F52OriginalTwo p q) : C60F52OriginalTwo p q :=
  ⟨c60F52LeftUnitSource X.original⟩

def c60F52RightUnitTwo
    {a b : IcosahedralDart} {p q : Quiver.Path a b}
    (X : C60F52OriginalTwo p q) : C60F52OriginalTwo p q :=
  ⟨c60F52RightUnitSource X.original⟩

def c60F52LeftUnitor
    {a b : IcosahedralDart} {p q : Quiver.Path a b}
    (X : C60F52OriginalTwo p q) : c60F52LeftUnitTwo X ⟶ X :=
  c60F52Of (.leftUnitor X.original)

def c60F52RightUnitor
    {a b : IcosahedralDart} {p q : Quiver.Path a b}
    (X : C60F52OriginalTwo p q) : c60F52RightUnitTwo X ⟶ X :=
  c60F52Of (.rightUnitor X.original)

theorem c60F52LeftUnitor_eval
    {a b : IcosahedralDart} {p q : Quiver.Path a b}
    (X : C60F52OriginalTwo p q) :
    c60F52Eval (c60F52LeftUnitor X) = 0 := rfl

theorem c60F52RightUnitor_eval
    {a b : IcosahedralDart} {p q : Quiver.Path a b}
    (X : C60F52OriginalTwo p q) :
    c60F52Eval (c60F52RightUnitor X) = 0 := rfl

/-- Retain the original F43 nontrivial interchange with its
real LEFT-first and RIGHT-first ORIGINAL F42 proof boundaries. -/
def c60F52OriginalInterchanger
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    (X : C60F52OriginalTwo p q)
    (Y : C60F52OriginalTwo r s) :
    c60F52OriginalTwoHorizontal X Y ⟶
      c60F52OriginalTwoHorizontalRight X Y :=
  c60F52Of (.ofF51 (.original (.interchange X.original Y.original)))

theorem c60F52OriginalInterchanger_eval
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    (X : C60F52OriginalTwo p q)
    (Y : C60F52OriginalTwo r s) :
    c60F52Eval (c60F52OriginalInterchanger X Y) =
      c60F43PhysicalInterchangerNative X.original Y.original := rfl

#print axioms c60F52ThreeCategory
#print axioms c60F52Hom_ext
#print axioms c60F52GrayFunctor
#print axioms c60F52Inclusion
#print axioms c60F52Inclusion_faithful
#print axioms c60F52Associator
#print axioms c60F52LeftUnitor
#print axioms c60F52RightUnitor
#print axioms c60F52OriginalInterchanger_eval

end
end KUOS.DependentOriginationGrayC60OriginalFaceAssociatorThreeHomV5_200
