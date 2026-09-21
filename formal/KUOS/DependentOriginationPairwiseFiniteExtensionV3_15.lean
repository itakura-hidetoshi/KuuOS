import KUOS.DependentOriginationQuotientGaugeCoordinateKeyV3_14

namespace KUOS.DependentOriginationPairwiseFiniteExtensionV3_15

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationCoherentQuotientTransportV2_59
open KUOS.DependentOriginationQuotientGaugeIndependenceV3_03
open KUOS.DependentOriginationThreeRouteCorrectionCompatibilityGapV3_09
open KUOS.DependentOriginationQuotientGaugeIntersectionObstructionV3_11
open KUOS.DependentOriginationQuotientGaugeCoordinateFootprintV3_12
open KUOS.DependentOriginationQuotientGaugeFootprintOverlapV3_13
open KUOS.DependentOriginationQuotientGaugeCoordinateKeyV3_14

universe u v uH vH

set_option linter.unnecessarySimpa false

/-!
# Pairwise finite extension of quotient-gauge footprints v3.15

v3.14 reduced pairwise compatibility to equality of the dependent quotient-gauge
values on the literal intersection of two finite route footprints, but retained
the converse as an explicit extension problem.

For the actual v3.03 quotient-gauge parameter space that converse can be
constructed directly.  A quotient gauge is only the pair of arbitrary dependent
families

* `mapIdGauge`;
* `mapCompGauge`.

Given local gauges `Qs` and `Qt`, define a patched gauge by taking `Qs` on
the footprint of `s`, `Qt` on the remaining coordinates of the footprint of
`t`, and `Qs` elsewhere.  Agreement on shared coordinates makes this one
gauge extend both local finite restrictions.

The patch is noncomputable only because footprint membership is decided
classically.  No compactness, convexity, topology, Helly theorem, or additional
algebraic hypothesis is used.

The main result is therefore

```text
AgreeOnRouteFootprintOverlap s t Qs Qt
  <->
CompatibleOnRouteOverlap s t Qs Qt.
```

Consequently the v3.14 predicate
`SharedCoordinatesButNoPairwiseExtension` is impossible for the actual
quotient-gauge family, and coordinate-level pairwise compatibility is
equivalent to the v3.13 common-extension formulation.

This closes the pairwise extension subproblem.  The next genuine issue is
pairwise-to-global amalgamation across all route states.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Patch two quotient gauges along two finite route footprints.

The first footprint has priority.  On an overlap the two values are assumed
equal only when proving the extension property below, so the definition itself
does not require a compatibility hypothesis. -/
noncomputable def patchQuotientGaugesOnRoutePair
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (s t : ThreeQuotientRouteState W)
    (Qs Qt : GeneratedQuotientGaugeParameters W R D) :
    GeneratedQuotientGaugeParameters W R D := by
  classical
  exact
    { mapIdGauge := fun X =>
        if RouteFootprintContains W s (.identity X) then
          Qs.mapIdGauge X
        else if RouteFootprintContains W t (.identity X) then
          Qt.mapIdGauge X
        else
          Qs.mapIdGauge X
      mapCompGauge := fun f g =>
        if RouteFootprintContains W s (.composition f g) then
          Qs.mapCompGauge f g
        else if RouteFootprintContains W t (.composition f g) then
          Qt.mapCompGauge f g
        else
          Qs.mapCompGauge f g }

/-- On the first route footprint, the patched gauge is literally the first
local gauge. -/
theorem patchQuotientGaugesOnRoutePair_value_of_left
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (s t : ThreeQuotientRouteState W)
    (Qs Qt : GeneratedQuotientGaugeParameters W R D)
    (c : QuotientGaugeCoordinate W)
    (hc : RouteFootprintContains W s c) :
    quotientGaugeCoordinateValue W R D
        (patchQuotientGaugesOnRoutePair W R D s t Qs Qt) c =
      quotientGaugeCoordinateValue W R D Qs c := by
  classical
  cases c with
  | identity X =>
      simp [patchQuotientGaugesOnRoutePair,
        quotientGaugeCoordinateValue, hc]
  | composition f g =>
      simp [patchQuotientGaugesOnRoutePair,
        quotientGaugeCoordinateValue, hc]

