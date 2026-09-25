import KUOS.DependentOriginationRawLocalizedCompositorBridgeV3_98
import Mathlib

namespace KUOS.DependentOriginationOctahedralResidualCancellationV3_99

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
open KUOS.DependentOriginationArbitraryFactorizationParityV3_74
open KUOS.DependentOriginationArbitraryFactorizationLocalizedCocycleV3_75
open KUOS.DependentOriginationMiddleSwitchCoherenceCellV3_76
open KUOS.DependentOriginationLocalizedCompositorNaturalityV3_77
open KUOS.DependentOriginationMiddleSwitchCoboundaryBridgeV3_78
open KUOS.DependentOriginationMiddleSwitchSixTermExpansionV3_82
open KUOS.DependentOriginationRawLocalizedCompositorBridgeV3_98

set_option autoImplicit false

noncomputable section

/-!
# Octahedral residual cancellation v3.99

v3.98 identifies the eight raw restricted-lift compositor scalars from v3.74
with the eight full-localization Q-image compositor scalars from v3.76.

The remaining cancellation can now be carried out entirely in ZMod 2.

Write

* D0 for the b00+b01 M0 object-coboundary pair;
* D1 for the b10+b11 M1 object-coboundary pair;
* L for the eight localized Q-image compositors;
* T for the four transported intermediate compositors;
* M for the four middle-switch compositors;
* U for the two twice-mapped M0-connector terms.

The previously proved equations are

  L = T + M
  M = D0 + U
  D1 = T + U.

Hence

  D0 + D1 + L
    = D0 + (T+U) + (T + D0 + U)
    = 0

in characteristic two.

Using v3.98, this is exactly the twelve-term v3.74 residual.  But v3.74
forces that residual to equal one.  Therefore every choice of source objects
A0 and A1 for an arbitrary higher-localization factorization yields a
contradiction.

The final removal of the explicit A0/A1 choices is left to the next theorem
unit.
-/

noncomputable def counterFactorizationM0CoboundaryPairAdd
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) : ZMod 2 :=
  counterFactorizationObjectCoboundaryAddAt H b00
      (counterFactorizationMiddleConnectorM0 H A0 A1) +
    counterFactorizationObjectCoboundaryAddAt H b01
      (counterFactorizationMiddleConnectorM0 H A0 A1)

noncomputable def counterFactorizationM1CoboundaryPairAdd
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) : ZMod 2 :=
  counterFactorizationObjectCoboundaryAddAt H b10
      (counterFactorizationMiddleConnectorM1 H A0 A1) +
    counterFactorizationObjectCoboundaryAddAt H b11
      (counterFactorizationMiddleConnectorM1 H A0 A1)

noncomputable def counterFactorizationTwiceMappedPairAdd
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) : ZMod 2 :=
  counterFactorizationLocalizedTwiceMappedSourceAddAt H H0
      counterMiddleSwitch (allMorphisms.Q.map b10)
      (counterFactorizationMiddleConnectorM0 H A0 A1) +
    counterFactorizationLocalizedTwiceMappedSourceAddAt H H1
      counterMiddleSwitch (allMorphisms.Q.map b11)
      (counterFactorizationMiddleConnectorM0 H A0 A1)

noncomputable def counterFactorizationTransportedFourAdd
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) : ZMod 2 :=
  counterFactorizationLocalizedTransportedCompAddAt H H0
      (allMorphisms.Q.map a00) counterMiddleSwitch
      (allMorphisms.Q.map b10) A0 +
    counterFactorizationLocalizedTransportedCompAddAt H H1
      (allMorphisms.Q.map a00) counterMiddleSwitch
      (allMorphisms.Q.map b11) A0 +
    counterFactorizationLocalizedTransportedCompAddAt H H0
      (allMorphisms.Q.map a10) counterMiddleSwitch
      (allMorphisms.Q.map b10) A1 +
    counterFactorizationLocalizedTransportedCompAddAt H H1
      (allMorphisms.Q.map a10) counterMiddleSwitch
      (allMorphisms.Q.map b11) A1

