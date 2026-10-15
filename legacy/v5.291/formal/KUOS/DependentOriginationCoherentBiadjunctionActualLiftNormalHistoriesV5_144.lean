import KUOS.DependentOriginationCoherentBiadjunctionOriginalMateNormalHistoriesV5_144
import KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientNonstrictMatesV5_141
import KUOS.DependentOriginationCoherentBiadjunctionActualLiftInterleavedRefinementV5_140
import KUOS.DependentOriginationCoherentBiadjunctionActualLiftFiniteRefinementTracesV5_139

namespace KUOS.DependentOriginationCoherentBiadjunctionActualLiftNormalHistoriesV5_144

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionFiniteHorizontalExchangeV5_133
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137
open KUOS.DependentOriginationCoherentBiadjunctionConstructiveRefinementV5_138
open KUOS.DependentOriginationCoherentBiadjunctionInterleavedRefinementV5_140
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141
open KUOS.DependentOriginationCoherentBiadjunctionActualLiftDoubleBracketedHexagonV5_136
open KUOS.DependentOriginationCoherentBiadjunctionOriginalMateNormalHistoriesV5_144.Generic
open KUOS.DependentOriginationCoherentBiadjunctionOriginalMateNormalHistoriesV5_144.Generic
open KUOS.DependentOriginationCoherentBiadjunctionChosenRightMateCategoriesV5_116.Generic
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
# F47-D / v5.144: ORIGINAL source η and target ε on native F19/F28 histories

Both original actualLift source-unit and target-counit
pseudonatural strong transformations are retained, as are original
chosen objectwise adjunctions, original NONSTRICT F/G mapId/mapComp,
and the ACTUAL right LAX mates. We specialize the F43 explicit
F46 exact classification of native Type-valued F19 modification
and genuine F28 quotient-category histories into SIX actual source/target
general/nonstrict identity/composition theorems.

At each intermediate step only one of the two genuinely different
categories changes; the other axis retains its original carrier.
F47-A/B proves that the two native F19-first/F28-first executions
have the same original F44 generated exchange class; this file
specializes all six actual source/target boundaries to its full histories.

No ambient bicategory biequivalence or prequotient faithfulness.
-/

universe u v uH vH uW uP
variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-- ORIGINAL source η chosen lax mate: arbitrary F19/F28 primitive exchange. -/
def actualLiftSourceNormalHistoriesGeneralMateIndependence
    (modsA modsB : Grid.Blocks
      (actualLiftSourceChosenMatePresentation (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) (actualLiftSourceChosenMatePresentation (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
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
    (pqA pqB : Grid.Blocks x y)
    {n m : Nat}
    (hm : Grid.AxisTrace n modsA modsB)
    (hc : Grid.AxisTrace m pqA pqB)
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
  originalMateNormalHistories
    (Pseudofunctor.id
      (ActualLiftSource.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel))
    (actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel))
    modsA modsB f
    uF uG vF vG wF wG pqA pqB hm hc basePath

/-- ORIGINAL source η: nonstrict mapId under arbitrary primitive exchange. -/
def actualLiftSourceNormalHistoriesMapIdMateIndependence
    (modsA modsB : Grid.Blocks
      (actualLiftSourceChosenMatePresentation (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) (actualLiftSourceChosenMatePresentation (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
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
    (pqA pqB : Grid.Blocks x y)
    {n m : Nat}
    (hm : Grid.AxisTrace n modsA modsB)
    (hc : Grid.AxisTrace m pqA pqB)
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
  originalMapIdNormalHistories
    (Pseudofunctor.id
      (ActualLiftSource.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel))
    (actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel))
    modsA modsB X
    uF uG vF vG wF wG pqA pqB hm hc basePath

/-- ORIGINAL source η: nonstrict mapComp under arbitrary primitive exchange. -/
def actualLiftSourceNormalHistoriesMapCompMateIndependence
    (modsA modsB : Grid.Blocks
      (actualLiftSourceChosenMatePresentation (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) (actualLiftSourceChosenMatePresentation (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
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
    (pqA pqB : Grid.Blocks x y)
    {n m : Nat}
    (hm : Grid.AxisTrace n modsA modsB)
    (hc : Grid.AxisTrace m pqA pqB)
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
  originalMapCompNormalHistories
    (Pseudofunctor.id
      (ActualLiftSource.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel))
    (actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel))
    modsA modsB f g
    uF uG vF vG wF wG pqA pqB hm hc basePath

/-- ORIGINAL target ε chosen lax mate: arbitrary F19/F28 primitive exchange. -/
def actualLiftTargetNormalHistoriesGeneralMateIndependence
    (modsA modsB : Grid.Blocks
      (actualLiftTargetChosenMatePresentation (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) (actualLiftTargetChosenMatePresentation (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
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
    (pqA pqB : Grid.Blocks x y)
    {n m : Nat}
    (hm : Grid.AxisTrace n modsA modsB)
    (hc : Grid.AxisTrace m pqA pqB)
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
  originalMateNormalHistories
    (actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel))
    (Pseudofunctor.id
      (ActualLiftTarget.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel))
    modsA modsB f
    uF uG vF vG wF wG pqA pqB hm hc basePath

/-- ORIGINAL target ε: nonstrict mapId under arbitrary primitive exchange. -/
def actualLiftTargetNormalHistoriesMapIdMateIndependence
    (modsA modsB : Grid.Blocks
      (actualLiftTargetChosenMatePresentation (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) (actualLiftTargetChosenMatePresentation (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
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
    (pqA pqB : Grid.Blocks x y)
    {n m : Nat}
    (hm : Grid.AxisTrace n modsA modsB)
    (hc : Grid.AxisTrace m pqA pqB)
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
  originalMapIdNormalHistories
    (actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel))
    (Pseudofunctor.id
      (ActualLiftTarget.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel))
    modsA modsB X
    uF uG vF vG wF wG pqA pqB hm hc basePath

/-- ORIGINAL target ε: nonstrict mapComp under arbitrary primitive exchange. -/
def actualLiftTargetNormalHistoriesMapCompMateIndependence
    (modsA modsB : Grid.Blocks
      (actualLiftTargetChosenMatePresentation (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) (actualLiftTargetChosenMatePresentation (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
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
    (pqA pqB : Grid.Blocks x y)
    {n m : Nat}
    (hm : Grid.AxisTrace n modsA modsB)
    (hc : Grid.AxisTrace m pqA pqB)
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
  originalMapCompNormalHistories
    (actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel))
    (Pseudofunctor.id
      (ActualLiftTarget.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel))
    modsA modsB f g
    uF uG vF vG wF wG pqA pqB hm hc basePath

#print axioms actualLiftSourceNormalHistoriesGeneralMateIndependence
#print axioms actualLiftSourceNormalHistoriesMapIdMateIndependence
#print axioms actualLiftSourceNormalHistoriesMapCompMateIndependence
#print axioms actualLiftTargetNormalHistoriesGeneralMateIndependence
#print axioms actualLiftTargetNormalHistoriesMapIdMateIndependence
#print axioms actualLiftTargetNormalHistoriesMapCompMateIndependence

end

end KUOS.DependentOriginationCoherentBiadjunctionActualLiftNormalHistoriesV5_144
