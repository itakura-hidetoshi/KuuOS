import KUOS.DependentOriginationExplicitInvertibleIsotropyV4_05
import KUOS.DependentOriginationGaugeObstructionV2_66
import Mathlib

namespace KUOS.DependentOriginationGaugeIndependentObstructionV4_06

open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationCoherentComparisonFactorizationV2_60
open KUOS.DependentOriginationPointwiseGeneralWChoiceV2_61
open KUOS.DependentOriginationCoherenceDefectsV2_65
open KUOS.DependentOriginationGaugeObstructionV2_66
open KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
open KUOS.DependentOriginationAbstractNonfactorizationV4_00
open KUOS.DependentOriginationCountermodelSufficientConditionFailuresV4_04

set_option autoImplicit false

noncomputable section

/-!
# Gauge-independent five-defect obstruction v4.06

v3.65 exhibited one fixed quotient gauge that corrects every unitor but fails
an associator.  By itself that was only a local fixed-gauge witness: another
gauge might still have corrected all coherence laws.

v4.00 changes the logical situation completely.  The concrete octahedral C2
countermodel admits no HigherLocalizationFactorization at all.

The v2.66 gauge theorem says, for any pointwise adjoint-equivalence datum D and
any pointwise base choice L0,

  coherent five-law data
    iff
  L0 is five-defect gauge-trivializable.

Since coherent five-law data would construct a genuine higher localization
factorization, v4.00 forces the whole gauge orbit to miss the zero-five-defect
locus.

Thus the obstruction is no longer tied to one bad fixed gauge.
-/

/-- No coherent general-W factorization package exists for any pointwise
adjoint-equivalence datum on the concrete countermodel. -/
theorem counterSystem_no_coherentGeneralWFactorizationData
    (D : PointwiseWAdjointEquivalenceData
      (W := allMorphisms) counterSystem) :
    ¬ HasCoherentGeneralWFactorizationData
      allMorphisms counterSystem D := by
  intro hCoherent
  apply counterSystem_no_hasHigherLocalizationFactorization
  exact
    hasHigherLocalizationFactorization_of_hasCoherentGeneralWFactorizationData
      allMorphisms counterSystem D hCoherent

/-- For arbitrary D and arbitrary pointwise base choice L0, the complete
five-defect gauge orbit never reaches a zero-defect representative. -/
theorem counterSystem_no_fiveDefectGaugeTrivializable
    (D : PointwiseWAdjointEquivalenceData
      (W := allMorphisms) counterSystem)
    (L0 : PointwiseGeneralWChoiceData
      (W := allMorphisms) counterSystem D) :
    ¬ FiveDefectGaugeTrivializable
      allMorphisms counterSystem D L0 := by
  intro hGauge
  apply counterSystem_no_coherentGeneralWFactorizationData D
  exact
    (hasCoherentGeneralWFactorizationData_iff_gaugeTrivializable
      allMorphisms counterSystem D L0).2 hGauge

/-- Equivalently, no pointwise choice at all can have all five coherence
defects trivial for the concrete countermodel. -/
theorem counterSystem_no_exists_fiveTrivialDefects
    (D : PointwiseWAdjointEquivalenceData
      (W := allMorphisms) counterSystem) :
    ¬ ∃ L : PointwiseGeneralWChoiceData
          (W := allMorphisms) counterSystem D,
        FiveCoherenceDefectsTrivial
          allMorphisms counterSystem D L := by
  intro hFive
  apply counterSystem_no_coherentGeneralWFactorizationData D
  exact
    (hasCoherentGeneralWFactorizationData_iff_exists_fiveTrivialDefects
      allMorphisms counterSystem D).2 hFive

/-- The gauge-independent statement can be packaged uniformly over every
possible base point of the pointwise-choice gauge orbit. -/
theorem counterSystem_every_pointwise_choice_has_nontrivial_five_defect_orbit
    (D : PointwiseWAdjointEquivalenceData
      (W := allMorphisms) counterSystem) :
    ∀ L0 : PointwiseGeneralWChoiceData
        (W := allMorphisms) counterSystem D,
      ¬ FiveDefectGaugeTrivializable
        allMorphisms counterSystem D L0 := by
  intro L0
  exact counterSystem_no_fiveDefectGaugeTrivializable D L0

/-- Canonical v2.61 specialization, recovering and strengthening the v4.04
canonical-gauge failure from the arbitrary-base-point theorem. -/
theorem counterSystem_canonical_choice_not_fiveDefectGaugeTrivializable :
    ¬ FiveDefectGaugeTrivializable
      allMorphisms counterSystem
      (pointwiseWAdjointEquivalenceDataOfAdmissible
        allMorphisms counterSystem_admissible)
      (pointwiseGeneralWChoiceData
        allMorphisms counterSystem
        (pointwiseWAdjointEquivalenceDataOfAdmissible
          allMorphisms counterSystem_admissible)) := by
  exact
    counterSystem_no_fiveDefectGaugeTrivializable
      (pointwiseWAdjointEquivalenceDataOfAdmissible
        allMorphisms counterSystem_admissible)
      (pointwiseGeneralWChoiceData
        allMorphisms counterSystem
        (pointwiseWAdjointEquivalenceDataOfAdmissible
          allMorphisms counterSystem_admissible))

/-!
## Boundary after v4.06

The local fixed-gauge obstruction from v3.65 has now been upgraded to a
gauge-independent statement.

For every admissibility-generated or otherwise supplied pointwise equivalence
datum D, and for every pointwise base choice L0, the entire gauge orbit misses
the zero-five-defect locus.

Therefore no alternative gauge can repair the concrete model into a coherent
five-law factorization.  The obstruction class is genuinely global and
gauge-invariant at the level detected by the v2.65-v2.66 five-defect package.

The truncated-icosahedral seam program should now transport this
gauge-independent obstruction class, rather than merely copy one bad
fixed-gauge representative.
-/

end

end KUOS.DependentOriginationGaugeIndependentObstructionV4_06
