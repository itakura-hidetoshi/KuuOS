import KUOS.DependentOriginationLocalizedCompositorNaturalityV3_77

namespace KUOS.DependentOriginationMiddleSwitchCoboundaryBridgeV3_78

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
open KUOS.DependentOriginationArbitraryTransportComparisonV3_69
open KUOS.DependentOriginationArbitraryFactorizationScalarV3_72
open KUOS.DependentOriginationFactorizationObjectCoboundaryV3_73
open KUOS.DependentOriginationArbitraryFactorizationParityV3_74
open KUOS.DependentOriginationArbitraryFactorizationLocalizedCocycleV3_75
open KUOS.DependentOriginationMiddleSwitchCoherenceCellV3_76
open KUOS.DependentOriginationLocalizedCompositorNaturalityV3_77

set_option autoImplicit false

noncomputable section

/-!
# Middle-switch coboundary bridge v3.78

v3.77 resolves the two M0 middle-switch compositor pairs into a single-arrow
mapped source scalar along Q(b00) or Q(b01), plus a twice-mapped source scalar
through the middle switch and the corresponding M1-to-upper edge.

The remaining bookkeeping step is to identify the first terms with the exact
inter-object coboundaries already present in the v3.74 residual.

This file first proves the generic raw/localized bridge

localizedMapped(Q(f), u) = rawMapped(f, u).

For the chosen M0 connector, its source comparison scalar is one by construction.
Consequently the v3.74 object coboundary is the inverse mapped scalar; after
passing to ZMod 2 the inverse has the same additive scalar. Therefore

d00 = localizedMapped(Q(b00), u_M0)
d01 = localizedMapped(Q(b01), u_M0).

Substituting these identities into the two v3.77 naturality squares absorbs the
M0 coboundary pair into the middle-switch boundary. No claim about the M1
connector or about a hexagonal/polyhedral closure is made here.
-/

/-- Restricting the arbitrary localized lift along a raw arrow and evaluating
the full-localization view on its Q-image give the same transported source
scalar. -/
@[simp] theorem counterFactorizationLocalizedMappedSourceScalarAt_Q_map
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    {X Y : OctahedralVertex} (f : X ⟶ Y)
    {A B : CounterFactorizationFiber H X}
    (u : A ⟶ B) :
    counterFactorizationLocalizedMappedSourceScalarAt H Y
        (allMorphisms.Q.map f) u =
      counterFactorizationMappedSourceScalarAt H f u := by
  rfl

/-- Additive form of the raw/localized mapped-source bridge. -/
@[simp] theorem counterFactorizationLocalizedMappedSourceAddAt_Q_map
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    {X Y : OctahedralVertex} (f : X ⟶ Y)
    {A B : CounterFactorizationFiber H X}
    (u : A ⟶ B) :
    counterFactorizationLocalizedMappedSourceAddAt H Y
        (allMorphisms.Q.map f) u =
      Multiplicative.toAdd
        (counterFactorizationMappedSourceScalarAt H f u) := by
  rfl

/-- The b00 coboundary of the chosen M0 connector is exactly the corresponding
localized mapped-source additive scalar. -/
theorem counterFactorizationMiddleConnectorM0_b00_coboundary_eq_localizedMapped
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) :
    counterFactorizationObjectCoboundaryAddAt H b00
        (counterFactorizationMiddleConnectorM0 H A0 A1) =
      counterFactorizationLocalizedMappedSourceAddAt H H0
        (allMorphisms.Q.map b00)
        (counterFactorizationMiddleConnectorM0 H A0 A1) := by
  simp only [counterFactorizationMiddleConnectorM0]
  unfold counterFactorizationObjectCoboundaryAddAt
  rw [counterFactorizationObjectCoboundaryAt_connector H b00
    (counterFactorizationPropagatedObject H a00 A0)
    (counterFactorizationPropagatedObject H a10 A1)]
  simp only [toAdd_inv, CharTwo.neg_eq,
    counterFactorizationLocalizedMappedSourceAddAt_Q_map]

/-- The b01 coboundary of the chosen M0 connector is exactly the corresponding
localized mapped-source additive scalar. -/
theorem counterFactorizationMiddleConnectorM0_b01_coboundary_eq_localizedMapped
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) :
    counterFactorizationObjectCoboundaryAddAt H b01
        (counterFactorizationMiddleConnectorM0 H A0 A1) =
      counterFactorizationLocalizedMappedSourceAddAt H H1
        (allMorphisms.Q.map b01)
        (counterFactorizationMiddleConnectorM0 H A0 A1) := by
  simp only [counterFactorizationMiddleConnectorM0]
  unfold counterFactorizationObjectCoboundaryAddAt
  rw [counterFactorizationObjectCoboundaryAt_connector H b01
    (counterFactorizationPropagatedObject H a00 A0)
    (counterFactorizationPropagatedObject H a10 A1)]
  simp only [toAdd_inv, CharTwo.neg_eq,
    counterFactorizationLocalizedMappedSourceAddAt_Q_map]

