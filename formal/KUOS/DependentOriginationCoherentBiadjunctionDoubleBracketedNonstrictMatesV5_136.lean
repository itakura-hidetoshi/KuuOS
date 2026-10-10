import KUOS.DependentOriginationCoherentBiadjunctionDoubleBracketedHexagonMatesV5_136
import KUOS.DependentOriginationCoherentBiadjunctionDoubleFiniteNonstrictMatesV5_135

namespace KUOS.DependentOriginationCoherentBiadjunctionDoubleBracketedNonstrictMatesV5_136

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionFiniteHorizontalExchangeV5_133
open KUOS.DependentOriginationCoherentBiadjunctionFiniteModificationMatePathsV5_135
open KUOS.DependentOriginationCoherentBiadjunctionFiniteModificationMatePathsV5_135.Generic
open KUOS.DependentOriginationCoherentBiadjunctionDoubleFinitePastingCoreV5_136.Finite
open KUOS.DependentOriginationCoherentBiadjunctionDoubleFiniteNonstrictMatesV5_135.Generic
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
# F39-D/v5.136 — simultaneously rebracketed ORIGINAL nonstrict data

Any two F19 finite original strong-modification pastings with the same
ordered flattened modifications and any two F28 original comparison
pastings with the same ordered flattened quotient arrows induce
the exact same original mapId/mapComp right-mate boundary pair and
F-ISO/G-forward compressed cell, even if the two axes are grouped
independently. G comparison cells need not be invertible.

Only the ORIGINAL chosen right mates, nonstrict mapId/mapComp and the
original F25/F33 kernel bridge are used.
-/

namespace Generic

universe uB vB wB uC vC wC
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]
variable (F G : Pseudofunctor B C)

/-- Original mapId boundary and F/G compressed comparison are
independent of both F19 and F28 binary pasting choices. -/
theorem doubleBracketedOriginalMapIdMateIndependence
    {a b : LeftMatePresentation F G}
    (modsA modsB : Chain.Bracketing a b)
    (hmods : modsA.flattened = modsB.flattened)
    (X : B)
    {aF bF aG bG eF eG : C}
    (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (vF : F.obj X ⟶ eF) (vG : G.obj X ⟶ eG)
    (wF : bF ⟶ F.obj X) (wG : bG ⟶ G.obj X)
    {x y : compressionKernelCategory aF bF aG bG}
    (pA pB : Chain.Bracketing x y)
    (hp : pA.flattened = pB.flattened)
    (basePath :
      (⟨⟨𝟙 (F.obj X), 𝟙 (G.obj X)⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj X) (G.obj X) (G.obj X)) ⟶
      ((leftKernelQuotientWhiskerFunctor aF bF aG bG
        (vF ≫ uF) (vG ≫ uG) ⋙
        rightKernelQuotientWhiskerFunctor (F.obj X) bF
          (G.obj X) bG wF wG).obj x)) :
    ((Finite.mapBracketing (rightMateFunctor F G) modsA).evaluated =
      (Finite.mapBracketing (rightMateFunctor F G) modsB).evaluated) ∧
    (let hexagon := kernelMixedHexagonStagewiseLongNatIso aF bF aG bG
      uF uG vF vG wF wG
    let routeLong := (rightKernelQuotientWhiskerFunctor (F.obj X) bF
        (G.obj X) bG wF wG).map
          ((leftKernelQuotientWhiskerFunctor aF bF aG bG
            (vF ≫ uF) (vG ≫ uG)).map pA.evaluated) ≫ hexagon.hom.app y
    let routeShort := hexagon.hom.app x ≫
      (leftKernelQuotientWhiskerFunctor aF (F.obj X)
        aG (G.obj X) (vF ≫ uF) (vG ≫ uG)).map
        ((rightKernelQuotientWhiskerFunctor aF bF aG bG
          wF wG).map pB.evaluated)
    let longClass := originalMapIdQuotientPrepend (F := F) (G := G) X
      (kernelCategoryHomToKernelHom (basePath ≫ routeLong))
    let shortClass := originalMapIdQuotientPrepend (F := F) (G := G) X
      (kernelCategoryHomToKernelHom (basePath ≫ routeShort))
    quotientLeftMateBoundary a.core.datum b.core.datum
        modsA.evaluated (𝟙 X) longClass =
      quotientRightMateBoundary a.core.datum b.core.datum
        modsB.evaluated (𝟙 X) shortClass ∧
      quotientComposite longClass = quotientComposite shortClass) := by
  have hm : modsA.evaluated = modsB.evaluated :=
    Chain.Bracketing.independent modsA modsB hmods
  have hpEval : pA.evaluated = pB.evaluated :=
    Chain.Bracketing.independent pA pB hp
  have h := doubleFiniteModificationHexagonOriginalMapIdMateNaturality F G modsA.flattened X
    uF uG vF vG wF wG pA.flattened basePath
  refine ⟨KUOS.DependentOriginationCoherentBiadjunctionDoubleFinitePastingCoreV5_136.Finite.mapBracketing_independent
    (rightMateFunctor F G) modsA modsB hmods, ?_⟩
  rw [← hm, ← hpEval]
  simpa only [Chain.Bracketing.evaluated_eq_flattened] using h.2

