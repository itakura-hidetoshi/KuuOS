import KUOS.DependentOriginationCoherentBiadjunctionHorizontalExchangeNonstrictMatesV5_131

namespace KUOS.DependentOriginationCoherentBiadjunctionActualLiftHorizontalExchangeV5_131

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionHorizontalExchangeMateModificationV5_131.Generic
open KUOS.DependentOriginationCoherentBiadjunctionHorizontalExchangeNonstrictMatesV5_131.Generic
open KUOS.DependentOriginationCoherentBiadjunctionHorizontalQuotientFunctorsV5_127.Generic
open KUOS.DependentOriginationCoherentBiadjunctionCompressionKernelQuotientCategoryV5_125.Generic
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactLiftableActualLiftSourceUnitV5_50
open KUOS.DependentOriginationExactLiftableActualLiftTargetCounitV5_49
open KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58
open KUOS.DependentOriginationCoherentBiadjunctionArbitraryModificationMatesV5_113

set_option autoImplicit false
noncomputable section

/-!
# F34/v5.131 — ORIGINAL source η / target ε mixed-whiskering naturality

The full F34 NATURAL mixed horizontal comparison exchange is
specialized for the original source-unit η and target-counit ε.
Six formulations retain the precise original F/G orientation:
original modification squares, mapId corrections, and mapComp corrections.
No replacement roundtrip, no new adjunctions, and no G inverse.
-/

