import KUOS.DependentOriginationCrossingCorrectionExistenceV3_95
import Mathlib

namespace KUOS.DependentOriginationLocalNaturalityGeneratedCorrectionsV3_96

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
open KUOS.DependentOriginationArbitraryFactorizationParityV3_74
open KUOS.DependentOriginationArbitraryFactorizationLocalizedCocycleV3_75
open KUOS.DependentOriginationHexagramScalarCarrierV3_91
open KUOS.DependentOriginationHexagramInnerHexagonV3_88
open KUOS.DependentOriginationHexagramCrossingCorrectionV3_93
open KUOS.DependentOriginationLocalNaturalityDefectZeroV3_94

set_option autoImplicit false

noncomputable section

/-!
# Local-naturality-generated crossing corrections v3.96

v3.95 separates arbitrary crossing-correction solvability from coherent origin:
if six correction scalars are unconstrained, preserving the outer/M1 residual
is trivial.

This file imposes the first genuine authority restriction.  A crossing
correction is called locally naturality generated when each of its six values
is the additive defect of an actual localized compositor naturality square.

The data of one such square includes its endpoint, two localization objects,
the composable localization arrows, two source-fiber objects, and a connecting
source morphism.  v3.94 proves the defect of every such square is exactly zero.

Therefore every locally naturality-generated crossing correction is pointwise
zero, its six-crossing total is zero, and its corrected inner boundary is zero.
Consequently no nonzero outer hexagram residual can be preserved by this class
of authority-bounded corrections.

This rules out the most local coherent source of recursive obstruction.  The
next admissible source must depend on global pasting/descent of several
individually commuting squares rather than on any one square in isolation.
-/

/-- Full data of one genuine localized compositor naturality square. -/
structure LocalizedNaturalitySquareDatum
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem) where
  T : OctahedralVertex
  X : allMorphisms.Localization
  Y : allMorphisms.Localization
  f : X ⟶ Y
  g : Y ⟶ allMorphisms.Q.obj T
  A : CounterFactorizationLocalizedFiber H X
  B : CounterFactorizationLocalizedFiber H X
  u : A ⟶ B

/-- Additive defect carried by one stored naturality square. -/
noncomputable def LocalizedNaturalitySquareDatum.defectAdd
    {H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem}
    (S : LocalizedNaturalitySquareDatum H) : ZMod 2 :=
  counterFactorizationLocalizedCompNaturalityDefectAdd
    H S.T S.f S.g S.u

/-- Every stored local naturality square has zero defect. -/
@[simp] theorem LocalizedNaturalitySquareDatum_defectAdd_eq_zero
    {H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem}
    (S : LocalizedNaturalitySquareDatum H) :
    S.defectAdd = 0 := by
  exact counterFactorizationLocalizedCompNaturalityDefectAdd_eq_zero
    H S.T S.f S.g S.u

/-- Six genuine local naturality squares, one assigned to each inner
hexagram crossing. -/
structure HexagramLocalNaturalityCorrectionData
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem) where
  square : HexagramInnerVertex → LocalizedNaturalitySquareDatum H

/-- Crossing-correction datum induced by the six stored local naturality
squares. -/
noncomputable def HexagramLocalNaturalityCorrectionData.toCrossingCorrectionData
    {H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem}
    (D : HexagramLocalNaturalityCorrectionData H) :
    HexagramCrossingCorrectionData where
  correction x := (D.square x).defectAdd

/-- Every correction generated from an individual local naturality square is
zero. -/
@[simp] theorem HexagramLocalNaturalityCorrectionData_correction_eq_zero
    {H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem}
    (D : HexagramLocalNaturalityCorrectionData H)
    (x : HexagramInnerVertex) :
    D.toCrossingCorrectionData.correction x = 0 := by
  change (D.square x).defectAdd = 0
  exact LocalizedNaturalitySquareDatum_defectAdd_eq_zero (D.square x)

