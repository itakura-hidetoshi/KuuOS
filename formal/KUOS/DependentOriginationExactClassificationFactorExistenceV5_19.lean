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
# Exact classification factor existence v5.19

v5.18 identifies exact liftability with stack-localization factorization.
The next classification obligation is factor existence.

There is a genuine universe boundary inherited from the already-proved ambient
theory.  In v5.11 the canonical ambient source is developed with four declared
universes `u v uH vH`; consequently the refinement-atlas index universe in
that theorem family is the same `uH` used for the object universe of
`Cat.{vH,uH}`.

Accordingly this theorem unit states that boundary explicitly:

  A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W).

No theorem for an independently larger atlas-index universe is manufactured.

For an exact-liftable classification object X, v4.50/v5.18 supplies a
stack-localization factorization

  H : HigherStackLocalizationFactorization W A X.raw.

Its localized lift has the already-fixed `Cat.{vH,uH}` universe.  Repackage it
as the ambient object

  Z : DO₂.{u,v,uH,uH,vH} := ⟨H.lift, H.isStack⟩.

v5.11 then gives a canonical exact-universal source over Z.  Its raw system is
definitionally the restriction of H.lift, while H.comparison is a directed
pointwise equivalence

  restrict(H.lift) --> X.raw.

Thus factor existence preserves the external classification label and the
chosen ambient carrier exactly, while retaining the precise directed
pointwise-equivalence relation to the original raw system.

No inverse raw comparison, raw equality, or arbitrary-factor coherent
uniqueness is asserted.
-/

universe u v uH vH uW uP

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- v5.11's ambient theorem family identifies the atlas-index universe with
`uH`.  v5.19 keeps exactly that existing theorem boundary. -/
variable
  (A :
    RefinementAtlas.{u, max u v, uH}
      (LocalizedContext W))

/-- The ambient DO₂ object type used by the canonical v5.11 source. -/
abbrev ClassificationAmbient :=
  DependentOriginationCompletion2.{u, v, uH, uH, vH}
    (W := W) A

/-- Build the ambient DO₂ object carried by one stack-localization
factorization.  The target and atlas universes are already fixed in the
signature, before elaboration of the subtype constructor begins. -/
def ambientCarrierOfStackFactorization
    {R :
      RawHigherContextualSystem.{u, v, uH, vH}
        (Context := Context)}
    (H :
      HigherStackLocalizationFactorization
        (W := W) A R) :
    ClassificationAmbient.{u, v, uH, vH}
      (W := W) A :=
  ⟨H.lift, H.isStack⟩

@[simp] theorem ambientCarrierOfStackFactorization_val
    {R :
      RawHigherContextualSystem.{u, v, uH, vH}
        (Context := Context)}
    (H :
      HigherStackLocalizationFactorization
        (W := W) A R) :
    higherStackObjectVal (W := W) A
        (ambientCarrierOfStackFactorization
          (W := W) A H) =
      H.lift :=
  rfl

/-- Core factor-existence theorem.

Every exact-liftable classification object has a label-preserving
exact-universal source whose raw restriction compares pointwise-equivalently to
the original raw system. -/
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
  have hStack :
      HasHigherStackLocalizationFactorization
        (W := W) A X.raw :=
    (hasExactHigherDependentOriginationPresentation_iff_stackFactorization
      (W := W) A X.raw).1 X.exact
  rcases hStack with ⟨H⟩
  let Z :
      ClassificationAmbient.{u, v, uH, vH}
        (W := W) A :=
    ambientCarrierOfStackFactorization
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

/-- The same factor-existence theorem starts from a weak semantic object once
an explicit v5.18 exact-liftability criterion witness is supplied.

The proof consumes the criterion itself; weak admissibility alone is never used
to manufacture an exact factor. -/
theorem WeakSemanticClassificationObject.exists_labelPreserving_exactUniversalSource_ofCriterion
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      WeakSemanticClassificationObject
        (W := W) WorldLabel PresentationLabel)
    (hCriterion :
      ExactLiftabilityCriterion
        (W := W) A X.raw) :
    ∃ Y :
        ExactUniversalClassificationObject
          (W := W) A WorldLabel PresentationLabel,
      Y.label = X.label ∧
        Nonempty
          (HigherPointwiseEquivalenceComparison
            Y.source.raw X.raw) := by
  rcases hCriterion with ⟨H, hStack⟩
  let HS :
      HigherStackLocalizationFactorization
        (W := W) A X.raw :=
    { toHigherLocalizationFactorization := H
      isStack := hStack }
  let Z :
      ClassificationAmbient.{u, v, uH, vH}
        (W := W) A :=
    ambientCarrierOfStackFactorization
      (W := W) A HS
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

At the exact universe boundary already used by v5.11:

  exact-liftable X
      -> stack-localization factorization H
      -> Z : DO₂.{u,v,uH,uH,vH}
      -> canonical exact-universal source S(Z)
      -> directed pointwise-equivalence
           S(Z).raw = restrict(H.lift) --> X.raw.

The external label is preserved literally.

Two boundaries remain explicit.

1. The current canonical ambient source theorem identifies the atlas-index
   universe with `uH`.  Generalizing that ambient package to an independent
   atlas universe is a separate theorem-engineering task, not part of v5.19.

2. The comparison above is directed.  It does not contain the inverse
   StrongTrans and unit/counit modifications required by v4.55's
   `HigherRawSystemCoherentEquivalence`.  Hence it cannot be silently upgraded
   to two-sided coherent equivalence.

The next coherent-uniqueness theorem should therefore use v4.54 for universal
targets over the same raw system, and v4.55 only when an explicit two-sided
coherent raw equivalence is supplied.
-/

end

end KUOS.DependentOriginationExactClassificationFactorExistenceV5_19
