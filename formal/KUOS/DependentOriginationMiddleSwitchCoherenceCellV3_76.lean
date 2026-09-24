import KUOS.DependentOriginationArbitraryFactorizationLocalizedCocycleV3_75
import Mathlib.Tactic.LinearCombination

namespace KUOS.DependentOriginationMiddleSwitchCoherenceCellV3_76

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
open KUOS.DependentOriginationArbitraryTransportComparisonV3_69
open KUOS.DependentOriginationArbitraryFactorizationParityV3_74
open KUOS.DependentOriginationArbitraryFactorizationLocalizedCocycleV3_75

set_option autoImplicit false

noncomputable section

/-!
# Middle-switch coherence cell v3.76

v3.74 reduces an arbitrary higher-localization factorization of the concrete
octahedral C2 countermodel to four object coboundaries plus eight lift-compositor
scalars.  v3.75 exposes the arbitrary localized lift on the full localization
and proves its exact object-dependent associator cocycle.

This file performs the first closed localization specialization.  The v3.75
cocycle is evaluated on the four triples

```text
Q(a00), counterMiddleSwitch, Q(b10)
Q(a00), counterMiddleSwitch, Q(b11)
Q(a10), counterMiddleSwitch, Q(b10)
Q(a10), counterMiddleSwitch, Q(b11)
```

and the exact localization equalities from v3.69 are used to identify the two
outer composites.  Summing the four balances in ZMod 2 gives a single closed
middle-switch boundary equation: the eight raw octahedral compositor terms are
equal to four transported intermediate compositors plus four compositors whose
first edge is the localization middle switch.

This is deliberately prior to choosing any polyhedral carrier.  In particular,
no dodecahedral, associahedral, or truncated-icosahedral incidence is assumed.
The resulting eight-term boundary is the finite datum that the next theorem
unit must compare with the four v3.74 object coboundaries.
-/

/-- The v3.75 localization cocycle on the L0-M0-M1-H0 middle-switch triple. -/
theorem counterFactorization_middleSwitch_cocycle_a00_b10
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0) :
    counterFactorizationLocalizedCompAddAt H H0
        (allMorphisms.Q.map a01) (allMorphisms.Q.map b10) A0 +
      counterFactorizationLocalizedTransportedCompAddAt H H0
        (allMorphisms.Q.map a00) counterMiddleSwitch
        (allMorphisms.Q.map b10) A0 =
    counterFactorizationLocalizedCompAddAt H H0
        counterMiddleSwitch (allMorphisms.Q.map b10)
        (counterFactorizationLocalizedPropagatedObject H
          (allMorphisms.Q.map a00) A0) +
      counterFactorizationLocalizedCompAddAt H H0
        (allMorphisms.Q.map a00) (allMorphisms.Q.map b00) A0 := by
  simpa only [counterA00_comp_middleSwitch, counterMiddleSwitch_comp_b10] using
    (counterFactorizationLocalizedCompAdd_cocycle
      H H0 (allMorphisms.Q.map a00) counterMiddleSwitch
        (allMorphisms.Q.map b10) A0)

/-- The v3.75 localization cocycle on the L0-M0-M1-H1 middle-switch triple. -/
theorem counterFactorization_middleSwitch_cocycle_a00_b11
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0) :
    counterFactorizationLocalizedCompAddAt H H1
        (allMorphisms.Q.map a01) (allMorphisms.Q.map b11) A0 +
      counterFactorizationLocalizedTransportedCompAddAt H H1
        (allMorphisms.Q.map a00) counterMiddleSwitch
        (allMorphisms.Q.map b11) A0 =
    counterFactorizationLocalizedCompAddAt H H1
        counterMiddleSwitch (allMorphisms.Q.map b11)
        (counterFactorizationLocalizedPropagatedObject H
          (allMorphisms.Q.map a00) A0) +
      counterFactorizationLocalizedCompAddAt H H1
        (allMorphisms.Q.map a00) (allMorphisms.Q.map b01) A0 := by
  simpa only [counterA00_comp_middleSwitch, counterMiddleSwitch_comp_b11] using
    (counterFactorizationLocalizedCompAdd_cocycle
      H H1 (allMorphisms.Q.map a00) counterMiddleSwitch
        (allMorphisms.Q.map b11) A0)

/-- The v3.75 localization cocycle on the L1-M0-M1-H0 middle-switch triple. -/
theorem counterFactorization_middleSwitch_cocycle_a10_b10
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A1 : CounterFactorizationFiber H L1) :
    counterFactorizationLocalizedCompAddAt H H0
        (allMorphisms.Q.map a11) (allMorphisms.Q.map b10) A1 +
      counterFactorizationLocalizedTransportedCompAddAt H H0
        (allMorphisms.Q.map a10) counterMiddleSwitch
        (allMorphisms.Q.map b10) A1 =
    counterFactorizationLocalizedCompAddAt H H0
        counterMiddleSwitch (allMorphisms.Q.map b10)
        (counterFactorizationLocalizedPropagatedObject H
          (allMorphisms.Q.map a10) A1) +
      counterFactorizationLocalizedCompAddAt H H0
        (allMorphisms.Q.map a10) (allMorphisms.Q.map b00) A1 := by
  simpa only [counterA10_comp_middleSwitch, counterMiddleSwitch_comp_b10] using
    (counterFactorizationLocalizedCompAdd_cocycle
      H H0 (allMorphisms.Q.map a10) counterMiddleSwitch
        (allMorphisms.Q.map b10) A1)

