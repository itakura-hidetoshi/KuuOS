import KUOS.DependentOriginationCoherentBiadjunctionQuotientCategoryCompatibilityV5_126

namespace KUOS.DependentOriginationCoherentBiadjunctionHorizontalCompositeFunctorsV5_127

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionComparisonCompressionFunctorV5_124.Generic
open KUOS.DependentOriginationCoherentBiadjunctionNonstrictKernelWhiskeringV5_126.Generic

set_option autoImplicit false
noncomputable section

/-!
# F30 / v5.127: actual functoriality of horizontal comparison operations

The F29 descended horizontal operations are not just maps of 2-cells:
left and right whiskering each define a real functor between ordinary
F27 composite-comparison categories, with genuine identity/composition
laws. F-side comparisons remain invertible and G-side comparison cells
remain arbitrary and potentially noninvertible.

This is the target-level prerequisite for descent to the actual F28
compression-kernel quotient categories, without asserting new
biequivalence of ambient bicategories.
-/

namespace Generic

universe uC vC wC
variable {C : Type uC} [Bicategory.{wC, vC} C]

/-- Real LEFT horizontal comparison functor for a fixed pair of
original outer 1-cells, acting independently on the F-ISO and on
the G arbitrary (possibly noninvertible) 2-cell. -/
def leftCompositeWhiskerFunctor (aF bF aG bG : C)
    {eF eG : C} (uF : eF ⟶ aF) (uG : eG ⟶ aG) :
    CompositeComparisonPair aF bF aG bG ⥤
      CompositeComparisonPair eF bF eG bG where
  obj x := ⟨uF ≫ x.fF, uG ≫ x.fG⟩
  map {_ _} pq := (Bicategory.whiskerLeftIso uF pq.1, uG ◁ pq.2)
  map_id x := by
    apply Prod.ext
    · apply Iso.ext
      change uF ◁ (𝟙 x.fF) = 𝟙 (uF ≫ x.fF)
      exact Bicategory.whiskerLeft_id uF x.fF
    · exact Bicategory.whiskerLeft_id uG x.fG
  map_comp p q := by
    apply Prod.ext
    · apply Iso.ext
      change uF ◁ (p.1.hom ≫ q.1.hom) =
        (uF ◁ p.1.hom) ≫ (uF ◁ q.1.hom)
      exact Bicategory.whiskerLeft_comp uF p.1.hom q.1.hom
    · exact Bicategory.whiskerLeft_comp uG p.2 q.2

/-- Real RIGHT horizontal comparison functor; G-side morphisms
are still ordinary 2-cells rather than isomorphisms. -/
def rightCompositeWhiskerFunctor (aF bF aG bG : C)
    {eF eG : C} (vF : bF ⟶ eF) (vG : bG ⟶ eG) :
    CompositeComparisonPair aF bF aG bG ⥤
      CompositeComparisonPair aF eF aG eG where
  obj x := ⟨x.fF ≫ vF, x.fG ≫ vG⟩
  map {_ _} pq := (Bicategory.whiskerRightIso pq.1 vF, pq.2 ▷ vG)
  map_id x := by
    apply Prod.ext
    · apply Iso.ext
      change (𝟙 x.fF) ▷ vF = 𝟙 (x.fF ≫ vF)
      exact Bicategory.id_whiskerRight x.fF vF
    · exact Bicategory.id_whiskerRight x.fG vG
  map_comp p q := by
    apply Prod.ext
    · apply Iso.ext
      change (p.1.hom ≫ q.1.hom) ▷ vF =
        (p.1.hom ▷ vF) ≫ (q.1.hom ▷ vF)
      exact Bicategory.comp_whiskerRight p.1.hom q.1.hom vF
    · exact Bicategory.comp_whiskerRight p.2 q.2 vG

/-- The left functor's actual arrow map is precisely the full
F29 horizontal operation, not only naturally equivalent to it. -/
theorem leftCompositeWhiskerFunctor_map (aF bF aG bG : C)
    {eF eG : C} (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    {x y : CompositeComparisonPair aF bF aG bG}
    (pq : x ⟶ y) :
    (leftCompositeWhiskerFunctor aF bF aG bG uF uG).map pq =
      (Bicategory.whiskerLeftIso uF pq.1, uG ◁ pq.2) := rfl

/-- Right functor's arrow map retains the original noninvertible
G-side horizontal whiskering. -/
theorem rightCompositeWhiskerFunctor_map (aF bF aG bG : C)
    {eF eG : C} (vF : bF ⟶ eF) (vG : bG ⟶ eG)
    {x y : CompositeComparisonPair aF bF aG bG}
    (pq : x ⟶ y) :
    (rightCompositeWhiskerFunctor aF bF aG bG vF vG).map pq =
      (Bicategory.whiskerRightIso pq.1 vF, pq.2 ▷ vG) := rfl

#print axioms leftCompositeWhiskerFunctor
#print axioms rightCompositeWhiskerFunctor
#print axioms leftCompositeWhiskerFunctor_map
#print axioms rightCompositeWhiskerFunctor_map

end Generic

end

end KUOS.DependentOriginationCoherentBiadjunctionHorizontalCompositeFunctorsV5_127
