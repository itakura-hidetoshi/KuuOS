import KUOS.DependentOriginationCoherentBiadjunctionQuotientMixedHexagonNaturalityV5_132

namespace KUOS.DependentOriginationCoherentBiadjunctionStagewiseQuotientMixedHexagonV5_132

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionCompressionKernelQuotientCategoryV5_125.Generic
open KUOS.DependentOriginationCoherentBiadjunctionKernelQuotientPentagonTriangleV5_129.Generic
open KUOS.DependentOriginationCoherentBiadjunctionHorizontalAssociatorUnitorCompositeV5_128.Generic
open KUOS.DependentOriginationCoherentBiadjunctionHorizontalQuotientFunctorsV5_127.Generic
open KUOS.DependentOriginationCoherentBiadjunctionKernelQuotientHorizontalExchangeV5_131.Generic
open KUOS.DependentOriginationCoherentBiadjunctionMixedAssociatorHexagonV5_132.Generic
open KUOS.DependentOriginationCoherentBiadjunctionQuotientMixedHexagonNaturalityV5_132.Generic

set_option autoImplicit false
noncomputable section

/-!
# F35/v5.132 — STAGEWISE original F28 quotient hexagon and NatIso coherence

F35-B proves the original four-stage composite comparison hexagon
descends to an ACTUAL natural iso of the original F28 mathlib quotient.
This file independently lifts EACH OF ITS FOUR ORIGINAL COMPONENTS
(as F31 associator, F34 mixed exchange, whiskered F34 exchange and
inverse F31 associator) via F32's exact fully faithful
`liftStructuralComparisonIso` and COMPOSES them inside the true
quotient CATEGORY, without replacing them by the single final iso.

We prove the exact image of this four-step COMPOSITE, equality with
F35-B's independently lifted full path, naturality for arbitrary
quotient arrows, and equality of the WHOLE stagewise NatIso with
F34's original mixed exchange NatIso.
-/

namespace Generic

universe uC vC wC
variable {C : Type uC} [Bicategory.{wC, vC} C]

/-- GENUINE four-stage quotient-category structural pasting:
the four F31/F34 coherence stages are SEPARATELY lifted into
F28, and composed in its actual quotient Hom. -/
def kernelMixedHexagonStagewiseLongIso (aF bF aG bG : C)
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
  (((liftStructuralComparisonIso
      (Bicategory.whiskerRightIso (α_ vF uF x.as.fF) wF)
      (Bicategory.whiskerRightIso (α_ vG uG x.as.fG) wG)).trans
    (liftStructuralComparisonIso
      (α_ vF (uF ≫ x.as.fF) wF)
      (α_ vG (uG ≫ x.as.fG) wG))).trans
    (liftStructuralComparisonIso
      (Bicategory.whiskerLeftIso vF (α_ uF x.as.fF wF))
      (Bicategory.whiskerLeftIso vG (α_ uG x.as.fG wG)))).trans
    (liftStructuralComparisonIso
      (α_ vF uF (x.as.fF ≫ wF)).symm
      (α_ vG uG (x.as.fG ≫ wG)).symm)

