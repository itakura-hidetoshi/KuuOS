import KUOS.DependentOriginationMiddleSwitchM1SourceCancellationV3_80

namespace KUOS.DependentOriginationMiddleSwitchScalarAlignmentV3_81

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
open KUOS.DependentOriginationArbitraryTransportComparisonV3_69
open KUOS.DependentOriginationArbitraryFactorizationScalarV3_72
open KUOS.DependentOriginationFactorizationObjectCoboundaryV3_73
open KUOS.DependentOriginationArbitraryFactorizationParityV3_74
open KUOS.DependentOriginationArbitraryFactorizationLocalizedCocycleV3_75
open KUOS.DependentOriginationLocalizedCompositorNaturalityV3_77
open KUOS.DependentOriginationMiddleSwitchCoboundaryBridgeV3_78
open KUOS.DependentOriginationMiddleSwitchEndpointAlignmentV3_79
open KUOS.DependentOriginationMiddleSwitchM1SourceCancellationV3_80

set_option autoImplicit false

noncomputable section

/-!
# Scalar-friendly middle-switch alignment v3.81

v3.79 constructs the transported M0 connector on the canonical M1 endpoints
using mapComp'.  That is the conceptual endpoint-alignment interface.

For the next scalar calculation it is useful to expose the same alignment as an
explicit five-factor composite:

1. equality transport from the canonical a01 endpoint to the composite
   a00-then-middle-switch endpoint;
2. the ordinary mapComp hom at A0;
3. the transported M0 connector;
4. the ordinary mapComp inverse at A1;
5. equality transport to the canonical a11 endpoint.

This form separates the two equality transports, whose endpoint C2 scalars are
units, from the two genuine compositor factors and the transported connector.

Because v3.79 proves that an object coboundary depends only on the endpoints of
the source-fiber morphism, the chosen M1 connector may be replaced by this
scalar-friendly aligned connector without changing d10 or d11.
-/

/-- Equality between the direct a01 endpoint and the source object of the
ordinary a00/middle-switch compositor. -/
theorem counterFactorizationMiddleSwitch_sourceEndpoint_eq
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0) :
    ((counterFactorizationLocalizationView H).map
        (allMorphisms.Q.map a01).toLoc).toFunctor.obj A0 =
      ((counterFactorizationLocalizationView H).map
        ((allMorphisms.Q.map a00).toLoc ≫ counterMiddleSwitch.toLoc)).toFunctor.obj A0 := by
  rw [counterA00_comp_middleSwitch_toLoc]

/-- Equality between the target object of the ordinary a10/middle-switch
compositor and the direct a11 endpoint. -/
theorem counterFactorizationMiddleSwitch_targetEndpoint_eq
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A1 : CounterFactorizationFiber H L1) :
    ((counterFactorizationLocalizationView H).map
        ((allMorphisms.Q.map a10).toLoc ≫ counterMiddleSwitch.toLoc)).toFunctor.obj A1 =
      ((counterFactorizationLocalizationView H).map
        (allMorphisms.Q.map a11).toLoc).toFunctor.obj A1 := by
  rw [counterA10_comp_middleSwitch_toLoc]

/-- A scalar-friendly representative of the transported M0 connector on the
canonical M1 endpoints.

Unlike the v3.79 mapComp' expression, the equality transports are explicit,
so the next theorem unit can discard their endpoint scalars as units before
reading the remaining three nontrivial factors. -/
noncomputable def counterFactorizationMiddleConnectorM0_scalarAlignedAtM1
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) :
    counterFactorizationPropagatedObject H a01 A0 ⟶
      counterFactorizationPropagatedObject H a11 A1 := by
  let F := counterFactorizationLocalizationView H
  exact
    eqToHom (counterFactorizationMiddleSwitch_sourceEndpoint_eq H A0) ≫
    (F.mapComp
      (allMorphisms.Q.map a00).toLoc counterMiddleSwitch.toLoc).hom.toNatTrans.app A0 ≫
    (F.map counterMiddleSwitch.toLoc).toFunctor.map
      (counterFactorizationMiddleConnectorM0 H A0 A1) ≫
    (F.mapComp
      (allMorphisms.Q.map a10).toLoc counterMiddleSwitch.toLoc).inv.toNatTrans.app A1 ≫
    eqToHom (counterFactorizationMiddleSwitch_targetEndpoint_eq H A1)

