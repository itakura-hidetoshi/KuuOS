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
open KUOS.DependentOriginationExactUniversalAmbientCanonicalSourceV5_11
open KUOS.DependentOriginationExactUniversalClassificationInterfaceV5_17
open KUOS.DependentOriginationExactLiftabilityCriterionV5_18

set_option autoImplicit false

noncomputable section

/-!
# Ambient-aligned classification factor existence v5.19

v5.18 identifies exact presentation existence with a higher localization
factorization plus stack descent.  A fresh universe audit shows that this does
not yet imply the universe alignment required by the v5.11 ambient canonical
source.

The distinction is visible in the native v2.10 type.  A stack localization
factorization has separate universe parameters for:

* the refinement-atlas index family;
* the objects of the localized Cat-valued lift;
* the morphisms of the localized Cat-valued lift.

Thus an exact-liftability witness for a raw system in
`Cat.{vH,uH}` may have a localized lift in `Cat.{vLift,uLift}`.
Nothing in v4.50/v5.18 identifies those universe levels.

By contrast, the existing v5.11 canonical ambient source is instantiated at

  DO₂.{u,v,uH,uH,vH},

so its atlas-index universe and localized Cat object universe are both `uH`.

The correct next criterion is therefore an explicitly ambient-aligned
stack-localization factorization.  Under that criterion, factor existence is
straightforward and theorem-backed:

  aligned stack factorization H
      -> Z := ⟨H.lift, H.isStack⟩ in DO₂.{u,v,uH,uH,vH}
      -> canonical exact-universal source S(Z)
      -> H.comparison : S(Z).raw --> R

with pointwise-equivalence components.

This file deliberately does not assert that ordinary v5.18 exact liftability
implies ambient alignment.  Proving such a universe-alignment/reindexing theorem
would be a separate theorem unit.
-/

universe u v uH vH uW uP

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-
The v5.11 theorem family uses the same universe `uH` for atlas indices and
localized Cat objects.  This is a theorem boundary, not a cosmetic annotation.
-/
variable
  (A :
    RefinementAtlas.{u, max u v, uH}
      (LocalizedContext W))

/-- Existence of a stack-localization factorization already living in the
universe used by the v5.11 ambient completion. -/
def AmbientAlignedExactLiftabilityCriterion
    (R :
      RawHigherContextualSystem.{u, v, uH, vH}
        (Context := Context)) : Prop :=
  Nonempty
    (HigherStackLocalizationFactorization.{u, v, uH, uH, vH}
      (W := W) A R)

/-- Ambient alignment is stronger than the v5.18 exact-liftability criterion:
forget the universe alignment, retain the ordinary higher factorization and its
stack witness. -/
theorem ambientAlignedExactLiftabilityCriterion_implies_exactLiftabilityCriterion
    (R :
      RawHigherContextualSystem.{u, v, uH, vH}
        (Context := Context))
    (hAligned :
      AmbientAlignedExactLiftabilityCriterion
        (W := W) A R) :
    ExactLiftabilityCriterion
      (W := W) A R := by
  rcases hAligned with ⟨H⟩
  exact
    ⟨H.toHigherLocalizationFactorization, H.isStack⟩

/-- The explicitly aligned stack factorization determines an object of the
ambient completion used by v5.11. -/
def ambientCarrierOfAlignedStackFactorization
    {R :
      RawHigherContextualSystem.{u, v, uH, vH}
        (Context := Context)}
    (H :
      HigherStackLocalizationFactorization.{u, v, uH, uH, vH}
        (W := W) A R) :
    DependentOriginationCompletion2.{u, v, uH, uH, vH}
      (W := W) A :=
  ⟨H.lift, H.isStack⟩

@[simp] theorem ambientCarrierOfAlignedStackFactorization_val
    {R :
      RawHigherContextualSystem.{u, v, uH, vH}
        (Context := Context)}
    (H :
      HigherStackLocalizationFactorization.{u, v, uH, uH, vH}
        (W := W) A R) :
    higherStackObjectVal (W := W) A
        (ambientCarrierOfAlignedStackFactorization
          (W := W) A H) =
      H.lift :=
  rfl

/-- Core v5.19 factor-existence theorem.

