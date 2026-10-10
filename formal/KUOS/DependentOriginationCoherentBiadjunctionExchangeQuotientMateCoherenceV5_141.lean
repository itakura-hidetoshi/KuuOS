import KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientConcatenationV5_141
import KUOS.DependentOriginationCoherentBiadjunctionFiniteTraceMateCoherenceV5_139

namespace KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientMateCoherenceV5_141

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionFiniteHorizontalExchangeV5_133
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137
open KUOS.DependentOriginationCoherentBiadjunctionConstructiveRefinementV5_138
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangleTracesV5_139
open KUOS.DependentOriginationCoherentBiadjunctionInterleavedRefinementV5_140
open KUOS.DependentOriginationCoherentBiadjunctionFiniteTraceMateCoherenceV5_139.Generic
open KUOS.DependentOriginationCoherentBiadjunctionChosenRightMateCategoriesV5_116.Generic
open KUOS.DependentOriginationCoherentBiadjunctionCompressionKernelQuotientCategoryV5_125.Generic
open KUOS.DependentOriginationCoherentBiadjunctionHorizontalQuotientFunctorsV5_127.Generic
open KUOS.DependentOriginationCoherentBiadjunctionKernelQuotientMateBoundaryBridgeV5_130.Generic
open KUOS.DependentOriginationCoherentBiadjunctionStagewiseQuotientMixedHexagonV5_132.Generic
open KUOS.DependentOriginationCoherentBiadjunctionArbitraryModificationMatesV5_113.Generic

set_option autoImplicit false
noncomputable section

/-!
# F44-C / v5.141 — original chosen mates descended to exchange classes

Unlike F42, which bundled a pair of independently finite F19/F28
primitive refinement traces, F43-B constructs an ACTUALLY ORDERED
two-axis path. At every intermediate step the original F19 chosen
StrongTrans.Modification or genuine F28 quotient-category path is
changed, and the other axis is held fixed.

Every such exchange descends to the existing F42 RectangleTrace and
hence to the ORIGINAL F35 four-stage hexagon / F25/F33 genuine
LEFT, RIGHT and CROSS lax right-mate boundaries and native KernelHom.
Sequential ordered shuffles add their respective exact step counts.
Both originals remain valid after a SECOND arbitrary potentially
noninvertible quotient-category NatTrans.

The ORIGINAL F19 right-mate functor itself transports individual
primitive moves and the entire exchange, not only composite equalities;
the quotient-axis functor is permitted to be an arbitrary honest
functor, while keeping its original F28 domain. These statements
do not assume any extra inverse of G's lax comparison cells.
-/

namespace Generic

universe uB vB wB uC vC wC uE vE
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]
variable (F G : Pseudofunctor B C)

/-- ORIGINAL chosen F19 right-mate functor transports EVERY explicit
interleaved primitive modification step, at exact original depth,
simultaneously with ANY actual F28 quotient-category functor. -/
def chosenRightMateExchangeQuotientTransport
    {a b : LeftMatePresentation F G}
    {aF bF aG bG : C}
    {x y : compressionKernelCategory aF bF aG bG}
    {modsA modsB : Grid.Blocks a b}
    {pqA pqB : Grid.Blocks x y}
    {n m : Nat}
    {T : Type uE} [Category.{vE} T]
    (K : compressionKernelCategory aF bF aG bG ⥤ T)
    (exchange : Grid.ExchangeClass n m modsA modsB pqA pqB) :
    Grid.ExchangeClass n m
      (Grid.mapBlocks (rightMateFunctor F G) modsA)
      (Grid.mapBlocks (rightMateFunctor F G) modsB)
      (Grid.mapBlocks K pqA)
      (Grid.mapBlocks K pqB) :=
  Grid.ExchangeClass.mapBoth (rightMateFunctor F G) K exchange

/-- The original independent-axis exchange sequence preserves the
unchanged F25/F33 left/right/cross lax mate boundary equations and
the original F25 KernelHom comparison, not merely their composite. -/
theorem exchangeQuotientOriginalMate
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
    (exchange : Grid.ExchangeClass n m modsA modsB pqA pqB)
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
  exact finiteTraceRectangleOriginalMate F G modsA modsB f uF uG vF vG wF wG pqA pqB
    (Grid.ExchangeClass.toInterleaving exchange).toRectangleTrace basePath

