import KUOS.DependentOriginationForwardSwallowtailContractionExpansionV5_89

namespace KUOS.DependentOriginationForwardSwallowtailExplicitResidualV5_90

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans

open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58
open KUOS.DependentOriginationExactLiftableActualLiftTriangleComponentsV5_51
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePseudofunctorV5_48
open KUOS.DependentOriginationExactLiftableActualLiftSourceUnitV5_50
open KUOS.DependentOriginationForwardSwallowtailComponentInterchangerV5_68
open KUOS.DependentOriginationBiadjunctionTriangulatorHorizontalPastesV5_64.Generic.IncoherentBiadjunctionDatum
open KUOS.DependentOriginationForwardSwallowtailPredicateV5_65
open KUOS.DependentOriginationForwardSwallowtailPredicateV5_65.Generic.IncoherentBiadjunctionDatum
open KUOS.DependentOriginationForwardSwallowtailNativeBoundaryV5_79
open KUOS.DependentOriginationForwardSwallowtailPointwiseBoundaryV5_88
open KUOS.DependentOriginationForwardSwallowtailContractionExpansionV5_89

set_option autoImplicit false
set_option maxHeartbeats 300000
noncomputable section

/-!
# Forward swallowtail: exact original-contraction residual (v5.90)

This continues v5.88/v5.89 without asserting the swallowtail law.
It expands the original right-hand side through the genuine forward
and reverse triangle contractions and the non-strict G.mapId cell,
then identifies the *single remaining* original four-cell equality.

The source and target StrongTrans hom categories are bound to precisely
the pinned Mathlib instances.  No replacement F, G, eta, eps, comparison
2-cell, or extra coherence assumption is introduced.
-/

universe u v uH vH uW uP

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