An exact-liftable classification object enters the v5.11 exact-universal
ambient source once an ambient-aligned witness is supplied.  The external label
is preserved literally and the raw system is related to the canonical source
by the original directed pointwise-equivalence comparison. -/
theorem ExactLiftableClassificationObject.exists_labelPreserving_exactUniversalSource_of_ambientAligned
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      ExactLiftableClassificationObject
        (W := W) A WorldLabel PresentationLabel)
    (hAligned :
      AmbientAlignedExactLiftabilityCriterion
        (W := W) A X.raw) :
    ∃ Y :
        ExactUniversalClassificationObject
          (W := W) A WorldLabel PresentationLabel,
      Y.label = X.label ∧
        Nonempty
          (HigherPointwiseEquivalenceComparison
            Y.source.raw X.raw) := by
  rcases hAligned with ⟨H⟩
  let Z :
      DependentOriginationCompletion2.{u, v, uH, uH, vH}
        (W := W) A :=
    ambientCarrierOfAlignedStackFactorization
      (W := W) A H
  let S :
      ExactUniversalRawObject.{u, v, uH, vH}
        (W := W) A :=
    exactUniversalAmbientCanonicalSource
      (W := W) A Z
  refine
    ⟨{ label := X.label
       source := S },
      rfl,
      ?_⟩
  refine ⟨?_⟩
  change
    HigherPointwiseEquivalenceComparison
      (restrictHigherLocalizedSystem W H.lift)
      X.raw
  exact
    { comparison := H.comparison
      comparison_isEquivalence := H.comparison_isEquivalence }

/-- The factor-existence theorem can also start at the weak semantic layer,
provided the stronger ambient-aligned criterion is supplied explicitly.

The criterion itself implies the v5.18 exact-liftability criterion; weak
admissibility alone remains insufficient. -/
theorem WeakSemanticClassificationObject.exists_labelPreserving_exactUniversalSource_of_ambientAligned
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      WeakSemanticClassificationObject
        (W := W) WorldLabel PresentationLabel)
    (hAligned :
      AmbientAlignedExactLiftabilityCriterion
        (W := W) A X.raw) :
    ∃ Y :
        ExactUniversalClassificationObject
          (W := W) A WorldLabel PresentationLabel,
      Y.label = X.label ∧
        Nonempty
          (HigherPointwiseEquivalenceComparison
            Y.source.raw X.raw) := by
  rcases hAligned with ⟨H⟩
  let Z :
      DependentOriginationCompletion2.{u, v, uH, uH, vH}
        (W := W) A :=
    ambientCarrierOfAlignedStackFactorization
      (W := W) A H
  let S :
      ExactUniversalRawObject.{u, v, uH, vH}
        (W := W) A :=
    exactUniversalAmbientCanonicalSource
      (W := W) A Z
  refine
    ⟨{ label := X.label
       source := S },
      rfl,
      ?_⟩
  refine ⟨?_⟩
  change
    HigherPointwiseEquivalenceComparison
      (restrictHigherLocalizedSystem W H.lift)
      X.raw
  exact
    { comparison := H.comparison
      comparison_isEquivalence := H.comparison_isEquivalence }

/-!
## Boundary after v5.19

The factor-existence boundary is now explicit:

  AmbientAlignedExactLiftabilityCriterion R
      -> ExactLiftabilityCriterion R
      -> IsHigherWAdmissible W R,

and, at the aligned level,

  aligned stack factorization H
      -> Z in DO₂.{u,v,uH,uH,vH}
      -> canonical exact-universal source S(Z)
      -> directed pointwise equivalence S(Z).raw --> R.

What is not proved is the converse

  ExactLiftabilityCriterion R
      -> AmbientAlignedExactLiftabilityCriterion R.

That missing arrow is a genuine universe-alignment/reindexing obligation.  It
must not be hidden by implicit universe inference.

Likewise the factor comparison is directed; it does not supply the inverse
StrongTrans and unit/counit modifications required by v4.55's
`HigherRawSystemCoherentEquivalence`.

The next theorem unit can therefore separate two independent obligations:

1. universe-alignment/reindexing, if the final classification theorem must start
   from all v5.18 exact-liftable objects; and
2. coherent uniqueness, using v4.54 on fixed-raw universal targets and v4.55
   only under explicit two-sided coherent raw equivalence.
-/

end

end KUOS.DependentOriginationExactClassificationFactorExistenceV5_19
