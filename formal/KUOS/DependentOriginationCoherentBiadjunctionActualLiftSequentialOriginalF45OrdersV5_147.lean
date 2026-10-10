import KUOS.DependentOriginationCoherentBiadjunctionOriginalF45SequentialMateNaturalityV5_147
import KUOS.DependentOriginationCoherentBiadjunctionOriginalF45OrderedMatesV5_146
import KUOS.DependentOriginationCoherentBiadjunctionOriginalMateNormalHistoriesV5_144
import KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientNonstrictMatesV5_141
import KUOS.DependentOriginationCoherentBiadjunctionActualLiftInterleavedRefinementV5_140
import KUOS.DependentOriginationCoherentBiadjunctionActualLiftFiniteRefinementTracesV5_139

namespace KUOS.DependentOriginationCoherentBiadjunctionActualLiftSequentialOriginalF45OrdersV5_147

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionFiniteHorizontalExchangeV5_133
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137
open KUOS.DependentOriginationCoherentBiadjunctionConstructiveRefinementV5_138
open KUOS.DependentOriginationCoherentBiadjunctionInterleavedRefinementV5_140
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141
open KUOS.DependentOriginationCoherentBiadjunctionActualLiftDoubleBracketedHexagonV5_136
open KUOS.DependentOriginationCoherentBiadjunctionOriginalF45OrderedMatesV5_146.Generic
open KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientMateCoherenceV5_141.Generic
open KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientNonstrictMatesV5_141.Generic
open KUOS.DependentOriginationCoherentBiadjunctionOriginalF45OrderedMatesV5_146.Generic
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
# F50-C / v5.147 — actual source η and target ε through SERIAL ORIGINAL F45 paths

F49 instantiated all six actualLift source η and target ε general /
nonstrict mapId / nonstrict mapComp comparison boundaries using ONE
genuine old F45 path and its original Eq.mp/Nat.zero_add transport.

This file goes strictly beyond one stage: it uses the ACTUAL ORIGINAL
F45 first and second independent-order path witnesses as inputs,
concatenates them in the real F44 generated adjacent-swap quotient
with exact per-axis depths n+n' / m+m', and feeds the result directly
into the ORIGINAL F25/F33 mate, F35 four-stage hexagon and ORIGINAL
forward F/G nonstrict comparison theorems.

F50-A proves the sequential class is precisely the canonical ORIGINAL
F45 total execution for ANY independently selected order. F50-B
proves the ORIGINAL chosen right-mate transport preserves this same
serial composition under an independent genuine F28 functor.

The original source η / target ε pseudonatural transformations,
chosen objectwise adjunctions, F-side isomorphisms and G-side
potentially NONINVERTIBLE forward comparisons are untouched. No
synthetic inverse, F19/F28 Hom collapse, or global bicategorical
biequivalence is introduced.

-/

