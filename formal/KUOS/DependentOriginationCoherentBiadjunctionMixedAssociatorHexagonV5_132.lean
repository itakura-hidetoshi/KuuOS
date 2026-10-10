import KUOS.DependentOriginationCoherentBiadjunctionActualLiftHorizontalExchangeV5_131

namespace KUOS.DependentOriginationCoherentBiadjunctionMixedAssociatorHexagonV5_132

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionComparisonCompressionFunctorV5_124.Generic
open KUOS.DependentOriginationCoherentBiadjunctionHorizontalCompositeFunctorsV5_127.Generic
open KUOS.DependentOriginationCoherentBiadjunctionHorizontalAssociatorUnitorCompositeV5_128.Generic
open KUOS.DependentOriginationCoherentBiadjunctionCompositeHorizontalExchangeV5_131.Generic

set_option autoImplicit false
noncomputable section

/-!
# F35/v5.132 — mixed horizontal exchange / left associator HEXAGON

F31's genuine left-associator natural isomorphism and F34's mixed
left/right exchange natural isomorphism induce TWO DISTINCT routes from
the twice-prewhiskered, postwhiskered comparison to the precomposed
left-whisker after postwhiskering.

The LONG route is a 4-stage genuine structural pasting:
  (α(v,u,x) ▷ w) ; α(v,u≫x,w) ; (v ◁ α(u,x,w)) ; α(v,u,x≫w)⁻¹.
The SHORT route is the F34 mixed exchange α(v≫u,x,w).
They agree by mathlib's ORIGINAL bicategorical PENTAGON law, for
both independent F and G components.

We then package that higher coherence as an equality of ACTUAL NATURAL
ISOMORPHISMS on the ordinary F27 composite comparison categories.
Crucially, the naturality of each route applies to every arbitrary
possibly NONINVERTIBLE G comparison 2-cell.
-/

namespace Generic

universe uC vC wC
variable {C : Type uC} [Bicategory.{wC, vC} C]

