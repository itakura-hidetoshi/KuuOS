import KUOS.DependentOriginationUnitSelfNaturalityExchangeV5_69

namespace KUOS.DependentOriginationForwardSwallowtailModificationObstructionV5_70

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans

open KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58
open KUOS.DependentOriginationForwardSwallowtailPredicateV5_65
open KUOS.DependentOriginationForwardSwallowtailPredicateV5_65.Generic.IncoherentBiadjunctionDatum
open KUOS.DependentOriginationBiadjunctionTriangulatorHorizontalPastesV5_64.Generic.IncoherentBiadjunctionDatum
open KUOS.DependentOriginationForwardSwallowtailComponentInterchangerV5_68
open KUOS.DependentOriginationUnitSelfNaturalityExchangeV5_69
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6

set_option autoImplicit false

noncomputable section

/-!
# Forward swallowtail modification obstruction v5.70

v5.68 constructs the canonical forward-swallowtail comparison at each object.
v5.69 isolates the native eta/eta exchange which is the substantive
non-structural identity expected to prove naturality of that component family.

This file records the exact remaining global obstruction and connects it to
Mathlib's native modification API.

For the unchanged actual-lift datum D, write

  L = forwardSwallowtailLeft D,
  R = forwardSwallowtailRight D,
  S = sourceRoundtrip D.

The v5.68 family sigma_X becomes a modification L ==> R exactly when

  Id.map f ◁ sigma_Y ; R.naturality(f)
    =
  L.naturality(f) ; sigma_X ▷ S.map f

for every f : X -> Y.

No inhabitant of this proposition is postulated.  If an inhabitant is later
proved, Mathlib's StrongTrans.isoMk packages the already invertible v5.68
components into the exact v5.65 ForwardSwallowtailInterchanger type.

Thus the boundary between pointwise coherence and global swallowtail
coherence is explicit and typed.
-/

universe u v uH vH uW uP

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

abbrev actualLiftForwardSwallowtailDatumV70 :=
  actualLiftForwardSwallowtailDatumV68
    (W := W) A
    (WorldLabel := WorldLabel)
    (PresentationLabel := PresentationLabel)

abbrev actualLiftForwardSwallowtailSourceV70 :=
  actualLiftForwardSwallowtailSourceV68
    (W := W) A
    (WorldLabel := WorldLabel)
    (PresentationLabel := PresentationLabel)

abbrev actualLiftForwardSwallowtailRoundtripV70 :=
  sourceRoundtrip
    (actualLiftForwardSwallowtailDatumV70
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel))

abbrev actualLiftForwardSwallowtailLeftV70 :=
  forwardSwallowtailLeft
    (actualLiftForwardSwallowtailDatumV70
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel))

abbrev actualLiftForwardSwallowtailRightV70 :=
  forwardSwallowtailRight
    (actualLiftForwardSwallowtailDatumV70
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel))

/-!
The source object type is written directly with all six universe levels in
this declaration header.  Under `set_option autoImplicit false`, Lean
elaborates binder types before using information from the body; routing the
binder through a local abbreviation leaves the hom-universe level
underconstrained here.  This is the same header-first issue already isolated
in v5.58.
-/

/-- Exact modification-naturality proposition for the v5.68 objectwise
interchanger family. -/
def ActualLiftForwardSwallowtailModificationNaturality : Prop :=
  ∀ {X Y :
      ActualLiftSource.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel}
    (f : X ⟶ Y),
    (Pseudofunctor.id
      (ActualLiftSource.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel)).map f ◁
        (actualLiftForwardSwallowtailComponentInterchanger
          (W := W) A
          (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel)
          Y).hom ≫
      ((actualLiftForwardSwallowtailRightV70
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)).naturality f).hom =
    ((actualLiftForwardSwallowtailLeftV70
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).naturality f).hom ≫
      (actualLiftForwardSwallowtailComponentInterchanger
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)
        X).hom ▷
        (actualLiftForwardSwallowtailRoundtripV70
          (W := W) A
          (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel)).map f

local instance actualLiftForwardSwallowtailHomCategoryV70 :
    Category
      (Pseudofunctor.StrongTrans
        (Pseudofunctor.id
          (ActualLiftSource.{u, v, uH, vH, uW, uP}
            (W := W) A WorldLabel PresentationLabel))
        (actualLiftForwardSwallowtailRoundtripV70
          (W := W) A
          (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel))) :=
  Pseudofunctor.StrongTrans.homCategory
    (B :=
      ActualLiftSource.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel)
    (C :=
      ActualLiftSource.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel)
    (F :=
      Pseudofunctor.id
        (actualLiftForwardSwallowtailSourceV70
          (W := W) A
          (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel)))
    (G :=
      actualLiftForwardSwallowtailRoundtripV70
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel))

/-- Package a proof of the exact v5.70 obstruction into the native
invertible-modification type required by v5.65.  No new component is chosen. -/
def actualLiftForwardSwallowtailInterchangerOfNaturality
    (h :
      ActualLiftForwardSwallowtailModificationNaturality
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)) :
    ActualLiftForwardSwallowtailInterchanger
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) :=
  Pseudofunctor.StrongTrans.isoMk
    (η :=
      actualLiftForwardSwallowtailLeftV70
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel))
    (θ :=
      actualLiftForwardSwallowtailRightV70
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel))
    (fun X =>
      actualLiftForwardSwallowtailComponentInterchanger
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)
        X)
    (by
      intro X Y f
      exact h f)

@[simp] theorem actualLiftForwardSwallowtailInterchangerOfNaturality_hom_app
    (h :
      ActualLiftForwardSwallowtailModificationNaturality
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel))
    (X :
      ActualLiftSource.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel) :
    (actualLiftForwardSwallowtailInterchangerOfNaturality
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)
      h).hom.as.app X =
      (actualLiftForwardSwallowtailComponentInterchanger
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)
        X).hom :=
  rfl

@[simp] theorem actualLiftForwardSwallowtailInterchangerOfNaturality_inv_app
    (h :
      ActualLiftForwardSwallowtailModificationNaturality
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel))
    (X :
      ActualLiftSource.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel) :
    (actualLiftForwardSwallowtailInterchangerOfNaturality
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)
      h).inv.as.app X =
      (actualLiftForwardSwallowtailComponentInterchanger
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)
        X).inv :=
  rfl

/-!
## Boundary after v5.70

The forward swallowtail has now been reduced to two explicit propositions:

1. v5.70 global modification naturality for the canonical v5.68 family;
2. after that is proved, the v5.65 equality between the resulting canonical
   interchanger and forwardTriangulatorPaste.

The immediate mathematical target is therefore precise: prove
ActualLiftForwardSwallowtailModificationNaturality by normalizing the
mapComp/associator/counit envelopes and applying the inverse eta/eta exchange
from v5.69.
-/

#print axioms ActualLiftForwardSwallowtailModificationNaturality
#print axioms actualLiftForwardSwallowtailInterchangerOfNaturality
#print axioms actualLiftForwardSwallowtailInterchangerOfNaturality_hom_app
#print axioms actualLiftForwardSwallowtailInterchangerOfNaturality_inv_app

end

end KUOS.DependentOriginationForwardSwallowtailModificationObstructionV5_70
