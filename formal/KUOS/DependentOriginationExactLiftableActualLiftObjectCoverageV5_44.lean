import KUOS.DependentOriginationExactLiftableActualLiftLocalHomEquivalenceV5_43
import KUOS.DependentOriginationExactUniversalSourceEquivalenceV4_78
import Mathlib.CategoryTheory.Bicategory.Adjunction.Basic

namespace KUOS.DependentOriginationExactLiftableActualLiftObjectCoverageV5_44

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseEquivalenceTransportV2_17
open KUOS.DependentOriginationExactUniversalTargetNaturalityV4_55
open KUOS.DependentOriginationExactUniversalMappingMorphismV4_57
open KUOS.DependentOriginationExactUniversalMappingBicategoryV4_69
open KUOS.DependentOriginationExactUniversalSourceEquivalenceV4_78
open KUOS.DependentOriginationExactUniversalClassificationInterfaceV5_17
open KUOS.DependentOriginationExactClassificationMorphismInterfaceV5_21
open KUOS.DependentOriginationExactClassificationHomFunctorV5_22
open KUOS.DependentOriginationExactClassificationBicategoryV5_23
open KUOS.DependentOriginationExactLiftableActualLiftOneCellV5_40
open KUOS.DependentOriginationExactLiftableActualLiftStrictPseudofunctorV5_42

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Label-preserving object coverage of the actual-lift projection v5.44

v5.43 proves that the native v5.41 actual-lift hom functor is an equivalence.
This file treats the independent object-level question for the v5.42 global
strict pseudofunctor F.

For an exact-universal classification object Y, take X := Y.toExactLiftable.
The canonical exact-universal representative of X has exactly Y.source.raw
and Y.label.  The identity coherent raw equivalence and v4.78 therefore give
an adjoint equivalence of the underlying exact-universal source objects.
Wrapping its legs with the explicit label equality gives

  F.obj (Y.toExactLiftable) equivalent to Y.

The unit and counit are actual invertible classification 2-cells.  Mathlib's
adjointification supplies the triangle laws, keeping both wrapped 1-cell legs.
The resulting counit is not asserted to equal the initially wrapped counit.

No equality of chosen presentations, no lift of every raw StrongTrans, and no
naturality of these objectwise equivalences is assumed.  The v5.43 deferred
comparison with the native global mapFunctor remains a separate obligation.
-/

universe u v uH vH uW uP

variable {Context : Type u} [Category.{v} Context]

/-- Identity raw equivalence with genuine unitor 2-isomorphisms. -/
private def rawCoherentIdentity
    (R : RawHigherContextualSystem.{u, v, uH, vH} (Context := Context)) :
    HigherRawSystemCoherentEquivalence R R where
  forward := HigherPointwiseEquivalenceComparison.refl R
  backward := HigherPointwiseEquivalenceComparison.refl R
  unit :=
    (Bicategory.leftUnitor
      (B := RawHigherContextualSystem.{u, v, uH, vH} (Context := Context))
      (𝟙 R)).symm
  counit :=
    Bicategory.leftUnitor
      (B := RawHigherContextualSystem.{u, v, uH, vH} (Context := Context))
      (𝟙 R)

variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-! ## Lift a source adjoint equivalence through the external-label wrapper -/

/-- An underlying source adjoint equivalence yields a classification adjoint
equivalence once the external labels are explicitly identified. -/
def exactUniversalClassificationEquivalenceOfUnderlying
    {X Y : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel}
    (hlabel : X.label = Y.label)
    (e : Bicategory.Equivalence
      (B := ExactUniversalRawObject.{u, v, uH, vH} (W := W) A)
      X.source Y.source) :
    Bicategory.Equivalence
      (B := ExactUniversalClassificationObject (W := W) A
        WorldLabel PresentationLabel) X Y := by
  let f : ExactUniversalClassificationOneCell (W := W) A X Y :=
    { label_eq := hlabel
      map := e.hom }
  let g : ExactUniversalClassificationOneCell (W := W) A Y X :=
    { label_eq := hlabel.symm
      map := e.inv }
  let unit :
      ExactUniversalClassificationOneCell.id (W := W) A X ≅
        ExactUniversalClassificationOneCell.comp (W := W) A f g :=
    ExactUniversalClassificationTwoCell.isoOfUnderlying
      (W := W) A
      (f := ExactUniversalClassificationOneCell.id (W := W) A X)
      (g := ExactUniversalClassificationOneCell.comp (W := W) A f g)
      e.unit
  let counit :
      ExactUniversalClassificationOneCell.comp (W := W) A g f ≅
        ExactUniversalClassificationOneCell.id (W := W) A Y :=
    ExactUniversalClassificationTwoCell.isoOfUnderlying
      (W := W) A
      (f := ExactUniversalClassificationOneCell.comp (W := W) A g f)
      (g := ExactUniversalClassificationOneCell.id (W := W) A Y)
      e.counit
  exact Bicategory.Equivalence.mkOfAdjointifyCounit
    (B := ExactUniversalClassificationObject (W := W) A
      WorldLabel PresentationLabel)
    (a := X) (b := Y) (f := f) (g := g) unit counit

@[simp] theorem exactUniversalClassificationEquivalenceOfUnderlying_hom_map
    {X Y : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel}
    (hlabel : X.label = Y.label)
    (e : Bicategory.Equivalence
      (B := ExactUniversalRawObject.{u, v, uH, vH} (W := W) A)
      X.source Y.source) :
    (exactUniversalClassificationEquivalenceOfUnderlying
      (W := W) A hlabel e).hom.map = e.hom :=
  rfl

