import KUOS.DependentOriginationSharedCoordinateNormalizerV3_19

namespace KUOS.DependentOriginationOverlapStarTransitivityV3_20

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationQuotientGaugeIndependenceV3_03
open KUOS.DependentOriginationThreeRouteCorrectionCompatibilityGapV3_09
open KUOS.DependentOriginationQuotientGaugeIntersectionObstructionV3_11
open KUOS.DependentOriginationQuotientGaugeCoordinateFootprintV3_12
open KUOS.DependentOriginationQuotientGaugeFootprintOverlapV3_13
open KUOS.DependentOriginationQuotientGaugeCoordinateKeyV3_14
open KUOS.DependentOriginationGlobalFootprintGluingV3_16
open KUOS.DependentOriginationPairwiseCorrelationCountermodelV3_17
open KUOS.DependentOriginationSharedCoordinateNormalizerV3_19

universe u v uH vH

/-!
# Overlap-star transitivity criterion v3.20

v3.18 and v3.19 close the witness-correlation gap by imposing uniqueness, or
uniqueness after normalization, on shared-coordinate values inside each
correction locus.

The concrete associator and unitor correction equations suggest a different
route-specific mechanism. To correlate the nested witnesses of v3.14, it is
enough that compatibility through one common correcting anchor closes
triangles.

If two correcting local gauges are both compatible with one common correcting
anchor, star transitivity says that they are compatible with each other.

Given the nested pairwise predicate, choose one anchor state. The witnesses
provided relative to that anchor form a star. Star transitivity upgrades the
star to a pairwise-compatible family, and v3.16 glues that family globally.

The theorem also handles the degenerate case where the route-state type is
empty: then the globally compatible family is vacuous.

The v3.17 parity countermodel fails the abstract analogue of star transitivity,
so this condition excludes exactly the triangular incompatibility exhibited
there without requiring literal coordinate uniqueness.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Any two correcting local gauges compatible with one common correcting
anchor are automatically compatible with each other. -/
def OverlapStarTransitiveCorrectionLoci
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R) : Prop :=
  ∀ s : ThreeQuotientRouteState W,
    ∀ Qs : GeneratedQuotientGaugeParameters W R D,
      Qs ∈ quotientRouteCorrectionLocus W R D s →
      ∀ t u : ThreeQuotientRouteState W,
        ∀ Qt Qu : GeneratedQuotientGaugeParameters W R D,
          Qt ∈ quotientRouteCorrectionLocus W R D t →
          Qu ∈ quotientRouteCorrectionLocus W R D u →
          AgreeOnRouteFootprintOverlap W R D s t Qs Qt →
          AgreeOnRouteFootprintOverlap W R D s u Qs Qu →
            AgreeOnRouteFootprintOverlap W R D t u Qt Qu

/-- Nested pairwise-compatible local corrections correlate into one globally
compatible family under overlap-star transitivity. -/
theorem hasGloballyCompatibleLocalCorrectionFamily_of_pairwiseShared_of_starTransitive
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (hPair :
      HasPairwiseSharedCoordinateCompatibleLocalCorrections W R D)
    (hStar : OverlapStarTransitiveCorrectionLoci W R D) :
    HasGloballyCompatibleLocalCorrectionFamily W R D := by
  classical
  by_cases hNonempty : Nonempty (ThreeQuotientRouteState W)
  · let s0 : ThreeQuotientRouteState W := Classical.choice hNonempty
    rcases hPair s0 with ⟨Q0, hQ0, hStarWitnesses⟩
    let Qlocal :
        ∀ t : ThreeQuotientRouteState W,
          GeneratedQuotientGaugeParameters W R D :=
      fun t => Classical.choose (hStarWitnesses t)
    have hCorrect :
        ∀ t : ThreeQuotientRouteState W,
          Qlocal t ∈ quotientRouteCorrectionLocus W R D t := by
      intro t
      exact (Classical.choose_spec (hStarWitnesses t)).1
    have hAnchorOverlap :
        ∀ t : ThreeQuotientRouteState W,
          AgreeOnRouteFootprintOverlap W R D s0 t Q0 (Qlocal t) := by
      intro t
      exact (Classical.choose_spec (hStarWitnesses t)).2
    refine ⟨Qlocal, hCorrect, ?_⟩
    intro t u
    exact
      hStar s0 Q0 hQ0 t u (Qlocal t) (Qlocal u)
        (hCorrect t) (hCorrect u)
        (hAnchorOverlap t) (hAnchorOverlap u)
  · refine ⟨fun s => False.elim (hNonempty ⟨s⟩), ?_, ?_⟩
    · intro s
      exact False.elim (hNonempty ⟨s⟩)
    · intro s
      exact False.elim (hNonempty ⟨s⟩)

