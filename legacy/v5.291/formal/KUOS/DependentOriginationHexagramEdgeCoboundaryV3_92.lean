import KUOS.DependentOriginationHexagramScalarCarrierV3_91
import Mathlib

namespace KUOS.DependentOriginationHexagramEdgeCoboundaryV3_92

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
open KUOS.DependentOriginationArbitraryFactorizationParityV3_74
open KUOS.DependentOriginationHexagramInnerHexagonV3_88
open KUOS.DependentOriginationHexagramScalarCarrierV3_91

set_option autoImplicit false

noncomputable section

/-!
# Hexagram endpoint coboundary and the inner-boundary zero test v3.92

v3.91 places the exact middle-switch scalar residual on the six outer tips of
the combinatorial hexagram.  This file tests the simplest possible descent of
that scalar field toward the inner hexagon.

To each star edge we assign the ZMod 2 coboundary of its two endpoint tip
values.  In characteristic two, subtraction and addition agree, so this is
represented by the sum of the endpoint values.

The union of the two interlaced triangles has degree two at every outer tip.
Consequently the total of the six induced star-edge coboundaries is zero:
every outer tip value appears exactly twice.

The six edges encountered by the inner hexagon are precisely those same six
star edges, only in alternating cyclic order.  Therefore the induced inner
boundary total is also zero.

This is an important negative result: plain endpoint-coboundary descent cannot
transport a nonzero outer middle-switch residual into the recursive inner
hexagon.  Any nontrivial recursive obstruction must use additional higher
crossing/compositor data rather than only the six outer tip values.
-/

/-- The endpoint coboundary on one star edge. -/
noncomputable def counterFactorizationHexagramStarEdgeCoboundaryAdd
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) :
    HexagramStarEdge → ZMod 2
  | .up0 =>
      counterFactorizationHexagramOuterTipAdd H A0 A1 .t0 +
        counterFactorizationHexagramOuterTipAdd H A0 A1 .t2
  | .up1 =>
      counterFactorizationHexagramOuterTipAdd H A0 A1 .t2 +
        counterFactorizationHexagramOuterTipAdd H A0 A1 .t4
  | .up2 =>
      counterFactorizationHexagramOuterTipAdd H A0 A1 .t4 +
        counterFactorizationHexagramOuterTipAdd H A0 A1 .t0
  | .down0 =>
      counterFactorizationHexagramOuterTipAdd H A0 A1 .t1 +
        counterFactorizationHexagramOuterTipAdd H A0 A1 .t3
  | .down1 =>
      counterFactorizationHexagramOuterTipAdd H A0 A1 .t3 +
        counterFactorizationHexagramOuterTipAdd H A0 A1 .t5
  | .down2 =>
      counterFactorizationHexagramOuterTipAdd H A0 A1 .t5 +
        counterFactorizationHexagramOuterTipAdd H A0 A1 .t1

/-- Total endpoint coboundary on all six star edges, grouped by the two
triangles. -/
noncomputable def counterFactorizationHexagramStarEdgeTotalCoboundaryAdd
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) : ZMod 2 :=
  counterFactorizationHexagramStarEdgeCoboundaryAdd H A0 A1 .up0 +
    counterFactorizationHexagramStarEdgeCoboundaryAdd H A0 A1 .up1 +
    counterFactorizationHexagramStarEdgeCoboundaryAdd H A0 A1 .up2 +
    counterFactorizationHexagramStarEdgeCoboundaryAdd H A0 A1 .down0 +
    counterFactorizationHexagramStarEdgeCoboundaryAdd H A0 A1 .down1 +
    counterFactorizationHexagramStarEdgeCoboundaryAdd H A0 A1 .down2

