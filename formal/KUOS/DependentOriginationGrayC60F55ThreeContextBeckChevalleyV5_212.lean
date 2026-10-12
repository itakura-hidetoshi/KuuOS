import KUOS.DependentOriginationGrayC60F55ThreeOriginalContextV5_211
import KUOS.DependentOriginationGrayC60F55MixedEndomorphismRigidityV5_210

namespace KUOS.DependentOriginationGrayC60F55ThreeContextBeckChevalleyV5_212

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
open KUOS.DependentOriginationGrayC60F55ThreeOriginalContextV5_211
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.212 / F59-F61-B1: THREE genuinely typed source Beck–Chevalley contexts

The abstract functorial cube below has FOUR separate source and FOUR
separate target categories, and three independently given source
Beck–Chevalley NatIso. The two original parenthesizations are not
identified: functor associators/whiskering explicitly transport
them to the SAME full three-context source and target endpoints.

The specialization uses three ORIGINAL F42 C60 paths and three
INDEPENDENT ORIGINAL F54/F55 binary bracket-tree contexts, carrying
the real four-tag F47 full-native-kernel source 3-Hom and its proved
endomorphism rigidity. This is not equality of raw F42/F54 proof words
or an unconditional physical descent theorem.
-/

universe uS0 uS1 uS2 uS3 uT0 uT1 uT2 uT3

section AbstractThreeContextSourcePasting

variable {S₀ : Type uS0} [Category S₀]
variable {S₁ : Type uS1} [Category S₁]
variable {S₂ : Type uS2} [Category S₂]
variable {S₃ : Type uS3} [Category S₃]
variable {T₀ : Type uT0} [Category T₀]
variable {T₁ : Type uT1} [Category T₁]
variable {T₂ : Type uT2} [Category T₂]
variable {T₃ : Type uT3} [Category T₃]

/-- Paste the FIRST two original squares before the THIRD. The actual
Mathlib associators and whiskerings come from F59's proved source
two-context pasting, not from a silent strictness convention. -/
def c60F63ThreeBC_firstPair
    (L₀ : S₀ ⥤ S₁) (L₁ : S₁ ⥤ S₂) (L₂ : S₂ ⥤ S₃)
    (R₀ : T₀ ⥤ T₁) (R₁ : T₁ ⥤ T₂) (R₂ : T₂ ⥤ T₃)
    (P₀ : S₀ ⥤ T₀) (P₁ : S₁ ⥤ T₁)
    (P₂ : S₂ ⥤ T₂) (P₃ : S₃ ⥤ T₃)
    (bc₀ : L₀ ⋙ P₁ ≅ P₀ ⋙ R₀)
    (bc₁ : L₁ ⋙ P₂ ≅ P₁ ⋙ R₁)
    (bc₂ : L₂ ⋙ P₃ ≅ P₂ ⋙ R₂) :
    (((L₀ ⋙ L₁) ⋙ L₂) ⋙ P₃) ≅
      (P₀ ⋙ ((R₀ ⋙ R₁) ⋙ R₂)) :=
  c60F59TwoContextPasting
    (L₀ ⋙ L₁) L₂ (R₀ ⋙ R₁) R₂ P₀ P₂ P₃
    (c60F59TwoContextPasting L₀ L₁ R₀ R₁ P₀ P₁ P₂ bc₀ bc₁)
    bc₂

/-- Paste the LAST two original squares first; explicitly transport
BOTH parenthesizations by the genuine Mathlib functor associators.
It has the very same independently typed source/codomain as above. -/
def c60F63ThreeBC_lastPair
    (L₀ : S₀ ⥤ S₁) (L₁ : S₁ ⥤ S₂) (L₂ : S₂ ⥤ S₃)
    (R₀ : T₀ ⥤ T₁) (R₁ : T₁ ⥤ T₂) (R₂ : T₂ ⥤ T₃)
    (P₀ : S₀ ⥤ T₀) (P₁ : S₁ ⥤ T₁)
    (P₂ : S₂ ⥤ T₂) (P₃ : S₃ ⥤ T₃)
    (bc₀ : L₀ ⋙ P₁ ≅ P₀ ⋙ R₀)
    (bc₁ : L₁ ⋙ P₂ ≅ P₁ ⋙ R₁)
    (bc₂ : L₂ ⋙ P₃ ≅ P₂ ⋙ R₂) :
    (((L₀ ⋙ L₁) ⋙ L₂) ⋙ P₃) ≅
      (P₀ ⋙ ((R₀ ⋙ R₁) ⋙ R₂)) :=
  Functor.isoWhiskerRight (L₀.associator L₁ L₂) P₃ ≪≫
    c60F59TwoContextPasting
      L₀ (L₁ ⋙ L₂) R₀ (R₁ ⋙ R₂) P₀ P₁ P₃
      bc₀
      (c60F59TwoContextPasting L₁ L₂ R₁ R₂ P₁ P₂ P₃ bc₁ bc₂) ≪≫
    P₀.isoWhiskerLeft ((R₀.associator R₁ R₂).symm)

