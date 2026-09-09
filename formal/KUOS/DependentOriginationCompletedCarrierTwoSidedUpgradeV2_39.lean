import KUOS.DependentOriginationUnitIsoAdjunctionCarrierTransferV2_38
import KUOS.DependentOriginationCoherentFactorForgetfulBridgeV2_20

namespace KUOS.DependentOriginationCompletedCarrierTwoSidedUpgradeV2_39

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationWeakHigherLocalizationUniversalPropertyV2_18
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationCoherentFactorForgetfulBridgeV2_20
open KUOS.DependentOriginationWeakHigherLocalizationGapDecompositionV2_31
open KUOS.DependentOriginationRouteCompletenessInternalGapV2_34
open KUOS.DependentOriginationFixedChosenEssentialUniquenessReflectionV2_36
open KUOS.DependentOriginationFixedChosenSplitCarrierTransferV2_37
open KUOS.DependentOriginationUnitIsoAdjunctionCarrierTransferV2_38

open scoped CategoryTheory.Pseudofunctor.StrongTrans

universe u v uH vH

/-!
# Completed-carrier two-sided upgrade v2.39

The v2.38 layer introduced two-sided factor equivalence data as a stronger
sufficient route than the one-sided split comparison of v2.37.  For an arbitrary
Stage II carrier that distinction is real.  For a **completed** Stage II carrier,
however, one side of the two-sided equivalence is already forced by Stage III
essential uniqueness.

Indeed, let `U` be the fixed coherent universal datum and let `C` be any Stage II
weak universal candidate.  Factor existence supplies genuine v2.18 factor maps

```text
U.chosen --p--> C.chosen --q--> U.chosen.
```

The forward map `p` comes from `C.factor`; the backward map `q` is obtained by
forgetting one coherent factor supplied by `U.factor`.  If `C` also satisfies
Stage III essential uniqueness, then the two factor morphisms

```text
C.chosen --q ≫ p--> C.chosen,
C.chosen ----id----> C.chosen
```

have isomorphic underlying StrongTrans 1-cells.  Therefore

```text
q.hom ≫ p.hom ≅ 𝟙 C.chosen.lift
```

is automatic on every completed carrier.

Consequently, on a completed carrier the only missing side of the v2.38
two-sided data is exactly the fixed-side split equation from v2.37:

```text
p.hom ≫ q.hom ≅ 𝟙 U.chosen.lift.
```

This file proves that the v2.37 split comparison and the v2.38 two-sided factor
equivalence data are equivalent **after Stage III completion of `C`**.  Hence a
split completed carrier automatically upgrades, via Mathlib's v2.38
`mkOfAdjointifyCounit` route, to an actual bicategorical adjoint equivalence of
the localized lifts.

No such upgrade is claimed for an uncompleted Stage II carrier.  No mutual factor
existence is promoted to an equivalence without the Stage III uniqueness theorem,
and no strictification, ordinary localization substitution, new axiom, `sorry`,
or `admit` is introduced.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- A bare pair of genuine v2.18 factor morphisms between the fixed coherent
carrier and another Stage II candidate.  No split, adjunction, or equivalence
data are stored. -/
structure HigherFixedChosenMutualFactorComparison
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (C : WeakHigherLocalizationUniversalCandidate (W := W) R) where
  forward : HigherLocalizationFactorMorphism (W := W) U.chosen C.chosen
  backward : HigherLocalizationFactorMorphism (W := W) C.chosen U.chosen

/-- Mutual weak factor existence is automatic between the fixed coherent carrier
and every Stage II candidate.

The forward factor comes from the candidate's Stage II universal factor property.
The backward factor comes from the coherent universal property of `U`, followed
by the v2.20 forgetful bridge.  This theorem intentionally produces only mutual
factor maps, not an adjunction or an equivalence. -/
theorem hasMutualFactorComparison
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (C : WeakHigherLocalizationUniversalCandidate (W := W) R) :
    Nonempty (HigherFixedChosenMutualFactorComparison (W := W) U C) := by
  rcases C.factor U.chosen with ⟨forward⟩
  rcases coherentWeakUniversalProperty_hasV2_18Factor
      (W := W) U C.chosen with ⟨backward⟩
  exact ⟨⟨forward, backward⟩⟩

