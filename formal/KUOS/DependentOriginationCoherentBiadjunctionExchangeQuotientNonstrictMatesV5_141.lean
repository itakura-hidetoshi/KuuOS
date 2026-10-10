import KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientMateCoherenceV5_141
import KUOS.DependentOriginationCoherentBiadjunctionFiniteTraceNonstrictMatesV5_139

namespace KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientNonstrictMatesV5_141

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionFiniteHorizontalExchangeV5_133
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137
open KUOS.DependentOriginationCoherentBiadjunctionConstructiveRefinementV5_138
open KUOS.DependentOriginationCoherentBiadjunctionInterleavedRefinementV5_140
open KUOS.DependentOriginationCoherentBiadjunctionFiniteTraceNonstrictMatesV5_139.Generic
open KUOS.DependentOriginationCoherentBiadjunctionFiniteModificationMatePathsV5_135
open KUOS.DependentOriginationCoherentBiadjunctionChosenRightMateCategoriesV5_116.Generic
open KUOS.DependentOriginationCoherentBiadjunctionCompressionKernelQuotientCategoryV5_125.Generic
open KUOS.DependentOriginationCoherentBiadjunctionComparisonKernelHomQuotientV5_125.Generic
open KUOS.DependentOriginationCoherentBiadjunctionNonstrictKernelWhiskeringV5_126.Generic
open KUOS.DependentOriginationCoherentBiadjunctionHorizontalQuotientFunctorsV5_127.Generic
open KUOS.DependentOriginationCoherentBiadjunctionKernelQuotientMateBoundaryBridgeV5_130.Generic
open KUOS.DependentOriginationCoherentBiadjunctionNonstrictMateCoherenceV5_130.Generic
open KUOS.DependentOriginationCoherentBiadjunctionStagewiseQuotientMixedHexagonV5_132.Generic

set_option autoImplicit false
noncomputable section

/-!
# F44-D / v5.141: ORIGINAL nonstrict comparisons descended to exchange classes

The actual primitive F19 modification-axis and F28 quotient-axis
refinement steps may be interleaved in ANY finite order. Original
pseudofunctor F.mapId and mapComp comparison ISOs, and the original
FORWARD potentially NONINVERTIBLE G.toOplax comparison 2-cells, are
retained. The ORIGINAL F25/F33 crossed mate boundaries and F/G
compressed comparison remain equal after ANY such interleaving.

Sequential interleavings genuinely concatenate with the exact
independent primitive step counts, not an arbitrary strictification.
No source or target chosen objectwise adjunction is changed.
-/

namespace Generic

universe uB vB wB uC vC wC
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]
variable (F G : Pseudofunctor B C)

/-- Original nonstrict mapId under ANY original two-axis primitive exchange. -/
theorem exchangeQuotientOriginalMapId
    {a b : LeftMatePresentation F G}
    (modsA modsB : Grid.Blocks a b)
    (X : B)
    {aF bF aG bG eF eG : C}
    (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (vF : F.obj X ⟶ eF) (vG : G.obj X ⟶ eG)
    (wF : bF ⟶ F.obj X) (wG : bG ⟶ G.obj X)
    {x y : compressionKernelCategory aF bF aG bG}
    (pA pB : Grid.Blocks x y)
    {n m : Nat}
    (exchange : Grid.ExchangeClass n m modsA modsB pA pB)
    (basePath :
      (⟨⟨𝟙 (F.obj X), 𝟙 (G.obj X)⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj X) (G.obj X) (G.obj X)) ⟶
      ((leftKernelQuotientWhiskerFunctor aF bF aG bG
        (vF ≫ uF) (vG ≫ uG) ⋙
        rightKernelQuotientWhiskerFunctor (F.obj X) bF
          (G.obj X) bG wF wG).obj x)) :
    ((Grid.mapBlocks (rightMateFunctor F G) modsA).composite =
      (Grid.mapBlocks (rightMateFunctor F G) modsB).composite) ∧
    (let hexagon := kernelMixedHexagonStagewiseLongNatIso aF bF aG bG
      uF uG vF vG wF wG
    let routeLong := (rightKernelQuotientWhiskerFunctor (F.obj X) bF
        (G.obj X) bG wF wG).map
          ((leftKernelQuotientWhiskerFunctor aF bF aG bG
            (vF ≫ uF) (vG ≫ uG)).map pA.composite) ≫ hexagon.hom.app y
    let routeShort := hexagon.hom.app x ≫
      (leftKernelQuotientWhiskerFunctor aF (F.obj X)
        aG (G.obj X) (vF ≫ uF) (vG ≫ uG)).map
        ((rightKernelQuotientWhiskerFunctor aF bF aG bG
          wF wG).map pB.composite)
    let longClass := originalMapIdQuotientPrepend (F := F) (G := G) X
      (kernelCategoryHomToKernelHom (basePath ≫ routeLong))
    let shortClass := originalMapIdQuotientPrepend (F := F) (G := G) X
      (kernelCategoryHomToKernelHom (basePath ≫ routeShort))
    quotientLeftMateBoundary a.core.datum b.core.datum modsA.composite (𝟙 X) longClass =
        quotientRightMateBoundary a.core.datum b.core.datum modsB.composite (𝟙 X) shortClass ∧
      quotientComposite longClass = quotientComposite shortClass ) := by
  exact finiteTraceOriginalMapId F G modsA modsB X
    uF uG vF vG wF wG pA pB
    (Grid.ExchangeClass.toInterleaving exchange).toRectangleTrace basePath

