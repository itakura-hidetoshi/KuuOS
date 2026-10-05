import KUOS.DependentOriginationLocalizedClassificationPresentationCriterionV5_33
import KUOS.DependentOriginationClassificationCoherentBiequivalenceV5_31
import Mathlib

namespace KUOS.DependentOriginationAlignedClassificationWitnessPackageV5_34

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseEquivalenceTransportV2_17
open KUOS.DependentOriginationExactUniversalClassificationInterfaceV5_17
open KUOS.DependentOriginationExactLiftabilityCriterionV5_18
open KUOS.DependentOriginationClassificationCoherentBiequivalenceV5_31
open KUOS.DependentOriginationLocalizedClassificationPresentationCriterionV5_33

set_option autoImplicit false

noncomputable section

/-!
# Aligned classification witness package v5.34

v5.33 proves the aligned-atlas object-level proposition

  ExactLiftabilityCriterion X.raw
    <->
  exists a label-preserving localized classification presentation of X.raw.

For the next mapping/classification layer, the existential proposition is more
useful as explicit data.  This file therefore introduces a witness structure
carrying exactly:

* a localized labelled DO₂ object;
* literal equality of its external label with the source label;
* a directed pointwise-equivalence comparison from the restricted localized
  carrier to the raw system.

The witness contains no reverse raw comparison and no coherence modification.
Consequently it is intentionally weaker than a two-sided coherent raw
equivalence.

The file then packages two already-proved levels together:

1. the v5.31 coherent biequivalence between exact-universal classification
   objects and localized classification objects;
2. the v5.33 exact-liftability criterion, now expressed as nonemptiness of the
   explicit witness type.

No implication from weak admissibility alone is introduced, and no arbitrary
atlas-universe resizing is claimed.
-/

universe u v uH vH uW uP

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable
  (A :
    RefinementAtlas.{u, max u v, uH}
      (LocalizedContext W))

/-- Explicit data underlying a label-preserving localized presentation of a raw
higher contextual system.

This is the data hidden behind the existential/Nonempty proposition of v5.33.
The comparison remains directed. -/
structure LabelPreservingLocalizedPresentationWitness
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
  comparison :
    HigherPointwiseEquivalenceComparison
      (localizedClassificationRestrictedCarrier
        (W := W) A target)
      R

/-- The v5.33 existential predicate is precisely nonemptiness of the explicit
witness type. -/
theorem hasLabelPreservingLocalizedClassificationPresentation_iff_nonemptyWitness
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (label : ClassificationLabel WorldLabel PresentationLabel)
    (R :
      RawHigherContextualSystem.{u, v, uH, vH}
        (Context := Context)) :
    HasLabelPreservingLocalizedClassificationPresentation
        (W := W) A label R ↔
      Nonempty
        (LabelPreservingLocalizedPresentationWitness
          (W := W) A label R) := by
  constructor
  · rintro ⟨Z, hLabel, ⟨E⟩⟩
    exact
      ⟨{
        target := Z
        label_eq := hLabel
        comparison := E
      }⟩
  · rintro ⟨P⟩
    exact
      ⟨P.target, P.label_eq, ⟨P.comparison⟩⟩

/-- Weak semantic object spelling of the direct aligned classification
criterion, now retaining the localized presentation as explicit data. -/
theorem WeakSemanticClassificationObject.exactLiftabilityCriterion_iff_nonemptyLocalizedPresentationWitness
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      WeakSemanticClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) WorldLabel PresentationLabel) :
    ExactLiftabilityCriterion (W := W) A X.raw ↔
      Nonempty
        (LabelPreservingLocalizedPresentationWitness
          (W := W) A X.label X.raw) := by
  exact
    (KUOS.DependentOriginationLocalizedClassificationPresentationCriterionV5_33.WeakSemanticClassificationObject.exactLiftabilityCriterion_iff_labelPreservingLocalizedPresentation
      (W := W) A X).trans
      (hasLabelPreservingLocalizedClassificationPresentation_iff_nonemptyWitness
        (W := W) A X.label X.raw)

/-- Every exact-liftable classification object has explicit localized
presentation data with the same external label. -/
theorem ExactLiftableClassificationObject.nonempty_labelPreservingLocalizedPresentationWitness
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel) :
    Nonempty
      (LabelPreservingLocalizedPresentationWitness
        (W := W) A X.label X.raw) := by
  exact
    (hasLabelPreservingLocalizedClassificationPresentation_iff_nonemptyWitness
      (W := W) A X.label X.raw).1
      (KUOS.DependentOriginationLocalizedClassificationPresentationCriterionV5_33.ExactLiftableClassificationObject.exists_labelPreserving_localizedPresentation
        (W := W) A X)

/-- Choose one explicit localized presentation from an exact criterion witness.