/-- Hence the total of all six locally generated crossing corrections is
zero. -/
theorem HexagramLocalNaturalityCorrectionData_total_eq_zero
    {H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem}
    (D : HexagramLocalNaturalityCorrectionData H) :
    D.toCrossingCorrectionData.total = 0 := by
  unfold HexagramCrossingCorrectionData.total
  rw [
    HexagramLocalNaturalityCorrectionData_correction_eq_zero D .x0,
    HexagramLocalNaturalityCorrectionData_correction_eq_zero D .x1,
    HexagramLocalNaturalityCorrectionData_correction_eq_zero D .x2,
    HexagramLocalNaturalityCorrectionData_correction_eq_zero D .x3,
    HexagramLocalNaturalityCorrectionData_correction_eq_zero D .x4,
    HexagramLocalNaturalityCorrectionData_correction_eq_zero D .x5
  ]
  simp

/-- The corrected inner boundary produced by six local naturality-square
defects is therefore zero. -/
theorem counterFactorizationHexagramLocalNaturalityCorrectedInner_eq_zero
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1)
    (D : HexagramLocalNaturalityCorrectionData H) :
    counterFactorizationHexagramCorrectedInnerBoundaryAdd H A0 A1
        D.toCrossingCorrectionData = 0 := by
  rw [
    counterFactorizationHexagramCorrectedInnerBoundaryAdd_eq_crossingTotal
      H A0 A1 D.toCrossingCorrectionData,
    HexagramLocalNaturalityCorrectionData_total_eq_zero D
  ]

/-- A nonzero outer hexagram residual cannot be reproduced by corrections
generated independently from local naturality squares. -/
theorem counterFactorizationHexagramLocalNaturalityCorrectedInner_ne_outer
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1)
    (D : HexagramLocalNaturalityCorrectionData H)
    (hOuter :
      counterFactorizationHexagramOuterCyclicAdd H A0 A1 ≠ 0) :
    counterFactorizationHexagramCorrectedInnerBoundaryAdd H A0 A1
        D.toCrossingCorrectionData ≠
      counterFactorizationHexagramOuterCyclicAdd H A0 A1 := by
  intro hEq
  have hZero :
      counterFactorizationHexagramOuterCyclicAdd H A0 A1 = 0 := by
    rw [
      ← hEq,
      counterFactorizationHexagramLocalNaturalityCorrectedInner_eq_zero
        H A0 A1 D
    ]
  exact hOuter hZero

/-- In existential form: when the outer residual is nonzero, no assignment of
six genuine local naturality squares can provide a preserving correction. -/
theorem no_localNaturalityGeneratedCorrection_preserves_nonzero_outer
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1)
    (hOuter :
      counterFactorizationHexagramOuterCyclicAdd H A0 A1 ≠ 0) :
    ¬ ∃ D : HexagramLocalNaturalityCorrectionData H,
      counterFactorizationHexagramCorrectedInnerBoundaryAdd H A0 A1
          D.toCrossingCorrectionData =
        counterFactorizationHexagramOuterCyclicAdd H A0 A1 := by
  intro h
  rcases h with ⟨D, hD⟩
  exact
    (counterFactorizationHexagramLocalNaturalityCorrectedInner_ne_outer
      H A0 A1 D hOuter) hD

/-!
## Boundary after v3.96

The first authority-bounded correction class has been completely evaluated.

Corrections generated independently from genuine localized compositor
naturality squares are all zero, because each local square already commutes
exactly.  Their six-crossing total and corrected inner boundary are therefore
zero.

So the freely solvable correction from v3.95 cannot be realized by choosing
six independent local naturality defects whenever the outer residual is
nonzero.

The next theorem unit must encode global pasting data: several exact local
squares together with identifications of their shared boundaries, followed by
a comparison of the two composite pastings around the interlaced triangles.
Only that global comparison can produce a descent mismatch not already forced
to zero locally.
-/

end

end KUOS.DependentOriginationLocalNaturalityGeneratedCorrectionsV3_96
