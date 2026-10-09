import KUOS.DependentOriginationNativeAdjunctionLosslessReturnV5_103
import Mathlib.CategoryTheory.Bicategory.Adjunction.Mate

namespace KUOS.DependentOriginationCoherentBiadjunctionNativeMatesV5_104

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans

open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactLiftableActualLiftOneCellV5_40
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePrelaxV5_46
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePseudofunctorV5_48
open KUOS.DependentOriginationExactLiftableActualLiftTargetCounitV5_49
open KUOS.DependentOriginationExactLiftableActualLiftSourceUnitV5_50
open KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58
open KUOS.DependentOriginationCoherentBiadjunctionActualLiftV5_101
open KUOS.DependentOriginationCoherentBiadjunctionMathlibAdjunctionBridgeV5_102
open KUOS.DependentOriginationNativeAdjunctionLosslessReturnV5_103

set_option autoImplicit false
noncomputable section

/-!
# Actual-lift original unit/counit naturality as native bicategorical mates (v5.104)

v5.102 constructs native mathlib adjunctions from the original source
unit and target counit equivalences. v5.103 verifies the exact, framed
round trip without reselecting data.

Here mathlib's \`Bicategory.mateEquiv\` transports the ORIGINAL StrongTrans
naturality 2-cells to squares of the corresponding RIGHT adjoint legs.

- source unit: f ; eta_Y => eta_X ; R_L(f)
  has mate eta_X^{-1} ; f => R_L(f) ; eta_Y^{-1};
- target counit: R_E(f) ; eps_Y => eps_X ; f
  has mate eps_X^{-1} ; R_E(f) => f ; eps_Y^{-1}.

Both mates retain the genuine source/target pseudofunctor maps.
We prove the mate can be transported BACK to precisely the original
left 2-cell, and transport the existing full 2-cell naturality equation.

No claim that mates of arbitrary invertible squares are themselves
invertible is made (general mateEquiv does not preserve that property).
No new unit, counit, strict quasi-inverse, or axiom is introduced.
-/

universe u v uH vH uW uP

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

section Source

variable {X Y : ActualLiftSource.{u, v, uH, vH, uW, uP}
    (W := W) A WorldLabel PresentationLabel}

/-- The genuine source unit pseudonaturality square, transported across
the native v5.102 adjuncts to a square of the original *right* legs. -/
def actualLiftSourceUnitRightMate (f : X ⟶ Y) :
    (actualLiftSourceNativeAdjHom (W := W) A X).r ≫ f ⟶
      (actualLiftSourceRoundtrip (W := W) A).map f ≫
        (actualLiftSourceNativeAdjHom (W := W) A Y).r :=
  Bicategory.mateEquiv
    (actualLiftSourceNativeAdjHom (W := W) A X).adj
    (actualLiftSourceNativeAdjHom (W := W) A Y).adj
    ((actualLiftSourceRoundtripUnit (W := W) A).naturality f).hom

/-- There is no independent choice of left square: unmating the
right square recovers the EXACT old eta pseudonaturality component. -/
theorem actualLiftSourceUnitRightMate_unmate (f : X ⟶ Y) :
    (Bicategory.mateEquiv
      (actualLiftSourceNativeAdjHom (W := W) A X).adj
      (actualLiftSourceNativeAdjHom (W := W) A Y).adj).symm
      (actualLiftSourceUnitRightMate (W := W) A f) =
        ((actualLiftSourceRoundtripUnit (W := W) A).naturality f).hom := by
  exact Equiv.symm_apply_apply _ _

/-- The same mate arises after the lossless v5.103 return to the exact
original source equivalences, not only from the v5.102 Adj.Hom wrappers. -/
theorem actualLiftSourceUnitRightMate_recovered (f : X ⟶ Y) :
    (Bicategory.mateEquiv
      (KUOS.DependentOriginationCoherentBiadjunctionMathlibAdjunctionBridgeV5_102.Generic.nativeAdjunctionOfEquivalence
        (actualLiftSourceRecoveredEquivalence (W := W) A X))
      (KUOS.DependentOriginationCoherentBiadjunctionMathlibAdjunctionBridgeV5_102.Generic.nativeAdjunctionOfEquivalence
        (actualLiftSourceRecoveredEquivalence (W := W) A Y)))
      ((actualLiftSourceRoundtripUnit (W := W) A).naturality f).hom =
        actualLiftSourceUnitRightMate (W := W) A f := by
  rw [actualLiftSourceRecoveredEquivalence_eq, actualLiftSourceRecoveredEquivalence_eq]
  rfl

