import KUOS.DependentOriginationGrayC60F55PhysicalIncidenceBeckChevalleyV5_207

namespace KUOS.DependentOriginationGrayC60F55TwoContextBeckChevalleyV5_208

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
open KUOS.DependentOriginationGrayC60F55PhysicalIncidenceBeckChevalleyV5_207
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.208 / F59-F59-A: two successive genuinely typed original contexts

F58 established actual SOURCE Beck–Chevalley NatIso for independently
typed original F42 C60 Quiver.Paths and independent F54/F55 bracket-tree
contexts. Here we explicitly paste two such squares, retaining the real
source four-boundary F47 categories at all six vertices of the diagram.
The three associators below are Mathlib functor associators, not an
implicit identification of the original F42/F54 word syntax.

The new comparison remains in the full-native-kernel F47 quotient.
It neither produces a tenth original F55 constructor nor implies global
physical descent or a raw-source Gray 3-category.
-/

universe uS0 uS1 uS2 uT0 uT1 uT2

section AbstractTypedTwoStepPasting

variable {S₀ : Type uS0} [Category S₀]
variable {S₁ : Type uS1} [Category S₁]
variable {S₂ : Type uS2} [Category S₂]
variable {T₀ : Type uT0} [Category T₀]
variable {T₁ : Type uT1} [Category T₁]
variable {T₂ : Type uT2} [Category T₂]

/-- True two-step pasting of SOURCE natural isomorphisms; the explicit
associators matter when adjacent presentations carry dependent types. -/
def c60F59TwoContextPasting
    (L₀ : S₀ ⥤ S₁) (L₁ : S₁ ⥤ S₂)
    (R₀ : T₀ ⥤ T₁) (R₁ : T₁ ⥤ T₂)
    (P₀ : S₀ ⥤ T₀) (P₁ : S₁ ⥤ T₁) (P₂ : S₂ ⥤ T₂)
    (bc₀ : L₀ ⋙ P₁ ≅ P₀ ⋙ R₀)
    (bc₁ : L₁ ⋙ P₂ ≅ P₁ ⋙ R₁) :
    (L₀ ⋙ L₁) ⋙ P₂ ≅ P₀ ⋙ (R₀ ⋙ R₁) :=
  (L₀.associator L₁ P₂) ≪≫
    L₀.isoWhiskerLeft bc₁ ≪≫
    (L₀.associator P₁ R₁).symm ≪≫
    Functor.isoWhiskerRight bc₀ R₁ ≪≫
    P₀.associator R₀ R₁

/-- The pasted cube acts naturally on *all* source 3-Hom arrows.
This equation retains its typed boundary objects and does not collapse
the underlying original source 2-cell terms. -/
theorem c60F59TwoContextPasting_naturality
    (L₀ : S₀ ⥤ S₁) (L₁ : S₁ ⥤ S₂)
    (R₀ : T₀ ⥤ T₁) (R₁ : T₁ ⥤ T₂)
    (P₀ : S₀ ⥤ T₀) (P₁ : S₁ ⥤ T₁) (P₂ : S₂ ⥤ T₂)
    (bc₀ : L₀ ⋙ P₁ ≅ P₀ ⋙ R₀)
    (bc₁ : L₁ ⋙ P₂ ≅ P₁ ⋙ R₁)
    {X Y : S₀} (f : X ⟶ Y) :
    ((L₀ ⋙ L₁) ⋙ P₂).map f ≫
        (c60F59TwoContextPasting L₀ L₁ R₀ R₁ P₀ P₁ P₂ bc₀ bc₁).hom.app Y =
      (c60F59TwoContextPasting L₀ L₁ R₀ R₁ P₀ P₁ P₂ bc₀ bc₁).hom.app X ≫
        (P₀ ⋙ (R₀ ⋙ R₁)).map f :=
  (c60F59TwoContextPasting L₀ L₁ R₀ R₁ P₀ P₁ P₂ bc₀ bc₁).hom.naturality f

end AbstractTypedTwoStepPasting

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section TwoSuccessiveOriginalLeftContexts

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

/-- The first physical left F42 path and original F54 later tree preserve
equality of the COMPLETE source-native F43 images for the two frames. -/
theorem c60F59LeftIntermediateFaceNative
    (hface : c60F44FaceThreeEval B₀.faceStep =
      c60F44FaceThreeEval B₁.faceStep)
    {u₀ u₁ : IcosahedralDart}
    (prior₀ : Quiver.Path u₀ v₀) (prior₁ : Quiver.Path u₁ v₁)
    {k₁ l₁ : Nat} {mc : Blocks a b} {pc : Blocks x y}
    (later₁ : OriginalF45BracketTree k₁ l₁ mb pb mc pc) :
    c60F44FaceThreeEval
        (c60F47WhiskerLeft B₀ prior₀ later₁).faceStep =
      c60F44FaceThreeEval
        (c60F47WhiskerLeft B₁ prior₁ later₁).faceStep := by
  calc
    c60F44FaceThreeEval (c60F47WhiskerLeft B₀ prior₀ later₁).faceStep =
        c60F44FaceThreeEval B₀.faceStep :=
      c60F45LeftWhiskerGrayMap prior₀ B₀.faceStep
    _ = c60F44FaceThreeEval B₁.faceStep := hface
    _ = c60F44FaceThreeEval
        (c60F47WhiskerLeft B₁ prior₁ later₁).faceStep :=
      (c60F45LeftWhiskerGrayMap prior₁ B₁.faceStep).symm

