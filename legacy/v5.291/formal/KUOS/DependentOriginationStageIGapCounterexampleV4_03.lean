import KUOS.DependentOriginationWeakLocalizationPrinciplesFalseV4_02
import KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
import KUOS.DependentOriginationWeakHigherLocalizationGapDecompositionV2_31
import Mathlib

namespace KUOS.DependentOriginationStageIGapCounterexampleV4_03

open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationHigherStrictificationPrincipleV2_15
open KUOS.DependentOriginationWeakHigherLocalizationUniversalPropertyV2_18
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationWeakHigherLocalizationGapDecompositionV2_31
open KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
open KUOS.DependentOriginationAbstractNonfactorizationV4_00
open KUOS.DependentOriginationAdmissibleNonfactorizationV4_01
open KUOS.DependentOriginationWeakLocalizationPrinciplesFalseV4_02

set_option autoImplicit false

noncomputable section

/-!
# The octahedral countermodel is a Stage-I gap counterexample v4.03

v4.02 refutes the unrestricted weak localization existence and universal
principles on the finite octahedral context.

The v2.31 gap decomposition distinguishes three possible failure stages:

1. Stage I: no higher-localization factorization exists;
2. Stage II: a factorization exists, but no universal candidate exists;
3. Stage III: a universal candidate exists, but essential uniqueness fails.

The concrete C2 countermodel is now known to fail already at Stage I.

This file records that exact location and propagates the same witness to the
coherent v2.19 universal principle and to the full v2.31 gap-completion
package.
-/

/-- The concrete admissible countermodel has the exact v2.31 Stage-I
factorization-existence obstruction. -/
theorem counterSystem_stageI_factorization_obstruction :
    HigherWeakLocalizationFactorizationExistenceObstruction
      (W := allMorphisms) counterSystem := by
  refine ⟨counterSystem_admissible, ?_⟩
  simpa [HasHigherLocalizationFactorization] using
    no_counterSystem_higherLocalizationFactorization

/-- Hence the complete v2.31 universal-property gap obstruction is present, and
specifically by its Stage-I branch. -/
theorem counterSystem_universal_gap_obstruction :
    HigherWeakLocalizationUniversalGapObstruction
      (W := allMorphisms) counterSystem := by
  exact Or.inl counterSystem_stageI_factorization_obstruction

/-- The concrete countermodel also admits no coherent v2.19 weak
higher-localization universal-property datum. -/
theorem counterSystem_no_coherentWeakHigherLocalizationUniversalProperty :
    ¬ HasCoherentWeakHigherLocalizationUniversalProperty
      (W := allMorphisms) counterSystem := by
  intro hU
  have hFactorization :
      HasHigherLocalizationFactorization
        (W := allMorphisms) counterSystem :=
    hasHigherLocalizationFactorization_of_hasCoherentWeakHigherLocalizationUniversalProperty
      allMorphisms hU
  have hNoFactorization :
      ¬ HasHigherLocalizationFactorization
        (W := allMorphisms) counterSystem := by
    simpa [HasHigherLocalizationFactorization] using
      no_counterSystem_higherLocalizationFactorization
  exact hNoFactorization hFactorization

/-- The coherent v2.19 global universal principle is false already on the
finite octahedral context. -/
theorem octahedral_coherentHigherWeakLocalizationUniversalPrinciple_false :
    ¬ CoherentHigherWeakLocalizationUniversalPrinciple.{0, 0, 0, 0}
      (W := allMorphisms) := by
  intro hCoherent
  have hExist :
      HigherWeakLocalizationExistence.{0, 0, 0, 0}
        (W := allMorphisms) :=
    higherWeakLocalizationExistence_of_coherentUniversalPrinciple
      allMorphisms hCoherent
  exact octahedral_higherWeakLocalizationExistence_false hExist

/-- The full v2.31 three-stage gap-completion package is false as well because
its first component is exactly the already-refuted Stage-I existence
principle. -/
theorem octahedral_higherWeakLocalizationUniversalGapCompletion_false :
    ¬ HigherWeakLocalizationUniversalGapCompletion.{0, 0, 0, 0}
      (W := allMorphisms) := by
  intro hGap
  exact octahedral_higherWeakLocalizationExistence_false hGap.1

/-!
## Boundary after v4.03

The finite counterexample is now located exactly in the old v2.31 obstruction
decomposition:

  Stage I fails.

There is no higher-localization factorization at all, so Stage II universality
and Stage III essential uniqueness are never reached.

Consequently the same concrete weakly admissible system refutes:

* v2.15 weak localization existence;
* v2.18 weak universal existence;
* v2.19 coherent weak universal existence;
* the v2.31 three-stage global gap-completion package.

Positive theorems from the earlier spine remain valid only under their stated
additional hypotheses; v4.03 identifies why such hypotheses are genuinely
needed.
-/

end

end KUOS.DependentOriginationStageIGapCounterexampleV4_03
