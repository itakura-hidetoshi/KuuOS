import KUOS.DependentOriginationActualLiftForwardMapCompGlobalV5_78

namespace KUOS.DependentOriginationForwardSwallowtailNativeBoundaryV5_79

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans

open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationForwardSwallowtailPredicateV5_65
open KUOS.DependentOriginationForwardSwallowtailModificationObstructionV5_70
open KUOS.DependentOriginationActualLiftForwardMapCompGlobalV5_78
open KUOS.DependentOriginationReassociatedSourceCounitInterchangerV5_77.Generic.IncoherentBiadjunctionDatum

set_option autoImplicit false
set_option maxHeartbeats 1000000
noncomputable section

/-!
# Native forward-swallowtail boundary compatibility v5.79

The v5.78 first mapComp modification and the v5.77 last-three-cells
modification are globally natural separately. The remaining interface is
the identity/coherence between their middle StrongTrans presentations,
followed by compatibility of the v5.77 right endpoint with v5.65.

This file tests both endpoints against the unchanged actual-lift datum.
The 1-cell component equalities hold without strictification. Whole-record
StrongTrans equalities, which also include pseudonaturality isomorphisms,
are checked separately and never inferred from components alone.
-/

universe u v uH vH uW uP
variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

abbrev actualLiftDatumV579 :=
  actualLiftForwardSwallowtailDatum
    (W := W) A
    (WorldLabel := WorldLabel)
    (PresentationLabel := PresentationLabel)


/- A fully general extensionality rule for StrongTrans records.
Unlike modification extensionality, equality of strong transformations
requires both app-fields and all naturality 2-isomorphisms. -/
namespace Generic

universe uB vB wB uC vC wC

variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]
variable {F G : Pseudofunctor B C}

theorem strongTrans_eq_of_app_and_naturality
    (sigma tau : Pseudofunctor.StrongTrans F G)
    (happ : ∀ X, sigma.app X = tau.app X)
    (hnat : ∀ {X Y : B} (f : X ⟶ Y),
      HEq (sigma.naturality f).hom (tau.naturality f).hom) :
    sigma = tau := by
  cases sigma with
  | mk sa sn snn sid scomp =>
    cases tau with
    | mk ta tn tnn tid tcomp =>
      have hApp : sa = ta := by
        funext X
        exact happ X
      cases hApp
      have hNat : @sn = @tn := by
        funext X Y f
        apply Iso.ext
        exact eq_of_heq (hnat f)
      cases hNat
      rfl

end Generic

/-- The middle path agrees objectwise with the native source-side
eta/post-unit/counit path. -/
@[simp] theorem middleComponent_eq (X :
    sourceV578 (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) :
    (targetMapCompPathV578 (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).app X =
    (sourcePostCounitPath
      (actualLiftDatumV579 (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel))).app X := by
  rfl

/-- The right path agrees objectwise with the original
v5.65 reverse-triangle boundary, including the unchanged counit. -/
@[simp] theorem rightComponent_eq (X :
    sourceV578 (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) :
    (sourcePreCounitPath
      (actualLiftDatumV579 (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel))).app X =
    (actualLiftForwardSwallowtailRightV70
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).app X := by
  rfl

/-!
## The genuine middle naturality boundary

Objectwise equality of two StrongTrans values does not imply equality of
the entire records. Their pseudonaturality isomorphisms can have different
compositions even when their objectwise 1-morphisms are definitionally
identical. Accordingly the original attempt to close the next goal by rfl
was not valid: a larger heartbeat budget establishes that the two records
are not definitionally equal.

For the full comparison we must prove that the existing naturality 2-cells
coincide, not replace them or postulate any extra coherence.
-/

/-- Exact remaining 2-cell naturality condition for the middle boundary.
HEq avoids prematurely transporting along an app-field equality and keeps
both actual StrongTrans naturality fields visible. -/
def MiddleNaturalityAgreement : Prop :=
  ∀ {X Y :
      ActualLiftSource.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel}
    (f : X ⟶ Y),
    HEq
      (((targetMapCompPathV578 (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)).naturality f).hom)
      (((sourcePostCounitPath
        (actualLiftDatumV579 (W := W) A
          (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel))).naturality f).hom)

/-- The middle transformation equality follows from object components
(which were already proved) together with precisely the missing naturality
2-cell agreement. No datum or mathematical assumption is added. -/
theorem middleStrongTrans_eq_of_naturality
    (h : MiddleNaturalityAgreement (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) :
    targetMapCompPathV578 (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) =
    sourcePostCounitPath
      (actualLiftDatumV579 (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)) := by
  apply Generic.strongTrans_eq_of_app_and_naturality
  · intro X
    exact middleComponent_eq (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) X
  · intro X Y f
    exact h f

/-- Test the stronger right bridge, including all naturality data. -/
theorem rightStrongTrans_eq :
    sourcePreCounitPath
      (actualLiftDatumV579 (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)) =
    actualLiftForwardSwallowtailRightV70
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) := by
  rfl

#print axioms middleComponent_eq
#print axioms rightComponent_eq
#print axioms MiddleNaturalityAgreement
#print axioms middleStrongTrans_eq_of_naturality
#print axioms rightStrongTrans_eq

end

end KUOS.DependentOriginationForwardSwallowtailNativeBoundaryV5_79
