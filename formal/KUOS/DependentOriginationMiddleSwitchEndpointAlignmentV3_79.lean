import KUOS.DependentOriginationMiddleSwitchCoboundaryBridgeV3_78

namespace KUOS.DependentOriginationMiddleSwitchEndpointAlignmentV3_79

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
open KUOS.DependentOriginationMiddleSwitchCoboundaryBridgeV3_78

set_option autoImplicit false

noncomputable section

/-!
# Middle-switch endpoint alignment v3.79

v3.78 absorbs the M0-side b00/b01 object coboundaries into the two
middle-switch naturality squares.  To reach the remaining M1-side
b10/b11 coboundaries, the transported M0 connector must first be compared
with the chosen M1 connector.

The endpoints do not match definitionally:

* transporting the M0 endpoints by counterMiddleSwitch gives
  F(p)(F(Q(a00)) A0) and F(p)(F(Q(a10)) A1);
* the canonical M1 endpoints are F(Q(a01)) A0 and F(Q(a11)) A1.

The exact localization equalities

Q(a00) ; p = Q(a01),
Q(a10) ; p = Q(a11)

therefore have to be incorporated through the pseudofunctor compositor.
Mathlib's mapComp' is the correct interface for this purpose: it packages a
chosen composite equality together with the compositor isomorphism.

This file constructs the aligned transported M0 connector and proves a second
structural fact: the object coboundary delta_f(u) depends only on the endpoints
of u, not on the chosen morphism between them.  This follows directly from the
v3.73 change-of-object equation by cancelling the common edge scalar.

Consequently the chosen M1 connector and the aligned transported M0 connector
have identical b10 and b11 coboundaries.  No scalar expansion of the aligned
connector is performed here; that is the next theorem unit.
-/

/-- The first lower edge followed by the localization middle switch is the
second lower edge, now stated in LocallyDiscrete form for mapComp'. -/
theorem counterA00_comp_middleSwitch_toLoc :
    (allMorphisms.Q.map a00).toLoc ≫ counterMiddleSwitch.toLoc =
      (allMorphisms.Q.map a01).toLoc := by
  simpa only [← Quiver.Hom.comp_toLoc] using
    congrArg (fun k => k.toLoc) counterA00_comp_middleSwitch

/-- The same endpoint equality for the L1 lower edge. -/
theorem counterA10_comp_middleSwitch_toLoc :
    (allMorphisms.Q.map a10).toLoc ≫ counterMiddleSwitch.toLoc =
      (allMorphisms.Q.map a11).toLoc := by
  simpa only [← Quiver.Hom.comp_toLoc] using
    congrArg (fun k => k.toLoc) counterA10_comp_middleSwitch

/-- The M0 connector transported through the middle switch, with both endpoints
aligned to the canonical M1 fibers using mapComp'.

The left mapComp' hom takes the canonical a01 endpoint into the iterated
a00-then-middle-switch endpoint.  The right mapComp' inverse returns from the
iterated a10-then-middle-switch endpoint to the canonical a11 endpoint. -/
noncomputable def counterFactorizationMiddleConnectorM0_alignedAtM1
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) :
    counterFactorizationPropagatedObject H a01 A0 ⟶
      counterFactorizationPropagatedObject H a11 A1 := by
  let F := counterFactorizationLocalizationView H
  exact
    (F.mapComp'
      (allMorphisms.Q.map a00).toLoc counterMiddleSwitch.toLoc
      (allMorphisms.Q.map a01).toLoc
      counterA00_comp_middleSwitch_toLoc).hom.toNatTrans.app A0 ≫
    (F.map counterMiddleSwitch.toLoc).toFunctor.map
      (counterFactorizationMiddleConnectorM0 H A0 A1) ≫
    (F.mapComp'
      (allMorphisms.Q.map a10).toLoc counterMiddleSwitch.toLoc
      (allMorphisms.Q.map a11).toLoc
      counterA10_comp_middleSwitch_toLoc).inv.toNatTrans.app A1

/-- The multiplicative object coboundary depends only on its two source-fiber
endpoints.

Both u and v express the same change of source object.  Applying the v3.73
change-of-object equation to each gives the same right multiplication by the
edge scalar, which can be cancelled in C2. -/
theorem counterFactorizationObjectCoboundaryAt_eq_of_parallel
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    {X Y : OctahedralVertex} (f : X ⟶ Y)
    {A B : CounterFactorizationFiber H X}
    (u v : A ⟶ B) :
    counterFactorizationObjectCoboundaryAt H f u =
      counterFactorizationObjectCoboundaryAt H f v := by
  have hu := counterFactorizationEdgeScalarAt_change_object H f u
  have hv := counterFactorizationEdgeScalarAt_change_object H f v
  have h :
      counterFactorizationObjectCoboundaryAt H f u *
          counterFactorizationEdgeScalarAt H f A =
        counterFactorizationObjectCoboundaryAt H f v *
          counterFactorizationEdgeScalarAt H f A :=
    hu.symm.trans hv
  exact mul_right_cancel h

