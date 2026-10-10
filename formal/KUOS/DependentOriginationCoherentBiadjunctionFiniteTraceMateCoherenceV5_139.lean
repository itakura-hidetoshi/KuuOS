import KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangleTracesV5_139
import KUOS.DependentOriginationCoherentBiadjunctionRefinementMateCoherenceV5_138

namespace KUOS.DependentOriginationCoherentBiadjunctionFiniteTraceMateCoherenceV5_139

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137
open KUOS.DependentOriginationCoherentBiadjunctionConstructiveRefinementV5_138
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangleTracesV5_139
open KUOS.DependentOriginationCoherentBiadjunctionRefinementMateCoherenceV5_138.Generic
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
# F42-C/v5.139 — original mate coherence along NAT-indexed refinement traces

The original F19 chosen StrongTrans.Modification axis uses exactly n
primitive refinement steps, while the ORIGINAL F28 quotient-comparison
axis independently uses exactly m primitive steps. The typed finite
certificates imply F41 constructive refinement via a proved theorem
rather than assuming equality of categorical composites.

The four-stage F35 hexagon, original F25/F33 left, right and cross
lax-mate boundaries, the original F25 KernelHom comparison, and
the original contravariant chosen right-mate functor are preserved.
Sequential certificates genuinely add their independent depth indices
(n1+n2, m1+m2), also with a second arbitrary NONINVERTIBLE NatTrans.

No mate square is inverted on G, no new adjunction, no F26 substitution,
and no ambient bicategory biequivalence is asserted.
-/

namespace Generic

universe uB vB wB uC vC wC
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]
variable (F G : Pseudofunctor B C)

/-- Native n/m-step two-axis traces imply the original F25/F33 lax
right-mate and four-stage mixed-hexagon coherence equations. -/
theorem finiteTraceRectangleOriginalMate
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
    (trace : Grid.RectangleTrace n m modsA modsB pqA pqB)
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
  exact constructiveRectangleOriginalMate F G modsA modsB f uF uG vF vG wF wG pqA pqB
    (Grid.RectangleTrace.toRefines trace) basePath

/-- The same original mate coherence for two successive explicit
finite trace certificates, preserving their exact independent depths. -/
theorem finiteTraceRectangleOriginalMateTrans
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
    (traceAB : Grid.RectangleTrace n₁ m₁ modsA modsB pqA pqB)
    (traceBC : Grid.RectangleTrace n₂ m₂ modsB modsC pqB pqC)
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
  exact finiteTraceRectangleOriginalMate F G modsA modsC f uF uG vF vG wF wG pqA pqC
    (Grid.RectangleTrace.trans traceAB traceBC) basePath

/-- Arbitrary potentially noninvertible quotient NatTrans preserves
both original crossed mate boundaries along two finite-depth axes. -/
theorem finiteTraceRectangleVerticalMate
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
    (trace : Grid.RectangleTrace n m modsA modsB pqA pqB)
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
  exact constructiveRectangleVerticalMate F G modsA modsB f uF uG vF vG wF wG T β pqA pqB
    (Grid.RectangleTrace.toRefines trace) basePath

/-- Sequential two-axis primitive traces compose even with the
additional noninvertible natural-transformation vertical paste. -/
theorem finiteTraceRectangleVerticalMateTrans
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
    (traceAB : Grid.RectangleTrace n₁ m₁ modsA modsB pqA pqB)
    (traceBC : Grid.RectangleTrace n₂ m₂ modsB modsC pqB pqC)
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
  exact finiteTraceRectangleVerticalMate F G modsA modsC f uF uG vF vG wF wG T β pqA pqC
    (Grid.RectangleTrace.trans traceAB traceBC) basePath

#print axioms finiteTraceRectangleOriginalMate
#print axioms finiteTraceRectangleOriginalMateTrans
#print axioms finiteTraceRectangleVerticalMate
#print axioms finiteTraceRectangleVerticalMateTrans

end Generic
end

end KUOS.DependentOriginationCoherentBiadjunctionFiniteTraceMateCoherenceV5_139