/-- Every outer tip occurs twice in the six star edges, so the total endpoint
coboundary vanishes in ZMod 2. -/
theorem counterFactorizationHexagramStarEdgeTotalCoboundaryAdd_eq_zero
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) :
    counterFactorizationHexagramStarEdgeTotalCoboundaryAdd H A0 A1 = 0 := by
  unfold counterFactorizationHexagramStarEdgeTotalCoboundaryAdd
  unfold counterFactorizationHexagramStarEdgeCoboundaryAdd
  calc
    (counterFactorizationHexagramOuterTipAdd H A0 A1 .t0 +
          counterFactorizationHexagramOuterTipAdd H A0 A1 .t2) +
        (counterFactorizationHexagramOuterTipAdd H A0 A1 .t2 +
          counterFactorizationHexagramOuterTipAdd H A0 A1 .t4) +
        (counterFactorizationHexagramOuterTipAdd H A0 A1 .t4 +
          counterFactorizationHexagramOuterTipAdd H A0 A1 .t0) +
        (counterFactorizationHexagramOuterTipAdd H A0 A1 .t1 +
          counterFactorizationHexagramOuterTipAdd H A0 A1 .t3) +
        (counterFactorizationHexagramOuterTipAdd H A0 A1 .t3 +
          counterFactorizationHexagramOuterTipAdd H A0 A1 .t5) +
        (counterFactorizationHexagramOuterTipAdd H A0 A1 .t5 +
          counterFactorizationHexagramOuterTipAdd H A0 A1 .t1) =
      (counterFactorizationHexagramOuterTipAdd H A0 A1 .t0 +
          counterFactorizationHexagramOuterTipAdd H A0 A1 .t0) +
        (counterFactorizationHexagramOuterTipAdd H A0 A1 .t1 +
          counterFactorizationHexagramOuterTipAdd H A0 A1 .t1) +
        (counterFactorizationHexagramOuterTipAdd H A0 A1 .t2 +
          counterFactorizationHexagramOuterTipAdd H A0 A1 .t2) +
        (counterFactorizationHexagramOuterTipAdd H A0 A1 .t3 +
          counterFactorizationHexagramOuterTipAdd H A0 A1 .t3) +
        (counterFactorizationHexagramOuterTipAdd H A0 A1 .t4 +
          counterFactorizationHexagramOuterTipAdd H A0 A1 .t4) +
        (counterFactorizationHexagramOuterTipAdd H A0 A1 .t5 +
          counterFactorizationHexagramOuterTipAdd H A0 A1 .t5) := by
            ac_rfl
    _ = 0 := by
      simp only [CharTwo.add_self_eq_zero, zero_add, add_zero]

/-- The induced endpoint-coboundary total in the cyclic order of the inner
hexagon.  The order follows x0,...,x5 from v3.88:
up0, down0, up1, down1, up2, down2. -/
noncomputable def counterFactorizationHexagramInnerBoundaryEndpointCoboundaryAdd
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) : ZMod 2 :=
  counterFactorizationHexagramStarEdgeCoboundaryAdd H A0 A1 .up0 +
    counterFactorizationHexagramStarEdgeCoboundaryAdd H A0 A1 .down0 +
    counterFactorizationHexagramStarEdgeCoboundaryAdd H A0 A1 .up1 +
    counterFactorizationHexagramStarEdgeCoboundaryAdd H A0 A1 .down1 +
    counterFactorizationHexagramStarEdgeCoboundaryAdd H A0 A1 .up2 +
    counterFactorizationHexagramStarEdgeCoboundaryAdd H A0 A1 .down2

/-- Inner cyclic order and triangle-grouped order contain exactly the same six
star-edge coboundaries. -/
theorem counterFactorizationHexagramInnerBoundaryEndpointCoboundaryAdd_eq_starTotal
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) :
    counterFactorizationHexagramInnerBoundaryEndpointCoboundaryAdd H A0 A1 =
      counterFactorizationHexagramStarEdgeTotalCoboundaryAdd H A0 A1 := by
  unfold counterFactorizationHexagramInnerBoundaryEndpointCoboundaryAdd
  unfold counterFactorizationHexagramStarEdgeTotalCoboundaryAdd
  ac_rfl

