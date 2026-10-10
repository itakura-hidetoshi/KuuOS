import KUOS.DependentOriginationCoherentBiadjunctionF33HorizontalMateWhiskeringV5_130

namespace KUOS.DependentOriginationCoherentBiadjunctionCompositeHorizontalExchangeV5_131

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionComparisonCompressionFunctorV5_124.Generic
open KUOS.DependentOriginationCoherentBiadjunctionHorizontalCompositeFunctorsV5_127.Generic
open KUOS.DependentOriginationCoherentBiadjunctionHorizontalAssociatorUnitorCompositeV5_128.Generic

set_option autoImplicit false
noncomputable section

/-!
# F34 / v5.131: NATURAL mixed left/right whiskering exchange

F31 has natural isomorphisms for consecutively left or consecutively
right whiskering. This module constructs the MISSING mixed-direction
comparison: LEFT then RIGHT versus RIGHT then LEFT, as a genuine
natural isomorphism of the ordinary F27 composite comparison functors.

Its components are the ORIGINAL (nonstrict) bicategory associators.
Naturality is proved for the actual F 2-ISOMORPHISM and independently
for an arbitrary forward G 2-CELL, without assuming that G cell
invertible. This is stronger than pointwise associator equality.
-/

namespace Generic

universe uC vC wC
variable {C : Type uC} [Bicategory.{wC, vC} C]

/-- Actual mixed-direction exchange NATURAL ISOMORPHISM of F27
comparison functors, not merely a pointwise family of 2-isomorphisms.

The original bicategory associator carries
`(uF ≫ x.fF) ≫ vF` to `uF ≫ (x.fF ≫ vF)`, and analogously for G.
The G comparison 2-cell `pq.2` remains arbitrary/noninvertible. -/
def compositeHorizontalExchangeNatIso (aF bF aG bG : C)
    {eF eG dF dG : C}
    (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (vF : bF ⟶ dF) (vG : bG ⟶ dG) :
    (leftCompositeWhiskerFunctor aF bF aG bG uF uG ⋙
      rightCompositeWhiskerFunctor eF bF eG bG vF vG) ≅
    (rightCompositeWhiskerFunctor aF bF aG bG vF vG ⋙
      leftCompositeWhiskerFunctor aF dF aG dG uF uG) :=
  NatIso.ofComponents
    (fun x => structuralComparisonPairIso
      (α_ uF x.fF vF) (α_ uG x.fG vG))
    (by
      intro x y pq
      apply Prod.ext
      · apply Iso.ext
        change ((uF ◁ pq.1.hom) ▷ vF) ≫
            (α_ uF y.fF vF).hom =
          (α_ uF x.fF vF).hom ≫ uF ◁ (pq.1.hom ▷ vF)
        exact Bicategory.associator_naturality_middle uF pq.1.hom vF
      · change ((uG ◁ pq.2) ▷ vG) ≫
            (α_ uG y.fG vG).hom =
          (α_ uG x.fG vG).hom ≫ uG ◁ (pq.2 ▷ vG)
        exact Bicategory.associator_naturality_middle uG pq.2 vG)

/-- The genuine F34 comparison's components are EXACTLY the original
two bicategory associators, not replacements chosen after quotienting. -/
theorem compositeHorizontalExchangeNatIso_hom_app (aF bF aG bG : C)
    {eF eG dF dG : C}
    (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (vF : bF ⟶ dF) (vG : bG ⟶ dG)
    (x : CompositeComparisonPair aF bF aG bG) :
    (compositeHorizontalExchangeNatIso aF bF aG bG
      uF uG vF vG).hom.app x =
      ((α_ uF x.fF vF), (α_ uG x.fG vG).hom) := rfl

/-- THE naturality square holds for EVERY 2-morphism `pq` in
the original F27 composite comparison category. No G inverse. -/
theorem compositeHorizontalExchangeNaturality (aF bF aG bG : C)
    {eF eG dF dG : C}
    (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (vF : bF ⟶ dF) (vG : bG ⟶ dG)
    {x y : CompositeComparisonPair aF bF aG bG}
    (pq : x ⟶ y) :
    ((uF ◁ pq.1.hom) ▷ vF) ≫ (α_ uF y.fF vF).hom =
      (α_ uF x.fF vF).hom ≫ uF ◁ (pq.1.hom ▷ vF) ∧
    ((uG ◁ pq.2) ▷ vG) ≫ (α_ uG y.fG vG).hom =
      (α_ uG x.fG vG).hom ≫ uG ◁ (pq.2 ▷ vG) := by
  exact ⟨Bicategory.associator_naturality_middle uF pq.1.hom vF,
    Bicategory.associator_naturality_middle uG pq.2 vG⟩

#print axioms compositeHorizontalExchangeNatIso
#print axioms compositeHorizontalExchangeNatIso_hom_app
#print axioms compositeHorizontalExchangeNaturality

end Generic

end

end KUOS.DependentOriginationCoherentBiadjunctionCompositeHorizontalExchangeV5_131
