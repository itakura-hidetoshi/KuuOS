import KUOS.DependentOriginationCoherentBiadjunctionDoubleFiniteHexagonAppendV5_136
import KUOS.DependentOriginationCoherentBiadjunctionDoubleFiniteHexagonMatesV5_135

namespace KUOS.DependentOriginationCoherentBiadjunctionDoubleBracketedHexagonMatesV5_136

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionFiniteHorizontalExchangeV5_133
open KUOS.DependentOriginationCoherentBiadjunctionFiniteModificationMatePathsV5_135
open KUOS.DependentOriginationCoherentBiadjunctionFiniteModificationMatePathsV5_135.Generic
open KUOS.DependentOriginationCoherentBiadjunctionDoubleFinitePastingCoreV5_136.Finite
open KUOS.DependentOriginationCoherentBiadjunctionDoubleFiniteHexagonMatesV5_135.Generic
open KUOS.DependentOriginationCoherentBiadjunctionChosenRightMateCategoriesV5_116.Generic
open KUOS.DependentOriginationCoherentBiadjunctionCompressionKernelQuotientCategoryV5_125.Generic
open KUOS.DependentOriginationCoherentBiadjunctionHorizontalQuotientFunctorsV5_127.Generic
open KUOS.DependentOriginationCoherentBiadjunctionKernelQuotientMateBoundaryBridgeV5_130.Generic
open KUOS.DependentOriginationCoherentBiadjunctionStagewiseQuotientMixedHexagonV5_132.Generic

set_option autoImplicit false
noncomputable section

/-!
# F39-C/v5.136 — simultaneous arbitrary binary-bracketing independence

Two independently chosen F19 strong-modification vertical pastings
with the same ordered flattened original modifications, and TWO
independently chosen F28 genuine quotient comparison horizontal
pastings with the same ordered flattened quotient arrows, yield exactly
the same right-mate modification, the same original F25 KernelHom
class, and all THREE original F25/F33 left/right/CROSS mate boundaries.
The comparison remains true with a second arbitrary noninvertible
quotient NatTrans pasted after the four-stage F35 hexagon.

This is not equality of F26 comparison chains with F28 Hom types.
No original strong/lax comparison is strictified or inverted on G.
-/

namespace Generic

universe uB vB wB uC vC wC
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]
variable (F G : Pseudofunctor B C)

