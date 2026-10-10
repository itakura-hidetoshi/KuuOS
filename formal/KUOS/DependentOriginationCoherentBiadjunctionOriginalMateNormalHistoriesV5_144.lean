import KUOS.DependentOriginationCoherentBiadjunctionF45OrderCompatibilityV5_144
import KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientNonstrictMatesV5_141
import KUOS.DependentOriginationCoherentBiadjunctionChosenRightMateNormalFormV5_143

namespace KUOS.DependentOriginationCoherentBiadjunctionOriginalMateNormalHistoriesV5_144

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans
open KUOS.DependentOriginationCoherentBiadjunctionFiniteHorizontalExchangeV5_133
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137
open KUOS.DependentOriginationCoherentBiadjunctionConstructiveRefinementV5_138
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangleTracesV5_139
open KUOS.DependentOriginationCoherentBiadjunctionInterleavedRefinementV5_140
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141
open KUOS.DependentOriginationCoherentBiadjunctionFiniteTraceMateCoherenceV5_139.Generic
open KUOS.DependentOriginationCoherentBiadjunctionChosenRightMateCategoriesV5_116.Generic
open KUOS.DependentOriginationCoherentBiadjunctionCompressionKernelQuotientCategoryV5_125.Generic
open KUOS.DependentOriginationCoherentBiadjunctionHorizontalQuotientFunctorsV5_127.Generic
open KUOS.DependentOriginationCoherentBiadjunctionKernelQuotientMateBoundaryBridgeV5_130.Generic
open KUOS.DependentOriginationCoherentBiadjunctionStagewiseQuotientMixedHexagonV5_132.Generic
open KUOS.DependentOriginationCoherentBiadjunctionArbitraryModificationMatesV5_113.Generic
open KUOS.DependentOriginationCoherentBiadjunctionFiniteTraceNonstrictMatesV5_139.Generic
open KUOS.DependentOriginationCoherentBiadjunctionFiniteModificationMatePathsV5_135
open KUOS.DependentOriginationCoherentBiadjunctionComparisonKernelHomQuotientV5_125.Generic
open KUOS.DependentOriginationCoherentBiadjunctionNonstrictKernelWhiskeringV5_126.Generic
open KUOS.DependentOriginationCoherentBiadjunctionNonstrictMateCoherenceV5_130.Generic
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid
open KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientMateCoherenceV5_141.Generic
open KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientNonstrictMatesV5_141.Generic
open KUOS.DependentOriginationCoherentBiadjunctionChosenRightMateNormalFormV5_143.Generic

set_option autoImplicit false
noncomputable section

/-!
# F47-C / v5.144 — original F19/F28 mate and nonstrict boundaries from complete histories

The F46 equivalence reduces a genuine F44 exchange class to one
pair of complete native F19 modification and F28 quotient-category
Type-valued primitive histories. F47-A proves the actual F19-first and F28-first native normal
executions belong to the SAME generated exchange class. F47-B proves
history preservation under arbitrary quotient concatenation.

The four original F44 mate/hexagon and forward nonstrict comparisons
are instantiated here directly on that pair of native histories.
The original F-side invertible mapId/mapComp and the potentially
noninvertible G.toOplax comparisons are unchanged. In particular,
no F26 comparison chain is substituted for F28 native quotient Hom.
-/

namespace Generic

universe uB vB wB uC vC wC uE vE
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]
variable (F G : Pseudofunctor B C)

