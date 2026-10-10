import KUOS.DependentOriginationCoherentBiadjunctionCompositeHorizontalExchangeV5_131

namespace KUOS.DependentOriginationCoherentBiadjunctionKernelQuotientHorizontalExchangeV5_131

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionCompressionKernelQuotientCategoryV5_125.Generic
open KUOS.DependentOriginationCoherentBiadjunctionHorizontalQuotientFunctorsV5_127.Generic
open KUOS.DependentOriginationCoherentBiadjunctionHorizontalCompositeFunctorsV5_127.Generic
open KUOS.DependentOriginationCoherentBiadjunctionCompositeHorizontalExchangeV5_131.Generic

set_option autoImplicit false
noncomputable section

/-!
# F34/v5.131: genuine NATURAL isomorphism between mixed-direction F30
whiskering functors on the ACTUAL F28 compression-kernel quotient category.

The component is exactly the FULL+FAITHFUL inverse image of the original
F34 associator pair. Naturality holds for every native quotient arrow,
not just a selected finite comparison path. Both orders of mixed
whiskering commute with F28 compression and the ORIGINAL F27 associator
naturality (including arbitrary noninvertible G comparison arrows).
-/

namespace Generic

universe uC vC wC
variable {C : Type uC} [Bicategory.{wC, vC} C]

