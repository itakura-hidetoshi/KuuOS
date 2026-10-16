import KUOS.DependentOriginationLocalizedClassificationRealizationV5_24
import KUOS.DependentOriginationExactUniversalHomEquivalenceV4_83
import Mathlib.CategoryTheory.Functor.FullyFaithful
import Mathlib

namespace KUOS.DependentOriginationClassificationLocalHomEquivalenceV5_25

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackCarrierV2_9
open KUOS.DependentOriginationExactUniversalMappingMorphismV4_57
open KUOS.DependentOriginationExactUniversalMappingTwoCellV4_58
open KUOS.DependentOriginationExactUniversalMappingHomCategoryV4_60
open KUOS.DependentOriginationExactUniversalHomEquivalenceV4_83
open KUOS.DependentOriginationExactUniversalClassificationInterfaceV5_17
open KUOS.DependentOriginationExactClassificationMorphismInterfaceV5_21
open KUOS.DependentOriginationExactClassificationHomFunctorV5_22
open KUOS.DependentOriginationLocalizedClassificationRealizationV5_24

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Classification local hom equivalence v5.25

v5.24 packages exact-universal classification realization as a strict
pseudofunctor between genuine bicategories.  This theorem unit proves the
local part of the expected classification biequivalence: on every fixed pair
of exact-universal classification objects, realization induces an equivalence
of hom categories.

The mathematical input is exactly v4.83.  There, for the underlying
exact-universal source objects X.source and Y.source, the realization hom
functor

  ExactUniversalRawMorphism X.source Y.source
    -> (X.source.carrier ⟶ Y.source.carrier)

is an equivalence.

The classification wrappers add only proposition-valued external label
bookkeeping.  For a fixed pair X,Y, every localized classification 1-cell
already carries a proof X.label = Y.label.  The local preimage therefore
reuses that same proof and applies the v4.83 preimage to the underlying DO₂
map.  No object-level coverage assumption and no ambient-alignment converse
is needed.

In particular, this file proves only local equivalence.  It does not assert:

* essential surjectivity of the global strict realization on objects;
* ExactLiftabilityCriterion -> AmbientAlignedExactLiftabilityCriterion;
* weak admissibility -> exact liftability;
* final classification biequivalence.
-/

universe u v uH vH uW uP

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

/-! ## Local faithfulness -/

/-- Classification realization is faithful on every fixed hom category.

After wrapper extensionality, this is exactly the v4.83/v4.76 faithfulness of
the underlying exact-universal realization hom functor. -/
instance exactUniversalClassificationRealizationHomFunctor_faithful
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X Y :
      ExactUniversalClassificationObject
        (W := W) A WorldLabel PresentationLabel) :
    (exactUniversalClassificationRealizationHomFunctor
      (W := W) A X Y).Faithful where
  map_injective {f g} := by
    intro eta theta h
    apply ExactUniversalClassificationTwoCell.ext
    apply
      (exactUniversalCompletion2HomFunctor
        (W := W) A X.source Y.source).map_injective
    exact congrArg (fun z => z.cell) h

/-! ## Local fullness -/

/-- Classification realization is full on every fixed hom category.

A target classification 2-cell is only a wrapper around a DO₂ 2-cell.
v4.83 supplies its compatible exact-universal preimage; wrapping that preimage
gives the required classification 2-cell. -/
instance exactUniversalClassificationRealizationHomFunctor_full
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X Y :
      ExactUniversalClassificationObject
        (W := W) A WorldLabel PresentationLabel) :
    (exactUniversalClassificationRealizationHomFunctor
      (W := W) A X Y).Full where
  map_surjective {f g} eta := by
    rcases
      (exactUniversalCompletion2HomFunctor
        (W := W) A X.source Y.source).map_surjective eta.cell with
      ⟨theta, htheta⟩
    refine ⟨{ cell := theta }, ?_⟩
    apply LocalizedClassificationTwoCell.ext
    exact htheta

/-! ## Local essential surjectivity on 1-cells -/

/-- Every localized classification 1-cell between realized objects is in the
essential image of the classification realization hom functor.

