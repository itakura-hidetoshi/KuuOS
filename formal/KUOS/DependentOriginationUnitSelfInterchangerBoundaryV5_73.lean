import KUOS.DependentOriginationUnitPostcompositionNativeSourceV5_72

namespace KUOS.DependentOriginationUnitSelfInterchangerBoundaryV5_73

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans

open KUOS.DependentOriginationExactLiftableActualLiftQuasiInverseTriangleUnitV5_53
open KUOS.DependentOriginationUnitPostcompositionNativeSourceV5_72
open KUOS.DependentOriginationUnitPostcompositionNativeSourceV5_72.Generic

set_option autoImplicit false

noncomputable section

/-!
# Unit self-interchanger boundary v5.73

This head is revalidated against the repaired v5.71/v5.72 stack; cascade
receipts from the former parent failure are not reused.
The v5.72 declarations used below live under
`DependentOriginationUnitPostcompositionNativeSourceV5_72.Generic`.
Lean's `open` is namespace-local rather than recursive through child
namespaces, so the Generic namespace is opened explicitly before referring to
`UnitPostcomposition.strongTrans`.

Let R : B -> B and eta : Id_B => R.

v5.53 gives the native left action of eta along R,

  UnitPrecomposition(R, eta) : R => R ; R,

with component eta_(R X).

v5.72 gives the native right action,

  UnitPostcomposition(R, eta) : R => R ; R,

with component R.map(eta_X).

After vertically composing each with eta itself, both paths run from Id_B to
R ; R:

  eta ; UnitPostcomposition(R, eta)
  eta ; UnitPrecomposition(R, eta).

The canonical objectwise comparison from the first path to the second is
exactly

  (eta.naturality (eta_X))^{-1}.

This file fixes that global StrongTrans boundary and isolates the one remaining
modification-naturality proposition.  No inhabitant of that proposition is
assumed.  The v5.69 eta/eta exchange is the substantive equation expected to
discharge it after structural normalization.
-/

namespace Generic

universe uB vB wB

variable {B : Type uB} [Bicategory.{wB, vB} B]

namespace UnitSelfInterchanger

variable (R : Pseudofunctor B B)
variable (eta : Pseudofunctor.StrongTrans (Pseudofunctor.id B) R)

/-- The eta/eta path using the native-source right action from v5.72. -/
abbrev postPath :
    Pseudofunctor.StrongTrans
      (Pseudofunctor.id B)
      (Pseudofunctor.comp R R) :=
  Pseudofunctor.StrongTrans.vcomp
    eta
    (UnitPostcomposition.strongTrans R eta)

/-- The eta/eta path using the native-source left action from v5.53. -/
abbrev prePath :
    Pseudofunctor.StrongTrans
      (Pseudofunctor.id B)
      (Pseudofunctor.comp R R) :=
  Pseudofunctor.StrongTrans.vcomp
    eta
    (UnitPrecomposition.strongTrans R eta)

/-- The canonical eta/eta component, oriented as required by the forward
swallowtail: from eta_X ; R(eta_X) to eta_X ; eta_(R X). -/
def componentIso (X : B) :
    (postPath R eta).app X ≅
      (prePath R eta).app X :=
  (eta.naturality (eta.app X)).symm

@[simp] theorem componentIso_hom (X : B) :
    (componentIso R eta X).hom =
      (eta.naturality (eta.app X)).inv :=
  rfl

@[simp] theorem componentIso_inv (X : B) :
    (componentIso R eta X).inv =
      (eta.naturality (eta.app X)).hom :=
  rfl

/-- Exact modification-naturality proposition for the canonical eta/eta
component family. -/
def Naturality : Prop :=
  ∀ {X Y : B} (f : X ⟶ Y),
    (Pseudofunctor.id B).map f ◁
          (componentIso R eta Y).hom ≫
        ((prePath R eta).naturality f).hom =
      ((postPath R eta).naturality f).hom ≫
        (componentIso R eta X).hom ▷
          (Pseudofunctor.comp R R).map f

local instance unitSelfHomCategory :
    Category
      (Pseudofunctor.StrongTrans
        (Pseudofunctor.id B)
        (Pseudofunctor.comp R R)) :=
  Pseudofunctor.StrongTrans.homCategory
    (B := B) (C := B)
    (F := Pseudofunctor.id B)
    (G := Pseudofunctor.comp R R)

/-- Once the v5.73 naturality proposition is proved, package the already fixed
eta/eta components into a native invertible modification. -/
def comparisonIsoOfNaturality
    (h : Naturality R eta) :
    @CategoryTheory.Iso
      (Pseudofunctor.StrongTrans
        (Pseudofunctor.id B)
        (Pseudofunctor.comp R R))
      (Pseudofunctor.StrongTrans.homCategory
        (B := B) (C := B)
        (F := Pseudofunctor.id B)
        (G := Pseudofunctor.comp R R))
      (postPath R eta)
      (prePath R eta) :=
  Pseudofunctor.StrongTrans.isoMk
    (η := postPath R eta)
    (θ := prePath R eta)
    (componentIso R eta)
    (by
      intro X Y f
      exact h f)

@[simp] theorem comparisonIsoOfNaturality_hom_app
    (h : Naturality R eta) (X : B) :
    (comparisonIsoOfNaturality R eta h).hom.as.app X =
      (eta.naturality (eta.app X)).inv :=
  rfl

@[simp] theorem comparisonIsoOfNaturality_inv_app
    (h : Naturality R eta) (X : B) :
    (comparisonIsoOfNaturality R eta h).inv.as.app X =
      (eta.naturality (eta.app X)).hom :=
  rfl

end UnitSelfInterchanger

end Generic

/-!
## Boundary after v5.73

The central eta/eta part of the forward swallowtail now has a precise global
boundary independent of the surrounding mapComp, associator and counit
whiskering.

The immediate proof target is

  Generic.UnitSelfInterchanger.Naturality R eta.

Its only non-structural ingredient is the v5.69 eta/eta exchange.  The next
file can expand the two StrongTrans.vcomp naturalities and the v5.72 mapped
square, use eta.naturality_comp on the two composite 1-cells, and reduce the
remaining middle square to that exchange.
-/

#print axioms Generic.UnitSelfInterchanger.componentIso
#print axioms Generic.UnitSelfInterchanger.Naturality
#print axioms Generic.UnitSelfInterchanger.comparisonIsoOfNaturality
#print axioms Generic.UnitSelfInterchanger.comparisonIsoOfNaturality_hom_app
#print axioms Generic.UnitSelfInterchanger.comparisonIsoOfNaturality_inv_app

end

end KUOS.DependentOriginationUnitSelfInterchangerBoundaryV5_73