/-- Original nonstrict mapId through successive independently counted
finite interleavings of F19 and F28 primitive refinement operations. -/
theorem exchangeQuotientOriginalMapIdTrans
    {a b : LeftMatePresentation F G}
    (modsA modsB modsC : Grid.Blocks a b)
    (X : B)
    {aF bF aG bG eF eG : C}
    (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (vF : F.obj X ⟶ eF) (vG : G.obj X ⟶ eG)
    (wF : bF ⟶ F.obj X) (wG : bG ⟶ G.obj X)
    {x y : compressionKernelCategory aF bF aG bG}
    (pA pB pC : Grid.Blocks x y)
    {n₁ n₂ m₁ m₂ : Nat}
    (exchangeAB : Grid.ExchangeClass n₁ m₁ modsA modsB pA pB)
    (exchangeBC : Grid.ExchangeClass n₂ m₂ modsB modsC pB pC)
    (basePath :
      (⟨⟨𝟙 (F.obj X), 𝟙 (G.obj X)⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj X) (G.obj X) (G.obj X)) ⟶
      ((leftKernelQuotientWhiskerFunctor aF bF aG bG
        (vF ≫ uF) (vG ≫ uG) ⋙
        rightKernelQuotientWhiskerFunctor (F.obj X) bF
          (G.obj X) bG wF wG).obj x)) :
    ((Grid.mapBlocks (rightMateFunctor F G) modsA).composite =
      (Grid.mapBlocks (rightMateFunctor F G) modsC).composite) ∧
    (let hexagon := kernelMixedHexagonStagewiseLongNatIso aF bF aG bG
      uF uG vF vG wF wG
    let routeLong := (rightKernelQuotientWhiskerFunctor (F.obj X) bF
        (G.obj X) bG wF wG).map
          ((leftKernelQuotientWhiskerFunctor aF bF aG bG
            (vF ≫ uF) (vG ≫ uG)).map pA.composite) ≫ hexagon.hom.app y
    let routeShort := hexagon.hom.app x ≫
      (leftKernelQuotientWhiskerFunctor aF (F.obj X)
        aG (G.obj X) (vF ≫ uF) (vG ≫ uG)).map
        ((rightKernelQuotientWhiskerFunctor aF bF aG bG
          wF wG).map pC.composite)
    let longClass := originalMapIdQuotientPrepend (F := F) (G := G) X
      (kernelCategoryHomToKernelHom (basePath ≫ routeLong))
    let shortClass := originalMapIdQuotientPrepend (F := F) (G := G) X
      (kernelCategoryHomToKernelHom (basePath ≫ routeShort))
    quotientLeftMateBoundary a.core.datum b.core.datum modsA.composite (𝟙 X) longClass =
        quotientRightMateBoundary a.core.datum b.core.datum modsC.composite (𝟙 X) shortClass ∧
      quotientComposite longClass = quotientComposite shortClass ) := by
  exact exchangeQuotientOriginalMapId F G modsA modsC X
    uF uG vF vG wF wG pA pC
    (Grid.ExchangeClass.append exchangeAB exchangeBC) basePath

