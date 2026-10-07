import KUOS.DependentOriginationUnitSelfInterchangerBoundaryV5_73

namespace KUOS.DependentOriginationUnitSelfInterchangerNaturalityV5_74

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans

open KUOS.DependentOriginationExactLiftableActualLiftQuasiInverseTriangleUnitV5_53
open KUOS.DependentOriginationUnitPostcompositionNativeSourceV5_72
open KUOS.DependentOriginationUnitPostcompositionNativeSourceV5_72.Generic
open KUOS.DependentOriginationUnitSelfInterchangerBoundaryV5_73
open KUOS.DependentOriginationUnitSelfInterchangerBoundaryV5_73.Generic

set_option autoImplicit false

noncomputable section

/-!
# Unit self-interchanger naturality v5.74

The v5.73 boundary compares the two native eta/eta paths

  eta ; UnitPostcomposition(R, eta)
  eta ; UnitPrecomposition(R, eta)

by the inverse of eta.naturality(eta_X).

It is cleaner to prove the opposite orientation first.  In that direction the
component is eta.naturality(eta_X).hom, and the unique non-structural square is
exactly eta.naturality_naturality applied to eta.naturality(f).hom.  Mathlib's
StrongTrans.isoMk then constructs the inverse modification automatically, so
the v5.73 post-to-pre orientation is obtained without re-proving inverse
naturality by hand.
-/

namespace Generic

universe uB vB wB

variable {B : Type uB} [Bicategory.{wB, vB} B]

namespace UnitSelfInterchanger

variable (R : Pseudofunctor B B)
variable (eta : Pseudofunctor.StrongTrans (Pseudofunctor.id B) R)

/-- The eta/eta component in the forward pseudonaturality orientation. -/
def reverseComponentIso (X : B) :
    (prePath R eta).app X ≅
      (postPath R eta).app X :=
  eta.naturality (eta.app X)

@[simp] theorem reverseComponentIso_hom (X : B) :
    (reverseComponentIso R eta X).hom =
      (eta.naturality (eta.app X)).hom :=
  rfl

/-- Modification naturality in the forward pseudonaturality orientation. -/
def ReverseNaturality : Prop :=
  ∀ {X Y : B} (f : X ⟶ Y),
    (Pseudofunctor.id B).map f ◁
          (reverseComponentIso R eta Y).hom ≫
        ((postPath R eta).naturality f).hom =
      ((prePath R eta).naturality f).hom ≫
        (reverseComponentIso R eta X).hom ▷
          (Pseudofunctor.comp R R).map f

/-- The central eta/eta modification square.  The only non-structural input is
2-cell naturality of eta at eta.naturality(f).hom; the two composition laws
then expose the pre- and post-composed naturality factors. -/
theorem reverseNaturality : ReverseNaturality R eta := by
  intro X Y f
  cat_disch

end UnitSelfInterchanger

end Generic

#print axioms Generic.UnitSelfInterchanger.reverseNaturality

end

end KUOS.DependentOriginationUnitSelfInterchangerNaturalityV5_74