/-- ANY independent binary regroupings of both finite axes preserve
the original lax right-mate crossed F33 square and F25 kernel class. -/
theorem doubleBracketedHexagonMateIndependence
    {a b : LeftMatePresentation F G}
    (modsA modsB : Chain.Bracketing a b)
    (hmods : modsA.flattened = modsB.flattened)
    {X Y : B} (f : X ⟶ Y)
    {aF bF aG bG eF eG : C}
    (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (vF : F.obj X ⟶ eF) (vG : G.obj X ⟶ eG)
    (wF : bF ⟶ F.obj Y) (wG : bG ⟶ G.obj Y)
    {x y : compressionKernelCategory aF bF aG bG}
    (pqA pqB : Chain.Bracketing x y)
    (hpq : pqA.flattened = pqB.flattened)
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
    let routeLong := L.map pqA.evaluated ≫ hexagon.hom.app y
    let routeShort := hexagon.hom.app x ≫ R.map pqB.evaluated
    ((Finite.mapBracketing (rightMateFunctor F G) modsA).evaluated =
      (Finite.mapBracketing (rightMateFunctor F G) modsB).evaluated) ∧
    (kernelCategoryLeftMateBoundary a.core.datum b.core.datum
        modsA.evaluated f (basePath ≫ routeLong) =
      kernelCategoryLeftMateBoundary a.core.datum b.core.datum
        modsB.evaluated f (basePath ≫ routeShort) ∧
     kernelCategoryRightMateBoundary a.core.datum b.core.datum
        modsA.evaluated f (basePath ≫ routeLong) =
      kernelCategoryRightMateBoundary a.core.datum b.core.datum
        modsB.evaluated f (basePath ≫ routeShort) ∧
     kernelCategoryLeftMateBoundary a.core.datum b.core.datum
        modsA.evaluated f (basePath ≫ routeLong) =
      kernelCategoryRightMateBoundary a.core.datum b.core.datum
        modsB.evaluated f (basePath ≫ routeShort)) ∧
    (kernelCategoryHomToKernelHom (basePath ≫ routeLong) =
      kernelCategoryHomToKernelHom (basePath ≫ routeShort)) := by
  have hm : modsA.evaluated = modsB.evaluated :=
    Chain.Bracketing.independent modsA modsB hmods
  have hq : pqA.evaluated = pqB.evaluated :=
    Chain.Bracketing.independent pqA pqB hpq
  have h := doubleFiniteModificationHexagonMateInterchange F G
    modsA.flattened f uF uG vF vG wF wG pqA.flattened basePath
  refine ⟨Finite.mapBracketing_independent
    (rightMateFunctor F G) modsA modsB hmods, ?_, ?_⟩
  · rw [← hm, ← hq]
    simpa only [Chain.Bracketing.evaluated_eq_flattened] using h.2.1
  · rw [← hq]
    simpa only [Chain.Bracketing.evaluated_eq_flattened] using h.2.2

/-- Same two-axis arbitrary-regrouping independence even after a
SECOND potentially noninvertible quotient natural transformation. -/
theorem doubleBracketedHexagonVerticalMateIndependence
    {a b : LeftMatePresentation F G}
    (modsA modsB : Chain.Bracketing a b)
    (hmods : modsA.flattened = modsB.flattened)
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
    (pqA pqB : Chain.Bracketing x y)
    (hpq : pqA.flattened = pqB.flattened)
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
      kernelCategoryHomToKernelHom (basePath ≫ routeShort))    let hexagon := kernelMixedHexagonStagewiseLongNatIso
      aF bF aG bG uF uG vF vG wF wG
    let routeLong := (L.map pqA.evaluated ≫ hexagon.hom.app y) ≫ β.app y
    let routeShort := hexagon.hom.app x ≫
      (β.app x ≫ T.map pqB.evaluated)
    ((Finite.mapBracketing (rightMateFunctor F G) modsA).evaluated =
      (Finite.mapBracketing (rightMateFunctor F G) modsB).evaluated) ∧
    (kernelCategoryLeftMateBoundary a.core.datum b.core.datum
        modsA.evaluated f (basePath ≫ routeLong) =
      kernelCategoryLeftMateBoundary a.core.datum b.core.datum
        modsB.evaluated f (basePath ≫ routeShort) ∧
     kernelCategoryRightMateBoundary a.core.datum b.core.datum
        modsA.evaluated f (basePath ≫ routeLong) =
      kernelCategoryRightMateBoundary a.core.datum b.core.datum
        modsB.evaluated f (basePath ≫ routeShort) ∧
     kernelCategoryLeftMateBoundary a.core.datum b.core.datum
        modsA.evaluated f (basePath ≫ routeLong) =
      kernelCategoryRightMateBoundary a.core.datum b.core.datum
        modsB.evaluated f (basePath ≫ routeShort)) ∧
    (kernelCategoryHomToKernelHom (basePath ≫ routeLong) =
      kernelCategoryHomToKernelHom (basePath ≫ routeShort)) := by
  have hm : modsA.evaluated = modsB.evaluated :=
    Chain.Bracketing.independent modsA modsB hmods
  have hq : pqA.evaluated = pqB.evaluated :=
    Chain.Bracketing.independent pqA pqB hpq
  have h := doubleFiniteModificationHexagonVerticalPasting F G
    modsA.flattened f uF uG vF vG wF wG T β pqA.flattened basePath
  refine ⟨Finite.mapBracketing_independent
    (rightMateFunctor F G) modsA modsB hmods, ?_, ?_⟩
  · rw [← hm, ← hq]
    simpa only [Chain.Bracketing.evaluated_eq_flattened] using h.2.1
  · rw [← hq]
    simpa only [Chain.Bracketing.evaluated_eq_flattened] using h.2.2

#print axioms doubleBracketedHexagonMateIndependence
#print axioms doubleBracketedHexagonVerticalMateIndependence

end Generic
end

end KUOS.DependentOriginationCoherentBiadjunctionDoubleBracketedHexagonMatesV5_136
