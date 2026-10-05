import KUOS.DependentOriginationExactLiftabilityCriterionV5_18
import KUOS.DependentOriginationExactUniversalAmbientCanonicalSourceV5_11
import KUOS.DependentOriginationPointwiseEquivalenceTransportV2_17
import Mathlib

namespace KUOS.DependentOriginationExactClassificationFactorExistenceV5_19

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackDescentV2_8
open KUOS.DependentOriginationHigherStackCarrierV2_9
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseEquivalenceTransportV2_17
open KUOS.DependentOriginationExactHigherPresentationSectorV4_50
open KUOS.DependentOriginationExactUniversalMappingMorphismV4_57
open KUOS.DependentOriginationExactUniversalAmbientRestrictionUniversalityV4_91
open KUOS.DependentOriginationExactUniversalAmbientCanonicalSourceV5_11
open KUOS.DependentOriginationExactUniversalClassificationInterfaceV5_17
open KUOS.DependentOriginationExactLiftabilityCriterionV5_18

set_option autoImplicit false

noncomputable section

/-!
# Exact classification factor existence v5.19

v5.18 identifies exact liftability with the existing stack-localization
factorization interface.  The next classification obligation is factor
existence.

A universe boundary has to be respected here.  The v4.50
`ExactHigherDependentOriginationPresentation.carrier` field was written
against the generated `DependentOriginationCompletion2` universe interface
without pinning its five generated universe arguments.  By contrast the ambient
v5.09-v5.16 theory deliberately fixes

  DO₂.{u, v, uH, uH, vH}.

Therefore this theorem unit does not project an arbitrary old presentation
carrier and feed it directly into the ambient canonical-source API.

Instead, from exact liftability we first recover the equivalent
`HigherStackLocalizationFactorization`.  Its localized lift already has the
raw system's exact `Cat.{vH,uH}` universes.  We then rebuild the ambient stack
carrier with an explicit type:

  Z : DO₂.{u, v, uH, uH, vH} := ⟨H.lift, H.isStack⟩.

The v5.11 canonical exact-universal source may now be applied to Z without any
unresolved universe metavariable.  Its raw system is definitionally the
restriction of H.lift, and H.comparison supplies the directed pointwise
equivalence

  source.raw = restrict(H.lift) --> X.raw.

Thus every exact-liftable classification object has a label-preserving
exact-universal factor with:

* an explicitly universe-pinned ambient DO₂ carrier;
* the same localized lift as its stack factorization;
* an exact-universal source realizing to that carrier;
* the original pointwise-equivalence comparison back to the raw system.

No inverse raw comparison and no coherent uniqueness between arbitrary factors
is asserted here.
-/

universe u v uH vH uW uP uE

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

/-- The ambient DO₂ universe used by the v5.09-v5.16 exact-universal theory. -/
abbrev ClassificationAmbient :=
  DependentOriginationCompletion2.{u, v, uH, uH, vH}
    (W := W) A

/-- Canonically choose the stack-localization factorization whose existence is
equivalent to an exact-liftable classification object.

This choice is made only after the raw target universes are fixed by `X.raw`. -/
noncomputable def exactLiftableChosenStackFactorization
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP, uE}
        (W := W) A WorldLabel PresentationLabel) :
    HigherStackLocalizationFactorization.{u, v, uH, vH}
      (W := W) A X.raw :=
  Classical.choice
    ((hasExactHigherDependentOriginationPresentation_iff_stackFactorization
      (W := W) A X.raw).1 X.exact)

/-- Rebuild the chosen stack-localization factorization as an explicitly
universe-pinned ambient DO₂ object. -/
noncomputable def exactLiftableClassificationAmbientCarrier
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP, uE}
        (W := W) A WorldLabel PresentationLabel) :
    ClassificationAmbient.{u, v, uH, vH} (W := W) A :=
  ⟨(exactLiftableChosenStackFactorization
      (W := W) A X).lift,
    (exactLiftableChosenStackFactorization
      (W := W) A X).isStack⟩