noncomputable def counterFactorizationMiddleSwitchFourAdd
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) : ZMod 2 :=
  (counterFactorizationLocalizedCompAddAt H H0
      counterMiddleSwitch (allMorphisms.Q.map b10)
      (counterFactorizationLocalizedPropagatedObject H
        (allMorphisms.Q.map a00) A0) +
    counterFactorizationLocalizedCompAddAt H H0
      counterMiddleSwitch (allMorphisms.Q.map b10)
      (counterFactorizationLocalizedPropagatedObject H
        (allMorphisms.Q.map a10) A1)) +
  (counterFactorizationLocalizedCompAddAt H H1
      counterMiddleSwitch (allMorphisms.Q.map b11)
      (counterFactorizationLocalizedPropagatedObject H
        (allMorphisms.Q.map a00) A0) +
    counterFactorizationLocalizedCompAddAt H H1
      counterMiddleSwitch (allMorphisms.Q.map b11)
      (counterFactorizationLocalizedPropagatedObject H
        (allMorphisms.Q.map a10) A1))

noncomputable def counterFactorizationLocalizedEightCompositorAdd
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) : ZMod 2 :=
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
      (allMorphisms.Q.map a11) (allMorphisms.Q.map b11) A1

noncomputable def counterFactorizationRawEightCompositorAdd
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) : ZMod 2 :=
  counterFactorizationLiftCompAddAt H a00 b00 A0 +
    counterFactorizationLiftCompAddAt H a01 b10 A0 +
    counterFactorizationLiftCompAddAt H a00 b01 A0 +
    counterFactorizationLiftCompAddAt H a01 b11 A0 +
    counterFactorizationLiftCompAddAt H a10 b00 A1 +
    counterFactorizationLiftCompAddAt H a11 b10 A1 +
    counterFactorizationLiftCompAddAt H a10 b01 A1 +
    counterFactorizationLiftCompAddAt H a11 b11 A1

theorem counterFactorizationLocalizedEightCompositorAdd_eq_transport_plus_middle
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) :
    counterFactorizationLocalizedEightCompositorAdd H A0 A1 =
      counterFactorizationTransportedFourAdd H A0 A1 +
        counterFactorizationMiddleSwitchFourAdd H A0 A1 := by
  unfold counterFactorizationLocalizedEightCompositorAdd
  calc
    _ =
      counterFactorizationLocalizedTransportedCompAddAt H H0
          (allMorphisms.Q.map a00) counterMiddleSwitch
          (allMorphisms.Q.map b10) A0 +
        counterFactorizationLocalizedTransportedCompAddAt H H1
          (allMorphisms.Q.map a00) counterMiddleSwitch
          (allMorphisms.Q.map b11) A0 +
        counterFactorizationLocalizedTransportedCompAddAt H H0
          (allMorphisms.Q.map a10) counterMiddleSwitch
          (allMorphisms.Q.map b10) A1 +
        counterFactorizationLocalizedTransportedCompAddAt H H1
          (allMorphisms.Q.map a10) counterMiddleSwitch
          (allMorphisms.Q.map b11) A1 +
        counterFactorizationLocalizedCompAddAt H H0
          counterMiddleSwitch (allMorphisms.Q.map b10)
          (counterFactorizationLocalizedPropagatedObject H
            (allMorphisms.Q.map a00) A0) +
        counterFactorizationLocalizedCompAddAt H H1
          counterMiddleSwitch (allMorphisms.Q.map b11)
          (counterFactorizationLocalizedPropagatedObject H
            (allMorphisms.Q.map a00) A0) +
        counterFactorizationLocalizedCompAddAt H H0
          counterMiddleSwitch (allMorphisms.Q.map b10)
          (counterFactorizationLocalizedPropagatedObject H
            (allMorphisms.Q.map a10) A1) +
        counterFactorizationLocalizedCompAddAt H H1
          counterMiddleSwitch (allMorphisms.Q.map b11)
          (counterFactorizationLocalizedPropagatedObject H
            (allMorphisms.Q.map a10) A1) :=
      counterFactorization_middleSwitch_closed_boundary H A0 A1
    _ =
      counterFactorizationTransportedFourAdd H A0 A1 +
        counterFactorizationMiddleSwitchFourAdd H A0 A1 := by
      unfold counterFactorizationTransportedFourAdd
      unfold counterFactorizationMiddleSwitchFourAdd
      ac_rfl

