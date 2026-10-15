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

A source 1-cell over E.forward is a coherent comparison from the transported
source presentation into the target presentation. Essential uniqueness in the
target supplies an isomorphism of the underlying StrongTrans, hence an
isomorphism between the two DO₂ lifts in the induced hom category.

This does not assert a compatible source 2-isomorphism. Compatibility with the
raw identity modification is a separate, strictly stronger obligation.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

/-- A source lift of the forward leg defines a coherent exact-presentation
comparison from the transported source into the target. -/
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
    change
      (restrictHigherLocalizedStrongTrans (W := W) f.lift.hom ≫
        Y.presentation.comparison) ≅
      (X.presentation.comparison ≫ E.forward.comparison)
    rw [← hraw]
    exact f.comparison_square

/-- The comparison wrapper retains exactly the underlying DO₂ StrongTrans. -/
@[simp] theorem exactPresentationComparisonOfForwardSourceMorphism_hom
    (X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A)
    (E : HigherRawSystemCoherentEquivalence X.raw Y.raw)
    (f : ExactUniversalRawMorphism (W := W) A X Y)
    (hraw : f.raw = E.forward.comparison) :
    (exactPresentationComparisonOfForwardSourceMorphism
      (W := W) A X Y E f hraw).hom = f.lift.hom :=
  rfl

/-- Any two source lifts of the same forward raw-equivalence leg have
isomorphic DO₂ realizations. -/
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
        alpha beta with ⟨e⟩
  have e' : f.lift.hom ≅ g.lift.hom := e
  exact ⟨CategoryTheory.Bicategory.InducedBicategory.isoMk e'⟩

/-- The same target-side essential uniqueness holds for the backward leg. -/
theorem exactUniversalRawMorphism_lifts_iso_of_same_backward_rawEquivalence
    (X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A)
    (E : HigherRawSystemCoherentEquivalence X.raw Y.raw)
    (f g : ExactUniversalRawMorphism (W := W) A Y X)
    (hf : f.raw = E.backward.comparison)
    (hg : g.raw = E.backward.comparison) :
    Nonempty (f.lift ≅ g.lift) :=
  exactUniversalRawMorphism_lifts_iso_of_same_forward_rawEquivalence
    (W := W) A Y X E.symm f g hf hg

/-!
## Boundary after v4.74

For each leg of a coherent raw equivalence, source lifts exist and their DO₂
realizations are unique up to isomorphism. The raw unit and counit have not yet
been paired with compatible DO₂ modifications to form source 2-isomorphisms.
The missing comparison-square equation must not be inferred from target-side
essential uniqueness alone.
-/

end

end KUOS.DependentOriginationExactUniversalEquivalenceLegUniquenessV4_74
