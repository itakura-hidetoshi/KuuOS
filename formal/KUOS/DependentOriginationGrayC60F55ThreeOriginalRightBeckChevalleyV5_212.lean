import KUOS.DependentOriginationGrayC60F55ThreeOriginalLeftBeckChevalleyV5_212
import KUOS.DependentOriginationGrayC60F55DirectPastedBeckChevalleyV5_210

namespace KUOS.DependentOriginationGrayC60F55ThreeOriginalRightBeckChevalleyV5_212

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
open KUOS.DependentOriginationGrayC60F55TwoContextPhysicalV5_208
open KUOS.DependentOriginationGrayC60F55MixedEndomorphismRigidityV5_210
open KUOS.DependentOriginationGrayC60F55ThreeContextBeckChevalleyV5_212
open KUOS.DependentOriginationGrayC60F55ThreeOriginalLeftBeckChevalleyV5_212
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.212 / F59-F61-B2 — THREE actual ORIGINAL F42/F54 right contexts

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

section ThreeOriginalRightContexts

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
variable (suffix₀ : Quiver.Path w₀ u₀) (suffix₁ : Quiver.Path w₁ u₁)
variable (middle₀ : Quiver.Path u₀ z₀) (middle₁ : Quiver.Path u₁ z₁)
variable (outer₀ : Quiver.Path z₀ t₀) (outer₁ : Quiver.Path z₁ t₁)
variable {k₁ l₁ k₂ l₂ k₃ l₃ : Nat}
variable {mc md me : Blocks a b} {pc pd pe : Blocks x y}
variable (earlier₁ : OriginalF45BracketTree k₁ l₁ mc pc ma pa)
variable (earlier₂ : OriginalF45BracketTree k₂ l₂ md pd mc pc)
variable (earlier₃ : OriginalF45BracketTree k₃ l₃ me pe md pd)

/-- Two *distinct actual source constructions*, each composed of
three F58 Beck–Chevalley NatIso with original F42 right suffix paths and original
F54/F55 independent trees, glued by genuine F59 two-context pasting.

The resulting pair shares exactly the SAME source and target functors.
No equality of unlike original F42/F54 source proof terms is assumed.
-/
def c60F63OriginalRightThreeBCPair :=
  let A₁ := c60F47WhiskerRight B₀ suffix₀ earlier₁
  let B₁' := c60F47WhiskerRight B₁ suffix₁ earlier₁
  let A₂ := c60F47WhiskerRight A₁ middle₀ earlier₂
  let B₂' := c60F47WhiskerRight B₁' middle₁ earlier₂
  let hface₁ := c60F59RightIntermediateFaceNative B₀ B₁
    hface suffix₀ suffix₁ earlier₁
  let hrot₁ := c60F59RightIntermediateRotationNative B₀ B₁
    hrot suffix₀ suffix₁ earlier₁
  let hface₂ := c60F59RightIntermediateFaceNative A₁ B₁'
    hface₁ middle₀ middle₁ earlier₂
  let hrot₂ := c60F59RightIntermediateRotationNative A₁ B₁'
    hrot₁ middle₀ middle₁ earlier₂
  have hedge₁ : A₁.edge = B₁'.edge := by
    change B₀.edge = B₁.edge
    exact hedge
  have hedge₂ : A₂.edge = B₂'.edge := by
    change B₀.edge = B₁.edge
    exact hedge
  let L₀ := c60F56OriginalRightMixedContextFunctor B₀ suffix₀ earlier₁
  let L₁ := c60F56OriginalRightMixedContextFunctor A₁ middle₀ earlier₂
  let L₂ := c60F56OriginalRightMixedContextFunctor A₂ outer₀ earlier₃
  let R₀ := c60F56OriginalRightMixedContextFunctor B₁ suffix₁ earlier₁
  let R₁ := c60F56OriginalRightMixedContextFunctor B₁' middle₁ earlier₂
  let R₂ := c60F56OriginalRightMixedContextFunctor B₂' outer₁ earlier₃
  let P₀ := c60F56ContextMixedFunctor B₀ B₁ hedge hface hrot
  let P₁ := c60F58RightAfterFaceChoice B₀ B₁ hedge hface hrot
    suffix₀ suffix₁ earlier₁
  let P₂ := c60F58RightAfterFaceChoice A₁ B₁' hedge₁ hface₁ hrot₁
    middle₀ middle₁ earlier₂
  let P₃ := c60F58RightAfterFaceChoice A₂ B₂' hedge₂ hface₂ hrot₂
    outer₀ outer₁ earlier₃
  let bc₀ := c60F58RightFaceContext_NatIso B₀ B₁ hedge hface hrot
    suffix₀ suffix₁ earlier₁
  let bc₁ := c60F58RightFaceContext_NatIso A₁ B₁'
    hedge₁ hface₁ hrot₁ middle₀ middle₁ earlier₂
  let bc₂ := c60F58RightFaceContext_NatIso A₂ B₂'
    hedge₂ hface₂ hrot₂ outer₀ outer₁ earlier₃
  (c60F63ThreeBC_firstPair L₀ L₁ L₂ R₀ R₁ R₂
      P₀ P₁ P₂ P₃ bc₀ bc₁ bc₂,
     c60F63ThreeBC_lastPair L₀ L₁ L₂ R₀ R₁ R₂
      P₀ P₁ P₂ P₃ bc₀ bc₁ bc₂)

/-- Three actual independent ORIGINAL C60/F42 path contexts and
original F54/F55 bracket-tree contexts have coherent BC pasting
under both distinct parenthesizations. The conclusion equates actual
Mathlib source NatIso in F47's four-tag full-native-kernel quotient,
not merely native Gray charges or raw F42/F54 proof-term syntax. -/
theorem c60F63OriginalRightThreeBC_coherent :
    (c60F63OriginalRightThreeBCPair B₀ B₁ hedge hface hrot
      suffix₀ suffix₁ middle₀ middle₁ outer₀ outer₁
      earlier₁ earlier₂ earlier₃).1 =
    (c60F63OriginalRightThreeBCPair B₀ B₁ hedge hface hrot
      suffix₀ suffix₁ middle₀ middle₁ outer₀ outer₁
      earlier₁ earlier₂ earlier₃).2 := by
  apply Iso.ext
  apply NatTrans.ext
  funext X
  cases X <;>
    exact c60F61MixedEndomorphism_unique
      (c60F47WhiskerRight
        (c60F47WhiskerRight
          (c60F47WhiskerRight B₁ suffix₁ earlier₁)
          middle₁ earlier₂) outer₁ earlier₃)
      _ _ _

#print axioms c60F63OriginalRightThreeBCPair
#print axioms c60F63OriginalRightThreeBC_coherent

end ThreeOriginalRightContexts
end
end KUOS.DependentOriginationGrayC60F55ThreeOriginalRightBeckChevalleyV5_212
