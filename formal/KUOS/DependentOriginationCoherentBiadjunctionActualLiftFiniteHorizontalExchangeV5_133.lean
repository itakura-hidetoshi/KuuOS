import KUOS.DependentOriginationCoherentBiadjunctionFiniteExchangeMateNaturalityV5_133
import KUOS.DependentOriginationCoherentBiadjunctionActualLiftHorizontalExchangeV5_131

namespace KUOS.DependentOriginationCoherentBiadjunctionActualLiftFiniteHorizontalExchangeV5_133

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionFiniteHorizontalExchangeV5_133
open KUOS.DependentOriginationCoherentBiadjunctionFiniteExchangeMateNaturalityV5_133.Generic
open KUOS.DependentOriginationCoherentBiadjunctionHorizontalExchangeNonstrictMatesV5_131.Generic
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactLiftableActualLiftSourceUnitV5_50
open KUOS.DependentOriginationExactLiftableActualLiftTargetCounitV5_49
open KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58
open KUOS.DependentOriginationCoherentBiadjunctionArbitraryModificationMatesV5_113
open KUOS.DependentOriginationCoherentBiadjunctionCompressionKernelQuotientCategoryV5_125.Generic
open KUOS.DependentOriginationCoherentBiadjunctionHorizontalQuotientFunctorsV5_127.Generic

set_option autoImplicit false
noncomputable section

/-!
# F36-D/v5.133: ORIGINAL actual source η and target ε finite paths

Specializations use the exact original roundtrip pseudofunctors and
selected mate data, unchanged source unit/target counit, original
nonstrict mapId/mapComp comparison cells, and the original forward
G-side potentially noninvertible comparison. The parameter is now a
genuine finite path of F28 quotient-category arrows, whose composite
is compatible with both original nonstrict mates.
-/