/-- Original F25/F33 mate and F35 four-stage hexagon boundaries for
a genuine pair of fully retained F19/F28 primitive histories. -/
theorem originalMateNormalHistories
    {a b : LeftMatePresentation F G}
    (modsA modsB : Grid.Blocks a b)
    {X Y : B} (f : X ⟶ Y)
    {aF bF aG bG eF eG : C}
    (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (vF : F.obj X ⟶ eF) (vG : G.obj X ⟶ eG)
    (wF : bF ⟶ F.obj Y) (wG : bG ⟶ G.obj Y)
    {x y : compressionKernelCategory aF bF aG bG}
    (pqA pqB : Grid.Blocks x y)
    {n m : Nat}
    (hm : Grid.AxisTrace n modsA modsB)
    (hc : Grid.AxisTrace m pqA pqB)
    (basePath :
      (⟨⟨F.map f, G.map f⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj Y)
          (G.obj X) (G.obj Y)) ⟶
      ((leftKernelQuotientWhiskerFunctor aF bF aG bG
        (vF ≫ uF) (vG ≫ uG) ⋙
        rightKernelQuotientWhiskerFunctor (F.obj X) bF
          (G.obj X) bG wF wG).obj x)) :
    let L := leftKernelQuotientWhiskerFunctor aF bF aG bG
      (vF ≫ uF) (vG ≫ uG) ⋙
      rightKernelQuotientWhiskerFunctor (F.obj X) bF
        (G.obj X) bG wF wG
    let R := rightKernelQuotientWhiskerFunctor aF bF aG bG wF wG ⋙
      leftKernelQuotientWhiskerFunctor aF (F.obj Y) aG (G.obj Y)
        (vF ≫ uF) (vG ≫ uG)
    let hexagon := kernelMixedHexagonStagewiseLongNatIso
      aF bF aG bG uF uG vF vG wF wG
    let routeLong := L.map pqA.composite ≫ hexagon.hom.app y
    let routeShort := hexagon.hom.app x ≫ R.map pqB.composite
    ((Grid.mapBlocks (rightMateFunctor F G) modsA).composite =
      (Grid.mapBlocks (rightMateFunctor F G) modsB).composite) ∧
    (kernelCategoryLeftMateBoundary a.core.datum b.core.datum
        modsA.composite f (basePath ≫ routeLong) =
      kernelCategoryLeftMateBoundary a.core.datum b.core.datum
        modsB.composite f (basePath ≫ routeShort) ∧
     kernelCategoryRightMateBoundary a.core.datum b.core.datum
        modsA.composite f (basePath ≫ routeLong) =
      kernelCategoryRightMateBoundary a.core.datum b.core.datum
        modsB.composite f (basePath ≫ routeShort) ∧
     kernelCategoryLeftMateBoundary a.core.datum b.core.datum
        modsA.composite f (basePath ≫ routeLong) =
      kernelCategoryRightMateBoundary a.core.datum b.core.datum
        modsB.composite f (basePath ≫ routeShort)) ∧
    (kernelCategoryHomToKernelHom (basePath ≫ routeLong) =
      kernelCategoryHomToKernelHom (basePath ≫ routeShort)) := by
  exact exchangeQuotientOriginalMate F G modsA modsB f
    uF uG vF vG wF wG pqA pqB
    (Grid.AxisTrace.pairToClass (hm, hc)) basePath

/-- The unchanged original crossed lax right-mate coherence under an
arbitrary additional potentially NONINVERTIBLE F28 NatTrans. -/
theorem verticalMateNormalHistories
    {a b : LeftMatePresentation F G}
    (modsA modsB : Grid.Blocks a b)
    {X Y : B} (f : X ⟶ Y)
    {aF bF aG bG eF eG : C}
    (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (vF : F.obj X ⟶ eF) (vG : G.obj X ⟶ eG)
    (wF : bF ⟶ F.obj Y) (wG : bG ⟶ G.obj Y)
    (T : compressionKernelCategory aF bF aG bG ⥤
      compressionKernelCategory (F.obj X) (F.obj Y)
        (G.obj X) (G.obj Y))
    (β :
      (rightKernelQuotientWhiskerFunctor aF bF aG bG wF wG ⋙
        leftKernelQuotientWhiskerFunctor aF (F.obj Y) aG (G.obj Y)
          (vF ≫ uF) (vG ≫ uG)) ⟶ T)
    {x y : compressionKernelCategory aF bF aG bG}
    (pqA pqB : Grid.Blocks x y)
    {n m : Nat}
    (hm : Grid.AxisTrace n modsA modsB)
    (hc : Grid.AxisTrace m pqA pqB)
    (basePath :
      (⟨⟨F.map f, G.map f⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj Y)
          (G.obj X) (G.obj Y)) ⟶
      ((leftKernelQuotientWhiskerFunctor aF bF aG bG
        (vF ≫ uF) (vG ≫ uG) ⋙
        rightKernelQuotientWhiskerFunctor (F.obj X) bF
          (G.obj X) bG wF wG).obj x)) :
    let L := leftKernelQuotientWhiskerFunctor aF bF aG bG
      (vF ≫ uF) (vG ≫ uG) ⋙
      rightKernelQuotientWhiskerFunctor (F.obj X) bF
        (G.obj X) bG wF wG
    let hexagon := kernelMixedHexagonStagewiseLongNatIso
      aF bF aG bG uF uG vF vG wF wG
    let routeLong := (L.map pqA.composite ≫ hexagon.hom.app y) ≫ β.app y
    let routeShort := hexagon.hom.app x ≫
      (β.app x ≫ T.map pqB.composite)
    ((Grid.mapBlocks (rightMateFunctor F G) modsA).composite =
      (Grid.mapBlocks (rightMateFunctor F G) modsB).composite) ∧
    (kernelCategoryLeftMateBoundary a.core.datum b.core.datum
        modsA.composite f (basePath ≫ routeLong) =
      kernelCategoryLeftMateBoundary a.core.datum b.core.datum
        modsB.composite f (basePath ≫ routeShort) ∧
     kernelCategoryRightMateBoundary a.core.datum b.core.datum
        modsA.composite f (basePath ≫ routeLong) =
      kernelCategoryRightMateBoundary a.core.datum b.core.datum
        modsB.composite f (basePath ≫ routeShort) ∧
     kernelCategoryLeftMateBoundary a.core.datum b.core.datum
        modsA.composite f (basePath ≫ routeLong) =
      kernelCategoryRightMateBoundary a.core.datum b.core.datum
        modsB.composite f (basePath ≫ routeShort)) ∧
    (kernelCategoryHomToKernelHom (basePath ≫ routeLong) =
      kernelCategoryHomToKernelHom (basePath ≫ routeShort)) := by
  exact exchangeQuotientVerticalMate F G modsA modsB f
    uF uG vF vG wF wG T β pqA pqB
    (Grid.AxisTrace.pairToClass (hm, hc)) basePath

