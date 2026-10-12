import KUOS.DependentOriginationGrayC60F55DirectCompositePhysicalV5_209

namespace KUOS.DependentOriginationGrayC60F55DirectPastedBeckChevalleyV5_210

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationGrayC60PresentedInterchangerV5_191
open KUOS.DependentOriginationGrayC60ThreeHomCategoriesV5_192
open KUOS.DependentOriginationGrayC60OriginalF55ThreeHomV5_192
open KUOS.DependentOriginationGrayC60FaceWhiskeringFunctorsV5_193
open KUOS.DependentOriginationGrayC60OriginalF55WhiskeringV5_193
open KUOS.DependentOriginationGrayC60MixedBoundaryThreeHomV5_195
open KUOS.DependentOriginationGrayC60MixedBoundaryWhiskeringV5_195
open KUOS.DependentOriginationGrayC60F55MixedOriginalContextV5_205
open KUOS.DependentOriginationGrayC60F55OriginalContextBeckChevalleyV5_207
open KUOS.DependentOriginationGrayC60F55TwoContextBeckChevalleyV5_208
open KUOS.DependentOriginationGrayC60F55DirectCompositeContextV5_209
open KUOS.DependentOriginationGrayC60F55DirectCompositePhysicalV5_209
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.210 / F59-F60-C — SOURCE Beck–Chevalley direct-vs-pasted cube

F58 gives original F42/F54 Beck–Chevalley NatIso, F59 gives its
two-successive-original-context pasting, and F60 gives genuinely
concatenated original F42 Quiver.Path + original F54 bracket-tree
node/direct-versus-nested normalization. The present module compares
the TWO resulting source NatIso in a common correctly typed F47
full-native-kernel FOUR-BOUNDARY category.

A direct original F42/F54 syntax term is NOT asserted equal to a
nested original syntax term. The final normalization functor and the
four tags are retained on all sides of the cube. This does not erase
the adjoined Delta, original F55 nonflat curvature or descent
obstructions.
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section OriginalLeftBeckChevalleyCube

variable {a b : D} {x y : E}
variable {n n' m m' : Nat}
variable {ma mb : Blocks a b} {pa pb : Blocks x y}
variable {first : OriginalF45BracketTree n m ma pa mb pb}
variable {last : OriginalF45BracketTree n' m' ma pa mb pb}
variable {r s : OriginalF45BracketTree.DepthRotationRoute first last}
variable {v₀ w₀ v₁ w₁ : IcosahedralDart}
variable {p₀ q₀ : Quiver.Path v₀ w₀}
variable {p₁ q₁ : Quiver.Path v₁ w₁}
variable {α₀ β₀ : C60F42PresentedFaceCell p₀ q₀}
variable {α₁ β₁ : C60F42PresentedFaceCell p₁ q₁}
variable (B₀ : C60F47SquareFrame α₀ β₀ r s)
variable (B₁ : C60F47SquareFrame α₁ β₁ r s)

