import KUOS.DependentOriginationQuotientGaugeFootprintOverlapV3_13

namespace KUOS.DependentOriginationQuotientGaugeCoordinateKeyV3_14

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationCoherentQuotientTransportV2_59
open KUOS.DependentOriginationQuotientGaugeIndependenceV3_03
open KUOS.DependentOriginationThreeRouteCorrectionCompatibilityGapV3_09
open KUOS.DependentOriginationQuotientGaugeIntersectionObstructionV3_11
open KUOS.DependentOriginationQuotientGaugeCoordinateFootprintV3_12
open KUOS.DependentOriginationQuotientGaugeFootprintOverlapV3_13

universe u v uH vH

set_option linter.unnecessarySimpa false

/-!
# Coordinate-key normal form for quotient-gauge footprints v3.14

v3.12 lists the finite `gId/gComp` coordinates inspected by each quotient
coherence route.  v3.13 packages pairwise compatibility as existence of one
quotient gauge extending two finite local restrictions and proves several
concrete shared-coordinate equalities.

This file removes the remaining case-by-case ambiguity by introducing one
dependent coordinate-key type for the quotient gauge space.

A coordinate is either

```text
id X
comp f g
```

and its value type is exactly the corresponding automorphism type used by
`GeneratedQuotientGaugeParameters`.

Each route state determines a finite predicate `RouteFootprintContains` on
these keys.  The main theorem identifies the v3.12 relation

```text
QuotientGaugesAgreeOnRouteState Q Q' s
```

with ordinary equality of coordinate values at every key in the finite
footprint of `s`.

Consequently v3.13 pairwise overlap compatibility implies equality at every
coordinate lying in both footprints, not merely the five displayed examples.

No converse extension theorem is assumed.  In particular, this file does not
claim that agreement on all shared keys is sufficient to construct a common
extension gauge; that constructive extension problem is left explicit for the
next theorem unit.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- A key for one coordinate of the quotient-only gauge parameter space. -/
inductive QuotientGaugeCoordinate : Type (max u v) where
  | identity (X : W.Localization)
  | composition {X Y Z : W.Localization}
      (f : X ⟶ Y) (g : Y ⟶ Z)

/-- The dependent value type stored at one quotient-gauge coordinate. -/
def QuotientGaugeCoordinateFiber
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R) :
    QuotientGaugeCoordinate W → Type _
  | .identity X =>
      (𝟙 (R.obj (.mk X.as.obj))) ≅ 𝟙 (R.obj (.mk X.as.obj))
  | .composition f g =>
      (quotientRepresentativeMap W R D f ≫
          quotientRepresentativeMap W R D g) ≅
        (quotientRepresentativeMap W R D f ≫
          quotientRepresentativeMap W R D g)

/-- Evaluate a quotient gauge at one coordinate key. -/
def quotientGaugeCoordinateValue
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (Q : GeneratedQuotientGaugeParameters W R D) :
    (c : QuotientGaugeCoordinate W) →
      QuotientGaugeCoordinateFiber W R D c
  | .identity X => Q.mapIdGauge X
  | .composition f g => Q.mapCompGauge f g

/-- The exact finite set of quotient-gauge coordinate keys inspected by one
route state. -/
def RouteFootprintContains :
    ThreeQuotientRouteState W → QuotientGaugeCoordinate W → Prop
  | .associator f g h, c =>
      c = .composition (f ≫ g) h ∨
      c = .composition f g ∨
      c = .composition g h ∨
      c = .composition f (g ≫ h)
  | .leftUnitor (X := X) f, c =>
      c = .composition (𝟙 X) f ∨
      c = .identity X
  | .rightUnitor (Y := Y) f, c =>
      c = .composition f (𝟙 Y) ∨
      c = .identity Y

