import KUOS.DependentOriginationCoherentBiadjunctionStagewiseHexagonMateNaturalityV5_132

namespace KUOS.DependentOriginationCoherentBiadjunctionActualLiftStagewiseHexagonV5_132

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionStagewiseHexagonMateNaturalityV5_132.Generic
open KUOS.DependentOriginationCoherentBiadjunctionCompressionKernelQuotientCategoryV5_125.Generic
open KUOS.DependentOriginationCoherentBiadjunctionHorizontalQuotientFunctorsV5_127.Generic
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactLiftableActualLiftSourceUnitV5_50
open KUOS.DependentOriginationExactLiftableActualLiftTargetCounitV5_49
open KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58
open KUOS.DependentOriginationCoherentBiadjunctionArbitraryModificationMatesV5_113

set_option autoImplicit false
noncomputable section

/-!
# F35/v5.132 — original source eta and target epsilon on the four-stage HEXAGON

All SIX specializations retain full explicit quantification of original
external 1-cells, arbitrary F28 quotient-category arrows and original
non-strict mapId/mapComp boundary inputs. A partial application of
the generic theorem without these arguments cannot infer the implicit
objects (aF/bF/aG/bG/eF/eG) in Lean 4, because the result type itself
does not determine them. We therefore bind them explicitly rather than
inserting arbitrary identities, assumptions or chosen adjunctions.

Source: F = original identity, G = original roundtrip.
Target: F = original roundtrip, G = original identity.
Chosen lax right mates and G-side potentially noninvertible 2-cells
remain exactly as in F14/F29/F34.
-/

universe u v uH vH uW uP
variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}


