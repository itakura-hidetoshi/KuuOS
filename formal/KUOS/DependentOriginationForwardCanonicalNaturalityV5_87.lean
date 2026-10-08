import KUOS.DependentOriginationForwardSwallowtailGlobalComponentAgreementV5_86

namespace KUOS.DependentOriginationForwardCanonicalNaturalityV5_87

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans

open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58
open KUOS.DependentOriginationForwardSwallowtailPredicateV5_65
open KUOS.DependentOriginationForwardSwallowtailModificationObstructionV5_70
open KUOS.DependentOriginationForwardSwallowtailComponentInterchangerV5_68
open KUOS.DependentOriginationGlobalForwardSwallowtailInterchangerV5_83
open KUOS.DependentOriginationForwardSwallowtailGlobalComponentAgreementV5_86

set_option autoImplicit false
set_option maxHeartbeats 300000
noncomputable section

/-!
# Original forward four-cell modification naturality (v5.87)

The v5.83 global native Iso has a genuine modification naturality field.
The theorem v5.86 proves that *its existing object components* are precisely
the unchanged original v5.68 four-cell interchangers. Transport the native
naturality field across this proved component identity to discharge v5.70's
original named obstruction, with no newly chosen coherence or strictification.

The resulting original-family isoMk is identified with the same v5.83 global
Iso using the pinned mathlib StrongTrans.homCategory.ext.

The separate forward/reverse swallowtail equations remain unproved.
-/

universe u v uH vH uW uP

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-- The same native hom-category as the already proved v5.83 Iso. -/
local instance forwardSwallowtailHomCategoryV587 :
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

/-- The untouched v5.68 original forward four-cell family obeys exactly
the v5.70 modification naturality equation, as a consequence of the
native v5.83 Iso and the proven v5.86 component equality. -/
theorem actualLiftForwardSwallowtailOriginalNaturality :
    ActualLiftForwardSwallowtailModificationNaturality (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) := by
  intro X Y f
  have hNatural :=
    (actualLiftForwardSwallowtailGlobalIso (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).hom.as.naturality f
  have hApp :=
    actualLiftGlobalCanonicalComponentAgreement (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)
  rw [hApp Y, hApp X] at hNatural
  exact hNatural

/-- v5.70's original isoMk construction is now populated by proved
naturality, rather than an additional assumption. -/
def actualLiftForwardSwallowtailCanonicalIso :
    ActualLiftForwardSwallowtailInterchanger (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) :=
  actualLiftForwardSwallowtailInterchangerOfNaturality (W := W) A
    (WorldLabel := WorldLabel)
    (PresentationLabel := PresentationLabel)
    (actualLiftForwardSwallowtailOriginalNaturality (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel))

/-- The originally assembled v5.70 isoMk and the v5.83 global Iso are
the same native modification: the component equality v5.86 and mathlib's
StrongTrans hom-category extensionality determine the entire hom. -/
theorem actualLiftForwardSwallowtailCanonicalIso_eq_global :
    actualLiftForwardSwallowtailCanonicalIso (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) =
    actualLiftForwardSwallowtailGlobalIso (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) := by
  apply Iso.ext
  apply Pseudofunctor.StrongTrans.homCategory.ext
  intro X
  calc
    (actualLiftForwardSwallowtailCanonicalIso (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).hom.as.app X =
      (actualLiftForwardSwallowtailComponentInterchanger
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) X).hom :=
      actualLiftForwardSwallowtailInterchangerOfNaturality_hom_app
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)
        (actualLiftForwardSwallowtailOriginalNaturality (W := W) A
          (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel)) X
    _ = (actualLiftForwardSwallowtailGlobalIso (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).hom.as.app X :=
      (actualLiftGlobalCanonicalComponentAgreement (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) X).symm

#print axioms actualLiftForwardSwallowtailOriginalNaturality
#print axioms actualLiftForwardSwallowtailCanonicalIso
#print axioms actualLiftForwardSwallowtailCanonicalIso_eq_global

end

end KUOS.DependentOriginationForwardCanonicalNaturalityV5_87
