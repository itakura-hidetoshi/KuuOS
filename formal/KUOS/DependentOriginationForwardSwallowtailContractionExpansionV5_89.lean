import KUOS.DependentOriginationForwardSwallowtailPointwiseBoundaryV5_88

namespace KUOS.DependentOriginationForwardSwallowtailContractionExpansionV5_89

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans

open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePseudofunctorV5_48
open KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58
open KUOS.DependentOriginationExactLiftableActualLiftTriangleComponentsV5_51
open KUOS.DependentOriginationExactLiftableActualLiftIncoherentBiadjunctionV5_59.Generic
open KUOS.DependentOriginationBiadjunctionTriangulatorHorizontalPastesV5_64.Generic.IncoherentBiadjunctionDatum
open KUOS.DependentOriginationForwardSwallowtailPredicateV5_65.Generic.IncoherentBiadjunctionDatum
open KUOS.DependentOriginationForwardSwallowtailNativeBoundaryV5_79

set_option autoImplicit false
set_option maxHeartbeats 300000
noncomputable section

/-!
# Expand the genuine source triangulator contractions (v5.89)

The v5.88 pointwise obstruction is not discharged here.  This file
normalizes its right-hand side into the two original triangle contractions
and the non-strict quasi-inverse's mapId cell.

The source-forward contraction has an additional G.mapId because
postcomposition by G does not preserve the identity StrongTrans strictly.
The source-reverse contraction is the original reverse contraction
precomposed by F, with no independent comparison choice.
-/

namespace Generic

universe uB vB wB uC vC wC

variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]
variable (D : IncoherentBiadjunctionDatum B C)

local instance roundtripHomCategoryV589 :
    Category (Pseudofunctor.StrongTrans (sourceRoundtrip D) (sourceRoundtrip D)) :=
  Pseudofunctor.StrongTrans.homCategory
    (B := B) (C := B)
    (F := sourceRoundtrip D) (G := sourceRoundtrip D)

/-! The forward paste is a modification in the Id-to-roundtrip hom
category, *not* in the endomorphism hom category above.  At this generic
bicategory/universe boundary the scoped Category instance cannot be recovered
from the overloaded Iso projection.  Supply Mathlib's exact existing
homCategory instance, as in v5.65 and v5.88; no new structure is chosen. -/
local instance forwardSwallowtailHomCategoryV589 :
    Category
      (Pseudofunctor.StrongTrans
        (Pseudofunctor.id B) (sourceRoundtrip D)) :=
  Pseudofunctor.StrongTrans.homCategory
    (B := B) (C := B)
    (F := Pseudofunctor.id B) (G := sourceRoundtrip D)

/-- The horizontal paste is *exactly* mapped forward contraction,
followed by the native non-strict G.mapId, followed by the inverse
of the original reverse contraction at F(X). -/
theorem sourceHorizontalPaste_hom_app (X : B) :
    (sourceHorizontalPaste D).hom.as.app X =
      (D.base.quasiInverse.map₂
          ((D.triangulators.forward.contraction).hom.as.app X) ≫
        (D.base.quasiInverse.mapId (D.base.whitehead.forward.obj X)).hom) ≫
      (D.triangulators.reverse.contraction).inv.as.app
        (D.base.whitehead.forward.obj X) := by
  rfl

/-- The full right-hand side of the forward swallowtail equation, before
specializing the original F, G, unit and counit. -/
theorem forwardTriangulatorPaste_hom_app (X : B) :
    (forwardTriangulatorPaste D).hom.as.app X =
      D.base.unit.app X ◁
        ((D.base.quasiInverse.map₂
              ((D.triangulators.forward.contraction).hom.as.app X) ≫
            (D.base.quasiInverse.mapId (D.base.whitehead.forward.obj X)).hom) ≫
          (D.triangulators.reverse.contraction).inv.as.app
            (D.base.whitehead.forward.obj X)) := by
  change
    D.base.unit.app X ◁ (sourceHorizontalPaste D).hom.as.app X =
      D.base.unit.app X ◁
        ((D.base.quasiInverse.map₂
              ((D.triangulators.forward.contraction).hom.as.app X) ≫
            (D.base.quasiInverse.mapId (D.base.whitehead.forward.obj X)).hom) ≫
          (D.triangulators.reverse.contraction).inv.as.app
            (D.base.whitehead.forward.obj X))
  exact congrArg
    (fun m => D.base.unit.app X ◁ m)
    (sourceHorizontalPaste_hom_app D X)

end Generic

universe u v uH vH uW uP

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

local instance roundtripHomCategoryV589 :
    Category
      (Pseudofunctor.StrongTrans
        (sourceRoundtrip
          (actualLiftDatumV579
            (W := W) A (WorldLabel := WorldLabel)
            (PresentationLabel := PresentationLabel)))
        (sourceRoundtrip
          (actualLiftDatumV579
            (W := W) A (WorldLabel := WorldLabel)
            (PresentationLabel := PresentationLabel)))) :=
  Pseudofunctor.StrongTrans.homCategory
    (B := ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)
    (C := ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)
    (F := sourceRoundtrip
      (actualLiftDatumV579
        (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)))
    (G := sourceRoundtrip
      (actualLiftDatumV579
        (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)))

/-- Concrete right-hand side, with the *original* forward counit and
reverse unit contractions and with the non-strict G.mapId retained. -/
theorem actualLiftSourceHorizontalPaste_hom_app_expanded
    (X : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    (sourceHorizontalPaste
      (actualLiftDatumV579
        (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel))).hom.as.app X =
      ((actualLiftQuasiInversePseudofunctor (W := W) A).map₂
          ((actualLiftForwardTriangleIso (W := W) A X).hom) ≫
        ((actualLiftQuasiInversePseudofunctor (W := W) A).mapId
          ((actualLiftForwardPseudofunctor
            (W := W) A WorldLabel PresentationLabel).obj X)).hom) ≫
      (actualLiftQuasiInverseTriangleIso (W := W) A
        ((actualLiftForwardPseudofunctor
          (W := W) A WorldLabel PresentationLabel).obj X)).inv := by
  exact Generic.sourceHorizontalPaste_hom_app
    (actualLiftDatumV579
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) X

#print axioms Generic.sourceHorizontalPaste_hom_app
#print axioms Generic.forwardTriangulatorPaste_hom_app
#print axioms actualLiftSourceHorizontalPaste_hom_app_expanded

end

end KUOS.DependentOriginationForwardSwallowtailContractionExpansionV5_89