theorem counterFactorizationMiddleSwitchFourAdd_eq_M0_plus_twiceMapped
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) :
    counterFactorizationMiddleSwitchFourAdd H A0 A1 =
      counterFactorizationM0CoboundaryPairAdd H A0 A1 +
        counterFactorizationTwiceMappedPairAdd H A0 A1 := by
  unfold counterFactorizationMiddleSwitchFourAdd
  calc
    _ =
      counterFactorizationObjectCoboundaryAddAt H b00
          (counterFactorizationMiddleConnectorM0 H A0 A1) +
        counterFactorizationObjectCoboundaryAddAt H b01
          (counterFactorizationMiddleConnectorM0 H A0 A1) +
        counterFactorizationLocalizedTwiceMappedSourceAddAt H H0
          counterMiddleSwitch (allMorphisms.Q.map b10)
          (counterFactorizationMiddleConnectorM0 H A0 A1) +
        counterFactorizationLocalizedTwiceMappedSourceAddAt H H1
          counterMiddleSwitch (allMorphisms.Q.map b11)
          (counterFactorizationMiddleConnectorM0 H A0 A1) :=
      counterFactorization_middleSwitch_M0_pairs_eq_coboundaries_plus_twiceMapped
        H A0 A1
    _ =
      counterFactorizationM0CoboundaryPairAdd H A0 A1 +
        counterFactorizationTwiceMappedPairAdd H A0 A1 := by
      unfold counterFactorizationM0CoboundaryPairAdd
      unfold counterFactorizationTwiceMappedPairAdd
      ac_rfl

theorem counterFactorizationM1CoboundaryPairAdd_eq_transport_plus_twiceMapped
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) :
    counterFactorizationM1CoboundaryPairAdd H A0 A1 =
      counterFactorizationTransportedFourAdd H A0 A1 +
        counterFactorizationTwiceMappedPairAdd H A0 A1 := by
  unfold counterFactorizationM1CoboundaryPairAdd
  calc
    _ =
      counterFactorizationLocalizedTransportedCompAddAt H H0
          (allMorphisms.Q.map a00) counterMiddleSwitch
          (allMorphisms.Q.map b10) A0 +
        counterFactorizationLocalizedTransportedCompAddAt H H1
          (allMorphisms.Q.map a00) counterMiddleSwitch
          (allMorphisms.Q.map b11) A0 +
        counterFactorizationLocalizedTransportedCompAddAt H H0
          (allMorphisms.Q.map a10) counterMiddleSwitch
          (allMorphisms.Q.map b10) A1 +
        counterFactorizationLocalizedTransportedCompAddAt H H1
          (allMorphisms.Q.map a10) counterMiddleSwitch
          (allMorphisms.Q.map b11) A1 +
        counterFactorizationLocalizedTwiceMappedSourceAddAt H H0
          counterMiddleSwitch (allMorphisms.Q.map b10)
          (counterFactorizationMiddleConnectorM0 H A0 A1) +
        counterFactorizationLocalizedTwiceMappedSourceAddAt H H1
          counterMiddleSwitch (allMorphisms.Q.map b11)
          (counterFactorizationMiddleConnectorM0 H A0 A1) :=
      counterFactorizationMiddleConnectorM1_pair_coboundary_sixTerm H A0 A1
    _ =
      counterFactorizationTransportedFourAdd H A0 A1 +
        counterFactorizationTwiceMappedPairAdd H A0 A1 := by
      unfold counterFactorizationTransportedFourAdd
      unfold counterFactorizationTwiceMappedPairAdd
      ac_rfl

/-- The four object coboundaries and eight localized compositors cancel
completely in ZMod 2. -/
theorem counterFactorization_localizedResidual_eq_zero
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) :
    counterFactorizationM0CoboundaryPairAdd H A0 A1 +
        counterFactorizationM1CoboundaryPairAdd H A0 A1 +
        counterFactorizationLocalizedEightCompositorAdd H A0 A1 =
      0 := by
  rw [
    counterFactorizationM1CoboundaryPairAdd_eq_transport_plus_twiceMapped
      H A0 A1,
    counterFactorizationLocalizedEightCompositorAdd_eq_transport_plus_middle
      H A0 A1,
    counterFactorizationMiddleSwitchFourAdd_eq_M0_plus_twiceMapped
      H A0 A1
  ]
  calc
    counterFactorizationM0CoboundaryPairAdd H A0 A1 +
          (counterFactorizationTransportedFourAdd H A0 A1 +
            counterFactorizationTwiceMappedPairAdd H A0 A1) +
          (counterFactorizationTransportedFourAdd H A0 A1 +
            (counterFactorizationM0CoboundaryPairAdd H A0 A1 +
              counterFactorizationTwiceMappedPairAdd H A0 A1)) =
      (counterFactorizationM0CoboundaryPairAdd H A0 A1 +
          counterFactorizationM0CoboundaryPairAdd H A0 A1) +
        (counterFactorizationTransportedFourAdd H A0 A1 +
          counterFactorizationTransportedFourAdd H A0 A1) +
        (counterFactorizationTwiceMappedPairAdd H A0 A1 +
          counterFactorizationTwiceMappedPairAdd H A0 A1) := by
      ac_rfl
    _ = 0 := by
      simp only [CharTwo.add_self_eq_zero, zero_add, add_zero]

