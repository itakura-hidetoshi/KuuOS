import KUOS.DependentOriginationQuotientGaugeIntersectionObstructionV3_11

namespace KUOS.DependentOriginationQuotientGaugeCoordinateFootprintV3_12

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationCoherenceDefectsV2_65
open KUOS.DependentOriginationGeneratedPointwiseChoiceV2_68
open KUOS.DependentOriginationFiveGeneratedCorrectionCoboundaryV3_00
open KUOS.DependentOriginationQuotientGaugeIndependenceV3_03
open KUOS.DependentOriginationQuotientDefectOrbitV3_06
open KUOS.DependentOriginationThreeRouteCorrectionCompatibilityGapV3_09
open KUOS.DependentOriginationJointCorrectionPowerV3_10
open KUOS.DependentOriginationQuotientGaugeIntersectionObstructionV3_11

universe u v uH vH

/-!
# Finite coordinate footprints of quotient correction loci v3.12

v3.11 identifies the first higher-localization obstruction with nonemptiness of
the total intersection of the concrete quotient-gauge correction loci.

This file exposes the coordinate dependence of each individual locus.

For an associator state `(f,g,h)`, correctness sees only four composition-gauge
coordinates:

```text
gComp(f ≫ g, h)
gComp(f, g)
gComp(g, h)
gComp(f, g ≫ h).
```

No identity-gauge coordinate occurs.

For a left unitor state at `f : X ⟶ Y`, correctness sees only

```text
gComp(𝟙 X, f),  gId(X),
```

and for a right unitor state only

```text
gComp(f, 𝟙 Y),  gId(Y).
```