/-- A v2.37 split comparison has, in particular, the underlying mutual factor
comparison. -/
def mutualFactorComparisonOfSplit
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R}
    {C : WeakHigherLocalizationUniversalCandidate (W := W) R}
    (S : HigherFixedChosenSplitCarrierComparison (W := W) U C) :
    HigherFixedChosenMutualFactorComparison (W := W) U C where
  forward := S.forward
  backward := S.backward

/-- Stage III essential uniqueness on `C` automatically closes the
**completed-carrier side** of any mutual factor comparison:

```text
backward.hom ≫ forward.hom ≅ 𝟙 C.chosen.lift.
```

This is the key asymmetry of v2.39.  It uses only `C.HasEssentialUniqueness`,
applied to the composite factor morphism `C -> U -> C` and the identity factor
morphism on `C`. -/
theorem completedCarrierCounitIso
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (C : WeakHigherLocalizationUniversalCandidate (W := W) R)
    (hUnique : C.HasEssentialUniqueness (W := W))
    (M : HigherFixedChosenMutualFactorComparison (W := W) U C) :
    Nonempty (M.backward.hom ≫ M.forward.hom ≅ 𝟙 C.chosen.lift) := by
  rcases hUnique C.chosen
      (higherLocalizationFactorMorphismComp (W := W) M.backward M.forward)
      (higherLocalizationFactorMorphismId (W := W) C.chosen) with ⟨e⟩
  change (M.backward.hom ≫ M.forward.hom) ≅ 𝟙 C.chosen.lift at e
  exact ⟨e⟩

/-- Therefore every completed Stage II candidate admits some mutual factor
comparison whose completed-carrier composite is isomorphic to the identity.

The theorem still says nothing about the opposite composite on `U.chosen`; that
is precisely the fixed-side obstruction. -/
theorem hasCompletedCarrierCounitSplitComparison
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (C : WeakHigherLocalizationUniversalCandidate (W := W) R)
    (hUnique : C.HasEssentialUniqueness (W := W)) :
    ∃ M : HigherFixedChosenMutualFactorComparison (W := W) U C,
      Nonempty (M.backward.hom ≫ M.forward.hom ≅ 𝟙 C.chosen.lift) := by
  rcases hasMutualFactorComparison (W := W) U C with ⟨M⟩
  exact ⟨M, completedCarrierCounitIso (W := W) U C hUnique M⟩

/-- On a completed carrier, a one-sided v2.37 split comparison upgrades to the
full two-sided factor equivalence data of v2.38.

The fixed-side unit is the inverse of the v2.37 retract.  The completed-carrier
counit is supplied automatically by `completedCarrierCounitIso`. -/
theorem hasTwoSidedCarrierEquivalenceData_of_splitCompletedCarrier
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (C : WeakHigherLocalizationUniversalCandidate (W := W) R)
    (hUnique : C.HasEssentialUniqueness (W := W))
    (S : HigherFixedChosenSplitCarrierComparison (W := W) U C) :
    Nonempty (HigherFixedChosenTwoSidedCarrierEquivalenceData (W := W) U C) := by
  rcases S.fixed_retract with ⟨eFixed⟩
  let M : HigherFixedChosenMutualFactorComparison (W := W) U C :=
    mutualFactorComparisonOfSplit (W := W) S
  rcases completedCarrierCounitIso (W := W) U C hUnique M with ⟨eCompleted⟩
  exact ⟨{
    forward := S.forward
    backward := S.backward
    unit := eFixed.symm
    counit := eCompleted
  }⟩

/-- A split completed carrier therefore yields an actual Mathlib bicategorical
adjoint equivalence between the two localized lifts.

The factor triangles are not forgotten in the construction: they are used first
to build the v2.38 two-sided factor data, from which the adjoint equivalence is
then constructed. -/
theorem hasAdjointEquivalence_of_splitCompletedCarrier
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (C : WeakHigherLocalizationUniversalCandidate (W := W) R)
    (hUnique : C.HasEssentialUniqueness (W := W))
    (S : HigherFixedChosenSplitCarrierComparison (W := W) U C) :
    Nonempty (Bicategory.Equivalence U.chosen.lift C.chosen.lift) := by
  rcases hasTwoSidedCarrierEquivalenceData_of_splitCompletedCarrier
      (W := W) U C hUnique S with ⟨E⟩
  exact ⟨adjointEquivalenceOfTwoSidedCarrierData (W := W) E⟩

