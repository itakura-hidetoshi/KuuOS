import KUOS.DependentOriginationTruncatedIcosahedralHexagonsV3_86
import Mathlib

namespace KUOS.DependentOriginationMiddleSwitchHexagramV3_87

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
open KUOS.DependentOriginationArbitraryTransportComparisonV3_69
open KUOS.DependentOriginationArbitraryFactorizationParityV3_74
open KUOS.DependentOriginationArbitraryFactorizationLocalizedCocycleV3_75
open KUOS.DependentOriginationLocalizedCompositorNaturalityV3_77
open KUOS.DependentOriginationMiddleSwitchCoboundaryBridgeV3_78
open KUOS.DependentOriginationMiddleSwitchEndpointAlignmentV3_79
open KUOS.DependentOriginationMiddleSwitchM1SourceCancellationV3_80
open KUOS.DependentOriginationMiddleSwitchScalarAlignmentV3_81
open KUOS.DependentOriginationMiddleSwitchSixTermExpansionV3_82
open KUOS.DependentOriginationTruncatedIcosahedralStarRefinementV3_83
open KUOS.DependentOriginationTruncatedIcosahedralHexagonsV3_86

set_option autoImplicit false

noncomputable section

/-!
# Middle-switch hexagram decomposition v3.87

The six terms proved in v3.82 are not introduced here as an arbitrary cyclic
six-tuple.  They already split canonically into two three-term families:

* the three terms transported to H0 through b10;
* the three terms transported to H1 through b11.

This is exactly the combinatorial 3 + 3 decomposition underlying a hexagram:
two triangular triples whose union has six tips.  The present theorem unit
formalizes that split before attempting any planar crossing or recursive inner
hexagon construction.

No geometric claim is made that the two algebraic triangles are already the
two Euclidean triangles of a realized Star of David.  What is proved is the
exact algebraic decomposition and the six-tip cardinality matching the
hexagram profile from v3.83.
-/

/-- The two triangular halves of the middle-switch hexagram candidate. -/
inductive MiddleSwitchHexagramTriangle
  | b10Triangle
  | b11Triangle
  deriving DecidableEq, Repr, Fintype

/-- The three positions inside one endpoint triangle. -/
inductive MiddleSwitchTriangleVertex
  | a00Transport
  | middleConnector
  | a10Transport
  deriving DecidableEq, Repr, Fintype

/-- A hexagram tip is one of three positions in one of two endpoint
triangles. -/
abbrev MiddleSwitchHexagramTip :=
  MiddleSwitchHexagramTriangle × MiddleSwitchTriangleVertex

@[simp] theorem middleSwitchHexagramTriangle_card :
    Fintype.card MiddleSwitchHexagramTriangle = 2 := by
  native_decide

@[simp] theorem middleSwitchTriangleVertex_card :
    Fintype.card MiddleSwitchTriangleVertex = 3 := by
  native_decide

@[simp] theorem middleSwitchHexagramTip_card :
    Fintype.card MiddleSwitchHexagramTip = 6 := by
  native_decide

/-- The six algebraic tips have the same arity as the recursive hexagram
profile introduced in v3.83. -/
theorem middleSwitchHexagramTip_card_eq_hexagramRefinement :
    Fintype.card MiddleSwitchHexagramTip =
      hexagramRefinement.sectors := by
  native_decide

/-- Value carried by one algebraic hexagram tip. -/
def middleSwitchHexagramTipValue
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) :
    MiddleSwitchHexagramTip → ZMod 2
  | (.b10Triangle, .a00Transport) =>
      counterFactorizationLocalizedTransportedCompAddAt H H0
        (allMorphisms.Q.map a00) counterMiddleSwitch
        (allMorphisms.Q.map b10) A0
  | (.b10Triangle, .middleConnector) =>
      counterFactorizationLocalizedTwiceMappedSourceAddAt H H0
        counterMiddleSwitch (allMorphisms.Q.map b10)
        (counterFactorizationMiddleConnectorM0 H A0 A1)
  | (.b10Triangle, .a10Transport) =>
      counterFactorizationLocalizedTransportedCompAddAt H H0
        (allMorphisms.Q.map a10) counterMiddleSwitch
        (allMorphisms.Q.map b10) A1
  | (.b11Triangle, .a00Transport) =>
      counterFactorizationLocalizedTransportedCompAddAt H H1
        (allMorphisms.Q.map a00) counterMiddleSwitch
        (allMorphisms.Q.map b11) A0
  | (.b11Triangle, .middleConnector) =>
      counterFactorizationLocalizedTwiceMappedSourceAddAt H H1
        counterMiddleSwitch (allMorphisms.Q.map b11)
        (counterFactorizationMiddleConnectorM0 H A0 A1)
  | (.b11Triangle, .a10Transport) =>
      counterFactorizationLocalizedTransportedCompAddAt H H1
        (allMorphisms.Q.map a10) counterMiddleSwitch
        (allMorphisms.Q.map b11) A1

