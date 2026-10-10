import KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientNonstrictMatesV5_141
import KUOS.DependentOriginationCoherentBiadjunctionActualLiftInterleavedRefinementV5_140
import KUOS.DependentOriginationCoherentBiadjunctionActualLiftFiniteRefinementTracesV5_139

namespace KUOS.DependentOriginationCoherentBiadjunctionActualLiftExchangeQuotientV5_141

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionFiniteHorizontalExchangeV5_133
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137
open KUOS.DependentOriginationCoherentBiadjunctionConstructiveRefinementV5_138
open KUOS.DependentOriginationCoherentBiadjunctionInterleavedRefinementV5_140
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141
open KUOS.DependentOriginationCoherentBiadjunctionActualLiftDoubleBracketedHexagonV5_136
open KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientMateCoherenceV5_141.Generic
open KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientNonstrictMatesV5_141.Generic
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
# F44-E / v5.141: ORIGINAL source η and target ε along ANY interleaving

Both original actualLift source-unit and target-counit
pseudonatural strong transformations are retained, as are original
chosen objectwise adjunctions, original NONSTRICT F/G mapId/mapComp,
and the ACTUAL right LAX mates. We specialize the F43 explicit
Interleaving n m of primitive F19 modification and F28 quotient-
comparison refinements into SIX fully typed original source/target
general/nonstrict identity/composition theorems.

At each intermediate step only one of the two genuinely different
categories changes; the other axis retains its original carrier.
Any arbitrary finite exchange order works, including mod-first and
comparison-first, without adding G comparison inverses.

No ambient bicategory biequivalence or prequotient faithfulness.
-/

universe u v uH vH uW uP
variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-- ORIGINAL source η chosen lax mate: arbitrary F19/F28 primitive exchange. -/
def actualLiftSourceExchangeQuotientGeneralMateIndependence
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
    (exchange : Grid.ExchangeClass n m modsA modsB pqA pqB)
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
  exchangeQuotientOriginalMate
    (Pseudofunctor.id
      (ActualLiftSource.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel))
    (actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel))
    modsA modsB f
    uF uG vF vG wF wG pqA pqB exchange basePath

/-- ORIGINAL source η: nonstrict mapId under arbitrary primitive exchange. -/
def actualLiftSourceExchangeQuotientMapIdMateIndependence
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
    (exchange : Grid.ExchangeClass n m modsA modsB pqA pqB)
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
  exchangeQuotientOriginalMapId
    (Pseudofunctor.id
      (ActualLiftSource.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel))
    (actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel))
    modsA modsB X
    uF uG vF vG wF wG pqA pqB exchange basePath

/-- ORIGINAL source η: nonstrict mapComp under arbitrary primitive exchange. -/
def actualLiftSourceExchangeQuotientMapCompMateIndependence
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
    (exchange : Grid.ExchangeClass n m modsA modsB pqA pqB)
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
  exchangeQuotientOriginalMapComp
    (Pseudofunctor.id
      (ActualLiftSource.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel))
    (actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel))
    modsA modsB f g
    uF uG vF vG wF wG pqA pqB exchange basePath

/-- ORIGINAL target ε chosen lax mate: arbitrary F19/F28 primitive exchange. -/
def actualLiftTargetExchangeQuotientGeneralMateIndependence
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
    (exchange : Grid.ExchangeClass n m modsA modsB pqA pqB)
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
  exchangeQuotientOriginalMate
    (actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel))
    (Pseudofunctor.id
      (ActualLiftTarget.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel))
    modsA modsB f
    uF uG vF vG wF wG pqA pqB exchange basePath

/-- ORIGINAL target ε: nonstrict mapId under arbitrary primitive exchange. -/
def actualLiftTargetExchangeQuotientMapIdMateIndependence
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
    (exchange : Grid.ExchangeClass n m modsA modsB pqA pqB)
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
  exchangeQuotientOriginalMapId
    (actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel))
    (Pseudofunctor.id
      (ActualLiftTarget.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel))
    modsA modsB X
    uF uG vF vG wF wG pqA pqB exchange basePath

/-- ORIGINAL target ε: nonstrict mapComp under arbitrary primitive exchange. -/
def actualLiftTargetExchangeQuotientMapCompMateIndependence
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
    (exchange : Grid.ExchangeClass n m modsA modsB pqA pqB)
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
  exchangeQuotientOriginalMapComp
    (actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel))
    (Pseudofunctor.id
      (ActualLiftTarget.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel))
    modsA modsB f g
    uF uG vF vG wF wG pqA pqB exchange basePath

#print axioms actualLiftSourceExchangeQuotientGeneralMateIndependence
#print axioms actualLiftSourceExchangeQuotientMapIdMateIndependence
#print axioms actualLiftSourceExchangeQuotientMapCompMateIndependence
#print axioms actualLiftTargetExchangeQuotientGeneralMateIndependence
#print axioms actualLiftTargetExchangeQuotientMapIdMateIndependence
#print axioms actualLiftTargetExchangeQuotientMapCompMateIndependence

end

end KUOS.DependentOriginationCoherentBiadjunctionActualLiftExchangeQuotientV5_141
