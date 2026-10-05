import KUOS.DependentOriginationLocalizedClassificationRealizationV5_24
import KUOS.DependentOriginationExactUniversalAmbientBiequivalenceCertificateV5_15
import Mathlib.CategoryTheory.Bicategory.Adjunction.Basic
import Mathlib

namespace KUOS.DependentOriginationClassificationObjectCoverageV5_26

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackCarrierV2_9
open KUOS.DependentOriginationExactUniversalClassificationInterfaceV5_17
open KUOS.DependentOriginationExactClassificationMorphismInterfaceV5_21
open KUOS.DependentOriginationExactClassificationHomFunctorV5_22
open KUOS.DependentOriginationLocalizedClassificationRealizationV5_24
open KUOS.DependentOriginationExactUniversalAmbientBiequivalenceCertificateV5_15

open scoped CategoryTheory.Bicategory
open scoped Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Classification object coverage v5.26

v5.25 proves that exact-universal classification realization is an equivalence
on every fixed hom category.  This theorem unit isolates the independent
object-level statement.

A crucial distinction is that a localized classification object already
contains an ambient DO₂ carrier.  Therefore object coverage of the
classification realization does **not** require constructing an ambient carrier
from an arbitrary raw or exact-liftable system.

Instead we apply the already established v5.15 ambient object coverage directly
to the stored carrier:

  Z : LocalizedClassificationObject
      -> Z.carrier : DO₂
      -> S : ExactUniversalRawObject
      -> S.carrier ≃ Z.carrier.

The new exact-universal classification object is simply S equipped with the
same external label as Z.

This does not prove, use, or hide the converse

  ExactLiftabilityCriterion R
    -> AmbientAlignedExactLiftabilityCriterion R.

That v5.19 universe-alignment boundary remains intact.  The present theorem is
only coverage of objects that are already in the localized classification
bicategory.
-/

universe u v uH vH uW uP

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable\n  (A :\n    RefinementAtlas.{u, max u v, uH}\n      (LocalizedContext W))

/-! ## Lift an underlying DO₂ equivalence through the label wrapper -/

/-- An underlying DO₂ adjoint equivalence lifts to an adjoint equivalence of
localized classification objects once their external labels are identified.

The label proof is used only in the two wrapped 1-cells.  Unit and counit are
the underlying DO₂ unit and counit wrapped by v5.24's native 2-cell wrapper. -/
noncomputable def localizedClassificationEquivalenceOfUnderlying
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y :
      LocalizedClassificationObject
        (W := W) A WorldLabel PresentationLabel}
    (hlabel : X.label = Y.label)
    (e : Bicategory.Equivalence X.carrier Y.carrier) :
    Bicategory.Equivalence X Y := by
  let f :
      LocalizedClassificationOneCell
        (W := W) A X Y :=
    { label_eq := hlabel
      map := e.hom }
  let g :
      LocalizedClassificationOneCell
        (W := W) A Y X :=
    { label_eq := hlabel.symm
      map := e.inv }

  have unit :
      𝟙 X ≅ f ≫ g := by
    exact
      LocalizedClassificationTwoCell.isoOfUnderlying
        (W := W) A e.unit

  have counit :
      g ≫ f ≅ 𝟙 Y := by
    exact
      LocalizedClassificationTwoCell.isoOfUnderlying
        (W := W) A e.counit

  exact
    Bicategory.Equivalence.mkOfAdjointifyCounit
      unit counit

/-! ## Classification object essential surjectivity -/

/-- Every localized classification object is bicategorically equivalent to the
realization of an exact-universal classification object with the **same
external label**.

This is v5.15 ambient object coverage applied directly to the target object's
stored DO₂ carrier.  No raw-system ambient-alignment hypothesis is involved. -/
theorem exactUniversalClassificationRealization_object_essentially_surjective
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (Z :
      LocalizedClassificationObject
        (W := W) A WorldLabel PresentationLabel) :
    ∃ X :
        ExactUniversalClassificationObject
          (W := W) A WorldLabel PresentationLabel,
      Nonempty
        (Bicategory.Equivalence
          ((exactUniversalClassificationRealization
            (W := W) A).obj X)
          Z) := by
  rcases
      exactUniversalAmbientBiequivalenceCertificate_object_essentially_surjective
        (W := W) A Z.carrier with
    ⟨S, ⟨e⟩⟩
  let X :
      ExactUniversalClassificationObject
        (W := W) A WorldLabel PresentationLabel :=
    { label := Z.label
      source := S }
  refine ⟨X, ⟨?_⟩⟩
  exact
    localizedClassificationEquivalenceOfUnderlying
      (W := W) A
      (X := (exactUniversalClassificationRealization (W := W) A).obj X)
      (Y := Z)
      rfl e

/-- The covering source can be chosen with label literally equal to the target
label. -/
theorem exists_exactUniversalClassificationObject_sameLabel_equivalent
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (Z :
      LocalizedClassificationObject
        (W := W) A WorldLabel PresentationLabel) :
    ∃ X :
        ExactUniversalClassificationObject
          (W := W) A WorldLabel PresentationLabel,
      X.label = Z.label ∧
        Nonempty
          (Bicategory.Equivalence
            ((exactUniversalClassificationRealization
              (W := W) A).obj X)
            Z) := by
  rcases
      exactUniversalAmbientBiequivalenceCertificate_object_essentially_surjective
        (W := W) A Z.carrier with
    ⟨S, ⟨e⟩⟩
  let X :
      ExactUniversalClassificationObject
        (W := W) A WorldLabel PresentationLabel :=
    { label := Z.label
      source := S }
  refine ⟨X, rfl, ⟨?_⟩⟩
  exact
    localizedClassificationEquivalenceOfUnderlying
      (W := W) A
      (X := (exactUniversalClassificationRealization (W := W) A).obj X)
      (Y := Z)
      rfl e

/-!
## Boundary after v5.26

For the classification bicategories themselves we now have:

* v5.25: local hom-category equivalence;
* v5.26: object essential surjectivity up to bicategorical equivalence.

The v5.19 ambient-alignment criterion remains relevant for a different
question: entering the ambient DO₂/classification layer from an arbitrary raw
or exact-liftable system.  It is not an obstruction once the target object is
already a LocalizedClassificationObject.

The next theorem unit can therefore combine v5.25 and v5.26 into a
Whitehead-style classification biequivalence certificate, without asserting
the missing exact-liftability-to-ambient-alignment converse.
-/

/-! ## Regression checks -/

section Regression

variable
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y :
      LocalizedClassificationObject
        (W := W) A WorldLabel PresentationLabel}

example
    (hlabel : X.label = Y.label)
    (e : Bicategory.Equivalence X.carrier Y.carrier) :
    Bicategory.Equivalence X Y :=
  localizedClassificationEquivalenceOfUnderlying
    (W := W) A hlabel e

example
    (Z :
      LocalizedClassificationObject
        (W := W) A WorldLabel PresentationLabel) :
    ∃ X :
        ExactUniversalClassificationObject
          (W := W) A WorldLabel PresentationLabel,
      Nonempty
        (Bicategory.Equivalence
          ((exactUniversalClassificationRealization
            (W := W) A).obj X)
          Z) :=
  exactUniversalClassificationRealization_object_essentially_surjective
    (W := W) A Z

end Regression

#print axioms localizedClassificationEquivalenceOfUnderlying
#print axioms exactUniversalClassificationRealization_object_essentially_surjective
#print axioms exists_exactUniversalClassificationObject_sameLabel_equivalent

end

end KUOS.DependentOriginationClassificationObjectCoverageV5_26