/-- Two arbitrary original ordered exchange sequences concatenate as
another original F19/F28 exchange, with EXACT additive n/m depths. -/
theorem exchangeQuotientOriginalMateTrans
    {a b : LeftMatePresentation F G}
    (modsA modsB modsC : Grid.Blocks a b)
    {X Y : B} (f : X ⟶ Y)
    {aF bF aG bG eF eG : C}
    (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (vF : F.obj X ⟶ eF) (vG : G.obj X ⟶ eG)
    (wF : bF ⟶ F.obj Y) (wG : bG ⟶ G.obj Y)
    {x y : compressionKernelCategory aF bF aG bG}
    (pqA pqB pqC : Grid.Blocks x y)
    {n₁ n₂ m₁ m₂ : Nat}
    (exchangeAB : Grid.ExchangeClass n₁ m₁ modsA modsB pqA pqB)
    (exchangeBC : Grid.ExchangeClass n₂ m₂ modsB modsC pqB pqC)
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
    let routeShort := hexagon.hom.app x ≫ R.map pqC.composite
    ((Grid.mapBlocks (rightMateFunctor F G) modsA).composite =
      (Grid.mapBlocks (rightMateFunctor F G) modsC).composite) ∧
    (kernelCategoryLeftMateBoundary a.core.datum b.core.datum
        modsA.composite f (basePath ≫ routeLong) =
      kernelCategoryLeftMateBoundary a.core.datum b.core.datum
        modsC.composite f (basePath ≫ routeShort) ∧
     kernelCategoryRightMateBoundary a.core.datum b.core.datum
        modsA.composite f (basePath ≫ routeLong) =
      kernelCategoryRightMateBoundary a.core.datum b.core.datum
        modsC.composite f (basePath ≫ routeShort) ∧
     kernelCategoryLeftMateBoundary a.core.datum b.core.datum
        modsA.composite f (basePath ≫ routeLong) =
      kernelCategoryRightMateBoundary a.core.datum b.core.datum
        modsC.composite f (basePath ≫ routeShort)) ∧
    (kernelCategoryHomToKernelHom (basePath ≫ routeLong) =
      kernelCategoryHomToKernelHom (basePath ≫ routeShort)) := by
  exact exchangeQuotientOriginalMate F G modsA modsC f uF uG vF vG wF wG pqA pqC
    (Grid.ExchangeClass.append exchangeAB exchangeBC) basePath

/-- Original crossed lax right-mate coherence survives an arbitrary
second (potentially NONINVERTIBLE) quotient NatTrans for ANY exchange. -/
theorem exchangeQuotientVerticalMate
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
    (exchange : Grid.ExchangeClass n m modsA modsB pqA pqB)
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
  exact finiteTraceRectangleVerticalMate F G modsA modsB f uF uG vF vG wF wG T β pqA pqB
    (Grid.ExchangeClass.toInterleaving exchange).toRectangleTrace basePath

/-- The same after TWO genuine interleaved original refinement paths,
without reordering F/G nonstrict comparisons or assuming invertibility. -/
theorem exchangeQuotientVerticalMateTrans
    {a b : LeftMatePresentation F G}
    (modsA modsB modsC : Grid.Blocks a b)
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
    (pqA pqB pqC : Grid.Blocks x y)
    {n₁ n₂ m₁ m₂ : Nat}
    (exchangeAB : Grid.ExchangeClass n₁ m₁ modsA modsB pqA pqB)
    (exchangeBC : Grid.ExchangeClass n₂ m₂ modsB modsC pqB pqC)
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
      (β.app x ≫ T.map pqC.composite)
    ((Grid.mapBlocks (rightMateFunctor F G) modsA).composite =
      (Grid.mapBlocks (rightMateFunctor F G) modsC).composite) ∧
    (kernelCategoryLeftMateBoundary a.core.datum b.core.datum
        modsA.composite f (basePath ≫ routeLong) =
      kernelCategoryLeftMateBoundary a.core.datum b.core.datum
        modsC.composite f (basePath ≫ routeShort) ∧
     kernelCategoryRightMateBoundary a.core.datum b.core.datum
        modsA.composite f (basePath ≫ routeLong) =
      kernelCategoryRightMateBoundary a.core.datum b.core.datum
        modsC.composite f (basePath ≫ routeShort) ∧
     kernelCategoryLeftMateBoundary a.core.datum b.core.datum
        modsA.composite f (basePath ≫ routeLong) =
      kernelCategoryRightMateBoundary a.core.datum b.core.datum
        modsC.composite f (basePath ≫ routeShort)) ∧
    (kernelCategoryHomToKernelHom (basePath ≫ routeLong) =
      kernelCategoryHomToKernelHom (basePath ≫ routeShort)) := by
  exact exchangeQuotientVerticalMate F G modsA modsC f uF uG vF vG wF wG T β pqA pqC
    (Grid.ExchangeClass.append exchangeAB exchangeBC) basePath

#print axioms chosenRightMateExchangeQuotientTransport
#print axioms exchangeQuotientOriginalMate
#print axioms exchangeQuotientOriginalMateTrans
#print axioms exchangeQuotientVerticalMate
#print axioms exchangeQuotientVerticalMateTrans

end Generic
end

end KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientMateCoherenceV5_141
