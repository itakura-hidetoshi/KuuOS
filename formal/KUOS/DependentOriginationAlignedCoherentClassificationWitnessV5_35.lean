import KUOS.DependentOriginationAlignedClassificationWitnessPackageV5_34
import KUOS.DependentOriginationPointwiseComparisonCoherentEquivalenceV5_34
import Mathlib

namespace KUOS.DependentOriginationAlignedCoherentClassificationWitnessV5_35

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseEquivalenceTransportV2_17
open KUOS.DependentOriginationExactUniversalTargetNaturalityV4_55
open KUOS.DependentOriginationExactUniversalClassificationInterfaceV5_17
open KUOS.DependentOriginationExactLiftabilityCriterionV5_18
open KUOS.DependentOriginationClassificationCoherentBiequivalenceV5_31
open KUOS.DependentOriginationLocalizedClassificationPresentationCriterionV5_33
open KUOS.DependentOriginationAlignedClassificationWitnessPackageV5_34
open KUOS.DependentOriginationPointwiseComparisonCoherentEquivalenceV5_34

set_option autoImplicit false

noncomputable section

/-!
# Aligned coherent classification witness v5.35

The first v5.34 classification witness package retained the v5.33 directed
pointwise-equivalence comparison explicitly.  The second v5.34 theorem then
proved that every such directed comparison canonically upgrades to the
two-sided coherent raw equivalence required by the v4.55 transport layer.

This file combines those two results.

The new witness stores:

* the localized classification target;
* literal equality of the external classification label;
* a genuine HigherRawSystemCoherentEquivalence from the restricted localized
  carrier to the raw system.

The old explicit witness is not discarded.  It canonically upgrades to the new
coherent witness, and every coherent witness forgets back to the old directed
one through its forward comparison.  Hence nonemptiness of the two witness
types is equivalent.

Consequently the aligned ExactLiftabilityCriterion is equivalent to nonemptiness
of an explicit label-preserving coherent presentation witness.

This closes the stale v5.34 boundary saying that the explicit witness carried
too little data for coherent raw transport.  It does not prove weak
admissibility implies exact liftability, does not resize arbitrary atlas
universes, and does not turn arbitrary raw morphisms into equivalences.
-/

universe u v uH vH uW uP

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable
  (A :
    RefinementAtlas.{u, max u v, uH}
      (LocalizedContext W))

/-- Explicit label-preserving localized presentation data carrying the
two-sided coherent raw equivalence now supplied by the second v5.34 theorem. -/
structure LabelPreservingLocalizedCoherentPresentationWitness
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (label : ClassificationLabel WorldLabel PresentationLabel)
    (R :
      RawHigherContextualSystem.{u, v, uH, vH}
        (Context := Context)) where
  target :
    LocalizedClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel
  label_eq : target.label = label
  equivalence :
    HigherRawSystemCoherentEquivalence
      (KUOS.DependentOriginationLocalizedClassificationPresentationCriterionV5_33.localizedClassificationRestrictedCarrier
        (W := W) A target)
      R

/-- Upgrade the original explicit directed witness of the first v5.34 package
to a coherent witness using the pointwise-to-coherent theorem. -/
noncomputable def
    directedWitnessToCoherent
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {label : ClassificationLabel WorldLabel PresentationLabel}
    {R :
      RawHigherContextualSystem.{u, v, uH, vH}
        (Context := Context)}
    (P :
      KUOS.DependentOriginationAlignedClassificationWitnessPackageV5_34.LabelPreservingLocalizedPresentationWitness
        (W := W) A label R) :
    LabelPreservingLocalizedCoherentPresentationWitness
      (W := W) A label R where
  target := P.target
  label_eq := P.label_eq
  equivalence :=
    KUOS.DependentOriginationPointwiseComparisonCoherentEquivalenceV5_34.pointwiseComparisonToCoherentEquivalence
      P.comparison

/-- Forget a coherent witness back to the original directed witness through the
forward comparison of the coherent raw equivalence. -/
def coherentWitnessToDirected
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {label : ClassificationLabel WorldLabel PresentationLabel}
    {R :
      RawHigherContextualSystem.{u, v, uH, vH}
        (Context := Context)}
    (P :
      LabelPreservingLocalizedCoherentPresentationWitness
        (W := W) A label R) :
    KUOS.DependentOriginationAlignedClassificationWitnessPackageV5_34.LabelPreservingLocalizedPresentationWitness
      (W := W) A label R where
  target := P.target
  label_eq := P.label_eq
  comparison := P.equivalence.forward

@[simp] theorem
    directedWitnessToCoherent_target
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {label : ClassificationLabel WorldLabel PresentationLabel}
    {R :
      RawHigherContextualSystem.{u, v, uH, vH}
        (Context := Context)}
    (P :
      KUOS.DependentOriginationAlignedClassificationWitnessPackageV5_34.LabelPreservingLocalizedPresentationWitness
        (W := W) A label R) :
    (directedWitnessToCoherent
      (W := W) A P).target = P.target :=
  rfl

