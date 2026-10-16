import KUOS.DependentOriginationForwardSwallowtailComponentInterchangerV5_68

namespace KUOS.DependentOriginationUnitSelfNaturalityExchangeV5_69

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans

open KUOS.DependentOriginationExactLiftableActualLiftIncoherentBiadjunctionV5_59
open KUOS.DependentOriginationExactLiftableActualLiftIncoherentBiadjunctionV5_59.Generic
open KUOS.DependentOriginationBiadjunctionTriangulatorHorizontalPastesV5_64.Generic.IncoherentBiadjunctionDatum
open KUOS.DependentOriginationForwardSwallowtailPredicateV5_65
open KUOS.DependentOriginationForwardSwallowtailComponentInterchangerV5_68
open KUOS.DependentOriginationUnitSelfNaturalityCoreV5_67
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6

set_option autoImplicit false

noncomputable section

/-!
# Unit self-naturality exchange v5.69

v5.67 isolates the eta/eta naturality core and v5.68 transports that core to
the pointwise forward-swallowtail boundary.

The next global obstruction is modification naturality.  Its irreducible
non-structural equation is already one of the native StrongTrans laws:
apply eta.naturality_naturality to the 2-cell eta.naturality(f).hom itself.

For eta : Id_B => R and f : X -> Y, eta.naturality(f).hom is a 2-cell

  Id.map f ; eta_Y  ==>  eta_X ; R.map f.

Naturality of eta with respect to this 2-cell compares the two ways of
evaluating eta again on those composite 1-cells.  This is exactly the
eta/eta exchange which later remains after the associator, mapComp and
counit-whiskering envelopes of v5.68 are normalized.

No swallowtail equation is proved here.  This file exposes the native exchange
in both orientations so the v5.68 component family can be upgraded to a
modification without hiding the substantive StrongTrans coherence step.
-/

namespace Generic

universe uB vB wB uC vC wC

variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]

namespace IncoherentBiadjunctionDatum

variable (D : IncoherentBiadjunctionDatum B C)

/-- The eta/eta exchange obtained by applying 2-cell naturality of the stored
unit to the forward naturality 2-cell of that same unit. -/
theorem unitSelfNaturalityExchange
    {X Y : B} (f : X ⟶ Y) :
    (Pseudofunctor.id B).map₂ (D.base.unit.naturality f).hom ▷
          D.base.unit.app ((sourceRoundtrip D).obj Y) ≫
        (D.base.unit.naturality
          (D.base.unit.app X ≫ (sourceRoundtrip D).map f)).hom =
      (D.base.unit.naturality
        ((Pseudofunctor.id B).map f ≫ D.base.unit.app Y)).hom ≫
        D.base.unit.app X ◁
          (sourceRoundtrip D).map₂ (D.base.unit.naturality f).hom :=
  D.base.unit.naturality_naturality (D.base.unit.naturality f).hom

/-- The same native eta/eta exchange in the inverse orientation.  This is the
orientation used when the v5.67 core appears inverted in the v5.68 component
interchanger. -/
theorem unitSelfNaturalityExchangeInv
    {X Y : B} (f : X ⟶ Y) :
    (Pseudofunctor.id B).map₂ (D.base.unit.naturality f).inv ▷
          D.base.unit.app ((sourceRoundtrip D).obj Y) ≫
        (D.base.unit.naturality
          ((Pseudofunctor.id B).map f ≫ D.base.unit.app Y)).hom =
      (D.base.unit.naturality
        (D.base.unit.app X ≫ (sourceRoundtrip D).map f)).hom ≫
        D.base.unit.app X ◁
          (sourceRoundtrip D).map₂ (D.base.unit.naturality f).inv :=
  D.base.unit.naturality_naturality (D.base.unit.naturality f).inv

end IncoherentBiadjunctionDatum

end Generic

open Generic

universe u v uH vH uW uP

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-- Actual-lift specialization of the forward eta/eta exchange. -/
theorem actualLiftUnitSelfNaturalityExchange
    {X Y :
      actualLiftForwardSwallowtailSourceV68
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)}
    (f : X ⟶ Y) :
    (Pseudofunctor.id
      (actualLiftForwardSwallowtailSourceV68
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel))).map₂
        ((actualLiftForwardSwallowtailDatumV68
          (W := W) A
          (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel)).base.unit.naturality f).hom ▷
      (actualLiftForwardSwallowtailDatumV68
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)).base.unit.app
          ((sourceRoundtrip
            (actualLiftForwardSwallowtailDatumV68
              (W := W) A
              (WorldLabel := WorldLabel)
              (PresentationLabel := PresentationLabel))).obj Y) ≫
      ((actualLiftForwardSwallowtailDatumV68
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)).base.unit.naturality
          ((actualLiftForwardSwallowtailDatumV68
            (W := W) A
            (WorldLabel := WorldLabel)
            (PresentationLabel := PresentationLabel)).base.unit.app X ≫
            (sourceRoundtrip
              (actualLiftForwardSwallowtailDatumV68
                (W := W) A
                (WorldLabel := WorldLabel)
                (PresentationLabel := PresentationLabel))).map f)).hom =
    ((actualLiftForwardSwallowtailDatumV68
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).base.unit.naturality
        ((Pseudofunctor.id
          (actualLiftForwardSwallowtailSourceV68
            (W := W) A
            (WorldLabel := WorldLabel)
            (PresentationLabel := PresentationLabel))).map f ≫
          (actualLiftForwardSwallowtailDatumV68
            (W := W) A
            (WorldLabel := WorldLabel)
            (PresentationLabel := PresentationLabel)).base.unit.app Y)).hom ≫
      (actualLiftForwardSwallowtailDatumV68
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)).base.unit.app X ◁
        (sourceRoundtrip
          (actualLiftForwardSwallowtailDatumV68
            (W := W) A
            (WorldLabel := WorldLabel)
            (PresentationLabel := PresentationLabel))).map₂
          ((actualLiftForwardSwallowtailDatumV68
            (W := W) A
            (WorldLabel := WorldLabel)
            (PresentationLabel := PresentationLabel)).base.unit.naturality f).hom :=
  Generic.IncoherentBiadjunctionDatum.unitSelfNaturalityExchange
    (actualLiftForwardSwallowtailDatumV68
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel))
    f

/-!
## Boundary after v5.69

The non-structural eta/eta exchange needed for modification naturality is now
available as a named generic theorem and is specialized to the unchanged
actual-lift datum.

The next step is to expand the v5.68 four-step component interchanger on a
morphism f, remove the surrounding mapComp/associator/counit envelopes using
native bicategory coherence, and reduce the remaining square to
unitSelfNaturalityExchangeInv.  That will produce the actual global
modification required by the v5.65 ForwardSwallowtailInterchanger type.
-/

#print axioms Generic.IncoherentBiadjunctionDatum.unitSelfNaturalityExchange
#print axioms Generic.IncoherentBiadjunctionDatum.unitSelfNaturalityExchangeInv
#print axioms actualLiftUnitSelfNaturalityExchange

end

end KUOS.DependentOriginationUnitSelfNaturalityExchangeV5_69
