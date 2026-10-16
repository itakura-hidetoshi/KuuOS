import KUOS.DependentOriginationArbitraryTransportComparisonV3_69

namespace KUOS.DependentOriginationCanonicalFiveLawCounterexampleV3_70

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationCoherentComparisonFactorizationV2_60
open KUOS.DependentOriginationCorrectionCoboundarySolvabilityV3_01
open KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
open KUOS.DependentOriginationArbitraryTransportComparisonV3_69

set_option autoImplicit false

noncomputable section

/-!
# Canonical five-law counterexample v3.70

v3.69 proves that, for the concrete octahedral C2 system and its canonical
pointwise adjoint-equivalence datum `counterD`, every coherent quotient
transport fails the Stage-II coherent presentation comparison.  Equivalently,
the canonical five-law package `HasCoherentGeneralWFactorizationData` is empty.

This file returns that result to the weak-admissibility boundary without
strengthening it to the full abstract `HasHigherLocalizationFactorization`
interface.

The exact conclusion is:

* `counterSystem` is weakly `allMorphisms`-admissible;
* its canonical pointwise datum is exactly `counterD`;
* nevertheless no canonical five-law coherent general-W factorization package
  exists;
* equivalently, the generated five-face correction coboundary is unsolvable.

Thus weak admissibility alone does not imply existence of the canonical
five-law package produced by the v2.56--v3.04 construction route.

No claim is made here that an arbitrary `HigherLocalizationFactorization`
cannot exist.  Such a statement still requires a separate necessity/normal-form
bridge theorem.
-/

/-- The concrete countermodel is weakly admissible but its canonical pointwise
adjoint-equivalence datum admits no five-law coherent factorization package. -/
theorem counterSystem_admissible_but_no_canonical_five_law_package :
    IsHigherWAdmissible allMorphisms counterSystem ∧
      ¬ HasCoherentGeneralWFactorizationData
          allMorphisms counterSystem
          (pointwiseWAdjointEquivalenceDataOfAdmissible
            allMorphisms counterSystem_admissible) := by
  refine ⟨counterSystem_admissible, ?_⟩
  simpa [counterD] using counterD_not_hasCoherentGeneralWFactorizationData

/-- The same obstruction in the exact generated-correction normal form:
there is no simultaneous solution of the five generated coboundary equations
for the canonical pointwise datum of the concrete weakly admissible system. -/
theorem counterSystem_no_generatedCorrectionCoboundarySolvable :
    ¬ GeneratedCorrectionCoboundarySolvable
        allMorphisms counterSystem counterD := by
  intro h
  have hFive :
      HasCoherentGeneralWFactorizationData
        allMorphisms counterSystem counterD :=
    (generatedCorrectionCoboundarySolvable_iff_hasCoherentGeneralWFactorizationData
      allMorphisms counterSystem counterD).1 h
  exact counterD_not_hasCoherentGeneralWFactorizationData hFive

/-- Exact implication refuted by the concrete truth test: weak admissibility
does not force solvability of the canonical generated five-face correction
problem.  The quantified statement is kept at the concrete octahedral context,
so no universe-general claim is hidden in this counterexample. -/
theorem not_all_admissible_octahedral_systems_have_canonical_coboundary_solution :
    ¬ (∀
      (R : RawHigherContextualSystem.{0, 0, 0, 0}
        (Context := OctahedralVertex))
      (hR : IsHigherWAdmissible allMorphisms R),
        GeneratedCorrectionCoboundarySolvable
          allMorphisms R
          (pointwiseWAdjointEquivalenceDataOfAdmissible allMorphisms hR)) := by
  intro h
  have hCounter :=
    h counterSystem counterSystem_admissible
  exact counterSystem_no_generatedCorrectionCoboundarySolvable hCounter

/-!
## Boundary after v3.70

Canonically established for the concrete octahedral C2 truth test:

```text
weak allMorphisms-admissibility
  does not imply
canonical generated five-face coboundary solvability
```

and equivalently:

```text
weak allMorphisms-admissibility
  does not imply
HasCoherentGeneralWFactorizationData
for the canonical pointwise adjoint-equivalence datum.
```

This is a counterexample to the canonical v2.56--v3.04 construction route,
not yet to the larger abstract `HasHigherLocalizationFactorization` interface.

The next frontier is therefore a necessity/normal-form truth test:

```text
Does every HigherLocalizationFactorization of the concrete C2 system
normalize to the canonical five-law package?
```

Only a proved bridge of that form would allow the v3.70 counterexample to be
promoted to genuine nonexistence of arbitrary higher-localization
factorization.
-/

end

end KUOS.DependentOriginationCanonicalFiveLawCounterexampleV3_70