/-- The H0 middle-switch compositor pair absorbs the b00 object coboundary. -/
theorem counterFactorization_middleSwitch_comp_pair_b10_eq_coboundary_plus_twiceMapped
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) :
    counterFactorizationLocalizedCompAddAt H H0
        counterMiddleSwitch (allMorphisms.Q.map b10)
        (counterFactorizationPropagatedObject H a00 A0) +
      counterFactorizationLocalizedCompAddAt H H0
        counterMiddleSwitch (allMorphisms.Q.map b10)
        (counterFactorizationPropagatedObject H a10 A1) =
    counterFactorizationObjectCoboundaryAddAt H b00
        (counterFactorizationMiddleConnectorM0 H A0 A1) +
      counterFactorizationLocalizedTwiceMappedSourceAddAt H H0
        counterMiddleSwitch (allMorphisms.Q.map b10)
        (counterFactorizationMiddleConnectorM0 H A0 A1) := by
  rw [counterFactorization_middleSwitch_comp_pair_b10 H A0 A1]
  rw [←
    counterFactorizationMiddleConnectorM0_b00_coboundary_eq_localizedMapped
      H A0 A1]

/-- The H1 middle-switch compositor pair absorbs the b01 object coboundary. -/
theorem counterFactorization_middleSwitch_comp_pair_b11_eq_coboundary_plus_twiceMapped
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) :
    counterFactorizationLocalizedCompAddAt H H1
        counterMiddleSwitch (allMorphisms.Q.map b11)
        (counterFactorizationPropagatedObject H a00 A0) +
      counterFactorizationLocalizedCompAddAt H H1
        counterMiddleSwitch (allMorphisms.Q.map b11)
        (counterFactorizationPropagatedObject H a10 A1) =
    counterFactorizationObjectCoboundaryAddAt H b01
        (counterFactorizationMiddleConnectorM0 H A0 A1) +
      counterFactorizationLocalizedTwiceMappedSourceAddAt H H1
        counterMiddleSwitch (allMorphisms.Q.map b11)
        (counterFactorizationMiddleConnectorM0 H A0 A1) := by
  rw [counterFactorization_middleSwitch_comp_pair_b11 H A0 A1]
  rw [←
    counterFactorizationMiddleConnectorM0_b01_coboundary_eq_localizedMapped
      H A0 A1]

/-- Aggregate M0 absorption identity.

The four compositor terms in v3.76 whose first edge is the middle switch are
the sum of the two M0 object coboundaries and the two twice-mapped connector
terms. -/
theorem counterFactorization_middleSwitch_M0_pairs_eq_coboundaries_plus_twiceMapped
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) :
    (counterFactorizationLocalizedCompAddAt H H0
        counterMiddleSwitch (allMorphisms.Q.map b10)
        (counterFactorizationPropagatedObject H a00 A0) +
      counterFactorizationLocalizedCompAddAt H H0
        counterMiddleSwitch (allMorphisms.Q.map b10)
        (counterFactorizationPropagatedObject H a10 A1)) +
    (counterFactorizationLocalizedCompAddAt H H1
        counterMiddleSwitch (allMorphisms.Q.map b11)
        (counterFactorizationPropagatedObject H a00 A0) +
      counterFactorizationLocalizedCompAddAt H H1
        counterMiddleSwitch (allMorphisms.Q.map b11)
        (counterFactorizationPropagatedObject H a10 A1)) =
    counterFactorizationObjectCoboundaryAddAt H b00
        (counterFactorizationMiddleConnectorM0 H A0 A1) +
      counterFactorizationObjectCoboundaryAddAt H b01
        (counterFactorizationMiddleConnectorM0 H A0 A1) +
      counterFactorizationLocalizedTwiceMappedSourceAddAt H H0
        counterMiddleSwitch (allMorphisms.Q.map b10)
        (counterFactorizationMiddleConnectorM0 H A0 A1) +
      counterFactorizationLocalizedTwiceMappedSourceAddAt H H1
        counterMiddleSwitch (allMorphisms.Q.map b11)
        (counterFactorizationMiddleConnectorM0 H A0 A1) := by
  rw [
    counterFactorization_middleSwitch_comp_pair_b10_eq_coboundary_plus_twiceMapped
      H A0 A1,
    counterFactorization_middleSwitch_comp_pair_b11_eq_coboundary_plus_twiceMapped
      H A0 A1]
  ac_rfl

/-!
## Boundary after v3.78

The M0 side of the v3.74/v3.76 residual is now connected exactly:

middle-switch M0 compositor pairs
  = d00 + d01 + twiceMapped_b10(u_M0) + twiceMapped_b11(u_M0).

Thus the b00 and b01 object coboundaries are no longer independent residual
freedoms once the middle-switch naturality squares are imposed.

The remaining work is on the M1 side. The next theorem unit should compare

* the two twice-mapped M0-connector terms,
* the four transported intermediate-compositor terms from v3.76, and
* the b10/b11 coboundaries of the chosen M1 connector.

That comparison determines whether a genuine six-term closure is forced before
any pentagon/hexagon or truncated-icosahedral carrier is introduced.
-/

end

end KUOS.DependentOriginationMiddleSwitchCoboundaryBridgeV3_78
