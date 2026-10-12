import KUOS.DependentOriginationGrayC60OriginalFaceDecoratedThreeHomV5_198

namespace KUOS.DependentOriginationGrayC60OriginalFaceWhiskeringNaturalityV5_198

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60CyclicGlobalPastingV5_156
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationGrayC60PresentedInterchangerV5_191
open KUOS.DependentOriginationGrayC60ThreeHomCategoriesV5_192
open KUOS.DependentOriginationGrayC60FaceWhiskeringFunctorsV5_193
open KUOS.DependentOriginationGrayC60GradedGrayThreeCategoryV5_197
open KUOS.DependentOriginationGrayC60GrayThreeCategoryCompositionFunctorsV5_197
open KUOS.DependentOriginationGrayC60OriginalFaceTypedThreeHomLiftV5_198
open KUOS.DependentOriginationGrayC60OriginalFaceDecoratedThreeHomV5_198

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# F59-F50 / v5.198 — whiskering naturality of ORIGINAL C60 face-source 3-Homs

The original F45 face-source left/right path whiskering functors
ACT on original F42 proof-relevant 2-cell objects and original
F43 categorical 3-morphisms. The new F50 functor is faithful
on the original F43 native-kernel quotient, while its GrayGrade
output belongs to F49's complete graded 3-category envelope.

We prove that ORIGINAL whiskering of real typed C60 1-paths and
the new original-source-aware F50 typed 3-Hom functor commute
both on 2-cell objects and on ALL complete F58 integer charges
and F59 independent Gray phases of 3-morphisms.

This is a literal object and arrow comparison for the ACTUAL
original source functors, not a claim that the two original
raw F42 path-context terms are judgmentally equal or that
an originally unprovided F54/F55 boundary comparison exists.
-/

/-! I. ORIGINAL left path whiskering: object and 3-arrow laws -/

/-- Both paths contain the ORIGINAL source 2-cell witness;
the F50 graded image is compatible with the F45 original
left-whiskering functor and F49's path-indexed graded output. -/
theorem c60F50LeftOriginalFaceWhisker_object
    {a b c : IcosahedralDart}
    (prior : Quiver.Path a b)
    {p q : Quiver.Path b c}
    (α : C60F42PresentedFaceCell p q) :
    (c60F50OriginalFaceTypedThreeHomFunctor
      (prior.comp p) (prior.comp q)).obj
        ((c60F45LeftWhiskerFunctor prior).obj α) =
    (c60F49LeftPathThreeHomFunctor prior).obj
      ((c60F50OriginalFaceTypedThreeHomFunctor p q).obj α) := by
  rfl

/-- Original F43 3-cell charge, NOT merely the face degree,
is preserved by the entire left source-whiskering diagram. -/
theorem c60F50LeftOriginalFaceWhisker_map
    {a b c : IcosahedralDart}
    (prior : Quiver.Path a b)
    {p q : Quiver.Path b c}
    {α β : C60F42PresentedFaceCell p q}
    (f : α ⟶ β) :
    (c60F50OriginalFaceTypedThreeHomFunctor
      (prior.comp p) (prior.comp q)).map
        ((c60F45LeftWhiskerFunctor prior).map f) =
    (c60F49LeftPathThreeHomFunctor prior).map
      ((c60F50OriginalFaceTypedThreeHomFunctor p q).map f) := by
  apply GradedThreeCell.ext
  · change
      (c60F44FaceThreeEval
        ((c60F45LeftWhiskerFunctor prior).map f)).charge =
      (c60F44FaceThreeEval f).charge
    rw [c60F45LeftWhiskerGrayMap]
  · change
      (c60F44FaceThreeEval
        ((c60F45LeftWhiskerFunctor prior).map f)).phase =
      (c60F44FaceThreeEval f).phase
    rw [c60F45LeftWhiskerGrayMap]

/-! II. ORIGINAL right path whiskering: object and 3-arrow laws -/

theorem c60F50RightOriginalFaceWhisker_object
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b}
    (suffix : Quiver.Path b c)
    (α : C60F42PresentedFaceCell p q) :
    (c60F50OriginalFaceTypedThreeHomFunctor
      (p.comp suffix) (q.comp suffix)).obj
        ((c60F45RightWhiskerFunctor suffix).obj α) =
    (c60F49RightPathThreeHomFunctor suffix).obj
      ((c60F50OriginalFaceTypedThreeHomFunctor p q).obj α) := by
  rfl

theorem c60F50RightOriginalFaceWhisker_map
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b}
    (suffix : Quiver.Path b c)
    {α β : C60F42PresentedFaceCell p q}
    (f : α ⟶ β) :
    (c60F50OriginalFaceTypedThreeHomFunctor
      (p.comp suffix) (q.comp suffix)).map
        ((c60F45RightWhiskerFunctor suffix).map f) =
    (c60F49RightPathThreeHomFunctor suffix).map
      ((c60F50OriginalFaceTypedThreeHomFunctor p q).map f) := by
  apply GradedThreeCell.ext
  · change
      (c60F44FaceThreeEval
        ((c60F45RightWhiskerFunctor suffix).map f)).charge =
      (c60F44FaceThreeEval f).charge
    rw [c60F45RightWhiskerGrayMap]
  · change
      (c60F44FaceThreeEval
        ((c60F45RightWhiskerFunctor suffix).map f)).phase =
      (c60F44FaceThreeEval f).phase
    rw [c60F45RightWhiskerGrayMap]

/-! III. Two original context orders: equality of complete Gray images -/

/-- Both differently TYPED original C60 F42 path-context
whiskering orders retain exactly the complete F43/F59 3-cell
evaluation. The original raw F42 witnesses are NOT equated. -/
theorem c60F50LeftRightOriginalGray_coherent
    {a b c d : IcosahedralDart}
    (prior : Quiver.Path a b)
    {p q : Quiver.Path b c}
    (suffix : Quiver.Path c d)
    {α β : C60F42PresentedFaceCell p q}
    (f : α ⟶ β) :
    c60F44FaceThreeEval
      ((c60F45RightWhiskerFunctor suffix).map
        ((c60F45LeftWhiskerFunctor prior).map f)) =
    c60F44FaceThreeEval
      ((c60F45LeftWhiskerFunctor prior).map
        ((c60F45RightWhiskerFunctor suffix).map f)) :=
  c60F45LeftRightGrayImage_coherent prior suffix f

#print axioms c60F50LeftOriginalFaceWhisker_object
#print axioms c60F50LeftOriginalFaceWhisker_map
#print axioms c60F50RightOriginalFaceWhisker_object
#print axioms c60F50RightOriginalFaceWhisker_map
#print axioms c60F50LeftRightOriginalGray_coherent

end
end KUOS.DependentOriginationGrayC60OriginalFaceWhiskeringNaturalityV5_198
