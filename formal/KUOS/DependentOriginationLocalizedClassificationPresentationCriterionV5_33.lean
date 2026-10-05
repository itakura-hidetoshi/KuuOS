import KUOS.DependentOriginationAlignedExactLiftabilityCollapseV5_32
import KUOS.DependentOriginationExactHigherPresentationInvarianceV4_51
import KUOS.DependentOriginationExactPresentationComparisonV4_52
import Mathlib

namespace KUOS.DependentOriginationLocalizedClassificationPresentationCriterionV5_33

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackCarrierV2_9
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseEquivalenceTransportV2_17
open KUOS.DependentOriginationExactHigherPresentationSectorV4_50
open KUOS.DependentOriginationExactHigherPresentationInvarianceV4_51
open KUOS.DependentOriginationExactPresentationComparisonV4_52
open KUOS.DependentOriginationExactUniversalClassificationInterfaceV5_17
open KUOS.DependentOriginationExactLiftabilityCriterionV5_18
open KUOS.DependentOriginationAlignedExactLiftabilityCollapseV5_32

set_option autoImplicit false

noncomputable section

/-!
# Label-preserving localized presentation criterion v5.33

v5.32 closes the universe-alignment bookkeeping gap under the atlas
specialization already used by v5.19:

  ExactLiftabilityCriterion R
    <-> AmbientAlignedExactLiftabilityCriterion R.

The present theorem unit turns that result into a direct object-level
classification criterion.  For a fixed external classification label and raw
system R, exact liftability is equivalent to existence of a localized labelled
DO₂ object Z carrying the same external label together with a directed
pointwise-equivalence comparison

  restrict(Z.carrier) --> R.

The forward direction deliberately passes through the v5.32 exact-universal
source theorem and then reuses the source presentation comparison.  The reverse
direction is carrier-first: Z.carrier plus the supplied comparison is exactly an
ExactHigherDependentOriginationPresentation of R.

This file does not assert weak admissibility -> exact liftability, does not
resize arbitrary atlas index universes, and does not upgrade a directed
pointwise-equivalence comparison to a two-sided coherent raw equivalence.
-/

universe u v uH vH uW uP

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable
  (A :
    RefinementAtlas.{u, max u v, uH}
      (LocalizedContext W))

/-- Raw contextual system obtained by restricting the carrier of a localized
classification object back to the original context. -/
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

/-- Direct labelled localized-presentation predicate.

The external label is preserved literally.  The mathematical witness is only
the directed pointwise-equivalence comparison supported by the existing
presentation interface. -/
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

/-- Under the aligned-atlas specialization, exact liftability is exactly
existence of a label-preserving localized classification presentation. -/
theorem exactLiftabilityCriterion_iff_labelPreservingLocalizedPresentation
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (label : ClassificationLabel WorldLabel PresentationLabel)
    (R :
      RawHigherContextualSystem.{u, v, uH, vH}
        (Context := Context)) :
    ExactLiftabilityCriterion (W := W) A R ↔
      HasLabelPreservingLocalizedClassificationPresentation
        (W := W) A label R := by
  constructor
  · intro hExact
    let X :
        ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
          (W := W) A WorldLabel PresentationLabel :=
      { label := label
        raw := R
        exact :=
          (hasExactHigherDependentOriginationPresentation_iff_exactLiftabilityCriterion
            (W := W) A R).2 hExact }
    rcases
        KUOS.DependentOriginationAlignedExactLiftabilityCollapseV5_32.ExactLiftableClassificationObject.exists_labelPreserving_exactUniversalSource
          (W := W) A X with
      ⟨Y, hLabel, ⟨E⟩⟩
    let P :
        ExactHigherDependentOriginationPresentation
          (W := W) A R :=
      exactPresentationOfPointwiseEquivalenceComparison
        (W := W) A Y.source.presentation E
    refine ⟨Y.realize (W := W) A, ?_, ?_⟩
    · exact hLabel
    · refine ⟨?_⟩
      change
        HigherPointwiseEquivalenceComparison
          (exactPresentationRestrictedCarrier (W := W) A P)
          R
      exact exactPresentationToRawComparison (W := W) A P
  · rintro ⟨Z, _hLabel, ⟨E⟩⟩
    have hPresentation :
        HasExactHigherDependentOriginationPresentation
          (W := W) A R := by
      refine ⟨?_⟩
      exact
        { carrier := Z.carrier
          comparison := E.comparison
          comparison_isEquivalence := E.comparison_isEquivalence }
    exact
      (hasExactHigherDependentOriginationPresentation_iff_exactLiftabilityCriterion
        (W := W) A R).1 hPresentation

/-- Classification-object spelling for a weak semantic object.  Its stored weak
admissibility is not used to manufacture exactness; the iff is controlled
entirely by the exact criterion above. -/
theorem WeakSemanticClassificationObject.exactLiftabilityCriterion_iff_labelPreservingLocalizedPresentation
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      WeakSemanticClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) WorldLabel PresentationLabel) :
    ExactLiftabilityCriterion (W := W) A X.raw ↔
      HasLabelPreservingLocalizedClassificationPresentation
        (W := W) A X.label X.raw :=
  exactLiftabilityCriterion_iff_labelPreservingLocalizedPresentation
    (W := W) A X.label X.raw

/-- Exact-liftable classification objects satisfy the same direct localized
presentation criterion with their external label retained literally. -/
theorem ExactLiftableClassificationObject.exactLiftabilityCriterion_iff_labelPreservingLocalizedPresentation
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel) :
    ExactLiftabilityCriterion (W := W) A X.raw ↔
      HasLabelPreservingLocalizedClassificationPresentation
        (W := W) A X.label X.raw :=
  exactLiftabilityCriterion_iff_labelPreservingLocalizedPresentation
    (W := W) A X.label X.raw

/-- In particular, every exact-liftable classification object has a localized
label-preserving presentation, with no additional ambient-alignment witness. -/
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

Within the aligned-atlas specialization, the exact raw/classification layer now
has a direct localized object presentation criterion:

  ExactLiftabilityCriterion R
    <->
  exists label-preserving Z in LocalizedClassification,
    restrict(Z.carrier) --> R pointwise-equivalently.

The reverse direction uses only the defining carrier-first exact-presentation
interface.  Therefore the result does not collapse any of the remaining
boundaries: weak admissibility is still insufficient, arbitrary atlas resizing
is still absent, and directed pointwise equivalence remains weaker than a
two-sided coherent raw equivalence.
-/

#print axioms exactLiftabilityCriterion_iff_labelPreservingLocalizedPresentation
#print axioms WeakSemanticClassificationObject.exactLiftabilityCriterion_iff_labelPreservingLocalizedPresentation
#print axioms ExactLiftableClassificationObject.exactLiftabilityCriterion_iff_labelPreservingLocalizedPresentation
#print axioms ExactLiftableClassificationObject.exists_labelPreserving_localizedPresentation

end

end KUOS.DependentOriginationLocalizedClassificationPresentationCriterionV5_33
