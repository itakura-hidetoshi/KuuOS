import KUOS.DependentOriginationAdmissibleNonfactorizationV4_01
import KUOS.DependentOriginationWeakHigherLocalizationUniversalPropertyV2_18
import Mathlib

namespace KUOS.DependentOriginationWeakLocalizationPrinciplesFalseV4_02

open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationHigherStrictificationPrincipleV2_15
open KUOS.DependentOriginationWeakHigherLocalizationUniversalPropertyV2_18
open KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
open KUOS.DependentOriginationAbstractNonfactorizationV4_00
open KUOS.DependentOriginationAdmissibleNonfactorizationV4_01

set_option autoImplicit false

noncomputable section

/-!
# Weak higher-localization principles fail on the finite octahedral model v4.02

v4.01 proves that the concrete octahedral C2 countermodel is weakly
allMorphisms-admissible while admitting no arbitrary
HigherLocalizationFactorization.

The v2.15 weak localization existence principle and the v2.18 weak universal
principle were intentionally left as propositions rather than assumed axioms.
Both quantify over all weakly admissible raw higher systems and assert
factorization or universal-property existence.

The concrete countermodel now refutes both principles on the finite octahedral
context.

Since every WeakHigherLocalizationUniversalProperty contains a chosen
HigherLocalizationFactorization, v4.00 immediately also rules out a universal
property for counterSystem itself.
-/

/-- The concrete admissible countermodel admits no v2.18 weak higher
localization universal-property datum. -/
theorem counterSystem_no_weakHigherLocalizationUniversalProperty :
    ¬ HasWeakHigherLocalizationUniversalProperty
      (W := allMorphisms) counterSystem := by
  intro hU
  rcases hU with ⟨U⟩
  exact no_counterSystem_higherLocalizationFactorization ⟨U.chosen⟩

/-- The v2.15 existence principle is false already on the finite octahedral
context. -/
theorem octahedral_higherWeakLocalizationExistence_false :
    ¬ HigherWeakLocalizationExistence.{0, 0, 0, 0}
      (W := allMorphisms) := by
  intro hExist
  have hCounter :
      HasHigherLocalizationFactorization
        (W := allMorphisms) counterSystem :=
    hExist counterSystem counterSystem_admissible
  exact no_counterSystem_higherLocalizationFactorization hCounter

/-- The v2.18 weak higher-localization universal principle is likewise false
already on the same finite octahedral context. -/
theorem octahedral_higherWeakLocalizationUniversalPrinciple_false :
    ¬ HigherWeakLocalizationUniversalPrinciple.{0, 0, 0, 0}
      (W := allMorphisms) := by
  intro hUniversal
  have hCounter :
      HasWeakHigherLocalizationUniversalProperty
        (W := allMorphisms) counterSystem :=
    hUniversal counterSystem counterSystem_admissible
  exact counterSystem_no_weakHigherLocalizationUniversalProperty hCounter

/-- The two failures are witnessed by the same concrete admissible system. -/
theorem counterSystem_refutes_weak_localization_principles :
    IsHigherWAdmissible allMorphisms counterSystem ∧
      ¬ HasHigherLocalizationFactorization
        (W := allMorphisms) counterSystem ∧
      ¬ HasWeakHigherLocalizationUniversalProperty
        (W := allMorphisms) counterSystem := by
  refine ⟨counterSystem_admissible, ?_, ?_⟩
  · exact no_counterSystem_higherLocalizationFactorization
  · exact counterSystem_no_weakHigherLocalizationUniversalProperty

/-!
## Boundary after v4.02

The original logical boundary from v2.15-v2.18 is no longer merely open on the
finite truth-test context.

For the concrete octahedral C2 system:

  weak allMorphisms-admissibility
    does not imply
  higher-localization factorization,

and therefore also does not imply the stronger weak higher-localization
universal-property datum.

Consequently the unrestricted v2.15 existence principle and v2.18 universal
principle are both false on this finite context.

Any valid positive localization theorem must impose additional hypotheses
beyond weak arrowwise equivalence, such as one of the later coherence,
thinness, separating, or descent conditions already isolated in the formal
spine.
-/

end

end KUOS.DependentOriginationWeakLocalizationPrinciplesFalseV4_02