/-- Horizontal front/back FACE-CHOICE square of the higher cube:
original F42 direct concatenation and original F54 direct node
versus original F42/F54 nested contextualization. Both are true
source Mathlib functors on the four F47 tags. -/
def c60F61LeftFaceChoiceDirectNestedNatIso
    (hedge : B₀.edge = B₁.edge)
    (hface : c60F44FaceThreeEval B₀.faceStep =
      c60F44FaceThreeEval B₁.faceStep)
    (hrot : c60F44OriginalF55Eval B₀.rotationStep =
      c60F44OriginalF55Eval B₁.rotationStep)
    {u₀ u₁ z₀ z₁ : IcosahedralDart}
    (prior₀ : Quiver.Path u₀ v₀) (prior₁ : Quiver.Path u₁ v₁)
    (outer₀ : Quiver.Path z₀ u₀) (outer₁ : Quiver.Path z₁ u₁)
    {k₁ l₁ k₂ l₂ : Nat}
    {mc md : Blocks a b} {pc pd : Blocks x y}
    (later₁ : OriginalF45BracketTree k₁ l₁ mb pb mc pc)
    (later₂ : OriginalF45BracketTree k₂ l₂ mc pc md pd) :
    (c60F58LeftAfterFaceChoice B₀ B₁ hedge hface hrot
        (outer₀.comp prior₀) (outer₁.comp prior₁)
        (OriginalF45BracketTree.node later₁ later₂)) ⋙
      (c60F60LeftDirectToNested B₁ prior₁ outer₁ later₁ later₂) ≅
    (c60F60LeftDirectToNested B₀ prior₀ outer₀ later₁ later₂) ⋙
      (c60F59LeftSecondFaceChoice B₀ B₁ hedge hface hrot
        prior₀ prior₁ outer₀ outer₁ later₁ later₂) :=
  NatIso.ofComponents
    (fun X => by cases X <;> exact Iso.refl _)
    (by
      intro X Y f
      cases X <;> cases Y
      all_goals
        calc
          _ = ((c60F58LeftAfterFaceChoice B₀ B₁ hedge hface hrot
                (outer₀.comp prior₀) (outer₁.comp prior₁)
                    (OriginalF45BracketTree.node later₁ later₂)) ⋙
                (c60F60LeftDirectToNested B₁ prior₁ outer₁ later₁ later₂)).map f :=
              Category.comp_id _
          _ = ((c60F60LeftDirectToNested B₀ prior₀ outer₀ later₁ later₂) ⋙
                (c60F59LeftSecondFaceChoice B₀ B₁ hedge hface hrot
                  prior₀ prior₁ outer₀ outer₁ later₁ later₂)).map f := by
              apply c60F47MixedGrayFunctor_faithful
                (c60F60LeftNestedFrame B₁ prior₁ outer₁ later₁ later₂)
              change c60F47MixedEval
                  ((c60F60LeftDirectToNested B₁ prior₁ outer₁ later₁ later₂).map
                    ((c60F58LeftAfterFaceChoice B₀ B₁ hedge hface hrot
                      (outer₀.comp prior₀) (outer₁.comp prior₁)
                    (OriginalF45BracketTree.node later₁ later₂)).map f)) =
                c60F47MixedEval
                  ((c60F59LeftSecondFaceChoice B₀ B₁ hedge hface hrot
                    prior₀ prior₁ outer₀ outer₁ later₁ later₂).map
                    ((c60F60LeftDirectToNested B₀ prior₀ outer₀ later₁ later₂).map f))
              simp only [c60F59LeftSecondFaceChoice,
                c60F58LeftAfterFaceChoice, c60F60LeftDirectToNested,
                c60F56ContextMixedFunctor_fullNative]
              calc
                _ = c60F47MixedEval f := by
                  apply c60F56ContextMixedFunctor_fullNative
                _ = _ := by
                  symm
                  apply c60F56ContextMixedFunctor_fullNative
          _ = _ := (Category.id_comp _).symm)

/-- The original DIRECT one-context F58 Beck–Chevalley NatIso,
whiskered along the genuinely source-typed F60 final normalization.
Its source and target functors match the full pasted route exactly. -/
def c60F61LeftDirectBCNormalizedNatIso
    (hedge : B₀.edge = B₁.edge)
    (hface : c60F44FaceThreeEval B₀.faceStep =
      c60F44FaceThreeEval B₁.faceStep)
    (hrot : c60F44OriginalF55Eval B₀.rotationStep =
      c60F44OriginalF55Eval B₁.rotationStep)
    {u₀ u₁ z₀ z₁ : IcosahedralDart}
    (prior₀ : Quiver.Path u₀ v₀) (prior₁ : Quiver.Path u₁ v₁)
    (outer₀ : Quiver.Path z₀ u₀) (outer₁ : Quiver.Path z₁ u₁)
    {k₁ l₁ k₂ l₂ : Nat}
    {mc md : Blocks a b} {pc pd : Blocks x y}
    (later₁ : OriginalF45BracketTree k₁ l₁ mb pb mc pc)
    (later₂ : OriginalF45BracketTree k₂ l₂ mc pc md pd) :
    ((c60F56OriginalLeftMixedContextFunctor B₀ (outer₀.comp prior₀)
      (OriginalF45BracketTree.node later₁ later₂)) ⋙
      (c60F58LeftAfterFaceChoice B₀ B₁ hedge hface hrot
        (outer₀.comp prior₀) (outer₁.comp prior₁)
        (OriginalF45BracketTree.node later₁ later₂))) ⋙
      (c60F60LeftDirectToNested B₁ prior₁ outer₁ later₁ later₂) ≅
    (c60F56ContextMixedFunctor B₀ B₁ hedge hface hrot) ⋙
      ((c60F56OriginalLeftMixedContextFunctor B₁ (outer₁.comp prior₁)
        (OriginalF45BracketTree.node later₁ later₂)) ⋙
        (c60F60LeftDirectToNested B₁ prior₁ outer₁ later₁ later₂)) :=
  Functor.isoWhiskerRight
      (c60F58LeftFaceContext_NatIso B₀ B₁ hedge hface hrot
        (outer₀.comp prior₀) (outer₁.comp prior₁)
        (OriginalF45BracketTree.node later₁ later₂))
      (c60F60LeftDirectToNested B₁ prior₁ outer₁ later₁ later₂) ≪≫
    (c60F56ContextMixedFunctor B₀ B₁ hedge hface hrot).associator
      (c60F56OriginalLeftMixedContextFunctor B₁ (outer₁.comp prior₁)
        (OriginalF45BracketTree.node later₁ later₂))
      (c60F60LeftDirectToNested B₁ prior₁ outer₁ later₁ later₂)

