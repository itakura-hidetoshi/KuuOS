import KUOS.DependentOriginationLocalNaturalityDefectZeroV3_94
import Mathlib

namespace KUOS.DependentOriginationCrossingCorrectionExistenceV3_95

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
open KUOS.DependentOriginationArbitraryFactorizationParityV3_74
open KUOS.DependentOriginationHexagramScalarCarrierV3_91
open KUOS.DependentOriginationHexagramCrossingCorrectionV3_93

set_option autoImplicit false

noncomputable section

/-!
# Unconstrained crossing corrections always exist v3.95

v3.93 shows that recursive preservation of the outer/M1 residual is equivalent
to one equation: the total of six crossing corrections must equal that
residual.  v3.94 shows that the required correction cannot be the defect of an
individual localized compositor naturality square, because every such local
defect vanishes.

This file separates algebraic existence from coherent origin.

If the six crossing corrections are allowed to be arbitrary ZMod 2 values,
then a solution always exists: concentrate the entire outer residual at one
crossing and set the other five corrections to zero.

Therefore there is no bare additive solvability obstruction at the crossing
level.  The remaining mathematical content is the authority-bounded problem:
can such a correction be derived canonically from the existing higher
coherence data rather than inserted freely?
-/

/-- A deliberately unconstrained correction datum concentrating the full
outer residual at x0. -/
noncomputable def counterFactorizationConcentratedCrossingCorrection
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) :
    HexagramCrossingCorrectionData where
  correction
    | .x0 => counterFactorizationHexagramOuterCyclicAdd H A0 A1
    | .x1 => 0
    | .x2 => 0
    | .x3 => 0
    | .x4 => 0
    | .x5 => 0

/-- The concentrated correction has total equal to the outer hexagram
residual. -/
theorem counterFactorizationConcentratedCrossingCorrection_total
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) :
    (counterFactorizationConcentratedCrossingCorrection H A0 A1).total =
      counterFactorizationHexagramOuterCyclicAdd H A0 A1 := by
  simp [counterFactorizationConcentratedCrossingCorrection,
    HexagramCrossingCorrectionData.total]

/-- Hence the corrected inner boundary exactly reproduces the outer residual. -/
theorem counterFactorizationConcentratedCrossingCorrection_correctedInner_eq_outer
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) :
    counterFactorizationHexagramCorrectedInnerBoundaryAdd H A0 A1
        (counterFactorizationConcentratedCrossingCorrection H A0 A1) =
      counterFactorizationHexagramOuterCyclicAdd H A0 A1 := by
  apply
    (counterFactorizationHexagram_correctedInner_eq_outer_iff_crossingTotal
      H A0 A1
      (counterFactorizationConcentratedCrossingCorrection H A0 A1)).2
  exact counterFactorizationConcentratedCrossingCorrection_total H A0 A1

/-- The same unconstrained correction reproduces the original M1 coboundary
residual because that residual equals the outer cyclic hexagram scalar. -/
theorem counterFactorizationConcentratedCrossingCorrection_correctedInner_eq_M1Residual
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) :
    counterFactorizationHexagramCorrectedInnerBoundaryAdd H A0 A1
        (counterFactorizationConcentratedCrossingCorrection H A0 A1) =
      counterFactorizationObjectCoboundaryAddAt H b10
          (counterFactorizationMiddleConnectorM1 H A0 A1) +
        counterFactorizationObjectCoboundaryAddAt H b11
          (counterFactorizationMiddleConnectorM1 H A0 A1) := by
  rw [
    counterFactorizationConcentratedCrossingCorrection_correctedInner_eq_outer
      H A0 A1
  ]
  exact
    (counterFactorizationMiddleConnectorM1_pair_coboundary_eq_hexagramOuterCyclicAdd
      H A0 A1).symm

/-- Bare algebraic existence of a six-crossing filler is automatic. -/
theorem exists_crossingCorrection_preserving_outer
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) :
    ∃ K : HexagramCrossingCorrectionData,
      counterFactorizationHexagramCorrectedInnerBoundaryAdd H A0 A1 K =
        counterFactorizationHexagramOuterCyclicAdd H A0 A1 := by
  exact ⟨counterFactorizationConcentratedCrossingCorrection H A0 A1,
    counterFactorizationConcentratedCrossingCorrection_correctedInner_eq_outer
      H A0 A1⟩

/-- Bare algebraic existence also suffices to reproduce the M1 residual. -/
theorem exists_crossingCorrection_preserving_M1Residual
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) :
    ∃ K : HexagramCrossingCorrectionData,
      counterFactorizationHexagramCorrectedInnerBoundaryAdd H A0 A1 K =
        counterFactorizationObjectCoboundaryAddAt H b10
            (counterFactorizationMiddleConnectorM1 H A0 A1) +
          counterFactorizationObjectCoboundaryAddAt H b11
            (counterFactorizationMiddleConnectorM1 H A0 A1) := by
  exact ⟨counterFactorizationConcentratedCrossingCorrection H A0 A1,
    counterFactorizationConcentratedCrossingCorrection_correctedInner_eq_M1Residual
      H A0 A1⟩

/-!
## Boundary after v3.95

The crossing layer has no unconstrained additive existence obstruction.

A six-crossing correction reproducing the outer/M1 residual can always be
manufactured by concentrating the entire residual at one crossing.  Therefore
the research question has sharpened again:

* existence of arbitrary corrections is trivial;
* defects of individual local naturality squares are identically zero;
* the nontrivial requirement is a correction derived canonically from allowed
  higher-coherence transport and global pasting/descent.

The next theorem unit should encode an authority condition on crossing
corrections: a correction is admissible only if it is obtained from a specified
pasting comparison built from existing pseudofunctor compositors,
associators, and middle-switch transport.  The obstruction then becomes the
failure of such an admissible correction to realize the freely solvable total.
-/

end

end KUOS.DependentOriginationCrossingCorrectionExistenceV3_95