/-- The chosen M1 b10 coboundary can be computed with the scalar-friendly
aligned M0 connector. -/
theorem counterFactorizationMiddleConnectorM1_b10_coboundary_eq_scalarAlignedM0
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) :
    counterFactorizationObjectCoboundaryAddAt H b10
        (counterFactorizationMiddleConnectorM1 H A0 A1) =
      counterFactorizationObjectCoboundaryAddAt H b10
        (counterFactorizationMiddleConnectorM0_scalarAlignedAtM1 H A0 A1) := by
  exact counterFactorizationObjectCoboundaryAddAt_eq_of_parallel H b10
    (counterFactorizationMiddleConnectorM1 H A0 A1)
    (counterFactorizationMiddleConnectorM0_scalarAlignedAtM1 H A0 A1)

/-- The analogous scalar-friendly replacement for b11. -/
theorem counterFactorizationMiddleConnectorM1_b11_coboundary_eq_scalarAlignedM0
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) :
    counterFactorizationObjectCoboundaryAddAt H b11
        (counterFactorizationMiddleConnectorM1 H A0 A1) =
      counterFactorizationObjectCoboundaryAddAt H b11
        (counterFactorizationMiddleConnectorM0_scalarAlignedAtM1 H A0 A1) := by
  exact counterFactorizationObjectCoboundaryAddAt_eq_of_parallel H b11
    (counterFactorizationMiddleConnectorM1 H A0 A1)
    (counterFactorizationMiddleConnectorM0_scalarAlignedAtM1 H A0 A1)

/-- The full M1 coboundary pair can therefore be read as the two upper
mapped-source scalars of the scalar-friendly aligned connector. -/
theorem counterFactorizationMiddleConnectorM1_pair_coboundary_eq_scalarAlignedMapped
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
        (counterFactorizationMiddleConnectorM0_scalarAlignedAtM1 H A0 A1) +
      counterFactorizationLocalizedMappedSourceAddAt H H1
        (allMorphisms.Q.map b11)
        (counterFactorizationMiddleConnectorM0_scalarAlignedAtM1 H A0 A1) := by
  rw [
    counterFactorizationMiddleConnectorM1_b10_coboundary_eq_scalarAlignedM0
      H A0 A1,
    counterFactorizationMiddleConnectorM1_b11_coboundary_eq_scalarAlignedM0
      H A0 A1]
  have hPair :=
    counterFactorizationObjectCoboundaryAdd_pair_eq_mapped_pair
      H b10 b11
      (counterFactorizationMiddleConnectorM0_scalarAlignedAtM1 H A0 A1)
  rw [counterFactorizationLocalizedMappedSourceAddAt_Q_map,
    counterFactorizationLocalizedMappedSourceAddAt_Q_map]
  exact hPair

/-!
## Boundary after v3.81

The M1 residual is now expressed using a connector whose scalar structure is
fully explicit:

eqToHom
  ; mapComp(a00, middleSwitch).hom
  ; F(middleSwitch)(u_M0)
  ; mapComp(a10, middleSwitch).inv
  ; eqToHom.

The next theorem unit should map this five-factor composite along b10 and b11.

The two equality-transport factors have unit endpoint scalar.  The remaining
three factors should become

* transported compositor at A0,
* twice-mapped M0 connector,
* inverse transported compositor at A1.

After additive scalarization in ZMod 2, the inverse contributes the same class.
This is the direct route to the candidate six-term closure.
-/

end

end KUOS.DependentOriginationMiddleSwitchScalarAlignmentV3_81
