import KUOS.DependentOriginationCoherentBiadjunctionDoubleFinitePastingCoreV5_136
import KUOS.DependentOriginationCoherentBiadjunctionDoubleFiniteHexagonMatesV5_135

namespace KUOS.DependentOriginationCoherentBiadjunctionDoubleFiniteHexagonAppendV5_136

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionDoubleFiniteHexagonMatesV5_135.Generic
open KUOS.DependentOriginationCoherentBiadjunctionFiniteHorizontalExchangeV5_133
open KUOS.DependentOriginationCoherentBiadjunctionFiniteModificationMatePathsV5_135
open KUOS.DependentOriginationCoherentBiadjunctionFiniteModificationMatePathsV5_135.Generic
open KUOS.DependentOriginationCoherentBiadjunctionChosenRightMateCategoriesV5_116.Generic
open KUOS.DependentOriginationCoherentBiadjunctionCompressionKernelQuotientCategoryV5_125.Generic
open KUOS.DependentOriginationCoherentBiadjunctionHorizontalQuotientFunctorsV5_127.Generic
open KUOS.DependentOriginationCoherentBiadjunctionKernelQuotientMateBoundaryBridgeV5_130.Generic
open KUOS.DependentOriginationCoherentBiadjunctionStagewiseQuotientMixedHexagonV5_132.Generic
open KUOS.DependentOriginationCoherentBiadjunctionArbitraryModificationMatesV5_113.Generic

set_option autoImplicit false
noncomputable section

/-!
# F39-B/v5.136: INDEPENDENT finite splits in BOTH original axes

The F19 strong-modification sequence is explicitly separated into
two nonempty-or-empty finite paths, as is the F28 genuine
compression-kernel quotient-category comparison sequence. The mapped
modification path is evaluated after its separate F19 right-mate
transports; the F28 hexagon's two comparison pieces are evaluated
separately by the original F30 quotient functors. Both F25/F33
original left/right crossed lax right-mate boundaries and original F25
KernelHom classes agree after the two independent splittings.

The same equations survive vertical composition of a SECOND arbitrary
(possibly noninvertible) quotient natural transformation. F/G original
nonstrict orientation and original chosen adjuncts are unchanged.
-/

namespace Generic

universe uB vB wB uC vC wC
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]
variable (F G : Pseudofunctor B C)

