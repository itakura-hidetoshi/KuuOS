import KUOS.DependentOriginationCoherentBiadjunctionDoubleFiniteHexagonMatesV5_135
import KUOS.DependentOriginationCoherentBiadjunctionFiniteHexagonNonstrictMatesV5_134

namespace KUOS.DependentOriginationCoherentBiadjunctionDoubleFiniteNonstrictMatesV5_135

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionFiniteHorizontalExchangeV5_133
open KUOS.DependentOriginationCoherentBiadjunctionChosenRightMateCategoriesV5_116.Generic
open KUOS.DependentOriginationCoherentBiadjunctionFiniteModificationMatePathsV5_135.Generic
open KUOS.DependentOriginationCoherentBiadjunctionCompressionKernelQuotientCategoryV5_125.Generic
open KUOS.DependentOriginationCoherentBiadjunctionComparisonKernelHomQuotientV5_125.Generic
open KUOS.DependentOriginationCoherentBiadjunctionNonstrictKernelWhiskeringV5_126.Generic
open KUOS.DependentOriginationCoherentBiadjunctionHorizontalQuotientFunctorsV5_127.Generic
open KUOS.DependentOriginationCoherentBiadjunctionKernelQuotientMateBoundaryBridgeV5_130.Generic
open KUOS.DependentOriginationCoherentBiadjunctionNonstrictMateCoherenceV5_130.Generic
open KUOS.DependentOriginationCoherentBiadjunctionStagewiseQuotientMixedHexagonV5_132.Generic
open KUOS.DependentOriginationCoherentBiadjunctionFiniteHexagonNonstrictMatesV5_134.Generic

set_option autoImplicit false
noncomputable section

/-!
# F38-C/v5.135: two independent finite axes with ORIGINAL nonstrict cells

We combine (1) the F19 chosen right-mate functor on arbitrary finite
strong-modification paths with (2) genuine F37 finite F28 quotient
hexagon naturality in the original F/G mapId and mapComp comparisons.
The exact original right-mate lax cells are retained: F comparison
2-isos are invertible and G comparison 2-cells need NOT be.
-/

namespace Generic

universe uB vB wB uC vC wC
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]
variable (F G : Pseudofunctor B C)

/-- Original nonstrict mapId/hexagon coherence along BOTH finite axes. -/
theorem doubleFiniteModificationHexagonOriginalMapIdMateNaturality
    {a b : LeftMatePresentation F G}
    (mods : Chain.Path a b)
    (X : B)
    {aF bF aG bG eF eG : C}
    (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (vF : F.obj X ⟶ eF) (vG : G.obj X ⟶ eG)
    (wF : bF ⟶ F.obj X) (wG : bG ⟶ G.obj X)
    {x y : compressionKernelCategory aF bF aG bG}
    (p : Chain.Path x y)
    (basePath :
      (⟨⟨𝟙 (F.obj X), 𝟙 (G.obj X)⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj X) (G.obj X) (G.obj X)) ⟶
      ((leftKernelQuotientWhiskerFunctor aF bF aG bG
        (vF ≫ uF) (vG ≫ uG) ⋙
        rightKernelQuotientWhiskerFunctor (F.obj X) bF
          (G.obj X) bG wF wG).obj x)) :
    ((rightMateFunctor F G).map mods.composite =
      (Finite.mapPath (rightMateFunctor F G) mods).composite) ∧
    (let hexagon := kernelMixedHexagonStagewiseLongNatIso aF bF aG bG
      uF uG vF vG wF wG
    let routeLong := (rightKernelQuotientWhiskerFunctor (F.obj X) bF
        (G.obj X) bG wF wG).map
          ((leftKernelQuotientWhiskerFunctor aF bF aG bG
            (vF ≫ uF) (vG ≫ uG)).map p.composite) ≫ hexagon.hom.app y
    let routeShort := hexagon.hom.app x ≫
      (leftKernelQuotientWhiskerFunctor aF (F.obj X)
        aG (G.obj X) (vF ≫ uF) (vG ≫ uG)).map
        ((rightKernelQuotientWhiskerFunctor aF bF aG bG
          wF wG).map p.composite)
    let longClass := originalMapIdQuotientPrepend (F := F) (G := G) X
      (kernelCategoryHomToKernelHom (basePath ≫ routeLong))
    let shortClass := originalMapIdQuotientPrepend (F := F) (G := G) X
      (kernelCategoryHomToKernelHom (basePath ≫ routeShort))
    quotientLeftMateBoundary a.core.datum b.core.datum mods.composite (𝟙 X) longClass =
        quotientRightMateBoundary a.core.datum b.core.datum mods.composite (𝟙 X) shortClass ∧
      quotientComposite longClass = quotientComposite shortClass ) := by
  refine ⟨(chosenRightMateFiniteModificationPath F G mods).symm, ?_⟩
  exact finiteStagewiseHexagonOriginalMapIdMateNaturality
    a.core.datum b.core.datum mods.composite X
    uF uG vF vG wF wG p basePath

