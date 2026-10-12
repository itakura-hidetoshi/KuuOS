import KUOS.DependentOriginationGrayC60GrayThreeCategoryCompositionFunctorsV5_197

namespace KUOS.DependentOriginationGrayC60OriginalFaceTypedThreeHomLiftV5_198

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60CyclicGlobalPastingV5_156
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationGrayC60PresentedInterchangerV5_191
open KUOS.DependentOriginationGrayC60ThreeHomCategoriesV5_192
open KUOS.DependentOriginationGrayC60FaceWhiskeringFunctorsV5_193
open KUOS.DependentOriginationGrayC60GradedGrayThreeCategoryV5_197
open KUOS.DependentOriginationGrayC60GrayThreeCategoryCompositionFunctorsV5_197

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# F59-F50 / v5.198 — ORIGINAL C60 proof-relevant 2-cell 3-Hom lift

F49's completed Gray 3-category envelope has the real 60-object C60
path 0/1-structure and the *grade-completed* GrayGrade local 3-Homs.
F44 separately constructed the ORIGINAL source 3-Hom categories:
their OBJECTS are proof-relevant F42 polygonal face 2-cell terms
with their exact original physical path boundaries, and their
MORPHISMS are original F43 source 3-cells modulo only their
full native Int×Int integer charge and independent ZMod2 phase.

This file constructs a NEW genuine Mathlib functor, for EVERY
original parallel C60 physical 1-path pair, from the ORIGINAL F42
2-cell 3-Hom CATEGORY to F49's ACTUAL path-indexed Gray 3-Hom.
Its object map is original F43 face degree; its morphism map uses
the F43 source-preservesFaceDegree proof for BOTH correctly typed
2-cell endpoints, and preserves the FULL independent charge/phase.
Both categorical unit and composition laws and faithfulness on
the ORIGINAL F44 3-cell kernel quotient are proved, not assumed.

Crucially this functor is NOT injective on raw F42 2-cell objects:
the two ORIGINAL north pentagon horizontal 2-cell pasting orders
are genuinely different source 2-cell syntax yet have equal
GrayGrade object values. We prove and EXPOSE this precise
original-presentation information loss rather than falsely
declaring the F49 graded envelope equivalent to all original
F42/F54/F55 source data.
-/

/-! I. Original source 3-cell morphisms preserve their true grades -/

/-- Every original F44 categorical 3-arrow is represented by
an F43 proof-relevant 3-cell whose endpoint face degrees agree.
This property survives exactly the full-native kernel quotient. -/
theorem c60F50OriginalFaceHom_degreeEq
    {a b : IcosahedralDart}
    {p q : Quiver.Path a b}
    {α β : C60F42PresentedFaceCell p q}
    (f : α ⟶ β) :
    c60F43FaceDegree α = c60F43FaceDegree β := by
  refine Quot.inductionOn f (fun raw => ?_)
  exact raw.preservesFaceDegree

/-- Lift a source F43 categorical 3-arrow to its FULL native
F49 typed Gray 3-arrow between the correct ORIGINAL F42 source
2-cell endpoint grades, not between fabricated neutral objects. -/
def c60F50OriginalFaceHom_typedLift
    {a b : IcosahedralDart}
    {p q : Quiver.Path a b}
    {α β : C60F42PresentedFaceCell p q}
    (f : α ⟶ β) :
    C60F49Three (c60F49OriginalFaceTwo α)
      (c60F49OriginalFaceTwo β) :=
  ⟨c60F50OriginalFaceHom_degreeEq f,
    (c60F44FaceThreeEval f).charge,
    (c60F44FaceThreeEval f).phase⟩

theorem c60F50OriginalFaceHom_typedLift_components
    {a b : IcosahedralDart}
    {p q : Quiver.Path a b}
    {α β : C60F42PresentedFaceCell p q}
    (f : α ⟶ β) :
    (c60F50OriginalFaceHom_typedLift f).charge =
      (c60F44FaceThreeEval f).charge ∧
    (c60F50OriginalFaceHom_typedLift f).phase =
      (c60F44FaceThreeEval f).phase :=
  ⟨rfl, rfl⟩

/-- ORIGINAL F42 face-2-cell 3-Hom to the complete F49
Gray 3-Hom is an ACTUAL Mathlib functor, with each original
source 2-cell retained as its source-category object. -/
def c60F50OriginalFaceTypedThreeHomFunctor
    {a b : IcosahedralDart} (p q : Quiver.Path a b) :
    C60F42PresentedFaceCell p q ⥤ C60F49Two p q where
  obj α := c60F49OriginalFaceTwo α
  map := fun {_ _} f => c60F50OriginalFaceHom_typedLift f
  map_id := by
    intro α
    apply GradedThreeCell.ext <;> rfl
  map_comp := by
    intro α β γ f g
    apply GradedThreeCell.ext
    · change
        (c60F44FaceThreeEval (c60F44FaceThreeComp f g)).charge =
          (c60F44FaceThreeEval f).charge +
            (c60F44FaceThreeEval g).charge
      rw [c60F44FaceThreeEval_comp]
      exact grayNeutral_add_charge _ _
    · change
        (c60F44FaceThreeEval (c60F44FaceThreeComp f g)).phase =
          (c60F44FaceThreeEval f).phase +
            (c60F44FaceThreeEval g).phase
      rw [c60F44FaceThreeEval_comp]
      exact grayNeutral_add_phase _ _

