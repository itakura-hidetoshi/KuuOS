import KUOS.DependentOriginationCoherentBiadjunctionHorizontalQuotientAssociatorV5_128

namespace KUOS.DependentOriginationCoherentBiadjunctionHorizontalQuotientUnitorV5_128

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionCompressionKernelQuotientCategoryV5_125.Generic
open KUOS.DependentOriginationCoherentBiadjunctionHorizontalQuotientFunctorsV5_127.Generic
open KUOS.DependentOriginationCoherentBiadjunctionHorizontalAssociatorUnitorCompositeV5_128.Generic

set_option autoImplicit false
noncomputable section

/-!
# F31/v5.128: right associator and both unitors descend to the
Genuine F28 mathlib compression-kernel quotient categories.

These are ACTUAL natural ISOMORPHISMS of the native F30 horizontal
quotient functors, proved natural under arbitrary quotient 2-morphisms.
The only structural isomorphisms are the original bicategorical
associators/unitors; arbitrary G comparison arrows are not inverted.
-/

namespace Generic

universe uC vC wC
variable {C : Type uC} [Bicategory.{wC, vC} C]

/-- Original RIGHT bicategory associator descends from the F31
composite comparison natural isomorphism to the native quotient
category's two-step horizontal whiskering functors. -/
def rightKernelQuotientAssociatorNatIso
    (aF bF aG bG : C)
    {eF eG dF dG : C}
    (uF : bF ⟶ eF) (uG : bG ⟶ eG)
    (vF : eF ⟶ dF) (vG : eG ⟶ dG) :
    (rightKernelQuotientWhiskerFunctor aF bF aG bG uF uG ⋙
      rightKernelQuotientWhiskerFunctor aF eF aG eG vF vG) ≅
        rightKernelQuotientWhiskerFunctor aF bF aG bG
          (uF ≫ vF) (uG ≫ vG) :=
  NatIso.ofComponents
    (fun x => (quotientCompositeFunctor aF dF aG dG).preimageIso
      ((rightCompositeAssociatorNatIso aF bF aG bG uF uG vF vG).app
        ((quotientCompositeFunctor aF bF aG bG).obj x)))
    (by
      intro x y pq
      apply (quotientCompositeFunctor aF dF aG dG).map_injective
      simp only [Functor.map_comp, Functor.comp_map,
        Functor.preimageIso_hom, Functor.map_preimage]
      rw [rightKernelQuotientWhisker_compression aF eF aG eG vF vG
        ((rightKernelQuotientWhiskerFunctor aF bF aG bG uF uG).map pq)]
      rw [rightKernelQuotientWhisker_compression aF bF aG bG uF uG pq]
      rw [rightKernelQuotientWhisker_compression aF bF aG bG
        (uF ≫ vF) (uG ≫ vG) pq]
      exact (rightCompositeAssociatorNatIso aF bF aG bG
        uF uG vF vG).hom.naturality
          ((quotientCompositeFunctor aF bF aG bG).map pq))

/-- Left unitor is a genuine NATURAL ISO from quotient left whiskering
by the original identity 1-cells to the actual identity quotient functor. -/
def leftKernelQuotientUnitorNatIso (aF bF aG bG : C) :
    leftKernelQuotientWhiskerFunctor aF bF aG bG (𝟙 aF) (𝟙 aG) ≅
      𝟭 (compressionKernelCategory aF bF aG bG) :=
  NatIso.ofComponents
    (fun x => (quotientCompositeFunctor aF bF aG bG).preimageIso
      ((leftCompositeUnitorNatIso aF bF aG bG).app
        ((quotientCompositeFunctor aF bF aG bG).obj x)))
    (by
      intro x y pq
      apply (quotientCompositeFunctor aF bF aG bG).map_injective
      simp only [Functor.map_comp, Functor.id_map,
        Functor.preimageIso_hom, Functor.map_preimage]
      rw [leftKernelQuotientWhisker_compression aF bF aG bG
        (𝟙 aF) (𝟙 aG) pq]
      exact (leftCompositeUnitorNatIso aF bF aG bG).hom.naturality
        ((quotientCompositeFunctor aF bF aG bG).map pq))

/-- Right unitor is a genuine NATURAL ISO on the actual quotient
category, with all G-side morphisms left potentially noninvertible. -/
def rightKernelQuotientUnitorNatIso (aF bF aG bG : C) :
    rightKernelQuotientWhiskerFunctor aF bF aG bG (𝟙 bF) (𝟙 bG) ≅
      𝟭 (compressionKernelCategory aF bF aG bG) :=
  NatIso.ofComponents
    (fun x => (quotientCompositeFunctor aF bF aG bG).preimageIso
      ((rightCompositeUnitorNatIso aF bF aG bG).app
        ((quotientCompositeFunctor aF bF aG bG).obj x)))
    (by
      intro x y pq
      apply (quotientCompositeFunctor aF bF aG bG).map_injective
      simp only [Functor.map_comp, Functor.id_map,
        Functor.preimageIso_hom, Functor.map_preimage]
      rw [rightKernelQuotientWhisker_compression aF bF aG bG
        (𝟙 bF) (𝟙 bG) pq]
      exact (rightCompositeUnitorNatIso aF bF aG bG).hom.naturality
        ((quotientCompositeFunctor aF bF aG bG).map pq))

#print axioms rightKernelQuotientAssociatorNatIso
#print axioms leftKernelQuotientUnitorNatIso
#print axioms rightKernelQuotientUnitorNatIso

end Generic

end

end KUOS.DependentOriginationCoherentBiadjunctionHorizontalQuotientUnitorV5_128