@[simp] theorem
    coherentWitnessToDirected_target
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {label : ClassificationLabel WorldLabel PresentationLabel}
    {R :
      RawHigherContextualSystem.{u, v, uH, vH}
        (Context := Context)}
    (P :
      LabelPreservingLocalizedCoherentPresentationWitness
        (W := W) A label R) :
    (coherentWitnessToDirected (W := W) A P).target = P.target :=
  rfl

/-- The old explicit directed witness and the new coherent witness have
equivalent existence content. -/
theorem nonemptyLocalizedPresentationWitness_iff_nonemptyCoherentWitness
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (label : ClassificationLabel WorldLabel PresentationLabel)
    (R :
      RawHigherContextualSystem.{u, v, uH, vH}
        (Context := Context)) :
    Nonempty
        (KUOS.DependentOriginationAlignedClassificationWitnessPackageV5_34.LabelPreservingLocalizedPresentationWitness
          (W := W) A label R) ↔
      Nonempty
        (LabelPreservingLocalizedCoherentPresentationWitness
          (W := W) A label R) := by
  constructor
  · rintro ⟨P⟩
    exact
      ⟨directedWitnessToCoherent
        (W := W) A P⟩
  · rintro ⟨P⟩
    exact
      ⟨coherentWitnessToDirected (W := W) A P⟩

/-- The existential coherent-presentation predicate of the second v5.34 file is
precisely nonemptiness of the explicit coherent witness type. -/
theorem
    hasLabelPreservingLocalizedClassificationCoherentPresentation_iff_nonemptyWitness
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (label : ClassificationLabel WorldLabel PresentationLabel)
    (R :
      RawHigherContextualSystem.{u, v, uH, vH}
        (Context := Context)) :
    KUOS.DependentOriginationPointwiseComparisonCoherentEquivalenceV5_34.HasLabelPreservingLocalizedClassificationCoherentPresentation
        (W := W) A label R ↔
      Nonempty
        (LabelPreservingLocalizedCoherentPresentationWitness
          (W := W) A label R) := by
  constructor
  · rintro ⟨Z, hLabel, ⟨E⟩⟩
    exact
      ⟨{
        target := Z
        label_eq := hLabel
        equivalence := E
      }⟩
  · rintro ⟨P⟩
    exact
      ⟨P.target, P.label_eq, ⟨P.equivalence⟩⟩

/-- Main v5.35 criterion: exact liftability is equivalent to nonemptiness of an
explicit label-preserving coherent localized presentation witness. -/
theorem exactLiftabilityCriterion_iff_nonemptyLocalizedCoherentPresentationWitness
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (label : ClassificationLabel WorldLabel PresentationLabel)
    (R :
      RawHigherContextualSystem.{u, v, uH, vH}
        (Context := Context)) :
    ExactLiftabilityCriterion (W := W) A R ↔
      Nonempty
        (LabelPreservingLocalizedCoherentPresentationWitness
          (W := W) A label R) := by
  exact
    (KUOS.DependentOriginationPointwiseComparisonCoherentEquivalenceV5_34.exactLiftabilityCriterion_iff_labelPreservingLocalizedCoherentPresentation
      (W := W) A label R).trans
      (hasLabelPreservingLocalizedClassificationCoherentPresentation_iff_nonemptyWitness
        (W := W) A label R)

/-- Weak semantic object spelling of the coherent explicit-witness criterion. -/
theorem
    WeakSemanticClassificationObject.exactLiftabilityCriterion_iff_nonemptyLocalizedCoherentPresentationWitness
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      WeakSemanticClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) WorldLabel PresentationLabel) :
    ExactLiftabilityCriterion (W := W) A X.raw ↔
      Nonempty
        (LabelPreservingLocalizedCoherentPresentationWitness
          (W := W) A X.label X.raw) := by
  exact
    exactLiftabilityCriterion_iff_nonemptyLocalizedCoherentPresentationWitness
      (W := W) A X.label X.raw

/-- Every exact-liftable classification object has an explicit
label-preserving coherent localized presentation witness. -/
theorem
    ExactLiftableClassificationObject.nonempty_labelPreservingLocalizedCoherentPresentationWitness
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel) :
    Nonempty
      (LabelPreservingLocalizedCoherentPresentationWitness
        (W := W) A X.label X.raw) := by
  exact
    (exactLiftabilityCriterion_iff_nonemptyLocalizedCoherentPresentationWitness
      (W := W) A X.label X.raw).1
      (KUOS.DependentOriginationExactLiftabilityCriterionV5_18.ExactLiftableClassificationObject.satisfiesExactLiftabilityCriterion
        (W := W) A X)