/-- A TRUE natural isomorphism of the F28 mathlib quotient-category
LEFT∘RIGHT and RIGHT∘LEFT F30 horizontal functors, whose components are
the same original nonstrict bicategory associators on F and G. -/
def kernelQuotientHorizontalExchangeNatIso (aF bF aG bG : C)
    {eF eG dF dG : C}
    (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (vF : bF ⟶ dF) (vG : bG ⟶ dG) :
    (leftKernelQuotientWhiskerFunctor aF bF aG bG uF uG ⋙
      rightKernelQuotientWhiskerFunctor eF bF eG bG vF vG) ≅
    (rightKernelQuotientWhiskerFunctor aF bF aG bG vF vG ⋙
      leftKernelQuotientWhiskerFunctor aF dF aG dG uF uG) :=
  NatIso.ofComponents
    (fun x => (quotientCompositeFunctor eF dF eG dG).preimageIso
      ((compositeHorizontalExchangeNatIso aF bF aG bG
        uF uG vF vG).app
        ((quotientCompositeFunctor aF bF aG bG).obj x)))
    (by
      intro x y pq
      apply (quotientCompositeFunctor eF dF eG dG).map_injective
      simp only [Functor.map_comp, Functor.comp_map,
        Functor.preimageIso_hom, Functor.map_preimage]
      have hleft :
          (quotientCompositeFunctor eF dF eG dG).map
            ((rightKernelQuotientWhiskerFunctor eF bF eG bG vF vG).map
              ((leftKernelQuotientWhiskerFunctor aF bF aG bG uF uG).map pq)) =
          (rightCompositeWhiskerFunctor eF bF eG bG vF vG).map
            ((leftCompositeWhiskerFunctor aF bF aG bG uF uG).map
              ((quotientCompositeFunctor aF bF aG bG).map pq)) := by
        calc
          _ = (rightCompositeWhiskerFunctor eF bF eG bG vF vG).map
                ((quotientCompositeFunctor eF bF eG bG).map
                  ((leftKernelQuotientWhiskerFunctor aF bF aG bG uF uG).map pq)) :=
            rightKernelQuotientWhisker_compression eF bF eG bG vF vG _
          _ = _ := congrArg
            (fun z => (rightCompositeWhiskerFunctor eF bF eG bG vF vG).map z)
            (leftKernelQuotientWhisker_compression aF bF aG bG uF uG pq)
      have hright :
          (quotientCompositeFunctor eF dF eG dG).map
            ((leftKernelQuotientWhiskerFunctor aF dF aG dG uF uG).map
              ((rightKernelQuotientWhiskerFunctor aF bF aG bG vF vG).map pq)) =
          (leftCompositeWhiskerFunctor aF dF aG dG uF uG).map
            ((rightCompositeWhiskerFunctor aF bF aG bG vF vG).map
              ((quotientCompositeFunctor aF bF aG bG).map pq)) := by
        calc
          _ = (leftCompositeWhiskerFunctor aF dF aG dG uF uG).map
                ((quotientCompositeFunctor aF dF aG dG).map
                  ((rightKernelQuotientWhiskerFunctor aF bF aG bG vF vG).map pq)) :=
            leftKernelQuotientWhisker_compression aF dF aG dG uF uG _
          _ = _ := congrArg
            (fun z => (leftCompositeWhiskerFunctor aF dF aG dG uF uG).map z)
            (rightKernelQuotientWhisker_compression aF bF aG bG vF vG pq)
      calc
        _ = (rightCompositeWhiskerFunctor eF bF eG bG vF vG).map
              ((leftCompositeWhiskerFunctor aF bF aG bG uF uG).map
                ((quotientCompositeFunctor aF bF aG bG).map pq)) ≫
              ((compositeHorizontalExchangeNatIso aF bF aG bG
                uF uG vF vG).app
                  ((quotientCompositeFunctor aF bF aG bG).obj y)).hom :=
          congrArg
            (fun z => z ≫ ((compositeHorizontalExchangeNatIso aF bF aG bG
              uF uG vF vG).app
                ((quotientCompositeFunctor aF bF aG bG).obj y)).hom)
            hleft
        _ = ((compositeHorizontalExchangeNatIso aF bF aG bG
              uF uG vF vG).app
                ((quotientCompositeFunctor aF bF aG bG).obj x)).hom ≫
              (leftCompositeWhiskerFunctor aF dF aG dG uF uG).map
                ((rightCompositeWhiskerFunctor aF bF aG bG vF vG).map
                  ((quotientCompositeFunctor aF bF aG bG).map pq)) :=
          (compositeHorizontalExchangeNatIso aF bF aG bG
            uF uG vF vG).hom.naturality
              ((quotientCompositeFunctor aF bF aG bG).map pq)
        _ = _ := congrArg
          (fun z => ((compositeHorizontalExchangeNatIso aF bF aG bG
            uF uG vF vG).app
              ((quotientCompositeFunctor aF bF aG bG).obj x)).hom ≫ z)
          hright.symm)

/-- The exact original F/G associator pair is recovered by F28
compression of each TRUE quotient NATURAL ISO component. -/
theorem kernelQuotientHorizontalExchange_compression (aF bF aG bG : C)
    {eF eG dF dG : C}
    (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (vF : bF ⟶ dF) (vG : bG ⟶ dG)
    (x : compressionKernelCategory aF bF aG bG) :
    (quotientCompositeFunctor eF dF eG dG).map
      ((kernelQuotientHorizontalExchangeNatIso aF bF aG bG
        uF uG vF vG).hom.app x) =
      (compositeHorizontalExchangeNatIso aF bF aG bG
        uF uG vF vG).hom.app
          ((quotientCompositeFunctor aF bF aG bG).obj x) := by
  simp only [kernelQuotientHorizontalExchangeNatIso,
    NatIso.ofComponents_hom_app,
    Functor.preimageIso_hom, Functor.map_preimage]

/-- Naturality of F34 is a genuine equality of two distinct
composites of F28 quotient-CATEGORY arrows, for ANY arrow `pq`. -/
theorem kernelQuotientHorizontalExchangeNaturality (aF bF aG bG : C)
    {eF eG dF dG : C}
    (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (vF : bF ⟶ dF) (vG : bG ⟶ dG)
    {x y : compressionKernelCategory aF bF aG bG}
    (pq : x ⟶ y) :
    (rightKernelQuotientWhiskerFunctor eF bF eG bG vF vG).map
      ((leftKernelQuotientWhiskerFunctor aF bF aG bG uF uG).map pq) ≫
      (kernelQuotientHorizontalExchangeNatIso aF bF aG bG
        uF uG vF vG).hom.app y =
    (kernelQuotientHorizontalExchangeNatIso aF bF aG bG
      uF uG vF vG).hom.app x ≫
      (leftKernelQuotientWhiskerFunctor aF dF aG dG uF uG).map
        ((rightKernelQuotientWhiskerFunctor aF bF aG bG vF vG).map pq) :=
  (kernelQuotientHorizontalExchangeNatIso aF bF aG bG
    uF uG vF vG).hom.naturality pq

#print axioms kernelQuotientHorizontalExchangeNatIso
#print axioms kernelQuotientHorizontalExchange_compression
#print axioms kernelQuotientHorizontalExchangeNaturality

end Generic

end

end KUOS.DependentOriginationCoherentBiadjunctionKernelQuotientHorizontalExchangeV5_131
