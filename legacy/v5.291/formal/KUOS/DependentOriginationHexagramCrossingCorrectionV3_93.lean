import KUOS.DependentOriginationHexagramEdgeCoboundaryV3_92
import Mathlib

namespace KUOS.DependentOriginationHexagramCrossingCorrectionV3_93

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
open KUOS.DependentOriginationArbitraryFactorizationParityV3_74
open KUOS.DependentOriginationHexagramInnerHexagonV3_88
open KUOS.DependentOriginationHexagramScalarCarrierV3_91
open KUOS.DependentOriginationHexagramEdgeCoboundaryV3_92

set_option autoImplicit false

noncomputable section

/-!
# Crossing-correction obligation for recursive hexagram descent v3.93

v3.92 proves that the naive endpoint coboundary induced from the six outer
hexagram tip values has zero total on the recursive inner hexagon.

Therefore any nonzero recursive obstruction must enter through additional
higher data located at the six crossings.  This file isolates that missing
datum without assuming a categorical construction for it yet.

A crossing-correction datum assigns one ZMod 2 scalar to each of the six
inner crossings x0,...,x5.  The corrected inner boundary is defined as

naive endpoint boundary + total crossing correction.

Since the naive term is already proved zero, the corrected inner obstruction
is exactly the total crossing correction.  Consequently preservation of the
outer hexagram residual, or equivalently the original M1 coboundary residual,
is equivalent to one explicit six-crossing sum equation.

This theorem unit turns the next problem into a precise interface obligation:
construct crossing corrections from genuine pseudofunctor/compositor
coherence and prove their six-term total has the required value.
-/

/-- Abstract higher correction carried by the six hexagram crossings. -/
structure HexagramCrossingCorrectionData where
  correction : HexagramInnerVertex → ZMod 2

/-- Total higher correction around the six inner crossings in cyclic order. -/
noncomputable def HexagramCrossingCorrectionData.total
    (K : HexagramCrossingCorrectionData) : ZMod 2 :=
  K.correction .x0 +
    K.correction .x1 +
    K.correction .x2 +
    K.correction .x3 +
    K.correction .x4 +
    K.correction .x5

/-- Corrected inner-hexagon boundary: naive endpoint coboundary plus the
crossing contribution. -/
noncomputable def counterFactorizationHexagramCorrectedInnerBoundaryAdd
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1)
    (K : HexagramCrossingCorrectionData) : ZMod 2 :=
  counterFactorizationHexagramInnerBoundaryEndpointCoboundaryAdd H A0 A1 +
    K.total

/-- Because the naive endpoint contribution vanishes, the corrected inner
boundary is exactly the crossing-correction total. -/
theorem counterFactorizationHexagramCorrectedInnerBoundaryAdd_eq_crossingTotal
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1)
    (K : HexagramCrossingCorrectionData) :
    counterFactorizationHexagramCorrectedInnerBoundaryAdd H A0 A1 K =
      K.total := by
  unfold counterFactorizationHexagramCorrectedInnerBoundaryAdd
  rw [
    counterFactorizationHexagramInnerBoundaryEndpointCoboundaryAdd_eq_zero
      H A0 A1
  ]
  exact zero_add K.total

/-- Exact preservation of the scalar-valued outer hexagram is equivalent to
one equation for the six crossing corrections. -/
theorem counterFactorizationHexagram_correctedInner_eq_outer_iff_crossingTotal
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1)
    (K : HexagramCrossingCorrectionData) :
    counterFactorizationHexagramCorrectedInnerBoundaryAdd H A0 A1 K =
        counterFactorizationHexagramOuterCyclicAdd H A0 A1 ↔
      K.total =
        counterFactorizationHexagramOuterCyclicAdd H A0 A1 := by
  rw [
    counterFactorizationHexagramCorrectedInnerBoundaryAdd_eq_crossingTotal
      H A0 A1 K
  ]

/-- Since the outer hexagram total equals the original M1 residual, recursive
preservation of that residual is equivalently the same crossing-total
equation. -/
theorem counterFactorizationHexagram_correctedInner_eq_M1Residual_iff_crossingTotal
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1)
    (K : HexagramCrossingCorrectionData) :
    counterFactorizationHexagramCorrectedInnerBoundaryAdd H A0 A1 K =
        counterFactorizationObjectCoboundaryAddAt H b10
            (counterFactorizationMiddleConnectorM1 H A0 A1) +
          counterFactorizationObjectCoboundaryAddAt H b11
            (counterFactorizationMiddleConnectorM1 H A0 A1) ↔
      K.total =
        counterFactorizationObjectCoboundaryAddAt H b10
            (counterFactorizationMiddleConnectorM1 H A0 A1) +
          counterFactorizationObjectCoboundaryAddAt H b11
            (counterFactorizationMiddleConnectorM1 H A0 A1) := by
  rw [
    counterFactorizationHexagramCorrectedInnerBoundaryAdd_eq_crossingTotal
      H A0 A1 K
  ]

/-- Equivalent formulation using the cyclic outer scalar carrier. -/
theorem counterFactorizationHexagram_crossingTotal_eq_outer_iff_M1Residual
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1)
    (K : HexagramCrossingCorrectionData) :
    K.total =
        counterFactorizationHexagramOuterCyclicAdd H A0 A1 ↔
      K.total =
        counterFactorizationObjectCoboundaryAddAt H b10
            (counterFactorizationMiddleConnectorM1 H A0 A1) +
          counterFactorizationObjectCoboundaryAddAt H b11
            (counterFactorizationMiddleConnectorM1 H A0 A1) := by
  rw [
    ← counterFactorizationMiddleConnectorM1_pair_coboundary_eq_hexagramOuterCyclicAdd
      H A0 A1
  ]

/-!
## Boundary after v3.93

The recursive-obstruction question is now concentrated in one exact datum.

The naive endpoint coboundary contributes zero.  Hence the inner hexagonal
obstruction after one refinement step is carried entirely by the six crossing
corrections.

Preserving the scalar-valued outer hexagram, and preserving the original M1
coboundary residual, are equivalent to the same equation:

sum of six crossing corrections = outer/M1 residual.

The next theorem unit should stop treating these corrections as abstract.
It should extract candidate crossing corrections from the existing
pseudofunctor coherence data: localized compositor naturality squares,
middle-switch transport, or an explicit interchanger comparison at each
crossing.  The target is now a concrete six-term equality rather than a
geometric analogy.
-/

end

end KUOS.DependentOriginationHexagramCrossingCorrectionV3_93
