import KUOS.DependentOriginationForwardSwallowtailActualLiftDescentV5_93

namespace KUOS.DependentOriginationReverseSwallowtailTargetPasteExpansionV5_94

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans

open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58
open KUOS.DependentOriginationExactLiftableActualLiftTriangleComponentsV5_51
open KUOS.DependentOriginationExactLiftableActualLiftTargetCounitV5_49
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePseudofunctorV5_48
open KUOS.DependentOriginationBiadjunctionTriangulatorHorizontalPastesV5_64.Generic.IncoherentBiadjunctionDatum
open KUOS.DependentOriginationReverseSwallowtailPredicateV5_66.Generic.IncoherentBiadjunctionDatum
open KUOS.DependentOriginationReverseSwallowtailPredicateV5_66

set_option autoImplicit false
set_option maxHeartbeats 300000
noncomputable section

/-!
# Reverse swallowtail: genuine target-side contraction expansion (v5.94)

After the proved F3 forward swallowtail (v5.93), this isolates the
target/counit F4 boundary without claiming the missing counit-centered
interchanger.  As in the source expansion v5.89, both triangle contractions
and the non-strict pseudofunctor's mapId are retained *exactly*.

The target forward contraction is the original forward contraction
precomposed with G. The target reverse contraction is the original reverse
contraction postcomposed with F, followed by the native F.mapId comparator.
When reversing the latter iso, the order is F.mapId.inv before F.map₂
of the original inverse reverse contraction.

No alternative triangle modification, replacement pseudofunctor, or new
coherence axiom is introduced.
-/

namespace Generic

universe uB vB wB uC vC wC

variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]
variable (D : KUOS.DependentOriginationExactLiftableActualLiftIncoherentBiadjunctionV5_59.Generic.IncoherentBiadjunctionDatum B C)

local instance targetEndHomCategoryV594 :
    Category (Pseudofunctor.StrongTrans (targetRoundtrip D) (targetRoundtrip D)) :=
  Pseudofunctor.StrongTrans.homCategory
    (B := C) (C := C)
    (F := targetRoundtrip D) (G := targetRoundtrip D)

local instance targetToIdentityHomCategoryV594 :
    Category (Pseudofunctor.StrongTrans (targetRoundtrip D) (Pseudofunctor.id C)) :=
  Pseudofunctor.StrongTrans.homCategory
    (B := C) (C := C)
    (F := targetRoundtrip D) (G := Pseudofunctor.id C)

/-- Target horizontal paste is the original forward contraction at G(Y),
then the *inverse* F.mapId comparison, and then the mapped inverse of
the original reverse contraction. -/
theorem targetHorizontalPaste_hom_app (Y : C) :
    (targetHorizontalPaste D).hom.as.app Y =
      (D.triangulators.forward.contraction).hom.as.app (D.base.quasiInverse.obj Y) ≫
        ((D.base.whitehead.forward.mapId (D.base.quasiInverse.obj Y)).inv ≫
          D.base.whitehead.forward.map₂
            ((D.triangulators.reverse.contraction).inv.as.app Y)) := by
  rfl

/-- Right whiskering by the original counit keeps the genuine paste
component and its order; the counit is not replaced by an identity. -/
theorem reverseTriangulatorPaste_hom_app (Y : C) :
    (reverseTriangulatorPaste D).hom.as.app Y =
      ((D.triangulators.forward.contraction).hom.as.app
          (D.base.quasiInverse.obj Y) ≫
        ((D.base.whitehead.forward.mapId (D.base.quasiInverse.obj Y)).inv ≫
          D.base.whitehead.forward.map₂
            ((D.triangulators.reverse.contraction).inv.as.app Y))) ▷
        D.base.counit.app Y := by
  change
    (targetHorizontalPaste D).hom.as.app Y ▷ D.base.counit.app Y =
      ((D.triangulators.forward.contraction).hom.as.app
          (D.base.quasiInverse.obj Y) ≫
        ((D.base.whitehead.forward.mapId (D.base.quasiInverse.obj Y)).inv ≫
          D.base.whitehead.forward.map₂
            ((D.triangulators.reverse.contraction).inv.as.app Y))) ▷
        D.base.counit.app Y
  exact congrArg
    (fun m => m ▷ D.base.counit.app Y)
    (targetHorizontalPaste_hom_app D Y)

end Generic

universe u v uH vH uW uP

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-!
The generic v5.66 reverse modification belongs to the StrongTrans hom
category from the *target roundtrip* to the identity pseudofunctor.
Although the two generic instances above elaborate without difficulty,
they are not local instances for the particular six-universe actual-lift
type.  Supply the existing Mathlib homCategory at both concrete endpoints
before elaborating the projected Iso and its component.  No category or
coherence data are redefined here.
-/

local instance actualLiftTargetEndHomCategoryV594 :
    Category
      (Pseudofunctor.StrongTrans
        (targetRoundtrip
          (actualLiftReverseSwallowtailDatum
        (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)))
        (targetRoundtrip
          (actualLiftReverseSwallowtailDatum
        (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)))) :=
  Pseudofunctor.StrongTrans.homCategory
    (B := ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)
    (C := ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)
    (F := targetRoundtrip
      (actualLiftReverseSwallowtailDatum
        (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)))
    (G := targetRoundtrip
      (actualLiftReverseSwallowtailDatum
        (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)))

local instance actualLiftTargetToIdentityHomCategoryV594 :
    Category
      (Pseudofunctor.StrongTrans
        (targetRoundtrip
          (actualLiftReverseSwallowtailDatum
        (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)))
        (Pseudofunctor.id
          (ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel))) :=
  Pseudofunctor.StrongTrans.homCategory
    (B := ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)
    (C := ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)
    (F := targetRoundtrip
      (actualLiftReverseSwallowtailDatum
        (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)))
    (G := Pseudofunctor.id
      (ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel))

/-- The original actual-lift F4 triangulator boundary retains the original
forward/reverse contractions and exact F.mapId.  In this specific model F
is strict, but its mapId cell remains visible rather than silently erased. -/
theorem actualLiftReverseTriangulatorPaste_hom_app
    (Y : ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    (reverseTriangulatorPaste
      (actualLiftReverseSwallowtailDatum
        (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel))).hom.as.app Y =
      ((actualLiftForwardTriangleIso (W := W) A
          ((actualLiftQuasiInversePseudofunctor
            (W := W) A).obj Y)).hom ≫
        (((actualLiftForwardPseudofunctor
          (W := W) A WorldLabel PresentationLabel).mapId
            ((actualLiftQuasiInversePseudofunctor
              (W := W) A).obj Y)).inv ≫
          (actualLiftForwardPseudofunctor
            (W := W) A WorldLabel PresentationLabel).map₂
            ((actualLiftQuasiInverseTriangleIso
              (W := W) A Y).inv))) ▷
          (actualLiftTargetRoundtripCounit (W := W) A).app Y := by
  exact Generic.reverseTriangulatorPaste_hom_app
    (actualLiftReverseSwallowtailDatum
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) Y

#print axioms Generic.targetHorizontalPaste_hom_app
#print axioms Generic.reverseTriangulatorPaste_hom_app
#print axioms actualLiftReverseTriangulatorPaste_hom_app

end

end KUOS.DependentOriginationReverseSwallowtailTargetPasteExpansionV5_94
