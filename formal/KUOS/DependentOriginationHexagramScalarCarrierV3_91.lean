import KUOS.DependentOriginationTruncatedIcosahedralRecursiveRefinementV3_90
import Mathlib

namespace KUOS.DependentOriginationHexagramScalarCarrierV3_91

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
open KUOS.DependentOriginationArbitraryFactorizationParityV3_74
open KUOS.DependentOriginationMiddleSwitchHexagramV3_87
open KUOS.DependentOriginationHexagramInnerHexagonV3_88

set_option autoImplicit false

noncomputable section

/-!
# Scalar-valued hexagram carrier v3.91

v3.87 proves that the remaining M1 coboundary pair is exactly six scalar
contributions organized as two three-term endpoint triangles.  v3.88 places
those six algebraic tips on an explicit cyclic hexagram carrier.

This file performs the first value-level transport onto that carrier.

Each outer hexagram tip is assigned the corresponding v3.87 scalar through
the explicit bijection from v3.88.  The resulting six values admit two useful
orders:

* triangle order: t0,t2,t4 followed by t1,t5,t3;
* cyclic order:   t0,t1,t2,t3,t4,t5.

The first is definitionally aligned with the two endpoint triangles proved in
v3.87.  The second is the actual cyclic order of the outer hexagonal carrier.
Commutativity and associativity in ZMod 2 identify the two total sums.

Thus the v3.82/v3.87 M1 residual is now genuinely a scalar-valued six-tip
hexagram carrier.  No value has yet been assigned to the inner hexagon.
-/

/-- Scalar carried by one outer hexagram tip. -/
noncomputable def counterFactorizationHexagramOuterTipAdd
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1)
    (t : HexagramOuterTip) : ZMod 2 :=
  middleSwitchHexagramTipValue H A0 A1
    (hexagramOuterTipToAlgebraic t)

/-- Sum on the even-tip triangle t0-t2-t4. -/
noncomputable def counterFactorizationHexagramEvenTriangleAdd
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) : ZMod 2 :=
  counterFactorizationHexagramOuterTipAdd H A0 A1 .t0 +
    counterFactorizationHexagramOuterTipAdd H A0 A1 .t2 +
    counterFactorizationHexagramOuterTipAdd H A0 A1 .t4

/-- Sum on the odd-tip triangle t1-t5-t3, ordered to match the v3.87 b11
triangle a00-middle-a10. -/
noncomputable def counterFactorizationHexagramOddTriangleAdd
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) : ZMod 2 :=
  counterFactorizationHexagramOuterTipAdd H A0 A1 .t1 +
    counterFactorizationHexagramOuterTipAdd H A0 A1 .t5 +
    counterFactorizationHexagramOuterTipAdd H A0 A1 .t3

/-- The even-tip triangle is exactly the b10 algebraic triangle. -/
theorem counterFactorizationHexagramEvenTriangleAdd_eq_b10
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) :
    counterFactorizationHexagramEvenTriangleAdd H A0 A1 =
      middleSwitchHexagramTriangleSum H A0 A1 .b10Triangle := by
  rfl

/-- The odd-tip triangle is exactly the b11 algebraic triangle. -/
theorem counterFactorizationHexagramOddTriangleAdd_eq_b11
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) :
    counterFactorizationHexagramOddTriangleAdd H A0 A1 =
      middleSwitchHexagramTriangleSum H A0 A1 .b11Triangle := by
  rfl

/-- Six-tip sum in the two-triangle order inherited from v3.87. -/
noncomputable def counterFactorizationHexagramTwoTriangleAdd
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) : ZMod 2 :=
  counterFactorizationHexagramEvenTriangleAdd H A0 A1 +
    counterFactorizationHexagramOddTriangleAdd H A0 A1

/-- Six-tip sum in the cyclic order of the outer hexagon. -/
noncomputable def counterFactorizationHexagramOuterCyclicAdd
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) : ZMod 2 :=
  counterFactorizationHexagramOuterTipAdd H A0 A1 .t0 +
    counterFactorizationHexagramOuterTipAdd H A0 A1 .t1 +
    counterFactorizationHexagramOuterTipAdd H A0 A1 .t2 +
    counterFactorizationHexagramOuterTipAdd H A0 A1 .t3 +
    counterFactorizationHexagramOuterTipAdd H A0 A1 .t4 +
    counterFactorizationHexagramOuterTipAdd H A0 A1 .t5

/-- The M1 coboundary pair is exactly the two-triangle hexagram sum. -/
theorem counterFactorizationMiddleConnectorM1_pair_coboundary_eq_hexagramTwoTriangleAdd
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) :
    counterFactorizationObjectCoboundaryAddAt H b10
        (counterFactorizationMiddleConnectorM1 H A0 A1) +
      counterFactorizationObjectCoboundaryAddAt H b11
        (counterFactorizationMiddleConnectorM1 H A0 A1) =
      counterFactorizationHexagramTwoTriangleAdd H A0 A1 := by
  rw [counterFactorizationMiddleConnectorM1_pair_coboundary_hexagram
    H A0 A1]
  rw [
    ← counterFactorizationHexagramEvenTriangleAdd_eq_b10 H A0 A1,
    ← counterFactorizationHexagramOddTriangleAdd_eq_b11 H A0 A1
  ]
  rfl

/-- Reordering the same six tip values from the two triangle order to the
actual cyclic order of the outer hexagon preserves their total scalar. -/
theorem counterFactorizationHexagramTwoTriangleAdd_eq_outerCyclicAdd
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) :
    counterFactorizationHexagramTwoTriangleAdd H A0 A1 =
      counterFactorizationHexagramOuterCyclicAdd H A0 A1 := by
  unfold counterFactorizationHexagramTwoTriangleAdd
  unfold counterFactorizationHexagramEvenTriangleAdd
  unfold counterFactorizationHexagramOddTriangleAdd
  unfold counterFactorizationHexagramOuterCyclicAdd
  ac_rfl

/-- The remaining M1 coboundary pair is therefore exactly the scalar sum
around the six outer tips in cyclic order. -/
theorem counterFactorizationMiddleConnectorM1_pair_coboundary_eq_hexagramOuterCyclicAdd
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) :
    counterFactorizationObjectCoboundaryAddAt H b10
        (counterFactorizationMiddleConnectorM1 H A0 A1) +
      counterFactorizationObjectCoboundaryAddAt H b11
        (counterFactorizationMiddleConnectorM1 H A0 A1) =
      counterFactorizationHexagramOuterCyclicAdd H A0 A1 := by
  rw [
    counterFactorizationMiddleConnectorM1_pair_coboundary_eq_hexagramTwoTriangleAdd
      H A0 A1,
    counterFactorizationHexagramTwoTriangleAdd_eq_outerCyclicAdd
      H A0 A1
  ]

/-!
## Boundary after v3.91

The combinatorial hexagram carrier now carries the actual v3.82/v3.87 scalar
data.  The M1 residual has two simultaneously certified presentations:

* two interlaced three-tip triangles;
* one cyclic six-tip outer boundary.

The presentations have the same total value by AC normalization in ZMod 2.

The next theorem unit should test the most naive descent of this scalar field
onto the six star edges: assign to each star edge the ZMod 2 coboundary of its
two endpoint tip values.  Because every outer tip has degree two in the union
of the two triangles, the total induced star-edge coboundary should vanish.
If formalized, that will show that plain endpoint coboundary transport cannot
carry a nonzero recursive obstruction into the inner hexagon; genuinely higher
crossing/compositor data would then be required.
-/

end

end KUOS.DependentOriginationHexagramScalarCarrierV3_91