/-- The explicitly pinned carrier has exactly the localized lift chosen above. -/
@[simp] theorem exactLiftableClassificationAmbientCarrier_val
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP, uE}
        (W := W) A WorldLabel PresentationLabel) :
    higherStackObjectVal (W := W) A
        (exactLiftableClassificationAmbientCarrier
          (W := W) A X) =
      (exactLiftableChosenStackFactorization
        (W := W) A X).lift :=
  rfl

/-- Factor data from one exact-liftable classification object through an
exact-universal source. -/
structure ExactUniversalClassificationFactor
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP, uE}
        (W := W) A WorldLabel PresentationLabel) where
  /-- Stack-localization data at the raw system's fixed universes. -/
  factorization :
    HigherStackLocalizationFactorization.{u, v, uH, vH}
      (W := W) A X.raw
  /-- Explicitly universe-pinned ambient carrier. -/
  carrier :
    ClassificationAmbient.{u, v, uH, vH} (W := W) A
  /-- Forgetting the stack witness recovers exactly the selected localized lift. -/
  carrier_val :
    higherStackObjectVal (W := W) A carrier =
      factorization.lift
  /-- Labelled exact-universal source attached to the ambient carrier. -/
  source :
    ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel
  /-- External labels are preserved literally. -/
  label_eq :
    source.label = X.label
  /-- The exact-universal source realizes to exactly the pinned carrier. -/
  source_carrier_eq :
    source.source.carrier = carrier
  /-- Its raw restriction compares by pointwise equivalence to the original raw
  contextual system. -/
  comparison :
    HigherPointwiseEquivalenceComparison.{u, v, uH, vH}
      source.source.raw X.raw

/-- Canonical factor data attached to an exact-liftable classification object.

The construction fixes all universe data before any bicategorical hom or
typeclass search is requested. -/
noncomputable def exactUniversalClassificationFactor
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP, uE}
        (W := W) A WorldLabel PresentationLabel) :
    ExactUniversalClassificationFactor
      (W := W) A X := by
  let H :
      HigherStackLocalizationFactorization
        (W := W) A X.raw :=
    exactLiftableChosenStackFactorization
      (W := W) A X
  let Z :
      ClassificationAmbient.{u, v, uH, vH} (W := W) A :=
    ⟨H.lift, H.isStack⟩
  let S :
      ExactUniversalRawObject.{u, v, uH, vH}
        (W := W) A :=
    exactUniversalAmbientCanonicalSource.{u, v, uH, vH}
      (W := W) A Z
  refine
    { factorization := H
      carrier := Z
      carrier_val := ?_
      source :=
        { label := X.label
          source := S }
      label_eq := rfl
      source_carrier_eq := ?_
      comparison := ?_ }
  · rfl
  · change S.carrier = Z
    exact
      exactUniversalAmbientCanonicalSource_carrier.{u, v, uH, vH}
        (W := W) A Z
  · change
      HigherPointwiseEquivalenceComparison.{u, v, uH, vH}
        (restrictHigherLocalizedSystem W H.lift)
        X.raw
    exact
      { comparison := H.comparison
        comparison_isEquivalence := H.comparison_isEquivalence }

/-- The canonical factor preserves the external classification label. -/
@[simp] theorem exactUniversalClassificationFactor_label
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP, uE}
        (W := W) A WorldLabel PresentationLabel) :
    (exactUniversalClassificationFactor
      (W := W) A X).source.label =
      X.label :=
  rfl

/-- The canonical factor's ambient carrier has exactly the selected localized
lift. -/
@[simp] theorem exactUniversalClassificationFactor_carrier_val
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP, uE}
        (W := W) A WorldLabel PresentationLabel) :
    higherStackObjectVal (W := W) A
        (exactUniversalClassificationFactor
          (W := W) A X).carrier =
      (exactUniversalClassificationFactor
        (W := W) A X).factorization.lift := by
  exact
    (exactUniversalClassificationFactor
      (W := W) A X).carrier_val

