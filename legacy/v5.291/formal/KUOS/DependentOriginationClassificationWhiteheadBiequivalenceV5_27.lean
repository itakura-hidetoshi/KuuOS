import KUOS.DependentOriginationClassificationLocalHomEquivalenceV5_25
import KUOS.DependentOriginationClassificationObjectCoverageV5_26
import KUOS.DependentOriginationExactUniversalLabelledBiequivalenceV4_89
import Mathlib.CategoryTheory.Bicategory.Adjunction.Basic
import Mathlib

namespace KUOS.DependentOriginationClassificationWhiteheadBiequivalenceV5_27

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackCarrierV2_9
open KUOS.DependentOriginationExactUniversalClassificationInterfaceV5_17
open KUOS.DependentOriginationExactClassificationMorphismInterfaceV5_21
open KUOS.DependentOriginationExactClassificationHomFunctorV5_22
open KUOS.DependentOriginationLocalizedClassificationRealizationV5_24
open KUOS.DependentOriginationClassificationLocalHomEquivalenceV5_25
open KUOS.DependentOriginationClassificationObjectCoverageV5_26
open KUOS.DependentOriginationExactUniversalLabelledBiequivalenceV4_89

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory
open scoped Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Classification Whitehead biequivalence certificate v5.27

v5.25 proves local equivalence of hom categories for exact-universal
classification realization.  v5.26 proves essential surjectivity on localized
classification objects up to bicategorical equivalence.

This theorem unit combines exactly those two independent results into the
minimal Whitehead-style certificate already used in v4.89:

* the global classification realization pseudofunctor;
* an equivalence on every fixed hom category;
* literal agreement of the forward functor of each local equivalence with the
  hom functor induced by global realization;
* essential surjectivity on localized classification objects up to
  bicategorical equivalence.

No explicit classification quasi-inverse pseudofunctor, global unit/counit
StrongTrans, or triangle modifications are asserted here.  Those are separate
higher-coherence obligations.

The v5.19 boundary is also unchanged: this certificate concerns objects already
inside the two classification bicategories.  It does not prove the converse

  ExactLiftabilityCriterion
    -> AmbientAlignedExactLiftabilityCriterion

for arbitrary raw/exact-liftable systems.
-/

universe u v uH vH uW uP

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable
  (A :
    RefinementAtlas.{u, max u v, uH}
      (LocalizedContext W))

abbrev ClassificationSource
    (WorldLabel : Type uW)
    (PresentationLabel : Type uP) :=
  ExactUniversalClassificationObject
    (W := W) A WorldLabel PresentationLabel

abbrev ClassificationTarget
    (WorldLabel : Type uW)
    (PresentationLabel : Type uP) :=
  LocalizedClassificationObject
    (W := W) A WorldLabel PresentationLabel

/-! ## Exact agreement of the local and global forward functors -/

/-- The forward functor of the v5.25 local equivalence is exactly the hom
functor induced by the global v5.24 strict classification realization.

The proof deliberately uses functor extensionality rather than relying on a
large reducibility step through the strict-pseudofunctor wrapper. -/
theorem exactUniversalClassificationRealizationHomEquivalence_forward
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X Y :
      ClassificationSource
        (W := W) A WorldLabel PresentationLabel) :
    (exactUniversalClassificationRealizationHomEquivalence
      (W := W) A X Y).functor =
      ((exactUniversalClassificationRealization
        (W := W) A).toPseudofunctor).mapFunctor X Y := by
  apply CategoryTheory.Functor.hext
  · intro f
    rfl
  · intro f g eta
    exact heq_of_eq rfl

/-! ## Whitehead certificate -/

/-- Whitehead-style biequivalence data for the full labelled classification
realization.

