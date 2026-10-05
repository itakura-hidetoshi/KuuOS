import KUOS.DependentOriginationAlignedExactLiftabilityCollapseV5_32
import Mathlib

namespace KUOS.DependentOriginationLocalizedClassificationPresentationCriterionV5_33

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackCarrierV2_9
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseEquivalenceTransportV2_17
open KUOS.DependentOriginationExactHigherPresentationSectorV4_50
open KUOS.DependentOriginationExactUniversalClassificationInterfaceV5_17
open KUOS.DependentOriginationExactLiftabilityCriterionV5_18
open KUOS.DependentOriginationAlignedExactLiftabilityCollapseV5_32

open scoped CategoryTheory.Pseudofunctor.StrongTrans

set_option autoImplicit false

noncomputable section

/-!
# Label-preserving localized presentation criterion v5.33

v5.32 removes the extra ambient-alignment witness under the atlas universe
specialization already used by v5.19.  This theorem unit turns that result into
a direct classification-level presentation criterion.

For a weak semantic classification object X, exact liftability of X.raw is
equivalent to existence of a localized labelled DO₂ object Z with the same
external label and a directed pointwise-equivalence comparison

  restrict(Z.carrier) --> X.raw.

The forward direction uses the v5.32 weak-object exact-universal source bridge.
The source's chosen exact presentation comparison is then composed with the
v5.32 directed raw comparison.  The reverse direction is carrier-first:
Z.carrier plus the supplied comparison is exactly an
ExactHigherDependentOriginationPresentation of X.raw.

No implication from weak admissibility alone is asserted.  No arbitrary atlas
universe resizing is introduced, and directed pointwise equivalence is not
upgraded to a two-sided coherent raw equivalence.
-/

universe u v uH vH uW uP

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable
  (A :
    RefinementAtlas.{u, max u v, uH}
      (LocalizedContext W))

/-- Raw contextual system obtained by restricting a localized classification
carrier back to the original context. -/
abbrev localizedClassificationRestrictedCarrier
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (Z :
      LocalizedClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel) :
    RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context) :=
  restrictHigherLocalizedSystem W
    (higherStackObjectVal (W := W) A Z.carrier)

/-- Direct label-preserving localized-presentation predicate. -/
def HasLabelPreservingLocalizedClassificationPresentation
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (label : ClassificationLabel WorldLabel PresentationLabel)
    (R :
      RawHigherContextualSystem.{u, v, uH, vH}
        (Context := Context)) : Prop :=
  ∃ Z :
      LocalizedClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel,
    Z.label = label ∧
      Nonempty
        (HigherPointwiseEquivalenceComparison
          (localizedClassificationRestrictedCarrier
            (W := W) A Z)
          R)

/-- For a weak semantic classification object, exact liftability is equivalent
to existence of a localized presentation carrying the same external label.

The stored weak admissibility is not used as a substitute for exactness: the
forward implication consumes an explicit ExactLiftabilityCriterion witness. -/
theorem WeakSemanticClassificationObject.exactLiftabilityCriterion_iff_labelPreservingLocalizedPresentation
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      WeakSemanticClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) WorldLabel PresentationLabel) :
    ExactLiftabilityCriterion (W := W) A X.raw ↔
      HasLabelPreservingLocalizedClassificationPresentation
        (W := W) A X.label X.raw := by
  constructor
  · intro hExact
    rcases
        KUOS.DependentOriginationAlignedExactLiftabilityCollapseV5_32.WeakSemanticClassificationObject.exists_labelPreserving_exactUniversalSource_of_exactCriterion
          (W := W) A X hExact with
      ⟨Y, hLabel, ⟨E⟩⟩
    refine ⟨Y.realize (W := W) A, ?_, ?_⟩
    · exact hLabel
    · refine ⟨?_⟩
      exact
        { comparison :=
            Y.source.presentation.comparison ≫ E.comparison
          comparison_isEquivalence := by
            intro C
            letI :
                (Y.source.presentation.comparison.app (.mk C)).toFunctor.IsEquivalence :=
              Y.source.presentation.comparison_isEquivalence C
            letI :
                (E.comparison.app (.mk C)).toFunctor.IsEquivalence :=
              E.comparison_isEquivalence C
            change
              ((Y.source.presentation.comparison.app (.mk C)).toFunctor ⋙
                (E.comparison.app (.mk C)).toFunctor).IsEquivalence
            infer_instance }
  · rintro ⟨Z, _hLabel, ⟨E⟩⟩
    have hPresentation :
        HasExactHigherDependentOriginationPresentation
          (W := W) A X.raw := by
      refine ⟨?_⟩
      exact
        { carrier := Z.carrier
          comparison := E.comparison
          comparison_isEquivalence := E.comparison_isEquivalence }
    exact
      (hasExactHigherDependentOriginationPresentation_iff_exactLiftabilityCriterion
        (W := W) A X.raw).1 hPresentation

/-- Exact-liftable objects inherit the same iff by forgetting only to their
weak semantic wrapper; label and raw carrier are definitionally unchanged. -/
theorem ExactLiftableClassificationObject.exactLiftabilityCriterion_iff_labelPreservingLocalizedPresentation
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel) :
    ExactLiftabilityCriterion (W := W) A X.raw ↔
      HasLabelPreservingLocalizedClassificationPresentation
        (W := W) A X.label X.raw := by
  simpa only [
      ExactLiftableClassificationObject.toWeak_label,
      ExactLiftableClassificationObject.toWeak_raw] using
    (WeakSemanticClassificationObject.exactLiftabilityCriterion_iff_labelPreservingLocalizedPresentation
      (W := W) A (X.toWeak (W := W) A))

/-- Every exact-liftable classification object therefore has a localized
label-preserving presentation, with no additional alignment witness. -/
theorem ExactLiftableClassificationObject.exists_labelPreserving_localizedPresentation
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel) :
    HasLabelPreservingLocalizedClassificationPresentation
      (W := W) A X.label X.raw := by
  exact
    (ExactLiftableClassificationObject.exactLiftabilityCriterion_iff_labelPreservingLocalizedPresentation
      (W := W) A X).1
      (KUOS.DependentOriginationExactLiftabilityCriterionV5_18.ExactLiftableClassificationObject.satisfiesExactLiftabilityCriterion
        (W := W) A X)

/-!
## Boundary after v5.33

Within the aligned-atlas specialization:

  ExactLiftabilityCriterion X.raw
    <->
  exists label-preserving Z in LocalizedClassification,
    restrict(Z.carrier) --> X.raw pointwise-equivalently.

The reverse implication uses only the carrier-first exact-presentation
interface.  Thus weak admissibility remains insufficient, arbitrary atlas
resizing remains absent, and directed pointwise equivalence remains strictly
weaker data than a two-sided coherent raw equivalence.
-/

#print axioms WeakSemanticClassificationObject.exactLiftabilityCriterion_iff_labelPreservingLocalizedPresentation
#print axioms ExactLiftableClassificationObject.exactLiftabilityCriterion_iff_labelPreservingLocalizedPresentation
#print axioms ExactLiftableClassificationObject.exists_labelPreserving_localizedPresentation

end

end KUOS.DependentOriginationLocalizedClassificationPresentationCriterionV5_33
