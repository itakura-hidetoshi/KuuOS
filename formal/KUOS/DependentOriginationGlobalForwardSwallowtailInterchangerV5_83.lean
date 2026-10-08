import KUOS.DependentOriginationForwardMiddleNaturalityPasteV5_82

namespace KUOS.DependentOriginationGlobalForwardSwallowtailInterchangerV5_83

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans

open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58
open KUOS.DependentOriginationForwardSwallowtailPredicateV5_65
open KUOS.DependentOriginationForwardSwallowtailModificationObstructionV5_70
open KUOS.DependentOriginationActualLiftForwardMapCompGlobalV5_78
open KUOS.DependentOriginationForwardSwallowtailNativeBoundaryV5_79
open KUOS.DependentOriginationForwardMiddleNaturalityPasteV5_82
open KUOS.DependentOriginationReassociatedSourceCounitInterchangerV5_77.Generic.IncoherentBiadjunctionDatum

set_option autoImplicit false
noncomputable section

/-!
# Global forward-swallowtail interchanger as a native modification (v5.83)

All required *global* naturality constituents now exist:

* v5.78: the leading G.mapComp as an invertible modification;
* v5.82: the proven exact middle StrongTrans equality, including all
  naturality 2-isomorphisms (not merely equality of app components);
* v5.77: the original unit/eta/counit interchanger with both associators;
* v5.79: equality of the final native StrongTrans with the v5.65 endpoint.

Compose these with equality transports only at the proved StrongTrans
equalities. The result is a canonical global invertible modification between
the precise v5.65 forward-swallowtail boundary values, preserving the
original F, G, eta, eps and every non-strict mapId/mapComp comparison.

This construction is not yet the v5.70 canonical interchanger: its component
must still be shown to equal the exact v5.68 four-cell paste. Nor is the
v5.65 swallowtail equation claimed or assumed.
-/

universe u v uH vH uW uP

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-- Use the exact pinned mathlib hom-category for StrongTrans of the
original source bicategory, not an inferred change of universe. -/
local instance forwardSwallowtailHomCategoryV583 :
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

/-- The actual native global iso is assembled from the original four
coherence cells. The endpoint and middle `eqToIso` adapters only transport
along *proved* whole-StrongTrans equalities; no coherence 2-cell is postulated.

The composition is oriented left-to-right, with explicit intermediate boundaries:

* `forwardSwallowtailLeft` to `sourceMapCompPathV578` (symmetric equality);
* `sourceMapCompPathV578` to `targetMapCompPathV578` (global `G.mapComp`);
* `targetMapCompPathV578` to `sourcePostCounitPath` (v5.82 naturality);
* `sourcePostCounitPath` to `sourcePreCounitPath` (native v5.77 modification);
* `sourcePreCounitPath` to `forwardSwallowtailRight` (v5.79 equality).

This documents the whole-record equality boundaries separately from the
canonical v5.68 component-comparison theorem, which remains a later goal. -/
def actualLiftForwardSwallowtailGlobalIso :
    ActualLiftForwardSwallowtailInterchanger (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) :=
  (eqToIso (sourceMapCompPathV578_eq_forwardSwallowtailLeft
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel))).symm ≪≫
    (forwardMapCompGlobalIso (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) ≪≫
    (eqToIso (middleStrongTrans_eq (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel))) ≪≫
    (sourceCounitReassociatedInterchangerIso
      (actualLiftDatumV579 (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel))) ≪≫
    (eqToIso (rightStrongTrans_eq (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)))

#print axioms actualLiftForwardSwallowtailGlobalIso

end

end KUOS.DependentOriginationGlobalForwardSwallowtailInterchangerV5_83
