import KUOS.DependentOriginationCoherentBiadjunctionHorizontalAssociatorUnitorCompositeV5_128

namespace KUOS.DependentOriginationCoherentBiadjunctionHorizontalQuotientAssociatorV5_128

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionCompressionKernelQuotientCategoryV5_125.Generic
open KUOS.DependentOriginationCoherentBiadjunctionHorizontalQuotientFunctorsV5_127.Generic
open KUOS.DependentOriginationCoherentBiadjunctionHorizontalAssociatorUnitorCompositeV5_128.Generic

set_option autoImplicit false
noncomputable section

/-!
# F31/v5.128: nonstrict bicategorical associators descend as genuine
natural isomorphisms of the actual F28 compression-kernel QUOTIENT categories.

F28's quotient-to-composite functors are FULL+FAITHFUL, so the actual
bicategorical associator comparison in F31-A can be lifted uniquely
back to a QUOTIENT natural isomorphism. Each quotient naturality proof
uses the original F30 compression equations, not an invented strictness
assumption. G comparison arrows remain potentially NONINVERTIBLE.
-/

namespace Generic

universe uC vC wC
variable {C : Type uC} [Bicategory.{wC, vC} C]

/-- The exact F30 LEFT horizontal kernel-quotient functors satisfy
the ORIGINAL nonstrict associator law as an actual natural ISO,
not merely pointwise equality of compressed comparison pairs. -/
def leftKernelQuotientAssociatorNatIso
    (aF bF aG bG : C)
    {eF eG dF dG : C}
    (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (vF : dF ⟶ eF) (vG : dG ⟶ eG) :
    leftKernelQuotientWhiskerFunctor aF bF aG bG
        (vF ≫ uF) (vG ≫ uG) ≅
      (leftKernelQuotientWhiskerFunctor aF bF aG bG uF uG ⋙
        leftKernelQuotientWhiskerFunctor eF bF eG bG vF vG) :=
  NatIso.ofComponents
    (fun x => (quotientCompositeFunctor dF bF dG bG).preimageIso
      ((leftCompositeAssociatorNatIso aF bF aG bG uF uG vF vG).app
        ((quotientCompositeFunctor aF bF aG bG).obj x)))
    (by
      intro x y pq
      apply (quotientCompositeFunctor dF bF dG bG).map_injective
      simpa only [Functor.map_comp, Functor.comp_map,
        Functor.preimageIso_hom, Functor.map_preimage,
        leftKernelQuotientWhisker_compression]
        using (leftCompositeAssociatorNatIso aF bF aG bG
          uF uG vF vG).hom.naturality
            ((quotientCompositeFunctor aF bF aG bG).map pq))

#print axioms leftKernelQuotientAssociatorNatIso

end Generic

end

end KUOS.DependentOriginationCoherentBiadjunctionHorizontalQuotientAssociatorV5_128