The choice is noncomputable by design; the theorem-level equivalence does not
assert a canonical raw-to-localized inverse comparison. -/
noncomputable def localizedPresentationWitnessOfExactCriterion
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      WeakSemanticClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) WorldLabel PresentationLabel)
    (hExact :
      ExactLiftabilityCriterion (W := W) A X.raw) :
    LabelPreservingLocalizedPresentationWitness
      (W := W) A X.label X.raw :=
  Classical.choice
    ((WeakSemanticClassificationObject.exactLiftabilityCriterion_iff_nonemptyLocalizedPresentationWitness
      (W := W) A X).1 hExact)

/-- Conversely, explicit localized presentation data reconstructs the
exact-liftable classification object while preserving label and raw system
definitionally. -/
def exactLiftableClassificationObjectOfLocalizedPresentationWitness
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      WeakSemanticClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) WorldLabel PresentationLabel)
    (P :
      LabelPreservingLocalizedPresentationWitness
        (W := W) A X.label X.raw) :
    ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel :=
  weakSemanticClassificationObjectToExactLiftableOfCriterion
    (W := W) A X
    ((WeakSemanticClassificationObject.exactLiftabilityCriterion_iff_nonemptyLocalizedPresentationWitness
      (W := W) A X).2 ⟨P⟩)

@[simp] theorem exactLiftableClassificationObjectOfLocalizedPresentationWitness_label
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      WeakSemanticClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) WorldLabel PresentationLabel)
    (P :
      LabelPreservingLocalizedPresentationWitness
        (W := W) A X.label X.raw) :
    (exactLiftableClassificationObjectOfLocalizedPresentationWitness
      (W := W) A X P).label = X.label :=
  rfl

@[simp] theorem exactLiftableClassificationObjectOfLocalizedPresentationWitness_raw
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      WeakSemanticClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) WorldLabel PresentationLabel)
    (P :
      LabelPreservingLocalizedPresentationWitness
        (W := W) A X.label X.raw) :
    (exactLiftableClassificationObjectOfLocalizedPresentationWitness
      (W := W) A X P).raw = X.raw :=
  rfl

/-! ## Unified aligned classification certificate -/

/-- The strongest current aligned classification package at the two levels that
are formally justified:

* coherent biequivalence on the exact-universal classification bicategory;
* object-level exact-liftability iff explicit label-preserving localized
  presentation data for weak semantic objects.

The package deliberately does not add morphisms to the merely exact-liftable
layer, because one directed pointwise-equivalence comparison is insufficient
for a two-sided coherent raw equivalence. -/
structure AlignedClassificationTheoremCertificate
    (WorldLabel : Type uW)
    (PresentationLabel : Type uP) where
  coherent :
    WhiteheadTriangleRepresentativeCertificate
      (ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel)
      (LocalizedClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel)
  exactCriterionPresentation :
    ∀ X :
      WeakSemanticClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) WorldLabel PresentationLabel,
      ExactLiftabilityCriterion (W := W) A X.raw ↔
        Nonempty
          (LabelPreservingLocalizedPresentationWitness
            (W := W) A X.label X.raw)

/-- Canonical assembly of the current aligned classification theorem package. -/
noncomputable def alignedClassificationTheoremCertificate
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP} :
    AlignedClassificationTheoremCertificate
      (W := W) A WorldLabel PresentationLabel where
  coherent :=
    exactUniversalClassificationCoherentBiequivalenceCertificate
      (W := W) A
  exactCriterionPresentation := by
    intro X
    exact
      WeakSemanticClassificationObject.exactLiftabilityCriterion_iff_nonemptyLocalizedPresentationWitness
        (W := W) A X

/-!
## Boundary after v5.34

The aligned exact sector now has both:

* a coherent classification biequivalence at the chosen exact-universal source
  level; and
* an explicit witness type characterizing exactly which weak semantic raw
  objects admit a label-preserving localized presentation.

What remains genuinely stronger is morphism-level transport on the merely
exact-liftable/raw layer.  A witness here contains only

  restrict(Z.carrier) --> R

as a directed pointwise equivalence.  It does not contain R --> restrict(Z),
triangle modifications, or a coherent raw equivalence.  Those data must not be
inferred silently.

The weak-admissibility counterexample and the arbitrary-atlas universe-resizing
boundary are unchanged.
-/

#print axioms hasLabelPreservingLocalizedClassificationPresentation_iff_nonemptyWitness
#print axioms WeakSemanticClassificationObject.exactLiftabilityCriterion_iff_nonemptyLocalizedPresentationWitness
#print axioms ExactLiftableClassificationObject.nonempty_labelPreservingLocalizedPresentationWitness
#print axioms localizedPresentationWitnessOfExactCriterion
#print axioms alignedClassificationTheoremCertificate

end

end KUOS.DependentOriginationAlignedClassificationWitnessPackageV5_34
