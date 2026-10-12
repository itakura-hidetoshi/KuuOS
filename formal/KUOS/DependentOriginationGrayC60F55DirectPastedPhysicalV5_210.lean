import KUOS.DependentOriginationGrayC60F55DirectPastedBeckChevalleyV5_210

namespace KUOS.DependentOriginationGrayC60F55DirectPastedPhysicalV5_210

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
open KUOS.DependentOriginationGrayC60F55TwoContextPhysicalV5_208
open KUOS.DependentOriginationGrayC60F55DirectCompositeContextV5_209
open KUOS.DependentOriginationGrayC60F55DirectCompositePhysicalV5_209
open KUOS.DependentOriginationGrayC60F55DirectPastedBeckChevalleyV5_210
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.210 / F59-F60-C — SOURCE RIGHT Beck–Chevalley direct-vs-pasted cube

RIGHT original F42/F54 Beck–Chevalley NatIso from F58; F59 gives its
two-successive-original-context pasting, and F60 gives genuinely
concatenated original F42 Quiver.Path + original F54 bracket-tree
node/direct-versus-nested normalization. The present module compares
the RIGHT two resulting source NatIso in a common correctly typed F47
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

section OriginalRightBeckChevalleyCube

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
original F42 suffix concatenation and original F54 earlier-tree direct node
versus original F42/F54 RIGHT-nested contextualization. Both are true
source Mathlib functors on the four F47 tags. -/
def c60F61RightFaceChoiceDirectNestedNatIso
    (hedge : B₀.edge = B₁.edge)
    (hface : c60F44FaceThreeEval B₀.faceStep =
      c60F44FaceThreeEval B₁.faceStep)
    (hrot : c60F44OriginalF55Eval B₀.rotationStep =
      c60F44OriginalF55Eval B₁.rotationStep)
    {u₀ u₁ z₀ z₁ : IcosahedralDart}
    (suffix₀ : Quiver.Path w₀ u₀) (suffix₁ : Quiver.Path w₁ u₁)
    (outer₀ : Quiver.Path u₀ z₀) (outer₁ : Quiver.Path u₁ z₁)
    {k₁ l₁ k₂ l₂ : Nat}
    {mc md : Blocks a b} {pc pd : Blocks x y}
    (earlier₁ : OriginalF45BracketTree k₁ l₁ mc pc ma pa)
    (earlier₂ : OriginalF45BracketTree k₂ l₂ md pd mc pc) :
    (c60F58RightAfterFaceChoice B₀ B₁ hedge hface hrot
        (suffix₀.comp outer₀) (suffix₁.comp outer₁)
        (OriginalF45BracketTree.node earlier₂ earlier₁)) ⋙
      (c60F60RightDirectToNested B₁ suffix₁ outer₁ earlier₁ earlier₂) ≅
    (c60F60RightDirectToNested B₀ suffix₀ outer₀ earlier₁ earlier₂) ⋙
      (c60F59RightSecondFaceChoice B₀ B₁ hedge hface hrot
        suffix₀ suffix₁ outer₀ outer₁ earlier₁ earlier₂) :=
  NatIso.ofComponents
    (fun X => by cases X <;> exact Iso.refl _)
    (by
      intro X Y f
      cases X <;> cases Y
      all_goals
        calc
          _ = ((c60F58RightAfterFaceChoice B₀ B₁ hedge hface hrot
                (suffix₀.comp outer₀) (suffix₁.comp outer₁)
                    (OriginalF45BracketTree.node earlier₂ earlier₁)) ⋙
                (c60F60RightDirectToNested B₁ suffix₁ outer₁ earlier₁ earlier₂)).map f :=
              Category.comp_id _
          _ = ((c60F60RightDirectToNested B₀ suffix₀ outer₀ earlier₁ earlier₂) ⋙
                (c60F59RightSecondFaceChoice B₀ B₁ hedge hface hrot
                  suffix₀ suffix₁ outer₀ outer₁ earlier₁ earlier₂)).map f := by
              apply c60F47MixedGrayFunctor_faithful
                (c60F60RightNestedFrame B₁ suffix₁ outer₁ earlier₁ earlier₂)
              change c60F47MixedEval
                  ((c60F60RightDirectToNested B₁ suffix₁ outer₁ earlier₁ earlier₂).map
                    ((c60F58RightAfterFaceChoice B₀ B₁ hedge hface hrot
                      (suffix₀.comp outer₀) (suffix₁.comp outer₁)
                    (OriginalF45BracketTree.node earlier₂ earlier₁)).map f)) =
                c60F47MixedEval
                  ((c60F59RightSecondFaceChoice B₀ B₁ hedge hface hrot
                    suffix₀ suffix₁ outer₀ outer₁ earlier₁ earlier₂).map
                    ((c60F60RightDirectToNested B₀ suffix₀ outer₀ earlier₁ earlier₂).map f))
              simp only [c60F59RightSecondFaceChoice,
                c60F58RightAfterFaceChoice, c60F60RightDirectToNested,
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
def c60F61RightDirectBCNormalizedNatIso
    (hedge : B₀.edge = B₁.edge)
    (hface : c60F44FaceThreeEval B₀.faceStep =
      c60F44FaceThreeEval B₁.faceStep)
    (hrot : c60F44OriginalF55Eval B₀.rotationStep =
      c60F44OriginalF55Eval B₁.rotationStep)
    {u₀ u₁ z₀ z₁ : IcosahedralDart}
    (suffix₀ : Quiver.Path w₀ u₀) (suffix₁ : Quiver.Path w₁ u₁)
    (outer₀ : Quiver.Path u₀ z₀) (outer₁ : Quiver.Path u₁ z₁)
    {k₁ l₁ k₂ l₂ : Nat}
    {mc md : Blocks a b} {pc pd : Blocks x y}
    (earlier₁ : OriginalF45BracketTree k₁ l₁ mc pc ma pa)
    (earlier₂ : OriginalF45BracketTree k₂ l₂ md pd mc pc) :
    ((c60F56OriginalRightMixedContextFunctor B₀ (suffix₀.comp outer₀)
      (OriginalF45BracketTree.node earlier₂ earlier₁)) ⋙
      (c60F58RightAfterFaceChoice B₀ B₁ hedge hface hrot
        (suffix₀.comp outer₀) (suffix₁.comp outer₁)
        (OriginalF45BracketTree.node earlier₂ earlier₁))) ⋙
      (c60F60RightDirectToNested B₁ suffix₁ outer₁ earlier₁ earlier₂) ≅
    (c60F56ContextMixedFunctor B₀ B₁ hedge hface hrot) ⋙
      ((c60F56OriginalRightMixedContextFunctor B₁ (suffix₁.comp outer₁)
        (OriginalF45BracketTree.node earlier₂ earlier₁)) ⋙
        (c60F60RightDirectToNested B₁ suffix₁ outer₁ earlier₁ earlier₂)) :=
  Functor.isoWhiskerRight
      (c60F58RightFaceContext_NatIso B₀ B₁ hedge hface hrot
        (suffix₀.comp outer₀) (suffix₁.comp outer₁)
        (OriginalF45BracketTree.node earlier₂ earlier₁))
      (c60F60RightDirectToNested B₁ suffix₁ outer₁ earlier₁ earlier₂) ≪≫
    (c60F56ContextMixedFunctor B₀ B₁ hedge hface hrot).associator
      (c60F56OriginalRightMixedContextFunctor B₁ (suffix₁.comp outer₁)
        (OriginalF45BracketTree.node earlier₂ earlier₁))
      (c60F60RightDirectToNested B₁ suffix₁ outer₁ earlier₁ earlier₂)

/-- The SECOND route around the same higher cube: first normalize
the direct original F42/F54 square, then paste BOTH original F58
Beck–Chevalley NatIso, and finally undo the target-side source
normalization. No untyped/raw original proof-term equalities. -/
def c60F61RightPastedBCNormalizedNatIso
    (hedge : B₀.edge = B₁.edge)
    (hface : c60F44FaceThreeEval B₀.faceStep =
      c60F44FaceThreeEval B₁.faceStep)
    (hrot : c60F44OriginalF55Eval B₀.rotationStep =
      c60F44OriginalF55Eval B₁.rotationStep)
    {u₀ u₁ z₀ z₁ : IcosahedralDart}
    (suffix₀ : Quiver.Path w₀ u₀) (suffix₁ : Quiver.Path w₁ u₁)
    (outer₀ : Quiver.Path u₀ z₀) (outer₁ : Quiver.Path u₁ z₁)
    {k₁ l₁ k₂ l₂ : Nat}
    {mc md : Blocks a b} {pc pd : Blocks x y}
    (earlier₁ : OriginalF45BracketTree k₁ l₁ mc pc ma pa)
    (earlier₂ : OriginalF45BracketTree k₂ l₂ md pd mc pc) :
    ((c60F56OriginalRightMixedContextFunctor B₀ (suffix₀.comp outer₀)
      (OriginalF45BracketTree.node earlier₂ earlier₁)) ⋙
      (c60F58RightAfterFaceChoice B₀ B₁ hedge hface hrot
        (suffix₀.comp outer₀) (suffix₁.comp outer₁)
        (OriginalF45BracketTree.node earlier₂ earlier₁))) ⋙
      (c60F60RightDirectToNested B₁ suffix₁ outer₁ earlier₁ earlier₂) ≅
    (c60F56ContextMixedFunctor B₀ B₁ hedge hface hrot) ⋙
      ((c60F56OriginalRightMixedContextFunctor B₁ (suffix₁.comp outer₁)
        (OriginalF45BracketTree.node earlier₂ earlier₁)) ⋙
        (c60F60RightDirectToNested B₁ suffix₁ outer₁ earlier₁ earlier₂)) := by
  let DL := c60F56OriginalRightMixedContextFunctor B₀
    (suffix₀.comp outer₀) (OriginalF45BracketTree.node earlier₂ earlier₁)
  let DR := c60F56OriginalRightMixedContextFunctor B₁
    (suffix₁.comp outer₁) (OriginalF45BracketTree.node earlier₂ earlier₁)
  let T₀ := c60F56ContextMixedFunctor B₀ B₁ hedge hface hrot
  let Q := c60F58RightAfterFaceChoice B₀ B₁ hedge hface hrot
    (suffix₀.comp outer₀) (suffix₁.comp outer₁)
    (OriginalF45BracketTree.node earlier₂ earlier₁)
  let N₀ := c60F60RightDirectToNested B₀ suffix₀ outer₀ earlier₁ earlier₂
  let N₁ := c60F60RightDirectToNested B₁ suffix₁ outer₁ earlier₁ earlier₂
  let T₂ := c60F59RightSecondFaceChoice B₀ B₁ hedge hface hrot
    suffix₀ suffix₁ outer₀ outer₁ earlier₁ earlier₂
  exact
    (DL.associator Q N₁) ≪≫
      DL.isoWhiskerLeft
        (c60F61RightFaceChoiceDirectNestedNatIso B₀ B₁ hedge hface hrot
          suffix₀ suffix₁ outer₀ outer₁ earlier₁ earlier₂) ≪≫
      (DL.associator N₀ T₂).symm ≪≫
      Functor.isoWhiskerRight
        (c60F60RightDirectVsNestedNatIso B₀
          suffix₀ outer₀ earlier₁ earlier₂) T₂ ≪≫
      (c60F59RightTwoContextNatIso B₀ B₁ hedge hface hrot
        suffix₀ suffix₁ outer₀ outer₁ earlier₁ earlier₂) ≪≫
      T₀.isoWhiskerLeft
        (c60F60RightDirectVsNestedNatIso B₁
          suffix₁ outer₁ earlier₁ earlier₂).symm

/-- The two genuinely different SOURCE constructions of the BC cube
give the same NATURAL ISOMORPHISM after exact original source
normalization. This is equality of 3-Hom categorical data, not
unquotiented F42/F54 raw proof syntax or global physical descent. -/
theorem c60F61RightDirectBC_eq_pastedBC
    (hedge : B₀.edge = B₁.edge)
    (hface : c60F44FaceThreeEval B₀.faceStep =
      c60F44FaceThreeEval B₁.faceStep)
    (hrot : c60F44OriginalF55Eval B₀.rotationStep =
      c60F44OriginalF55Eval B₁.rotationStep)
    {u₀ u₁ z₀ z₁ : IcosahedralDart}
    (suffix₀ : Quiver.Path w₀ u₀) (suffix₁ : Quiver.Path w₁ u₁)
    (outer₀ : Quiver.Path u₀ z₀) (outer₁ : Quiver.Path u₁ z₁)
    {k₁ l₁ k₂ l₂ : Nat}
    {mc md : Blocks a b} {pc pd : Blocks x y}
    (earlier₁ : OriginalF45BracketTree k₁ l₁ mc pc ma pa)
    (earlier₂ : OriginalF45BracketTree k₂ l₂ md pd mc pc) :
    c60F61RightDirectBCNormalizedNatIso B₀ B₁ hedge hface hrot
      suffix₀ suffix₁ outer₀ outer₁ earlier₁ earlier₂ =
    c60F61RightPastedBCNormalizedNatIso B₀ B₁ hedge hface hrot
      suffix₀ suffix₁ outer₀ outer₁ earlier₁ earlier₂ := by
  apply Iso.ext
  apply NatTrans.ext
  funext X
  cases X <;>
    (apply c60F47MixedGrayFunctor_faithful
      (c60F60RightNestedFrame B₁ suffix₁ outer₁ earlier₁ earlier₂)
     dsimp only [
       c60F61RightDirectBCNormalizedNatIso,
       c60F61RightPastedBCNormalizedNatIso,
       c60F61RightFaceChoiceDirectNestedNatIso,
       c60F59RightTwoContextNatIso,
       c60F59TwoContextPasting,
       c60F58RightFaceContext_NatIso,
       c60F60RightDirectVsNestedNatIso]
     simp only [Iso.trans_hom, NatTrans.comp_app]
     simp [c60F56OriginalRightMixedContextFunctor,
       c60F56ContextMixedPoint,
       c60F56ContextMixedFunctor,
       c60F58RightAfterFaceChoice,
       c60F59RightSecondFaceChoice,
       c60F60RightDirectToNested,
       c60F47MixedGrayFunctor, c60F47MixedCategory,
       c60F47MixedEval, c60F47MixedComp,
       c60F47MixedOf, c60F56ContextMixedRaw,
       C60F47PresentedMixedThreeCell.toNative])
#print axioms c60F61RightFaceChoiceDirectNestedNatIso
#print axioms c60F61RightDirectBCNormalizedNatIso
#print axioms c60F61RightPastedBCNormalizedNatIso
#print axioms c60F61RightDirectBC_eq_pastedBC

end OriginalRightBeckChevalleyCube
end
end KUOS.DependentOriginationGrayC60F55DirectPastedPhysicalV5_210
