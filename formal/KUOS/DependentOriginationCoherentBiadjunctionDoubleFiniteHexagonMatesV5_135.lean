import KUOS.DependentOriginationCoherentBiadjunctionFiniteModificationMatePathsV5_135
import KUOS.DependentOriginationCoherentBiadjunctionFiniteHexagonOriginalMatesV5_134

namespace KUOS.DependentOriginationCoherentBiadjunctionDoubleFiniteHexagonMatesV5_135

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionFiniteHorizontalExchangeV5_133
open KUOS.DependentOriginationCoherentBiadjunctionFiniteHexagonOriginalMatesV5_134.Generic
open KUOS.DependentOriginationCoherentBiadjunctionFiniteModificationMatePathsV5_135
open KUOS.DependentOriginationCoherentBiadjunctionFiniteModificationMatePathsV5_135.Generic
open KUOS.DependentOriginationCoherentBiadjunctionChosenRightMateCategoriesV5_116.Generic
open KUOS.DependentOriginationCoherentBiadjunctionCompressionKernelQuotientCategoryV5_125.Generic
open KUOS.DependentOriginationCoherentBiadjunctionHorizontalQuotientFunctorsV5_127.Generic
open KUOS.DependentOriginationCoherentBiadjunctionKernelQuotientMateBoundaryBridgeV5_130.Generic
open KUOS.DependentOriginationCoherentBiadjunctionStagewiseQuotientMixedHexagonV5_132.Generic
open KUOS.DependentOriginationCoherentBiadjunctionAutomaticModificationMatesV5_114.Generic
open KUOS.DependentOriginationCoherentBiadjunctionArbitraryModificationMatesV5_113.Generic

set_option autoImplicit false
noncomputable section

/-!
# F38-B/v5.135: two independent arbitrary finite axes

The first axis is a finite sequence of ORIGINAL strong modifications in
the F19 category of chosen adjunct presentations. The second axis is
an arbitrary finite sequence of genuine F28 quotient-category comparison
arrows; it is deliberately NOT identified with the F26 finite chain.

The F19 rightMateFunctor carries the ENTIRE first axis, contravariantly
on the unchanged right lax mates; the F37 four-stage hexagon preserves
the original F25/F33 mate boundaries along the ENTIRE second axis.
Both statements are proved TOGETHER for the very same finite input,
original adjunctions and arbitrary (possibly noninvertible) G-cells.
-/

namespace Generic

universe uB vB wB uC vC wC
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]
variable (F G : Pseudofunctor B C)

/-- Exact two-independent-finite-axes interchange:
the entire strong-modification path is transported by the ACTUAL
contravariant right-mate functor, while the ORIGINAL F25/F33 lax mate
boundary and ORIGINAL KernelHom class stay invariant under the
four-stage F35 hexagon pasted along an arbitrary finite F28 path. -/
theorem doubleFiniteModificationHexagonMateInterchange
    {a b : LeftMatePresentation F G}
    (mods : Chain.Path a b)
    {X Y : B} (f : X ⟶ Y)
    {aF bF aG bG eF eG : C}
    (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (vF : F.obj X ⟶ eF) (vG : G.obj X ⟶ eG)
    (wF : bF ⟶ F.obj Y) (wG : bG ⟶ G.obj Y)
    {x y : compressionKernelCategory aF bF aG bG}
    (pq : Chain.Path x y)
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
      (Finite.mapPath (rightMateFunctor F G) mods).composite) ∧
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
  refine ⟨(chosenRightMateFiniteModificationPath F G mods).symm, ?_, ?_⟩
  · exact finiteStagewiseHexagonOriginalMateNaturality
      a.core.datum b.core.datum mods.composite f
      uF uG vF vG wF wG pq basePath
  · exact finiteStagewiseHexagonOriginalKernelClass
      (F := F) (G := G) f
      uF uG vF vG wF wG pq basePath

/-- Stronger F38 interchange: the second quotient naturality axis may
also be followed by an ARBITRARY, potentially noninvertible NatTrans.
Both original F33 crossed mate squares, the original F25 kernel class,
and the reverse-order right mate of every strong modification survive. -/
theorem doubleFiniteModificationHexagonVerticalPasting
    {a b : LeftMatePresentation F G}
    (mods : Chain.Path a b)
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
    (pq : Chain.Path x y)
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
      (Finite.mapPath (rightMateFunctor F G) mods).composite) ∧
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
  refine ⟨(chosenRightMateFiniteModificationPath F G mods).symm, ?_, ?_⟩
  · exact finiteStagewiseHexagonVerticalOriginalMateNaturality
      a.core.datum b.core.datum mods.composite f
      uF uG vF vG wF wG T β pq basePath
  · exact finiteStagewiseHexagonVerticalOriginalKernelClass
      (F := F) (G := G) f
      uF uG vF vG wF wG T β pq basePath

#print axioms doubleFiniteModificationHexagonMateInterchange
#print axioms doubleFiniteModificationHexagonVerticalPasting

end Generic
end

end KUOS.DependentOriginationCoherentBiadjunctionDoubleFiniteHexagonMatesV5_135
