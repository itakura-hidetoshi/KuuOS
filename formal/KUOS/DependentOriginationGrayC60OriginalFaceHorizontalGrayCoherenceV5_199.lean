import KUOS.DependentOriginationGrayC60OriginalFaceHorizontalCompositionV5_199

namespace KUOS.DependentOriginationGrayC60OriginalFaceHorizontalGrayCoherenceV5_199

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60CyclicGlobalPastingV5_156
open KUOS.DependentOriginationGrayC60NativePathFunctorV5_189
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationGrayC60PresentedInterchangerV5_191
open KUOS.DependentOriginationGrayC60ThreeHomCategoriesV5_192
open KUOS.DependentOriginationGrayC60GradedGrayThreeCategoryV5_197
open KUOS.DependentOriginationGrayC60GrayThreeCategoryCompositionFunctorsV5_197
open KUOS.DependentOriginationGrayC60OriginalFaceTypedThreeHomLiftV5_198
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalPresentationV5_199
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalThreeHomV5_199
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalCompositionV5_199

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.199 / F59-F51-D — original horizontal 3-Hom / native Gray coherence

The NEW original-source horizontal and vertical categorical
3-Hom bifunctors are compatible with the old already-proved
FULL F49 Gray tensor in BOTH independent Int generator charges
and the separate ZMod2 phase. No parity-only projection is used.

Most importantly, the physical original F43 interchanger
remains a genuinely TYPED arrow between two DIFFERENT raw
F42 horizontal 2-cell pasting orders. We embed that old
source word as the ORIGINAL constructor of the new F51
category and prove its genuine odd/odd Gray value is NONZERO
at the actual north pentagon. This is not a replacement by
an identity exchange or a fabricated surface square.

The present results give honest horizontal composition
FUNCTORS on proof-relevant original face sources. The strict
associativity of raw F42 horizontal 2-cell terms and their
mixed F54/F55 global 3-dimensional pasting are not inferred:
source associators and mixed naturality remain distinct
higher coherence obligations.
-/

/-! I. FULL Gray-compatible original horizontal/vertical 3-Hom -/

/-- The complete original F51 source 2-cell horizontal
pasting maps to exactly the original F49 two-cell tensor. -/
theorem c60F51HorizontalGray_objects
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    (X : C60F51OriginalTwo p q)
    (Y : C60F51OriginalTwo r s) :
    (c60F51GrayFunctor (p.comp r) (q.comp s)).obj
      (c60F51OriginalTwoHorizontal X Y) =
    c60F49HorizontalTwo
      ((c60F51GrayFunctor p q).obj X)
      ((c60F51GrayFunctor r s).obj Y) := rfl

theorem c60F51VerticalGray_objects
    {a b : IcosahedralDart}
    {p q r : Quiver.Path a b}
    (X : C60F51OriginalTwo p q)
    (Y : C60F51OriginalTwo q r) :
    (c60F51GrayFunctor p r).obj
      (c60F51OriginalTwoVertical X Y) =
    c60F49VerticalTwo
      ((c60F51GrayFunctor p q).obj X)
      ((c60F51GrayFunctor q r).obj Y) := rfl