/-- Additive form of endpoint-independence of the object coboundary. -/
theorem counterFactorizationObjectCoboundaryAddAt_eq_of_parallel
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    {X Y : OctahedralVertex} (f : X ⟶ Y)
    {A B : CounterFactorizationFiber H X}
    (u v : A ⟶ B) :
    counterFactorizationObjectCoboundaryAddAt H f u =
      counterFactorizationObjectCoboundaryAddAt H f v := by
  exact congrArg (@Multiplicative.toAdd (ZMod 2))
    (counterFactorizationObjectCoboundaryAt_eq_of_parallel H f u v)

/-- The chosen M1 connector and the aligned transported M0 connector have the
same b10 object coboundary. -/
theorem counterFactorizationMiddleConnectorM1_b10_coboundary_eq_alignedM0
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) :
    counterFactorizationObjectCoboundaryAddAt H b10
        (counterFactorizationMiddleConnectorM1 H A0 A1) =
      counterFactorizationObjectCoboundaryAddAt H b10
        (counterFactorizationMiddleConnectorM0_alignedAtM1 H A0 A1) := by
  exact counterFactorizationObjectCoboundaryAddAt_eq_of_parallel H b10
    (counterFactorizationMiddleConnectorM1 H A0 A1)
    (counterFactorizationMiddleConnectorM0_alignedAtM1 H A0 A1)

/-- The analogous equality for the b11 object coboundary. -/
theorem counterFactorizationMiddleConnectorM1_b11_coboundary_eq_alignedM0
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) :
    counterFactorizationObjectCoboundaryAddAt H b11
        (counterFactorizationMiddleConnectorM1 H A0 A1) =
      counterFactorizationObjectCoboundaryAddAt H b11
        (counterFactorizationMiddleConnectorM0_alignedAtM1 H A0 A1) := by
  exact counterFactorizationObjectCoboundaryAddAt_eq_of_parallel H b11
    (counterFactorizationMiddleConnectorM1 H A0 A1)
    (counterFactorizationMiddleConnectorM0_alignedAtM1 H A0 A1)

/-- Aggregate replacement of the two chosen M1 coboundaries by the single
aligned transported M0 connector. -/
theorem counterFactorizationMiddleConnectorM1_pair_coboundary_eq_alignedM0
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) :
    counterFactorizationObjectCoboundaryAddAt H b10
        (counterFactorizationMiddleConnectorM1 H A0 A1) +
      counterFactorizationObjectCoboundaryAddAt H b11
        (counterFactorizationMiddleConnectorM1 H A0 A1) =
    counterFactorizationObjectCoboundaryAddAt H b10
        (counterFactorizationMiddleConnectorM0_alignedAtM1 H A0 A1) +
      counterFactorizationObjectCoboundaryAddAt H b11
        (counterFactorizationMiddleConnectorM0_alignedAtM1 H A0 A1) := by
  rw [
    counterFactorizationMiddleConnectorM1_b10_coboundary_eq_alignedM0
      H A0 A1,
    counterFactorizationMiddleConnectorM1_b11_coboundary_eq_alignedM0
      H A0 A1]

/-!
## Boundary after v3.79

The M1 residual no longer depends on the arbitrary choice of the canonical M1
connector.  It can be computed using the connector obtained by transporting the
already-fixed M0 connector through counterMiddleSwitch and aligning its
endpoints with the two mapComp' isomorphisms.

The next theorem unit should scalarize this aligned connector.

For b10 and b11 separately, mapping the aligned connector to the upper endpoint
breaks into exactly three pieces:

* transported compositor at the A0 endpoint,
* twice-mapped M0 connector,
* inverse transported compositor at the A1 endpoint.

When the b10 and b11 coboundaries are added, the common source scalar of the
aligned connector appears twice and vanishes in ZMod 2.  This is the candidate
six-term closure:

d10 + d11
  = four transported compositor terms
      + twiceMapped_b10(u_M0)
      + twiceMapped_b11(u_M0).

That equality must be proved directly before introducing any hexagonal or
truncated-icosahedral carrier.
-/

end

end KUOS.DependentOriginationMiddleSwitchEndpointAlignmentV3_79
