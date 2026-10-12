import KUOS.DependentOriginationGrayC60F55ThreeContextBeckChevalleyV5_212
import KUOS.DependentOriginationGrayC60F55DirectPastedBeckChevalleyV5_210

namespace KUOS.DependentOriginationGrayC60F55ThreeOriginalLeftBeckChevalleyV5_212

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
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
open KUOS.DependentOriginationGrayC60F55MixedEndomorphismRigidityV5_210
open KUOS.DependentOriginationGrayC60F55ThreeContextBeckChevalleyV5_212
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.212 / F59-F61-B2 — THREE actual ORIGINAL F42/F54 left contexts

This specializes the two genuinely different triple-BC Mathlib
NatIso constructions to actual source F47 mixed FOUR-TAG categories.
Each of the THREE original C60 prior Quiver.Paths and each of the
THREE independent ORIGINAL F54/F55 binary bracket trees remains
typed, with all intermediate F43 face and old F55 Gray comparisons.

The two distinct parenthesizations are equal as source NATURAL
ISOMORPHISMS in the chosen full-native-kernel F47 source quotient,
using the previously theorem-proved uniqueness of tagged endomorphisms.
There is no raw unquotiented F42/F54 syntax equality and no physical
global descent assertion.
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section ThreeOriginalLeftContexts

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
variable (hedge : B₀.edge = B₁.edge)
variable (hface : c60F44FaceThreeEval B₀.faceStep =
  c60F44FaceThreeEval B₁.faceStep)
variable (hrot : c60F44OriginalF55Eval B₀.rotationStep =
  c60F44OriginalF55Eval B₁.rotationStep)
variable {u₀ u₁ z₀ z₁ t₀ t₁ : IcosahedralDart}
variable (prior₀ : Quiver.Path u₀ v₀) (prior₁ : Quiver.Path u₁ v₁)
variable (middle₀ : Quiver.Path z₀ u₀) (middle₁ : Quiver.Path z₁ u₁)
variable (outer₀ : Quiver.Path t₀ z₀) (outer₁ : Quiver.Path t₁ z₁)
variable {k₁ l₁ k₂ l₂ k₃ l₃ : Nat}
variable {mc md me : Blocks a b} {pc pd pe : Blocks x y}
variable (later₁ : OriginalF45BracketTree k₁ l₁ mb pb mc pc)
variable (later₂ : OriginalF45BracketTree k₂ l₂ mc pc md pd)
variable (later₃ : OriginalF45BracketTree k₃ l₃ md pd me pe)

/-- Two *distinct actual source constructions*, each composed of
three F58 Beck–Chevalley NatIso with original F42 paths and original
F54/F55 independent trees, glued by genuine F59 two-context pasting.

