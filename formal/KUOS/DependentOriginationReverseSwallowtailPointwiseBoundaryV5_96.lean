import KUOS.DependentOriginationReverseSwallowtailTargetPasteExpansionV5_94
import KUOS.DependentOriginationReverseSwallowtailCounitFourCellV5_95

namespace KUOS.DependentOriginationReverseSwallowtailPointwiseBoundaryV5_96

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans

open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58
open KUOS.DependentOriginationExactLiftableActualLiftTriangleComponentsV5_51
open KUOS.DependentOriginationExactLiftableActualLiftTargetCounitV5_49
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePseudofunctorV5_48
open KUOS.DependentOriginationBiadjunctionTriangulatorHorizontalPastesV5_64.Generic.IncoherentBiadjunctionDatum
open KUOS.DependentOriginationReverseSwallowtailPredicateV5_66
open KUOS.DependentOriginationReverseSwallowtailPredicateV5_66.Generic.IncoherentBiadjunctionDatum
open KUOS.DependentOriginationReverseSwallowtailTargetPasteExpansionV5_94
open KUOS.DependentOriginationReverseSwallowtailCounitFourCellV5_95

set_option autoImplicit false
set_option maxHeartbeats 300000
noncomputable section

/-!
# The exact original reverse swallowtail boundary after v5.94–v5.95 (v5.96)

The original counit-centered four-cell family must obey modification
naturality before it can become a global native inverse modification.
That naturality is independent of equality with the original v5.64 target
horizontal triangulator paste. Both obligations are retained explicitly.

The pointwise equation is normalized through the genuine original forward
and reverse triangle contractions including the native F.mapId. The
equivalence with the native F4 predicate is conditional on a proof of
naturality. Neither F4 obligation is assumed or claimed solved.
-/

universe u v uH vH uW uP

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

