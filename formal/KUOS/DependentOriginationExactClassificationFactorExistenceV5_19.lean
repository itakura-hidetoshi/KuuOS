import KUOS.DependentOriginationExactLiftabilityCriterionV5_18
import KUOS.DependentOriginationExactUniversalAmbientCanonicalSourceV5_11
import KUOS.DependentOriginationPointwiseEquivalenceTransportV2_17
import Mathlib

namespace KUOS.DependentOriginationExactClassificationFactorExistenceV5_19

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackCarrierV2_9
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseEquivalenceTransportV2_17
open KUOS.DependentOriginationExactHigherPresentationSectorV4_50
open KUOS.DependentOriginationExactUniversalMappingMorphismV4_57
open KUOS.DependentOriginationExactUniversalAmbientCanonicalSourceV5_11
open KUOS.DependentOriginationExactUniversalClassificationInterfaceV5_17
open KUOS.DependentOriginationExactLiftabilityCriterionV5_18

set_option autoImplicit false

noncomputable section

/-!
# Exact classification factor existence v5.19

v5.18 identifies exact liftability with the existence of a higher localization
factorization whose chosen lift satisfies stack descent.  The next
classification obligation is factor existence.

There is an important type boundary.  An exact-liftable object stores only
existence of an exact presentation of its raw system.  It does not, by itself,
store a coherent universal-target witness for that same raw system.  Therefore
we must not silently turn

  X.raw

itself into an ExactUniversalRawObject.

Instead choose one exact presentation P of X.raw.  Its carrier

  Z := P.carrier

is an actual object of DO₂.  v5.11 attaches to every ambient DO₂ object Z a
canonical exact-universal source whose raw system is the tautological
restriction restrict(Z), whose exact presentation has carrier exactly Z, and
whose presentation is a coherent universal target.

The original exact presentation P already contains a directed
pointwise-equivalence comparison

  restrict(Z) --> X.raw.

Thus every exact-liftable classification object factors through an
exact-universal source while preserving:

* the external classification label literally;
* the selected exact carrier literally;
* the raw semantic object up to the existing directed pointwise-equivalence
  comparison.

This is the exact factor-existence statement justified by the current formal
development.  No inverse raw comparison and no coherent uniqueness between
different choices of exact presentation are asserted here.
-/

universe u v uH vH uW uP

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

/-- Factor data from one exact-liftable classification object through an
exact-universal source.

The source raw system need not be definitionally equal to X.raw.  The directed
pointwise-equivalence comparison records the precise relationship. -/
structure ExactUniversalClassificationFactor
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      ExactLiftableClassificationObject
        (W := W) A WorldLabel PresentationLabel) where
  /-- The selected exact presentation of the original raw system. -/
  presentation :
    ExactHigherDependentOriginationPresentation
      (W := W) A X.raw
  /-- The exact-universal source canonically attached to the selected carrier,
  retaining the external classification label. -/
  source :
    ExactUniversalClassificationObject
      (W := W) A WorldLabel PresentationLabel
  /-- The external label is preserved literally. -/
  label_eq :
    source.label = X.label
  /-- The universal source realizes to exactly the selected exact carrier. -/
  carrier_eq :
    source.source.carrier = presentation.carrier
  /-- The tautological restriction raw system of the universal source compares
  by a directed pointwise equivalence to the original raw system. -/
  comparison :
    HigherPointwiseEquivalenceComparison
      source.source.raw X.raw

/-- Build exact-universal factor data from one explicitly selected exact
presentation.

The only universal-target choice is the v5.11 canonical witness attached to
the ambient carrier P.carrier. -/
noncomputable def exactUniversalClassificationFactorOfPresentation
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      ExactLiftableClassificationObject
        (W := W) A WorldLabel PresentationLabel)
    (P :
      ExactHigherDependentOriginationPresentation
        (W := W) A X.raw) :
    ExactUniversalClassificationFactor
      (W := W) A X where
  presentation := P
  source :=
    { label := X.label
      source :=
        exactUniversalAmbientCanonicalSource
          (W := W) A P.carrier }
  label_eq := rfl
  carrier_eq := by
    exact
      exactUniversalAmbientCanonicalSource_carrier
        (W := W) A P.carrier
  comparison :=
    { comparison := by
        change
          ((restrictHigherLocalizedSystem W
              (higherStackObjectVal (W := W) A P.carrier) :
            RawHigherContextualSystem.{u, v, uH, vH}
              (Context := Context)) ⟶
            X.raw
        exact P.comparison
      comparison_isEquivalence := by
        intro U
        change (P.comparison.app (.mk U)).toFunctor.IsEquivalence
        exact P.comparison_isEquivalence U }

/-- The factor built from P preserves the external label definitionally. -/
@[simp] theorem exactUniversalClassificationFactorOfPresentation_label
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      ExactLiftableClassificationObject
        (W := W) A WorldLabel PresentationLabel)
    (P :
      ExactHigherDependentOriginationPresentation
        (W := W) A X.raw) :
    (exactUniversalClassificationFactorOfPresentation
      (W := W) A X P).source.label =
      X.label :=
  rfl

