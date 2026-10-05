import KUOS.DependentOriginationExactClassificationCoherentUniquenessV5_20
import KUOS.DependentOriginationAlignedExactLiftabilityCollapseV5_32
import KUOS.DependentOriginationPointwiseComparisonCoherentEquivalenceV5_34
import Mathlib

namespace KUOS.DependentOriginationExactLiftableCoherentUniversalizationV5_36

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseEquivalenceTransportV2_17
open KUOS.DependentOriginationExactUniversalTargetMutualUniquenessV4_54
open KUOS.DependentOriginationExactUniversalTargetNaturalityV4_55
open KUOS.DependentOriginationExactUniversalMappingMorphismV4_57
open KUOS.DependentOriginationExactUniversalClassificationInterfaceV5_17
open KUOS.DependentOriginationExactClassificationCoherentUniquenessV5_20
open KUOS.DependentOriginationAlignedExactLiftabilityCollapseV5_32
open KUOS.DependentOriginationPointwiseComparisonCoherentEquivalenceV5_34

set_option autoImplicit false

noncomputable section

/-!
# Exact-liftable coherent universalization v5.36

v5.19 produced, under ambient alignment, a canonical exact-universal source
whose raw system maps to the target raw system by a directed pointwise-
equivalence comparison.  v5.32 removed the extra ambient-alignment hypothesis
for the aligned atlas specialization used by the classification program.
v5.34 then proved that every such directed comparison canonically upgrades to a
HigherRawSystemCoherentEquivalence.

The v5.20 transport theorem can therefore now be applied to the actual directed
factor produced by v5.19/v5.32.

This file records that consequence explicitly.

For an exact-liftable classification object X:

1. v5.32 produces an exact-universal classification source Y with the same
   external label and a pointwise-equivalence comparison Y.source.raw -> X.raw;
2. v5.34 upgrades that comparison to a coherent raw equivalence;
3. v5.20 transports Y.source.presentation and Y.source.universal across that
   coherent equivalence;
4. the result is a genuine FixedRawExactUniversalClassificationObject over
   X.raw itself.

Thus exact liftability, under the aligned atlas already fixed by v5.32, now
implies existence of a coherent universal target on the original raw system,
not merely on an auxiliary source raw system.

This still does not make weak admissibility exact, resize arbitrary atlas
universes, or make arbitrary raw morphisms equivalences.
-/

universe u v uH vH uW uP

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable
  (A :
    RefinementAtlas.{u, max u v, uH}
      (LocalizedContext W))

/-! ## Exact-universal classification objects as fixed-raw universal objects -/

/-- Forget only the outer exact-universal classification wrapper while retaining
its external label, exact presentation, and coherent universal-target witness. -/
def exactUniversalClassificationObjectToFixedRaw
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (Y :
      ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel) :
    KUOS.DependentOriginationExactClassificationCoherentUniquenessV5_20.FixedRawExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)
      Y.source.raw where
  label := Y.label
  presentation := Y.source.presentation
  universal := Y.source.universal

@[simp] theorem exactUniversalClassificationObjectToFixedRaw_label
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (Y :
      ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel) :
    (exactUniversalClassificationObjectToFixedRaw
      (W := W) A Y).label = Y.label :=
  rfl

@[simp] theorem exactUniversalClassificationObjectToFixedRaw_presentation
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (Y :
      ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel) :
    (exactUniversalClassificationObjectToFixedRaw
      (W := W) A Y).presentation = Y.source.presentation :=
  rfl

/-! ## v5.20 transport directly from a directed pointwise comparison -/

/-- Transport an exact coherent universal classification object across the
actual v2.17 directed pointwise-equivalence comparison.

v5.34 supplies the coherent inverse/unit/counit data required by v5.20. -/
noncomputable def pointwiseTransportFixedRawExactUniversalClassificationObject
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {R S :
      RawHigherContextualSystem.{u, v, uH, vH}
        (Context := Context)}
    (E : HigherPointwiseEquivalenceComparison R S)
    (X :
      KUOS.DependentOriginationExactClassificationCoherentUniquenessV5_20.FixedRawExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)
        R) :
    KUOS.DependentOriginationExactClassificationCoherentUniquenessV5_20.FixedRawExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)
      S :=
  KUOS.DependentOriginationExactClassificationCoherentUniquenessV5_20.FixedRawExactUniversalClassificationObject.transport
    (W := W) A
    (KUOS.DependentOriginationPointwiseComparisonCoherentEquivalenceV5_34.pointwiseComparisonToCoherentEquivalence E)
    X

