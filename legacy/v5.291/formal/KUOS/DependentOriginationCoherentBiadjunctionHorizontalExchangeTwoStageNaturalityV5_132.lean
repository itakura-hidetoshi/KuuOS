import KUOS.DependentOriginationCoherentBiadjunctionActualLiftHorizontalExchangeV5_131

namespace KUOS.DependentOriginationCoherentBiadjunctionHorizontalExchangeTwoStageNaturalityV5_132

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionCompressionKernelQuotientCategoryV5_125.Generic
open KUOS.DependentOriginationCoherentBiadjunctionHorizontalQuotientFunctorsV5_127.Generic
open KUOS.DependentOriginationCoherentBiadjunctionKernelQuotientHorizontalExchangeV5_131.Generic

set_option autoImplicit false
noncomputable section

/-!
# F35/v5.132: vertical pasting of mixed horizontal-exchange NATURALITY squares

F34 provides a genuine NatIso between left-then-right and right-then-left
whiskering functors on the original F28 comparison-kernel quotient
category. F35 proves the vertical pasting law for TWO independent
quotient arrows with an arbitrary intermediate comparison object,
without any invertibility condition on their G-side comparison 2-cells.

The component at the intermediate object must genuinely appear; the
proof pastes the TWO original naturality squares with their exact
composition order, not only the naturality of a precomposed arrow.
-/

namespace Generic

universe uC vC wC
variable {C : Type uC} [Bicategory.{wC, vC} C]

/-- Two genuinely separate F34 quotient naturality squares paste
vertically at any intermediate comparison object. The original
component of the exchange at that intermediate object is retained
until the two squares are composed. -/
theorem kernelHorizontalExchangeTwoStageNaturality
    (aF bF aG bG : C)
    {eF eG dF dG : C}
    (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (vF : bF ⟶ dF) (vG : bG ⟶ dG)
    {x y z : compressionKernelCategory aF bF aG bG}
    (q : x ⟶ y) (r : y ⟶ z) :
    let L := leftKernelQuotientWhiskerFunctor aF bF aG bG uF uG ⋙
      rightKernelQuotientWhiskerFunctor eF bF eG bG vF vG
    let R := rightKernelQuotientWhiskerFunctor aF bF aG bG vF vG ⋙
      leftKernelQuotientWhiskerFunctor aF dF aG dG uF uG
    let exchange := kernelQuotientHorizontalExchangeNatIso
      aF bF aG bG uF uG vF vG
    (L.map q ≫ L.map r) ≫ exchange.hom.app z =
      exchange.hom.app x ≫ (R.map q ≫ R.map r) := by
  dsimp only
  let L := leftKernelQuotientWhiskerFunctor aF bF aG bG uF uG ⋙
    rightKernelQuotientWhiskerFunctor eF bF eG bG vF vG
  let R := rightKernelQuotientWhiskerFunctor aF bF aG bG vF vG ⋙
    leftKernelQuotientWhiskerFunctor aF dF aG dG uF uG
  let exchange := kernelQuotientHorizontalExchangeNatIso aF bF aG bG
    uF uG vF vG
  change (L.map q ≫ L.map r) ≫ exchange.hom.app z =
    exchange.hom.app x ≫ (R.map q ≫ R.map r)
  calc
    (L.map q ≫ L.map r) ≫ exchange.hom.app z =
      L.map q ≫ (L.map r ≫ exchange.hom.app z) :=
        Category.assoc _ _ _
    _ = L.map q ≫ (exchange.hom.app y ≫ R.map r) :=
      congrArg (fun t => L.map q ≫ t) (exchange.hom.naturality r)
    _ = (L.map q ≫ exchange.hom.app y) ≫ R.map r :=
      (Category.assoc _ _ _).symm
    _ = (exchange.hom.app x ≫ R.map q) ≫ R.map r :=
      congrArg (fun t => t ≫ R.map r) (exchange.hom.naturality q)
    _ = exchange.hom.app x ≫ (R.map q ≫ R.map r) :=
      Category.assoc _ _ _

/-- The two-stage vertically pasted mixed naturality square is
EXACTLY the single original quotient naturality square on the
composite comparison arrow, with no G-side inverse. -/
theorem kernelHorizontalExchangeTwoStage_eq_composite
    (aF bF aG bG : C)
    {eF eG dF dG : C}
    (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (vF : bF ⟶ dF) (vG : bG ⟶ dG)
    {x y z : compressionKernelCategory aF bF aG bG}
    (q : x ⟶ y) (r : y ⟶ z) :
    let L := leftKernelQuotientWhiskerFunctor aF bF aG bG uF uG ⋙
      rightKernelQuotientWhiskerFunctor eF bF eG bG vF vG
    let R := rightKernelQuotientWhiskerFunctor aF bF aG bG vF vG ⋙
      leftKernelQuotientWhiskerFunctor aF dF aG dG uF uG
    let exchange := kernelQuotientHorizontalExchangeNatIso
      aF bF aG bG uF uG vF vG
    L.map (q ≫ r) ≫ exchange.hom.app z =
      exchange.hom.app x ≫ R.map (q ≫ r) := by
  dsimp only
  simp only [Functor.map_comp]
  exact kernelHorizontalExchangeTwoStageNaturality aF bF aG bG
    uF uG vF vG q r

#print axioms kernelHorizontalExchangeTwoStageNaturality
#print axioms kernelHorizontalExchangeTwoStage_eq_composite

end Generic

end

end KUOS.DependentOriginationCoherentBiadjunctionHorizontalExchangeTwoStageNaturalityV5_132