/-- The realized carrier of the factor built from P is exactly P.carrier. -/
theorem exactUniversalClassificationFactorOfPresentation_carrier
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      ExactLiftableClassificationObject
        (W := W) A WorldLabel PresentationLabel)
    (P :
      ExactHigherDependentOriginationPresentation
        (W := W) A X.raw) :
    (exactUniversalClassificationFactorOfPresentation
      (W := W) A X P).source.source.carrier =
      P.carrier := by
  exact
    exactUniversalAmbientCanonicalSource_carrier
      (W := W) A P.carrier

/-- Every exact-liftable classification object admits exact-universal factor
data. -/
theorem ExactLiftableClassificationObject.existsExactUniversalClassificationFactor
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      ExactLiftableClassificationObject
        (W := W) A WorldLabel PresentationLabel) :
    Nonempty
      (ExactUniversalClassificationFactor
        (W := W) A X) := by
  rcases X.exact with ⟨P⟩
  let F :
      ExactUniversalClassificationFactor
        (W := W) A X :=
    exactUniversalClassificationFactorOfPresentation
      (W := W) A X P
  exact ⟨F⟩

/-- A concise existence statement: every exact-liftable classification object
has a label-preserving exact-universal source whose raw system compares
pointwise-equivalently to the original raw system. -/
theorem ExactLiftableClassificationObject.exists_labelPreserving_exactUniversalSource
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      ExactLiftableClassificationObject
        (W := W) A WorldLabel PresentationLabel) :
    ∃ Y :
        ExactUniversalClassificationObject
          (W := W) A WorldLabel PresentationLabel,
      Y.label = X.label ∧
        Nonempty
          (HigherPointwiseEquivalenceComparison
            Y.source.raw X.raw) := by
  rcases
      ExactLiftableClassificationObject.existsExactUniversalClassificationFactor
        (W := W) A X with
    ⟨F⟩
  exact ⟨F.source, F.label_eq, ⟨F.comparison⟩⟩

/-- The same factor-existence result starts from a weak semantic object once an
explicit v5.18 exact-liftability criterion witness is supplied.

No implication from weak admissibility alone is used. -/
theorem WeakSemanticClassificationObject.exists_labelPreserving_exactUniversalSource_ofCriterion
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      WeakSemanticClassificationObject
        (W := W) WorldLabel PresentationLabel)
    (hCriterion :
      ExactLiftabilityCriterion (W := W) A X.raw) :
    ∃ Y :
        ExactUniversalClassificationObject
          (W := W) A WorldLabel PresentationLabel,
      Y.label = X.label ∧
        Nonempty
          (HigherPointwiseEquivalenceComparison
            Y.source.raw X.raw) := by
  let XExact :
      ExactLiftableClassificationObject
        (W := W) A WorldLabel PresentationLabel :=
    weakSemanticClassificationObjectToExactLiftableOfCriterion
      (W := W) A X hCriterion
  rcases
      ExactLiftableClassificationObject.exists_labelPreserving_exactUniversalSource
        (W := W) A XExact with
    ⟨Y, hLabel, hComparison⟩
  exact ⟨Y, hLabel, hComparison⟩

/-!
## Boundary after v5.19

Factor existence is now explicit:

  exact-liftable X
      -> choose exact presentation P of X.raw
      -> Z := P.carrier in DO₂
      -> canonical exact-universal source S(Z)
      -> directed pointwise-equivalence comparison
           S(Z).raw = restrict(Z) --> X.raw.

The source preserves the external label and realizes to exactly the selected
carrier.

This does not yet prove coherent uniqueness of factors arising from two
different exact presentations P and Q of the same raw system.  v4.52 already
warns that the common-target pointwise-equivalence cospan does not by itself
produce a coherent directed comparison P --> Q.  Therefore the next theorem
unit must formulate coherent uniqueness with precisely the additional
universal/coherence data that are already theorem-backed, rather than
manufacturing an inverse StrongTrans or identifying arbitrary factors.

The countermodel boundary from v5.18 remains unchanged: weak admissibility
alone does not produce the criterion required to enter this factorization
theorem.
-/

end

end KUOS.DependentOriginationExactClassificationFactorExistenceV5_19