@[simp] theorem pointwiseTransportFixedRawExactUniversalClassificationObject_label
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {R S :
      RawHigherContextualSystem.{u, v, uH, vH}
        (Context := Context)}
    (E : HigherPointwiseEquivalenceComparison R S)
    (X :
      KUOS.DependentOriginationExactClassificationCoherentUniquenessV5_20.FixedRawExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)
        R) :
    (pointwiseTransportFixedRawExactUniversalClassificationObject
      (W := W) A E X).label = X.label :=
  rfl

/-- Pointwise transport preserves the chosen DO2 carrier because v5.20/v4.55
transport preserves it definitionally. -/
@[simp] theorem pointwiseTransportFixedRawExactUniversalClassificationObject_carrier
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {R S :
      RawHigherContextualSystem.{u, v, uH, vH}
        (Context := Context)}
    (E : HigherPointwiseEquivalenceComparison R S)
    (X :
      KUOS.DependentOriginationExactClassificationCoherentUniquenessV5_20.FixedRawExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)
        R) :
    (pointwiseTransportFixedRawExactUniversalClassificationObject
      (W := W) A E X).presentation.carrier =
      X.presentation.carrier := by
  exact
    KUOS.DependentOriginationExactClassificationCoherentUniquenessV5_20.FixedRawExactUniversalClassificationObject.transport_carrier
      (W := W) A
      (KUOS.DependentOriginationPointwiseComparisonCoherentEquivalenceV5_34.pointwiseComparisonToCoherentEquivalence E)
      X

/-- The v5.20 mutual coherent uniqueness theorem is now available directly from
a one-way pointwise-equivalence comparison. -/
theorem pointwiseTransported_hasMutualCoherentUniqueness
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {R S :
      RawHigherContextualSystem.{u, v, uH, vH}
        (Context := Context)}
    (E : HigherPointwiseEquivalenceComparison R S)
    (X :
      KUOS.DependentOriginationExactClassificationCoherentUniquenessV5_20.FixedRawExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)
        R)
    (Y :
      KUOS.DependentOriginationExactClassificationCoherentUniquenessV5_20.FixedRawExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)
        S) :
    Nonempty
      (ExactUniversalTargetMutualCoherentUniqueness
        (W := W) A
        (pointwiseTransportFixedRawExactUniversalClassificationObject
          (W := W) A E X).presentation
        Y.presentation) := by
  exact
    KUOS.DependentOriginationExactClassificationCoherentUniquenessV5_20.transported_hasMutualCoherentUniqueness
      (W := W) A
      (KUOS.DependentOriginationPointwiseComparisonCoherentEquivalenceV5_34.pointwiseComparisonToCoherentEquivalence E)
      X Y

/-- Label-preserving v5.20 uniqueness, again requiring only the actual
pointwise-equivalence comparison produced by the classification factorization
layer. -/
theorem pointwiseTransported_existsLabelPreservingMutualCoherentUniqueness
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {R S :
      RawHigherContextualSystem.{u, v, uH, vH}
        (Context := Context)}
    (E : HigherPointwiseEquivalenceComparison R S)
    (X :
      KUOS.DependentOriginationExactClassificationCoherentUniquenessV5_20.FixedRawExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)
        R)
    (Y :
      KUOS.DependentOriginationExactClassificationCoherentUniquenessV5_20.FixedRawExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)
        S)
    (hLabel : X.label = Y.label) :
    Nonempty
      (KUOS.DependentOriginationExactClassificationCoherentUniquenessV5_20.LabelPreservingMutualCoherentUniqueness
        (W := W) A
        (pointwiseTransportFixedRawExactUniversalClassificationObject
          (W := W) A E X)
        Y) := by
  exact
    KUOS.DependentOriginationExactClassificationCoherentUniquenessV5_20.transported_existsLabelPreservingMutualCoherentUniqueness
      (W := W) A
      (KUOS.DependentOriginationPointwiseComparisonCoherentEquivalenceV5_34.pointwiseComparisonToCoherentEquivalence E)
      X Y hLabel

/-! ## Exact-liftable raw systems acquire coherent universal targets -/

/-- Main v5.36 existence theorem.

