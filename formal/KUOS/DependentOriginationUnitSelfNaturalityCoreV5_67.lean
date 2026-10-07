import KUOS.DependentOriginationReverseSwallowtailPredicateV5_66

namespace KUOS.DependentOriginationUnitSelfNaturalityCoreV5_67

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans

open KUOS.DependentOriginationExactLiftableActualLiftIncoherentBiadjunctionV5_59
open KUOS.DependentOriginationExactLiftableActualLiftIncoherentBiadjunctionV5_59.Generic
open KUOS.DependentOriginationBiadjunctionTriangulatorHorizontalPastesV5_64.Generic.IncoherentBiadjunctionDatum
open KUOS.DependentOriginationForwardSwallowtailPredicateV5_65
open KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6

set_option autoImplicit false

noncomputable section

/-!
# Unit self-naturality core v5.67

The forward swallowtail predicate of v5.65 requires a canonical
unit-centered interchanger paste.  The irreducible core of that paste is not
new data: it is the pseudonaturality isomorphism of the stored unit evaluated
at the unit component itself.

For an incoherent biadjunction datum with

  eta : Id_B => R,   R = F ; G,

and X : B, pseudonaturality at eta_X gives

  Id_B.map(eta_X) ; eta_(R X)
      ~=
  eta_X ; R.map(eta_X).

This is the native eta/eta interchanger core.  The identity-pseudofunctor map
is kept explicit in the type, rather than silently strictified.  Later files
may normalize it together with the associator, unitor, counit-whiskering and
mapComp cells needed to reach the full v5.65 swallowtail boundary.

No modification-level swallowtail cell is asserted here.
-/

namespace Generic

universe uB vB wB uC vC wC

variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]

namespace IncoherentBiadjunctionDatum

variable (D : IncoherentBiadjunctionDatum B C)

/-- The canonical eta/eta interchanger core: the stored unit's native
pseudonaturality isomorphism evaluated at its own component. -/
def unitSelfNaturalityIso (X : B) :
    (Pseudofunctor.id B).map (D.base.unit.app X) ≫
          D.base.unit.app ((sourceRoundtrip D).obj X) ≅
      D.base.unit.app X ≫
          (sourceRoundtrip D).map (D.base.unit.app X) :=
  D.base.unit.naturality (D.base.unit.app X)

@[simp] theorem unitSelfNaturalityIso_hom (X : B) :
    (unitSelfNaturalityIso D X).hom =
      (D.base.unit.naturality (D.base.unit.app X)).hom :=
  rfl

@[simp] theorem unitSelfNaturalityIso_inv (X : B) :
    (unitSelfNaturalityIso D X).inv =
      (D.base.unit.naturality (D.base.unit.app X)).inv :=
  rfl

end IncoherentBiadjunctionDatum

end Generic

open Generic

universe u v uH vH uW uP

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-- The unchanged actual-lift source object used for the eta/eta
pseudonaturality core. -/
abbrev actualLiftUnitSelfSource :=
  ActualLiftSource
    (W := W) A WorldLabel PresentationLabel

/-- The canonical actual-lift eta/eta interchanger core.  This is exactly the
stored source unit naturality at its own component; no new 2-cell is chosen. -/
def actualLiftUnitSelfNaturalityIso
    (X :
      actualLiftUnitSelfSource
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)) :=
  Generic.IncoherentBiadjunctionDatum.unitSelfNaturalityIso
    (actualLiftForwardSwallowtailDatum
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel))
    X

/-!
## Boundary after v5.67

The canonical eta/eta interchanger core is now a named native isomorphism,
both generically and for the unchanged actual-lift datum.

The next step is to transport this core to the full v5.65 boundary.  That
transport must retain, rather than erase:

* the source-roundtrip mapComp cells;
* the relevant associators and unitors;
* the counit whiskering which closes the two triangle paths.

Only after those structural corrections are assembled and proved natural as
a modification can the v5.65 forward swallowtail predicate be discharged.
-/

#print axioms Generic.IncoherentBiadjunctionDatum.unitSelfNaturalityIso
#print axioms Generic.IncoherentBiadjunctionDatum.unitSelfNaturalityIso_hom
#print axioms Generic.IncoherentBiadjunctionDatum.unitSelfNaturalityIso_inv
#print axioms actualLiftUnitSelfNaturalityIso

end

end KUOS.DependentOriginationUnitSelfNaturalityCoreV5_67
