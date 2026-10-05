import KUOS.DependentOriginationExactClassificationFactorExistenceV5_19
import KUOS.DependentOriginationExactUniversalTargetMutualUniquenessV4_54
import KUOS.DependentOriginationExactUniversalTargetNaturalityV4_55
import Mathlib

namespace KUOS.DependentOriginationExactClassificationCoherentUniquenessV5_20

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackDescentV2_8
open KUOS.DependentOriginationHigherStackCarrierV2_9
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseEquivalenceTransportV2_17
open KUOS.DependentOriginationExactHigherPresentationSectorV4_50
open KUOS.DependentOriginationExactPresentationComparisonV4_52
open KUOS.DependentOriginationExactPresentationEssentialUniquenessV4_53
open KUOS.DependentOriginationExactUniversalTargetMutualUniquenessV4_54
open KUOS.DependentOriginationExactUniversalTargetNaturalityV4_55
open KUOS.DependentOriginationExactUniversalClassificationInterfaceV5_17
open KUOS.DependentOriginationExactClassificationFactorExistenceV5_19

set_option autoImplicit false

noncomputable section

/-!
# Classification coherent uniqueness v5.20

v5.19 isolates the factor-existence boundary and deliberately does not identify
arbitrary exact-universal factors.  The present theorem unit adds exactly the
coherent uniqueness already justified by v4.54-v4.55.

There are two distinct statements.

1. Fixed raw system.

   For a fixed raw higher contextual system R, two exact presentations Q₁ and
   Q₂ equipped with coherent universal-target witnesses are mutually coherent:

     Q₁ --> Q₂,
     Q₂ --> Q₁,

   and the two roundtrips are modification-isomorphic to the corresponding
   coherent identities.

   External classification labels are retained separately.  Carrier/presentation
   uniqueness does not erase or identify them.  If the labels are known equal,
   that equality is packaged alongside the coherent uniqueness datum.

2. Transport across raw systems.

   Given an explicit v4.55 HigherRawSystemCoherentEquivalence R S, an exact
   coherent universal target over R transports to one over S with the same
   external label and the same DO₂ carrier.  Once transported, v4.54 compares
   it coherently with every other universal target over S.

No theorem below upgrades a one-way HigherPointwiseEquivalenceComparison to a
two-sided coherent raw equivalence.  Hence the directed factor supplied by
v5.19 is not silently sufficient for cross-raw uniqueness.
-/

universe u v uH vH uW uP

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

/-- A classification object over one fixed raw system, retaining the external
label independently of its exact universal presentation. -/
structure FixedRawExactUniversalClassificationObject
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (R :
      RawHigherContextualSystem.{u, v, uH, vH}
        (Context := Context)) where
  label :
    ClassificationLabel WorldLabel PresentationLabel
  presentation :
    ExactHigherDependentOriginationPresentation
      (W := W) A R
  universal :
    ExactPresentationCoherentUniversalTarget
      (W := W) A presentation

/-- Fixed-raw coherent uniqueness with explicit retention of label equality.

The coherent field is the v4.54 mutual comparison datum.  The label field is
kept independent: mathematical uniqueness of the universal presentation does
not manufacture equality of external names. -/
structure LabelPreservingMutualCoherentUniqueness
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {R :
      RawHigherContextualSystem.{u, v, uH, vH}
        (Context := Context)}
    (X Y :
      FixedRawExactUniversalClassificationObject
        (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) R) where
  label_eq :
    X.label = Y.label
  coherent :
    ExactUniversalTargetMutualCoherentUniqueness
      (W := W) A X.presentation Y.presentation

/-- Any two universal classification presentations over the same raw system
have v4.54 mutual coherent uniqueness.  No claim about their external labels is
needed for this mathematical statement. -/
theorem fixedRaw_hasMutualCoherentUniqueness
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {R :
      RawHigherContextualSystem.{u, v, uH, vH}
        (Context := Context)}
    (X Y :
      FixedRawExactUniversalClassificationObject
        (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) R) :
    Nonempty
      (ExactUniversalTargetMutualCoherentUniqueness
        (W := W) A X.presentation Y.presentation) := by
  exact
    hasMutualCoherentUniqueness_of_universalTargets
      (W := W) A X.universal Y.universal

/-- If two fixed-raw universal presentations carry the same external label,
package that label equality together with their mutual coherent uniqueness. -/
theorem fixedRaw_existsLabelPreservingMutualCoherentUniqueness
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {R :
      RawHigherContextualSystem.{u, v, uH, vH}
        (Context := Context)}
    (X Y :
      FixedRawExactUniversalClassificationObject
        (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) R)
    (hLabel : X.label = Y.label) :
    Nonempty
      (LabelPreservingMutualCoherentUniqueness
        (W := W) A X Y) := by
  rcases
      fixedRaw_hasMutualCoherentUniqueness
        (W := W) A X Y with
    ⟨hCoherent⟩
  exact
    ⟨{
      label_eq := hLabel
      coherent := hCoherent
    }⟩

