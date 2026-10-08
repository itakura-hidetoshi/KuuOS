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

/-- Test the stronger middle bridge, including all naturality data. -/
theorem middleStrongTrans_eq :
    targetMapCompPathV578 (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) =
    sourcePostCounitPath
      (actualLiftDatumV579 (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)) := by
  rfl

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
#print axioms middleStrongTrans_eq
#print axioms rightStrongTrans_eq

end

end KUOS.DependentOriginationForwardSwallowtailNativeBoundaryV5_79