/-- Exact fixed-carrier reduction for one completed candidate:

```text
one-sided split comparison
    ↔
two-sided factor equivalence data.
```

The reverse implication is the unconditional v2.38 forgetful construction; the
forward implication is the new Stage III upgrade proved above. -/
theorem nonempty_splitCarrierComparison_iff_nonempty_twoSidedEquivalenceData_of_completed
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (C : WeakHigherLocalizationUniversalCandidate (W := W) R)
    (hUnique : C.HasEssentialUniqueness (W := W)) :
    Nonempty (HigherFixedChosenSplitCarrierComparison (W := W) U C) ↔
      Nonempty (HigherFixedChosenTwoSidedCarrierEquivalenceData (W := W) U C) := by
  constructor
  · rintro ⟨S⟩
    exact hasTwoSidedCarrierEquivalenceData_of_splitCompletedCarrier
      (W := W) U C hUnique S
  · rintro ⟨E⟩
    exact ⟨splitCarrierComparisonOfTwoSidedCarrierData (W := W) E⟩

/-- At the completion-principle level, the v2.38 two-sided condition is therefore
not stronger than the v2.37 split condition: because both predicates quantify
only over candidates already carrying Stage III uniqueness, they are exactly
equivalent. -/
theorem splitCarrierComparisonCompletion_iff_twoSidedCarrierEquivalenceCompletion
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherFixedChosenSplitCarrierComparisonCompletion (W := W) U ↔
      HigherFixedChosenTwoSidedCarrierEquivalenceCompletion (W := W) U := by
  constructor
  · intro hSplit C hUnique
    rcases hSplit C hUnique with ⟨S⟩
    exact hasTwoSidedCarrierEquivalenceData_of_splitCompletedCarrier
      (W := W) U C hUnique S
  · exact splitCarrierComparisonCompletion_of_twoSidedEquivalenceCompletion
      (W := W) U

/-- There exists a Stage III-completed weak carrier carrying two-sided factor
equivalence data with the fixed coherent carrier. -/
def HasHigherFixedChosenTwoSidedEquivalentCompletedCarrier
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) : Prop :=
  ∃ C : WeakHigherLocalizationUniversalCandidate (W := W) R,
    C.HasEssentialUniqueness (W := W) ∧
      Nonempty (HigherFixedChosenTwoSidedCarrierEquivalenceData (W := W) U C)

/-- Existence of a two-sided-equivalent completed carrier is exactly existence of
a split completed carrier. -/
theorem hasTwoSidedEquivalentCompletedCarrier_iff_hasSplitCompletedCarrier
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HasHigherFixedChosenTwoSidedEquivalentCompletedCarrier (W := W) U ↔
      HasHigherFixedChosenSplitCompletedCarrier (W := W) U := by
  constructor
  · rintro ⟨C, hUnique, ⟨E⟩⟩
    exact ⟨C, hUnique, ⟨splitCarrierComparisonOfTwoSidedCarrierData (W := W) E⟩⟩
  · rintro ⟨C, hUnique, ⟨S⟩⟩
    exact ⟨C, hUnique,
      hasTwoSidedCarrierEquivalenceData_of_splitCompletedCarrier
        (W := W) U C hUnique S⟩

/-- Hence existence of a two-sided-equivalent completed carrier is exactly
fixed-carrier Stage III essential uniqueness. -/
theorem hasTwoSidedEquivalentCompletedCarrier_iff_fixedChosenEssentialUniqueness
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HasHigherFixedChosenTwoSidedEquivalentCompletedCarrier (W := W) U ↔
      HigherFixedChosenEssentialUniqueness (W := W) U :=
  (hasTwoSidedEquivalentCompletedCarrier_iff_hasSplitCompletedCarrier
    (W := W) U).trans
      (hasSplitCompletedCarrier_iff_fixedChosenEssentialUniqueness (W := W) U)