/-- Sum of the three tips in one endpoint triangle. -/
def middleSwitchHexagramTriangleSum
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) :
    MiddleSwitchHexagramTriangle → ZMod 2
  | .b10Triangle =>
      middleSwitchHexagramTipValue H A0 A1
          (.b10Triangle, .a00Transport) +
        middleSwitchHexagramTipValue H A0 A1
          (.b10Triangle, .middleConnector) +
        middleSwitchHexagramTipValue H A0 A1
          (.b10Triangle, .a10Transport)
  | .b11Triangle =>
      middleSwitchHexagramTipValue H A0 A1
          (.b11Triangle, .a00Transport) +
        middleSwitchHexagramTipValue H A0 A1
          (.b11Triangle, .middleConnector) +
        middleSwitchHexagramTipValue H A0 A1
          (.b11Triangle, .a10Transport)

/-- The b10 triangle is exactly the three-term scalar-aligned expansion on
the H0 endpoint. -/
theorem middleSwitchHexagramTriangleSum_b10
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) :
    middleSwitchHexagramTriangleSum H A0 A1 .b10Triangle =
      counterFactorizationLocalizedMappedSourceAddAt H H0
        (allMorphisms.Q.map b10)
        (counterFactorizationMiddleConnectorM0_scalarAlignedAtM1
          H A0 A1) := by
  simpa [middleSwitchHexagramTriangleSum,
    middleSwitchHexagramTipValue] using
    (counterFactorization_scalarAligned_mappedSourceAdd
      H b10 A0 A1).symm

/-- The b11 triangle is exactly the three-term scalar-aligned expansion on
the H1 endpoint. -/
theorem middleSwitchHexagramTriangleSum_b11
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) :
    middleSwitchHexagramTriangleSum H A0 A1 .b11Triangle =
      counterFactorizationLocalizedMappedSourceAddAt H H1
        (allMorphisms.Q.map b11)
        (counterFactorizationMiddleConnectorM0_scalarAlignedAtM1
          H A0 A1) := by
  simpa [middleSwitchHexagramTriangleSum,
    middleSwitchHexagramTipValue] using
    (counterFactorization_scalarAligned_mappedSourceAdd
      H b11 A0 A1).symm

/-- The M1 coboundary pair is the sum of the two endpoint triangles.

This is the exact algebraic 3 + 3 decomposition suggested by the hexagram:
one three-term triangle at b10 and one three-term triangle at b11.
-/
theorem counterFactorizationMiddleConnectorM1_pair_coboundary_hexagram
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) :
    counterFactorizationObjectCoboundaryAddAt H b10
        (counterFactorizationMiddleConnectorM1 H A0 A1) +
      counterFactorizationObjectCoboundaryAddAt H b11
        (counterFactorizationMiddleConnectorM1 H A0 A1) =
      middleSwitchHexagramTriangleSum H A0 A1 .b10Triangle +
        middleSwitchHexagramTriangleSum H A0 A1 .b11Triangle := by
  rw [
    counterFactorizationMiddleConnectorM1_pair_coboundary_eq_scalarAlignedMapped
      H A0 A1,
    ← middleSwitchHexagramTriangleSum_b10 H A0 A1,
    ← middleSwitchHexagramTriangleSum_b11 H A0 A1
  ]

/-- Expanding the two triangles reproduces exactly the v3.82 six-term theorem,
now ordered as the two three-tip hexagram halves. -/
theorem counterFactorizationMiddleConnectorM1_pair_coboundary_hexagram_sixTips
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) :
    counterFactorizationObjectCoboundaryAddAt H b10
        (counterFactorizationMiddleConnectorM1 H A0 A1) +
      counterFactorizationObjectCoboundaryAddAt H b11
        (counterFactorizationMiddleConnectorM1 H A0 A1) =
      middleSwitchHexagramTipValue H A0 A1
          (.b10Triangle, .a00Transport) +
        middleSwitchHexagramTipValue H A0 A1
          (.b10Triangle, .middleConnector) +
        middleSwitchHexagramTipValue H A0 A1
          (.b10Triangle, .a10Transport) +
        middleSwitchHexagramTipValue H A0 A1
          (.b11Triangle, .a00Transport) +
        middleSwitchHexagramTipValue H A0 A1
          (.b11Triangle, .middleConnector) +
        middleSwitchHexagramTipValue H A0 A1
          (.b11Triangle, .a10Transport) := by
  rw [counterFactorizationMiddleConnectorM1_pair_coboundary_hexagram
    H A0 A1]
  simp only [middleSwitchHexagramTriangleSum]
  ac_rfl

/-!
## Boundary after v3.87

The v3.82 six-term expansion now has an intrinsic hexagram-like organization:

* three b10 terms form one endpoint triangle;
* three b11 terms form the other endpoint triangle;
* their sum is exactly the original M1 coboundary pair;
* the union has six tips, matching the hexagram refinement arity.

This 3 + 3 split is stronger than a bare equality of cardinalities and avoids
forcing the six terms directly onto the outer six-edge boundary.

The next theorem unit should compare these two algebraic triangles with the
two interlaced triangles of an explicit combinatorial hexagram refinement
inside one v3.86 hexagonal face.  Their intersections should then define the
candidate inner hexagon.  Only that incidence construction can justify the
recursive hexagon-to-hexagram-to-inner-hexagon interpretation.
-/

end

end KUOS.DependentOriginationMiddleSwitchHexagramV3_87
