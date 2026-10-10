import KUOS.DependentOriginationCoherentBiadjunctionActualLiftHorizontalCoherenceV5_128

namespace KUOS.DependentOriginationCoherentBiadjunctionCompositePentagonTriangleV5_129

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionComparisonCompressionFunctorV5_124.Generic
open KUOS.DependentOriginationCoherentBiadjunctionHorizontalAssociatorUnitorCompositeV5_128.Generic

set_option autoImplicit false
noncomputable section

/-!
# F32 / v5.129 — authentic bicategory pentagon and triangle on F/G comparison pairs

The F31 structural associators and unitors must satisfy the actual
bicategorical higher coherence laws, rather than being postulated as
strict identities.  We construct the TWO composite-presentation
isomorphisms for each side of the pentagon and triangle and prove
their equality using pinned mathlib's native Bicategory.pentagon and
Bicategory.triangle. Both F and G structural cells are isomorphisms,
but comparison arrows on G remain arbitrary and potentially noninvertible.
-/

namespace Generic

universe uC vC wC
variable {C : Type uC} [Bicategory.{wC, vC} C]
variable {aF bF cF dF eF aG bG cG dG eG : C}

/-- The three-edge pentagon pasting of ACTUAL structural isomorphisms
inside the F27 composite-comparison category. -/
def compositePentagonLongIso
    (fF : aF ⟶ bF) (gF : bF ⟶ cF) (hF : cF ⟶ dF) (iF : dF ⟶ eF)
    (fG : aG ⟶ bG) (gG : bG ⟶ cG) (hG : cG ⟶ dG) (iG : dG ⟶ eG) :
    (⟨(((fF ≫ gF) ≫ hF) ≫ iF), (((fG ≫ gG) ≫ hG) ≫ iG)⟩ :
      CompositeComparisonPair aF eF aG eG) ≅
    (⟨fF ≫ (gF ≫ (hF ≫ iF)), fG ≫ (gG ≫ (hG ≫ iG))⟩ :
      CompositeComparisonPair aF eF aG eG) :=
  structuralComparisonPairIso
    (((Bicategory.whiskerRightIso (α_ fF gF hF) iF).trans
      (α_ fF (gF ≫ hF) iF)).trans
      (Bicategory.whiskerLeftIso fF (α_ gF hF iF)))
    (((Bicategory.whiskerRightIso (α_ fG gG hG) iG).trans
      (α_ fG (gG ≫ hG) iG)).trans
      (Bicategory.whiskerLeftIso fG (α_ gG hG iG)))

/-- The two-edge pentagon pasting of ORIGINAL structural comparison
isomorphisms; its F/G source and target match the long paste exactly. -/
def compositePentagonShortIso
    (fF : aF ⟶ bF) (gF : bF ⟶ cF) (hF : cF ⟶ dF) (iF : dF ⟶ eF)
    (fG : aG ⟶ bG) (gG : bG ⟶ cG) (hG : cG ⟶ dG) (iG : dG ⟶ eG) :
    (⟨(((fF ≫ gF) ≫ hF) ≫ iF), (((fG ≫ gG) ≫ hG) ≫ iG)⟩ :
      CompositeComparisonPair aF eF aG eG) ≅
    (⟨fF ≫ (gF ≫ (hF ≫ iF)), fG ≫ (gG ≫ (hG ≫ iG))⟩ :
      CompositeComparisonPair aF eF aG eG) :=
  structuralComparisonPairIso
    ((α_ (fF ≫ gF) hF iF).trans (α_ fF gF (hF ≫ iF)))
    ((α_ (fG ≫ gG) hG iG).trans (α_ fG gG (hG ≫ iG)))

