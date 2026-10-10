import KUOS.DependentOriginationCoherentBiadjunctionComparisonKernelHomQuotientV5_125
import Mathlib.CategoryTheory.Quotient
import Mathlib.CategoryTheory.Equivalence

namespace KUOS.DependentOriginationCoherentBiadjunctionCompressionKernelQuotientCategoryV5_125

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionFiniteMateComparisonChainsV5_122.Generic
open KUOS.DependentOriginationCoherentBiadjunctionFiniteComparisonChainConcatenationV5_123.Generic
open KUOS.DependentOriginationCoherentBiadjunctionComparisonCompressionFunctorV5_124.Generic
open KUOS.DependentOriginationCoherentBiadjunctionComparisonKernelHomQuotientV5_125.Generic

set_option autoImplicit false
noncomputable section

/-!
# F28 / v5.125: true category quotient by the compression kernel

The F27 full comparison-compression functor induces its original HomRel.
The pinned mathlib category quotient of precisely that relation
preserves native finite path composition. Since the relation IS the
compression kernel, the quotient does not introduce any extra
identifications, and its lifted comparison functor is fully faithful
and essentially surjective: an actual equivalence of ordinary
comparison-presentation CATEGORIES, not a biequivalence of the
original ambient bicategories B and C.

Together with F28's genuine quotient-Hom boundary functions, this
shows descent of both original lax right-mate pastings through an
actual category quotient, with no invertibility imposed on G cells.
-/

namespace Generic

universe uB vB wB uC vC wC
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]

/-- Actual kernel HomRel induced by the SAME F27 compression functor,
not a newly stipulated relation or a strictified comparison. -/
def compressionKernelHomRel (aF bF aG bG : C) :
    HomRel (ComparisonPair aF bF aG bG) :=
  (comparisonCompressionFunctor aF bF aG bG).homRel

/-- The kernel relation is a congruence under the GENUINE F26
concatenation in the original unquotiented finite-path category. -/
instance compressionKernelCongruence (aF bF aG bG : C) :
    Congruence (compressionKernelHomRel aF bF aG bG) :=
  Functor.congruence_homRel (comparisonCompressionFunctor aF bF aG bG)

/-- The ACTUAL mathlib quotient category by the compression kernel.
Its homs are quotient classes of original finite path presentations;
its composition is the induced native path composition. -/
def compressionKernelCategory (aF bF aG bG : C) :=
  CategoryTheory.Quotient (compressionKernelHomRel aF bF aG bG)

/-- The canonical functor from the unquotiented F26 comparison-path
category into the genuine quotient category. -/
def comparisonKernelQuotientFunctor (aF bF aG bG : C) :
    ComparisonPair aF bF aG bG ⥤
      compressionKernelCategory aF bF aG bG :=
  CategoryTheory.Quotient.functor (compressionKernelHomRel aF bF aG bG)

/-- The ORIGINAL F27 compression descends to a true functor OUT OF
the actual quotient category via the pinned mathlib universal lift. -/
def quotientCompositeFunctor (aF bF aG bG : C) :
    compressionKernelCategory aF bF aG bG ⥤
      CompositeComparisonPair aF bF aG bG :=
  CategoryTheory.Quotient.lift
    (compressionKernelHomRel aF bF aG bG)
    (comparisonCompressionFunctor aF bF aG bG)
    (fun _ _ _ _ h => h)

/-- No extra identifications: two original finite paths map to the
SAME quotient arrow iff the original F and G composites agree. -/
theorem kernelQuotient_map_eq_iff
    (aF bF aG bG : C)
    {x y : ComparisonPair aF bF aG bG}
    (c₁ c₂ : x ⟶ y) :
    (comparisonKernelQuotientFunctor aF bF aG bG).map c₁ =
      (comparisonKernelQuotientFunctor aF bF aG bG).map c₂ ↔
        c₁.fComposite = c₂.fComposite ∧
        c₁.gComposite = c₂.gComposite := by
  have h := CategoryTheory.Quotient.functor_map_eq_iff
    (compressionKernelHomRel aF bF aG bG) c₁ c₂
  exact h.trans (comparisonCompressionFunctor_map_eq_iff aF bF aG bG c₁ c₂)

