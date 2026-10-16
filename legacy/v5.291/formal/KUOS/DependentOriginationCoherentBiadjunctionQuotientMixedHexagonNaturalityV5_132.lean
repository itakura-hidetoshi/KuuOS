import KUOS.DependentOriginationCoherentBiadjunctionMixedAssociatorHexagonV5_132

namespace KUOS.DependentOriginationCoherentBiadjunctionQuotientMixedHexagonNaturalityV5_132

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionComparisonCompressionFunctorV5_124.Generic
open KUOS.DependentOriginationCoherentBiadjunctionCompressionKernelQuotientCategoryV5_125.Generic
open KUOS.DependentOriginationCoherentBiadjunctionHorizontalQuotientFunctorsV5_127.Generic
open KUOS.DependentOriginationCoherentBiadjunctionKernelQuotientHorizontalExchangeV5_131.Generic
open KUOS.DependentOriginationCoherentBiadjunctionMixedAssociatorHexagonV5_132.Generic

set_option autoImplicit false
noncomputable section

/-!
# F35/v5.132 — mixed associator hexagon as a GENUINE QUOTIENT NatIso equality

Lift the ORIGINAL F31/F34 four-stage mixed-associator hexagon from F27's
true composite comparison category through the proven F28 FULL+FAITHFUL
compression-kernel quotient functor. The resulting components are
actual isomorphisms IN THE QUOTIENT CATEGORY. They form a genuine NatIso
for all original arrows, with arbitrary potentially noninvertible G
comparison 2-cells. This new NatIso is exactly the F34 natural exchange
with the composite outer-left 1-cell, as equality of WHOLE NatIso values.
-/

namespace Generic

universe uC vC wC
variable {C : Type uC} [Bicategory.{wC, vC} C]