/-! ## Transport across an explicit coherent raw equivalence -/

/-- Transport a fixed-raw exact-universal classification object along a
two-sided coherent raw equivalence.

The external label is preserved literally; v4.55 transports the exact
presentation and its coherent universal-target witness. -/
noncomputable def FixedRawExactUniversalClassificationObject.transport
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {R S :
      RawHigherContextualSystem.{u, v, uH, vH}
        (Context := Context)}
    (E : HigherRawSystemCoherentEquivalence R S)
    (X :
      FixedRawExactUniversalClassificationObject
        (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) R) :
    FixedRawExactUniversalClassificationObject
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) S where
  label := X.label
  presentation :=
    transportExactPresentation
      (W := W) A E X.presentation
  universal :=
    transportExactUniversalTarget
      (W := W) A E X.presentation X.universal

@[simp] theorem FixedRawExactUniversalClassificationObject.transport_label
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {R S :
      RawHigherContextualSystem.{u, v, uH, vH}
        (Context := Context)}
    (E : HigherRawSystemCoherentEquivalence R S)
    (X :
      FixedRawExactUniversalClassificationObject
        (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) R) :
    (X.transport (W := W) A E).label =
      X.label :=
  rfl

/-- v4.55 transport preserves the DO₂ carrier definitionally. -/
@[simp] theorem FixedRawExactUniversalClassificationObject.transport_carrier
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {R S :
      RawHigherContextualSystem.{u, v, uH, vH}
        (Context := Context)}
    (E : HigherRawSystemCoherentEquivalence R S)
    (X :
      FixedRawExactUniversalClassificationObject
        (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) R) :
    (X.transport (W := W) A E).presentation.carrier =
      X.presentation.carrier := by
  exact
    transportExactPresentation_carrier
      (W := W) A E X.presentation

/-- After transporting one universal classification presentation along an
explicit two-sided coherent raw equivalence, it is mutually coherently unique
with every universal classification presentation over the target raw system. -/
theorem transported_hasMutualCoherentUniqueness
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {R S :
      RawHigherContextualSystem.{u, v, uH, vH}
        (Context := Context)}
    (E : HigherRawSystemCoherentEquivalence R S)
    (X :
      FixedRawExactUniversalClassificationObject
        (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) R)
    (Y :
      FixedRawExactUniversalClassificationObject
        (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) S) :
    Nonempty
      (ExactUniversalTargetMutualCoherentUniqueness
        (W := W) A
        (X.transport (W := W) A E).presentation
        Y.presentation) := by
  exact
    fixedRaw_hasMutualCoherentUniqueness
      (W := W) A (X.transport (W := W) A E) Y

/-- Label-preserving version of transported coherent uniqueness.  The label of
the transported object is definitionally X.label, so an external equality
X.label = Y.label is exactly the extra datum required. -/
theorem transported_existsLabelPreservingMutualCoherentUniqueness
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {R S :
      RawHigherContextualSystem.{u, v, uH, vH}
        (Context := Context)}
    (E : HigherRawSystemCoherentEquivalence R S)
    (X :
      FixedRawExactUniversalClassificationObject
        (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) R)
    (Y :
      FixedRawExactUniversalClassificationObject
        (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) S)
    (hLabel : X.label = Y.label) :
    Nonempty
      (LabelPreservingMutualCoherentUniqueness
        (W := W) A
        (X.transport (W := W) A E) Y) := by
  apply
    fixedRaw_existsLabelPreservingMutualCoherentUniqueness
      (W := W) A
      (X.transport (W := W) A E) Y
  simpa using hLabel

/-!
## Boundary after v5.20

The coherent-uniqueness layer is now classification-ready at exactly the
already-proved strengths:

* fixed raw R:
    universal target Q₁ and universal target Q₂
      -> mutual coherent comparisons
      -> both roundtrips modification-isomorphic to identity;

* explicit coherent raw equivalence R <-> S:
    universal target over R
      -> transported universal target over S
      -> mutual coherent uniqueness with every universal target over S.

External labels remain independent data and are never erased by carrier or
presentation uniqueness.

Still not proved:

* a directed v5.19 pointwise-equivalence factor yields a two-sided coherent raw
  equivalence;
* ordinary v5.18 exact liftability yields v5.19 ambient alignment;
* arbitrary admissible raw morphisms carry a classification-level universal
  realization;
* the final mapping-space/classification equivalence.

The next theorem unit should therefore address one of the two actual remaining
bridges: universe-alignment/reindexing, or arbitrary-morphism functoriality of
the classification interface.  Neither should be hidden inside the uniqueness
theorem.
-/

end

end KUOS.DependentOriginationExactClassificationCoherentUniquenessV5_20