/-- F32 Pentagon: the REAL two pentagon pastes agree as isomorphisms
in the F27 comparison-pair category; neither F nor G is strictified. -/
theorem compositePentagon
    (fF : aF ⟶ bF) (gF : bF ⟶ cF) (hF : cF ⟶ dF) (iF : dF ⟶ eF)
    (fG : aG ⟶ bG) (gG : bG ⟶ cG) (hG : cG ⟶ dG) (iG : dG ⟶ eG) :
    compositePentagonLongIso fF gF hF iF fG gG hG iG =
      compositePentagonShortIso fF gF hF iF fG gG hG iG := by
  apply Iso.ext
  apply Prod.ext
  · apply Iso.ext
    change
      ((α_ fF gF hF).hom ▷ iF ≫
        (α_ fF (gF ≫ hF) iF).hom) ≫
          fF ◁ (α_ gF hF iF).hom =
        (α_ (fF ≫ gF) hF iF).hom ≫
          (α_ fF gF (hF ≫ iF)).hom
    exact Bicategory.pentagon fF gF hF iF
  · change
      ((α_ fG gG hG).hom ▷ iG ≫
        (α_ fG (gG ≫ hG) iG).hom) ≫
          fG ◁ (α_ gG hG iG).hom =
        (α_ (fG ≫ gG) hG iG).hom ≫
          (α_ fG gG (hG ≫ iG)).hom
    exact Bicategory.pentagon fG gG hG iG

variable {aF bF cF aG bG cG : C}

/-- Original associator followed by the left unitor, both as REAL
comparison-pair isomorphisms, is the long triangle paste. -/
def compositeTriangleLongIso
    (fF : aF ⟶ bF) (gF : bF ⟶ cF)
    (fG : aG ⟶ bG) (gG : bG ⟶ cG) :
    (⟨(fF ≫ 𝟙 bF) ≫ gF, (fG ≫ 𝟙 bG) ≫ gG⟩ :
      CompositeComparisonPair aF cF aG cG) ≅
    (⟨fF ≫ gF, fG ≫ gG⟩ :
      CompositeComparisonPair aF cF aG cG) :=
  structuralComparisonPairIso
    ((α_ fF (𝟙 bF) gF).trans
      (Bicategory.whiskerLeftIso fF (λ_ gF)))
    ((α_ fG (𝟙 bG) gG).trans
      (Bicategory.whiskerLeftIso fG (λ_ gG)))

/-- Original right unitor, whiskered on its right, gives the short
triangle paste with the same F/G source and target. -/
def compositeTriangleShortIso
    (fF : aF ⟶ bF) (gF : bF ⟶ cF)
    (fG : aG ⟶ bG) (gG : bG ⟶ cG) :
    (⟨(fF ≫ 𝟙 bF) ≫ gF, (fG ≫ 𝟙 bG) ≫ gG⟩ :
      CompositeComparisonPair aF cF aG cG) ≅
    (⟨fF ≫ gF, fG ≫ gG⟩ :
      CompositeComparisonPair aF cF aG cG) :=
  structuralComparisonPairIso
    (Bicategory.whiskerRightIso (ρ_ fF) gF)
    (Bicategory.whiskerRightIso (ρ_ fG) gG)

/-- F32 Triangle: the two ACTUAL triangle pastes agree as comparison
isomorphisms, by native bicategory coherence separately on F/G. -/
theorem compositeTriangle
    (fF : aF ⟶ bF) (gF : bF ⟶ cF)
    (fG : aG ⟶ bG) (gG : bG ⟶ cG) :
    compositeTriangleLongIso fF gF fG gG =
      compositeTriangleShortIso fF gF fG gG := by
  apply Iso.ext
  apply Prod.ext
  · apply Iso.ext
    change (α_ fF (𝟙 bF) gF).hom ≫
      fF ◁ (λ_ gF).hom = (ρ_ fF).hom ▷ gF
    exact Bicategory.triangle fF gF
  · change (α_ fG (𝟙 bG) gG).hom ≫
      fG ◁ (λ_ gG).hom = (ρ_ fG).hom ▷ gG
    exact Bicategory.triangle fG gG

#print axioms compositePentagonLongIso
#print axioms compositePentagonShortIso
#print axioms compositePentagon
#print axioms compositeTriangleLongIso
#print axioms compositeTriangleShortIso
#print axioms compositeTriangle

end Generic

end

end KUOS.DependentOriginationCoherentBiadjunctionCompositePentagonTriangleV5_129