/-- On the second route footprint, overlap agreement makes the patched gauge
equal to the second local gauge as well. -/
theorem patchQuotientGaugesOnRoutePair_value_of_right
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (s t : ThreeQuotientRouteState W)
    (Qs Qt : GeneratedQuotientGaugeParameters W R D)
    (H : AgreeOnRouteFootprintOverlap W R D s t Qs Qt)
    (c : QuotientGaugeCoordinate W)
    (hc : RouteFootprintContains W t c) :
    quotientGaugeCoordinateValue W R D
        (patchQuotientGaugesOnRoutePair W R D s t Qs Qt) c =
      quotientGaugeCoordinateValue W R D Qt c := by
  classical
  by_cases hs : RouteFootprintContains W s c
  · exact
      (patchQuotientGaugesOnRoutePair_value_of_left
        W R D s t Qs Qt c hs).trans (H c hs hc)
  · cases c with
    | identity X =>
        simp [patchQuotientGaugesOnRoutePair,
          quotientGaugeCoordinateValue, hs, hc]
    | composition f g =>
        simp [patchQuotientGaugesOnRoutePair,
          quotientGaugeCoordinateValue, hs, hc]

/-- Coordinate equality on every key of one route footprint reconstructs the
v3.12 route-state agreement relation.

This is the reverse normalization deliberately deferred by v3.14.  It is proved
route-by-route, so no dependent global reconstruction principle is hidden. -/
theorem quotientGaugesAgreeOnRouteState_of_coordinateValue_eq
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (Q Q' : GeneratedQuotientGaugeParameters W R D)
    (s : ThreeQuotientRouteState W)
    (H : ∀ c : QuotientGaugeCoordinate W,
      RouteFootprintContains W s c →
        quotientGaugeCoordinateValue W R D Q c =
          quotientGaugeCoordinateValue W R D Q' c) :
    QuotientGaugesAgreeOnRouteState W R D Q Q' s := by
  cases s with
  | associator f g h =>
      refine ⟨?_, ?_, ?_, ?_⟩
      · simpa only [quotientGaugeCoordinateValue] using
          H (.composition (f ≫ g) h)
            (by simp [RouteFootprintContains])
      · simpa only [quotientGaugeCoordinateValue] using
          H (.composition f g)
            (by simp [RouteFootprintContains])
      · simpa only [quotientGaugeCoordinateValue] using
          H (.composition g h)
            (by simp [RouteFootprintContains])
      · simpa only [quotientGaugeCoordinateValue] using
          H (.composition f (g ≫ h))
            (by simp [RouteFootprintContains])
  | leftUnitor f =>
      constructor
      · simpa only [quotientGaugeCoordinateValue] using
          H (.composition (𝟙 _) f)
            (by simp [RouteFootprintContains])
      · simpa only [quotientGaugeCoordinateValue] using
          H (.identity _)
            (by simp [RouteFootprintContains])
  | rightUnitor f =>
      constructor
      · simpa only [quotientGaugeCoordinateValue] using
          H (.composition f (𝟙 _))
            (by simp [RouteFootprintContains])
      · simpa only [quotientGaugeCoordinateValue] using
          H (.identity _)
            (by simp [RouteFootprintContains])

/-- The pair patch extends the first local route restriction. -/
theorem patchQuotientGaugesOnRoutePair_agrees_left
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (s t : ThreeQuotientRouteState W)
    (Qs Qt : GeneratedQuotientGaugeParameters W R D) :
    QuotientGaugesAgreeOnRouteState W R D
      (patchQuotientGaugesOnRoutePair W R D s t Qs Qt) Qs s := by
  apply quotientGaugesAgreeOnRouteState_of_coordinateValue_eq
    W R D
  intro c hc
  exact patchQuotientGaugesOnRoutePair_value_of_left
    W R D s t Qs Qt c hc

/-- Under shared-coordinate agreement, the pair patch also extends the second
local route restriction. -/
theorem patchQuotientGaugesOnRoutePair_agrees_right
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (s t : ThreeQuotientRouteState W)
    (Qs Qt : GeneratedQuotientGaugeParameters W R D)
    (H : AgreeOnRouteFootprintOverlap W R D s t Qs Qt) :
    QuotientGaugesAgreeOnRouteState W R D
      (patchQuotientGaugesOnRoutePair W R D s t Qs Qt) Qt t := by
  apply quotientGaugesAgreeOnRouteState_of_coordinateValue_eq
    W R D
  intro c hc
  exact patchQuotientGaugesOnRoutePair_value_of_right
    W R D s t Qs Qt H c hc

/-- Agreement on every literally shared finite coordinate is sufficient for a
common pairwise extension in the actual quotient-gauge parameter space. -/
theorem compatibleOnRouteOverlap_of_agreeOnRouteFootprintOverlap
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (s t : ThreeQuotientRouteState W)
    (Qs Qt : GeneratedQuotientGaugeParameters W R D)
    (H : AgreeOnRouteFootprintOverlap W R D s t Qs Qt) :
    CompatibleOnRouteOverlap W R D s t Qs Qt := by
  refine
    ⟨patchQuotientGaugesOnRoutePair W R D s t Qs Qt, ?_, ?_⟩
  · exact patchQuotientGaugesOnRoutePair_agrees_left
      W R D s t Qs Qt
  · exact patchQuotientGaugesOnRoutePair_agrees_right
      W R D s t Qs Qt H

/-- v3.13 common-extension compatibility and v3.14 shared-coordinate
compatibility are exactly equivalent. -/
theorem compatibleOnRouteOverlap_iff_agreeOnRouteFootprintOverlap
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (s t : ThreeQuotientRouteState W)
    (Qs Qt : GeneratedQuotientGaugeParameters W R D) :
    CompatibleOnRouteOverlap W R D s t Qs Qt ↔
      AgreeOnRouteFootprintOverlap W R D s t Qs Qt := by
  constructor
  · exact agreeOnRouteFootprintOverlap_of_compatibleOnRouteOverlap
      W R D s t Qs Qt
  · exact compatibleOnRouteOverlap_of_agreeOnRouteFootprintOverlap
      W R D s t Qs Qt

/-- Coordinate-level pairwise-compatible local corrections are equivalent to
pairwise common-extension-compatible local corrections. -/
theorem hasPairwiseOverlapCompatibleLocalCorrections_iff_sharedCoordinates
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R) :
    HasPairwiseOverlapCompatibleLocalCorrections W R D ↔
      HasPairwiseSharedCoordinateCompatibleLocalCorrections W R D := by
  constructor
  · exact
      hasPairwiseSharedCoordinateCompatibleLocalCorrections_of_pairwiseOverlap
        W R D
  · intro H s
    rcases H s with ⟨Qs, hQs, hs⟩
    refine ⟨Qs, hQs, ?_⟩
    intro t
    rcases hs t with ⟨Qt, hQt, hover⟩
    exact
      ⟨Qt, hQt,
        compatibleOnRouteOverlap_of_agreeOnRouteFootprintOverlap
          W R D s t Qs Qt hover⟩

/-- The v3.14 proposed gap between shared-coordinate compatibility and pairwise
extension cannot occur for the actual quotient-gauge family. -/
theorem not_sharedCoordinatesButNoPairwiseExtension
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R) :
    ¬ SharedCoordinatesButNoPairwiseExtension W R D := by
  rintro ⟨hShared, hNoPairwise⟩
  apply hNoPairwise
  exact
    (hasPairwiseOverlapCompatibleLocalCorrections_iff_sharedCoordinates
      W R D).2 hShared

/-!
## Factorization frontier after v3.15

The pairwise finite-extension question is closed positively:

```text
shared-coordinate agreement
        <->
one common extension over the two finite footprints.
```

The proof is specific to the actual quotient-gauge space: its `gId/gComp`
fields are unrestricted dependent families and can therefore be patched
coordinatewise.  Classical footprint-membership decision is explicit in the
noncomputable patch.

The next unresolved implication is genuinely global:

```text
for every pair of route states:
  compatible finite local restrictions
        ?->
one quotient gauge compatible with all route states.
```

Equivalently, one must determine whether pairwise-compatible local correction
data force `HasFiniteFootprintAmalgamation`, or whether a higher-order
multi-overlap obstruction remains.

No pairwise counterexample can now witness that obstruction.
-/

end KUOS.DependentOriginationPairwiseFiniteExtensionV3_15
