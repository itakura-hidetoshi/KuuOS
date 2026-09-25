import KUOS.DependentOriginationMiddleSwitchSixTermExpansionV3_82
import Mathlib

namespace KUOS.DependentOriginationRawLocalizedCompositorBridgeV3_98

open CategoryTheory
open CategoryTheory.Bicategory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
open KUOS.DependentOriginationArbitraryFactorizationScalarV3_72
open KUOS.DependentOriginationArbitraryFactorizationParityV3_74
open KUOS.DependentOriginationArbitraryFactorizationLocalizedCocycleV3_75

set_option autoImplicit false

noncomputable section

/-!
# Raw-to-localized compositor bridge v3.98

v3.74 expresses the arbitrary-factorization parity residual using eight
compositor scalars of the raw restricted lift.  v3.76-v3.82 instead work with
the same arbitrary lift viewed directly on the full localization.

The missing bridge is purely the presentation wrapper.  On a raw composable
pair f,g, restricting H.lift along the presentation unit

  Q followed by opOp

and evaluating the full-localization view on Q(f),Q(g) expose the same
underlying H.lift compositor component.

This file removes those wrappers first at the multiplicative C2 scalar level,
then at the additive ZMod 2 level, and finally on the complete eight-face
octahedral compositor sum.

No new coherence or object-independence hypothesis is introduced.
-/

/-- On localization images of raw arrows, the full-localization compositor
scalar is exactly the raw restricted-lift compositor scalar. -/
@[simp] theorem counterFactorizationLocalizedCompImageScalarAt_Q_map
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    {X Y Z : OctahedralVertex}
    (f : X ⟶ Y) (g : Y ⟶ Z)
    (A : CounterFactorizationFiber H X) :
    counterFactorizationLocalizedCompImageScalarAt H Z
        (allMorphisms.Q.map f) (allMorphisms.Q.map g) A =
      counterFactorizationLiftCompImageScalarAt H f g A := by
  set_option backward.isDefEq.respectTransparency false in
    simp [
      counterFactorizationLocalizedCompImageScalarAt,
      counterFactorizationLiftCompImageScalarAt,
      counterFactorizationLocalizationView,
      restrictHigherLocalizedSystem,
      higherPresentationUnitFunctor,
      CategoryTheory.Pseudofunctor.comp,
      CategoryTheory.Functor.toPseudofunctor,
      CategoryTheory.pseudofunctorOfIsLocallyDiscrete,
      CategoryTheory.LocallyDiscrete.mkPseudofunctor
    ]

/-- Additive form of the same raw/full-localization bridge. -/
@[simp] theorem counterFactorizationLocalizedCompAddAt_Q_map
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    {X Y Z : OctahedralVertex}
    (f : X ⟶ Y) (g : Y ⟶ Z)
    (A : CounterFactorizationFiber H X) :
    counterFactorizationLocalizedCompAddAt H Z
        (allMorphisms.Q.map f) (allMorphisms.Q.map g) A =
      counterFactorizationLiftCompAddAt H f g A := by
  unfold counterFactorizationLocalizedCompAddAt
  unfold counterFactorizationLiftCompAddAt
  rw [counterFactorizationLocalizedCompImageScalarAt_Q_map H f g A]

/-- The complete eight raw octahedral compositor terms from v3.74 are exactly
the eight Q-image full-localization compositor terms used in v3.76. -/
theorem counterFactorization_rawEightCompositors_eq_localizedEightCompositors
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) :
    counterFactorizationLiftCompAddAt H a00 b00 A0 +
      counterFactorizationLiftCompAddAt H a01 b10 A0 +
      counterFactorizationLiftCompAddAt H a00 b01 A0 +
      counterFactorizationLiftCompAddAt H a01 b11 A0 +
      counterFactorizationLiftCompAddAt H a10 b00 A1 +
      counterFactorizationLiftCompAddAt H a11 b10 A1 +
      counterFactorizationLiftCompAddAt H a10 b01 A1 +
      counterFactorizationLiftCompAddAt H a11 b11 A1 =
    counterFactorizationLocalizedCompAddAt H H0
        (allMorphisms.Q.map a00) (allMorphisms.Q.map b00) A0 +
      counterFactorizationLocalizedCompAddAt H H0
        (allMorphisms.Q.map a01) (allMorphisms.Q.map b10) A0 +
      counterFactorizationLocalizedCompAddAt H H1
        (allMorphisms.Q.map a00) (allMorphisms.Q.map b01) A0 +
      counterFactorizationLocalizedCompAddAt H H1
        (allMorphisms.Q.map a01) (allMorphisms.Q.map b11) A0 +
      counterFactorizationLocalizedCompAddAt H H0
        (allMorphisms.Q.map a10) (allMorphisms.Q.map b00) A1 +
      counterFactorizationLocalizedCompAddAt H H0
        (allMorphisms.Q.map a11) (allMorphisms.Q.map b10) A1 +
      counterFactorizationLocalizedCompAddAt H H1
        (allMorphisms.Q.map a10) (allMorphisms.Q.map b01) A1 +
      counterFactorizationLocalizedCompAddAt H H1
        (allMorphisms.Q.map a11) (allMorphisms.Q.map b11) A1 := by
  rw [
    counterFactorizationLocalizedCompAddAt_Q_map H a00 b00 A0,
    counterFactorizationLocalizedCompAddAt_Q_map H a01 b10 A0,
    counterFactorizationLocalizedCompAddAt_Q_map H a00 b01 A0,
    counterFactorizationLocalizedCompAddAt_Q_map H a01 b11 A0,
    counterFactorizationLocalizedCompAddAt_Q_map H a10 b00 A1,
    counterFactorizationLocalizedCompAddAt_Q_map H a11 b10 A1,
    counterFactorizationLocalizedCompAddAt_Q_map H a10 b01 A1,
    counterFactorizationLocalizedCompAddAt_Q_map H a11 b11 A1
  ]

/-!
## Boundary after v3.98

The last representation mismatch between v3.74 and v3.76 has been isolated
and removed: the eight raw restricted-lift compositor scalars are exactly the
eight full-localization Q-image compositor scalars.

The next theorem unit can now combine, without any additional bridge:

* v3.74: raw odd class = four object coboundaries + eight raw compositors;
* v3.76: eight localized compositors = transported family + M0 family;
* v3.78: M0 family = d00+d01 + twice-mapped pair;
* v3.82: d10+d11 = transported family + the same twice-mapped pair.

In ZMod 2 every term then occurs twice.  The expected conclusion is that the
v3.74 residual is zero, contradicting its forced value one.
-/

end

end KUOS.DependentOriginationRawLocalizedCompositorBridgeV3_98