/-- Therefore star transitivity closes the finite-footprint amalgamation
problem from the nested pairwise predicate. -/
theorem hasFiniteFootprintAmalgamation_of_pairwiseShared_of_starTransitive
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (hPair :
      HasPairwiseSharedCoordinateCompatibleLocalCorrections W R D)
    (hStar : OverlapStarTransitiveCorrectionLoci W R D) :
    HasFiniteFootprintAmalgamation W R D := by
  exact
    hasFiniteFootprintAmalgamation_of_globalFamily W R D
      (hasGloballyCompatibleLocalCorrectionFamily_of_pairwiseShared_of_starTransitive
        W R D hPair hStar)

/-- Star transitivity rules out the v3.16 witness-correlation obstruction. -/
theorem not_pairwiseWitnessCorrelationGap_of_starTransitive
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (hStar : OverlapStarTransitiveCorrectionLoci W R D) :
    ¬ PairwiseWitnessCorrelationGap W R D := by
  rintro ⟨hPair, hNoGlobal⟩
  exact hNoGlobal
    (hasGloballyCompatibleLocalCorrectionFamily_of_pairwiseShared_of_starTransitive
      W R D hPair hStar)

/-- Abstract v3.17 analogue of overlap-star transitivity. -/
def AbstractOverlapStarTransitive : Prop :=
  ∀ s : CorrelationState,
    ∀ qs : CorrelationCoord → Bool,
      LocalCorrected s qs →
      ∀ t u : CorrelationState,
        ∀ qt qu : CorrelationCoord → Bool,
          LocalCorrected t qt →
          LocalCorrected u qu →
          OverlapAgree s t qs qt →
          OverlapAgree s u qs qu →
            OverlapAgree t u qt qu

/-- The v3.17 parity triangle violates star transitivity. Use state a as the
anchor, the zero section at b, and cFromA at c. Both agree with the anchor,
but they disagree at the bc coordinate shared by b and c. -/
theorem not_abstractOverlapStarTransitive :
    ¬ AbstractOverlapStarTransitive := by
  intro hStar
  have hBC :=
    hStar .a zeroSection zeroSection_local_a
      .b .c zeroSection cFromA
      zeroSection_local_b cFromA_local_c
      (by
        intro k _ _
        rfl)
      (by
        intro k hka hkc
        cases k <;>
          simp [footprint, zeroSection, cFromA] at hka hkc ⊢)
  have hEq :
      zeroSection .bc = cFromA .bc :=
    hBC .bc
      (by simp [footprint])
      (by simp [footprint])
  simpa [zeroSection, cFromA] using hEq

/-!
## Factorization frontier after v3.20

There are now three structurally different sufficient routes that eliminate
the v3.17 correlation obstruction:

1. literal shared-coordinate rigidity from v3.18;
2. routewise gauge fixing to normalized rigidity from v3.19;
3. overlap-star transitivity from v3.20.

The third criterion does not ask that correcting witnesses be unique. It asks
only that compatibility through one common correcting anchor close triangles.

This is closer to a cocycle/descent condition and therefore better matched to
the actual associator and unitor equations. The next route-specific theorem
unit should inspect whether the concrete generated quotient correction loci
satisfy this triangle-closing property, possibly first for the unitor-only
subsystem and then for associator/unit mixed triangles.

No claim is made here that the full concrete correction loci already satisfy
star transitivity.
-/

end KUOS.DependentOriginationOverlapStarTransitivityV3_20