/-- Original source naturality for any 2-cell between f and g is
transported through the *same* native mate equivalence.  This is the
full StrongTrans naturality-naturality field, not objectwise equality. -/
theorem actualLiftSourceUnitRightMate_naturality₂
    {f g : X ⟶ Y} (theta : f ⟶ g) :
    (Bicategory.mateEquiv
      (actualLiftSourceNativeAdjHom (W := W) A X).adj
      (actualLiftSourceNativeAdjHom (W := W) A Y).adj)
      (theta ▷ (actualLiftSourceRoundtripUnit (W := W) A).app Y ≫
        ((actualLiftSourceRoundtripUnit (W := W) A).naturality g).hom) =
    (Bicategory.mateEquiv
      (actualLiftSourceNativeAdjHom (W := W) A X).adj
      (actualLiftSourceNativeAdjHom (W := W) A Y).adj)
      (((actualLiftSourceRoundtripUnit (W := W) A).naturality f).hom ≫
        (actualLiftSourceRoundtripUnit (W := W) A).app X ◁
          (actualLiftSourceRoundtrip (W := W) A).map₂ theta) := by
  exact congrArg _ ((actualLiftSourceRoundtripUnit (W := W) A).naturality_naturality theta)

end Source

section Target

variable {X Y : ActualLiftTarget.{u, v, uH, vH, uW, uP}
    (W := W) A WorldLabel PresentationLabel}

/-- The original target counit naturality, now the native mate between
right adjoints at F(G(X)) and F(G(Y)). -/
def actualLiftTargetCounitRightMate (f : X ⟶ Y) :
    (actualLiftTargetNativeAdjHom (W := W) A X).r ≫
      (actualLiftTargetRoundtrip (W := W) A).map f ⟶
        f ≫ (actualLiftTargetNativeAdjHom (W := W) A Y).r :=
  Bicategory.mateEquiv
    (actualLiftTargetNativeAdjHom (W := W) A X).adj
    (actualLiftTargetNativeAdjHom (W := W) A Y).adj
    ((actualLiftTargetRoundtripCounit (W := W) A).naturality f).hom

/-- Unmating recovers the OLD counit naturality 2-cell, with no
strictification or replacement of the non-strict G compositor. -/
theorem actualLiftTargetCounitRightMate_unmate (f : X ⟶ Y) :
    (Bicategory.mateEquiv
      (actualLiftTargetNativeAdjHom (W := W) A X).adj
      (actualLiftTargetNativeAdjHom (W := W) A Y).adj).symm
      (actualLiftTargetCounitRightMate (W := W) A f) =
        ((actualLiftTargetRoundtripCounit (W := W) A).naturality f).hom := by
  exact Equiv.symm_apply_apply _ _

/-- The mate is unchanged if the v5.103 reconstructed, framed
target equivalences are substituted for the v5.102 native adjuncts. -/
theorem actualLiftTargetCounitRightMate_recovered (f : X ⟶ Y) :
    (Bicategory.mateEquiv
      (KUOS.DependentOriginationCoherentBiadjunctionMathlibAdjunctionBridgeV5_102.Generic.nativeAdjunctionOfEquivalence
        (actualLiftTargetRecoveredEquivalence (W := W) A X))
      (KUOS.DependentOriginationCoherentBiadjunctionMathlibAdjunctionBridgeV5_102.Generic.nativeAdjunctionOfEquivalence
        (actualLiftTargetRecoveredEquivalence (W := W) A Y)))
      ((actualLiftTargetRoundtripCounit (W := W) A).naturality f).hom =
        actualLiftTargetCounitRightMate (W := W) A f := by
  rw [actualLiftTargetRecoveredEquivalence_eq, actualLiftTargetRecoveredEquivalence_eq]
  rfl

/-- Native mate transport of the original target counit's
naturality-naturality field for all 2-cells. -/
theorem actualLiftTargetCounitRightMate_naturality₂
    {f g : X ⟶ Y} (theta : f ⟶ g) :
    (Bicategory.mateEquiv
      (actualLiftTargetNativeAdjHom (W := W) A X).adj
      (actualLiftTargetNativeAdjHom (W := W) A Y).adj)
      ((actualLiftTargetRoundtrip (W := W) A).map₂ theta ▷
        (actualLiftTargetRoundtripCounit (W := W) A).app Y ≫
        ((actualLiftTargetRoundtripCounit (W := W) A).naturality g).hom) =
    (Bicategory.mateEquiv
      (actualLiftTargetNativeAdjHom (W := W) A X).adj
      (actualLiftTargetNativeAdjHom (W := W) A Y).adj)
      (((actualLiftTargetRoundtripCounit (W := W) A).naturality f).hom ≫
        (actualLiftTargetRoundtripCounit (W := W) A).app X ◁ theta) := by
  exact congrArg _ ((actualLiftTargetRoundtripCounit (W := W) A).naturality_naturality theta)

end Target

#print axioms actualLiftSourceUnitRightMate
#print axioms actualLiftSourceUnitRightMate_unmate
#print axioms actualLiftSourceUnitRightMate_recovered
#print axioms actualLiftSourceUnitRightMate_naturality₂
#print axioms actualLiftTargetCounitRightMate
#print axioms actualLiftTargetCounitRightMate_unmate
#print axioms actualLiftTargetCounitRightMate_recovered
#print axioms actualLiftTargetCounitRightMate_naturality₂

end

end KUOS.DependentOriginationCoherentBiadjunctionNativeMatesV5_104
