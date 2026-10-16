import KUOS.DependentOriginationGeneratedCoboundaryUnsolvableV4_08
import KUOS.DependentOriginationHigherLocalizationLiftingProblemV3_04
import Mathlib

namespace KUOS.DependentOriginationComparisonLiftUnsolvableV4_09

open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationQuotientGaugeIndependenceV3_03
open KUOS.DependentOriginationHigherLocalizationLiftingProblemV3_04
open KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
open KUOS.DependentOriginationGeneratedCoboundaryUnsolvableV4_08

set_option autoImplicit false

noncomputable section

/-!
# Every solved quotient stage has no comparison lift v4.09

v3.04 characterizes the full generated correction coboundary as:

  a quotient-gauge solution
    plus
  a comparison-gauge lift over that exact quotient solution.

v4.08 proves that the full generated correction coboundary is unsolvable for
every pointwise adjoint-equivalence datum D on the concrete countermodel.

Therefore no solved quotient gauge can admit a comparison-gauge lift.
This statement is conditional on a quotient solution being supplied; it does
not claim that the quotient stage itself is solvable.
-/

/-- No quotient solution together with a comparison lift exists. -/
theorem counterSystem_no_quotientSolution_with_comparisonLift
    (D : PointwiseWAdjointEquivalenceData
      (W := allMorphisms) counterSystem) :
    ¬ ∃ Q : GeneratedQuotientGaugeParameters
          allMorphisms counterSystem D,
        ∃ hQ : GeneratedQuotientGaugeCoboundary
            allMorphisms counterSystem D Q,
          GeneratedComparisonGaugeLiftSolvable
            allMorphisms counterSystem D Q hQ := by
  intro hStages
  apply counterSystem_generatedCorrectionCoboundary_unsolvable D
  exact
    (generatedCorrectionCoboundarySolvable_iff_quotient_and_comparisonLift
      allMorphisms counterSystem D).2 hStages

/-- Pointwise form: every actual quotient solution fails at the comparison
lifting stage. -/
theorem counterSystem_every_quotientSolution_has_no_comparisonLift
    (D : PointwiseWAdjointEquivalenceData
      (W := allMorphisms) counterSystem) :
    ∀
      (Q : GeneratedQuotientGaugeParameters
        allMorphisms counterSystem D)
      (hQ : GeneratedQuotientGaugeCoboundary
        allMorphisms counterSystem D Q),
      ¬ GeneratedComparisonGaugeLiftSolvable
        allMorphisms counterSystem D Q hQ := by
  intro Q hQ hLift
  apply counterSystem_no_quotientSolution_with_comparisonLift D
  exact ⟨Q, hQ, hLift⟩

/-- Canonical admissibility-generated specialization. -/
theorem counterSystem_canonical_every_quotientSolution_has_no_comparisonLift :
    ∀
      (Q : GeneratedQuotientGaugeParameters
        allMorphisms counterSystem
        (pointwiseWAdjointEquivalenceDataOfAdmissible
          allMorphisms counterSystem_admissible))
      (hQ : GeneratedQuotientGaugeCoboundary
        allMorphisms counterSystem
        (pointwiseWAdjointEquivalenceDataOfAdmissible
          allMorphisms counterSystem_admissible) Q),
      ¬ GeneratedComparisonGaugeLiftSolvable
        allMorphisms counterSystem
        (pointwiseWAdjointEquivalenceDataOfAdmissible
          allMorphisms counterSystem_admissible) Q hQ := by
  exact
    counterSystem_every_quotientSolution_has_no_comparisonLift
      (pointwiseWAdjointEquivalenceDataOfAdmissible
        allMorphisms counterSystem_admissible)

/-!
## Boundary after v4.09

The Stage-I obstruction is now localized to the exact v3.04 two-stage lifting
problem.

For every quotient gauge Q that solves the first three quotient-coboundary
faces, the two comparison residual equations admit no comparison-gauge lift.

This still leaves open whether the quotient stage itself has any global
solution.  What is proved is stronger than mere full-coboundary failure:
any such quotient solution is necessarily terminally nonliftable.

The next theorem unit can ask whether the existing fixed-gauge associator
obstruction of v3.65 already prevents quotient-stage solvability, or whether a
quotient solution exists but is blocked only at the comparison lift.
-/

end

end KUOS.DependentOriginationComparisonLiftUnsolvableV4_09