/-- Choose the coherent explicit witness determined existentially by an exact
criterion witness. -/
noncomputable def localizedCoherentPresentationWitnessOfExactCriterion
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      WeakSemanticClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) WorldLabel PresentationLabel)
    (hExact :
      ExactLiftabilityCriterion (W := W) A X.raw) :
    LabelPreservingLocalizedCoherentPresentationWitness
      (W := W) A X.label X.raw :=
  Classical.choice
    ((WeakSemanticClassificationObject.exactLiftabilityCriterion_iff_nonemptyLocalizedCoherentPresentationWitness
      (W := W) A X).1 hExact)

/-- A coherent explicit witness reconstructs the exact-liftable classification
object by forgetting only to its forward directed comparison. -/
def exactLiftableClassificationObjectOfLocalizedCoherentPresentationWitness
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      WeakSemanticClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) WorldLabel PresentationLabel)
    (P :
      LabelPreservingLocalizedCoherentPresentationWitness
        (W := W) A X.label X.raw) :
    ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel :=
  KUOS.DependentOriginationAlignedClassificationWitnessPackageV5_34.exactLiftableClassificationObjectOfLocalizedPresentationWitness
    (W := W) A X
    (coherentWitnessToDirected (W := W) A P)

@[simp] theorem
    exactLiftableClassificationObjectOfLocalizedCoherentPresentationWitness_label
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      WeakSemanticClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) WorldLabel PresentationLabel)
    (P :
      LabelPreservingLocalizedCoherentPresentationWitness
        (W := W) A X.label X.raw) :
    (exactLiftableClassificationObjectOfLocalizedCoherentPresentationWitness
      (W := W) A X P).label = X.label :=
  rfl

@[simp] theorem
    exactLiftableClassificationObjectOfLocalizedCoherentPresentationWitness_raw
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      WeakSemanticClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) WorldLabel PresentationLabel)
    (P :
      LabelPreservingLocalizedCoherentPresentationWitness
        (W := W) A X.label X.raw) :
    (exactLiftableClassificationObjectOfLocalizedCoherentPresentationWitness
      (W := W) A X P).raw = X.raw :=
  rfl

/-! ## Strengthened aligned certificate -/

/-- The aligned classification certificate after closing the explicit
pointwise-versus-coherent witness gap.

The previous v5.34 certificate is retained verbatim as base data, while the new
field records the stronger exact-criterion characterization by an explicit
coherent witness. -/
structure AlignedCoherentClassificationTheoremCertificate
    (WorldLabel : Type uW)
    (PresentationLabel : Type uP) where
  base :
    KUOS.DependentOriginationAlignedClassificationWitnessPackageV5_34.AlignedClassificationTheoremCertificate
      (W := W) A WorldLabel PresentationLabel
  exactCriterionCoherentPresentation :
    ∀ X :
      WeakSemanticClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) WorldLabel PresentationLabel,
      ExactLiftabilityCriterion (W := W) A X.raw ↔
        Nonempty
          (LabelPreservingLocalizedCoherentPresentationWitness
            (W := W) A X.label X.raw)

/-- Canonical assembly of the strengthened aligned coherent classification
certificate. -/
noncomputable def alignedCoherentClassificationTheoremCertificate
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP} :
    AlignedCoherentClassificationTheoremCertificate
      (W := W) A WorldLabel PresentationLabel where
  base :=
    KUOS.DependentOriginationAlignedClassificationWitnessPackageV5_34.alignedClassificationTheoremCertificate
      (W := W) A
  exactCriterionCoherentPresentation := by
    intro X
    exact
      WeakSemanticClassificationObject.exactLiftabilityCriterion_iff_nonemptyLocalizedCoherentPresentationWitness
        (W := W) A X

/-!
## Boundary after v5.35

Closed at object level:

* every v5.34 directed explicit presentation witness canonically upgrades to a
  coherent raw-equivalence witness;
* exact liftability is equivalent to nonemptiness of that coherent witness;
* the aligned classification certificate now records this stronger statement.

Still open / unchanged:

* weak semantic admissibility alone does not imply exact liftability;
* arbitrary refinement-atlas index universes have not been resized away;
* arbitrary raw morphisms are not equivalences merely because source and target
  objects are exact-liftable.  Their transport still belongs to the established
  exact-universal mapping-morphism machinery.
-/

#print axioms directedWitnessToCoherent
#print axioms nonemptyLocalizedPresentationWitness_iff_nonemptyCoherentWitness
#print axioms exactLiftabilityCriterion_iff_nonemptyLocalizedCoherentPresentationWitness
#print axioms ExactLiftableClassificationObject.nonempty_labelPreservingLocalizedCoherentPresentationWitness
#print axioms alignedCoherentClassificationTheoremCertificate

end

end KUOS.DependentOriginationAlignedCoherentClassificationWitnessV5_35