The target 1-cell itself supplies the required label equality.  Its underlying
DO₂ map is lifted by v4.83's exactUniversalOneCellOfLift, whose realized map is
definitionally the original DO₂ map. -/
instance exactUniversalClassificationRealizationHomFunctor_essSurj
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X Y :
      ExactUniversalClassificationObject
        (W := W) A WorldLabel PresentationLabel) :
    (exactUniversalClassificationRealizationHomFunctor
      (W := W) A X Y).EssSurj where
  mem_essImage ell := by
    let f :
        ExactUniversalClassificationOneCell
          (W := W) A X Y :=
      { label_eq := ell.label_eq
        map :=
          exactUniversalOneCellOfLift
            (W := W) A X.source Y.source ell.map }
    refine ⟨f, ⟨?_⟩⟩
    change
      ExactUniversalClassificationOneCell.realize
          (W := W) A f ≅
        ell
    have h :
        ExactUniversalClassificationOneCell.realize
            (W := W) A f =
          ell := by
      cases ell
      rfl
    exact eqToIso h

/-! ## Native Mathlib equivalence interface -/

/-- The classification realization hom functor is a Mathlib equivalence on
every fixed pair of exact-universal classification objects. -/
instance exactUniversalClassificationRealizationHomFunctor_isEquivalence
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X Y :
      ExactUniversalClassificationObject
        (W := W) A WorldLabel PresentationLabel) :
    (exactUniversalClassificationRealizationHomFunctor
      (W := W) A X Y).IsEquivalence where
  essSurj :=
    exactUniversalClassificationRealizationHomFunctor_essSurj
      (W := W) A X Y

/-- Data-bearing fully faithful interface for the classification realization
hom functor. -/
def exactUniversalClassificationRealizationHomFullyFaithful
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X Y :
      ExactUniversalClassificationObject
        (W := W) A WorldLabel PresentationLabel) :
    (exactUniversalClassificationRealizationHomFunctor
      (W := W) A X Y).FullyFaithful :=
  Functor.FullyFaithful.ofFullyFaithful _

/-- The local classification realization equivalence.  Its forward functor is
literally the v5.22 classification realization hom functor. -/
noncomputable def exactUniversalClassificationRealizationHomEquivalence
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X Y :
      ExactUniversalClassificationObject
        (W := W) A WorldLabel PresentationLabel) :
    ExactUniversalClassificationOneCell
        (W := W) A X Y ≌
      LocalizedClassificationOneCell
        (W := W) A
        (X.realize (W := W) A)
        (Y.realize (W := W) A) :=
  (exactUniversalClassificationRealizationHomFunctor
    (W := W) A X Y).asEquivalence

@[simp] theorem exactUniversalClassificationRealizationHomEquivalence_functor
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X Y :
      ExactUniversalClassificationObject
        (W := W) A WorldLabel PresentationLabel) :
    (exactUniversalClassificationRealizationHomEquivalence
      (W := W) A X Y).functor =
      exactUniversalClassificationRealizationHomFunctor
        (W := W) A X Y :=
  rfl

/-! ## Regression checks -/

section Regression

variable
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X Y :
      ExactUniversalClassificationObject
        (W := W) A WorldLabel PresentationLabel)

example :
    (exactUniversalClassificationRealizationHomFunctor
      (W := W) A X Y).Faithful :=
  inferInstance

example :
    (exactUniversalClassificationRealizationHomFunctor
      (W := W) A X Y).Full :=
  inferInstance

example :
    (exactUniversalClassificationRealizationHomFunctor
      (W := W) A X Y).EssSurj :=
  inferInstance

example :
    (exactUniversalClassificationRealizationHomFunctor
      (W := W) A X Y).IsEquivalence :=
  inferInstance

example :
    ExactUniversalClassificationOneCell
        (W := W) A X Y ≌
      LocalizedClassificationOneCell
        (W := W) A
        (X.realize (W := W) A)
        (Y.realize (W := W) A) :=
  exactUniversalClassificationRealizationHomEquivalence
    (W := W) A X Y

end Regression

#print axioms exactUniversalClassificationRealizationHomFullyFaithful
#print axioms exactUniversalClassificationRealizationHomEquivalence

end

end KUOS.DependentOriginationClassificationLocalHomEquivalenceV5_25
