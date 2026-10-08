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

namespace Generic

universe uB vB wB uC vC wC

variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]
variable {F G : Pseudofunctor B C}

local instance nativeHomCategory :
    Category (Pseudofunctor.StrongTrans F G) :=
  Pseudofunctor.StrongTrans.homCategory
    (B := B) (C := C) (F := F) (G := G)

/-- Equality-transport inversion changes no 2-cell choice: it transports
the inverse equality between the two actual object components. -/
theorem eqToIso_inv_app_of_app_eq
    {sigma tau : Pseudofunctor.StrongTrans F G}
    (h : sigma = tau) (X : B)
    (happ : tau.app X = sigma.app X) :
    (eqToIso h).inv.as.app X = eqToHom happ := by
  cases h
  cases happ
  rfl

/-- Evaluate the entire five-stage native global modification on one object
*before* specializing to the nested actual-lift pseudofunctors. This keeps
universe and hom-category inference at the small generic boundary. -/
theorem fiveStage_hom_app
    {sigma0 sigma1 sigma2 sigma3 sigma4 sigma5 :
      Pseudofunctor.StrongTrans F G}
    (h1 : sigma1 = sigma0)
    (e1 : sigma1 ≅ sigma2)
    (h2 : sigma2 = sigma3)
    (e2 : sigma3 ≅ sigma4)
    (h3 : sigma4 = sigma5)
    (X : B)
    (happ1 : sigma0.app X = sigma1.app X)
    (happ2 : sigma2.app X = sigma3.app X)
    (happ3 : sigma4.app X = sigma5.app X) :
    ((eqToIso h1).symm ≪≫ e1 ≪≫ eqToIso h2 ≪≫
      e2 ≪≫ eqToIso h3).hom.as.app X =
      eqToHom happ1 ≫ e1.hom.as.app X ≫
        eqToHom happ2 ≫ e2.hom.as.app X ≫ eqToHom happ3 := by
  simp only [isoTrans_hom_app, Iso.symm_hom]
  rw [eqToIso_inv_app_of_app_eq h1 X happ1,
    eqToIso_hom_app_of_app_eq h2 X happ2,
    eqToIso_hom_app_of_app_eq h3 X happ3]

/-- The three whole-StrongTrans equality transports can be erased
pointwise when the entire equality is eliminated *generically*. This
avoids elaborating equality recursors for the large actual-lift records. -/
theorem fiveStage_hom_app_reduced
    {sigma0 sigma1 sigma2 sigma3 sigma4 sigma5 :
      Pseudofunctor.StrongTrans F G}
    (h1 : sigma1 = sigma0)
    (e1 : sigma1 ≅ sigma2)
    (h2 : sigma2 = sigma3)
    (e2 : sigma3 ≅ sigma4)
    (h3 : sigma4 = sigma5) (X : B) :
    ((eqToIso h1).symm ≪≫ e1 ≪≫ eqToIso h2 ≪≫
      e2 ≪≫ eqToIso h3).hom.as.app X =
      e1.hom.as.app X ≫ e2.hom.as.app X := by
  cases h1
  cases h2
  cases h3
  simpa only [eqToHom_refl, Category.id_comp, Category.comp_id] using
    (fiveStage_hom_app (h1 := rfl) (e1 := e1) (h2 := rfl)
      (e2 := e2) (h3 := rfl) (X := X)
      (happ1 := rfl) (happ2 := rfl) (happ3 := rfl))

end Generic

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
  let leading :=
    forwardMapCompGlobalIso (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)
  let trailing :=
    sourceCounitReassociatedInterchangerIso
      (actualLiftDatumV579 (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel))
  have hcomponents :
      (actualLiftForwardSwallowtailGlobalIso (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)).hom.as.app X =
      leading.hom.as.app X ≫ trailing.hom.as.app X := by
    unfold actualLiftForwardSwallowtailGlobalIso
    exact Generic.fiveStage_hom_app_reduced
      (sourceMapCompPathV578_eq_forwardSwallowtailLeft (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      leading
      (middleStrongTrans_eq (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      trailing
      (rightStrongTrans_eq (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      X
  calc
    _ = leading.hom.as.app X ≫ trailing.hom.as.app X := hcomponents
    _ = (actualLiftForwardSwallowtailComponentInterchanger (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) X).hom := by
      dsimp only [leading, trailing]
      rw [forwardMapCompGlobalIso_hom_app (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel) X]
      rw [sourceCounitReassociatedInterchangerIso_hom_app
        (actualLiftDatumV579 (W := W) A
          (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel)) X]
      rfl

#print axioms Generic.eqToIso_inv_app_of_app_eq
#print axioms Generic.fiveStage_hom_app
#print axioms Generic.fiveStage_hom_app_reduced
#print axioms actualLiftForwardSwallowtailGlobalIso_hom_app

end

end KUOS.DependentOriginationForwardSwallowtailGlobalComponentAgreementV5_85
