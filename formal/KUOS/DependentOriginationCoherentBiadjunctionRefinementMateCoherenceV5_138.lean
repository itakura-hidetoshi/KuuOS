import KUOS.DependentOriginationCoherentBiadjunctionConstructiveRefinementV5_138
import KUOS.DependentOriginationCoherentBiadjunctionRectangularSubdivisionIndependenceV5_137

namespace KUOS.DependentOriginationCoherentBiadjunctionRefinementMateCoherenceV5_138

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionConstructiveRefinementV5_138
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137
open KUOS.DependentOriginationCoherentBiadjunctionRectangularSubdivisionIndependenceV5_137.Generic
open KUOS.DependentOriginationCoherentBiadjunctionFiniteHorizontalExchangeV5_133
open KUOS.DependentOriginationCoherentBiadjunctionChosenRightMateCategoriesV5_116.Generic
open KUOS.DependentOriginationCoherentBiadjunctionCompressionKernelQuotientCategoryV5_125.Generic
open KUOS.DependentOriginationCoherentBiadjunctionHorizontalQuotientFunctorsV5_127.Generic
open KUOS.DependentOriginationCoherentBiadjunctionKernelQuotientMateBoundaryBridgeV5_130.Generic
open KUOS.DependentOriginationCoherentBiadjunctionStagewiseQuotientMixedHexagonV5_132.Generic
open KUOS.DependentOriginationCoherentBiadjunctionArbitraryModificationMatesV5_113.Generic

set_option autoImplicit false
noncomputable section

/-!
# F41-B/v5.138 — GENERATIVE two-axis refinements through original mates

No equality of composite original F19 modification morphisms or F28
quotient comparison morphisms is given as an input. Both equalities
are DERIVED from the F41-A constructive refinement constructors:
true block split, empty block insertion, right-context extension and
arbitrarily repeated (transitive) refinement steps.

The original chosen mate functor, F35 four-stage hexagon, all three
F25/F33 right-mate boundary equations, and original F25 KernelHom
comparison are preserved under a two-axis refinement certificate.

We also prove compatibility under an ACTUAL COMPOSITION of TWO
refinement certificates, including a SECOND arbitrary potentially
noninvertible quotient natural transformation, with no inversion of
the original G-side lax comparison.
-/

namespace Generic

universe uB vB wB uC vC wC
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]
variable (F G : Pseudofunctor B C)

/-- Constructive two-axis refinement preserves the original LEFT,
RIGHT and CROSS lax mate boundaries and F25 comparison kernel. -/
theorem constructiveRectangleOriginalMate
    {a b : LeftMatePresentation F G}
    (modsA modsB : Grid.Blocks a b)
    {X Y : B} (f : X ⟶ Y)
    {aF bF aG bG eF eG : C}
    (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (vF : F.obj X ⟶ eF) (vG : G.obj X ⟶ eG)
    (wF : bF ⟶ F.obj Y) (wG : bG ⟶ G.obj Y)
    {x y : compressionKernelCategory aF bF aG bG}
    (pqA pqB : Grid.Blocks x y)
    (hrect : Grid.RectangleRefines modsA modsB pqA pqB)
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
  exact rectangularSubdivisionOriginalMateIndependent F G modsA modsB
    (Grid.Refines.composite_eq hrect.modifications)
    f uF uG vF vG wF wG pqA pqB
    (Grid.Refines.composite_eq hrect.comparisons) basePath

/-- TWO genuinely consecutive constructive grid refinements also
preserve the same ORIGINAL mate boundaries, via certified transitivity. -/
theorem constructiveRectangleOriginalMateTrans
    {a b : LeftMatePresentation F G}
    (modsA modsB modsC : Grid.Blocks a b)
    {X Y : B} (f : X ⟶ Y)
    {aF bF aG bG eF eG : C}
    (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (vF : F.obj X ⟶ eF) (vG : G.obj X ⟶ eG)
    (wF : bF ⟶ F.obj Y) (wG : bG ⟶ G.obj Y)
    {x y : compressionKernelCategory aF bF aG bG}
    (pqA pqB pqC : Grid.Blocks x y)
    (hAB : Grid.RectangleRefines modsA modsB pqA pqB)
    (hBC : Grid.RectangleRefines modsB modsC pqB pqC)
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
  exact constructiveRectangleOriginalMate F G modsA modsC
    f uF uG vF vG wF wG pqA pqC
    (Grid.RectangleRefines.trans hAB hBC) basePath

/-- The same constructive refinement descent after one further arbitrary
potentially noninvertible natural transformation. -/
theorem constructiveRectangleVerticalMate
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
    (hrect : Grid.RectangleRefines modsA modsB pqA pqB)
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
  exact rectangularSubdivisionVerticalMateIndependent F G modsA modsB
    (Grid.Refines.composite_eq hrect.modifications)
    f uF uG vF vG wF wG T β pqA pqB
    (Grid.Refines.composite_eq hrect.comparisons) basePath

/-- Transitive DOUBLE refinement remains compatible with an independent
noninvertible natural transformation pasted after the hexagon. -/
theorem constructiveRectangleVerticalMateTrans
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
    (hAB : Grid.RectangleRefines modsA modsB pqA pqB)
    (hBC : Grid.RectangleRefines modsB modsC pqB pqC)
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
  exact constructiveRectangleVerticalMate F G modsA modsC
    f uF uG vF vG wF wG T β pqA pqC
    (Grid.RectangleRefines.trans hAB hBC) basePath

#print axioms constructiveRectangleOriginalMate
#print axioms constructiveRectangleOriginalMateTrans
#print axioms constructiveRectangleVerticalMate
#print axioms constructiveRectangleVerticalMateTrans

end Generic

end

end KUOS.DependentOriginationCoherentBiadjunctionRefinementMateCoherenceV5_138
