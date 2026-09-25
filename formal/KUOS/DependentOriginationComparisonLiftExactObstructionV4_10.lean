import KUOS.DependentOriginationComparisonLiftUnsolvableV4_09
import KUOS.DependentOriginationQuotientTransportObstructionV3_05
import KUOS.DependentOriginationCounterCoherentQuotientTransportV3_67
import Mathlib

namespace KUOS.DependentOriginationComparisonLiftExactObstructionV4_10

open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationGeneratedCoboundaryUnsolvableV4_08
open KUOS.DependentOriginationCorrectionCoboundarySolvabilityV3_01
open KUOS.DependentOriginationCoherentQuotientTransportV2_59
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationQuotientGaugeIndependenceV3_03
open KUOS.DependentOriginationQuotientTransportObstructionV3_05
open KUOS.DependentOriginationHigherLocalizationLiftingProblemV3_04
open KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
open KUOS.DependentOriginationCounterCoherentQuotientTransportV3_67
open KUOS.DependentOriginationComparisonLiftUnsolvableV4_09

set_option autoImplicit false

noncomputable section

/-!
# Exact Stage-I obstruction: quotient transport exists, comparison lift fails v4.10

v3.67 already constructs an explicit coherent quotient transport
counterD_coherentQuotientTransportData for the canonical pointwise datum
counterD.

v3.05 converts any coherent quotient transport into a solved minimal quotient
gauge.

v4.09 proves that every such quotient solution admits no comparison-gauge lift.

Therefore the concrete countermodel does not fail at the quotient-pseudofunctor
stage.  Its Stage-I obstruction is exactly the second-stage comparison lift.
-/

/-- Canonical solved quotient gauge extracted from the explicit coherent
quotient transport of v3.67. -/
noncomputable def counterCanonicalSolvedQuotientGauge :
    GeneratedQuotientGaugeParameters
      allMorphisms counterSystem counterD :=
  generatedQuotientGaugeParametersOfCoherentTransport
    allMorphisms counterSystem counterD
    counterD_coherentQuotientTransportData

/-- The canonical quotient gauge really solves the three quotient coboundary
families. -/
noncomputable def counterCanonicalSolvedQuotientGauge_coboundary :
    GeneratedQuotientGaugeCoboundary
      allMorphisms counterSystem counterD
      counterCanonicalSolvedQuotientGauge :=
  generatedQuotientGaugeCoboundaryOfCoherentTransport
    allMorphisms counterSystem counterD
    counterD_coherentQuotientTransportData

/-- The quotient-stage coboundary is solvable for the canonical countermodel
datum. -/
theorem counterD_generatedQuotientGaugeCoboundarySolvable :
    GeneratedQuotientGaugeCoboundarySolvable
      allMorphisms counterSystem counterD := by
  exact
    ⟨counterCanonicalSolvedQuotientGauge,
      counterCanonicalSolvedQuotientGauge_coboundary⟩

/-- But the explicit solved quotient gauge admits no comparison-gauge lift. -/
theorem counterCanonicalSolvedQuotientGauge_no_comparisonLift :
    ¬ GeneratedComparisonGaugeLiftSolvable
      allMorphisms counterSystem counterD
      counterCanonicalSolvedQuotientGauge
      counterCanonicalSolvedQuotientGauge_coboundary := by
  exact
    counterSystem_every_quotientSolution_has_no_comparisonLift
      counterD
      counterCanonicalSolvedQuotientGauge
      counterCanonicalSolvedQuotientGauge_coboundary

/-- Exact witness of the two-stage obstruction: a quotient solution exists and
that same solution is terminally nonliftable. -/
theorem counterSystem_exists_quotientSolution_without_comparisonLift :
    ∃
      (Q : GeneratedQuotientGaugeParameters
        allMorphisms counterSystem counterD)
      (hQ : GeneratedQuotientGaugeCoboundary
        allMorphisms counterSystem counterD Q),
      ¬ GeneratedComparisonGaugeLiftSolvable
        allMorphisms counterSystem counterD Q hQ := by
  exact
    ⟨counterCanonicalSolvedQuotientGauge,
      counterCanonicalSolvedQuotientGauge_coboundary,
      counterCanonicalSolvedQuotientGauge_no_comparisonLift⟩

/-- The Stage-I failure is therefore strictly after quotient transport
existence for the canonical datum. -/
theorem counterSystem_quotientTransport_exists_but_full_coboundary_fails :
    HasCoherentQuotientTransportData
        allMorphisms counterSystem counterD ∧
      ¬ GeneratedCorrectionCoboundarySolvable
        allMorphisms counterSystem counterD := by
  exact
    ⟨counterD_hasCoherentQuotientTransportData,
      counterSystem_generatedCorrectionCoboundary_unsolvable counterD⟩

/-!
## Boundary after v4.10

The location of the finite obstruction is now exact.

The canonical countermodel has:

* a coherent quotient transport;
* an explicit quotient gauge solving all three quotient coherence families;
* no comparison-gauge lift over that solved quotient stage;
* hence no full five-face generated correction coboundary;
* hence no HigherLocalizationFactorization.

So the obstruction is not failure to construct the localized pseudofunctor
carrier.  It is failure to lift that coherent quotient carrier through the
comparison data back to the raw pseudofunctor.

This is the pre-factorization obstruction that should be transported onto any
future recursive geometric carrier.
-/

end

end KUOS.DependentOriginationComparisonLiftExactObstructionV4_10