/-- The SECOND route around the same higher cube: first normalize
the direct original F42/F54 square, then paste BOTH original F58
Beck–Chevalley NatIso, and finally undo the target-side source
normalization. No untyped/raw original proof-term equalities. -/
def c60F61LeftPastedBCNormalizedNatIso
    (hedge : B₀.edge = B₁.edge)
    (hface : c60F44FaceThreeEval B₀.faceStep =
      c60F44FaceThreeEval B₁.faceStep)
    (hrot : c60F44OriginalF55Eval B₀.rotationStep =
      c60F44OriginalF55Eval B₁.rotationStep)
    {u₀ u₁ z₀ z₁ : IcosahedralDart}
    (prior₀ : Quiver.Path u₀ v₀) (prior₁ : Quiver.Path u₁ v₁)
    (outer₀ : Quiver.Path z₀ u₀) (outer₁ : Quiver.Path z₁ u₁)
    {k₁ l₁ k₂ l₂ : Nat}
    {mc md : Blocks a b} {pc pd : Blocks x y}
    (later₁ : OriginalF45BracketTree k₁ l₁ mb pb mc pc)
    (later₂ : OriginalF45BracketTree k₂ l₂ mc pc md pd) :
    ((c60F56OriginalLeftMixedContextFunctor B₀ (outer₀.comp prior₀)
      (OriginalF45BracketTree.node later₁ later₂)) ⋙
      (c60F58LeftAfterFaceChoice B₀ B₁ hedge hface hrot
        (outer₀.comp prior₀) (outer₁.comp prior₁)
        (OriginalF45BracketTree.node later₁ later₂))) ⋙
      (c60F60LeftDirectToNested B₁ prior₁ outer₁ later₁ later₂) ≅
    (c60F56ContextMixedFunctor B₀ B₁ hedge hface hrot) ⋙
      ((c60F56OriginalLeftMixedContextFunctor B₁ (outer₁.comp prior₁)
        (OriginalF45BracketTree.node later₁ later₂)) ⋙
        (c60F60LeftDirectToNested B₁ prior₁ outer₁ later₁ later₂)) := by
  let DL := c60F56OriginalLeftMixedContextFunctor B₀
    (outer₀.comp prior₀) (OriginalF45BracketTree.node later₁ later₂)
  let DR := c60F56OriginalLeftMixedContextFunctor B₁
    (outer₁.comp prior₁) (OriginalF45BracketTree.node later₁ later₂)
  let T₀ := c60F56ContextMixedFunctor B₀ B₁ hedge hface hrot
  let Q := c60F58LeftAfterFaceChoice B₀ B₁ hedge hface hrot
    (outer₀.comp prior₀) (outer₁.comp prior₁)
    (OriginalF45BracketTree.node later₁ later₂)
  let N₀ := c60F60LeftDirectToNested B₀ prior₀ outer₀ later₁ later₂
  let N₁ := c60F60LeftDirectToNested B₁ prior₁ outer₁ later₁ later₂
  let T₂ := c60F59LeftSecondFaceChoice B₀ B₁ hedge hface hrot
    prior₀ prior₁ outer₀ outer₁ later₁ later₂
  exact
    (DL.associator Q N₁) ≪≫
      DL.isoWhiskerLeft
        (c60F61LeftFaceChoiceDirectNestedNatIso B₀ B₁ hedge hface hrot
          prior₀ prior₁ outer₀ outer₁ later₁ later₂) ≪≫
      (DL.associator N₀ T₂).symm ≪≫
      Functor.isoWhiskerRight
        (c60F60LeftDirectVsNestedNatIso B₀
          prior₀ outer₀ later₁ later₂) T₂ ≪≫
      (c60F59LeftTwoContextNatIso B₀ B₁ hedge hface hrot
        prior₀ prior₁ outer₀ outer₁ later₁ later₂) ≪≫
      T₀.isoWhiskerLeft
        (c60F60LeftDirectVsNestedNatIso B₁
          prior₁ outer₁ later₁ later₂).symm