/-- The independent original F54/F55 first-stage left context also
preserves the entire native F55 evaluator, including the second charge. -/
theorem c60F59LeftIntermediateRotationNative
    (hrot : c60F44OriginalF55Eval B₀.rotationStep =
      c60F44OriginalF55Eval B₁.rotationStep)
    {u₀ u₁ : IcosahedralDart}
    (prior₀ : Quiver.Path u₀ v₀) (prior₁ : Quiver.Path u₁ v₁)
    {k₁ l₁ : Nat} {mc : Blocks a b} {pc : Blocks x y}
    (later₁ : OriginalF45BracketTree k₁ l₁ mb pb mc pc) :
    c60F44OriginalF55Eval
        (c60F47WhiskerLeft B₀ prior₀ later₁).rotationStep =
      c60F44OriginalF55Eval
        (c60F47WhiskerLeft B₁ prior₁ later₁).rotationStep := by
  calc
    c60F44OriginalF55Eval (c60F47WhiskerLeft B₀ prior₀ later₁).rotationStep =
        c60F44OriginalF55Eval B₀.rotationStep :=
      c60F45F55LeftContextGrayMap later₁ B₀.rotationStep
    _ = c60F44OriginalF55Eval B₁.rotationStep := hrot
    _ = c60F44OriginalF55Eval
        (c60F47WhiskerLeft B₁ prior₁ later₁).rotationStep :=
      (c60F45F55LeftContextGrayMap later₁ B₁.rotationStep).symm

/-- The SECOND original context square uses the genuinely transported
F42/F54 source frames, not fabricated equalities of raw F42 and F54. -/
def c60F59LeftSecondFaceChoice
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
    C60F47BoundaryPoint
        (c60F47WhiskerLeft (c60F47WhiskerLeft B₀ prior₀ later₁)
          outer₀ later₂) ⥤
      C60F47BoundaryPoint
        (c60F47WhiskerLeft (c60F47WhiskerLeft B₁ prior₁ later₁)
          outer₁ later₂) :=
  c60F58LeftAfterFaceChoice
    (c60F47WhiskerLeft B₀ prior₀ later₁)
    (c60F47WhiskerLeft B₁ prior₁ later₁)
    (by change B₀.edge = B₁.edge; exact hedge)
    (c60F59LeftIntermediateFaceNative B₀ B₁ hface prior₀ prior₁ later₁)
    (c60F59LeftIntermediateRotationNative B₀ B₁ hrot prior₀ prior₁ later₁)
    outer₀ outer₁ later₂

/-- TWO genuine original F42 prior paths on each side, followed by
TWO separately typed independent F54 bracket-tree context operations.
The resulting pasting is a source NatIso between the final full F47
three-Hom categories, with the original four boundary tags retained. -/
def c60F59LeftTwoContextNatIso
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
    ((c60F56OriginalLeftMixedContextFunctor B₀ prior₀ later₁) ⋙
      (c60F56OriginalLeftMixedContextFunctor
        (c60F47WhiskerLeft B₀ prior₀ later₁) outer₀ later₂)) ⋙
      (c60F59LeftSecondFaceChoice B₀ B₁ hedge hface hrot
        prior₀ prior₁ outer₀ outer₁ later₁ later₂) ≅
    (c60F56ContextMixedFunctor B₀ B₁ hedge hface hrot) ⋙
      ((c60F56OriginalLeftMixedContextFunctor B₁ prior₁ later₁) ⋙
        (c60F56OriginalLeftMixedContextFunctor
          (c60F47WhiskerLeft B₁ prior₁ later₁) outer₁ later₂)) := by
  let B₀' := c60F47WhiskerLeft B₀ prior₀ later₁
  let B₁' := c60F47WhiskerLeft B₁ prior₁ later₁
  let hedge' : B₀'.edge = B₁'.edge := by
    change B₀.edge = B₁.edge
    exact hedge
  let hface' : c60F44FaceThreeEval B₀'.faceStep =
      c60F44FaceThreeEval B₁'.faceStep :=
    c60F59LeftIntermediateFaceNative B₀ B₁ hface prior₀ prior₁ later₁
  let hrot' : c60F44OriginalF55Eval B₀'.rotationStep =
      c60F44OriginalF55Eval B₁'.rotationStep :=
    c60F59LeftIntermediateRotationNative B₀ B₁ hrot prior₀ prior₁ later₁
  exact c60F59TwoContextPasting
    (c60F56OriginalLeftMixedContextFunctor B₀ prior₀ later₁)
    (c60F56OriginalLeftMixedContextFunctor B₀' outer₀ later₂)
    (c60F56OriginalLeftMixedContextFunctor B₁ prior₁ later₁)
    (c60F56OriginalLeftMixedContextFunctor B₁' outer₁ later₂)
    (c60F56ContextMixedFunctor B₀ B₁ hedge hface hrot)
    (c60F58LeftAfterFaceChoice B₀ B₁ hedge hface hrot
      prior₀ prior₁ later₁)
    (c60F58LeftAfterFaceChoice B₀' B₁' hedge' hface' hrot'
      outer₀ outer₁ later₂)
    (c60F58LeftFaceContext_NatIso B₀ B₁ hedge hface hrot
      prior₀ prior₁ later₁)
    (c60F58LeftFaceContext_NatIso B₀' B₁' hedge' hface' hrot'
      outer₀ outer₁ later₂)

end TwoSuccessiveOriginalLeftContexts

#print axioms c60F59TwoContextPasting
#print axioms c60F59TwoContextPasting_naturality
#print axioms c60F59LeftIntermediateFaceNative
#print axioms c60F59LeftIntermediateRotationNative
#print axioms c60F59LeftSecondFaceChoice
#print axioms c60F59LeftTwoContextNatIso

end KUOS.DependentOriginationGrayC60F55TwoContextBeckChevalleyV5_208
