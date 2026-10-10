import KUOS.DependentOriginationCoherentBiadjunctionHorizontalQuotientFunctorsV5_127

namespace KUOS.DependentOriginationCoherentBiadjunctionHorizontalAssociatorUnitorCompositeV5_128

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionComparisonCompressionFunctorV5_124.Generic
open KUOS.DependentOriginationCoherentBiadjunctionHorizontalCompositeFunctorsV5_127.Generic

set_option autoImplicit false
noncomputable section

/-!
# F31/v5.128: genuine nonstrict associator and unitor on horizontal comparisons

F30's horizontal whiskering functors are not strict as the surrounding
bicategory is not strict. Actual bicategorical associators and unitors
therefore provide componentwise ISOMORPHISMS of comparison-pair objects.
We build actual NatIso values, with naturality proved for a genuine
invertible F comparison and an arbitrary potentially NONINVERTIBLE
G comparison. No G-side invertibility is imposed on comparison arrows.
-/

namespace Generic

universe uC vC wC
variable {C : Type uC} [Bicategory.{wC, vC} C]

/-- A pair of original hom-category isomorphisms gives a genuine
isomorphism in the F27 composite comparison-pair category. The G
isomorphism here is the STRUCTURAL associator/unitor, not a restriction
on general G comparison morphisms. -/
def structuralComparisonPairIso
    {aF bF aG bG : C}
    {x y : CompositeComparisonPair aF bF aG bG}
    (p : x.fF ≅ y.fF) (q : x.fG ≅ y.fG) : x ≅ y where
  hom := (p, q.hom)
  inv := (p.symm, q.inv)
  hom_inv_id := by
    apply Prod.ext
    · apply Iso.ext
      change p.hom ≫ p.inv = 𝟙 x.fF
      exact p.hom_inv_id
    · exact q.hom_inv_id
  inv_hom_id := by
    apply Prod.ext
    · apply Iso.ext
      change p.inv ≫ p.hom = 𝟙 y.fF
      exact p.inv_hom_id
    · exact q.inv_hom_id

/-- Native left associator is a NATURAL ISOMORPHISM between successive
and composite left-whiskering functors. The F/G comparison cells retain
their authentic original orientations. -/
def leftCompositeAssociatorNatIso
    (aF bF aG bG : C)
    {eF eG dF dG : C}
    (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (vF : dF ⟶ eF) (vG : dG ⟶ eG) :
    leftCompositeWhiskerFunctor aF bF aG bG (vF ≫ uF) (vG ≫ uG) ≅
      leftCompositeWhiskerFunctor aF bF aG bG uF uG ⋙
        leftCompositeWhiskerFunctor eF bF eG bG vF vG :=
  NatIso.ofComponents
    (fun x => structuralComparisonPairIso
      (α_ vF uF x.fF) (α_ vG uG x.fG))
    (by
      intro x y pq
      apply Prod.ext
      · apply Iso.ext
        change ((vF ≫ uF) ◁ pq.1.hom) ≫ (α_ vF uF y.fF).hom =
          (α_ vF uF x.fF).hom ≫ vF ◁ (uF ◁ pq.1.hom)
        exact Bicategory.associator_naturality_right vF uF pq.1.hom
      · change ((vG ≫ uG) ◁ pq.2) ≫ (α_ vG uG y.fG).hom =
          (α_ vG uG x.fG).hom ≫ vG ◁ (uG ◁ pq.2)
        exact Bicategory.associator_naturality_right vG uG pq.2)

/-- Native right associator NATURAL ISOMORPHISM between the two
non-strict compositions of F30 right-whiskering functors. -/
def rightCompositeAssociatorNatIso
    (aF bF aG bG : C)
    {eF eG dF dG : C}
    (uF : bF ⟶ eF) (uG : bG ⟶ eG)
    (vF : eF ⟶ dF) (vG : eG ⟶ dG) :
    (rightCompositeWhiskerFunctor aF bF aG bG uF uG ⋙
      rightCompositeWhiskerFunctor aF eF aG eG vF vG) ≅
        rightCompositeWhiskerFunctor aF bF aG bG
          (uF ≫ vF) (uG ≫ vG) :=
  NatIso.ofComponents
    (fun x => structuralComparisonPairIso
      (α_ x.fF uF vF) (α_ x.fG uG vG))
    (by
      intro x y pq
      apply Prod.ext
      · apply Iso.ext
        change ((pq.1.hom ▷ uF) ▷ vF) ≫ (α_ y.fF uF vF).hom =
          (α_ x.fF uF vF).hom ≫ pq.1.hom ▷ (uF ≫ vF)
        exact Bicategory.associator_naturality_left pq.1.hom uF vF
      · change ((pq.2 ▷ uG) ▷ vG) ≫ (α_ y.fG uG vG).hom =
          (α_ x.fG uG vG).hom ≫ pq.2 ▷ (uG ≫ vG)
        exact Bicategory.associator_naturality_left pq.2 uG vG)

/-- Original LEFT unitor compares the actual identity left-whisker
functor with the identity comparison functor by native naturality. -/
def leftCompositeUnitorNatIso (aF bF aG bG : C) :
    leftCompositeWhiskerFunctor aF bF aG bG (𝟙 aF) (𝟙 aG) ≅
      𝟭 (CompositeComparisonPair aF bF aG bG) :=
  NatIso.ofComponents
    (fun x => structuralComparisonPairIso (λ_ x.fF) (λ_ x.fG))
    (by
      intro x y pq
      apply Prod.ext
      · apply Iso.ext
        change ((𝟙 aF) ◁ pq.1.hom) ≫ (λ_ y.fF).hom =
          (λ_ x.fF).hom ≫ pq.1.hom
        exact Bicategory.leftUnitor_naturality pq.1.hom
      · change ((𝟙 aG) ◁ pq.2) ≫ (λ_ y.fG).hom =
          (λ_ x.fG).hom ≫ pq.2
        exact Bicategory.leftUnitor_naturality pq.2)

/-- Original RIGHT unitor compares F30 identity right-whiskering with
the identity functor, preserving noninvertible G comparisons. -/
def rightCompositeUnitorNatIso (aF bF aG bG : C) :
    rightCompositeWhiskerFunctor aF bF aG bG (𝟙 bF) (𝟙 bG) ≅
      𝟭 (CompositeComparisonPair aF bF aG bG) :=
  NatIso.ofComponents
    (fun x => structuralComparisonPairIso (ρ_ x.fF) (ρ_ x.fG))
    (by
      intro x y pq
      apply Prod.ext
      · apply Iso.ext
        change (pq.1.hom ▷ 𝟙 bF) ≫ (ρ_ y.fF).hom =
          (ρ_ x.fF).hom ≫ pq.1.hom
        exact Bicategory.rightUnitor_naturality pq.1.hom
      · change (pq.2 ▷ 𝟙 bG) ≫ (ρ_ y.fG).hom =
          (ρ_ x.fG).hom ≫ pq.2
        exact Bicategory.rightUnitor_naturality pq.2)

#print axioms structuralComparisonPairIso
#print axioms leftCompositeAssociatorNatIso
#print axioms rightCompositeAssociatorNatIso
#print axioms leftCompositeUnitorNatIso
#print axioms rightCompositeUnitorNatIso

end Generic

end

end KUOS.DependentOriginationCoherentBiadjunctionHorizontalAssociatorUnitorCompositeV5_128