local instance reverseSwallowtailHomCategoryV596 :
    Category
      (Pseudofunctor.StrongTrans
        (targetRoundtrip
          (actualLiftReverseSwallowtailDatum (W := W) A
            (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
        (Pseudofunctor.id
          (ActualLiftTarget.{u, v, uH, vH, uW, uP}
            (W := W) A WorldLabel PresentationLabel))) :=
  Pseudofunctor.StrongTrans.homCategory
    (B := ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)
    (C := ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)
    (F := targetRoundtrip
      (actualLiftReverseSwallowtailDatum (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
    (G := Pseudofunctor.id
      (ActualLiftTarget.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel))

local instance targetEndHomCategoryV596 :
    Category
      (Pseudofunctor.StrongTrans
        (targetRoundtrip
          (actualLiftReverseSwallowtailDatum (W := W) A
            (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
        (targetRoundtrip
          (actualLiftReverseSwallowtailDatum (W := W) A
            (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))) :=
  Pseudofunctor.StrongTrans.homCategory
    (B := ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)
    (C := ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)
    (F := targetRoundtrip
      (actualLiftReverseSwallowtailDatum (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
    (G := targetRoundtrip
      (actualLiftReverseSwallowtailDatum (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))

/-- The genuine modification naturality square for the original v5.95
counit-centered reverse four-cell at each original target 1-cell. -/
def ActualLiftReverseSwallowtailModificationNaturality : Prop :=
  ∀ {Y Z : ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel}
    (f : Y ⟶ Z),
    (targetRoundtrip
      (actualLiftReverseSwallowtailDatum (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).map f ◁
      (actualLiftReverseSwallowtailComponentInterchanger
        (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) Z).hom ≫
      ((reverseSwallowtailRight
        (actualLiftReverseSwallowtailDatum (W := W) A
          (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).naturality f).hom =
    ((reverseSwallowtailLeft
      (actualLiftReverseSwallowtailDatum (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).naturality f).hom ≫
      (actualLiftReverseSwallowtailComponentInterchanger
        (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) Y).hom ▷
      (Pseudofunctor.id
        (ActualLiftTarget.{u, v, uH, vH, uW, uP}
          (W := W) A WorldLabel PresentationLabel)).map f

/-- Package the original objectwise reverse four-cells into Mathlib's
native invertible modification, *given* its exact naturality proof. -/
def actualLiftReverseSwallowtailInterchangerOfNaturality
    (h : ActualLiftReverseSwallowtailModificationNaturality.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) :
    ActualLiftReverseSwallowtailInterchanger.{u, v, uH, uW, uP, vH}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) :=
  Pseudofunctor.StrongTrans.isoMk
    (η := reverseSwallowtailLeft
      (actualLiftReverseSwallowtailDatum (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
    (θ := reverseSwallowtailRight
      (actualLiftReverseSwallowtailDatum (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
    (fun Y => actualLiftReverseSwallowtailComponentInterchanger
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) Y)
    (by intro Y Z f; exact h f)

@[simp] theorem actualLiftReverseInterchangerOfNaturality_hom_app
    (h : ActualLiftReverseSwallowtailModificationNaturality.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel))
    (Y : ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    (actualLiftReverseSwallowtailInterchangerOfNaturality
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) h).hom.as.app Y =
      (actualLiftReverseSwallowtailComponentInterchanger
        (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) Y).hom :=
  rfl

/-- The naturality requirement is equivalent to existence of a native
global Iso having exactly the original v5.95 components. -/
theorem actualLiftReverseNaturality_iff_exists_modification :
    ActualLiftReverseSwallowtailModificationNaturality.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) ↔
    ∃ Sigma : ActualLiftReverseSwallowtailInterchanger.{u, v, uH, uW, uP, vH}
        (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel),
      ∀ Y : ActualLiftTarget.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel,
        Sigma.hom.as.app Y =
          (actualLiftReverseSwallowtailComponentInterchanger
            (W := W) A (WorldLabel := WorldLabel)
            (PresentationLabel := PresentationLabel) Y).hom := by
  constructor
  · intro h
    exact ⟨actualLiftReverseSwallowtailInterchangerOfNaturality
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) h,
      by intro Y; rfl⟩
  · rintro ⟨Sigma, hApp⟩ Y Z f
    have hNatural := Sigma.hom.as.naturality f
    rw [hApp Z, hApp Y] at hNatural
    exact hNatural

/-- The genuinely remaining pointwise F4 equation, without assuming the
naturality of its original four-cell family. -/
def ActualLiftReverseSwallowtailPointwiseAgreement : Prop :=
  ∀ Y : ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel,
    (actualLiftReverseSwallowtailComponentInterchanger
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) Y).hom =
    (reverseTriangulatorPaste
      (actualLiftReverseSwallowtailDatum (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))).hom.as.app Y

/-- The original F4 condition with both genuine triangle contractions,
the unchanged strict F.mapId, and counit right whiskering visible. -/
def ActualLiftReverseSwallowtailExpandedResidual : Prop :=
  ∀ Y : ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel,
    (actualLiftReverseSwallowtailComponentInterchanger
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) Y).hom =
      ((actualLiftForwardTriangleIso (W := W) A
          ((actualLiftQuasiInversePseudofunctor (W := W) A).obj Y)).hom ≫
        (((actualLiftForwardPseudofunctor
          (W := W) A WorldLabel PresentationLabel).mapId
            ((actualLiftQuasiInversePseudofunctor
              (W := W) A).obj Y)).inv ≫
          (actualLiftForwardPseudofunctor
            (W := W) A WorldLabel PresentationLabel).map₂
            ((actualLiftQuasiInverseTriangleIso (W := W) A Y).inv))) ▷
          (actualLiftTargetRoundtripCounit (W := W) A).app Y

/-- v5.94's exact source component expansion gives an equivalence
of the two genuine F4 pointwise residual formulations. -/
theorem actualLiftReversePointwise_iff_expanded :
    ActualLiftReverseSwallowtailPointwiseAgreement.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) ↔
    ActualLiftReverseSwallowtailExpandedResidual.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) := by
  constructor
  · intro h Y
    exact (h Y).trans
      (actualLiftReverseTriangulatorPaste_hom_app
        (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) Y)
  · intro h Y
    exact (h Y).trans
      (actualLiftReverseTriangulatorPaste_hom_app
        (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) Y).symm

/-- Given naturality, the original reverse v5.66 predicate is exactly the
v5.95 versus v5.94 pointwise equation, and is not proved here. -/
theorem actualLiftReversePredicate_iff_pointwise
    (hNat : ActualLiftReverseSwallowtailModificationNaturality.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) :
    actualLiftReverseSwallowtailPredicate (W := W) A
      (actualLiftReverseSwallowtailInterchangerOfNaturality
        (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) hNat) ↔
    ActualLiftReverseSwallowtailPointwiseAgreement.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) := by
  constructor
  · intro h Y
    change
      actualLiftReverseSwallowtailInterchangerOfNaturality
        (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) hNat =
      reverseTriangulatorPaste
        (actualLiftReverseSwallowtailDatum (W := W) A
          (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) at h
    have hApp := congrArg
      (fun Sigma : ActualLiftReverseSwallowtailInterchanger.{u, v, uH, uW, uP, vH}
        (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) =>
        Sigma.hom.as.app Y) h
    exact
      (actualLiftReverseInterchangerOfNaturality_hom_app
        (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) hNat Y).symm.trans hApp
  · intro h
    change
      actualLiftReverseSwallowtailInterchangerOfNaturality
        (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) hNat =
      reverseTriangulatorPaste
        (actualLiftReverseSwallowtailDatum (W := W) A
          (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    apply Iso.ext
    apply Pseudofunctor.StrongTrans.homCategory.ext
    intro Y
    exact
      (actualLiftReverseInterchangerOfNaturality_hom_app
        (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) hNat Y).trans (h Y)

/-- Same global predicate reduced to the actual original contractions,
conditionally on the independent naturality obligation. -/
theorem actualLiftReversePredicate_iff_expanded
    (hNat : ActualLiftReverseSwallowtailModificationNaturality.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) :
    actualLiftReverseSwallowtailPredicate (W := W) A
      (actualLiftReverseSwallowtailInterchangerOfNaturality
        (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) hNat) ↔
    ActualLiftReverseSwallowtailExpandedResidual.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) :=
  (actualLiftReversePredicate_iff_pointwise
    (W := W) A (WorldLabel := WorldLabel)
    (PresentationLabel := PresentationLabel) hNat).trans
    (actualLiftReversePointwise_iff_expanded
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel))

#print axioms ActualLiftReverseSwallowtailModificationNaturality
#print axioms actualLiftReverseSwallowtailInterchangerOfNaturality
#print axioms actualLiftReverseNaturality_iff_exists_modification
#print axioms ActualLiftReverseSwallowtailPointwiseAgreement
#print axioms ActualLiftReverseSwallowtailExpandedResidual
#print axioms actualLiftReversePointwise_iff_expanded
#print axioms actualLiftReversePredicate_iff_pointwise
#print axioms actualLiftReversePredicate_iff_expanded

end

end KUOS.DependentOriginationReverseSwallowtailPointwiseBoundaryV5_96