universe u v uH vH uW uP
variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-- ORIGINAL source η chosen lax mate: arbitrary F19/F28 primitive exchange. -/
def actualLiftSourceSequentialOriginalF45GeneralMateIndependence
    (modsA modsM modsB : Grid.Blocks
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
    (pqA pqM pqB : Grid.Blocks x y)
    {n m n' m' : Nat}
    (first second : Grid.OriginalF45Order)
    (hm₁ : Grid.AxisTrace n modsA modsM)
    (hm₂ : Grid.AxisTrace n' modsM modsB)
    (hc₁ : Grid.AxisTrace m pqA pqM)
    (hc₂ : Grid.AxisTrace m' pqM pqB)
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
    uF uG vF vG wF wG pqA pqB
    (Grid.ExchangeClass.append
      (Grid.AxisTrace.originalF45OrderClass first hm₁ hc₁)
      (Grid.AxisTrace.originalF45OrderClass second hm₂ hc₂)) basePath

/-- ORIGINAL source η: nonstrict mapId under arbitrary primitive exchange. -/
def actualLiftSourceSequentialOriginalF45MapIdMateIndependence
    (modsA modsM modsB : Grid.Blocks
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
    (pqA pqM pqB : Grid.Blocks x y)
    {n m n' m' : Nat}
    (first second : Grid.OriginalF45Order)
    (hm₁ : Grid.AxisTrace n modsA modsM)
    (hm₂ : Grid.AxisTrace n' modsM modsB)
    (hc₁ : Grid.AxisTrace m pqA pqM)
    (hc₂ : Grid.AxisTrace m' pqM pqB)
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
    uF uG vF vG wF wG pqA pqB
    (Grid.ExchangeClass.append
      (Grid.AxisTrace.originalF45OrderClass first hm₁ hc₁)
      (Grid.AxisTrace.originalF45OrderClass second hm₂ hc₂)) basePath

/-- ORIGINAL source η: nonstrict mapComp under arbitrary primitive exchange. -/
def actualLiftSourceSequentialOriginalF45MapCompMateIndependence
    (modsA modsM modsB : Grid.Blocks
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
    (pqA pqM pqB : Grid.Blocks x y)
    {n m n' m' : Nat}
    (first second : Grid.OriginalF45Order)
    (hm₁ : Grid.AxisTrace n modsA modsM)
    (hm₂ : Grid.AxisTrace n' modsM modsB)
    (hc₁ : Grid.AxisTrace m pqA pqM)
    (hc₂ : Grid.AxisTrace m' pqM pqB)
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
    uF uG vF vG wF wG pqA pqB
    (Grid.ExchangeClass.append
      (Grid.AxisTrace.originalF45OrderClass first hm₁ hc₁)
      (Grid.AxisTrace.originalF45OrderClass second hm₂ hc₂)) basePath

/-- ORIGINAL target ε chosen lax mate: arbitrary F19/F28 primitive exchange. -/
def actualLiftTargetSequentialOriginalF45GeneralMateIndependence
    (modsA modsM modsB : Grid.Blocks
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
    (pqA pqM pqB : Grid.Blocks x y)
    {n m n' m' : Nat}
    (first second : Grid.OriginalF45Order)
    (hm₁ : Grid.AxisTrace n modsA modsM)
    (hm₂ : Grid.AxisTrace n' modsM modsB)
    (hc₁ : Grid.AxisTrace m pqA pqM)
    (hc₂ : Grid.AxisTrace m' pqM pqB)
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
    uF uG vF vG wF wG pqA pqB
    (Grid.ExchangeClass.append
      (Grid.AxisTrace.originalF45OrderClass first hm₁ hc₁)
      (Grid.AxisTrace.originalF45OrderClass second hm₂ hc₂)) basePath

/-- ORIGINAL target ε: nonstrict mapId under arbitrary primitive exchange. -/
def actualLiftTargetSequentialOriginalF45MapIdMateIndependence
    (modsA modsM modsB : Grid.Blocks
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
    (pqA pqM pqB : Grid.Blocks x y)
    {n m n' m' : Nat}
    (first second : Grid.OriginalF45Order)
    (hm₁ : Grid.AxisTrace n modsA modsM)
    (hm₂ : Grid.AxisTrace n' modsM modsB)
    (hc₁ : Grid.AxisTrace m pqA pqM)
    (hc₂ : Grid.AxisTrace m' pqM pqB)
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
    uF uG vF vG wF wG pqA pqB
    (Grid.ExchangeClass.append
      (Grid.AxisTrace.originalF45OrderClass first hm₁ hc₁)
      (Grid.AxisTrace.originalF45OrderClass second hm₂ hc₂)) basePath

/-- ORIGINAL target ε: nonstrict mapComp under arbitrary primitive exchange. -/
def actualLiftTargetSequentialOriginalF45MapCompMateIndependence
    (modsA modsM modsB : Grid.Blocks
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
    (pqA pqM pqB : Grid.Blocks x y)
    {n m n' m' : Nat}
    (first second : Grid.OriginalF45Order)
    (hm₁ : Grid.AxisTrace n modsA modsM)
    (hm₂ : Grid.AxisTrace n' modsM modsB)
    (hc₁ : Grid.AxisTrace m pqA pqM)
    (hc₂ : Grid.AxisTrace m' pqM pqB)
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
    uF uG vF vG wF wG pqA pqB
    (Grid.ExchangeClass.append
      (Grid.AxisTrace.originalF45OrderClass first hm₁ hc₁)
      (Grid.AxisTrace.originalF45OrderClass second hm₂ hc₂)) basePath

#print axioms actualLiftSourceSequentialOriginalF45GeneralMateIndependence
#print axioms actualLiftSourceSequentialOriginalF45MapIdMateIndependence
#print axioms actualLiftSourceSequentialOriginalF45MapCompMateIndependence
#print axioms actualLiftTargetSequentialOriginalF45GeneralMateIndependence
#print axioms actualLiftTargetSequentialOriginalF45MapIdMateIndependence
#print axioms actualLiftTargetSequentialOriginalF45MapCompMateIndependence

end

end KUOS.DependentOriginationCoherentBiadjunctionActualLiftSequentialOriginalF45OrdersV5_147