/-- The exact-universal source of the canonical factor realizes to exactly the
explicitly pinned ambient carrier. -/
theorem exactUniversalClassificationFactor_source_carrier
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP, uE}
        (W := W) A WorldLabel PresentationLabel) :
    (exactUniversalClassificationFactor
      (W := W) A X).source.source.carrier =
      (exactUniversalClassificationFactor
        (W := W) A X).carrier := by
  exact
    (exactUniversalClassificationFactor
      (W := W) A X).source_carrier_eq

/-- Every exact-liftable classification object admits exact-universal factor
data. -/
theorem ExactLiftableClassificationObject.existsExactUniversalClassificationFactor
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP, uE}
        (W := W) A WorldLabel PresentationLabel) :
    Nonempty
      (ExactUniversalClassificationFactor
        (W := W) A X) :=
  ⟨exactUniversalClassificationFactor
    (W := W) A X⟩

/-- Every exact-liftable classification object therefore admits a
label-preserving exact-universal source whose raw restriction is related to the
original raw system by the already-stored directed pointwise equivalence. -/
theorem ExactLiftableClassificationObject.exists_labelPreserving_exactUniversalSource
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP, uE}
        (W := W) A WorldLabel PresentationLabel) :
    ∃ Y :
        ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
          (W := W) A WorldLabel PresentationLabel,
      Y.label = X.label ∧
        Nonempty
          (HigherPointwiseEquivalenceComparison.{u, v, uH, vH}
            Y.source.raw X.raw) := by
  rcases
      ExactLiftableClassificationObject.existsExactUniversalClassificationFactor
        (W := W) A X with
    ⟨F⟩
  exact
    ⟨F.source, F.label_eq, ⟨F.comparison⟩⟩

/-- The same factor-existence result starts from a weak semantic object once an
explicit v5.18 exact-liftability criterion witness is supplied.

No implication from weak admissibility alone is used. -/
theorem WeakSemanticClassificationObject.exists_labelPreserving_exactUniversalSource_ofCriterion
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      WeakSemanticClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) WorldLabel PresentationLabel)
    (hCriterion :
      ExactLiftabilityCriterion (W := W) A X.raw) :
    ∃ Y :
        ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
          (W := W) A WorldLabel PresentationLabel,
      Y.label = X.label ∧
        Nonempty
          (HigherPointwiseEquivalenceComparison.{u, v, uH, vH}
            Y.source.raw X.raw) := by
  let XExact :=
    weakSemanticClassificationObjectToExactLiftableOfCriterion
      (W := W) A X hCriterion
  exact
    ExactLiftableClassificationObject.exists_labelPreserving_exactUniversalSource
      (W := W) A XExact

/-!
## Boundary after v5.19

Factor existence is now explicit without crossing the universe boundary of the
old v4.50 presentation carrier:

  exact-liftable X
      -> chosen stack-localization factorization H
      -> Z : DO₂.{u,v,uH,uH,vH} := ⟨H.lift, H.isStack⟩
      -> canonical exact-universal source S(Z)
      -> directed pointwise-equivalence comparison
           S(Z).raw = restrict(H.lift) --> X.raw.

The source preserves the external label and realizes to exactly the explicitly
pinned carrier.

This does not yet prove coherent uniqueness of arbitrary factors.  The v5.19
comparison is directed; it does not contain an inverse StrongTrans or
unit/counit modifications.  Therefore it must not be silently upgraded to the
v4.55 `HigherRawSystemCoherentEquivalence` interface.

The next theorem unit should separate:

1. fixed-raw coherent uniqueness, already theorem-backed by v4.54 for two
   coherent universal targets; and
2. transport of that uniqueness across raw systems only when an explicit
   two-sided coherent raw equivalence is supplied, as in v4.55.

The countermodel boundary from v5.18 remains unchanged: weak admissibility
alone does not produce the exact criterion required here.
-/

end

end KUOS.DependentOriginationExactClassificationFactorExistenceV5_19
