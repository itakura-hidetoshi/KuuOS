import KUOS.DependentOriginationForwardTransportComponentsV5_84

namespace KUOS.DependentOriginationForwardSwallowtailGlobalComponentAgreementV5_85

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans

open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58
open KUOS.DependentOriginationForwardSwallowtailPredicateV5_65
open KUOS.DependentOriginationForwardSwallowtailModificationObstructionV5_70
open KUOS.DependentOriginationForwardSwallowtailComponentInterchangerV5_68
open KUOS.DependentOriginationActualLiftForwardMapCompGlobalV5_78
open KUOS.DependentOriginationForwardSwallowtailNativeBoundaryV5_79
open KUOS.DependentOriginationForwardMiddleNaturalityPasteV5_82
open KUOS.DependentOriginationGlobalForwardSwallowtailInterchangerV5_83
open KUOS.DependentOriginationForwardTransportComponentsV5_84.Generic
open KUOS.DependentOriginationReassociatedSourceCounitInterchangerV5_77.Generic.IncoherentBiadjunctionDatum

set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section

/-!
# Global interchanger versus the original four-cell component (v5.85)

Compare the v5.83 native, globally natural invertible modification with the
unchanged v5.68 G.mapComp--associator--unit-naturality--associator paste.
The three `eqToIso` adapters in the global modification transport only along
already proved whole StrongTrans equalities. In particular, no alteration of
the original unit, counit, pseudofunctor mapComp, or source object is allowed.

This is distinct from the v5.65 swallowtail equation against the
triangulator paste, which remains a separate obligation.
-/

universe u v uH vH uW uP

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

local instance sourceHomCategoryV585 :
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
    (F := Pseudofunctor.id _)
    (G := actualLiftForwardSwallowtailRoundtripV70 (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel))

/-- The v5.83 global comparison has precisely the original canonical v5.68
four-cell paste on each source object. The independent naturality theorem
then promotes that specific old family to a modification. -/
theorem actualLiftForwardSwallowtailGlobalIso_hom_app
    (X : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    (actualLiftForwardSwallowtailGlobalIso (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).hom.as.app X =
    (actualLiftForwardSwallowtailComponentInterchanger (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) X).hom := by
  simp only [actualLiftForwardSwallowtailGlobalIso,
    Iso.trans_hom, Iso.symm_hom,
    Pseudofunctor.StrongTrans.homCategory_comp_as_app,
    eqToIso_inv_app, eqToIso_hom_app,
    eqToHom_refl, Category.id_comp, Category.comp_id,
    forwardMapCompGlobalIso_hom_app,
    sourceCounitReassociatedInterchangerIso_hom_app,
    sourceCounitReassociatedComponentIso,
    actualLiftForwardSwallowtailComponentInterchanger,
    Category.assoc]
  rfl

#print axioms actualLiftForwardSwallowtailGlobalIso_hom_app

end

end KUOS.DependentOriginationForwardSwallowtailGlobalComponentAgreementV5_85