/-- LONG four-stage composition of the original F31 left associator,
the middle/right F34 mixed exchanges and the inverse F31 left
associator, as an actual F/G comparison isomorphism. -/
def compositeMixedHexagonLongIso
    (aF bF aG bG : C)
    {eF eG dF dG cF cG : C}
    (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (vF : dF ⟶ eF) (vG : dG ⟶ eG)
    (wF : bF ⟶ cF) (wG : bG ⟶ cG)
    (x : CompositeComparisonPair aF bF aG bG) :
    (⟨((vF ≫ uF) ≫ x.fF) ≫ wF,
       ((vG ≫ uG) ≫ x.fG) ≫ wG⟩ :
       CompositeComparisonPair dF cF dG cG) ≅
    (⟨(vF ≫ uF) ≫ (x.fF ≫ wF),
       (vG ≫ uG) ≫ (x.fG ≫ wG)⟩ :
       CompositeComparisonPair dF cF dG cG) :=
  structuralComparisonPairIso
    ((((Bicategory.whiskerRightIso (α_ vF uF x.fF) wF).trans
        (α_ vF (uF ≫ x.fF) wF)).trans
        (Bicategory.whiskerLeftIso vF (α_ uF x.fF wF))).trans
        (α_ vF uF (x.fF ≫ wF)).symm)
    ((((Bicategory.whiskerRightIso (α_ vG uG x.fG) wG).trans
        (α_ vG (uG ≫ x.fG) wG)).trans
        (Bicategory.whiskerLeftIso vG (α_ uG x.fG wG))).trans
        (α_ vG uG (x.fG ≫ wG)).symm)

/-- SHORT route is exactly the F34 mixed exchange at the original
nonstrict composite outer left 1-cell; no auxiliary strictification. -/
def compositeMixedHexagonShortIso
    (aF bF aG bG : C)
    {eF eG dF dG cF cG : C}
    (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (vF : dF ⟶ eF) (vG : dG ⟶ eG)
    (wF : bF ⟶ cF) (wG : bG ⟶ cG)
    (x : CompositeComparisonPair aF bF aG bG) :
    (⟨((vF ≫ uF) ≫ x.fF) ≫ wF,
       ((vG ≫ uG) ≫ x.fG) ≫ wG⟩ :
       CompositeComparisonPair dF cF dG cG) ≅
    (⟨(vF ≫ uF) ≫ (x.fF ≫ wF),
       (vG ≫ uG) ≫ (x.fG ≫ wG)⟩ :
       CompositeComparisonPair dF cF dG cG) :=
  structuralComparisonPairIso
    (α_ (vF ≫ uF) x.fF wF)
    (α_ (vG ≫ uG) x.fG wG)

/-- F35 genuine mixed-associator HEXAGON: four independent F31/F34
coherence steps equal the original direct F34 exchange on BOTH F/G
components by the authentic ORIGINAL bicategory pentagon. -/
theorem compositeMixedHexagon
    (aF bF aG bG : C)
    {eF eG dF dG cF cG : C}
    (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (vF : dF ⟶ eF) (vG : dG ⟶ eG)
    (wF : bF ⟶ cF) (wG : bG ⟶ cG)
    (x : CompositeComparisonPair aF bF aG bG) :
    compositeMixedHexagonLongIso aF bF aG bG uF uG vF vG wF wG x =
      compositeMixedHexagonShortIso aF bF aG bG uF uG vF vG wF wG x := by
  apply Iso.ext
  apply Prod.ext
  · apply Iso.ext
    change
      ((((α_ vF uF x.fF).hom ▷ wF ≫
        (α_ vF (uF ≫ x.fF) wF).hom) ≫
        vF ◁ (α_ uF x.fF wF).hom) ≫
        (α_ vF uF (x.fF ≫ wF)).inv) =
        (α_ (vF ≫ uF) x.fF wF).hom
    have h := congrArg
      (fun t => t ≫ (α_ vF uF (x.fF ≫ wF)).inv)
      (Bicategory.pentagon vF uF x.fF wF)
    simpa only [Category.assoc, Iso.hom_inv_id, Category.comp_id] using h
  · change
      ((((α_ vG uG x.fG).hom ▷ wG ≫
        (α_ vG (uG ≫ x.fG) wG).hom) ≫
        vG ◁ (α_ uG x.fG wG).hom) ≫
        (α_ vG uG (x.fG ≫ wG)).inv) =
        (α_ (vG ≫ uG) x.fG wG).hom
    have h := congrArg
      (fun t => t ≫ (α_ vG uG (x.fG ≫ wG)).inv)
      (Bicategory.pentagon vG uG x.fG wG)
    simpa only [Category.assoc, Iso.hom_inv_id, Category.comp_id] using h

/-- The genuine four-step HEXAGON is itself a NATURAL ISOMORPHISM
between two F30 comparison functors. Naturality holds for all F-ISO /
arbitrary (possibly noninvertible) G 2-cell morphisms. -/
def compositeMixedHexagonLongNatIso
    (aF bF aG bG : C)
    {eF eG dF dG cF cG : C}
    (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (vF : dF ⟶ eF) (vG : dG ⟶ eG)
    (wF : bF ⟶ cF) (wG : bG ⟶ cG) :
    (leftCompositeWhiskerFunctor aF bF aG bG
      (vF ≫ uF) (vG ≫ uG) ⋙
      rightCompositeWhiskerFunctor dF bF dG bG wF wG) ≅
    (rightCompositeWhiskerFunctor aF bF aG bG wF wG ⋙
      leftCompositeWhiskerFunctor aF cF aG cG
        (vF ≫ uF) (vG ≫ uG)) :=
  NatIso.ofComponents
    (fun x => compositeMixedHexagonLongIso aF bF aG bG
      uF uG vF vG wF wG x)
    (by
      intro x y pq
      change
        (leftCompositeWhiskerFunctor aF bF aG bG
          (vF ≫ uF) (vG ≫ uG) ⋙
          rightCompositeWhiskerFunctor dF bF dG bG wF wG).map pq ≫
          (compositeMixedHexagonLongIso aF bF aG bG
            uF uG vF vG wF wG y).hom =
        (compositeMixedHexagonLongIso aF bF aG bG
          uF uG vF vG wF wG x).hom ≫
          (rightCompositeWhiskerFunctor aF bF aG bG wF wG ⋙
            leftCompositeWhiskerFunctor aF cF aG cG
              (vF ≫ uF) (vG ≫ uG)).map pq
      rw [compositeMixedHexagon aF bF aG bG uF uG vF vG wF wG x,
          compositeMixedHexagon aF bF aG bG uF uG vF vG wF wG y]
      exact (compositeHorizontalExchangeNatIso aF bF aG bG
        (vF ≫ uF) (vG ≫ uG) wF wG).hom.naturality pq)

/-- F35 higher NATURAL-ISOMORPHISM coherence: not merely a pointwise
identity. All the real four-stage F31/F34 structural pastes equal the
actual F34 mixed exchange as natural isomorphisms on the ENTIRE
F27 comparison category, including arbitrary noninvertible G cells. -/
theorem compositeMixedHexagonNatIso_coherence
    (aF bF aG bG : C)
    {eF eG dF dG cF cG : C}
    (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (vF : dF ⟶ eF) (vG : dG ⟶ eG)
    (wF : bF ⟶ cF) (wG : bG ⟶ cG) :
    compositeMixedHexagonLongNatIso aF bF aG bG uF uG vF vG wF wG =
      compositeHorizontalExchangeNatIso aF bF aG bG
        (vF ≫ uF) (vG ≫ uG) wF wG := by
  apply Iso.ext
  apply NatTrans.ext
  funext x
  change (compositeMixedHexagonLongIso aF bF aG bG
      uF uG vF vG wF wG x).hom =
    (compositeMixedHexagonShortIso aF bF aG bG
      uF uG vF vG wF wG x).hom
  exact congrArg Iso.hom
    (compositeMixedHexagon aF bF aG bG uF uG vF vG wF wG x)

#print axioms compositeMixedHexagonLongIso
#print axioms compositeMixedHexagonShortIso
#print axioms compositeMixedHexagon
#print axioms compositeMixedHexagonLongNatIso
#print axioms compositeMixedHexagonNatIso_coherence

end Generic

end

end KUOS.DependentOriginationCoherentBiadjunctionMixedAssociatorHexagonV5_132