local instance sourceRoundtripHomCategoryV590 :
    Category
      (Pseudofunctor.StrongTrans
        (sourceRoundtrip
          (actualLiftDatumV579 (W := W) A
            (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
        (sourceRoundtrip
          (actualLiftDatumV579 (W := W) A
            (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))) :=
  Pseudofunctor.StrongTrans.homCategory
    (B := ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)
    (C := ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)
    (F := sourceRoundtrip
      (actualLiftDatumV579 (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
    (G := sourceRoundtrip
      (actualLiftDatumV579 (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))

local instance forwardHomCategoryV590 :
    Category
      (Pseudofunctor.StrongTrans
        (Pseudofunctor.id
          (ActualLiftSource.{u, v, uH, vH, uW, uP}
            (W := W) A WorldLabel PresentationLabel))
        (sourceRoundtrip
          (actualLiftDatumV579 (W := W) A
            (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))) :=
  Pseudofunctor.StrongTrans.homCategory
    (B := ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)
    (C := ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)
    (F := Pseudofunctor.id
      (ActualLiftSource.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel))
    (G := sourceRoundtrip
      (actualLiftDatumV579 (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))

/-- The original v5.65 triangulator paste, at a source object,
is the old unit whiskering the v5.51 forward contraction mapped through
the original non-strict G, its actual G.mapId, and the inverse of the
v5.51 reverse contraction. -/
theorem actualLiftForwardTriangulatorPaste_hom_app_expanded
    (X : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    (forwardTriangulatorPaste
      (actualLiftDatumV579 (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel))).hom.as.app X =
      ((actualLiftSourceRoundtripUnit (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)).app X) ◁
        (((actualLiftQuasiInversePseudofunctor (W := W) A).map₂
            ((actualLiftForwardTriangleIso (W := W) A X).hom) ≫
          ((actualLiftQuasiInversePseudofunctor (W := W) A).mapId
            ((actualLiftForwardPseudofunctor
              (W := W) A WorldLabel PresentationLabel).obj X)).hom) ≫
          (actualLiftQuasiInverseTriangleIso (W := W) A
            ((actualLiftForwardPseudofunctor
              (W := W) A WorldLabel PresentationLabel).obj X)).inv) := by
  exact Generic.forwardTriangulatorPaste_hom_app
    (actualLiftDatumV579 (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) X

/-- No swallowtail assumption: the exact component comparison
between v5.64's original right-hand side and the explicit normal form. -/
theorem actualLiftForwardOriginalPaste_eq_expanded
    (X : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    ((actualLiftSourceRoundtripUnit (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).app X) ◁
      (sourceHorizontalPaste
        (actualLiftDatumV579 (W := W) A
          (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel))).hom.as.app X =
    ((actualLiftSourceRoundtripUnit (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).app X) ◁
      (((actualLiftQuasiInversePseudofunctor (W := W) A).map₂
          ((actualLiftForwardTriangleIso (W := W) A X).hom) ≫
        ((actualLiftQuasiInversePseudofunctor (W := W) A).mapId
          ((actualLiftForwardPseudofunctor
            (W := W) A WorldLabel PresentationLabel).obj X)).hom) ≫
        (actualLiftQuasiInverseTriangleIso (W := W) A
          ((actualLiftForwardPseudofunctor
            (W := W) A WorldLabel PresentationLabel).obj X)).inv) := by
  exact congrArg
    (fun m =>
      ((actualLiftSourceRoundtripUnit (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)).app X) ◁ m)
    (actualLiftSourceHorizontalPaste_hom_app_expanded
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) X)

/-- The F3 obstruction stated with no abstract horizontal paste:
the original v5.68 four-cell comparison must equal the actual
v5.51 contraction terms, including non-strict G.mapId. -/
def ActualLiftForwardSwallowtailExpandedResidual : Prop :=
  ∀ X : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel,
    (actualLiftForwardSwallowtailComponentInterchanger.{u, v, uH, uW, uP, vH}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) X).hom =
    ((actualLiftSourceRoundtripUnit (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).app X) ◁
      (((actualLiftQuasiInversePseudofunctor (W := W) A).map₂
          ((actualLiftForwardTriangleIso (W := W) A X).hom) ≫
        ((actualLiftQuasiInversePseudofunctor (W := W) A).mapId
          ((actualLiftForwardPseudofunctor
            (W := W) A WorldLabel PresentationLabel).obj X)).hom) ≫
        (actualLiftQuasiInverseTriangleIso (W := W) A
          ((actualLiftForwardPseudofunctor
            (W := W) A WorldLabel PresentationLabel).obj X)).inv)

/-- The original pointwise F3 proposition from v5.88 is *equivalent*
to the explicit contraction residual, with no coherence law assumed. -/
theorem actualLiftForwardPointwise_iff_expanded :
    ActualLiftForwardSwallowtailPointwiseAgreement.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) ↔
    ActualLiftForwardSwallowtailExpandedResidual.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) := by
  constructor
  · intro h X
    exact (h X).trans
      (actualLiftForwardOriginalPaste_eq_expanded
        (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) X)
  · intro h X
    exact (h X).trans
      (actualLiftForwardOriginalPaste_eq_expanded
        (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) X).symm

/-- The genuine v5.65 global forward swallowtail predicate is now
reduced to the *same* concrete four-cell/contraction residual.
In particular this theorem does not establish either side. -/
theorem actualLiftForwardPredicate_iff_expanded :
    actualLiftForwardSwallowtailPredicate.{u, v, uH, uW, uP, vH}
      (W := W) A
      (actualLiftForwardSwallowtailCanonicalIso.{u, v, uH, uW, uP, vH}
        (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)) ↔
    ActualLiftForwardSwallowtailExpandedResidual.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) := by
  exact
    (actualLiftForwardSwallowtailPredicate_iff_pointwise
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).trans
    (actualLiftForwardPointwise_iff_expanded
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel))

#print axioms actualLiftForwardTriangulatorPaste_hom_app_expanded
#print axioms actualLiftForwardOriginalPaste_eq_expanded
#print axioms ActualLiftForwardSwallowtailExpandedResidual
#print axioms actualLiftForwardPointwise_iff_expanded
#print axioms actualLiftForwardPredicate_iff_expanded

end

end KUOS.DependentOriginationForwardSwallowtailExplicitResidualV5_90
