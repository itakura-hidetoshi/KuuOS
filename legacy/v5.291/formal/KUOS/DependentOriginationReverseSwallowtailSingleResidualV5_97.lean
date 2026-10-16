import KUOS.DependentOriginationReverseSwallowtailPointwiseBoundaryV5_96

namespace KUOS.DependentOriginationReverseSwallowtailSingleResidualV5_97

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans

open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58
open KUOS.DependentOriginationBiadjunctionTriangulatorHorizontalPastesV5_64.Generic.IncoherentBiadjunctionDatum
open KUOS.DependentOriginationReverseSwallowtailPredicateV5_66
open KUOS.DependentOriginationReverseSwallowtailPredicateV5_66.Generic.IncoherentBiadjunctionDatum
open KUOS.DependentOriginationReverseSwallowtailCounitFourCellV5_95
open KUOS.DependentOriginationReverseSwallowtailPointwiseBoundaryV5_96

set_option autoImplicit false
set_option maxHeartbeats 300000
noncomputable section

/-!
# F4: The original pointwise comparison implies its own naturality (v5.97)

The original v5.94 target triangulator paste is already an actual native
invertible modification. Therefore if its component equals the *unchanged*
v5.95 counit four-cell at every original target object, the original
four-cell must satisfy the required modification naturality square.
No second naturality assumption is needed.

This is not a proof of pointwise agreement. It reduces the two obligations
isolated in v5.96 to the genuine single original F4 residual and proves
that this condition supplies precisely the original v5.66 global law.
-/

universe u v uH vH uW uP

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

local instance reverseHomCategoryV597 :
    Category
      (Pseudofunctor.StrongTrans
        (targetRoundtrip (actualLiftReverseSwallowtailDatum (W := W) A
          (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
        (Pseudofunctor.id
          (ActualLiftTarget.{u, v, uH, vH, uW, uP}
            (W := W) A WorldLabel PresentationLabel))) :=
  Pseudofunctor.StrongTrans.homCategory
    (B := ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)
    (C := ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)
    (F := targetRoundtrip (actualLiftReverseSwallowtailDatum (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
    (G := Pseudofunctor.id
      (ActualLiftTarget.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel))

/-- The fully native original v5.94 triangulator paste makes the
original v5.95 four-cell family natural as soon as the original
pointwise F4 equality has been proved. -/
theorem actualLiftReversePointwise_implies_naturality
    (h : ActualLiftReverseSwallowtailPointwiseAgreement.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) :
    ActualLiftReverseSwallowtailModificationNaturality.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) := by
  intro Y Z f
  have hNatural :=
    (reverseTriangulatorPaste
      (actualLiftReverseSwallowtailDatum (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel))).hom.as.naturality f
  rw [← h Z, ← h Y] at hNatural
  exact hNatural

/-- The single *original* pointwise equation exactly characterizes
existence of a native global inverse modification whose components
are the original v5.95 counit four-cells and which satisfies the
unchanged v5.66 reverse swallowtail predicate. No arbitrary
comparison 2-cell can be substituted. -/
theorem actualLiftReversePointwise_iff_original_global_swallowtail :
    ActualLiftReverseSwallowtailPointwiseAgreement.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) ↔
    ∃ Sigma : ActualLiftReverseSwallowtailInterchanger.{u, v, uH, uW, uP, vH}
        (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel),
      (∀ Y : ActualLiftTarget.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel,
        Sigma.hom.as.app Y =
          (actualLiftReverseSwallowtailComponentInterchanger
            (W := W) A (WorldLabel := WorldLabel)
            (PresentationLabel := PresentationLabel) Y).hom) ∧
      actualLiftReverseSwallowtailPredicate (W := W) A Sigma := by
  constructor
  · intro h
    have hn :
        ActualLiftReverseSwallowtailModificationNaturality.{u, v, uH, vH, uW, uP}
          (W := W) A (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel) :=
      actualLiftReversePointwise_implies_naturality
        (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) h
    refine ⟨actualLiftReverseSwallowtailInterchangerOfNaturality
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) hn, ?_, ?_⟩
    · intro Y
      rfl
    · exact (actualLiftReversePredicate_iff_pointwise
        (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) hn).mpr h
  · rintro ⟨Sigma, hApp, hPred⟩ Y
    change Sigma =
      reverseTriangulatorPaste
        (actualLiftReverseSwallowtailDatum (W := W) A
          (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel)) at hPred
    have hComponent := congrArg
      (fun e : ActualLiftReverseSwallowtailInterchanger.{u, v, uH, uW, uP, vH}
        (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) => e.hom.as.app Y) hPred
    exact (hApp Y).symm.trans hComponent

/-- The single genuine F4 obstruction can be displayed using only
the original contractions and F.mapId (v5.94), without any independent
naturality premise. Both directions are proved equivalences. -/
theorem actualLiftReverseExpanded_iff_original_global_swallowtail :
    ActualLiftReverseSwallowtailExpandedResidual.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) ↔
    ∃ Sigma : ActualLiftReverseSwallowtailInterchanger.{u, v, uH, uW, uP, vH}
        (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel),
      (∀ Y : ActualLiftTarget.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel,
        Sigma.hom.as.app Y =
          (actualLiftReverseSwallowtailComponentInterchanger
            (W := W) A (WorldLabel := WorldLabel)
            (PresentationLabel := PresentationLabel) Y).hom) ∧
      actualLiftReverseSwallowtailPredicate (W := W) A Sigma :=
  (actualLiftReversePointwise_iff_expanded
    (W := W) A (WorldLabel := WorldLabel)
    (PresentationLabel := PresentationLabel)).symm.trans
    (actualLiftReversePointwise_iff_original_global_swallowtail
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel))

#print axioms actualLiftReversePointwise_implies_naturality
#print axioms actualLiftReversePointwise_iff_original_global_swallowtail
#print axioms actualLiftReverseExpanded_iff_original_global_swallowtail

end

end KUOS.DependentOriginationReverseSwallowtailSingleResidualV5_97