Every exact-liftable classification object in the aligned atlas specialization
admits a coherent exact-universal classification object over its own raw system,
with the same external label. -/
theorem ExactLiftableClassificationObject.exists_labelPreserving_fixedRawExactUniversalTarget
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel) :
    ∃ U :
        KUOS.DependentOriginationExactClassificationCoherentUniquenessV5_20.FixedRawExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
          (W := W) A
          (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel)
          X.raw,
      U.label = X.label := by
  rcases
      KUOS.DependentOriginationAlignedExactLiftabilityCollapseV5_32.ExactLiftableClassificationObject.exists_labelPreserving_exactUniversalSource
        (W := W) A X with
    ⟨Y, hLabel, ⟨E⟩⟩
  refine
    ⟨pointwiseTransportFixedRawExactUniversalClassificationObject
      (W := W) A E
      (exactUniversalClassificationObjectToFixedRaw
        (W := W) A Y),
      ?_⟩
  simpa using hLabel

/-- Weak-semantic spelling: an explicit exact criterion is sufficient to put a
coherent exact-universal target directly over the original raw system. -/
theorem WeakSemanticClassificationObject.exists_labelPreserving_fixedRawExactUniversalTarget_of_exactCriterion
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      WeakSemanticClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) WorldLabel PresentationLabel)
    (hExact :
      KUOS.DependentOriginationExactLiftabilityCriterionV5_18.ExactLiftabilityCriterion
        (W := W) A X.raw) :
    ∃ U :
        KUOS.DependentOriginationExactClassificationCoherentUniquenessV5_20.FixedRawExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
          (W := W) A
          (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel)
          X.raw,
      U.label = X.label := by
  rcases
      KUOS.DependentOriginationAlignedExactLiftabilityCollapseV5_32.WeakSemanticClassificationObject.exists_labelPreserving_exactUniversalSource_of_exactCriterion
        (W := W) A X hExact with
    ⟨Y, hLabel, ⟨E⟩⟩
  refine
    ⟨pointwiseTransportFixedRawExactUniversalClassificationObject
      (W := W) A E
      (exactUniversalClassificationObjectToFixedRaw
        (W := W) A Y),
      ?_⟩
  simpa using hLabel

/-- Noncomputably choose one coherent universal classification object over the
raw system of an exact-liftable object. -/
noncomputable def fixedRawExactUniversalTargetOfExactLiftable
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel) :
    KUOS.DependentOriginationExactClassificationCoherentUniquenessV5_20.FixedRawExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)
      X.raw :=
  Classical.choose
    (ExactLiftableClassificationObject.exists_labelPreserving_fixedRawExactUniversalTarget
      (W := W) A X)

@[simp] theorem fixedRawExactUniversalTargetOfExactLiftable_label
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel) :
    (fixedRawExactUniversalTargetOfExactLiftable
      (W := W) A X).label = X.label :=
  Classical.choose_spec
    (ExactLiftableClassificationObject.exists_labelPreserving_fixedRawExactUniversalTarget
      (W := W) A X)

/-- The chosen v5.36 target is coherently mutually unique with every other
coherent universal classification target over the same raw system. -/
theorem fixedRawExactUniversalTargetOfExactLiftable_hasMutualCoherentUniqueness
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel)
    (Y :
      KUOS.DependentOriginationExactClassificationCoherentUniquenessV5_20.FixedRawExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)
        X.raw) :
    Nonempty
      (ExactUniversalTargetMutualCoherentUniqueness
        (W := W) A
        (fixedRawExactUniversalTargetOfExactLiftable
          (W := W) A X).presentation
        Y.presentation) := by
  exact
    KUOS.DependentOriginationExactClassificationCoherentUniquenessV5_20.fixedRaw_hasMutualCoherentUniqueness
      (W := W) A
      (fixedRawExactUniversalTargetOfExactLiftable
        (W := W) A X)
      Y

/-!
## Boundary after v5.36

Closed:

* the v5.19/v5.32 directed factor is sufficient for v5.20 transport;
* every exact-liftable classification object in the aligned atlas
  specialization has a coherent universal target over its own raw system;
* that target is mutually coherently unique with every other universal target
  over the same raw system.

Still unchanged:

* weak admissibility alone does not imply exact liftability;
* arbitrary refinement-atlas index universe resizing is not proved;
* arbitrary raw morphisms are not automatically equivalences.  Mapping-level
  functoriality for such morphisms remains the next genuine classification
  frontier.
-/

#print axioms exactUniversalClassificationObjectToFixedRaw
#print axioms pointwiseTransportFixedRawExactUniversalClassificationObject
#print axioms pointwiseTransported_hasMutualCoherentUniqueness
#print axioms ExactLiftableClassificationObject.exists_labelPreserving_fixedRawExactUniversalTarget
#print axioms fixedRawExactUniversalTargetOfExactLiftable
#print axioms fixedRawExactUniversalTargetOfExactLiftable_hasMutualCoherentUniqueness

end

end KUOS.DependentOriginationExactLiftableCoherentUniversalizationV5_36