@[simp] theorem exactUniversalClassificationEquivalenceOfUnderlying_inv_map
    {X Y : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel}
    (hlabel : X.label = Y.label)
    (e : Bicategory.Equivalence
      (B := ExactUniversalRawObject.{u, v, uH, vH} (W := W) A)
      X.source Y.source) :
    (exactUniversalClassificationEquivalenceOfUnderlying
      (W := W) A hlabel e).inv.map = e.inv :=
  rfl

/-- Two exact-universal classification objects with identical raw systems and
explicitly equal labels are adjoint equivalent.  Their presentations need not
be equal.  This is an object statement, not uniqueness of arbitrary raw lifts. -/
theorem exactUniversalClassification_equivalent_of_sameRaw
    (X Y : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)
    (hlabel : X.label = Y.label)
    (hraw : X.source.raw = Y.source.raw) :
    Nonempty (Bicategory.Equivalence
      (B := ExactUniversalClassificationObject (W := W) A
        WorldLabel PresentationLabel) X Y) := by
  have E : HigherRawSystemCoherentEquivalence X.source.raw Y.source.raw := by
    rw [hraw]
    exact rawCoherentIdentity Y.source.raw
  rcases exactUniversalRawObject_equivalent_of_rawCoherentEquivalence
      (W := W) A X.source Y.source E with ⟨e⟩
  exact ⟨exactUniversalClassificationEquivalenceOfUnderlying
    (W := W) A (X := X) (Y := Y) hlabel e⟩

/-! ## Canonical objectwise round trip and essential surjectivity -/

/-- Forgetting to exact liftability and then taking the canonical universal
representative recovers the original object up to classification adjoint
equivalence.  Both the raw equality and label equality are reflexivity proofs. -/
theorem canonicalExactUniversalObject_toExactLiftable_equivalent
    (Y : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    Nonempty (Bicategory.Equivalence
      (B := ExactUniversalClassificationObject (W := W) A
        WorldLabel PresentationLabel)
      (CanonicalExactUniversalObject (W := W) A
        (Y.toExactLiftable (W := W) A)) Y) :=
  exactUniversalClassification_equivalent_of_sameRaw
    (W := W) A
    (CanonicalExactUniversalObject (W := W) A
      (Y.toExactLiftable (W := W) A)) Y rfl rfl

/-- The covering exact-liftable source retains exactly the target's label. -/
theorem exists_exactLiftableObject_sameLabel_equivalent
    (Y : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    ∃ X : ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel,
      X.label = Y.label ∧
        Nonempty (Bicategory.Equivalence
          (B := ExactUniversalClassificationObject (W := W) A
            WorldLabel PresentationLabel)
          ((exactLiftableActualLiftStrictPseudofunctor (W := W) A).obj X) Y) := by
  refine ⟨Y.toExactLiftable (W := W) A, rfl, ?_⟩
  exact canonicalExactUniversalObject_toExactLiftable_equivalent (W := W) A Y

/-- Object essential surjectivity of the actual-lift strict pseudofunctor.
This uses its native object map, independently of the deferred mapFunctor bridge. -/
theorem exactLiftableActualLiftStrictPseudofunctor_object_essentially_surjective
    (Y : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    ∃ X : ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel,
      Nonempty (Bicategory.Equivalence
        (B := ExactUniversalClassificationObject (W := W) A
          WorldLabel PresentationLabel)
        ((exactLiftableActualLiftStrictPseudofunctor (W := W) A).obj X) Y) := by
  rcases exists_exactLiftableObject_sameLabel_equivalent (W := W) A Y with
    ⟨X, _, h⟩
  exact ⟨X, h⟩

/-! ## Regression checks -/

example
    (Y : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    Nonempty (Bicategory.Equivalence
      (B := ExactUniversalClassificationObject (W := W) A
        WorldLabel PresentationLabel)
      ((exactLiftableActualLiftStrictPseudofunctor (W := W) A).obj
        (Y.toExactLiftable (W := W) A)) Y) :=
  canonicalExactUniversalObject_toExactLiftable_equivalent (W := W) A Y

example
    (X Y : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)
    (hlabel : X.label = Y.label)
    (hraw : X.source.raw = Y.source.raw) :
    Nonempty (Bicategory.Equivalence
      (B := ExactUniversalClassificationObject (W := W) A
        WorldLabel PresentationLabel) Y X) :=
  exactUniversalClassification_equivalent_of_sameRaw
    (W := W) A Y X hlabel.symm hraw.symm

/-!
## Boundary after v5.44

Object coverage is proved for the native v5.42 object map, preserving external
labels.  Together with v5.43 we have object coverage and equivalences of the
explicit native v5.41 hom functors.

Still separate: identify those hom functors with the inherited v5.42 mapFunctor
API, then package the resulting global local-equivalence/Whitehead certificate.
No coherent pseudonatural unit for the objectwise round trip is claimed here.
-/

#print axioms exactUniversalClassificationEquivalenceOfUnderlying
#print axioms exactUniversalClassificationEquivalenceOfUnderlying_hom_map
#print axioms exactUniversalClassificationEquivalenceOfUnderlying_inv_map
#print axioms exactUniversalClassification_equivalent_of_sameRaw
#print axioms canonicalExactUniversalObject_toExactLiftable_equivalent
#print axioms exists_exactLiftableObject_sameLabel_equivalent
#print axioms exactLiftableActualLiftStrictPseudofunctor_object_essentially_surjective

end

end KUOS.DependentOriginationExactLiftableActualLiftObjectCoverageV5_44
