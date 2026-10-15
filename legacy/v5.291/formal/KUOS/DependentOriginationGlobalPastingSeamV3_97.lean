import KUOS.DependentOriginationLocalNaturalityGeneratedCorrectionsV3_96
import Mathlib

namespace KUOS.DependentOriginationGlobalPastingSeamV3_97

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
open KUOS.DependentOriginationArbitraryFactorizationParityV3_74
open KUOS.DependentOriginationHexagramScalarCarrierV3_91
open KUOS.DependentOriginationHexagramInnerHexagonV3_88
open KUOS.DependentOriginationHexagramCrossingCorrectionV3_93
open KUOS.DependentOriginationLocalNaturalityGeneratedCorrectionsV3_96

set_option autoImplicit false

noncomputable section

/-!
# Global-pasting seam correction v3.97

v3.96 proves that corrections generated independently from six genuine local
naturality squares are pointwise zero.  Thus any nonzero recursive correction
must come from data comparing how those exact local squares are pasted
together globally.

This file isolates that remaining datum as a seam/descent correction at each
of the six hexagram crossings.

A global-pasting correction consists of

* six genuine local naturality squares, contributing zero local defect;
* six seam values measuring the mismatch of the chosen global identifications
  along their shared boundaries.

The induced crossing correction is local defect plus seam correction.  Since
the local part vanishes, the total crossing correction and the corrected inner
boundary are exactly the six-seam total.

Therefore preserving the outer/M1 residual is equivalent to one explicit
global descent equation: the sum of the six seam corrections must equal the
outer residual.

No claim is made yet that the seam values arise canonically from existing
associators/compositors.  That construction is the next authority obligation.
-/

/-- Global-pasting data: exact local squares together with one seam correction
at each inner hexagram crossing. -/
structure HexagramGlobalPastingCorrectionData
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem) where
  localNaturality : HexagramLocalNaturalityCorrectionData H
  seam : HexagramInnerVertex → ZMod 2

/-- Total seam correction around the six inner crossings. -/
noncomputable def HexagramGlobalPastingCorrectionData.seamTotal
    {H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem}
    (D : HexagramGlobalPastingCorrectionData H) : ZMod 2 :=
  D.seam .x0 +
    D.seam .x1 +
    D.seam .x2 +
    D.seam .x3 +
    D.seam .x4 +
    D.seam .x5

/-- Crossing correction induced by global-pasting data: local naturality defect
plus seam mismatch. -/
noncomputable def HexagramGlobalPastingCorrectionData.toCrossingCorrectionData
    {H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem}
    (D : HexagramGlobalPastingCorrectionData H) :
    HexagramCrossingCorrectionData where
  correction x :=
    D.localNaturality.toCrossingCorrectionData.correction x + D.seam x

/-- The total induced crossing correction splits into local and seam totals. -/
theorem HexagramGlobalPastingCorrectionData_total_eq_local_add_seam
    {H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem}
    (D : HexagramGlobalPastingCorrectionData H) :
    D.toCrossingCorrectionData.total =
      D.localNaturality.toCrossingCorrectionData.total + D.seamTotal := by
  simp only [
    HexagramCrossingCorrectionData.total,
    HexagramGlobalPastingCorrectionData.toCrossingCorrectionData,
    HexagramGlobalPastingCorrectionData.seamTotal
  ]
  ac_rfl

/-- Since all local naturality defects vanish, only the seam total survives. -/
theorem HexagramGlobalPastingCorrectionData_total_eq_seam
    {H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem}
    (D : HexagramGlobalPastingCorrectionData H) :
    D.toCrossingCorrectionData.total = D.seamTotal := by
  rw [
    HexagramGlobalPastingCorrectionData_total_eq_local_add_seam D,
    HexagramLocalNaturalityCorrectionData_total_eq_zero D.localNaturality,
    zero_add
  ]

/-- The corrected inner boundary produced by global-pasting data is exactly the
six-seam total. -/
theorem counterFactorizationHexagramGlobalPastingCorrectedInner_eq_seam
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1)
    (D : HexagramGlobalPastingCorrectionData H) :
    counterFactorizationHexagramCorrectedInnerBoundaryAdd H A0 A1
        D.toCrossingCorrectionData =
      D.seamTotal := by
  rw [
    counterFactorizationHexagramCorrectedInnerBoundaryAdd_eq_crossingTotal
      H A0 A1 D.toCrossingCorrectionData,
    HexagramGlobalPastingCorrectionData_total_eq_seam D
  ]

/-- Preservation of the outer scalar carrier is equivalent to the global seam
equation. -/
theorem counterFactorizationHexagram_globalPasting_preserves_outer_iff_seamTotal
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1)
    (D : HexagramGlobalPastingCorrectionData H) :
    counterFactorizationHexagramCorrectedInnerBoundaryAdd H A0 A1
        D.toCrossingCorrectionData =
        counterFactorizationHexagramOuterCyclicAdd H A0 A1 ↔
      D.seamTotal =
        counterFactorizationHexagramOuterCyclicAdd H A0 A1 := by
  rw [
    counterFactorizationHexagramGlobalPastingCorrectedInner_eq_seam
      H A0 A1 D
  ]

/-- A globally pasted correction with zero seam total cannot preserve a nonzero
outer residual. -/
theorem counterFactorizationHexagram_zeroSeam_ne_nonzero_outer
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1)
    (D : HexagramGlobalPastingCorrectionData H)
    (hSeam : D.seamTotal = 0)
    (hOuter :
      counterFactorizationHexagramOuterCyclicAdd H A0 A1 ≠ 0) :
    counterFactorizationHexagramCorrectedInnerBoundaryAdd H A0 A1
        D.toCrossingCorrectionData ≠
      counterFactorizationHexagramOuterCyclicAdd H A0 A1 := by
  intro hEq
  have hOuterZero :
      counterFactorizationHexagramOuterCyclicAdd H A0 A1 = 0 := by
    rw [
      ← hEq,
      counterFactorizationHexagramGlobalPastingCorrectedInner_eq_seam
        H A0 A1 D,
      hSeam
    ]
  exact hOuter hOuterZero

/-!
## Boundary after v3.97

The recursive correction problem now has a strict local/global decomposition.

Local naturality defects contribute exactly zero.  The entire nontrivial
corrected inner obstruction is carried by the six global seam/descent values.

Thus the next authority question is no longer vague:

construct the six seam corrections canonically from existing higher-coherence
pasting data, and determine whether their total equals the outer/M1 residual.

If the canonical seam total is zero, recursive preservation fails for every
nonzero outer residual.  If it equals the residual, the obstruction has been
transported through one recursive refinement step.  Any intermediate value is
an explicit descent mismatch.

The next theorem unit should derive a candidate seam from a concrete comparison
of the two triangle pastings rather than postulating six free seam scalars.
-/

end

end KUOS.DependentOriginationGlobalPastingSeamV3_97