This is the direct classification analogue of v4.89, but its target is the
entire localized classification bicategory rather than only the old
object-labelled realized sector. -/
noncomputable def exactUniversalClassificationWhiteheadBiequivalence
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP} :
    WhiteheadBiequivalenceData
      (ClassificationSource
        (W := W) A WorldLabel PresentationLabel)
      (ClassificationTarget
        (W := W) A WorldLabel PresentationLabel) where
  forward :=
    (exactUniversalClassificationRealization
      (W := W) A).toPseudofunctor
  homEquiv X Y :=
    exactUniversalClassificationRealizationHomEquivalence
      (W := W) A X Y
  homEquiv_functor X Y :=
    exactUniversalClassificationRealizationHomEquivalence_forward
      (W := W) A X Y
  object_essentially_surjective Z :=
    exactUniversalClassificationRealization_object_essentially_surjective
      (W := W) A Z

/-! ## Projection theorems -/

@[simp] theorem exactUniversalClassificationWhiteheadBiequivalence_forward
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP} :
    (exactUniversalClassificationWhiteheadBiequivalence
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).forward =
      (exactUniversalClassificationRealization
        (W := W) A).toPseudofunctor :=
  rfl

theorem exactUniversalClassificationWhiteheadBiequivalence_homEquiv
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X Y :
      ClassificationSource
        (W := W) A WorldLabel PresentationLabel) :
    (exactUniversalClassificationWhiteheadBiequivalence
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).homEquiv X Y =
      exactUniversalClassificationRealizationHomEquivalence
        (W := W) A X Y :=
  rfl

theorem exactUniversalClassificationWhiteheadBiequivalence_object_essentially_surjective
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (Z :
      ClassificationTarget
        (W := W) A WorldLabel PresentationLabel) :
    ∃ X :
        ClassificationSource
          (W := W) A WorldLabel PresentationLabel,
      Nonempty
        (Bicategory.Equivalence
          ((exactUniversalClassificationWhiteheadBiequivalence
            (W := W) A
            (WorldLabel := WorldLabel)
            (PresentationLabel := PresentationLabel)).forward.obj X)
          Z) :=
  (exactUniversalClassificationWhiteheadBiequivalence
    (W := W) A
    (WorldLabel := WorldLabel)
    (PresentationLabel := PresentationLabel)).object_essentially_surjective Z

/-!
## Boundary after v5.27

The classification realization now has a formal Whitehead-style
biequivalence certificate:

  ExactUniversalClassification
      -- realization -->
  LocalizedClassification

with local hom equivalences and target-object coverage.

This is stronger than v5.25 or v5.26 separately, but it is intentionally not
yet the explicit quasi-inverse/unit/counit package of v5.15.  The next theorem
unit may construct a label-preserving classification quasi-inverse from the
ambient canonical section and then lift the ambient roundtrip unit/counit to
classification wrappers.

No claim is made here about weak semantic objects, arbitrary exact-liftable raw
systems, or the missing universe-alignment converse from v5.19.
-/

/-! ## Regression checks -/

section Regression

variable
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X Y :
      ClassificationSource
        (W := W) A WorldLabel PresentationLabel)
    (Z :
      ClassificationTarget
        (W := W) A WorldLabel PresentationLabel)

example :
    CategoryTheory.Equivalence
      (X ⟶ Y)
      (((exactUniversalClassificationRealization
        (W := W) A).toPseudofunctor).obj X ⟶
       ((exactUniversalClassificationRealization
        (W := W) A).toPseudofunctor).obj Y) :=
  (exactUniversalClassificationWhiteheadBiequivalence
    (W := W) A
    (WorldLabel := WorldLabel)
    (PresentationLabel := PresentationLabel)).homEquiv X Y

example :
    ∃ X :
        ClassificationSource
          (W := W) A WorldLabel PresentationLabel,
      Nonempty
        (Bicategory.Equivalence
          ((exactUniversalClassificationRealization
            (W := W) A).obj X)
          Z) :=
  exactUniversalClassificationRealization_object_essentially_surjective
    (W := W) A Z

end Regression

#print axioms exactUniversalClassificationRealizationHomEquivalence_forward
#print axioms exactUniversalClassificationWhiteheadBiequivalence
#print axioms exactUniversalClassificationWhiteheadBiequivalence_object_essentially_surjective

end

end KUOS.DependentOriginationClassificationWhiteheadBiequivalenceV5_27