/-- Original nonstrict mapComp through any interleaved refinement. -/
theorem exchangeQuotientOriginalMapComp
    {a b : LeftMatePresentation F G}
    (modsA modsB : Grid.Blocks a b)
    {X Y Z : B} (f : X ⟶ Y) (g : Y ⟶ Z)
    {aF bF aG bG eF eG : C}
    (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (vF : F.obj X ⟶ eF) (vG : G.obj X ⟶ eG)
    (wF : bF ⟶ F.obj Z) (wG : bG ⟶ G.obj Z)
    {x y : compressionKernelCategory aF bF aG bG}
    (pA pB : Grid.Blocks x y)
    {n m : Nat}
    (exchange : Grid.ExchangeClass n m modsA modsB pA pB)
    (basePath :
      (⟨⟨F.map f ≫ F.map g, G.map f ≫ G.map g⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj Z) (G.obj X) (G.obj Z)) ⟶
      ((leftKernelQuotientWhiskerFunctor aF bF aG bG
        (vF ≫ uF) (vG ≫ uG) ⋙
        rightKernelQuotientWhiskerFunctor (F.obj X) bF
          (G.obj X) bG wF wG).obj x)) :
    ((Grid.mapBlocks (rightMateFunctor F G) modsA).composite =
      (Grid.mapBlocks (rightMateFunctor F G) modsB).composite) ∧
    (let hexagon := kernelMixedHexagonStagewiseLongNatIso aF bF aG bG
      uF uG vF vG wF wG
    let routeLong := (rightKernelQuotientWhiskerFunctor (F.obj X) bF
        (G.obj X) bG wF wG).map
          ((leftKernelQuotientWhiskerFunctor aF bF aG bG
            (vF ≫ uF) (vG ≫ uG)).map pA.composite) ≫ hexagon.hom.app y
    let routeShort := hexagon.hom.app x ≫
      (leftKernelQuotientWhiskerFunctor aF (F.obj Z)
        aG (G.obj Z) (vF ≫ uF) (vG ≫ uG)).map
        ((rightKernelQuotientWhiskerFunctor aF bF aG bG
          wF wG).map pB.composite)
    let longClass := originalMapCompQuotientPrepend (F := F) (G := G) f g
      (kernelCategoryHomToKernelHom (basePath ≫ routeLong))
    let shortClass := originalMapCompQuotientPrepend (F := F) (G := G) f g
      (kernelCategoryHomToKernelHom (basePath ≫ routeShort))
    quotientLeftMateBoundary a.core.datum b.core.datum modsA.composite (f ≫ g) longClass =
        quotientRightMateBoundary a.core.datum b.core.datum modsB.composite (f ≫ g) shortClass ∧
      quotientComposite longClass = quotientComposite shortClass ) := by
  exact finiteTraceOriginalMapComp F G modsA modsB f g
    uF uG vF vG wF wG pA pB
    (Grid.ExchangeClass.toInterleaving exchange).toRectangleTrace basePath

/-- Original nonstrict mapComp coherence under concatenated two-axis
primitive refinement interleavings with exact additive step counts. -/
theorem exchangeQuotientOriginalMapCompTrans
    {a b : LeftMatePresentation F G}
    (modsA modsB modsC : Grid.Blocks a b)
    {X Y Z : B} (f : X ⟶ Y) (g : Y ⟶ Z)
    {aF bF aG bG eF eG : C}
    (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (vF : F.obj X ⟶ eF) (vG : G.obj X ⟶ eG)
    (wF : bF ⟶ F.obj Z) (wG : bG ⟶ G.obj Z)
    {x y : compressionKernelCategory aF bF aG bG}
    (pA pB pC : Grid.Blocks x y)
    {n₁ n₂ m₁ m₂ : Nat}
    (exchangeAB : Grid.ExchangeClass n₁ m₁ modsA modsB pA pB)
    (exchangeBC : Grid.ExchangeClass n₂ m₂ modsB modsC pB pC)
    (basePath :
      (⟨⟨F.map f ≫ F.map g, G.map f ≫ G.map g⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj Z) (G.obj X) (G.obj Z)) ⟶
      ((leftKernelQuotientWhiskerFunctor aF bF aG bG
        (vF ≫ uF) (vG ≫ uG) ⋙
        rightKernelQuotientWhiskerFunctor (F.obj X) bF
          (G.obj X) bG wF wG).obj x)) :
    ((Grid.mapBlocks (rightMateFunctor F G) modsA).composite =
      (Grid.mapBlocks (rightMateFunctor F G) modsC).composite) ∧
    (let hexagon := kernelMixedHexagonStagewiseLongNatIso aF bF aG bG
      uF uG vF vG wF wG
    let routeLong := (rightKernelQuotientWhiskerFunctor (F.obj X) bF
        (G.obj X) bG wF wG).map
          ((leftKernelQuotientWhiskerFunctor aF bF aG bG
            (vF ≫ uF) (vG ≫ uG)).map pA.composite) ≫ hexagon.hom.app y
    let routeShort := hexagon.hom.app x ≫
      (leftKernelQuotientWhiskerFunctor aF (F.obj Z)
        aG (G.obj Z) (vF ≫ uF) (vG ≫ uG)).map
        ((rightKernelQuotientWhiskerFunctor aF bF aG bG
          wF wG).map pC.composite)
    let longClass := originalMapCompQuotientPrepend (F := F) (G := G) f g
      (kernelCategoryHomToKernelHom (basePath ≫ routeLong))
    let shortClass := originalMapCompQuotientPrepend (F := F) (G := G) f g
      (kernelCategoryHomToKernelHom (basePath ≫ routeShort))
    quotientLeftMateBoundary a.core.datum b.core.datum modsA.composite (f ≫ g) longClass =
        quotientRightMateBoundary a.core.datum b.core.datum modsC.composite (f ≫ g) shortClass ∧
      quotientComposite longClass = quotientComposite shortClass ) := by
  exact exchangeQuotientOriginalMapComp F G modsA modsC f g
    uF uG vF vG wF wG pA pC
    (Grid.ExchangeClass.append exchangeAB exchangeBC) basePath

#print axioms exchangeQuotientOriginalMapId
#print axioms exchangeQuotientOriginalMapIdTrans
#print axioms exchangeQuotientOriginalMapComp
#print axioms exchangeQuotientOriginalMapCompTrans

end Generic
end

end KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientNonstrictMatesV5_141
