import KUOS.DependentOriginationForwardTransportComponentsV5_84

namespace KUOS.DependentOriginationForwardSwallowtailGlobalComponentAgreementV5_85

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


/-- Transfer the five-stage component formula to a *named* native Iso.
The input `hSigma` is an ordinary proved equality, not another
coherence cell. This avoids re-elaborating the expanded actual-lift
Iso components at the specialization site. -/
theorem fiveStage_hom_app_of_iso_eq
    {sigma0 sigma1 sigma2 sigma3 sigma4 sigma5 :
      Pseudofunctor.StrongTrans F G}
    (h1 : sigma1 = sigma0)
    (e1 : sigma1 ≅ sigma2)
    (h2 : sigma2 = sigma3)
    (e2 : sigma3 ≅ sigma4)
    (h3 : sigma4 = sigma5)
    (Sigma : sigma0 ≅ sigma5)
    (hSigma : Sigma = (eqToIso h1).symm ≪≫ e1 ≪≫
      eqToIso h2 ≪≫ e2 ≪≫ eqToIso h3)
    (X : B)
    (happ1 : sigma0.app X = sigma1.app X)
    (happ2 : sigma2.app X = sigma3.app X)
    (happ3 : sigma4.app X = sigma5.app X) :
    Sigma.hom.as.app X =
      eqToHom happ1 ≫ e1.hom.as.app X ≫
        eqToHom happ2 ≫ e2.hom.as.app X ≫ eqToHom happ3 := by
  rw [hSigma]
  exact fiveStage_hom_app h1 e1 h2 e2 h3 X happ1 happ2 happ3


/-- Combine a global Iso's proven five-stage presentation with a supplied
pointwise target cell entirely at the generic StrongTrans boundary.
This ensures `Eq.trans` is elaborated without expanding actual-lift records. -/
theorem fiveStage_hom_app_of_iso_eq_and_component
    {sigma0 sigma1 sigma2 sigma3 sigma4 sigma5 :
      Pseudofunctor.StrongTrans F G}
    (h1 : sigma1 = sigma0)
    (e1 : sigma1 ≅ sigma2)
    (h2 : sigma2 = sigma3)
    (e2 : sigma3 ≅ sigma4)
    (h3 : sigma4 = sigma5)
    (Sigma : sigma0 ≅ sigma5)
    (hSigma : Sigma = (eqToIso h1).symm ≪≫ e1 ≪≫
      eqToIso h2 ≪≫ e2 ≪≫ eqToIso h3)
    (X : B)
    (happ1 : sigma0.app X = sigma1.app X)
    (happ2 : sigma2.app X = sigma3.app X)
    (happ3 : sigma4.app X = sigma5.app X)
    (target : sigma0.app X ⟶ sigma5.app X)
    (hcanonical :
      eqToHom happ1 ≫ e1.hom.as.app X ≫ eqToHom happ2 ≫
        e2.hom.as.app X ≫ eqToHom happ3 = target) :
    Sigma.hom.as.app X = target :=
  (fiveStage_hom_app_of_iso_eq h1 e1 h2 e2 h3 Sigma hSigma
    X happ1 happ2 happ3).trans hcanonical


end Generic

universe u v uH vH uW uP

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-- Pin the *syntactic* v5.78 StrongTrans hom category needed by
`forwardMapCompGlobalIso`. The elaborator does not reliably synthesize
this through the expanded v5.70 aliases at large universe levels. -/
local instance sourceHomCategoryV585 :
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

/-- v5.65 presents the same category by the original source
and stored biadjunction roundtrip, rather than the v5.78 abbreviations. -/
local instance sourceHomCategoryV585Predicate :
    Category
      (Pseudofunctor.StrongTrans
        (Pseudofunctor.id
          (ActualLiftSource.{u, v, uH, vH, uW, uP}
            (W := W) A WorldLabel PresentationLabel))
        (sourceRoundtrip
          (actualLiftForwardSwallowtailDatum (W := W) A
            (WorldLabel := WorldLabel)
            (PresentationLabel := PresentationLabel)))) :=
  Pseudofunctor.StrongTrans.homCategory
    (B := ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)
    (C := ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)
    (F := Pseudofunctor.id _)
    (G := sourceRoundtrip
      (actualLiftForwardSwallowtailDatum (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)))

