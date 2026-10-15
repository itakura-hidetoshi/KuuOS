import KUOS.DependentOriginationStageIGapCounterexampleV4_03
import KUOS.DependentOriginationFiberFunctorTwoThinV2_62
import KUOS.DependentOriginationFiberHomThinV2_63
import KUOS.DependentOriginationFiberIsoThinV2_64
import KUOS.DependentOriginationGaugeObstructionV2_66
import Mathlib

namespace KUOS.DependentOriginationCountermodelSufficientConditionFailuresV4_04

open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationFiberFunctorTwoThinV2_62
open KUOS.DependentOriginationFiberHomThinV2_63
open KUOS.DependentOriginationFiberIsoThinV2_64
open KUOS.DependentOriginationGaugeObstructionV2_66
open KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
open KUOS.DependentOriginationAbstractNonfactorizationV4_00
open KUOS.DependentOriginationAdmissibleNonfactorizationV4_01

set_option autoImplicit false

noncomputable section

/-!
# Necessary failures of earlier sufficient conditions v4.04

The pre-v4.00 formal spine contains several genuine sufficient conditions for
higher localization factorization:

* fiber-functor 2-thinness;
* fiber-hom thinness;
* fiber-functor iso-thinness;
* fiber-core thinness;
* trivial fiber automorphisms;
* canonical five-defect gauge trivializability.

Each of these conditions, together with weak admissibility where required,
constructs an actual HigherLocalizationFactorization.

The concrete C2 countermodel is weakly admissible but has no such
factorization.  Therefore it must fail every one of these sufficient
conditions.

This does not turn the sufficient conditions into necessary conditions in
general.  It identifies, for this specific truth-test model, which previously
known positive sectors it lies outside.
-/

/-- Convenient proposition-level form of v4.00. -/
theorem counterSystem_no_hasHigherLocalizationFactorization :
    ¬ HasHigherLocalizationFactorization
      (W := allMorphisms) counterSystem := by
  simpa [HasHigherLocalizationFactorization] using
    no_counterSystem_higherLocalizationFactorization

/-- The countermodel is not in the fiber-functor 2-thin sufficient sector. -/
theorem counterSystem_not_fiberFunctorTwoThin :
    ¬ IsFiberFunctorTwoThin counterSystem := by
  intro hthin
  apply counterSystem_no_hasHigherLocalizationFactorization
  exact
    hasHigherLocalizationFactorization_of_admissible_and_fiberFunctorTwoThin
      allMorphisms counterSystem_admissible hthin

/-- The countermodel is not in the stronger fiber-hom thin sector. -/
theorem counterSystem_not_fiberHomThin :
    ¬ IsFiberHomThin counterSystem := by
  intro hthin
  apply counterSystem_no_hasHigherLocalizationFactorization
  exact
    hasHigherLocalizationFactorization_of_admissible_and_fiberHomThin
      allMorphisms counterSystem_admissible hthin

/-- The countermodel is not even iso-thin at the relevant functor 2-cell
level. -/
theorem counterSystem_not_fiberFunctorIsoThin :
    ¬ IsFiberFunctorIsoThin counterSystem := by
  intro hiso
  apply counterSystem_no_hasHigherLocalizationFactorization
  exact
    hasHigherLocalizationFactorization_of_admissible_and_fiberFunctorIsoThin
      allMorphisms counterSystem_admissible hiso

/-- The core groupoids of the countermodel fibers are not thin in the sense
sufficient for higher localization. -/
theorem counterSystem_not_fiberCoreThin :
    ¬ IsFiberCoreThin counterSystem := by
  intro hcore
  apply counterSystem_no_hasHigherLocalizationFactorization
  exact
    hasHigherLocalizationFactorization_of_admissible_and_fiberCoreThin
      allMorphisms counterSystem_admissible hcore

/-- In particular, the countermodel does not have trivial fiber
automorphisms. -/
theorem counterSystem_not_trivialFiberAutomorphisms :
    ¬ IsFiberAutomorphismTrivial counterSystem := by
  intro htriv
  apply counterSystem_no_hasHigherLocalizationFactorization
  exact
    hasHigherLocalizationFactorization_of_admissible_and_trivialFiberAutomorphisms
      allMorphisms counterSystem_admissible htriv

/-- The canonical pointwise gauge orbit of the countermodel does not meet the
zero-five-defect locus. -/
theorem counterSystem_not_canonicalGaugeTrivializable :
    ¬ CanonicalGeneralWGaugeTrivializable
      allMorphisms counterSystem
      (pointwiseWAdjointEquivalenceDataOfAdmissible
        allMorphisms counterSystem_admissible) := by
  intro hGauge
  apply counterSystem_no_hasHigherLocalizationFactorization
  exact
    hasHigherLocalizationFactorization_of_admissible_and_canonicalGaugeTrivializable
      allMorphisms counterSystem_admissible hGauge

/-!
## Boundary after v4.04

The abstract nonfactorization theorem now has a concrete structural reading.

The C2 octahedral countermodel lies outside every earlier thin/coherence sector
that was already known to force factorization.  In particular it has
nontrivial invertible 2-dimensional isotropy and a nontrivial canonical gauge
obstruction.

Thus the obstruction exposed by v4.00-v4.04 is not caused by arbitrary
noninvertible 2-cells.  It survives precisely in the invertible coherence
sector that the v2.64-v2.66 hierarchy had isolated as the remaining source of
ambiguity.
-/

end

end KUOS.DependentOriginationCountermodelSufficientConditionFailuresV4_04