Thus every statewise correction locus is a cylinder over a finite coordinate
footprint in the full quotient-gauge space.  The total intersection problem is
therefore an amalgamation problem for these overlapping finite footprints, not
an opaque global search through all gauge coordinates.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Two quotient gauges agree on exactly the coordinates inspected by one
concrete quotient-coherence state. -/
def QuotientGaugesAgreeOnRouteState
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (Q Q' : GeneratedQuotientGaugeParameters W R D) :
    ThreeQuotientRouteState W → Prop
  | .associator f g h =>
      Q.mapCompGauge (f ≫ g) h = Q'.mapCompGauge (f ≫ g) h ∧
      Q.mapCompGauge f g = Q'.mapCompGauge f g ∧
      Q.mapCompGauge g h = Q'.mapCompGauge g h ∧
      Q.mapCompGauge f (g ≫ h) = Q'.mapCompGauge f (g ≫ h)
  | .leftUnitor (X := X) f =>
      Q.mapCompGauge (𝟙 X) f = Q'.mapCompGauge (𝟙 X) f ∧
      Q.mapIdGauge X = Q'.mapIdGauge X
  | .rightUnitor (Y := Y) f =>
      Q.mapCompGauge f (𝟙 Y) = Q'.mapCompGauge f (𝟙 Y) ∧
      Q.mapIdGauge Y = Q'.mapIdGauge Y

/-- Agreement on an associator footprint gives equality of the four adjusted
composition witnesses used in that associator equation. -/
private theorem associator_adjusted_mapComp_eqs
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (Q Q' : GeneratedQuotientGaugeParameters W R D)
    {X Y Z T : W.Localization}
    (f : X ⟶ Y) (g : Y ⟶ Z) (h : Z ⟶ T)
    (H : QuotientGaugesAgreeOnRouteState W R D Q Q'
      (.associator f g h)) :
    (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapComp (f ≫ g) h =
        (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q').mapComp (f ≫ g) h ∧
    (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapComp f g =
        (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q').mapComp f g ∧
    (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapComp g h =
        (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q').mapComp g h ∧
    (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapComp f (g ≫ h) =
        (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q').mapComp f (g ≫ h) := by
  rcases H with ⟨Hfgh, Hfg, Hgh, Hfgh'⟩
  constructor
  · simpa [quotientGaugeAdjustedGeneratedPointwiseChoice,
      gaugeAdjustedGeneratedPointwiseChoice,
      canonicalPointwiseGaugeOfQuotientGauge,
      extendGeneratedQuotientGaugeParameters] using
      congrArg (fun q =>
        generatedCompositionMapIso W R D (f ≫ g) h ≪≫ q) Hfgh
  constructor
  · simpa [quotientGaugeAdjustedGeneratedPointwiseChoice,
      gaugeAdjustedGeneratedPointwiseChoice,
      canonicalPointwiseGaugeOfQuotientGauge,
      extendGeneratedQuotientGaugeParameters] using
      congrArg (fun q => generatedCompositionMapIso W R D f g ≪≫ q) Hfg
  constructor
  · simpa [quotientGaugeAdjustedGeneratedPointwiseChoice,
      gaugeAdjustedGeneratedPointwiseChoice,
      canonicalPointwiseGaugeOfQuotientGauge,
      extendGeneratedQuotientGaugeParameters] using
      congrArg (fun q => generatedCompositionMapIso W R D g h ≪≫ q) Hgh
  · simpa [quotientGaugeAdjustedGeneratedPointwiseChoice,
      gaugeAdjustedGeneratedPointwiseChoice,
      canonicalPointwiseGaugeOfQuotientGauge,
      extendGeneratedQuotientGaugeParameters] using
      congrArg (fun q =>
        generatedCompositionMapIso W R D f (g ≫ h) ≪≫ q) Hfgh'

/-- Agreement on a left-unitor footprint gives equality of the two adjusted
witnesses occurring in that equation. -/
private theorem leftUnitor_adjusted_eqs
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (Q Q' : GeneratedQuotientGaugeParameters W R D)
    {X Y : W.Localization} (f : X ⟶ Y)
    (H : QuotientGaugesAgreeOnRouteState W R D Q Q' (.leftUnitor f)) :
    (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapComp (𝟙 X) f =
        (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q').mapComp (𝟙 X) f ∧
    (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapId X =
        (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q').mapId X := by
  rcases H with ⟨Hcomp, Hid⟩
  constructor
  · simpa [quotientGaugeAdjustedGeneratedPointwiseChoice,
      gaugeAdjustedGeneratedPointwiseChoice,
      canonicalPointwiseGaugeOfQuotientGauge,
      extendGeneratedQuotientGaugeParameters] using
      congrArg (fun q =>
        generatedCompositionMapIso W R D (𝟙 X) f ≪≫ q) Hcomp
  · simpa [quotientGaugeAdjustedGeneratedPointwiseChoice,
      gaugeAdjustedGeneratedPointwiseChoice,
      canonicalPointwiseGaugeOfQuotientGauge,
      extendGeneratedQuotientGaugeParameters] using
      congrArg (fun q => generatedIdentityMapIso W R D X ≪≫ q) Hid

/-- Agreement on a right-unitor footprint gives equality of the two adjusted
witnesses occurring in that equation. -/
private theorem rightUnitor_adjusted_eqs
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (Q Q' : GeneratedQuotientGaugeParameters W R D)
    {X Y : W.Localization} (f : X ⟶ Y)
    (H : QuotientGaugesAgreeOnRouteState W R D Q Q' (.rightUnitor f)) :
    (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapComp f (𝟙 Y) =
        (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q').mapComp f (𝟙 Y) ∧
    (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q).mapId Y =
        (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q').mapId Y := by
  rcases H with ⟨Hcomp, Hid⟩
  constructor
  · simpa [quotientGaugeAdjustedGeneratedPointwiseChoice,
      gaugeAdjustedGeneratedPointwiseChoice,
      canonicalPointwiseGaugeOfQuotientGauge,
      extendGeneratedQuotientGaugeParameters] using
      congrArg (fun q =>
        generatedCompositionMapIso W R D f (𝟙 Y) ≪≫ q) Hcomp
  · simpa [quotientGaugeAdjustedGeneratedPointwiseChoice,
      gaugeAdjustedGeneratedPointwiseChoice,
      canonicalPointwiseGaugeOfQuotientGauge,
      extendGeneratedQuotientGaugeParameters] using
      congrArg (fun q => generatedIdentityMapIso W R D Y ≪≫ q) Hid

/-- Statewise correctness depends only on the finite quotient-gauge footprint
listed by `QuotientGaugesAgreeOnRouteState`. -/
theorem quotientRouteCorrectedBy_congr_of_agreesOnRouteState
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (Q Q' : GeneratedQuotientGaugeParameters W R D)
    (s : ThreeQuotientRouteState W)
    (H : QuotientGaugesAgreeOnRouteState W R D Q Q' s) :
    quotientRouteCorrectedBy W R D Q s ↔
      quotientRouteCorrectedBy W R D Q' s := by
  cases s with
  | associator f g h =>
      rcases associator_adjusted_mapComp_eqs W R D Q Q' f g h H with
        ⟨Hfgh, Hfg, Hgh, Hfgh'⟩
      have Hfgh_hom := congrArg Iso.hom Hfgh
      have Hfg_hom := congrArg Iso.hom Hfg
      have Hgh_inv := congrArg Iso.inv Hgh
      have Hfgh'_inv := congrArg Iso.inv Hfgh'
      constructor
      · intro hQ
        have hEq :=
          (quotientAssociatorDefect_eq_refl_iff W R D
            (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q)
            f g h).1 hQ
        apply
          (quotientAssociatorDefect_eq_refl_iff W R D
            (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q')
            f g h).2
        simpa only [Hfgh_hom, Hfg_hom, Hgh_inv, Hfgh'_inv] using hEq
      · intro hQ'
        have hEq :=
          (quotientAssociatorDefect_eq_refl_iff W R D
            (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q')
            f g h).1 hQ'
        apply
          (quotientAssociatorDefect_eq_refl_iff W R D
            (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q)
            f g h).2
        simpa only [← Hfgh_hom, ← Hfg_hom, ← Hgh_inv, ← Hfgh'_inv] using hEq
  | leftUnitor f =>
      rcases leftUnitor_adjusted_eqs W R D Q Q' f H with ⟨Hcomp, Hid⟩
      have Hcomp_hom := congrArg Iso.hom Hcomp
      have Hid_hom := congrArg Iso.hom Hid
      constructor
      · intro hQ
        have hEq :=
          (quotientLeftUnitorDefect_eq_refl_iff W R D
            (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q)
            f).1 hQ
        apply
          (quotientLeftUnitorDefect_eq_refl_iff W R D
            (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q')
            f).2
        simpa only [Hcomp_hom, Hid_hom] using hEq
      · intro hQ'
        have hEq :=
          (quotientLeftUnitorDefect_eq_refl_iff W R D
            (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q')
            f).1 hQ'
        apply
          (quotientLeftUnitorDefect_eq_refl_iff W R D
            (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q)
            f).2
        simpa only [← Hcomp_hom, ← Hid_hom] using hEq
  | rightUnitor f =>
      rcases rightUnitor_adjusted_eqs W R D Q Q' f H with ⟨Hcomp, Hid⟩
      have Hcomp_hom := congrArg Iso.hom Hcomp
      have Hid_hom := congrArg Iso.hom Hid
      constructor
      · intro hQ
        have hEq :=
          (quotientRightUnitorDefect_eq_refl_iff W R D
            (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q)
            f).1 hQ
        apply
          (quotientRightUnitorDefect_eq_refl_iff W R D
            (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q')
            f).2
        simpa only [Hcomp_hom, Hid_hom] using hEq
      · intro hQ'
        have hEq :=
          (quotientRightUnitorDefect_eq_refl_iff W R D
            (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q')
            f).1 hQ'
        apply
          (quotientRightUnitorDefect_eq_refl_iff W R D
            (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q)
            f).2
        simpa only [← Hcomp_hom, ← Hid_hom] using hEq

@[simp]
theorem quotientGaugesAgreeOnRouteState_self
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (Q : GeneratedQuotientGaugeParameters W R D)
    (s : ThreeQuotientRouteState W) :
    QuotientGaugesAgreeOnRouteState W R D Q Q s := by
  cases s <;> simp [QuotientGaugesAgreeOnRouteState]

/-- Each correction locus is a cylinder with respect to its finite route-state
footprint: changing all other quotient-gauge coordinates preserves membership. -/
theorem mem_quotientRouteCorrectionLocus_congr_of_agreesOnRouteState
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (Q Q' : GeneratedQuotientGaugeParameters W R D)
    (s : ThreeQuotientRouteState W)
    (H : QuotientGaugesAgreeOnRouteState W R D Q Q' s) :
    Q ∈ quotientRouteCorrectionLocus W R D s ↔
      Q' ∈ quotientRouteCorrectionLocus W R D s := by
  exact quotientRouteCorrectedBy_congr_of_agreesOnRouteState
    W R D Q Q' s H

/-- A global quotient gauge exists exactly when the statewise correcting gauges
can be amalgamated into one gauge matching each local witness on that state's
finite footprint. -/
theorem commonLocus_nonempty_iff_finiteFootprintAmalgamation
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R) :
    (commonQuotientRouteCorrectionLocus W R D).Nonempty ↔
      ∃ Q : GeneratedQuotientGaugeParameters W R D,
        ∀ s : ThreeQuotientRouteState W,
          ∃ Qs : GeneratedQuotientGaugeParameters W R D,
            Qs ∈ quotientRouteCorrectionLocus W R D s ∧
            QuotientGaugesAgreeOnRouteState W R D Q Qs s := by
  constructor
  · rintro ⟨Q, hQ⟩
    refine ⟨Q, ?_⟩
    intro s
    exact ⟨Q, hQ s, quotientGaugesAgreeOnRouteState_self W R D Q s⟩
  · rintro ⟨Q, hQ⟩
    refine ⟨Q, ?_⟩
    intro s
    rcases hQ s with ⟨Qs, hQs, hagree⟩
    exact
      (mem_quotientRouteCorrectionLocus_congr_of_agreesOnRouteState
        W R D Q Qs s hagree).2 hQs

/-!
## Factorization frontier after v3.12

The v3.11 intersection obstruction is now a finite-coordinate amalgamation
problem.

Each individual equation sees only a small footprint:

* associator: four `gComp` coordinates;
* left unitor: one `gComp` and one `gId` coordinate;
* right unitor: one `gComp` and one `gId` coordinate.

Consequently a common quotient gauge exists exactly when local correcting
gauges can be chosen whose values on these overlapping footprints glue to one
global pair of gauge families.

The next theorem unit should analyze overlap consistency among these finite
footprints.  In particular, one should isolate the compatibility equations
forced when two route states share a `gComp` or `gId` coordinate, and then
test whether generated localization relations make those overlaps automatically
consistent or leave a genuine obstruction.
-/

end KUOS.DependentOriginationQuotientGaugeCoordinateFootprintV3_12
