import KUOS.DependentOriginationAbstractNonfactorizationV4_00
import Mathlib

namespace KUOS.DependentOriginationAdmissibleNonfactorizationV4_01

open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
open KUOS.DependentOriginationAbstractNonfactorizationV4_00

set_option autoImplicit false

noncomputable section

/-!
# Weak admissibility does not imply abstract higher factorization v4.01

v3.70 established only that the concrete octahedral C2 countermodel defeats
the canonical generated five-law factorization route.

v4.00 closes the stronger statement: the same countermodel admits no arbitrary
HigherLocalizationFactorization at all.

Since counterSystem is already proved weakly admissible for allMorphisms, it
now supplies a direct counterexample to the unrestricted implication

  IsHigherWAdmissible W R
    -> Nonempty (HigherLocalizationFactorization (W := W) R).

The quantified theorem below stays at the concrete octahedral context and the
pinned universes used throughout the finite truth test.  No universe-general
claim is hidden in the result.
-/

/-- The concrete countermodel is weakly admissible but has no abstract
higher-localization factorization. -/
theorem counterSystem_admissible_but_no_higherLocalizationFactorization :
    IsHigherWAdmissible allMorphisms counterSystem ∧
      ¬ Nonempty
        (HigherLocalizationFactorization
          (W := allMorphisms) counterSystem) := by
  exact ⟨counterSystem_admissible,
    no_counterSystem_higherLocalizationFactorization⟩

/-- Weak admissibility does not imply existence of an arbitrary
higher-localization factorization, already on the finite octahedral context. -/
theorem not_all_admissible_octahedral_systems_have_higherLocalizationFactorization :
    ¬ (∀
      (R : RawHigherContextualSystem.{0, 0, 0, 0}
        (Context := OctahedralVertex))
      (_hR : IsHigherWAdmissible allMorphisms R),
        Nonempty
          (HigherLocalizationFactorization
            (W := allMorphisms) R)) := by
  intro h
  have hCounter :=
    h counterSystem counterSystem_admissible
  exact no_counterSystem_higherLocalizationFactorization hCounter

/-!
## Boundary after v4.01

The necessity question left open after v3.70 is now settled for the concrete
finite truth test.

The obstruction is not merely a failure of one canonical normalization or one
chosen five-law package.  Weak allMorphisms-admissibility itself does not force
the existence of any HigherLocalizationFactorization.

The truncated-icosahedral refinement program can therefore be interpreted as
an analysis of how this established higher-coherence obstruction behaves under
self-similar carrier refinement, rather than as a search for an obstruction
that has not yet been proved.
-/

end

end KUOS.DependentOriginationAdmissibleNonfactorizationV4_01