/-- Functor-level factorization: quotient first, then compress,
is EXACTLY the original F27 compression (not merely naturally iso). -/
theorem compression_factors_through_kernel_quotient
    (aF bF aG bG : C) :
    comparisonKernelQuotientFunctor aF bF aG bG ⋙
      quotientCompositeFunctor aF bF aG bG =
        comparisonCompressionFunctor aF bF aG bG := by
  exact CategoryTheory.Quotient.lift_spec
    (compressionKernelHomRel aF bF aG bG)
    (comparisonCompressionFunctor aF bF aG bG)
    (fun _ _ _ _ h => h)

/-- The quotient-to-composite functor is FULL: the canonical singleton
path lifts every genuine F-ISO / arbitrary G 2-cell. -/
instance quotientCompositeFunctorFull (aF bF aG bG : C) :
    (quotientCompositeFunctor aF bF aG bG).Full where
  map_surjective := by
    rintro ⟨x⟩ ⟨y⟩ pq
    obtain ⟨p, hp⟩ :=
      (comparisonCompressionFunctor aF bF aG bG).map_surjective pq
    refine ⟨(comparisonKernelQuotientFunctor aF bF aG bG).map p, ?_⟩
    simpa only [quotientCompositeFunctor, comparisonKernelQuotientFunctor,
      CategoryTheory.Quotient.lift_map_functor_map] using hp

/-- The lifted compression is FAITHFUL: the only path
identifications are the original F/G composite kernel relation. -/
instance quotientCompositeFunctorFaithful (aF bF aG bG : C) :
    (quotientCompositeFunctor aF bF aG bG).Faithful where
  map_injective := by
    intro X Y p q h
    rcases X with ⟨x⟩
    rcases Y with ⟨y⟩
    induction p using Quot.inductionOn with
    | _ p =>
        induction q using Quot.inductionOn with
        | _ q =>
            have hh : (compressionKernelHomRel aF bF aG bG) p q := h
            exact (CategoryTheory.Quotient.functor_map_eq_iff
              (compressionKernelHomRel aF bF aG bG) p q).2 hh

/-- Every compressed F/G comparison object has a genuine preimage in
the kernel quotient category, with the SAME original pair of 1-cells. -/
instance quotientCompositeFunctorEssSurj (aF bF aG bG : C) :
    (quotientCompositeFunctor aF bF aG bG).EssSurj :=
  Functor.essSurj_of_surj (by
    intro y
    exact ⟨⟨⟨y.fF, y.fG⟩⟩, rfl⟩)

/-- Therefore the *ordinary comparison categories* become equivalent
after quotienting presentations by the exact compression kernel.
This makes NO claim of a biequivalence of the base bicategories. -/
instance quotientCompositeFunctorIsEquivalence (aF bF aG bG : C) :
    (quotientCompositeFunctor aF bF aG bG).IsEquivalence where
  faithful := inferInstance
  full := inferInstance
  essSurj := inferInstance

/-- A real equivalence of ordinary categories constructed from the
exact full, faithful and essentially surjective lifted functor. -/
def comparisonKernelEquivalence (aF bF aG bG : C) :
    compressionKernelCategory aF bF aG bG ≌
      CompositeComparisonPair aF bF aG bG :=
  Functor.asEquivalence (quotientCompositeFunctor aF bF aG bG)

#print axioms compressionKernelHomRel
#print axioms compressionKernelCongruence
#print axioms compressionKernelCategory
#print axioms comparisonKernelQuotientFunctor
#print axioms quotientCompositeFunctor
#print axioms kernelQuotient_map_eq_iff
#print axioms compression_factors_through_kernel_quotient
#print axioms quotientCompositeFunctorFull
#print axioms quotientCompositeFunctorFaithful
#print axioms quotientCompositeFunctorEssSurj
#print axioms quotientCompositeFunctorIsEquivalence
#print axioms comparisonKernelEquivalence

end Generic

end

end KUOS.DependentOriginationCoherentBiadjunctionCompressionKernelQuotientCategoryV5_125