/-- Agreement on a v3.12 route footprint gives equality of the dependent gauge
value at every coordinate key belonging to that footprint. -/
theorem quotientGaugeCoordinateValue_eq_of_agreesOnRouteState
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (Q Q' : GeneratedQuotientGaugeParameters W R D)
    (s : ThreeQuotientRouteState W)
    (H : QuotientGaugesAgreeOnRouteState W R D Q Q' s)
    (c : QuotientGaugeCoordinate W)
    (hc : RouteFootprintContains W s c) :
    quotientGaugeCoordinateValue W R D Q c =
      quotientGaugeCoordinateValue W R D Q' c := by
  cases s with
  | associator f g h =>
      simp only [RouteFootprintContains] at hc
      rcases hc with hc | hc | hc | hc
      · subst c
        simpa [quotientGaugeCoordinateValue,
          QuotientGaugesAgreeOnRouteState] using H.1
      · subst c
        simpa [quotientGaugeCoordinateValue,
          QuotientGaugesAgreeOnRouteState] using H.2.1
      · subst c
        simpa [quotientGaugeCoordinateValue,
          QuotientGaugesAgreeOnRouteState] using H.2.2.1
      · subst c
        simpa [quotientGaugeCoordinateValue,
          QuotientGaugesAgreeOnRouteState] using H.2.2.2
  | leftUnitor f =>
      simp only [RouteFootprintContains] at hc
      rcases hc with hc | hc
      · subst c
        simpa [quotientGaugeCoordinateValue,
          QuotientGaugesAgreeOnRouteState] using H.1
      · subst c
        simpa [quotientGaugeCoordinateValue,
          QuotientGaugesAgreeOnRouteState] using H.2
  | rightUnitor f =>
      simp only [RouteFootprintContains] at hc
      rcases hc with hc | hc
      · subst c
        simpa [quotientGaugeCoordinateValue,
          QuotientGaugesAgreeOnRouteState] using H.1
      · subst c
        simpa [quotientGaugeCoordinateValue,
          QuotientGaugesAgreeOnRouteState] using H.2

/-!
The converse direction is intentionally not asserted in v3.14.  Reconstructing
one dependent quotient-gauge family from coordinate equalities is an extension
problem rather than a definitional simplification; it is isolated for v3.15.
-/

/-- Two local quotient gauges agree on the actual overlap of two route
footprints when their dependent coordinate values agree at every key belonging
to both footprints. -/
def AgreeOnRouteFootprintOverlap
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (s t : ThreeQuotientRouteState W)
    (Qs Qt : GeneratedQuotientGaugeParameters W R D) : Prop :=
  ∀ c : QuotientGaugeCoordinate W,
    RouteFootprintContains W s c →
    RouteFootprintContains W t c →
      quotientGaugeCoordinateValue W R D Qs c =
        quotientGaugeCoordinateValue W R D Qt c

/-- The concrete overlap-agreement relation is symmetric. -/
theorem agreeOnRouteFootprintOverlap_symm
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (s t : ThreeQuotientRouteState W)
    (Qs Qt : GeneratedQuotientGaugeParameters W R D) :
    AgreeOnRouteFootprintOverlap W R D s t Qs Qt ↔
      AgreeOnRouteFootprintOverlap W R D t s Qt Qs := by
  constructor
  · intro h c htc hsc
    exact (h c hsc htc).symm
  · intro h c hsc htc
    exact (h c htc hsc).symm

/-- v3.13 pairwise common-extension compatibility forces equality on every
genuinely shared quotient-gauge coordinate. -/
theorem agreeOnRouteFootprintOverlap_of_compatibleOnRouteOverlap
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (s t : ThreeQuotientRouteState W)
    (Qs Qt : GeneratedQuotientGaugeParameters W R D)
    (H : CompatibleOnRouteOverlap W R D s t Qs Qt) :
    AgreeOnRouteFootprintOverlap W R D s t Qs Qt := by
  rcases H with ⟨Q, hs, ht⟩
  intro c hsc htc
  have hsValue :=
    quotientGaugeCoordinateValue_eq_of_agreesOnRouteState
      W R D Q Qs s hs c hsc
  have htValue :=
    quotientGaugeCoordinateValue_eq_of_agreesOnRouteState
      W R D Q Qt t ht c htc
  exact hsValue.symm.trans htValue

/-- The v3.13 left/left identity-coordinate overlap is recovered as an instance
of the generic coordinate-key theorem. -/
theorem mapId_eq_of_compatible_leftUnitor_leftUnitor_via_coordinate
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y Z : W.Localization}
    (f : X ⟶ Y) (g : X ⟶ Z)
    (Qs Qt : GeneratedQuotientGaugeParameters W R D)
    (H : CompatibleOnRouteOverlap W R D
      (.leftUnitor f) (.leftUnitor g) Qs Qt) :
    Qs.mapIdGauge X = Qt.mapIdGauge X := by
  have hover :=
    agreeOnRouteFootprintOverlap_of_compatibleOnRouteOverlap
      W R D (.leftUnitor f) (.leftUnitor g) Qs Qt H
  simpa [quotientGaugeCoordinateValue, QuotientGaugeCoordinateFiber] using
    hover (.identity X)
      (by simp [RouteFootprintContains])
      (by simp [RouteFootprintContains])

/-- Pairwise overlap-compatible local correction data from v3.13 therefore
always carries a weaker, purely coordinate-level pairwise compatibility. -/
def HasPairwiseSharedCoordinateCompatibleLocalCorrections
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R) : Prop :=
  ∀ s : ThreeQuotientRouteState W,
    ∃ Qs : GeneratedQuotientGaugeParameters W R D,
      Qs ∈ quotientRouteCorrectionLocus W R D s ∧
        ∀ t : ThreeQuotientRouteState W,
          ∃ Qt : GeneratedQuotientGaugeParameters W R D,
            Qt ∈ quotientRouteCorrectionLocus W R D t ∧
              AgreeOnRouteFootprintOverlap W R D s t Qs Qt