The resulting pair shares exactly the SAME source and target functors.
No equality of unlike original F42/F54 source proof terms is assumed.
-/
def c60F63OriginalLeftThreeBCPair := by
  let A₁ := c60F47WhiskerLeft B₀ prior₀ later₁
  let B₁' := c60F47WhiskerLeft B₁ prior₁ later₁
  let A₂ := c60F47WhiskerLeft A₁ middle₀ later₂
  let B₂' := c60F47WhiskerLeft B₁' middle₁ later₂
  let hface₁ := c60F59LeftIntermediateFaceNative B₀ B₁
    hface prior₀ prior₁ later₁
  let hrot₁ := c60F59LeftIntermediateRotationNative B₀ B₁
    hrot prior₀ prior₁ later₁
  let hface₂ := c60F59LeftIntermediateFaceNative A₁ B₁'
    hface₁ middle₀ middle₁ later₂
  let hrot₂ := c60F59LeftIntermediateRotationNative A₁ B₁'
    hrot₁ middle₀ middle₁ later₂
  have hedge₁ : A₁.edge = B₁'.edge := by
    change B₀.edge = B₁.edge
    exact hedge
  have hedge₂ : A₂.edge = B₂'.edge := by
    change B₀.edge = B₁.edge
    exact hedge
  let L₀ := c60F56OriginalLeftMixedContextFunctor B₀ prior₀ later₁
  let L₁ := c60F56OriginalLeftMixedContextFunctor A₁ middle₀ later₂
  let L₂ := c60F56OriginalLeftMixedContextFunctor A₂ outer₀ later₃
  let R₀ := c60F56OriginalLeftMixedContextFunctor B₁ prior₁ later₁
  let R₁ := c60F56OriginalLeftMixedContextFunctor B₁' middle₁ later₂
  let R₂ := c60F56OriginalLeftMixedContextFunctor B₂' outer₁ later₃
  let P₀ := c60F56ContextMixedFunctor B₀ B₁ hedge hface hrot
  let P₁ := c60F58LeftAfterFaceChoice B₀ B₁ hedge hface hrot
    prior₀ prior₁ later₁
  let P₂ := c60F58LeftAfterFaceChoice A₁ B₁' hedge₁ hface₁ hrot₁
    middle₀ middle₁ later₂
  let P₃ := c60F58LeftAfterFaceChoice A₂ B₂' hedge₂ hface₂ hrot₂
    outer₀ outer₁ later₃
  let bc₀ := c60F58LeftFaceContext_NatIso B₀ B₁ hedge hface hrot
    prior₀ prior₁ later₁
  let bc₁ := c60F58LeftFaceContext_NatIso A₁ B₁'
    hedge₁ hface₁ hrot₁ middle₀ middle₁ later₂
  let bc₂ := c60F58LeftFaceContext_NatIso A₂ B₂'
    hedge₂ hface₂ hrot₂ outer₀ outer₁ later₃
  exact show
    ((((L₀ ⋙ L₁) ⋙ L₂) ⋙ P₃) ≅ (P₀ ⋙ ((R₀ ⋙ R₁) ⋙ R₂))) ×
    ((((L₀ ⋙ L₁) ⋙ L₂) ⋙ P₃) ≅ (P₀ ⋙ ((R₀ ⋙ R₁) ⋙ R₂))) from
      (c60F63ThreeBC_firstPair L₀ L₁ L₂ R₀ R₁ R₂
      P₀ P₁ P₂ P₃ bc₀ bc₁ bc₂,
     c60F63ThreeBC_lastPair L₀ L₁ L₂ R₀ R₁ R₂
      P₀ P₁ P₂ P₃ bc₀ bc₁ bc₂)

/-- Three actual independent ORIGINAL C60/F42 path contexts and
original F54/F55 bracket-tree contexts have coherent BC pasting
under both distinct parenthesizations. The conclusion equates actual
Mathlib source NatIso in F47's four-tag full-native-kernel quotient,
not merely native Gray charges or raw F42/F54 proof-term syntax. -/
theorem c60F63OriginalLeftThreeBC_coherent :
    (c60F63OriginalLeftThreeBCPair B₀ B₁ hedge hface hrot
      prior₀ prior₁ middle₀ middle₁ outer₀ outer₁
      later₁ later₂ later₃).1 =
    (c60F63OriginalLeftThreeBCPair B₀ B₁ hedge hface hrot
      prior₀ prior₁ middle₀ middle₁ outer₀ outer₁
      later₁ later₂ later₃).2 := by
  apply Iso.ext
  apply NatTrans.ext
  funext X
  cases X <;>
    exact c60F61MixedEndomorphism_unique
      (c60F47WhiskerLeft
        (c60F47WhiskerLeft
          (c60F47WhiskerLeft B₁ prior₁ later₁)
          middle₁ later₂) outer₁ later₃)
      _ _ _

#print axioms c60F63OriginalLeftThreeBCPair
#print axioms c60F63OriginalLeftThreeBC_coherent

end ThreeOriginalLeftContexts
end
end KUOS.DependentOriginationGrayC60F55ThreeOriginalLeftBeckChevalleyV5_212