universe u v uH vH uW uP
variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-- ORIGINAL SOURCE η/ε F34 mixed left/right exchange:
genuine lax right-mate modification naturality on arbitrary quotient paths.
The original F 2-ISO and arbitrary G 2-cell remain oriented as given. -/
def actualLiftSourceHorizontalExchangeMateNaturality
    (Γ : Pseudofunctor.StrongTrans.Modification (actualLiftSourceRoundtripUnit.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) (actualLiftSourceRoundtripUnit.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
    {X Y : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel} (f : X ⟶ Y)
    {aF bF aG bG : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel}
    (uF : X ⟶ aF) (uG : ((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj X ⟶ aG)
    (vF : bF ⟶ Y) (vG : bG ⟶ ((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj Y)
    {x y : compressionKernelCategory aF bF aG bG}
    (q : x ⟶ y)
    (basePath :
      (⟨⟨f, ((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).map f⟩⟩ :
        compressionKernelCategory X Y ((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj X ((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj Y) ⟶
      ((leftKernelQuotientWhiskerFunctor aF bF aG bG uF uG ⋙
        rightKernelQuotientWhiskerFunctor X bF
          ((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj X bG vF vG).obj x)) :=
  horizontalExchangeOriginalMateModificationNaturality
    (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) Γ f uF uG vF vG q basePath

/-- ORIGINAL SOURCE η/ε F34 mixed left/right exchange:
nonstrict original mapId correction and both unchanged mate boundaries.
The original F 2-ISO and arbitrary G 2-cell remain oriented as given. -/
def actualLiftSourceHorizontalExchangeMapIdMateNaturality
    (Γ : Pseudofunctor.StrongTrans.Modification (actualLiftSourceRoundtripUnit.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) (actualLiftSourceRoundtripUnit.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
    (X : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)
    {aF bF aG bG : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel}
    (uF : X ⟶ aF) (uG : ((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj X ⟶ aG)
    (vF : bF ⟶ X) (vG : bG ⟶ ((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj X)
    {x y : compressionKernelCategory aF bF aG bG}
    (q : x ⟶ y)
    (basePath :
      (⟨⟨𝟙 X, 𝟙 (((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj X)⟩⟩ :
        compressionKernelCategory X X ((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj X ((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj X) ⟶
      ((leftKernelQuotientWhiskerFunctor aF bF aG bG uF uG ⋙
        rightKernelQuotientWhiskerFunctor X bF
          ((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj X bG vF vG).obj x)) :=
  originalMapIdHorizontalExchangeMateNaturality
    (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) Γ X uF uG vF vG q basePath

/-- ORIGINAL SOURCE η/ε F34 mixed left/right exchange:
nonstrict original mapComp correction and both unchanged mate boundaries.
The original F 2-ISO and arbitrary G 2-cell remain oriented as given. -/
def actualLiftSourceHorizontalExchangeMapCompMateNaturality
    (Γ : Pseudofunctor.StrongTrans.Modification (actualLiftSourceRoundtripUnit.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) (actualLiftSourceRoundtripUnit.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
    {X Y Z : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel} (f : X ⟶ Y) (g : Y ⟶ Z)
    {aF bF aG bG : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel}
    (uF : X ⟶ aF) (uG : ((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj X ⟶ aG)
    (vF : bF ⟶ Z) (vG : bG ⟶ ((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj Z)
    {x y : compressionKernelCategory aF bF aG bG}
    (q : x ⟶ y)
    (basePath :
      (⟨⟨f ≫ g, ((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).map f ≫ ((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).map g⟩⟩ :
        compressionKernelCategory X Z ((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj X ((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj Z) ⟶
      ((leftKernelQuotientWhiskerFunctor aF bF aG bG uF uG ⋙
        rightKernelQuotientWhiskerFunctor X bF
          ((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj X bG vF vG).obj x)) :=
  originalMapCompHorizontalExchangeMateNaturality
    (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) Γ f g uF uG vF vG q basePath

/-- ORIGINAL TARGET η/ε F34 mixed left/right exchange:
genuine lax right-mate modification naturality on arbitrary quotient paths.
The original F 2-ISO and arbitrary G 2-cell remain oriented as given. -/
def actualLiftTargetHorizontalExchangeMateNaturality
    (Γ : Pseudofunctor.StrongTrans.Modification (actualLiftTargetRoundtripCounit.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) (actualLiftTargetRoundtripCounit.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
    {X Y : ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel} (f : X ⟶ Y)
    {aF bF aG bG : ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel}
    (uF : ((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj X ⟶ aF) (uG : X ⟶ aG)
    (vF : bF ⟶ ((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj Y) (vG : bG ⟶ Y)
    {x y : compressionKernelCategory aF bF aG bG}
    (q : x ⟶ y)
    (basePath :
      (⟨⟨((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).map f, f⟩⟩ :
        compressionKernelCategory ((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj X ((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj Y X Y) ⟶
      ((leftKernelQuotientWhiskerFunctor aF bF aG bG uF uG ⋙
        rightKernelQuotientWhiskerFunctor ((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj X bF
          X bG vF vG).obj x)) :=
  horizontalExchangeOriginalMateModificationNaturality
    (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) Γ f uF uG vF vG q basePath

/-- ORIGINAL TARGET η/ε F34 mixed left/right exchange:
nonstrict original mapId correction and both unchanged mate boundaries.
The original F 2-ISO and arbitrary G 2-cell remain oriented as given. -/
def actualLiftTargetHorizontalExchangeMapIdMateNaturality
    (Γ : Pseudofunctor.StrongTrans.Modification (actualLiftTargetRoundtripCounit.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) (actualLiftTargetRoundtripCounit.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
    (X : ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)
    {aF bF aG bG : ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel}
    (uF : ((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj X ⟶ aF) (uG : X ⟶ aG)
    (vF : bF ⟶ ((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj X) (vG : bG ⟶ X)
    {x y : compressionKernelCategory aF bF aG bG}
    (q : x ⟶ y)
    (basePath :
      (⟨⟨𝟙 (((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj X), 𝟙 X⟩⟩ :
        compressionKernelCategory ((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj X ((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj X X X) ⟶
      ((leftKernelQuotientWhiskerFunctor aF bF aG bG uF uG ⋙
        rightKernelQuotientWhiskerFunctor ((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj X bF
          X bG vF vG).obj x)) :=
  originalMapIdHorizontalExchangeMateNaturality
    (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) Γ X uF uG vF vG q basePath

/-- ORIGINAL TARGET η/ε F34 mixed left/right exchange:
nonstrict original mapComp correction and both unchanged mate boundaries.
The original F 2-ISO and arbitrary G 2-cell remain oriented as given. -/
def actualLiftTargetHorizontalExchangeMapCompMateNaturality
    (Γ : Pseudofunctor.StrongTrans.Modification (actualLiftTargetRoundtripCounit.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) (actualLiftTargetRoundtripCounit.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
    {X Y Z : ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel} (f : X ⟶ Y) (g : Y ⟶ Z)
    {aF bF aG bG : ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel}
    (uF : ((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj X ⟶ aF) (uG : X ⟶ aG)
    (vF : bF ⟶ ((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj Z) (vG : bG ⟶ Z)
    {x y : compressionKernelCategory aF bF aG bG}
    (q : x ⟶ y)
    (basePath :
      (⟨⟨((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).map f ≫ ((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).map g, f ≫ g⟩⟩ :
        compressionKernelCategory ((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj X ((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj Z X Z) ⟶
      ((leftKernelQuotientWhiskerFunctor aF bF aG bG uF uG ⋙
        rightKernelQuotientWhiskerFunctor ((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).obj X bF
          X bG vF vG).obj x)) :=
  originalMapCompHorizontalExchangeMateNaturality
    (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) Γ f g uF uG vF vG q basePath
#print axioms actualLiftSourceHorizontalExchangeMateNaturality
#print axioms actualLiftSourceHorizontalExchangeMapIdMateNaturality
#print axioms actualLiftSourceHorizontalExchangeMapCompMateNaturality
#print axioms actualLiftTargetHorizontalExchangeMateNaturality
#print axioms actualLiftTargetHorizontalExchangeMapIdMateNaturality
#print axioms actualLiftTargetHorizontalExchangeMapCompMateNaturality

end

end KUOS.DependentOriginationCoherentBiadjunctionActualLiftHorizontalExchangeV5_131
