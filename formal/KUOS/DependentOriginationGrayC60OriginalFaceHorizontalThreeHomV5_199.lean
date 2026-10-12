import KUOS.DependentOriginationGrayC60OriginalFaceHorizontalPresentationV5_199

namespace KUOS.DependentOriginationGrayC60OriginalFaceHorizontalThreeHomV5_199

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60CyclicGlobalPastingV5_156
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationGrayC60PresentedInterchangerV5_191
open KUOS.DependentOriginationGrayC60ThreeHomCategoriesV5_192
open KUOS.DependentOriginationGrayC60GradedGrayThreeCategoryV5_197
open KUOS.DependentOriginationGrayC60OriginalFaceTypedThreeHomLiftV5_198
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalPresentationV5_199

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.199 / F59-F51-B — honest source 3-Hom category and original inclusion

The new F51 original horizontal 3-cell presentation is a real
DEPENDENT inductive source. Its raw 3-cell terms do not satisfy
literal strict categorical associativity, so exactly as in F44
we quotient ONLY by equality of their COMPLETE native F59
Int×Int charge AND independent braided ZMod2 exchange phase.

Each local category has an object type NEWLY WRAPPED around the
complete proof-relevant original F42 2-cell; hence it does not
replace or conflict with the existing original F44 source category.

We prove all Mathlib category axioms, a faithful functor into
the actual F49 graded 3-Hom over exactly the original C60
parallel physical 1-paths, and a faithful source inclusion of
ALL original F43/F44 categorical 3-cells. No preexisting
original F43 horizontal constructor is invented: all new
horizontal 3-cells belong precisely to the new F51 language.
-/

variable {a b : IcosahedralDart}
variable {p q : Quiver.Path a b}

/-- Full-native kernel equality ONLY between correctly parallel
new original-source 3-cell terms with fixed original F42 2-cell
boundaries. Both integer charges and phase are retained. -/
def c60F51NativeRel
    {α β : C60F42PresentedFaceCell p q}
    (f g : C60F51PresentedThreeCell α β) : Prop :=
  f.toNative = g.toNative

abbrev C60F51Hom
    (X Y : C60F51OriginalTwo p q) : Type :=
  Quot (c60F51NativeRel (α := X.original) (β := Y.original))

def c60F51Of
    {X Y : C60F51OriginalTwo p q}
    (f : C60F51PresentedThreeCell X.original Y.original) :
    C60F51Hom X Y :=
  Quot.mk _ f

def c60F51Eval
    {X Y : C60F51OriginalTwo p q}
    (f : C60F51Hom X Y) : GradedThreeCell 0 0 :=
  Quot.liftOn f (fun raw => raw.toNative) (by
    intro f g h
    exact h)

@[simp] theorem c60F51Eval_of
    {X Y : C60F51OriginalTwo p q}
    (f : C60F51PresentedThreeCell X.original Y.original) :
    c60F51Eval (c60F51Of f) = f.toNative := rfl

def c60F51Comp
    {X Y Z : C60F51OriginalTwo p q}
    (f : C60F51Hom X Y) (g : C60F51Hom Y Z) :
    C60F51Hom X Z :=
  Quot.liftOn₂ f g
    (fun x y => c60F51Of (.trans x y))
    (by
      intro x y₁ y₂ hh
      apply Quot.sound
      change x.toNative + y₁.toNative =
        x.toNative + y₂.toNative
      rw [hh])
    (by
      intro x₁ x₂ y hh
      apply Quot.sound
      change x₁.toNative + y.toNative =
        x₂.toNative + y.toNative
      rw [hh])

theorem c60F51Eval_comp
    {X Y Z : C60F51OriginalTwo p q}
    (f : C60F51Hom X Y) (g : C60F51Hom Y Z) :
    c60F51Eval (c60F51Comp f g) =
      c60F51Eval f + c60F51Eval g := by
  refine Quot.inductionOn f (fun f => ?_)
  refine Quot.inductionOn g (fun g => ?_)
  rfl

/-- The actual F51 original proof-relevant 2-cell 3-Hom:
new original F42-witness objects, F43 plus adjoined horizontal
source words as categorical arrows, with full target-kernel
quotient and complete associative/unital Mathlib laws. -/
instance c60F51ThreeCategory :
    Category (C60F51OriginalTwo p q) where
  Hom := C60F51Hom
  id X := c60F51Of (.ident X.original)
  comp := c60F51Comp
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

/-- Every genuinely typed F51 categorical 3-arrow has
equal original F43 face-degree at both actual F42 endpoints. -/
theorem c60F51Hom_degreeEq
    {X Y : C60F51OriginalTwo p q}
    (f : X ⟶ Y) :
    c60F43FaceDegree X.original =
      c60F43FaceDegree Y.original := by
  refine Quot.inductionOn f (fun raw => ?_)
  exact raw.preservesFaceDegree