/-- Selection formulation: whenever the weak route supplies some Stage III
completed candidate, one can select a completed candidate that is two-sided
factor-equivalent to the fixed coherent carrier. -/
def HigherFixedChosenTwoSidedCarrierEquivalenceSelection
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) : Prop :=
  HasWeakHigherLocalizationUniversalCandidateWithUniqueness (W := W) R →
    HasHigherFixedChosenTwoSidedEquivalentCompletedCarrier (W := W) U

/-- Split-carrier selection and two-sided-equivalence selection are exactly the
same completion problem. -/
theorem splitCarrierSelection_iff_twoSidedCarrierEquivalenceSelection
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherFixedChosenSplitCarrierSelection (W := W) U ↔
      HigherFixedChosenTwoSidedCarrierEquivalenceSelection (W := W) U := by
  constructor
  · intro hSplit hComplete
    exact
      (hasTwoSidedEquivalentCompletedCarrier_iff_hasSplitCompletedCarrier
        (W := W) U).mpr (hSplit hComplete)
  · intro hTwoSided hComplete
    exact
      (hasTwoSidedEquivalentCompletedCarrier_iff_hasSplitCompletedCarrier
        (W := W) U).mp (hTwoSided hComplete)

/-- Coherent route completeness can therefore be expressed exactly as selection
of a Stage III-completed carrier carrying genuine two-sided factor equivalence
data with the fixed carrier. -/
theorem routeCompleteness_iff_twoSidedCarrierEquivalenceSelection
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherCoherentRouteCompleteness (W := W) U ↔
      HigherFixedChosenTwoSidedCarrierEquivalenceSelection (W := W) U :=
  (routeCompleteness_iff_splitCarrierSelection (W := W) U).trans
    (splitCarrierSelection_iff_twoSidedCarrierEquivalenceSelection (W := W) U)

/-- Non-vacuous failure normal form for the two-sided selection route. -/
def HigherFixedChosenTwoSidedCarrierEquivalenceSelectionFailure
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) : Prop :=
  HasWeakHigherLocalizationUniversalCandidateWithUniqueness (W := W) R ∧
    ¬ HasHigherFixedChosenTwoSidedEquivalentCompletedCarrier (W := W) U

/-- Route incompleteness is exactly the non-vacuous failure to select a completed
carrier with two-sided factor equivalence data. -/
theorem not_routeCompleteness_iff_twoSidedCarrierEquivalenceSelectionFailure
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    (¬ HigherCoherentRouteCompleteness (W := W) U) ↔
      HigherFixedChosenTwoSidedCarrierEquivalenceSelectionFailure (W := W) U := by
  classical
  have h := not_congr
    (routeCompleteness_iff_twoSidedCarrierEquivalenceSelection (W := W) U)
  simpa [HigherFixedChosenTwoSidedCarrierEquivalenceSelection,
    HigherFixedChosenTwoSidedCarrierEquivalenceSelectionFailure] using h

/-!
## Boundary after v2.39

For every Stage III-completed carrier `C`, the comparison problem is now reduced
to one exact side:

```text
Stage II factor existence
        |
        v
U --p--> C --q--> U
        |
        | Stage III uniqueness on C
        v
q ≫ p ≅ id_C                    proved automatically

p ≫ q ≅ id_U                    still the fixed-side obstruction
        |
        | together with the automatic C-side isomorphism
        v
two-sided factor equivalence data
        |
        | v2.38 / Mathlib mkOfAdjointifyCounit
        v
actual adjoint equivalence of localized lifts.
```

Thus the remaining obstruction is not the existence of mutual factors, not the
completed-carrier counit side, and not the bicategorical triangle identities.
It is exactly the fixed-side split/unit problem on `U.chosen`.

A next theorem unit should therefore target a justified mechanism producing

```text
p.hom ≫ q.hom ≅ 𝟙 U.chosen.lift
```

for a completed carrier—e.g. from a representable local full-faithfulness,
conservativity, a suitable hom-category universal property, or another explicit
bicategorical cancellation principle.  None of those stronger mechanisms is
assumed here.
-/

end KUOS.DependentOriginationCompletedCarrierTwoSidedUpgradeV2_39