/-- Compress the ACTUAL four stagewise quotient arrows: their
image is exactly the original FOUR original structural
comparison cells (F ISO and G structural ISO) composed in F27. -/
theorem kernelMixedHexagonStagewiseLongIso_compression
    (aF bF aG bG : C)
    {eF eG dF dG cF cG : C}
    (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (vF : dF ⟶ eF) (vG : dG ⟶ eG)
    (wF : bF ⟶ cF) (wG : bG ⟶ cG)
    (x : compressionKernelCategory aF bF aG bG) :
    (quotientCompositeFunctor dF cF dG cG).map
      (kernelMixedHexagonStagewiseLongIso aF bF aG bG
        uF uG vF vG wF wG x).hom =
    (compositeMixedHexagonLongIso aF bF aG bG
      uF uG vF vG wF wG
      ((quotientCompositeFunctor aF bF aG bG).obj x)).hom := by
  rcases x with ⟨x⟩
  let Q := quotientCompositeFunctor dF cF dG cG
  let p1 := liftStructuralComparisonIso
    (Bicategory.whiskerRightIso (α_ vF uF x.fF) wF)
    (Bicategory.whiskerRightIso (α_ vG uG x.fG) wG)
  let p2 := liftStructuralComparisonIso
    (α_ vF (uF ≫ x.fF) wF) (α_ vG (uG ≫ x.fG) wG)
  let p3 := liftStructuralComparisonIso
    (Bicategory.whiskerLeftIso vF (α_ uF x.fF wF))
    (Bicategory.whiskerLeftIso vG (α_ uG x.fG wG))
  let p4 := liftStructuralComparisonIso
    (α_ vF uF (x.fF ≫ wF)).symm
    (α_ vG uG (x.fG ≫ wG)).symm
  change Q.map (((p1.hom ≫ p2.hom) ≫ p3.hom) ≫ p4.hom) =
    (compositeMixedHexagonLongIso aF bF aG bG
      uF uG vF vG wF wG
      ⟨x.fF, x.fG⟩).hom
  rw [Q.map_comp ((p1.hom ≫ p2.hom) ≫ p3.hom) p4.hom]
  rw [Q.map_comp (p1.hom ≫ p2.hom) p3.hom]
  rw [Q.map_comp p1.hom p2.hom]
  simpa only [p1, p2, p3, p4, Q,
    liftStructuralComparisonIso_compression,
    compositeMixedHexagonLongIso, structuralComparisonPairIso,
    Iso.trans_hom, Category.assoc]

/-- The independently staged four F31/F34 quotient arrows paste to
exactly the F35-B full-hexagon quotient ISO. Proved using F28's
FAITHFULNESS rather than collapsing the intermediate arrows. -/
theorem kernelMixedHexagonStagewiseLongIso_eq_full
    (aF bF aG bG : C)
    {eF eG dF dG cF cG : C}
    (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (vF : dF ⟶ eF) (vG : dG ⟶ eG)
    (wF : bF ⟶ cF) (wG : bG ⟶ cG)
    (x : compressionKernelCategory aF bF aG bG) :
    kernelMixedHexagonStagewiseLongIso aF bF aG bG
      uF uG vF vG wF wG x =
    kernelMixedHexagonLongComponent aF bF aG bG
      uF uG vF vG wF wG x := by
  apply Iso.ext
  apply (quotientCompositeFunctor dF cF dG cG).map_injective
  rw [kernelMixedHexagonStagewiseLongIso_compression]
  simp only [kernelMixedHexagonLongComponent,
    Functor.preimageIso_hom, Functor.map_preimage]

/-- The four independently composed F31/F34 F28 quotient
structural isomorphisms form a TRUE NatIso, natural for ALL
original quotient morphisms (including arbitrary G 2-cells). -/
def kernelMixedHexagonStagewiseLongNatIso (aF bF aG bG : C)
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
    (fun x => kernelMixedHexagonStagewiseLongIso aF bF aG bG
      uF uG vF vG wF wG x)
    (by
      intro x y pq
      change
        (leftKernelQuotientWhiskerFunctor aF bF aG bG
          (vF ≫ uF) (vG ≫ uG) ⋙
          rightKernelQuotientWhiskerFunctor dF bF dG bG wF wG).map pq ≫
        (kernelMixedHexagonStagewiseLongIso aF bF aG bG
          uF uG vF vG wF wG y).hom =
        (kernelMixedHexagonStagewiseLongIso aF bF aG bG
          uF uG vF vG wF wG x).hom ≫
        (rightKernelQuotientWhiskerFunctor aF bF aG bG wF wG ⋙
          leftKernelQuotientWhiskerFunctor aF cF aG cG
            (vF ≫ uF) (vG ≫ uG)).map pq
      rw [kernelMixedHexagonStagewiseLongIso_eq_full
          aF bF aG bG uF uG vF vG wF wG x,
          kernelMixedHexagonStagewiseLongIso_eq_full
          aF bF aG bG uF uG vF vG wF wG y]
      exact (kernelMixedHexagonLongNatIso aF bF aG bG
        uF uG vF vG wF wG).hom.naturality pq)

/-- STRONGER F35 hexagon: equality of the genuine four-stage
quotient NATURAL ISO and the direct original F34 mixed exchange
NATURAL ISO, for the WHOLE genuine mathlib quotient CATEGORY. -/
theorem kernelMixedHexagonStagewiseNatIso_coherence (aF bF aG bG : C)
    {eF eG dF dG cF cG : C}
    (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (vF : dF ⟶ eF) (vG : dG ⟶ eG)
    (wF : bF ⟶ cF) (wG : bG ⟶ cG) :
    kernelMixedHexagonStagewiseLongNatIso aF bF aG bG
      uF uG vF vG wF wG =
    kernelQuotientHorizontalExchangeNatIso aF bF aG bG
      (vF ≫ uF) (vG ≫ uG) wF wG := by
  calc
    _ = kernelMixedHexagonLongNatIso aF bF aG bG
          uF uG vF vG wF wG := by
      apply Iso.ext
      apply NatTrans.ext
      funext x
      change (kernelMixedHexagonStagewiseLongIso aF bF aG bG
        uF uG vF vG wF wG x).hom =
        (kernelMixedHexagonLongComponent aF bF aG bG
          uF uG vF vG wF wG x).hom
      exact congrArg Iso.hom
        (kernelMixedHexagonStagewiseLongIso_eq_full aF bF aG bG
          uF uG vF vG wF wG x)
    _ = _ := kernelMixedHexagonNatIso_coherence aF bF aG bG
      uF uG vF vG wF wG

#print axioms kernelMixedHexagonStagewiseLongIso
#print axioms kernelMixedHexagonStagewiseLongIso_compression
#print axioms kernelMixedHexagonStagewiseLongIso_eq_full
#print axioms kernelMixedHexagonStagewiseLongNatIso
#print axioms kernelMixedHexagonStagewiseNatIso_coherence

end Generic

end

end KUOS.DependentOriginationCoherentBiadjunctionStagewiseQuotientMixedHexagonV5_132