universe u v uH vH uW uP
variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-- Finite original source η exchange: every native F28 quotient path,
via the F36 inductive naturality theorem, preserves both original mates. -/
def actualLiftSourceFiniteHorizontalExchangeMateNaturality
    (Γ : Pseudofunctor.StrongTrans.Modification (actualLiftSourceRoundtripUnit.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) (actualLiftSourceRoundtripUnit.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
    {X Y : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel} (f : X ⟶ Y)
    {aF bF aG bG : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel}
    (uF : X ⟶ aF) (uG : (((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj X) ⟶ aG)
    (vF : bF ⟶ Y) (vG : bG ⟶ (((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj Y))
    {x y : compressionKernelCategory aF bF aG bG}
    (p : Chain.Path x y)
    (basePath :
      (⟨⟨f, ((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).map f⟩⟩ :
        compressionKernelCategory X Y (((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj X) (((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj Y)) ⟶
      ((leftKernelQuotientWhiskerFunctor aF bF aG bG uF uG ⋙
        rightKernelQuotientWhiskerFunctor X bF
          (((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj X) bG vF vG).obj x)) :=
  finiteHorizontalExchangeOriginalMateNaturality
    (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) Γ f uF uG vF vG p basePath

/-- Finite source η with ORIGINAL nonstrict mapId cells unchanged. -/
def actualLiftSourceFiniteHorizontalExchangeMapIdMateNaturality
    (Γ : Pseudofunctor.StrongTrans.Modification (actualLiftSourceRoundtripUnit.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) (actualLiftSourceRoundtripUnit.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
    (X : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)
    {aF bF aG bG : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel}
    (uF : X ⟶ aF) (uG : (((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj X) ⟶ aG)
    (vF : bF ⟶ X) (vG : bG ⟶ (((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj X))
    {x y : compressionKernelCategory aF bF aG bG}
    (p : Chain.Path x y)
    (basePath :
      (⟨⟨𝟙 X, 𝟙 ((((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj X))⟩⟩ :
        compressionKernelCategory X X (((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj X) (((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj X)) ⟶
      ((leftKernelQuotientWhiskerFunctor aF bF aG bG uF uG ⋙
        rightKernelQuotientWhiskerFunctor X bF
          (((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj X) bG vF vG).obj x)) :=
  originalMapIdHorizontalExchangeMateNaturality
    (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) Γ X uF uG vF vG p.composite basePath

/-- Finite source η with ORIGINAL nonstrict mapComp cells unchanged. -/
def actualLiftSourceFiniteHorizontalExchangeMapCompMateNaturality
    (Γ : Pseudofunctor.StrongTrans.Modification (actualLiftSourceRoundtripUnit.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) (actualLiftSourceRoundtripUnit.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
    {X Y Z : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel} (f : X ⟶ Y) (g : Y ⟶ Z)
    {aF bF aG bG : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel}
    (uF : X ⟶ aF) (uG : (((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj X) ⟶ aG)
    (vF : bF ⟶ Z) (vG : bG ⟶ (((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj Z))
    {x y : compressionKernelCategory aF bF aG bG}
    (p : Chain.Path x y)
    (basePath :
      (⟨⟨f ≫ g, ((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).map f ≫ ((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).map g⟩⟩ :
        compressionKernelCategory X Z (((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj X) (((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj Z)) ⟶
      ((leftKernelQuotientWhiskerFunctor aF bF aG bG uF uG ⋙
        rightKernelQuotientWhiskerFunctor X bF
          (((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj X) bG vF vG).obj x)) :=
  originalMapCompHorizontalExchangeMateNaturality
    (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) Γ f g uF uG vF vG p.composite basePath

/-- Finite original target ε exchange: every native F28 quotient path,
via the F36 inductive naturality theorem, preserves both original mates. -/
def actualLiftTargetFiniteHorizontalExchangeMateNaturality
    (Γ : Pseudofunctor.StrongTrans.Modification (actualLiftTargetRoundtripCounit.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) (actualLiftTargetRoundtripCounit.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
    {X Y : ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel} (f : X ⟶ Y)
    {aF bF aG bG : ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel}
    (uF : (((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj X) ⟶ aF) (uG : X ⟶ aG)
    (vF : bF ⟶ (((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj Y)) (vG : bG ⟶ Y)
    {x y : compressionKernelCategory aF bF aG bG}
    (p : Chain.Path x y)
    (basePath :
      (⟨⟨((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).map f, f⟩⟩ :
        compressionKernelCategory (((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj X) (((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj Y) X Y) ⟶
      ((leftKernelQuotientWhiskerFunctor aF bF aG bG uF uG ⋙
        rightKernelQuotientWhiskerFunctor (((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj X) bF
          X bG vF vG).obj x)) :=
  finiteHorizontalExchangeOriginalMateNaturality
    (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) Γ f uF uG vF vG p basePath

/-- Finite target ε with ORIGINAL nonstrict mapId cells unchanged. -/
def actualLiftTargetFiniteHorizontalExchangeMapIdMateNaturality
    (Γ : Pseudofunctor.StrongTrans.Modification (actualLiftTargetRoundtripCounit.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) (actualLiftTargetRoundtripCounit.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
    (X : ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)
    {aF bF aG bG : ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel}
    (uF : (((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj X) ⟶ aF) (uG : X ⟶ aG)
    (vF : bF ⟶ (((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj X)) (vG : bG ⟶ X)
    {x y : compressionKernelCategory aF bF aG bG}
    (p : Chain.Path x y)
    (basePath :
      (⟨⟨𝟙 ((((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj X)), 𝟙 X⟩⟩ :
        compressionKernelCategory (((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj X) (((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj X) X X) ⟶
      ((leftKernelQuotientWhiskerFunctor aF bF aG bG uF uG ⋙
        rightKernelQuotientWhiskerFunctor (((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj X) bF
          X bG vF vG).obj x)) :=
  originalMapIdHorizontalExchangeMateNaturality
    (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) Γ X uF uG vF vG p.composite basePath

/-- Finite target ε with ORIGINAL nonstrict mapComp cells unchanged. -/
def actualLiftTargetFiniteHorizontalExchangeMapCompMateNaturality
    (Γ : Pseudofunctor.StrongTrans.Modification (actualLiftTargetRoundtripCounit.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) (actualLiftTargetRoundtripCounit.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
    {X Y Z : ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel} (f : X ⟶ Y) (g : Y ⟶ Z)
    {aF bF aG bG : ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel}
    (uF : (((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj X) ⟶ aF) (uG : X ⟶ aG)
    (vF : bF ⟶ (((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj Z)) (vG : bG ⟶ Z)
    {x y : compressionKernelCategory aF bF aG bG}
    (p : Chain.Path x y)
    (basePath :
      (⟨⟨((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).map f ≫ ((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).map g, f ≫ g⟩⟩ :
        compressionKernelCategory (((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj X) (((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj Z) X Z) ⟶
      ((leftKernelQuotientWhiskerFunctor aF bF aG bG uF uG ⋙
        rightKernelQuotientWhiskerFunctor (((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj X) bF
          X bG vF vG).obj x)) :=
  originalMapCompHorizontalExchangeMateNaturality
    (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) Γ f g uF uG vF vG p.composite basePath

#print axioms actualLiftSourceFiniteHorizontalExchangeMateNaturality
#print axioms actualLiftSourceFiniteHorizontalExchangeMapIdMateNaturality
#print axioms actualLiftSourceFiniteHorizontalExchangeMapCompMateNaturality
#print axioms actualLiftTargetFiniteHorizontalExchangeMateNaturality
#print axioms actualLiftTargetFiniteHorizontalExchangeMapIdMateNaturality
#print axioms actualLiftTargetFiniteHorizontalExchangeMapCompMateNaturality

end

end KUOS.DependentOriginationCoherentBiadjunctionActualLiftFiniteHorizontalExchangeV5_133
