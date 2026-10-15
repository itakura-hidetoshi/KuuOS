import KUOS.DependentOriginationMiddleSwitchEndpointAlignmentV3_79

namespace KUOS.DependentOriginationMiddleSwitchM1SourceCancellationV3_80

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
open KUOS.DependentOriginationArbitraryFactorizationScalarV3_72
open KUOS.DependentOriginationFactorizationObjectCoboundaryV3_73
open KUOS.DependentOriginationArbitraryFactorizationParityV3_74
open KUOS.DependentOriginationArbitraryFactorizationLocalizedCocycleV3_75
open KUOS.DependentOriginationLocalizedCompositorNaturalityV3_77
open KUOS.DependentOriginationMiddleSwitchCoboundaryBridgeV3_78
open KUOS.DependentOriginationMiddleSwitchEndpointAlignmentV3_79

set_option autoImplicit false

noncomputable section

/-!
# M1 source-scalar cancellation v3.80

v3.79 replaces the chosen M1 connector by the transported-and-aligned M0
connector when computing the b10 and b11 object coboundaries.

For one fixed source-fiber morphism u : A ⟶ B, the two coboundaries are

delta_b10(u) = source(u) + mapped_b10(u),
delta_b11(u) = source(u) + mapped_b11(u)

after additive scalarization in ZMod 2.  The common source scalar therefore
occurs twice and vanishes.

This file isolates exactly that characteristic-two cancellation.  It reduces
the remaining M1 residual to two mapped-source terms of the aligned M0
connector, but does not yet expand those mapped terms into transported
compositors and the twice-mapped connector.
-/

/-- For one fixed source-fiber morphism, the sum of two object coboundaries
with the same source vertex loses the common source scalar in characteristic
two. -/
theorem counterFactorizationObjectCoboundaryAdd_pair_eq_mapped_pair
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    {X Y Z : OctahedralVertex}
    (f : X ⟶ Y) (g : X ⟶ Z)
    {A B : CounterFactorizationFiber H X}
    (u : A ⟶ B) :
    counterFactorizationObjectCoboundaryAddAt H f u +
        counterFactorizationObjectCoboundaryAddAt H g u =
      Multiplicative.toAdd (counterFactorizationMappedSourceScalarAt H f u) +
        Multiplicative.toAdd (counterFactorizationMappedSourceScalarAt H g u) := by
  unfold counterFactorizationObjectCoboundaryAddAt
  unfold counterFactorizationObjectCoboundaryAt
  simp only [toAdd_mul, toAdd_inv, CharTwo.neg_eq]
  calc
    (Multiplicative.toAdd (counterFactorizationSourceScalarAt H X u) +
          Multiplicative.toAdd (counterFactorizationMappedSourceScalarAt H f u)) +
        (Multiplicative.toAdd (counterFactorizationSourceScalarAt H X u) +
          Multiplicative.toAdd (counterFactorizationMappedSourceScalarAt H g u)) =
      (Multiplicative.toAdd (counterFactorizationSourceScalarAt H X u) +
          Multiplicative.toAdd (counterFactorizationSourceScalarAt H X u)) +
        (Multiplicative.toAdd (counterFactorizationMappedSourceScalarAt H f u) +
          Multiplicative.toAdd (counterFactorizationMappedSourceScalarAt H g u)) := by
            ac_rfl
    _ =
      Multiplicative.toAdd (counterFactorizationMappedSourceScalarAt H f u) +
        Multiplicative.toAdd (counterFactorizationMappedSourceScalarAt H g u) := by
          rw [CharTwo.add_self_eq_zero, zero_add]

/-- The chosen M1 b10+b11 coboundary pair is therefore exactly the two
mapped-source scalars of the aligned transported M0 connector. -/
theorem counterFactorizationMiddleConnectorM1_pair_coboundary_eq_alignedMapped
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) :
    counterFactorizationObjectCoboundaryAddAt H b10
        (counterFactorizationMiddleConnectorM1 H A0 A1) +
      counterFactorizationObjectCoboundaryAddAt H b11
        (counterFactorizationMiddleConnectorM1 H A0 A1) =
    Multiplicative.toAdd
        (counterFactorizationMappedSourceScalarAt H b10
          (counterFactorizationMiddleConnectorM0_alignedAtM1 H A0 A1)) +
      Multiplicative.toAdd
        (counterFactorizationMappedSourceScalarAt H b11
          (counterFactorizationMiddleConnectorM0_alignedAtM1 H A0 A1)) := by
  rw [counterFactorizationMiddleConnectorM1_pair_coboundary_eq_alignedM0
    H A0 A1]
  exact counterFactorizationObjectCoboundaryAdd_pair_eq_mapped_pair
    H b10 b11
    (counterFactorizationMiddleConnectorM0_alignedAtM1 H A0 A1)

/-- Full-localization form of the same M1 reduction.  This is the exact input
needed for the next theorem unit, where each mapped aligned connector is
expanded into its three middle-switch factors. -/
theorem counterFactorizationMiddleConnectorM1_pair_coboundary_eq_localizedMapped
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) :
    counterFactorizationObjectCoboundaryAddAt H b10
        (counterFactorizationMiddleConnectorM1 H A0 A1) +
      counterFactorizationObjectCoboundaryAddAt H b11
        (counterFactorizationMiddleConnectorM1 H A0 A1) =
    counterFactorizationLocalizedMappedSourceAddAt H H0
        (allMorphisms.Q.map b10)
        (counterFactorizationMiddleConnectorM0_alignedAtM1 H A0 A1) +
      counterFactorizationLocalizedMappedSourceAddAt H H1
        (allMorphisms.Q.map b11)
        (counterFactorizationMiddleConnectorM0_alignedAtM1 H A0 A1) := by
  rw [counterFactorizationMiddleConnectorM1_pair_coboundary_eq_alignedMapped
    H A0 A1]
  rw [counterFactorizationLocalizedMappedSourceAddAt_Q_map,
    counterFactorizationLocalizedMappedSourceAddAt_Q_map]

/-!
## Boundary after v3.80

The M1 residual is now reduced to two full-localization mapped-source terms:

d10 + d11
  = mapped_b10(aligned u_M0) + mapped_b11(aligned u_M0).

The source scalar of the aligned connector has disappeared completely by
characteristic-two cancellation.

The next theorem unit should expand each mapped term.  Because the aligned
connector is a composite of

1. the left endpoint mapComp' hom,
2. F(counterMiddleSwitch)(u_M0),
3. the right endpoint mapComp' inverse,

its upper mapped scalar should split into

transported compositor at A0
  + twiceMapped(u_M0)
  + transported compositor at A1.

Proving that expansion for b10 and b11 yields the candidate six-term closure.
-/

end

end KUOS.DependentOriginationMiddleSwitchM1SourceCancellationV3_80
