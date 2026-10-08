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
open KUOS.DependentOriginationForwardSwallowtailNativeBoundaryV5_79
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

/-- The triangulator-side horizontal paste lives in the *endomorphism*
hom category of the original roundtrip pseudofunctor, not in the
Id-to-roundtrip hom category used by the final forward Iso.
Both are the pinned mathlib hom-category; no new coherence data. -/
local instance roundtripHomCategoryV588 :
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

/-- The triangulator side at X is *exactly* the old unit component
whiskering the original source horizontal paste from v5.64. -/
theorem actualLiftForwardTriangulatorPaste_hom_app
    (X : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    (forwardTriangulatorPaste
      (actualLiftDatumV579 (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel))).hom.as.app X =
    ((actualLiftDatumV579 (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).base.unit.app X) ◁
      (sourceHorizontalPaste
        (actualLiftDatumV579 (W := W) A
          (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel))).hom.as.app X := by
  simp only [forwardTriangulatorPaste, Bicategory.whiskerLeftIso_hom,
    Pseudofunctor.StrongTrans.whiskerLeft_as_app]

/-- The original v5.70 isoMk has exactly the unchanged v5.68
four-cell component; keep this typed bridge separate from the enormous
global predicate so subsequent congruence does not unfold the Iso. -/
theorem actualLiftForwardCanonicalIso_hom_app
    (X : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    (actualLiftForwardSwallowtailCanonicalIso.{u, v, uH, uW, uP, vH}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).hom.as.app X =
    (actualLiftForwardSwallowtailComponentInterchanger.{u, v, uH, uW, uP, vH}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) X).hom :=
  actualLiftForwardSwallowtailInterchangerOfNaturality_hom_app.{u, v, uH, vH, uW, uP}
    (W := W) A (WorldLabel := WorldLabel)
    (PresentationLabel := PresentationLabel)
    (actualLiftForwardSwallowtailOriginalNaturality.{u, v, uH, uW, uP, vH}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) X

/-- The *remaining* source-side forward swallowtail condition, expressed
without any equality transports or an abstract global modification:
four original v5.68 cells against the v5.64 horizontal triangulator paste. -/
def ActualLiftForwardSwallowtailPointwiseAgreement : Prop :=
  ∀ X : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel,
    (actualLiftForwardSwallowtailComponentInterchanger.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) X).hom =
    ((actualLiftDatumV579 (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).base.unit.app X) ◁
      (sourceHorizontalPaste
        (actualLiftDatumV579 (W := W) A
          (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel))).hom.as.app X

/-- The original v5.65 global forward swallowtail law is logically
equivalent to the displayed pointwise comparison, because the original
four-cell components are already modification-natural (v5.87). -/
theorem actualLiftForwardSwallowtailPredicate_iff_pointwise :
    actualLiftForwardSwallowtailPredicate.{u, v, uH, uW, uP, vH} (W := W) A
      (actualLiftForwardSwallowtailCanonicalIso.{u, v, uH, uW, uP, vH} (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)) ↔
    ActualLiftForwardSwallowtailPointwiseAgreement.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) := by
  constructor
  · intro h X
    change
      actualLiftForwardSwallowtailCanonicalIso.{u, v, uH, uW, uP, vH} (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) =
      forwardTriangulatorPaste
        (actualLiftDatumV579 (W := W) A
          (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel)) at h
    have hApp := congrArg
      (fun e : ActualLiftForwardSwallowtailInterchanger.{u, v, uH, uW, uP, vH}
        (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) =>
        e.hom.as.app X) h
    -- Beta-reduce the *small* component projection, not the actual-lift
    -- Iso records. A named isoMk is not a rewrite-pattern occurrence.
    change
      (actualLiftForwardSwallowtailCanonicalIso.{u, v, uH, uW, uP, vH}
        (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)).hom.as.app X =
      (forwardTriangulatorPaste
        (actualLiftDatumV579 (W := W) A
          (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel))).hom.as.app X at hApp
    exact
      (actualLiftForwardCanonicalIso_hom_app (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) X).symm.trans
      (hApp.trans
        (actualLiftForwardTriangulatorPaste_hom_app (W := W) A
          (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel) X))
  · intro h
    change
      actualLiftForwardSwallowtailCanonicalIso.{u, v, uH, uW, uP, vH} (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) =
      forwardTriangulatorPaste
        (actualLiftDatumV579 (W := W) A
          (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel))
    apply Iso.ext
    apply Pseudofunctor.StrongTrans.homCategory.ext
    intro X
    -- Compose three *typed* component equalities. Avoid dependent calc
    -- elaboration trying to infer a fresh hom-universe for the middle step.
    exact
      ((actualLiftForwardCanonicalIso_hom_app (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) X).trans (h X)).trans
        (actualLiftForwardTriangulatorPaste_hom_app (W := W) A
          (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel) X).symm

/-- Same obstruction measured using the exact v5.83 global Iso, by
v5.87's equality between the canonical and global native Iso. -/
theorem actualLiftForwardGlobalPredicate_iff_pointwise :
    actualLiftForwardSwallowtailPredicate.{u, v, uH, uW, uP, vH} (W := W) A
      (actualLiftForwardSwallowtailGlobalIso.{u, v, uH, uW, uP, vH} (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)) ↔
    ActualLiftForwardSwallowtailPointwiseAgreement.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) := by
  rw [← actualLiftForwardSwallowtailCanonicalIso_eq_global.{u, v, uH, uW, uP, vH} (W := W) A
    (WorldLabel := WorldLabel)
    (PresentationLabel := PresentationLabel)]
  exact actualLiftForwardSwallowtailPredicate_iff_pointwise (W := W) A
    (WorldLabel := WorldLabel)
    (PresentationLabel := PresentationLabel)

#print axioms actualLiftForwardTriangulatorPaste_hom_app
#print axioms actualLiftForwardCanonicalIso_hom_app
#print axioms ActualLiftForwardSwallowtailPointwiseAgreement
#print axioms actualLiftForwardSwallowtailPredicate_iff_pointwise
#print axioms actualLiftForwardGlobalPredicate_iff_pointwise

end

end KUOS.DependentOriginationForwardSwallowtailPointwiseBoundaryV5_88