/-- Original nonstrict mapComp/hexagon coherence along BOTH finite axes. -/
theorem doubleFiniteModificationHexagonOriginalMapCompMateNaturality
    {a b : LeftMatePresentation F G}
    (mods : Chain.Path a b)
    {X Y Z : B} (f : X ⟶ Y) (g : Y ⟶ Z)
    {aF bF aG bG eF eG : C}
    (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (vF : F.obj X ⟶ eF) (vG : G.obj X ⟶ eG)
    (wF : bF ⟶ F.obj Z) (wG : bG ⟶ G.obj Z)
    {x y : compressionKernelCategory aF bF aG bG}
    (p : Chain.Path x y)
    (basePath :
      (⟨⟨F.map f ≫ F.map g, G.map f ≫ G.map g⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj Z) (G.obj X) (G.obj Z)) ⟶
      ((leftKernelQuotientWhiskerFunctor aF bF aG bG
        (vF ≫ uF) (vG ≫ uG) ⋙
        rightKernelQuotientWhiskerFunctor (F.obj X) bF
          (G.obj X) bG wF wG).obj x)) :
    ((rightMateFunctor F G).map mods.composite =
      (Finite.mapPath (rightMateFunctor F G) mods).composite) ∧
    (let hexagon := kernelMixedHexagonStagewiseLongNatIso aF bF aG bG
      uF uG vF vG wF wG
    let routeLong := (rightKernelQuotientWhiskerFunctor (F.obj X) bF
        (G.obj X) bG wF wG).map
          ((leftKernelQuotientWhiskerFunctor aF bF aG bG
            (vF ≫ uF) (vG ≫ uG)).map p.composite) ≫ hexagon.hom.app y
    let routeShort := hexagon.hom.app x ≫
      (leftKernelQuotientWhiskerFunctor aF (F.obj Z)
        aG (G.obj Z) (vF ≫ uF) (vG ≫ uG)).map
        ((rightKernelQuotientWhiskerFunctor aF bF aG bG
          wF wG).map p.composite)
    let longClass := originalMapCompQuotientPrepend (F := F) (G := G) f g
      (kernelCategoryHomToKernelHom (basePath ≫ routeLong))
    let shortClass := originalMapCompQuotientPrepend (F := F) (G := G) f g
      (kernelCategoryHomToKernelHom (basePath ≫ routeShort))
    quotientLeftMateBoundary a.core.datum b.core.datum mods.composite (f ≫ g) longClass =
        quotientRightMateBoundary a.core.datum b.core.datum mods.composite (f ≫ g) shortClass ∧
      quotientComposite longClass = quotientComposite shortClass ) := by
  refine ⟨(chosenRightMateFiniteModificationPath F G mods).symm, ?_⟩
  exact finiteStagewiseHexagonOriginalMapCompMateNaturality
    a.core.datum b.core.datum mods.composite f g
    uF uG vF vG wF wG p basePath

#print axioms doubleFiniteModificationHexagonOriginalMapIdMateNaturality
#print axioms doubleFiniteModificationHexagonOriginalMapCompMateNaturality

end Generic
end

end KUOS.DependentOriginationCoherentBiadjunctionDoubleFiniteNonstrictMatesV5_135
