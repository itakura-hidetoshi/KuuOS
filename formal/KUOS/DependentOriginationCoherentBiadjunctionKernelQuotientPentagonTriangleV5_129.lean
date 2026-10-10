import KUOS.DependentOriginationCoherentBiadjunctionCompositePentagonTriangleV5_129

namespace KUOS.DependentOriginationCoherentBiadjunctionKernelQuotientPentagonTriangleV5_129

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionCompressionKernelQuotientCategoryV5_125.Generic
open KUOS.DependentOriginationCoherentBiadjunctionHorizontalAssociatorUnitorCompositeV5_128.Generic
open KUOS.DependentOriginationCoherentBiadjunctionCompositePentagonTriangleV5_129.Generic

set_option autoImplicit false
noncomputable section

/-!
# F32 / v5.129 — pentagon and triangle ACTUALLY PASTED in the F28 kernel quotient

F31 proves that original nonstrict structural associators and unitors
are genuine NATURAL ISOMORPHISMS of the horizontal quotient-category
functors. This layer forms the distinct long/short routes as explicit
compositions of quotient structural isomorphisms. It proves that their
images under the original fully faithful F28 quotient-compression
functor are EXACTLY the F/G composite pastes from F32-A. The original
bicategorical pentagon/triangle and faithfulness therefore give actual
equality of the TWO distinct quotient paths, not merely equality
after choosing a representative. No new ambient biequivalence, no
strictification, and no G-side comparison invertibility assumption.
-/

namespace Generic

universe uC vC wC
variable {C : Type uC} [Bicategory.{wC, vC} C]
variable {aF bF cF dF eF aG bG cG dG eG : C}

/-- An ACTUAL triple of independently lifted structural comparisons,
corresponding to the 3-edge pentagon paste inside the kernel quotient. -/
def kernelPentagonLongIso
    (fF : aF ⟶ bF) (gF : bF ⟶ cF) (hF : cF ⟶ dF) (iF : dF ⟶ eF)
    (fG : aG ⟶ bG) (gG : bG ⟶ cG) (hG : cG ⟶ dG) (iG : dG ⟶ eG) :
    (⟨⟨(((fF ≫ gF) ≫ hF) ≫ iF), (((fG ≫ gG) ≫ hG) ≫ iG)⟩⟩ :
      compressionKernelCategory aF eF aG eG) ≅
    (⟨⟨fF ≫ (gF ≫ (hF ≫ iF)), fG ≫ (gG ≫ (hG ≫ iG))⟩⟩ :
      compressionKernelCategory aF eF aG eG) :=
  let Q := quotientCompositeFunctor aF eF aG eG
  ((Q.preimageIso (structuralComparisonPairIso
      (Bicategory.whiskerRightIso (α_ fF gF hF) iF)
      (Bicategory.whiskerRightIso (α_ fG gG hG) iG))).trans
   (Q.preimageIso (structuralComparisonPairIso
      (α_ fF (gF ≫ hF) iF)
      (α_ fG (gG ≫ hG) iG)))).trans
   (Q.preimageIso (structuralComparisonPairIso
      (Bicategory.whiskerLeftIso fF (α_ gF hF iF))
      (Bicategory.whiskerLeftIso fG (α_ gG hG iG))))