/-- The v3.75 localization cocycle on the L1-M0-M1-H1 middle-switch triple. -/
theorem counterFactorization_middleSwitch_cocycle_a10_b11
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A1 : CounterFactorizationFiber H L1) :
    counterFactorizationLocalizedCompAddAt H H1
        (allMorphisms.Q.map a11) (allMorphisms.Q.map b11) A1 +
      counterFactorizationLocalizedTransportedCompAddAt H H1
        (allMorphisms.Q.map a10) counterMiddleSwitch
        (allMorphisms.Q.map b11) A1 =
    counterFactorizationLocalizedCompAddAt H H1
        counterMiddleSwitch (allMorphisms.Q.map b11)
        (counterFactorizationLocalizedPropagatedObject H
          (allMorphisms.Q.map a10) A1) +
      counterFactorizationLocalizedCompAddAt H H1
        (allMorphisms.Q.map a10) (allMorphisms.Q.map b01) A1 := by
  simpa only [counterA10_comp_middleSwitch, counterMiddleSwitch_comp_b11] using
    (counterFactorizationLocalizedCompAdd_cocycle
      H H1 (allMorphisms.Q.map a10) counterMiddleSwitch
        (allMorphisms.Q.map b11) A1)

/-- Closed middle-switch boundary in ZMod 2.

The eight compositor terms attached to the original octahedral triangular
faces are exactly the sum of the four transported intermediate compositors and
the four compositors beginning with the localization middle switch. -/
theorem counterFactorization_middleSwitch_closed_boundary
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) :
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
        (allMorphisms.Q.map a11) (allMorphisms.Q.map b11) A1 =
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
          (allMorphisms.Q.map a10) A1) := by
  have h00 :=
    counterFactorization_middleSwitch_cocycle_a00_b10 H A0
  have h01 :=
    counterFactorization_middleSwitch_cocycle_a00_b11 H A0
  have h10 :=
    counterFactorization_middleSwitch_cocycle_a10_b10 H A1
  have h11 :=
    counterFactorization_middleSwitch_cocycle_a10_b11 H A1

  let E : ZMod 2 :=
    counterFactorizationLocalizedCompAddAt H H0
        (allMorphisms.Q.map a00) (allMorphisms.Q.map b00) A0 +
      counterFactorizationLocalizedCompAddAt H H1
        (allMorphisms.Q.map a00) (allMorphisms.Q.map b01) A0 +
      counterFactorizationLocalizedCompAddAt H H0
        (allMorphisms.Q.map a10) (allMorphisms.Q.map b00) A1 +
      counterFactorizationLocalizedCompAddAt H H1
        (allMorphisms.Q.map a10) (allMorphisms.Q.map b01) A1
  let O : ZMod 2 :=
    counterFactorizationLocalizedCompAddAt H H0
        (allMorphisms.Q.map a01) (allMorphisms.Q.map b10) A0 +
      counterFactorizationLocalizedCompAddAt H H1
        (allMorphisms.Q.map a01) (allMorphisms.Q.map b11) A0 +
      counterFactorizationLocalizedCompAddAt H H0
        (allMorphisms.Q.map a11) (allMorphisms.Q.map b10) A1 +
      counterFactorizationLocalizedCompAddAt H H1
        (allMorphisms.Q.map a11) (allMorphisms.Q.map b11) A1
  let T : ZMod 2 :=
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
  let M : ZMod 2 :=
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
          (allMorphisms.Q.map a10) A1)

  have hsum : O + T = M + E := by
    dsimp [O, T, M, E]
    linear_combination h00 + h01 + h10 + h11
  have hzero : (O + T) + (M + E) = 0 :=
    CharTwo.add_eq_zero.mpr hsum
  have hEO : E + O = T + M := by
    apply CharTwo.add_eq_zero.mp
    calc
      (E + O) + (T + M) = (O + T) + (M + E) := by
        ac_rfl
      _ = 0 := hzero

  calc
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
          (allMorphisms.Q.map a11) (allMorphisms.Q.map b11) A1 =
      E + O := by
        dsimp [E, O]
        ac_rfl
    _ = T + M := hEO
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
            (allMorphisms.Q.map a10) A1) := by
        dsimp [T, M]
        ac_rfl

/-!
## Boundary after v3.76

The arbitrary localized-lift contribution is no longer an unstructured sum of
eight raw face compositors.  It is a closed middle-switch boundary consisting
of two four-term families:

* four transported compositors on `Q(a_i0), middleSwitch, Q(b_1j)`;
* four compositors on `middleSwitch, Q(b_1j)`, evaluated at the two propagated
  M0-fiber objects.

The next theorem unit should compare the second family across the v3.74 M0
connector and compare the transported first family with the corresponding M1
connector.  Only after those incidence identities are proved should a
pentagon/hexagon polyhedral carrier be selected.

A truncated-icosahedral carrier remains a live candidate because it has two
face types, but v3.76 does not build that geometry into the theorem statement.
-/

end

end KUOS.DependentOriginationMiddleSwitchCoherenceCellV3_76