/-- NEW original F42 3-arrow HORIZONTAL composition evaluates
to the genuine complete F49 graded Gray three-cell tensor.
This asserts equality of TYPED 3-CELLS, not just their phases. -/
theorem c60F51HorizontalGray_morphisms
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    {X X' : C60F51OriginalTwo p q}
    {Y Y' : C60F51OriginalTwo r s}
    (f : X ⟶ X') (g : Y ⟶ Y') :
    (c60F51GrayFunctor (p.comp r) (q.comp s)).map
      (c60F51HorizontalMap f g) =
    c60F49HorizontalThree
      ((c60F51GrayFunctor p q).map f)
      ((c60F51GrayFunctor r s).map g) := by
  apply GradedThreeCell.ext
  · change
      (c60F51Eval (c60F51HorizontalMap f g)).charge =
      (c60F51Eval f).charge + (c60F51Eval g).charge
    rw [c60F51HorizontalMap_eval]
    exact grayNeutral_add_charge _ _
  · change
      (c60F51Eval (c60F51HorizontalMap f g)).phase =
      (c60F51Eval f).phase + (c60F51Eval g).phase
    rw [c60F51HorizontalMap_eval]
    exact grayNeutral_add_phase _ _

theorem c60F51VerticalGray_morphisms
    {a b : IcosahedralDart}
    {p q r : Quiver.Path a b}
    {X X' : C60F51OriginalTwo p q}
    {Y Y' : C60F51OriginalTwo q r}
    (f : X ⟶ X') (g : Y ⟶ Y') :
    (c60F51GrayFunctor p r).map
      (c60F51VerticalTwoMap f g) =
    c60F49VerticalTensorThree
      ((c60F51GrayFunctor p q).map f)
      ((c60F51GrayFunctor q r).map g) := by
  apply GradedThreeCell.ext
  · change
      (c60F51Eval (c60F51VerticalTwoMap f g)).charge =
      (c60F51Eval f).charge + (c60F51Eval g).charge
    rw [c60F51VerticalTwoMap_eval]
    exact grayNeutral_add_charge _ _
  · change
      (c60F51Eval (c60F51VerticalTwoMap f g)).phase =
      (c60F51Eval f).phase + (c60F51Eval g).phase
    rw [c60F51VerticalTwoMap_eval]
    exact grayNeutral_add_phase _ _

/-! II. Genuine ORIGINAL F43 Gray interchange in the new source -/

/-- A true original F43 interchange generator, not an adjoined
horizontal 3-cell, between the two DIFFERENT horizontal
pasting orders of original C60 physical F42 face 2-cells. -/
def c60F51OriginalInterchanger
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    (X : C60F51OriginalTwo p q)
    (Y : C60F51OriginalTwo r s) :
    c60F51OriginalTwoHorizontal X Y ⟶
      c60F51OriginalTwoHorizontalRight X Y :=
  c60F51Of (.original (.interchange X.original Y.original))

/-- Complete native source-to-target image of a REAL F43
interchanger: BOTH integer components remain zero, whereas
its independent Gray exchange phase is the original product
of the full source face degrees. -/
theorem c60F51OriginalInterchanger_native
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    (X : C60F51OriginalTwo p q)
    (Y : C60F51OriginalTwo r s) :
    c60F51Eval (c60F51OriginalInterchanger X Y) =
      c60F43PhysicalInterchangerNative X.original Y.original := rfl

theorem c60F51OriginalInterchanger_nativeComponents
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    (X : C60F51OriginalTwo p q)
    (Y : C60F51OriginalTwo r s) :
    (c60F51Eval (c60F51OriginalInterchanger X Y)).charge =
        ((0 : Int), (0 : Int)) ∧
    (c60F51Eval (c60F51OriginalInterchanger X Y)).phase =
      c60F43FaceDegree X.original *
        c60F43FaceDegree Y.original :=
  ⟨rfl, rfl⟩

/-- The original exact F43 north-pentagon face 2-cell,
retained as an original source F42 witness, now a separate
object of the new F51 original face source category. -/
def c60F51NorthFaceSourceTwo :
    C60F51OriginalTwo
      (c60F41PentagonBoundaryLoop .north) Quiver.Path.nil :=
  c60F51OriginalTwoOf c60F43NorthPentagonFaceTwoCell

/-- The ACTUAL original F43 north-pentagon interchanger
survives with its two truly distinct proof-relevant source
2-cell pasting boundaries, even after the F51 source extension. -/
def c60F51NorthOriginalInterchanger :
    c60F51OriginalTwoHorizontal
      c60F51NorthFaceSourceTwo c60F51NorthFaceSourceTwo ⟶
    c60F51OriginalTwoHorizontalRight
      c60F51NorthFaceSourceTwo c60F51NorthFaceSourceTwo :=
  c60F51OriginalInterchanger
    c60F51NorthFaceSourceTwo c60F51NorthFaceSourceTwo

theorem c60F51NorthOriginalInterchanger_native
    (h : GradedThreeCell 0 0) :
    (c60F51Eval c60F51NorthOriginalInterchanger = h) ↔
      c60F43NorthPentagonInterchange.toNative = h := by
  change c60F43NorthPentagonInterchange.toNative = h ↔
    c60F43NorthPentagonInterchange.toNative = h
  rfl

theorem c60F51NorthOriginalInterchanger_phaseOne :
    (c60F51Eval c60F51NorthOriginalInterchanger).phase =
      (1 : ZMod 2) := by
  change c60F43NorthPentagonInterchange.toNative.phase = 1
  exact c60F43NorthPentagonInterchange_components.2

theorem c60F51NorthOriginalInterchanger_nontrivial :
    c60F51Eval c60F51NorthOriginalInterchanger ≠
      (0 : GradedThreeCell 0 0) := by
  intro h
  have hp := congrArg GradedThreeCell.phase h
  change (1 : ZMod 2) = 0 at hp
  exact (by decide : (1 : ZMod 2) ≠ 0) hp

/-- This original north exchange is EXACTLY the embedded old
F43/F44 source arrow, rather than a fabricated new horizontal
generator or any newly adjoined F54/F55 comparison. -/
theorem c60F51NorthInterchanger_isOriginalF43 :
    c60F51NorthOriginalInterchanger =
      (c60F51OriginalInclusion
        ((c60F41PentagonBoundaryLoop .north).comp
          (c60F41PentagonBoundaryLoop .north))
        (Quiver.Path.nil)).map
      (c60F44FaceThreeOf c60F43NorthPentagonInterchange) := rfl

#print axioms c60F51HorizontalGray_objects
#print axioms c60F51HorizontalGray_morphisms
#print axioms c60F51VerticalGray_objects
#print axioms c60F51VerticalGray_morphisms
#print axioms c60F51OriginalInterchanger_native
#print axioms c60F51NorthOriginalInterchanger_phaseOne
#print axioms c60F51NorthOriginalInterchanger_nontrivial
#print axioms c60F51NorthInterchanger_isOriginalF43

end
end KUOS.DependentOriginationGrayC60OriginalFaceHorizontalGrayCoherenceV5_199
