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
# F32/v5.129 — ACTUAL quotient pentagon and triangle

The original F/G structural associators and unitors are separately
lifted into the genuine F28 comparison-kernel quotient Hom, not
treated as strict identities. They are composed stage by stage.
The two full pastes compress to exactly the original F32 composite
comparison cells. Faithfulness of the proven F28 quotient-compression
functor and pinned mathlib's bicategorical pentagon/triangle establish
the equality of the full quotient pastes. Arbitrary G comparison
morphisms need NOT be invertible.
-/

namespace Generic

universe uC vC wC
variable {C : Type uC} [Bicategory.{wC, vC} C]

/-- Lift one actual F/G *structural* pair of 2-isomorphisms through
the F28 quotient's FULL+FAITHFUL functor. All quotient source and
target objects are explicit, preventing unresolved dependent Homs. -/
def liftStructuralComparisonIso
    {aF bF aG bG : C}
    {fF kF : aF ⟶ bF} {fG kG : aG ⟶ bG}
    (p : fF ≅ kF) (q : fG ≅ kG) :
    (⟨⟨fF, fG⟩⟩ : compressionKernelCategory aF bF aG bG) ≅
    (⟨⟨kF, kG⟩⟩ : compressionKernelCategory aF bF aG bG) :=
  (quotientCompositeFunctor aF bF aG bG).preimageIso
    (X := (⟨⟨fF, fG⟩⟩ : compressionKernelCategory aF bF aG bG))
    (Y := (⟨⟨kF, kG⟩⟩ : compressionKernelCategory aF bF aG bG))
    (structuralComparisonPairIso
      (x := (⟨fF, fG⟩ : CompositeComparisonPair aF bF aG bG))
      (y := (⟨kF, kG⟩ : CompositeComparisonPair aF bF aG bG))
      p q)

/-- Exact compression of one independently lifted actual structural
comparison into the original F-ISO/G-2-cell category. -/
theorem liftStructuralComparisonIso_compression
    {aF bF aG bG : C}
    {fF kF : aF ⟶ bF} {fG kG : aG ⟶ bG}
    (p : fF ≅ kF) (q : fG ≅ kG) :
    (quotientCompositeFunctor aF bF aG bG).map
      (liftStructuralComparisonIso p q).hom =
    (structuralComparisonPairIso p q).hom := by
  simp only [liftStructuralComparisonIso,
    Functor.preimageIso_hom, Functor.map_preimage]

variable {aF bF cF dF eF aG bG cG dG eG : C}

/-- Three actual independently lifted F31 structural comparison
steps of the long pentagon route in the F28 quotient category. -/
def kernelPentagonLongIso
    (fF : aF ⟶ bF) (gF : bF ⟶ cF) (hF : cF ⟶ dF) (iF : dF ⟶ eF)
    (fG : aG ⟶ bG) (gG : bG ⟶ cG) (hG : cG ⟶ dG) (iG : dG ⟶ eG) :
    (⟨⟨(((fF ≫ gF) ≫ hF) ≫ iF), (((fG ≫ gG) ≫ hG) ≫ iG)⟩⟩ :
      compressionKernelCategory aF eF aG eG) ≅
    (⟨⟨fF ≫ (gF ≫ (hF ≫ iF)), fG ≫ (gG ≫ (hG ≫ iG))⟩⟩ :
      compressionKernelCategory aF eF aG eG) :=
  ((liftStructuralComparisonIso
      (Bicategory.whiskerRightIso (α_ fF gF hF) iF)
      (Bicategory.whiskerRightIso (α_ fG gG hG) iG)).trans
   (liftStructuralComparisonIso
      (α_ fF (gF ≫ hF) iF)
      (α_ fG (gG ≫ hG) iG))).trans
   (liftStructuralComparisonIso
      (Bicategory.whiskerLeftIso fF (α_ gF hF iF))
      (Bicategory.whiskerLeftIso fG (α_ gG hG iG)))

/-- Two actual independently lifted F31 structural comparison
steps of the short pentagon route, with the SAME quotient endpoints. -/
def kernelPentagonShortIso
    (fF : aF ⟶ bF) (gF : bF ⟶ cF) (hF : cF ⟶ dF) (iF : dF ⟶ eF)
    (fG : aG ⟶ bG) (gG : bG ⟶ cG) (hG : cG ⟶ dG) (iG : dG ⟶ eG) :
    (⟨⟨(((fF ≫ gF) ≫ hF) ≫ iF), (((fG ≫ gG) ≫ hG) ≫ iG)⟩⟩ :
      compressionKernelCategory aF eF aG eG) ≅
    (⟨⟨fF ≫ (gF ≫ (hF ≫ iF)), fG ≫ (gG ≫ (hG ≫ iG))⟩⟩ :
      compressionKernelCategory aF eF aG eG) :=
  (liftStructuralComparisonIso
      (α_ (fF ≫ gF) hF iF)
      (α_ (fG ≫ gG) hG iG)).trans
    (liftStructuralComparisonIso
      (α_ fF gF (hF ≫ iF))
      (α_ fG gG (hG ≫ iG)))