/-- The actual FOUR-STEP structural F31/F34 path independently
lifted into the original F28 kernel quotient Hom by the exact
full+faithful F28 quotient-to-composite functor. -/
def kernelMixedHexagonLongComponent (aF bF aG bG : C)
    {eF eG dF dG cF cG : C}
    (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (vF : dF ⟶ eF) (vG : dG ⟶ eG)
    (wF : bF ⟶ cF) (wG : bG ⟶ cG)
    (x : compressionKernelCategory aF bF aG bG) :
    ((leftKernelQuotientWhiskerFunctor aF bF aG bG
      (vF ≫ uF) (vG ≫ uG) ⋙
      rightKernelQuotientWhiskerFunctor dF bF dG bG wF wG).obj x) ≅
    ((rightKernelQuotientWhiskerFunctor aF bF aG bG wF wG ⋙
      leftKernelQuotientWhiskerFunctor aF cF aG cG
        (vF ≫ uF) (vG ≫ uG)).obj x) :=
  (quotientCompositeFunctor dF cF dG cG).preimageIso
    (compositeMixedHexagonLongIso aF bF aG bG
      uF uG vF vG wF wG
      ((quotientCompositeFunctor aF bF aG bG).obj x))

/-- A genuine F28 QUOTIENT structural isomorphism realizing the four
F31/F34 steps is exactly the component of the ORIGINAL F34 natural
exchange. The proof descends via the fully faithful F28 functor and
uses the original F35 pentagon, without identifying quotient paths. -/
theorem kernelMixedHexagonLongComponent_eq_exchange (aF bF aG bG : C)
    {eF eG dF dG cF cG : C}
    (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (vF : dF ⟶ eF) (vG : dG ⟶ eG)
    (wF : bF ⟶ cF) (wG : bG ⟶ cG)
    (x : compressionKernelCategory aF bF aG bG) :
    kernelMixedHexagonLongComponent aF bF aG bG
      uF uG vF vG wF wG x =
    (kernelQuotientHorizontalExchangeNatIso aF bF aG bG
      (vF ≫ uF) (vG ≫ uG) wF wG).app x := by
  apply Iso.ext
  apply (quotientCompositeFunctor dF cF dG cG).map_injective
  change (quotientCompositeFunctor dF cF dG cG).map
      ((kernelMixedHexagonLongComponent aF bF aG bG
        uF uG vF vG wF wG x).hom) =
    (quotientCompositeFunctor dF cF dG cG).map
      ((kernelQuotientHorizontalExchangeNatIso aF bF aG bG
        (vF ≫ uF) (vG ≫ uG) wF wG).hom.app x)
  rw [kernelQuotientHorizontalExchange_compression]
  simp only [kernelMixedHexagonLongComponent,
    Functor.preimageIso_hom, Functor.map_preimage]
  change (compositeMixedHexagonLongIso aF bF aG bG
      uF uG vF vG wF wG
      ((quotientCompositeFunctor aF bF aG bG).obj x)).hom =
    (compositeMixedHexagonShortIso aF bF aG bG
      uF uG vF vG wF wG
      ((quotientCompositeFunctor aF bF aG bG).obj x)).hom
  exact congrArg Iso.hom (compositeMixedHexagon aF bF aG bG
    uF uG vF vG wF wG
    ((quotientCompositeFunctor aF bF aG bG).obj x))

/-- The ORIGINAL four-stage hexagon components assemble into a
GENUINE natural isomorphism on the actual F28 quotient categories:
its naturality handles arbitrary quotient-category morphisms, without
requiring the G comparison to be invertible. -/
def kernelMixedHexagonLongNatIso (aF bF aG bG : C)
    {eF eG dF dG cF cG : C}
    (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (vF : dF ⟶ eF) (vG : dG ⟶ eG)
    (wF : bF ⟶ cF) (wG : bG ⟶ cG) :
    (leftKernelQuotientWhiskerFunctor aF bF aG bG
      (vF ≫ uF) (vG ≫ uG) ⋙
      rightKernelQuotientWhiskerFunctor dF bF dG bG wF wG) ≅
    (rightKernelQuotientWhiskerFunctor aF bF aG bG wF wG ⋙
      leftKernelQuotientWhiskerFunctor aF cF aG cG
        (vF ≫ uF) (vG ≫ uG)) :=
  NatIso.ofComponents
    (fun x => kernelMixedHexagonLongComponent aF bF aG bG
      uF uG vF vG wF wG x)
    (by
      intro x y pq
      change
        (leftKernelQuotientWhiskerFunctor aF bF aG bG
          (vF ≫ uF) (vG ≫ uG) ⋙
          rightKernelQuotientWhiskerFunctor dF bF dG bG wF wG).map pq ≫
        (kernelMixedHexagonLongComponent aF bF aG bG
          uF uG vF vG wF wG y).hom =
        (kernelMixedHexagonLongComponent aF bF aG bG
          uF uG vF vG wF wG x).hom ≫
        (rightKernelQuotientWhiskerFunctor aF bF aG bG wF wG ⋙
          leftKernelQuotientWhiskerFunctor aF cF aG cG
            (vF ≫ uF) (vG ≫ uG)).map pq
      rw [kernelMixedHexagonLongComponent_eq_exchange
          aF bF aG bG uF uG vF vG wF wG x,
          kernelMixedHexagonLongComponent_eq_exchange
          aF bF aG bG uF uG vF vG wF wG y]
      exact (kernelQuotientHorizontalExchangeNatIso aF bF aG bG
        (vF ≫ uF) (vG ≫ uG) wF wG).hom.naturality pq)

/-- F35 higher COHERENCE as an equality of ACTUAL NatIso values
on the original F28 mathlib compression-kernel QUOTIENT CATEGORIES:
the four-stage F31/F34 pentagon hexagon and direct mixed exchange
are identical NATURAL transformations for every quotient arrow. -/
theorem kernelMixedHexagonNatIso_coherence (aF bF aG bG : C)
    {eF eG dF dG cF cG : C}
    (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (vF : dF ⟶ eF) (vG : dG ⟶ eG)
    (wF : bF ⟶ cF) (wG : bG ⟶ cG) :
    kernelMixedHexagonLongNatIso aF bF aG bG
      uF uG vF vG wF wG =
    kernelQuotientHorizontalExchangeNatIso aF bF aG bG
      (vF ≫ uF) (vG ≫ uG) wF wG := by
  apply Iso.ext
  apply NatTrans.ext
  funext x
  change (kernelMixedHexagonLongComponent aF bF aG bG
    uF uG vF vG wF wG x).hom =
    ((kernelQuotientHorizontalExchangeNatIso aF bF aG bG
      (vF ≫ uF) (vG ≫ uG) wF wG).app x).hom
  exact congrArg Iso.hom
    (kernelMixedHexagonLongComponent_eq_exchange aF bF aG bG
      uF uG vF vG wF wG x)

#print axioms kernelMixedHexagonLongComponent
#print axioms kernelMixedHexagonLongComponent_eq_exchange
#print axioms kernelMixedHexagonLongNatIso
#print axioms kernelMixedHexagonNatIso_coherence

end Generic

end

end KUOS.DependentOriginationCoherentBiadjunctionQuotientMixedHexagonNaturalityV5_132