/-- Simultaneous two-axis split/paste interchange through the original
FOUR-stage mixed associator hexagon and BOTH original mate boundaries. -/
theorem doubleFiniteHexagonIndependentAppend
    {a b c : LeftMatePresentation F G}
    (modsP : Chain.Path a b) (modsQ : Chain.Path b c)
    {X Y : B} (f : X ⟶ Y)
    {aF bF aG bG eF eG : C}
    (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (vF : F.obj X ⟶ eF) (vG : G.obj X ⟶ eG)
    (wF : bF ⟶ F.obj Y) (wG : bG ⟶ G.obj Y)
    {x middle y : compressionKernelCategory aF bF aG bG}
    (pqP : Chain.Path x middle) (pqQ : Chain.Path middle y)
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
    let routeLong := (L.map pqP.composite ≫ L.map pqQ.composite) ≫ hexagon.hom.app y
    let routeShort := hexagon.hom.app x ≫ (R.map pqP.composite ≫ R.map pqQ.composite)
    ((rightMateFunctor F G).map (modsP.composite ≫ modsQ.composite) =
      ((Finite.mapPath (rightMateFunctor F G) modsP).composite ≫
        (Finite.mapPath (rightMateFunctor F G) modsQ).composite)) ∧
    (kernelCategoryLeftMateBoundary a.core.datum c.core.datum
        (modsP.composite ≫ modsQ.composite) f (basePath ≫ routeLong) =
      kernelCategoryLeftMateBoundary a.core.datum c.core.datum
        (modsP.composite ≫ modsQ.composite) f (basePath ≫ routeShort) ∧
     kernelCategoryRightMateBoundary a.core.datum c.core.datum
        (modsP.composite ≫ modsQ.composite) f (basePath ≫ routeLong) =
      kernelCategoryRightMateBoundary a.core.datum c.core.datum
        (modsP.composite ≫ modsQ.composite) f (basePath ≫ routeShort) ∧
     kernelCategoryLeftMateBoundary a.core.datum c.core.datum
        (modsP.composite ≫ modsQ.composite) f (basePath ≫ routeLong) =
      kernelCategoryRightMateBoundary a.core.datum c.core.datum
        (modsP.composite ≫ modsQ.composite) f (basePath ≫ routeShort)) ∧
    (kernelCategoryHomToKernelHom (basePath ≫ routeLong) =
      kernelCategoryHomToKernelHom (basePath ≫ routeShort)) := by
  have h := doubleFiniteModificationHexagonMateInterchange F G
    (modsP.append modsQ) f uF uG vF vG wF wG (pqP.append pqQ) basePath
  simpa only [Chain.Path.composite_append, Finite.mapPath_append,
    Functor.map_comp] using h

/-- The independent split/paste comparison also commutes with any
additional noninvertible quotient natural transformation. -/
theorem doubleFiniteHexagonVerticalIndependentAppend
    {a b c : LeftMatePresentation F G}
    (modsP : Chain.Path a b) (modsQ : Chain.Path b c)
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
    {x middle y : compressionKernelCategory aF bF aG bG}
    (pqP : Chain.Path x middle) (pqQ : Chain.Path middle y)
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
    let routeLong := ((L.map pqP.composite ≫ L.map pqQ.composite) ≫ hexagon.hom.app y) ≫ β.app y
    let routeShort := hexagon.hom.app x ≫
      (β.app x ≫ (T.map pqP.composite ≫ T.map pqQ.composite))
    ((rightMateFunctor F G).map (modsP.composite ≫ modsQ.composite) =
      ((Finite.mapPath (rightMateFunctor F G) modsP).composite ≫
        (Finite.mapPath (rightMateFunctor F G) modsQ).composite)) ∧
    (kernelCategoryLeftMateBoundary a.core.datum c.core.datum
        (modsP.composite ≫ modsQ.composite) f (basePath ≫ routeLong) =
      kernelCategoryLeftMateBoundary a.core.datum c.core.datum
        (modsP.composite ≫ modsQ.composite) f (basePath ≫ routeShort) ∧
     kernelCategoryRightMateBoundary a.core.datum c.core.datum
        (modsP.composite ≫ modsQ.composite) f (basePath ≫ routeLong) =
      kernelCategoryRightMateBoundary a.core.datum c.core.datum
        (modsP.composite ≫ modsQ.composite) f (basePath ≫ routeShort) ∧
     kernelCategoryLeftMateBoundary a.core.datum c.core.datum
        (modsP.composite ≫ modsQ.composite) f (basePath ≫ routeLong) =
      kernelCategoryRightMateBoundary a.core.datum c.core.datum
        (modsP.composite ≫ modsQ.composite) f (basePath ≫ routeShort)) ∧
    (kernelCategoryHomToKernelHom (basePath ≫ routeLong) =
      kernelCategoryHomToKernelHom (basePath ≫ routeShort)) := by
  have h := doubleFiniteModificationHexagonVerticalPasting F G
    (modsP.append modsQ) f uF uG vF vG wF wG T β (pqP.append pqQ) basePath
  simpa only [Chain.Path.composite_append, Finite.mapPath_append,
    Functor.map_comp] using h

#print axioms doubleFiniteHexagonIndependentAppend
#print axioms doubleFiniteHexagonVerticalIndependentAppend

end Generic
end

end KUOS.DependentOriginationCoherentBiadjunctionDoubleFiniteHexagonAppendV5_136
