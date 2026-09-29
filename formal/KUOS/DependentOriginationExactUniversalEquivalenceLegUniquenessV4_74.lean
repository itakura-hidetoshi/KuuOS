import KUOS.DependentOriginationExactUniversalEquivalenceLegLiftabilityV4_73
import Mathlib

namespace KUOS.DependentOriginationExactUniversalEquivalenceLegUniquenessV4_74

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackCarrierV2_9
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationExactPresentationComparisonV4_52
open KUOS.DependentOriginationExactPresentationEssentialUniquenessV4_53
open KUOS.DependentOriginationExactUniversalTargetNaturalityV4_55
open KUOS.DependentOriginationExactUniversalMappingMorphismV4_57
open KUOS.DependentOriginationExactUniversalEquivalenceLegLiftabilityV4_73

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Essential uniqueness of coherent-equivalence lifts v4.74

v4.73 proves that each forward/backward leg of a coherent raw equivalence
between exact-universal source objects lifts to an actual source 1-cell.

A source 1-cell over E.forward can be read as a coherent comparison from
X.presentation transported along E into Y.presentation.  The universal-target
essential uniqueness of Y then says that any two such factor maps are
isomorphic by an invertible modification of their underlying StrongTrans.

Since DO₂ is the induced bicategory on the chosen stack carriers, that
invertible modification packages as an isomorphism between the two DO₂
1-morphisms.

This is exactly the uniqueness supplied by the existing universal property.
We do not silently strengthen it to an invertible source 2-cell: compatibility
of that modification with the raw identity 2-cell remains a separate
obligation.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

/-- A source 1-cell whose raw projection is the forward leg determines a
coherent exact-presentation factor from the transported source presentation to
the target presentation. -/
noncomputable def exactPresentationComparisonOfForwardSourceMorphism
    (X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A)
    (E : HigherRawSystemCoherentEquivalence X.raw Y.raw)
    (f : ExactUniversalRawMorphism (W := W) A X Y)
    (hraw : f.raw = E.forward.comparison) :
    ExactPresentationCoherentComparison
      (W := W) A
      (transportExactPresentation (W := W) A E X.presentation)
      Y.presentation where
  hom := f.lift.hom
  comparison_triangle := by
    simp only [transportExactPresentation_comparison]
    rw [← hraw]
    exact f.comparison_square

/-- The comparison wrapper remembers exactly the DO₂ StrongTrans carried by
the source morphism.  Exposing this projection avoids unfolding the dependent
comparison structure inside essential-uniqueness proofs. -/
@[simp] theorem exactPresentationComparisonOfForwardSourceMorphism_hom
    (X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A)
    (E : HigherRawSystemCoherentEquivalence X.raw Y.raw)
    (f : ExactUniversalRawMorphism (W := W) A X Y)
    (hraw : f.raw = E.forward.comparison) :
    (exactPresentationComparisonOfForwardSourceMorphism
      (W := W) A X Y E f hraw).hom = f.lift.hom :=
  rfl

/-- Two source lifts of the same coherent forward raw-equivalence leg are
isomorphic in the DO₂ hom category. -/
theorem exactUniversalRawMorphism_lifts_iso_of_same_forward_rawEquivalence
    (X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A)
    (E : HigherRawSystemCoherentEquivalence X.raw Y.raw)
    (f g : ExactUniversalRawMorphism (W := W) A X Y)
    (hf : f.raw = E.forward.comparison)
    (hg : g.raw = E.forward.comparison) :
    Nonempty (f.lift ≅ g.lift) := by
  let alpha :=
    exactPresentationComparisonOfForwardSourceMorphism
      (W := W) A X Y E f hf
  let beta :=
    exactPresentationComparisonOfForwardSourceMorphism
      (W := W) A X Y E g hg
  rcases
      Y.universal.essential_unique
        (transportExactPresentation (W := W) A E X.presentation)
        alpha beta with
    ⟨e⟩
  have e' : f.lift.hom ≅ g.lift.hom := by
    simpa only [
      alpha,
      beta,
      exactPresentationComparisonOfForwardSourceMorphism_hom
    ] using e
  exact
    ⟨CategoryTheory.Bicategory.InducedBicategory.isoMk e'⟩

/-- The same essential uniqueness holds for lifts of the backward leg. -/
theorem exactUniversalRawMorphism_lifts_iso_of_same_backward_rawEquivalence
    (X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A)
    (E : HigherRawSystemCoherentEquivalence X.raw Y.raw)
    (f g : ExactUniversalRawMorphism (W := W) A Y X)
    (hf : f.raw = E.backward.comparison)
    (hg : g.raw = E.backward.comparison) :
    Nonempty (f.lift ≅ g.lift) := by
  exact
    exactUniversalRawMorphism_lifts_iso_of_same_forward_rawEquivalence
      (W := W) A Y X E.symm f g
      (by
        simpa only [HigherRawSystemCoherentEquivalence.symm] using hf)
      (by
        simpa only [HigherRawSystemCoherentEquivalence.symm] using hg)

/-!
## Boundary after v4.74

For each leg of a coherent raw equivalence:

* source lifts exist;
* any two source lifts have isomorphic DO₂ realizations.

What remains before obtaining a bicategorical equivalence in the source is
strictly stronger: one needs compatible source 2-isomorphisms between the
chosen forward/backward composites and the source identities.  The raw
unit/counit of E supply the raw components, while v4.74 supplies target-side
essential uniqueness; the missing step is the compatibility equation tying
those two components together.

That equation is the next obstruction boundary and should not be inferred from
DO₂ essential uniqueness alone.
-/

end

end KUOS.DependentOriginationExactUniversalEquivalenceLegUniquenessV4_74