/-- Therefore the naive endpoint-coboundary carried by the inner hexagonal
boundary is always zero. -/
theorem counterFactorizationHexagramInnerBoundaryEndpointCoboundaryAdd_eq_zero
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) :
    counterFactorizationHexagramInnerBoundaryEndpointCoboundaryAdd H A0 A1 =
      0 := by
  rw [
    counterFactorizationHexagramInnerBoundaryEndpointCoboundaryAdd_eq_starTotal
      H A0 A1,
    counterFactorizationHexagramStarEdgeTotalCoboundaryAdd_eq_zero
      H A0 A1
  ]

/-- If the scalar-valued outer hexagram has nonzero total, the naive inner
endpoint-coboundary cannot equal it. -/
theorem counterFactorizationHexagramInnerBoundary_ne_outer_of_outer_ne_zero
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1)
    (hOuter :
      counterFactorizationHexagramOuterCyclicAdd H A0 A1 ≠ 0) :
    counterFactorizationHexagramInnerBoundaryEndpointCoboundaryAdd H A0 A1 ≠
      counterFactorizationHexagramOuterCyclicAdd H A0 A1 := by
  intro hEq
  have hZero :
      counterFactorizationHexagramOuterCyclicAdd H A0 A1 = 0 := by
    rw [
      ← hEq,
      counterFactorizationHexagramInnerBoundaryEndpointCoboundaryAdd_eq_zero
        H A0 A1
    ]
  exact hOuter hZero

/-- Equivalently, a nonzero M1 coboundary residual cannot be carried into the
inner hexagon by this naive endpoint-coboundary construction. -/
theorem counterFactorizationHexagramInnerBoundary_ne_M1Residual_of_nonzero
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1)
    (hResidual :
      counterFactorizationObjectCoboundaryAddAt H b10
          (counterFactorizationMiddleConnectorM1 H A0 A1) +
        counterFactorizationObjectCoboundaryAddAt H b11
          (counterFactorizationMiddleConnectorM1 H A0 A1) ≠ 0) :
    counterFactorizationHexagramInnerBoundaryEndpointCoboundaryAdd H A0 A1 ≠
      counterFactorizationObjectCoboundaryAddAt H b10
          (counterFactorizationMiddleConnectorM1 H A0 A1) +
        counterFactorizationObjectCoboundaryAddAt H b11
          (counterFactorizationMiddleConnectorM1 H A0 A1) := by
  intro hEq
  have hZero :
      counterFactorizationObjectCoboundaryAddAt H b10
          (counterFactorizationMiddleConnectorM1 H A0 A1) +
        counterFactorizationObjectCoboundaryAddAt H b11
          (counterFactorizationMiddleConnectorM1 H A0 A1) = 0 := by
    rw [
      ← hEq,
      counterFactorizationHexagramInnerBoundaryEndpointCoboundaryAdd_eq_zero
        H A0 A1
    ]
  exact hResidual hZero

/-!
## Boundary after v3.92

The first recursive scalar-transport test has a definite answer.

The outer six-tip field may carry the full M1 residual, but its naive
endpoint-coboundary on the six star edges always has zero total.  The induced
inner hexagonal boundary therefore also has zero endpoint-coboundary total.

So a nonzero recursive obstruction, if it persists under the
hexagon -> hexagram -> inner-hexagon refinement, cannot be represented solely
by endpoint differences of the six outer scalar values.  The next theorem
unit must introduce genuinely higher data at the crossings: for example a
crossing/interchanger scalar, a compositor defect attached to the crossing
square, or an explicit descent obstruction comparing the two triangular
presentations.

This identifies a concrete obstruction boundary rather than assuming
self-similar preservation.
-/

end

end KUOS.DependentOriginationHexagramEdgeCoboundaryV3_92