/-- The original SOURCE General four-stage hexagon
mate naturality, for EVERY explicitly quantified pair of external
left/right 1-cells and arbitrary original F28 quotient-category arrow.
No G-side comparison inverse, strictification or new adjunction. -/
def actualLiftSourceStagewiseHexagonGeneralMateNaturality
    (Γ : Pseudofunctor.StrongTrans.Modification
      (actualLiftSourceRoundtripUnit.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) (actualLiftSourceRoundtripUnit.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)))
    {X Y : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel} (f : X ⟶ Y)
    {aF bF aG bG eF eG : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel}
    (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (vF : X ⟶ eF) (vG : ((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).obj X) ⟶ eG)
    (wF : bF ⟶ Y) (wG : bG ⟶ ((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).obj Y))
    {x y : compressionKernelCategory aF bF aG bG}
    (q : x ⟶ y)
    (basePath :
      (⟨⟨f, (actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).map f⟩⟩ :
        compressionKernelCategory X Y
          ((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).obj X) ((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).obj Y)) ⟶
      ((leftKernelQuotientWhiskerFunctor aF bF aG bG
        (vF ≫ uF) (vG ≫ uG) ⋙
        rightKernelQuotientWhiskerFunctor X bF
          ((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).obj X) bG wF wG).obj x)) :=
  kernelStagewiseHexagonOriginalMateNaturality
    (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) Γ f
    uF uG vF vG wF wG q basePath

/-- The original SOURCE MapId four-stage hexagon
mate naturality, for EVERY explicitly quantified pair of external
left/right 1-cells and arbitrary original F28 quotient-category arrow.
No G-side comparison inverse, strictification or new adjunction. -/
def actualLiftSourceStagewiseHexagonMapIdMateNaturality
    (Γ : Pseudofunctor.StrongTrans.Modification
      (actualLiftSourceRoundtripUnit.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) (actualLiftSourceRoundtripUnit.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)))
    (X : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)
    {aF bF aG bG eF eG : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel}
    (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (vF : X ⟶ eF) (vG : ((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).obj X) ⟶ eG)
    (wF : bF ⟶ X) (wG : bG ⟶ ((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).obj X))
    {x y : compressionKernelCategory aF bF aG bG}
    (q : x ⟶ y)
    (basePath :
      (⟨⟨𝟙 (X), 𝟙 (((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).obj X))⟩⟩ :
        compressionKernelCategory X X
          ((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).obj X) ((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).obj X)) ⟶
      ((leftKernelQuotientWhiskerFunctor aF bF aG bG
        (vF ≫ uF) (vG ≫ uG) ⋙
        rightKernelQuotientWhiskerFunctor X bF
          ((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).obj X) bG wF wG).obj x)) :=
  kernelStagewiseHexagonOriginalMapIdMateNaturality
    (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) Γ X
    uF uG vF vG wF wG q basePath

/-- The original SOURCE MapComp four-stage hexagon
mate naturality, for EVERY explicitly quantified pair of external
left/right 1-cells and arbitrary original F28 quotient-category arrow.
No G-side comparison inverse, strictification or new adjunction. -/
def actualLiftSourceStagewiseHexagonMapCompMateNaturality
    (Γ : Pseudofunctor.StrongTrans.Modification
      (actualLiftSourceRoundtripUnit.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) (actualLiftSourceRoundtripUnit.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)))
    {X Y Z : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel} (f : X ⟶ Y) (g : Y ⟶ Z)
    {aF bF aG bG eF eG : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel}
    (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (vF : X ⟶ eF) (vG : ((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).obj X) ⟶ eG)
    (wF : bF ⟶ Z) (wG : bG ⟶ ((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).obj Z))
    {x y : compressionKernelCategory aF bF aG bG}
    (q : x ⟶ y)
    (basePath :
      (⟨⟨f ≫ g, (actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).map f ≫ (actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).map g⟩⟩ :
        compressionKernelCategory X Z
          ((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).obj X) ((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).obj Z)) ⟶
      ((leftKernelQuotientWhiskerFunctor aF bF aG bG
        (vF ≫ uF) (vG ≫ uG) ⋙
        rightKernelQuotientWhiskerFunctor X bF
          ((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).obj X) bG wF wG).obj x)) :=
  kernelStagewiseHexagonOriginalMapCompMateNaturality
    (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) Γ f g
    uF uG vF vG wF wG q basePath

/-- The original TARGET General four-stage hexagon
mate naturality, for EVERY explicitly quantified pair of external
left/right 1-cells and arbitrary original F28 quotient-category arrow.
No G-side comparison inverse, strictification or new adjunction. -/
def actualLiftTargetStagewiseHexagonGeneralMateNaturality
    (Γ : Pseudofunctor.StrongTrans.Modification
      (actualLiftTargetRoundtripCounit.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) (actualLiftTargetRoundtripCounit.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)))
    {X Y : ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel} (f : X ⟶ Y)
    {aF bF aG bG eF eG : ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel}
    (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (vF : ((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).obj X) ⟶ eF) (vG : X ⟶ eG)
    (wF : bF ⟶ ((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).obj Y)) (wG : bG ⟶ Y)
    {x y : compressionKernelCategory aF bF aG bG}
    (q : x ⟶ y)
    (basePath :
      (⟨⟨(actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).map f, f⟩⟩ :
        compressionKernelCategory ((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).obj X) ((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).obj Y)
          X Y) ⟶
      ((leftKernelQuotientWhiskerFunctor aF bF aG bG
        (vF ≫ uF) (vG ≫ uG) ⋙
        rightKernelQuotientWhiskerFunctor ((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).obj X) bF
          X bG wF wG).obj x)) :=
  kernelStagewiseHexagonOriginalMateNaturality
    (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) Γ f
    uF uG vF vG wF wG q basePath

/-- The original TARGET MapId four-stage hexagon
mate naturality, for EVERY explicitly quantified pair of external
left/right 1-cells and arbitrary original F28 quotient-category arrow.
No G-side comparison inverse, strictification or new adjunction. -/
def actualLiftTargetStagewiseHexagonMapIdMateNaturality
    (Γ : Pseudofunctor.StrongTrans.Modification
      (actualLiftTargetRoundtripCounit.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) (actualLiftTargetRoundtripCounit.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)))
    (X : ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)
    {aF bF aG bG eF eG : ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel}
    (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (vF : ((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).obj X) ⟶ eF) (vG : X ⟶ eG)
    (wF : bF ⟶ ((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).obj X)) (wG : bG ⟶ X)
    {x y : compressionKernelCategory aF bF aG bG}
    (q : x ⟶ y)
    (basePath :
      (⟨⟨𝟙 (((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).obj X)), 𝟙 (X)⟩⟩ :
        compressionKernelCategory ((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).obj X) ((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).obj X)
          X X) ⟶
      ((leftKernelQuotientWhiskerFunctor aF bF aG bG
        (vF ≫ uF) (vG ≫ uG) ⋙
        rightKernelQuotientWhiskerFunctor ((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).obj X) bF
          X bG wF wG).obj x)) :=
  kernelStagewiseHexagonOriginalMapIdMateNaturality
    (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) Γ X
    uF uG vF vG wF wG q basePath

/-- The original TARGET MapComp four-stage hexagon
mate naturality, for EVERY explicitly quantified pair of external
left/right 1-cells and arbitrary original F28 quotient-category arrow.
No G-side comparison inverse, strictification or new adjunction. -/
def actualLiftTargetStagewiseHexagonMapCompMateNaturality
    (Γ : Pseudofunctor.StrongTrans.Modification
      (actualLiftTargetRoundtripCounit.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) (actualLiftTargetRoundtripCounit.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)))
    {X Y Z : ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel} (f : X ⟶ Y) (g : Y ⟶ Z)
    {aF bF aG bG eF eG : ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel}
    (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (vF : ((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).obj X) ⟶ eF) (vG : X ⟶ eG)
    (wF : bF ⟶ ((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).obj Z)) (wG : bG ⟶ Z)
    {x y : compressionKernelCategory aF bF aG bG}
    (q : x ⟶ y)
    (basePath :
      (⟨⟨(actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).map f ≫ (actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).map g, f ≫ g⟩⟩ :
        compressionKernelCategory ((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).obj X) ((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).obj Z)
          X Z) ⟶
      ((leftKernelQuotientWhiskerFunctor aF bF aG bG
        (vF ≫ uF) (vG ≫ uG) ⋙
        rightKernelQuotientWhiskerFunctor ((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).obj X) bF
          X bG wF wG).obj x)) :=
  kernelStagewiseHexagonOriginalMapCompMateNaturality
    (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) Γ f g
    uF uG vF vG wF wG q basePath

#print axioms actualLiftSourceStagewiseHexagonGeneralMateNaturality
#print axioms actualLiftSourceStagewiseHexagonMapIdMateNaturality
#print axioms actualLiftSourceStagewiseHexagonMapCompMateNaturality
#print axioms actualLiftTargetStagewiseHexagonGeneralMateNaturality
#print axioms actualLiftTargetStagewiseHexagonMapIdMateNaturality
#print axioms actualLiftTargetStagewiseHexagonMapCompMateNaturality

end

end KUOS.DependentOriginationCoherentBiadjunctionActualLiftStagewiseHexagonV5_132