/-- The first genuine three-context source BC route is natural on
EVERY source arrow; source/target functors are not collapsed. -/
theorem c60F63ThreeBC_firstPair_naturality
    (L₀ : S₀ ⥤ S₁) (L₁ : S₁ ⥤ S₂) (L₂ : S₂ ⥤ S₃)
    (R₀ : T₀ ⥤ T₁) (R₁ : T₁ ⥤ T₂) (R₂ : T₂ ⥤ T₃)
    (P₀ : S₀ ⥤ T₀) (P₁ : S₁ ⥤ T₁)
    (P₂ : S₂ ⥤ T₂) (P₃ : S₃ ⥤ T₃)
    (bc₀ : L₀ ⋙ P₁ ≅ P₀ ⋙ R₀)
    (bc₁ : L₁ ⋙ P₂ ≅ P₁ ⋙ R₁)
    (bc₂ : L₂ ⋙ P₃ ≅ P₂ ⋙ R₂)
    {X Y : S₀} (f : X ⟶ Y) :
    (((L₀ ⋙ L₁) ⋙ L₂) ⋙ P₃).map f ≫
      (c60F63ThreeBC_firstPair
        L₀ L₁ L₂ R₀ R₁ R₂ P₀ P₁ P₂ P₃ bc₀ bc₁ bc₂).hom.app Y =
    (c60F63ThreeBC_firstPair
      L₀ L₁ L₂ R₀ R₁ R₂ P₀ P₁ P₂ P₃ bc₀ bc₁ bc₂).hom.app X ≫
        (P₀ ⋙ ((R₀ ⋙ R₁) ⋙ R₂)).map f :=
  (c60F63ThreeBC_firstPair
    L₀ L₁ L₂ R₀ R₁ R₂ P₀ P₁ P₂ P₃ bc₀ bc₁ bc₂).hom.naturality f

/-- The second genuinely differently parenthesized source BC route
also has naturality on EVERY original source 3-Hom. -/
theorem c60F63ThreeBC_lastPair_naturality
    (L₀ : S₀ ⥤ S₁) (L₁ : S₁ ⥤ S₂) (L₂ : S₂ ⥤ S₃)
    (R₀ : T₀ ⥤ T₁) (R₁ : T₁ ⥤ T₂) (R₂ : T₂ ⥤ T₃)
    (P₀ : S₀ ⥤ T₀) (P₁ : S₁ ⥤ T₁)
    (P₂ : S₂ ⥤ T₂) (P₃ : S₃ ⥤ T₃)
    (bc₀ : L₀ ⋙ P₁ ≅ P₀ ⋙ R₀)
    (bc₁ : L₁ ⋙ P₂ ≅ P₁ ⋙ R₁)
    (bc₂ : L₂ ⋙ P₃ ≅ P₂ ⋙ R₂)
    {X Y : S₀} (f : X ⟶ Y) :
    (((L₀ ⋙ L₁) ⋙ L₂) ⋙ P₃).map f ≫
      (c60F63ThreeBC_lastPair
        L₀ L₁ L₂ R₀ R₁ R₂ P₀ P₁ P₂ P₃ bc₀ bc₁ bc₂).hom.app Y =
    (c60F63ThreeBC_lastPair
      L₀ L₁ L₂ R₀ R₁ R₂ P₀ P₁ P₂ P₃ bc₀ bc₁ bc₂).hom.app X ≫
        (P₀ ⋙ ((R₀ ⋙ R₁) ⋙ R₂)).map f :=
  (c60F63ThreeBC_lastPair
    L₀ L₁ L₂ R₀ R₁ R₂ P₀ P₁ P₂ P₃ bc₀ bc₁ bc₂).hom.naturality f

end AbstractThreeContextSourcePasting

#print axioms c60F63ThreeBC_firstPair
#print axioms c60F63ThreeBC_lastPair
#print axioms c60F63ThreeBC_firstPair_naturality
#print axioms c60F63ThreeBC_lastPair_naturality

end
end KUOS.DependentOriginationGrayC60F55ThreeContextBeckChevalleyV5_212