/-- v5.79's native counit boundary retains a separately named datum. -/
local instance sourceHomCategoryV585Native :
    Category
      (Pseudofunctor.StrongTrans
        (Pseudofunctor.id
          (ActualLiftSource.{u, v, uH, vH, uW, uP}
            (W := W) A WorldLabel PresentationLabel))
        (sourceRoundtrip
          (actualLiftDatumV579 (W := W) A
            (WorldLabel := WorldLabel)
            (PresentationLabel := PresentationLabel)))) :=
  Pseudofunctor.StrongTrans.homCategory
    (B := ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)
    (C := ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)
    (F := Pseudofunctor.id _)
    (G := sourceRoundtrip
      (actualLiftDatumV579 (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)))

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
  -- Use the same concrete hom-category as v5.83 at this specialization.
  -- Avoid three distinct syntactic aliases during eqToIso elaboration.
  letI : Category
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

  let leading :=
    forwardMapCompGlobalIso (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)
  let trailing :=
    sourceCounitReassociatedInterchangerIso
      (actualLiftDatumV579 (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel))
  let hleft :=
    sourceMapCompPathV578_eq_forwardSwallowtailLeft (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)
  let hmiddle :=
    middleStrongTrans_eq (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)
  let hright :=
    rightStrongTrans_eq (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)
  -- Whole-record equalities come from v5.78, v5.82 and v5.79.
  have hIso :
      actualLiftForwardSwallowtailGlobalIso (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) =
        (eqToIso hleft).symm ≪≫ leading ≪≫
          eqToIso hmiddle ≪≫ trailing ≪≫ eqToIso hright := by
    rfl
  -- Specialize the *generic* Iso equality bridge before projecting
  -- components. The resulting LHS is the named original v5.83 Iso.
  -- Match the original v5.68 four-cell paste using the exact v5.78
  -- leading and v5.77 trailing components, not a newly chosen 2-cell.
  have hcanonical :
      leading.hom.as.app X ≫ trailing.hom.as.app X =
      (actualLiftForwardSwallowtailComponentInterchanger (W := W) A
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
  -- The generic `trans` proof avoids comparing the two enormous
  -- actual-lift hom-category expressions at the conclusion.
  exact Generic.fiveStage_hom_app_of_iso_eq_and_component
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
    hleft leading hmiddle trailing hright
    (actualLiftForwardSwallowtailGlobalIso (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel))
    hIso X
      (show (sourceMapCompPathV578 (W := W) A
          (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel)).app X =
        (sourceMapCompPathV578 (W := W) A
          (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel)).app X from rfl)
      (show (sourcePostCounitPath (actualLiftDatumV579 (W := W) A
          (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel))).app X =
        (sourcePostCounitPath (actualLiftDatumV579 (W := W) A
          (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel))).app X from rfl)
      (show (sourcePreCounitPath (actualLiftDatumV579 (W := W) A
          (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel))).app X =
        (sourcePreCounitPath (actualLiftDatumV579 (W := W) A
          (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel))).app X from rfl)
    (actualLiftForwardSwallowtailComponentInterchanger (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) X).hom
    (by
      simp only [eqToHom_refl, Category.id_comp, Category.comp_id]
      exact hcanonical)


#print axioms Generic.eqToIso_inv_app_of_app_eq
#print axioms Generic.fiveStage_hom_app
#print axioms Generic.fiveStage_hom_app_of_iso_eq
#print axioms Generic.fiveStage_hom_app_of_iso_eq_and_component
#print axioms actualLiftForwardSwallowtailGlobalIso_hom_app

end

end KUOS.DependentOriginationForwardSwallowtailGlobalComponentAgreementV5_85