/-- Original F.mapId ISO and forward G.toOplax.mapId comparison
retain their original direction in both complete histories. -/
theorem originalMapIdNormalHistories
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
    (hm : Grid.AxisTrace n modsA modsB)
    (hc : Grid.AxisTrace m pA pB)
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
  exact exchangeQuotientOriginalMapId F G modsA modsB X
    uF uG vF vG wF wG pA pB
    (Grid.AxisTrace.pairToClass (hm, hc)) basePath

/-- Original F.mapComp ISO and forward G.toOplax.mapComp comparison
retain their original direction in both complete histories. -/
theorem originalMapCompNormalHistories
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
    (hm : Grid.AxisTrace n modsA modsB)
    (hc : Grid.AxisTrace m pA pB)
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
  exact exchangeQuotientOriginalMapComp F G modsA modsB f g
    uF uG vF vG wF wG pA pB
    (Grid.AxisTrace.pairToClass (hm, hc)) basePath

/-- The ACTUAL F19-first and F28-first normal execution orders commute even after
applying the ORIGINAL chosen right-mate functor on the F19 axis,
and a separate arbitrary honest functor on the F28 axis. -/
theorem chosenRightMateNormalOrdersAgree
    {a b : LeftMatePresentation F G}
    {aF bF aG bG : C}
    {x y : compressionKernelCategory aF bF aG bG}
    {modsA modsB : Grid.Blocks a b}
    {pqA pqB : Grid.Blocks x y}
    {n m : Nat} {T : Type uE} [Category.{vE} T]
    (K : compressionKernelCategory aF bF aG bG ⥤ T)
    (hm : Grid.AxisTrace n modsA modsB)
    (hc : Grid.AxisTrace m pqA pqB) :
    Grid.ExchangeClass.mapBoth (rightMateFunctor F G) K
      (Grid.AxisTrace.modificationNormal hm hc).toClass =
    Grid.ExchangeClass.mapBoth (rightMateFunctor F G) K
      (Grid.AxisTrace.comparisonNormal hm hc).toClass :=
  congrArg (Grid.ExchangeClass.mapBoth (rightMateFunctor F G) K)
    (Grid.AxisTrace.modificationNormal_class_eq_comparisonNormal hm hc)

/-- The genuine F47 F19-first normal path, transported through the ORIGINAL
F19 chosen right mate and independent F28 functor, is completely
classified by the TWO transported native Type-level histories. -/
theorem chosenRightMateF19FirstNormalHistories
    {a b : LeftMatePresentation F G}
    {aF bF aG bG : C}
    {x y : compressionKernelCategory aF bF aG bG}
    {modsA modsB : Grid.Blocks a b}
    {pqA pqB : Grid.Blocks x y}
    {n m : Nat} {T : Type uE} [Category.{vE} T]
    (K : compressionKernelCategory aF bF aG bG ⥤ T)
    (hm : Grid.AxisTrace n modsA modsB)
    (hc : Grid.AxisTrace m pqA pqB) :
    chosenRightMateExchangeQuotientTransport F G K
      ((Grid.AxisTrace.modificationNormal hm hc).toClass) =
    Grid.AxisTrace.pairToClass
      (Grid.AxisTrace.mapBlocks (rightMateFunctor F G) hm,
       Grid.AxisTrace.mapBlocks K hc) := by
  calc
    chosenRightMateExchangeQuotientTransport F G K
        ((Grid.AxisTrace.modificationNormal hm hc).toClass) =
      Grid.AxisTrace.pairToClass
        (Grid.AxisTrace.mapBlocks (rightMateFunctor F G)
          ((Grid.AxisTrace.modificationNormal hm hc).toClass).axisTraces.1,
         Grid.AxisTrace.mapBlocks K
          ((Grid.AxisTrace.modificationNormal hm hc).toClass).axisTraces.2) :=
      chosenRightMateExchangeNormalForm F G K _
    _ = Grid.AxisTrace.pairToClass
          (Grid.AxisTrace.mapBlocks (rightMateFunctor F G) hm,
           Grid.AxisTrace.mapBlocks K hc) := by
      rw [Grid.OrderedInterleaving.axisTraces_toClass,
        Grid.AxisTrace.modificationNormal_modificationTrace,
        Grid.AxisTrace.modificationNormal_comparisonTrace]

#print axioms originalMateNormalHistories
#print axioms verticalMateNormalHistories
#print axioms originalMapIdNormalHistories
#print axioms originalMapCompNormalHistories
#print axioms chosenRightMateNormalOrdersAgree
#print axioms chosenRightMateF19FirstNormalHistories

end Generic
end
end KUOS.DependentOriginationCoherentBiadjunctionOriginalMateNormalHistoriesV5_144