/-- The genuine two-edge pentagon route lifted stage by stage into
the SAME mathlib F28 quotient Hom, retaining each structural 2-cell. -/
def kernelPentagonShortIso
    (fF : aF ⟶ bF) (gF : bF ⟶ cF) (hF : cF ⟶ dF) (iF : dF ⟶ eF)
    (fG : aG ⟶ bG) (gG : bG ⟶ cG) (hG : cG ⟶ dG) (iG : dG ⟶ eG) :
    (⟨⟨(((fF ≫ gF) ≫ hF) ≫ iF), (((fG ≫ gG) ≫ hG) ≫ iG)⟩⟩ :
      compressionKernelCategory aF eF aG eG) ≅
    (⟨⟨fF ≫ (gF ≫ (hF ≫ iF)), fG ≫ (gG ≫ (hG ≫ iG))⟩⟩ :
      compressionKernelCategory aF eF aG eG) :=
  let Q := quotientCompositeFunctor aF eF aG eG
  (Q.preimageIso (structuralComparisonPairIso
      (α_ (fF ≫ gF) hF iF)
      (α_ (fG ≫ gG) hG iG))).trans
    (Q.preimageIso (structuralComparisonPairIso
      (α_ fF gF (hF ≫ iF))
      (α_ fG gG (hG ≫ iG)))

/-- The compression of the whole long QUOTIENT PASTE is precisely the
original three structural comparisons, not an arbitrary representative. -/
theorem kernelPentagonLongIso_compression
    (fF : aF ⟶ bF) (gF : bF ⟶ cF) (hF : cF ⟶ dF) (iF : dF ⟶ eF)
    (fG : aG ⟶ bG) (gG : bG ⟶ cG) (hG : cG ⟶ dG) (iG : dG ⟶ eG) :
    (quotientCompositeFunctor aF eF aG eG).map
      (kernelPentagonLongIso fF gF hF iF fG gG hG iG).hom =
      (compositePentagonLongIso fF gF hF iF fG gG hG iG).hom := by
  simp only [kernelPentagonLongIso, Iso.trans_hom, Functor.map_comp,
    Functor.preimageIso_hom, Functor.map_preimage]
  rfl

/-- The compressed short QUOTIENT PASTE is the exact original
two-edge pentagon path. -/
theorem kernelPentagonShortIso_compression
    (fF : aF ⟶ bF) (gF : bF ⟶ cF) (hF : cF ⟶ dF) (iF : dF ⟶ eF)
    (fG : aG ⟶ bG) (gG : bG ⟶ cG) (hG : cG ⟶ dG) (iG : dG ⟶ eG) :
    (quotientCompositeFunctor aF eF aG eG).map
      (kernelPentagonShortIso fF gF hF iF fG gG hG iG).hom =
      (compositePentagonShortIso fF gF hF iF fG gG hG iG).hom := by
  simp only [kernelPentagonShortIso, Iso.trans_hom, Functor.map_comp,
    Functor.preimageIso_hom, Functor.map_preimage]
  rfl

/-- F32's genuine PENTAGON LAW: three-stage and two-stage pastings
are equal as actual F28 quotient isomorphisms. This uses both native
bicategory pentagons and FAITHFULNESS of the proven F28 quotient functor. -/
theorem kernelQuotientPentagon
    (fF : aF ⟶ bF) (gF : bF ⟶ cF) (hF : cF ⟶ dF) (iF : dF ⟶ eF)
    (fG : aG ⟶ bG) (gG : bG ⟶ cG) (hG : cG ⟶ dG) (iG : dG ⟶ eG) :
    kernelPentagonLongIso fF gF hF iF fG gG hG iG =
      kernelPentagonShortIso fF gF hF iF fG gG hG iG := by
  apply Iso.ext
  apply (quotientCompositeFunctor aF eF aG eG).map_injective
  rw [kernelPentagonLongIso_compression,
      kernelPentagonShortIso_compression]
  exact congrArg Iso.hom (compositePentagon fF gF hF iF fG gG hG iG)

/-- Actual triangle long route, composed from distinct original
associator and left-unitor lifts in the mathlib quotient category. -/
def kernelTriangleLongIso
    (fF : aF ⟶ bF) (gF : bF ⟶ cF)
    (fG : aG ⟶ bG) (gG : bG ⟶ cG) :
    (⟨⟨(fF ≫ 𝟙 bF) ≫ gF, (fG ≫ 𝟙 bG) ≫ gG⟩⟩ :
      compressionKernelCategory aF cF aG cG) ≅
    (⟨⟨fF ≫ gF, fG ≫ gG⟩⟩ :
      compressionKernelCategory aF cF aG cG) :=
  let Q := quotientCompositeFunctor aF cF aG cG
  (Q.preimageIso (structuralComparisonPairIso
      (α_ fF (𝟙 bF) gF)
      (α_ fG (𝟙 bG) gG))).trans
    (Q.preimageIso (structuralComparisonPairIso
      (Bicategory.whiskerLeftIso fF (λ_ gF))
      (Bicategory.whiskerLeftIso fG (λ_ gG))))

/-- Actual triangle short route, the right unitor whiskered by the
original gF/gG pair, lifted into exactly the same quotient Hom. -/
def kernelTriangleShortIso
    (fF : aF ⟶ bF) (gF : bF ⟶ cF)
    (fG : aG ⟶ bG) (gG : bG ⟶ cG) :
    (⟨⟨(fF ≫ 𝟙 bF) ≫ gF, (fG ≫ 𝟙 bG) ≫ gG⟩⟩ :
      compressionKernelCategory aF cF aG cG) ≅
    (⟨⟨fF ≫ gF, fG ≫ gG⟩⟩ :
      compressionKernelCategory aF cF aG cG) :=
  (quotientCompositeFunctor aF cF aG cG).preimageIso
    (structuralComparisonPairIso
      (Bicategory.whiskerRightIso (ρ_ fF) gF)
      (Bicategory.whiskerRightIso (ρ_ fG) gG))

/-- The long triangle quotient paste compresses to the exact F/G
original triangle, with both structural stages retained. -/
theorem kernelTriangleLongIso_compression
    (fF : aF ⟶ bF) (gF : bF ⟶ cF)
    (fG : aG ⟶ bG) (gG : bG ⟶ cG) :
    (quotientCompositeFunctor aF cF aG cG).map
      (kernelTriangleLongIso fF gF fG gG).hom =
      (compositeTriangleLongIso fF gF fG gG).hom := by
  simp only [kernelTriangleLongIso, Iso.trans_hom, Functor.map_comp,
    Functor.preimageIso_hom, Functor.map_preimage]
  rfl

/-- Exact compression of the native right-unitor triangle quotient route. -/
theorem kernelTriangleShortIso_compression
    (fF : aF ⟶ bF) (gF : bF ⟶ cF)
    (fG : aG ⟶ bG) (gG : bG ⟶ cG) :
    (quotientCompositeFunctor aF cF aG cG).map
      (kernelTriangleShortIso fF gF fG gG).hom =
      (compositeTriangleShortIso fF gF fG gG).hom := by
  simp only [kernelTriangleShortIso,
    Functor.preimageIso_hom, Functor.map_preimage]
  rfl

/-- F32's genuine TRIANGLE LAW: two independently constructed pastes
are equal as ACTUAL quotient isomorphisms, from the original mathlib
bicategorical triangle and proved full-faithful quotient compression. -/
theorem kernelQuotientTriangle
    (fF : aF ⟶ bF) (gF : bF ⟶ cF)
    (fG : aG ⟶ bG) (gG : bG ⟶ cG) :
    kernelTriangleLongIso fF gF fG gG =
      kernelTriangleShortIso fF gF fG gG := by
  apply Iso.ext
  apply (quotientCompositeFunctor aF cF aG cG).map_injective
  rw [kernelTriangleLongIso_compression,
      kernelTriangleShortIso_compression]
  exact congrArg Iso.hom (compositeTriangle fF gF fG gG)

#print axioms kernelPentagonLongIso
#print axioms kernelPentagonShortIso
#print axioms kernelPentagonLongIso_compression
#print axioms kernelPentagonShortIso_compression
#print axioms kernelQuotientPentagon
#print axioms kernelTriangleLongIso
#print axioms kernelTriangleShortIso
#print axioms kernelTriangleLongIso_compression
#print axioms kernelTriangleShortIso_compression
#print axioms kernelQuotientTriangle

end Generic

end

end KUOS.DependentOriginationCoherentBiadjunctionKernelQuotientPentagonTriangleV5_129