theorem counterFactorizationRawEightCompositorAdd_eq_localized
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) :
    counterFactorizationRawEightCompositorAdd H A0 A1 =
      counterFactorizationLocalizedEightCompositorAdd H A0 A1 := by
  unfold counterFactorizationRawEightCompositorAdd
  unfold counterFactorizationLocalizedEightCompositorAdd
  exact counterFactorization_rawEightCompositors_eq_localizedEightCompositors
    H A0 A1

noncomputable def counterFactorizationRawParityResidualAdd
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) : ZMod 2 :=
  counterFactorizationM0CoboundaryPairAdd H A0 A1 +
    counterFactorizationM1CoboundaryPairAdd H A0 A1 +
    counterFactorizationRawEightCompositorAdd H A0 A1

/-- The complete twelve-term v3.74 residual is zero. -/
theorem counterFactorizationRawParityResidualAdd_eq_zero
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) :
    counterFactorizationRawParityResidualAdd H A0 A1 = 0 := by
  unfold counterFactorizationRawParityResidualAdd
  rw [counterFactorizationRawEightCompositorAdd_eq_localized H A0 A1]
  exact counterFactorization_localizedResidual_eq_zero H A0 A1

/-- For every chosen pair of source objects, v3.74 now contradicts the closed
middle-switch coherence calculation. -/
theorem counterFactorization_rawParity_contradiction_at_objects
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) :
    False := by
  have hRaw :=
    counterFactorization_rawParity_forces_coboundary_plus_compositor_residual
      H A0 A1
  have hResidualZero :=
    counterFactorizationRawParityResidualAdd_eq_zero H A0 A1
  have hOneZero : (1 : ZMod 2) = 0 := by
    calc
      (1 : ZMod 2) =
        counterFactorizationObjectCoboundaryAddAt H b00
            (counterFactorizationMiddleConnectorM0 H A0 A1) +
          counterFactorizationObjectCoboundaryAddAt H b01
            (counterFactorizationMiddleConnectorM0 H A0 A1) +
          counterFactorizationObjectCoboundaryAddAt H b10
            (counterFactorizationMiddleConnectorM1 H A0 A1) +
          counterFactorizationObjectCoboundaryAddAt H b11
            (counterFactorizationMiddleConnectorM1 H A0 A1) +
          counterFactorizationLiftCompAddAt H a00 b00 A0 +
          counterFactorizationLiftCompAddAt H a01 b10 A0 +
          counterFactorizationLiftCompAddAt H a00 b01 A0 +
          counterFactorizationLiftCompAddAt H a01 b11 A0 +
          counterFactorizationLiftCompAddAt H a10 b00 A1 +
          counterFactorizationLiftCompAddAt H a11 b10 A1 +
          counterFactorizationLiftCompAddAt H a10 b01 A1 +
          counterFactorizationLiftCompAddAt H a11 b11 A1 := hRaw
      _ = counterFactorizationRawParityResidualAdd H A0 A1 := by
        unfold counterFactorizationRawParityResidualAdd
        unfold counterFactorizationM0CoboundaryPairAdd
        unfold counterFactorizationM1CoboundaryPairAdd
        unfold counterFactorizationRawEightCompositorAdd
        ac_rfl
      _ = 0 := hResidualZero
  exact one_ne_zero hOneZero

/-!
## Boundary after v3.99

The arbitrary-factorization octahedral residual is now closed.

For every arbitrary higher-localization factorization H and every choice of
source objects A0 over L0 and A1 over L1, the v3.74 odd-parity equation forces
one while the middle-switch coherence calculation forces the same residual to
zero.  Hence such a pair of source objects is impossible.

The only remaining step to obtain unconditional abstract nonfactorization is
to remove the explicit A0/A1 parameters.  Since each comparison component of H
is an equivalence onto the nonempty one-object target CounterFiber, the source
fibers over L0 and L1 are nonempty.  The next theorem unit should choose those
objects from essential surjectivity and apply the contradiction above.
-/

end

end KUOS.DependentOriginationOctahedralResidualCancellationV3_99