/-- The complete long quotient pasting compresses to precisely the
original three-step structural pentagon paste, on F and G alike. -/
theorem kernelPentagonLongIso_compression
    (fF : aF ⟶ bF) (gF : bF ⟶ cF) (hF : cF ⟶ dF) (iF : dF ⟶ eF)
    (fG : aG ⟶ bG) (gG : bG ⟶ cG) (hG : cG ⟶ dG) (iG : dG ⟶ eG) :
    (quotientCompositeFunctor aF eF aG eG).map
      (kernelPentagonLongIso fF gF hF iF fG gG hG iG).hom =
      (compositePentagonLongIso fF gF hF iF fG gG hG iG).hom := by
  simp only [kernelPentagonLongIso, Iso.trans_hom, Functor.map_comp,
    liftStructuralComparisonIso_compression]
  rfl

/-- The complete short quotient pasting compresses to exactly the
original two-step structural pentagon paste. -/
theorem kernelPentagonShortIso_compression
    (fF : aF ⟶ bF) (gF : bF ⟶ cF) (hF : cF ⟶ dF) (iF : dF ⟶ eF)
    (fG : aG ⟶ bG) (gG : bG ⟶ cG) (hG : cG ⟶ dG) (iG : dG ⟶ eG) :
    (quotientCompositeFunctor aF eF aG eG).map
      (kernelPentagonShortIso fF gF hF iF fG gG hG iG).hom =
      (compositePentagonShortIso fF gF hF iF fG gG hG iG).hom := by
  simp only [kernelPentagonShortIso, Iso.trans_hom, Functor.map_comp,
    liftStructuralComparisonIso_compression]
  rfl

/-- ACTUAL F32 quotient Pentagon: independently constructed 3-stage
and 2-stage pentagon pastes are equal as genuine F28 quotient isomorphisms,
by F28 faithfulness and both ORIGINAL bicategorical pentagons. -/
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

/-- The ORIGINAL associator and left unitor are separately lifted
and composed in the long triangle route inside the true quotient. -/
def kernelTriangleLongIso
    (fF : aF ⟶ bF) (gF : bF ⟶ cF)
    (fG : aG ⟶ bG) (gG : bG ⟶ cG) :
    (⟨⟨(fF ≫ 𝟙 bF) ≫ gF, (fG ≫ 𝟙 bG) ≫ gG⟩⟩ :
      compressionKernelCategory aF cF aG cG) ≅
    (⟨⟨fF ≫ gF, fG ≫ gG⟩⟩ :
      compressionKernelCategory aF cF aG cG) :=
  (liftStructuralComparisonIso
      (α_ fF (𝟙 bF) gF) (α_ fG (𝟙 bG) gG)).trans
    (liftStructuralComparisonIso
      (Bicategory.whiskerLeftIso fF (λ_ gF))
      (Bicategory.whiskerLeftIso fG (λ_ gG)))

/-- Genuine independent short triangle paste: the ORIGINAL right
unitor whiskered by the given F/G 1-cells. -/
def kernelTriangleShortIso
    (fF : aF ⟶ bF) (gF : bF ⟶ cF)
    (fG : aG ⟶ bG) (gG : bG ⟶ cG) :
    (⟨⟨(fF ≫ 𝟙 bF) ≫ gF, (fG ≫ 𝟙 bG) ≫ gG⟩⟩ :
      compressionKernelCategory aF cF aG cG) ≅
    (⟨⟨fF ≫ gF, fG ≫ gG⟩⟩ :
      compressionKernelCategory aF cF aG cG) :=
  liftStructuralComparisonIso
    (Bicategory.whiskerRightIso (ρ_ fF) gF)
    (Bicategory.whiskerRightIso (ρ_ fG) gG)

/-- The stagewise long triangle quotient paste compresses to the
authentic F32 composite triangle long paste. -/
theorem kernelTriangleLongIso_compression
    (fF : aF ⟶ bF) (gF : bF ⟶ cF)
    (fG : aG ⟶ bG) (gG : bG ⟶ cG) :
    (quotientCompositeFunctor aF cF aG cG).map
      (kernelTriangleLongIso fF gF fG gG).hom =
      (compositeTriangleLongIso fF gF fG gG).hom := by
  simp only [kernelTriangleLongIso, Iso.trans_hom, Functor.map_comp,
    liftStructuralComparisonIso_compression]
  rfl

/-- Exact image of the independently lifted short triangle paste. -/
theorem kernelTriangleShortIso_compression
    (fF : aF ⟶ bF) (gF : bF ⟶ cF)
    (fG : aG ⟶ bG) (gG : bG ⟶ cG) :
    (quotientCompositeFunctor aF cF aG cG).map
      (kernelTriangleShortIso fF gF fG gG).hom =
      (compositeTriangleShortIso fF gF fG gG).hom := by
  exact liftStructuralComparisonIso_compression
    (Bicategory.whiskerRightIso (ρ_ fF) gF)
    (Bicategory.whiskerRightIso (ρ_ fG) gG)

/-- ACTUAL F32 quotient Triangle: the two original structural
routes agree in the genuine quotient Hom; no G comparison inverse. -/
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

#print axioms liftStructuralComparisonIso
#print axioms liftStructuralComparisonIso_compression
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