/-- Original F43 source 3-cell constructors are transported to
EXACTLY the independently constructed F49 typed 3-morphisms.
No source phase or F58 charge projection and no arbitrary
choice of original 2-cell boundary is performed. -/
theorem c60F50OriginalRawThreeCell_map
    {a b : IcosahedralDart}
    {p q : Quiver.Path a b}
    {α β : C60F42PresentedFaceCell p q}
    (f : C60F43PresentedThreeCell α β) :
    (c60F50OriginalFaceTypedThreeHomFunctor p q).map
      (c60F44FaceThreeOf f) =
        c60F49OriginalFaceThree f := by
  apply GradedThreeCell.ext <;> rfl

/-- COMPLETE native morphism faithfulness on the real original
F43/F44 source-kernel quotient, not an unproved faithful
embedding of all ORIGINAL F42 2-cell objects. -/
theorem c60F50OriginalFaceTypedThreeHomFunctor_faithful
    {a b : IcosahedralDart} {p q : Quiver.Path a b}
    {α β : C60F42PresentedFaceCell p q}
    {f g : α ⟶ β}
    (h : (c60F50OriginalFaceTypedThreeHomFunctor p q).map f =
      (c60F50OriginalFaceTypedThreeHomFunctor p q).map g) :
    f = g := by
  have hc := congrArg GradedThreeCell.charge h
  have hp := congrArg GradedThreeCell.phase h
  change (c60F44FaceThreeEval f).charge =
    (c60F44FaceThreeEval g).charge at hc
  change (c60F44FaceThreeEval f).phase =
    (c60F44FaceThreeEval g).phase at hp
  apply c60F44FaceThreeGrayFunctor_faithful
  exact GradedThreeCell.ext hc hp

/-! II. Detect, rather than erase, two DIFFERENT genuine C60 2-cells -/

/-- The original two horizontal 2-cell pasting orders around
the ACTUAL north pentagon are different proof-relevant F42
source 2-cell terms. Their first trans-generator branches
are different original whiskering constructors. -/
theorem c60F50OriginalNorthTwoPastingOrders_distinct :
    (c60F43NorthPentagonFaceTwoCell.horizontalLeftFirst
      c60F43NorthPentagonFaceTwoCell) ≠
    (c60F43NorthPentagonFaceTwoCell.horizontalRightFirst
      c60F43NorthPentagonFaceTwoCell) := by
  intro h
  cases h

/-- Despite genuinely DIFFERENT original F42 source 2-cell
proof terms, the graded-envelope 2-cell image is EQUAL.
This demonstrates precisely why an unqualified assertion
of faithfulness on source 2-cell objects would be incorrect. -/
theorem c60F50OriginalNorthTwoPastingOrders_sameGrade :
    c60F49OriginalFaceTwo
      (c60F43NorthPentagonFaceTwoCell.horizontalLeftFirst
        c60F43NorthPentagonFaceTwoCell) =
    c60F49OriginalFaceTwo
      (c60F43NorthPentagonFaceTwoCell.horizontalRightFirst
        c60F43NorthPentagonFaceTwoCell) := rfl

/-- The ACTUAL original F43 north interchanger survives as
a nonidentity source 3-morphism and keeps the exact native
nonzero exchange phase after the source-typed functor. -/
theorem c60F50OriginalNorthInterchanger_typedPhase :
    ((c60F50OriginalFaceTypedThreeHomFunctor
      (c60F41PentagonBoundaryLoop .north |>.comp
        (c60F41PentagonBoundaryLoop .north))
      (Quiver.Path.nil)).map
      (c60F44FaceThreeOf c60F43NorthPentagonInterchange)).phase =
        (1 : ZMod 2) := by
  rw [c60F50OriginalRawThreeCell_map]
  exact c60F43NorthPentagonInterchange_components.2

#print axioms c60F50OriginalFaceHom_degreeEq
#print axioms c60F50OriginalFaceHom_typedLift_components
#print axioms c60F50OriginalFaceTypedThreeHomFunctor
#print axioms c60F50OriginalRawThreeCell_map
#print axioms c60F50OriginalFaceTypedThreeHomFunctor_faithful
#print axioms c60F50OriginalNorthTwoPastingOrders_distinct
#print axioms c60F50OriginalNorthTwoPastingOrders_sameGrade
#print axioms c60F50OriginalNorthInterchanger_typedPhase

end
end KUOS.DependentOriginationGrayC60OriginalFaceTypedThreeHomLiftV5_198
