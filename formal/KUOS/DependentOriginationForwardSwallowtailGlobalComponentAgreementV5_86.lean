import KUOS.DependentOriginationForwardSwallowtailGlobalComponentAgreementV5_85

namespace KUOS.DependentOriginationForwardSwallowtailGlobalComponentAgreementV5_86

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans

open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58
open KUOS.DependentOriginationBiadjunctionTriangulatorHorizontalPastesV5_64.Generic.IncoherentBiadjunctionDatum
open KUOS.DependentOriginationForwardSwallowtailPredicateV5_65
open KUOS.DependentOriginationForwardSwallowtailModificationObstructionV5_70
open KUOS.DependentOriginationForwardSwallowtailComponentInterchangerV5_68
open KUOS.DependentOriginationActualLiftForwardMapCompGlobalV5_78
open KUOS.DependentOriginationForwardSwallowtailNativeBoundaryV5_79
open KUOS.DependentOriginationForwardMiddleNaturalityPasteV5_82
open KUOS.DependentOriginationGlobalForwardSwallowtailInterchangerV5_83
open KUOS.DependentOriginationForwardSwallowtailGlobalComponentAgreementV5_85
open KUOS.DependentOriginationReassociatedSourceCounitInterchangerV5_77.Generic.IncoherentBiadjunctionDatum

set_option autoImplicit false
set_option maxHeartbeats 300000
noncomputable section

/-!
# Native global-to-canonical component comparison (v5.86)

The three intermediate eqToIso adapters of the native v5.83 global
modification are equality transports. Their object components are
definitionally equal for the *unchanged* actual-lift datum. We use the
generic v5.85 transport calculus and the separately pinned v5.85
component-identity lemmas instead of unfolding the actual-lift records.
This theorem is not the v5.65 forward swallowtail equation.
-/

universe u v uH vH uW uP

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-- Use exactly the native v5.83 syntactic StrongTrans hom category.
In particular the v5.78 `roundtripV578` abbreviation alone does not
reliably trigger instance resolution for v5.65/v5.79 boundary records. -/
local instance forwardSwallowtailHomCategoryV586 :
    Category
      (Pseudofunctor.StrongTrans
        (Pseudofunctor.id
          (ActualLiftSource.{u, v, uH, vH, uW, uP}
            (W := W) A WorldLabel PresentationLabel))
        (actualLiftForwardSwallowtailRoundtripV70 (W := W) A
          (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel))) :=
  Pseudofunctor.StrongTrans.homCategory
    (B := ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)
    (C := ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)
    (F := Pseudofunctor.id
      (ActualLiftSource.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel))
    (G := actualLiftForwardSwallowtailRoundtripV70 (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel))

/-- The v5.78 factor has its own explicit syntactic presentation.
The declared category is the *same mathlib homCategory*, not a
different structure or a strictification of F/G. -/
local instance sourceHomCategoryV586MapComp :
    Category
      (Pseudofunctor.StrongTrans
        (Pseudofunctor.id
          (sourceV578 (W := W) A
            (WorldLabel := WorldLabel)
            (PresentationLabel := PresentationLabel)))
        (roundtripV578 (W := W) A
          (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel))) :=
  Pseudofunctor.StrongTrans.homCategory
    (B := sourceV578 (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    (C := sourceV578 (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    (F := Pseudofunctor.id _)
    (G := roundtripV578 (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel))

/-- The five native stages before removing the three componentwise
reflexive equality transports. No expansion of the biadjunction datum
is used to evaluate the modification composition. -/
theorem actualLiftGlobalIso_hom_app_fiveStage
    (X : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    (actualLiftForwardSwallowtailGlobalIso (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).hom.as.app X =
    eqToHom (show
      (actualLiftForwardSwallowtailLeftV70 (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)).app X =
      (sourceMapCompPathV578 (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)).app X from rfl) ≫
    (forwardMapCompGlobalIso (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).hom.as.app X ≫
    eqToHom (middleComponent_eq (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) X) ≫
    (sourceCounitReassociatedInterchangerIso
      (actualLiftDatumV579 (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel))).hom.as.app X ≫
    eqToHom (rightComponent_eq (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) X) := by
  exact
    KUOS.DependentOriginationForwardSwallowtailGlobalComponentAgreementV5_85.Generic.fiveStage_hom_app_of_iso_eq
      (sourceMapCompPathV578_eq_forwardSwallowtailLeft (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel))
      (forwardMapCompGlobalIso (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel))
      (middleStrongTrans_eq (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel))
      (sourceCounitReassociatedInterchangerIso
        (actualLiftDatumV579 (W := W) A
          (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel)))
      (rightStrongTrans_eq (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel))
      (actualLiftForwardSwallowtailGlobalIso (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel))
      (by rfl)
      X
      (by rfl)
      (middleComponent_eq (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) X)
      (rightComponent_eq (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) X)

/-- The three equality transports are identity 2-cells at every original
actual-lift source object. Hence the complete five-stage component is the
two-factor native modification paste. -/
theorem actualLiftGlobalIso_hom_app_twoFactor
    (X : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    (actualLiftForwardSwallowtailGlobalIso (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).hom.as.app X =
    (forwardMapCompGlobalIso (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).hom.as.app X ≫
    (sourceCounitReassociatedInterchangerIso
      (actualLiftDatumV579 (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel))).hom.as.app X := by
  rw [actualLiftGlobalIso_hom_app_fiveStage (W := W) A
    (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel) X]
  rw [leftEqToHom_app_is_id (W := W) A
    (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel) X]
  rw [middleEqToHom_app_is_id (W := W) A
    (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel) X
    (middleComponent_eq (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) X)]
  rw [rightEqToHom_app_is_id (W := W) A
    (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel) X]
  simp only [Category.id_comp, Category.comp_id]

/-- The originally constructed global v5.83 Iso has, at every actual-lift
source object, *exactly* the unchanged four-cell v5.68 component.
This does not assert forward/reverse swallowtail coherence. -/
theorem actualLiftGlobalCanonicalComponentAgreement :
    ActualLiftGlobalCanonicalComponentAgreement (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) := by
  intro X
  exact
    (actualLiftGlobalIso_hom_app_twoFactor (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) X).trans
    (actualLiftForwardSwallowtailTwoFactor_hom_app (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) X)

#print axioms actualLiftGlobalIso_hom_app_fiveStage
#print axioms actualLiftGlobalIso_hom_app_twoFactor
#print axioms actualLiftGlobalCanonicalComponentAgreement

end

end KUOS.DependentOriginationForwardSwallowtailGlobalComponentAgreementV5_86