/-- Lift the actual source arrow to the full F59 *typed*
Gray 3-cell between the degrees of its ORIGINAL F42 2-cell
boundaries. No second integer charge or phase is erased. -/
def c60F51Lift
    {X Y : C60F51OriginalTwo p q}
    (f : X ⟶ Y) :
    C60F49Three
      (c60F49OriginalFaceTwo X.original)
      (c60F49OriginalFaceTwo Y.original) :=
  ⟨c60F51Hom_degreeEq f,
    (c60F51Eval f).charge, (c60F51Eval f).phase⟩

/-- The ACTUAL original source/horizontal extension maps
into the genuine F49 3-Hom category through a Mathlib
functor on EVERY parallel original C60 1-path pair. -/
def c60F51GrayFunctor (p q : Quiver.Path a b) :
    C60F51OriginalTwo p q ⥤ C60F49Two p q where
  obj X := c60F49OriginalFaceTwo X.original
  map := fun {_ _} f => c60F51Lift f
  map_id := by
    intro X
    apply GradedThreeCell.ext <;> rfl
  map_comp := by
    intro X Y Z f g
    apply GradedThreeCell.ext
    · change (c60F51Eval (c60F51Comp f g)).charge =
        (c60F51Eval f).charge + (c60F51Eval g).charge
      rw [c60F51Eval_comp]
      exact grayNeutral_add_charge _ _
    · change (c60F51Eval (c60F51Comp f g)).phase =
        (c60F51Eval f).phase + (c60F51Eval g).phase
      rw [c60F51Eval_comp]
      exact grayNeutral_add_phase _ _

theorem c60F51GrayFunctor_faithful
    (p q : Quiver.Path a b)
    {X Y : C60F51OriginalTwo p q}
    {f g : X ⟶ Y}
    (h : (c60F51GrayFunctor p q).map f =
      (c60F51GrayFunctor p q).map g) : f = g := by
  have hc := congrArg GradedThreeCell.charge h
  have hp := congrArg GradedThreeCell.phase h
  change (c60F51Eval f).charge = (c60F51Eval g).charge at hc
  change (c60F51Eval f).phase = (c60F51Eval g).phase at hp
  apply Quot.sound
  exact GradedThreeCell.ext hc hp

/-! ## Genuine ORIGINAL F43/F44 source injection -/

/-- A native F44 proof-relevant original 3-arrow becomes a
literal original-3-cell constructor in the strictly LARGER
F51 source presentation; equal complete native values
remain identified by the exact F51 quotient. -/
def c60F51OriginalInclusion (p q : Quiver.Path a b) :
    C60F42PresentedFaceCell p q ⥤
      C60F51OriginalTwo p q where
  obj X := ⟨X⟩
  map := fun {X Y} f =>
    Quot.liftOn f
      (fun raw => c60F51Of
        (X := ⟨X⟩) (Y := ⟨Y⟩) (.original raw))
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

theorem c60F51OriginalInclusion_native
    (p q : Quiver.Path a b)
    {α β : C60F42PresentedFaceCell p q}
    (f : α ⟶ β) :
    c60F51Eval ((c60F51OriginalInclusion p q).map f) =
      c60F44FaceThreeEval f := by
  refine Quot.inductionOn f (fun raw => ?_)
  rfl

theorem c60F51OriginalInclusion_faithful
    (p q : Quiver.Path a b)
    {α β : C60F42PresentedFaceCell p q}
    {f g : α ⟶ β}
    (h : (c60F51OriginalInclusion p q).map f =
      (c60F51OriginalInclusion p q).map g) : f = g := by
  have hh := congrArg
    (fun z => c60F51Eval z) h
  rw [c60F51OriginalInclusion_native,
    c60F51OriginalInclusion_native] at hh
  exact c60F44FaceThreeGrayFunctor_faithful hh

/-- The new source and OLD F50 source faithfully have the
same complete F59 target interpretation on all original
3-morphisms, although the new horizontal extension has
strictly more raw SOURCE constructors than original F43. -/
theorem c60F51OriginalInclusion_GrayMap
    (p q : Quiver.Path a b)
    {α β : C60F42PresentedFaceCell p q} (f : α ⟶ β) :
    (c60F51GrayFunctor p q).map
      ((c60F51OriginalInclusion p q).map f) =
    (c60F50OriginalFaceTypedThreeHomFunctor p q).map f := by
  have hh := c60F51OriginalInclusion_native p q f
  apply GradedThreeCell.ext
  · exact congrArg GradedThreeCell.charge hh
  · exact congrArg GradedThreeCell.phase hh

#print axioms c60F51ThreeCategory
#print axioms c60F51Eval_comp
#print axioms c60F51GrayFunctor
#print axioms c60F51GrayFunctor_faithful
#print axioms c60F51OriginalInclusion
#print axioms c60F51OriginalInclusion_native
#print axioms c60F51OriginalInclusion_faithful
#print axioms c60F51OriginalInclusion_GrayMap

end
end KUOS.DependentOriginationGrayC60OriginalFaceHorizontalThreeHomV5_199