/-- The two genuinely different SOURCE constructions of the BC cube
give the same NATURAL ISOMORPHISM after exact original source
normalization. This is equality of 3-Hom categorical data, not
unquotiented F42/F54 raw proof syntax or global physical descent. -/
theorem c60F61LeftDirectBC_eq_pastedBC
    (hedge : B₀.edge = B₁.edge)
    (hface : c60F44FaceThreeEval B₀.faceStep =
      c60F44FaceThreeEval B₁.faceStep)
    (hrot : c60F44OriginalF55Eval B₀.rotationStep =
      c60F44OriginalF55Eval B₁.rotationStep)
    {u₀ u₁ z₀ z₁ : IcosahedralDart}
    (prior₀ : Quiver.Path u₀ v₀) (prior₁ : Quiver.Path u₁ v₁)
    (outer₀ : Quiver.Path z₀ u₀) (outer₁ : Quiver.Path z₁ u₁)
    {k₁ l₁ k₂ l₂ : Nat}
    {mc md : Blocks a b} {pc pd : Blocks x y}
    (later₁ : OriginalF45BracketTree k₁ l₁ mb pb mc pc)
    (later₂ : OriginalF45BracketTree k₂ l₂ mc pc md pd) :
    c60F61LeftDirectBCNormalizedNatIso B₀ B₁ hedge hface hrot
      prior₀ prior₁ outer₀ outer₁ later₁ later₂ =
    c60F61LeftPastedBCNormalizedNatIso B₀ B₁ hedge hface hrot
      prior₀ prior₁ outer₀ outer₁ later₁ later₂ := by
  apply Iso.ext
  apply NatTrans.ext
  funext X
  cases X <;>
    (apply c60F47MixedGrayFunctor_faithful
      (c60F60LeftNestedFrame B₁ prior₁ outer₁ later₁ later₂)
     simp [c60F47MixedEval, c60F47MixedEval_comp,
       c60F47MixedEval_of,
       c60F61LeftDirectBCNormalizedNatIso,
      c60F61LeftPastedBCNormalizedNatIso,
      c60F61LeftFaceChoiceDirectNestedNatIso,
      c60F59LeftTwoContextNatIso,
      c60F59TwoContextPasting,
      c60F58LeftFaceContext_NatIso,
      c60F60LeftDirectVsNestedNatIso,
      c60F56OriginalLeftMixedContextFunctor,
      c60F56ContextMixedPoint,
      c60F56ContextMixedFunctor,
      c60F58LeftAfterFaceChoice,
      c60F59LeftSecondFaceChoice,
      c60F60LeftDirectToNested])

#print axioms c60F61LeftFaceChoiceDirectNestedNatIso
#print axioms c60F61LeftDirectBCNormalizedNatIso
#print axioms c60F61LeftPastedBCNormalizedNatIso
#print axioms c60F61LeftDirectBC_eq_pastedBC

end OriginalLeftBeckChevalleyCube
end
end KUOS.DependentOriginationGrayC60F55DirectPastedBeckChevalleyV5_210