/-- Common-extension pairwise compatibility implies shared-coordinate pairwise
compatibility. -/
theorem hasPairwiseSharedCoordinateCompatibleLocalCorrections_of_pairwiseOverlap
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (H : HasPairwiseOverlapCompatibleLocalCorrections W R D) :
    HasPairwiseSharedCoordinateCompatibleLocalCorrections W R D := by
  intro s
  rcases H s with ⟨Qs, hQs, hs⟩
  refine ⟨Qs, hQs, ?_⟩
  intro t
  rcases hs t with ⟨Qt, hQt, hcompat⟩
  exact ⟨Qt, hQt,
    agreeOnRouteFootprintOverlap_of_compatibleOnRouteOverlap
      W R D s t Qs Qt hcompat⟩

/-- Hence genuine finite-footprint amalgamation implies coordinate-level
pairwise overlap compatibility. -/
theorem hasPairwiseSharedCoordinateCompatibleLocalCorrections_of_finiteFootprintAmalgamation
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (H : HasFiniteFootprintAmalgamation W R D) :
    HasPairwiseSharedCoordinateCompatibleLocalCorrections W R D := by
  exact
    hasPairwiseSharedCoordinateCompatibleLocalCorrections_of_pairwiseOverlap
      W R D
      (hasPairwiseOverlapCompatibleLocalCorrections_of_finiteFootprintAmalgamation
        W R D H)

/-- The next constructive gap: local correcting gauges can be chosen to agree
on every literally shared coordinate, but no pairwise common extension gauge is
available.  Existence of such a gap is not asserted here. -/
def SharedCoordinatesButNoPairwiseExtension
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R) : Prop :=
  HasPairwiseSharedCoordinateCompatibleLocalCorrections W R D ∧
    ¬ HasPairwiseOverlapCompatibleLocalCorrections W R D

/-!
## Factorization frontier after v3.14

The quotient-stage finite gluing problem now has a literal coordinate language.

For every route state `s`, v3.14 proves the forward coordinate normalization:

```text
QuotientGaugesAgreeOnRouteState Q Q' s
  ->
Q and Q' have equal values at every coordinate key in footprint(s).
```

For every pair `s,t`:

```text
CompatibleOnRouteOverlap s t Qs Qt
  ->
Qs and Qt agree at every key in footprint(s) ∩ footprint(t).
```

Thus the v3.13 compatibility relation has been reduced to an ordinary
dependent-coordinate overlap condition as a necessary consequence.

The converse remains deliberately open:

```text
agreement on every shared coordinate
  ?->
existence of one gauge extending both finite restrictions.
```

Proving that converse requires an actual finite extension/patching construction
in the dependent gauge family; it cannot be obtained by renaming the overlap
condition.  v3.15 should test precisely that extension lemma, keeping any use of
classical decidable equality or choice explicit.

Only after that pairwise extension problem is settled should one ask whether
pairwise-compatible finite restrictions force one global amalgamation.
-/

end KUOS.DependentOriginationQuotientGaugeCoordinateKeyV3_14
