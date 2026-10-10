import KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137
import KUOS.DependentOriginationCoherentBiadjunctionDoubleFiniteHexagonMatesV5_135

namespace KUOS.DependentOriginationCoherentBiadjunctionRectangularBlockMateNaturalityV5_137

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionFiniteHorizontalExchangeV5_133
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137
open KUOS.DependentOriginationCoherentBiadjunctionFiniteModificationMatePathsV5_135
open KUOS.DependentOriginationCoherentBiadjunctionFiniteModificationMatePathsV5_135.Generic
open KUOS.DependentOriginationCoherentBiadjunctionDoubleFiniteHexagonMatesV5_135.Generic
open KUOS.DependentOriginationCoherentBiadjunctionChosenRightMateCategoriesV5_116.Generic
open KUOS.DependentOriginationCoherentBiadjunctionCompressionKernelQuotientCategoryV5_125.Generic
open KUOS.DependentOriginationCoherentBiadjunctionHorizontalQuotientFunctorsV5_127.Generic
open KUOS.DependentOriginationCoherentBiadjunctionKernelQuotientMateBoundaryBridgeV5_130.Generic
open KUOS.DependentOriginationCoherentBiadjunctionStagewiseQuotientMixedHexagonV5_132.Generic
open KUOS.DependentOriginationCoherentBiadjunctionArbitraryModificationMatesV5_113.Generic

set_option autoImplicit false
noncomputable section

/-!
# F40-B/v5.137: arbitrary finite rectangular subdivision of two axes

The vertical axis has an arbitrary finite number of F19 ORIGINAL
StrongTrans.Modification blocks, with EACH block itself containing
an arbitrary finite number of those original strong modifications.
The horizontal axis independently has an arbitrary finite number
of F28 genuine compression-kernel quotient CATEGORY comparison blocks.
Each block may be empty; there is NO identification with F26 chains.

The entire F19 sequence is transported contravariantly through the
ORIGINAL chosen-mate functor, block by block. The ORIGINAL four-stage
F35 mixed associator hexagon is pasted against the entire F28 axis,
and EXACT ORIGINAL F25/F33 left/right/cross lax mate boundaries and
the original F25 KernelHom class agree. An additional arbitrary
possibly noninvertible quotient NatTrans may be vertically pasted.

This is rectangular TWO-AXIS finite subdivision coherence in ordinary
categories, not a generic two-dimensional array of higher 2-cells.
No F/G strictification or new chosen adjunctions are introduced.
-/

namespace Generic

universe uB vB wB uC vC wC
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]
variable (F G : Pseudofunctor B C)

/-- Arbitrarily many INDEPENDENT finite blocks on BOTH original axes
preserve the full original right-mate boundary crossed square and
native F25 kernel class after the genuine four-stage hexagon. -/
theorem rectangularBlocksOriginalMate
    {a b : LeftMatePresentation F G}
    (mods : Grid.Blocks a b)
    {X Y : B} (f : X ⟶ Y)
    {aF bF aG bG eF eG : C}
    (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (vF : F.obj X ⟶ eF) (vG : G.obj X ⟶ eG)
    (wF : bF ⟶ F.obj Y) (wG : bG ⟶ G.obj Y)
    {x y : compressionKernelCategory aF bF aG bG}
    (pq : Grid.Blocks x y)
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
    let routeLong := L.map pq.composite ≫ hexagon.hom.app y
    let routeShort := hexagon.hom.app x ≫ R.map pq.composite
    ((rightMateFunctor F G).map mods.composite =
      (Grid.mapBlocks (rightMateFunctor F G) mods).composite) ∧
    (kernelCategoryLeftMateBoundary a.core.datum b.core.datum
        mods.composite f (basePath ≫ routeLong) =
      kernelCategoryLeftMateBoundary a.core.datum b.core.datum
        mods.composite f (basePath ≫ routeShort) ∧
     kernelCategoryRightMateBoundary a.core.datum b.core.datum
        mods.composite f (basePath ≫ routeLong) =
      kernelCategoryRightMateBoundary a.core.datum b.core.datum
        mods.composite f (basePath ≫ routeShort) ∧
     kernelCategoryLeftMateBoundary a.core.datum b.core.datum
        mods.composite f (basePath ≫ routeLong) =
      kernelCategoryRightMateBoundary a.core.datum b.core.datum
        mods.composite f (basePath ≫ routeShort)) ∧
    (kernelCategoryHomToKernelHom (basePath ≫ routeLong) =
      kernelCategoryHomToKernelHom (basePath ≫ routeShort)) := by
  have h := doubleFiniteModificationHexagonMateInterchange F G
    mods.flatten f uF uG vF vG wF wG pq.flatten basePath
  refine ⟨(Grid.mapBlocks_composite (rightMateFunctor F G) mods).symm, ?_, ?_⟩
  · simpa only [Grid.Blocks.composite_eq_flatten] using h.2.1
  · simpa only [Grid.Blocks.composite_eq_flatten] using h.2.2

/-- Rectangular subdivision coherence also survives a SECOND arbitrary
noninvertible quotient natural-transformation vertical pasting. -/
theorem rectangularBlocksVerticalOriginalMate
    {a b : LeftMatePresentation F G}
    (mods : Grid.Blocks a b)
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
    (pq : Grid.Blocks x y)
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
    let routeLong := (L.map pq.composite ≫ hexagon.hom.app y) ≫ β.app y
    let routeShort := hexagon.hom.app x ≫
      (β.app x ≫ T.map pq.composite)
    ((rightMateFunctor F G).map mods.composite =
      (Grid.mapBlocks (rightMateFunctor F G) mods).composite) ∧
    (kernelCategoryLeftMateBoundary a.core.datum b.core.datum
        mods.composite f (basePath ≫ routeLong) =
      kernelCategoryLeftMateBoundary a.core.datum b.core.datum
        mods.composite f (basePath ≫ routeShort) ∧
     kernelCategoryRightMateBoundary a.core.datum b.core.datum
        mods.composite f (basePath ≫ routeLong) =
      kernelCategoryRightMateBoundary a.core.datum b.core.datum
        mods.composite f (basePath ≫ routeShort) ∧
     kernelCategoryLeftMateBoundary a.core.datum b.core.datum
        mods.composite f (basePath ≫ routeLong) =
      kernelCategoryRightMateBoundary a.core.datum b.core.datum
        mods.composite f (basePath ≫ routeShort)) ∧
    (kernelCategoryHomToKernelHom (basePath ≫ routeLong) =
      kernelCategoryHomToKernelHom (basePath ≫ routeShort)) := by
  have h := doubleFiniteModificationHexagonVerticalPasting F G
    mods.flatten f uF uG vF vG wF wG T β pq.flatten basePath
  refine ⟨(Grid.mapBlocks_composite (rightMateFunctor F G) mods).symm, ?_, ?_⟩
  · simpa only [Grid.Blocks.composite_eq_flatten] using h.2.1
  · simpa only [Grid.Blocks.composite_eq_flatten] using h.2.2

#print axioms rectangularBlocksOriginalMate
#print axioms rectangularBlocksVerticalOriginalMate

end Generic

end

end KUOS.DependentOriginationCoherentBiadjunctionRectangularBlockMateNaturalityV5_137
