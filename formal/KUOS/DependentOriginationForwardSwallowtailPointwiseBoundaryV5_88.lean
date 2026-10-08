import KUOS.DependentOriginationForwardCanonicalNaturalityV5_87

namespace KUOS.DependentOriginationForwardSwallowtailPointwiseBoundaryV5_88

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans

open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58
open KUOS.DependentOriginationBiadjunctionTriangulatorHorizontalPastesV5_64.Generic.IncoherentBiadjunctionDatum
open KUOS.DependentOriginationForwardSwallowtailPredicateV5_65
open KUOS.DependentOriginationForwardSwallowtailPredicateV5_65.Generic.IncoherentBiadjunctionDatum
open KUOS.DependentOriginationForwardSwallowtailModificationObstructionV5_70
open KUOS.DependentOriginationForwardSwallowtailComponentInterchangerV5_68
open KUOS.DependentOriginationGlobalForwardSwallowtailInterchangerV5_83
open KUOS.DependentOriginationForwardCanonicalNaturalityV5_87

set_option autoImplicit false
set_option maxHeartbeats 300000
noncomputable section

/-!
# Exact pointwise boundary of the original forward swallowtail law (v5.88)

v5.87 proves that the original four-cell family is modification-natural,
and gives a canonical Iso identical to the v5.83 global Iso.

The remaining v5.65 swallowtail *equation* is not inferred from this:
its triangulator side is the left-whiskering of the stored horizontal
paste. This file identifies the exact residual equation at each object
and proves equivalence with the native global-Iso predicate. No
triangulator or extra coherence axiom is chosen.
-/

universe u v uH vH uW uP

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-- Use the exact native v5.83/v5.87 StrongTrans hom-category. -/
local instance forwardSwallowtailHomCategoryV588 :
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

/-- The triangulator side at X is *exactly* the old unit component
whiskering the original source horizontal paste from v5.64. -/
theorem actualLiftForwardTriangulatorPaste_hom_app
    (X : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    (forwardTriangulatorPaste
      (actualLiftForwardSwallowtailDatum (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel))).hom.as.app X =
    ((actualLiftForwardSwallowtailDatum (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).base.unit.app X) ◁
      (sourceHorizontalPaste
        (actualLiftForwardSwallowtailDatum (W := W) A
          (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel))).hom.as.app X := by
  simp only [forwardTriangulatorPaste, Bicategory.whiskerLeftIso_hom,
    Pseudofunctor.StrongTrans.whiskerLeft_as_app]

/-- The *remaining* source-side forward swallowtail condition, expressed
without any equality transports or an abstract global modification:
four original v5.68 cells against the v5.64 horizontal triangulator paste. -/
def ActualLiftForwardSwallowtailPointwiseAgreement : Prop :=
  ∀ X : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel,
    (actualLiftForwardSwallowtailComponentInterchanger (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) X).hom =
    ((actualLiftForwardSwallowtailDatum (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).base.unit.app X) ◁
      (sourceHorizontalPaste
        (actualLiftForwardSwallowtailDatum (W := W) A
          (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel))).hom.as.app X

/-- The original v5.65 global forward swallowtail law is logically
equivalent to the displayed pointwise comparison, because the original
four-cell components are already modification-natural (v5.87). -/
theorem actualLiftForwardSwallowtailPredicate_iff_pointwise :
    actualLiftForwardSwallowtailPredicate (W := W) A
      (actualLiftForwardSwallowtailCanonicalIso (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)) ↔
    ActualLiftForwardSwallowtailPointwiseAgreement (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) := by
  constructor
  · intro h X
    change
      actualLiftForwardSwallowtailCanonicalIso (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) =
      forwardTriangulatorPaste
        (actualLiftForwardSwallowtailDatum (W := W) A
          (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel)) at h
    have hApp := congrArg
      (fun e : ActualLiftForwardSwallowtailInterchanger (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) =>
        e.hom.as.app X) h
    rw [actualLiftForwardSwallowtailInterchangerOfNaturality_hom_app
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)
      (actualLiftForwardSwallowtailOriginalNaturality (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)) X] at hApp
    rw [actualLiftForwardTriangulatorPaste_hom_app (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) X] at hApp
    exact hApp
  · intro h
    change
      actualLiftForwardSwallowtailCanonicalIso (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) =
      forwardTriangulatorPaste
        (actualLiftForwardSwallowtailDatum (W := W) A
          (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel))
    apply Iso.ext
    apply Pseudofunctor.StrongTrans.homCategory.ext
    intro X
    calc
      (actualLiftForwardSwallowtailCanonicalIso (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)).hom.as.app X =
        (actualLiftForwardSwallowtailComponentInterchanger (W := W) A
          (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel) X).hom :=
        actualLiftForwardSwallowtailInterchangerOfNaturality_hom_app
          (W := W) A
          (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel)
          (actualLiftForwardSwallowtailOriginalNaturality (W := W) A
            (WorldLabel := WorldLabel)
            (PresentationLabel := PresentationLabel)) X
      _ = ((actualLiftForwardSwallowtailDatum (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)).base.unit.app X) ◁
          (sourceHorizontalPaste
            (actualLiftForwardSwallowtailDatum (W := W) A
              (WorldLabel := WorldLabel)
              (PresentationLabel := PresentationLabel))).hom.as.app X := h X
      _ = (forwardTriangulatorPaste
        (actualLiftForwardSwallowtailDatum (W := W) A
          (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel))).hom.as.app X :=
        (actualLiftForwardTriangulatorPaste_hom_app (W := W) A
          (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel) X).symm

/-- Same obstruction measured using the exact v5.83 global Iso, by
v5.87's equality between the canonical and global native Iso. -/
theorem actualLiftForwardGlobalPredicate_iff_pointwise :
    actualLiftForwardSwallowtailPredicate (W := W) A
      (actualLiftForwardSwallowtailGlobalIso (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)) ↔
    ActualLiftForwardSwallowtailPointwiseAgreement (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) := by
  rw [← actualLiftForwardSwallowtailCanonicalIso_eq_global (W := W) A
    (WorldLabel := WorldLabel)
    (PresentationLabel := PresentationLabel)]
  exact actualLiftForwardSwallowtailPredicate_iff_pointwise (W := W) A
    (WorldLabel := WorldLabel)
    (PresentationLabel := PresentationLabel)

#print axioms actualLiftForwardTriangulatorPaste_hom_app
#print axioms ActualLiftForwardSwallowtailPointwiseAgreement
#print axioms actualLiftForwardSwallowtailPredicate_iff_pointwise
#print axioms actualLiftForwardGlobalPredicate_iff_pointwise

end

end KUOS.DependentOriginationForwardSwallowtailPointwiseBoundaryV5_88