/-- Original mapComp boundary and F/G compressed comparison are
independent of both F19 and F28 binary pasting choices. -/
theorem doubleBracketedOriginalMapCompMateIndependence
    {a b : LeftMatePresentation F G}
    (modsA modsB : Chain.Bracketing a b)
    (hmods : modsA.flattened = modsB.flattened)
    {X Y Z : B} (f : X ⟶ Y) (g : Y ⟶ Z)
    {aF bF aG bG eF eG : C}
    (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (vF : F.obj X ⟶ eF) (vG : G.obj X ⟶ eG)
    (wF : bF ⟶ F.obj Z) (wG : bG ⟶ G.obj Z)
    {x y : compressionKernelCategory aF bF aG bG}
    (pA pB : Chain.Bracketing x y)
    (hp : pA.flattened = pB.flattened)
    (basePath :
      (⟨⟨F.map f ≫ F.map g, G.map f ≫ G.map g⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj Z) (G.obj X) (G.obj Z)) ⟶
      ((leftKernelQuotientWhiskerFunctor aF bF aG bG
        (vF ≫ uF) (vG ≫ uG) ⋙
        rightKernelQuotientWhiskerFunctor (F.obj X) bF
          (G.obj X) bG wF wG).obj x)) :
    ((Finite.mapBracketing (rightMateFunctor F G) modsA).evaluated =
      (Finite.mapBracketing (rightMateFunctor F G) modsB).evaluated) ∧
    (let hexagon := kernelMixedHexagonStagewiseLongNatIso aF bF aG bG
      uF uG vF vG wF wG
    let routeLong := (rightKernelQuotientWhiskerFunctor (F.obj X) bF
        (G.obj X) bG wF wG).map
          ((leftKernelQuotientWhiskerFunctor aF bF aG bG
            (vF ≫ uF) (vG ≫ uG)).map pA.evaluated) ≫ hexagon.hom.app y
    let routeShort := hexagon.hom.app x ≫
      (leftKernelQuotientWhiskerFunctor aF (F.obj Z)
        aG (G.obj Z) (vF ≫ uF) (vG ≫ uG)).map
        ((rightKernelQuotientWhiskerFunctor aF bF aG bG
          wF wG).map pB.evaluated)
    let longClass := originalMapCompQuotientPrepend (F := F) (G := G) f g
      (kernelCategoryHomToKernelHom (basePath ≫ routeLong))
    let shortClass := originalMapCompQuotientPrepend (F := F) (G := G) f g
      (kernelCategoryHomToKernelHom (basePath ≫ routeShort))
    quotientLeftMateBoundary a.core.datum b.core.datum
        modsA.evaluated (f ≫ g) longClass =
      quotientRightMateBoundary a.core.datum b.core.datum
        modsB.evaluated (f ≫ g) shortClass ∧
      quotientComposite longClass = quotientComposite shortClass) := by
  have hm : modsA.evaluated = modsB.evaluated :=
    Chain.Bracketing.independent modsA modsB hmods
  have hpEval : pA.evaluated = pB.evaluated :=
    Chain.Bracketing.independent pA pB hp
  have h := doubleFiniteModificationHexagonOriginalMapCompMateNaturality F G modsA.flattened f g
    uF uG vF vG wF wG pA.flattened basePath
  refine ⟨KUOS.DependentOriginationCoherentBiadjunctionDoubleFinitePastingCoreV5_136.Finite.mapBracketing_independent
    (rightMateFunctor F G) modsA modsB hmods, ?_⟩
  rw [← hm, ← hpEval]
  simpa only [Chain.Bracketing.evaluated_eq_flattened] using h.2

#print axioms doubleBracketedOriginalMapIdMateIndependence
#print axioms doubleBracketedOriginalMapCompMateIndependence

end Generic
end

end KUOS.DependentOriginationCoherentBiadjunctionDoubleBracketedNonstrictMatesV5_136
