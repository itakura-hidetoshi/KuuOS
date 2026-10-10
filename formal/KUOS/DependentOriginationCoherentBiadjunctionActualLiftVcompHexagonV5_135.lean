import KUOS.DependentOriginationCoherentBiadjunctionDoubleFiniteNonstrictMatesV5_135
import KUOS.DependentOriginationCoherentBiadjunctionActualLiftFiniteHexagonV5_134

namespace KUOS.DependentOriginationCoherentBiadjunctionActualLiftVcompHexagonV5_135

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionFiniteHorizontalExchangeV5_133
open KUOS.DependentOriginationCoherentBiadjunctionFiniteHexagonOriginalMatesV5_134.Generic
open KUOS.DependentOriginationCoherentBiadjunctionFiniteHexagonNonstrictMatesV5_134.Generic
open KUOS.DependentOriginationCoherentBiadjunctionChosenRightMateCategoriesV5_116.Generic
open KUOS.DependentOriginationCoherentBiadjunctionAutomaticModificationMatesV5_114.Generic
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
# F38-D/v5.135 — the ORIGINAL source η and target ε, with genuine
StrongTrans.Modification vertical composition and F37 finite hexagons

Γ, deltaMod are unrestricted endomodifications of the unchanged source
unit or target counit. Their original strong vertical composition is
used AS IS. The genuine chosen right-mate lax transformations then
transport this composite in the REVERSE order by F17; independently,
all original F37 finite quotient hexagon equations, mapId and mapComp
comparisons remain valid. No modification component is inverted.
-/

universe u v uH vH uW uP
variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-- Original source η: unrestricted vertical strong-modification composite,
with finite mate naturality hexagon. -/
def actualLiftSourceFiniteStagewiseHexagonVcompGeneralMateNaturality
    (Γ deltaMod : Pseudofunctor.StrongTrans.Modification
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
    (p : Chain.Path x y)
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
  finiteStagewiseHexagonOriginalMateNaturality
    (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) (Pseudofunctor.StrongTrans.Modification.vcomp Γ deltaMod) f
    uF uG vF vG wF wG p basePath

/-- Original source η: unrestricted vertical strong-modification composite,
with finite nonstrict mapId hexagon. -/
def actualLiftSourceFiniteStagewiseHexagonVcompMapIdMateNaturality
    (Γ deltaMod : Pseudofunctor.StrongTrans.Modification
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
    (p : Chain.Path x y)
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
  finiteStagewiseHexagonOriginalMapIdMateNaturality
    (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) (Pseudofunctor.StrongTrans.Modification.vcomp Γ deltaMod) X
    uF uG vF vG wF wG p basePath

/-- Original source η: unrestricted vertical strong-modification composite,
with finite nonstrict mapComp hexagon. -/
def actualLiftSourceFiniteStagewiseHexagonVcompMapCompMateNaturality
    (Γ deltaMod : Pseudofunctor.StrongTrans.Modification
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
    (p : Chain.Path x y)
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
  finiteStagewiseHexagonOriginalMapCompMateNaturality
    (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) (Pseudofunctor.StrongTrans.Modification.vcomp Γ deltaMod) f g
    uF uG vF vG wF wG p basePath

/-- Original target ε: unrestricted vertical strong-modification composite,
with finite mate naturality hexagon. -/
def actualLiftTargetFiniteStagewiseHexagonVcompGeneralMateNaturality
    (Γ deltaMod : Pseudofunctor.StrongTrans.Modification
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
    (p : Chain.Path x y)
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
  finiteStagewiseHexagonOriginalMateNaturality
    (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) (Pseudofunctor.StrongTrans.Modification.vcomp Γ deltaMod) f
    uF uG vF vG wF wG p basePath

/-- Original target ε: unrestricted vertical strong-modification composite,
with finite nonstrict mapId hexagon. -/
def actualLiftTargetFiniteStagewiseHexagonVcompMapIdMateNaturality
    (Γ deltaMod : Pseudofunctor.StrongTrans.Modification
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
    (p : Chain.Path x y)
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
  finiteStagewiseHexagonOriginalMapIdMateNaturality
    (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) (Pseudofunctor.StrongTrans.Modification.vcomp Γ deltaMod) X
    uF uG vF vG wF wG p basePath

/-- Original target ε: unrestricted vertical strong-modification composite,
with finite nonstrict mapComp hexagon. -/
def actualLiftTargetFiniteStagewiseHexagonVcompMapCompMateNaturality
    (Γ deltaMod : Pseudofunctor.StrongTrans.Modification
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
    (p : Chain.Path x y)
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
  finiteStagewiseHexagonOriginalMapCompMateNaturality
    (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) (Pseudofunctor.StrongTrans.Modification.vcomp Γ deltaMod) f g
    uF uG vF vG wF wG p basePath

/-- Full ORIGINAL source right-mate vertical anti-functoriality;
not merely equality after quotient compression or on selected cells. -/
theorem actualLiftSourceFiniteHexagonRightMateVcomp
    (Γ deltaMod : Pseudofunctor.StrongTrans.Modification
    (actualLiftSourceRoundtripUnit.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel))
    (actualLiftSourceRoundtripUnit.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel))) :
    let d := actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)
    rightModification d d
      (Pseudofunctor.StrongTrans.Modification.vcomp Γ deltaMod) =
    Oplax.LaxTrans.Modification.vcomp
      (rightModification d d deltaMod)
      (rightModification d d Γ) := by
  dsimp only
  exact rightModification_vcomp _ _ _ Γ deltaMod

/-- Full ORIGINAL target right-mate vertical anti-functoriality;
not merely equality after quotient compression or on selected cells. -/
theorem actualLiftTargetFiniteHexagonRightMateVcomp
    (Γ deltaMod : Pseudofunctor.StrongTrans.Modification
    (actualLiftTargetRoundtripCounit.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel))
    (actualLiftTargetRoundtripCounit.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel))) :
    let d := actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)
    rightModification d d
      (Pseudofunctor.StrongTrans.Modification.vcomp Γ deltaMod) =
    Oplax.LaxTrans.Modification.vcomp
      (rightModification d d deltaMod)
      (rightModification d d Γ) := by
  dsimp only
  exact rightModification_vcomp _ _ _ Γ deltaMod

#print axioms actualLiftSourceFiniteStagewiseHexagonVcompGeneralMateNaturality
#print axioms actualLiftSourceFiniteStagewiseHexagonVcompMapIdMateNaturality
#print axioms actualLiftSourceFiniteStagewiseHexagonVcompMapCompMateNaturality
#print axioms actualLiftTargetFiniteStagewiseHexagonVcompGeneralMateNaturality
#print axioms actualLiftTargetFiniteStagewiseHexagonVcompMapIdMateNaturality
#print axioms actualLiftTargetFiniteStagewiseHexagonVcompMapCompMateNaturality
#print axioms actualLiftSourceFiniteHexagonRightMateVcomp
#print axioms actualLiftTargetFiniteHexagonRightMateVcomp

end

end KUOS.DependentOriginationCoherentBiadjunctionActualLiftVcompHexagonV5_135
