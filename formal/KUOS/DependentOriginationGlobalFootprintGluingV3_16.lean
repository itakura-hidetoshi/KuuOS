import KUOS.DependentOriginationPairwiseFiniteExtensionV3_15

namespace KUOS.DependentOriginationGlobalFootprintGluingV3_16

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
open KUOS.DependentOriginationPairwiseFiniteExtensionV3_15

universe u v uH vH

set_option linter.unnecessarySimpa false

/-!
# Global gluing from one compatible local correction family v3.16

v3.15 proves that, for any fixed pair of route states, equality on the literal
intersection of their finite coordinate footprints is equivalent to existence
of one quotient gauge extending both restrictions.

That closes pairwise extension.  The remaining issue is the quantifier order in
the local witnesses.

The v3.13 pairwise predicate has the shape

```text
∀ s, ∃ Q_s, local(s,Q_s) ∧
  ∀ t, ∃ Q_t, local(t,Q_t) ∧ compatible(s,t,Q_s,Q_t),
```

where the witness chosen for `t` may depend on the anchor state `s`.

This file separates that from a genuinely coherent family

```text
∃ Qlocal : ∀ s, Gauge,
  (∀ s, local(s,Qlocal s))
  ∧
  (∀ s t, Qlocal s and Qlocal t agree on every shared coordinate).
```

For the actual quotient-gauge parameter space, such a single compatible family
always glues globally.  At each gauge coordinate, choose any route state whose
footprint contains that coordinate and copy the local value from that state.
Pairwise overlap equality makes the result independent of which route state was
chosen.

Thus:

```text
HasFiniteFootprintAmalgamation
  <->
HasGloballyCompatibleLocalCorrectionFamily.
```

No compactness, convexity, Helly theorem, finiteness of the total route-state
type, or extra algebraic structure is used.  Classical choice is explicit in
the global coordinate selector.

The unresolved gap after v3.16 is therefore not geometric patching.  It is the
correlation/selection gap between nested pairwise witnesses and one globally
chosen pairwise-compatible local family.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- One simultaneous choice of a correcting local quotient gauge for every
route state, pairwise equal on all literally shared footprint coordinates. -/
def HasGloballyCompatibleLocalCorrectionFamily
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R) : Prop :=
  ∃ Qlocal :
      ∀ s : ThreeQuotientRouteState W,
        GeneratedQuotientGaugeParameters W R D,
    (∀ s : ThreeQuotientRouteState W,
      Qlocal s ∈ quotientRouteCorrectionLocus W R D s) ∧
    ∀ s t : ThreeQuotientRouteState W,
      AgreeOnRouteFootprintOverlap W R D s t (Qlocal s) (Qlocal t)

/-- A coherent local family is stronger than the nested pairwise existence
predicate of v3.14. -/
theorem hasPairwiseSharedCoordinateCompatibleLocalCorrections_of_globalFamily
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (H : HasGloballyCompatibleLocalCorrectionFamily W R D) :
    HasPairwiseSharedCoordinateCompatibleLocalCorrections W R D := by
  rcases H with ⟨Qlocal, hCorrect, hPair⟩
  intro s
  refine ⟨Qlocal s, hCorrect s, ?_⟩
  intro t
  exact ⟨Qlocal t, hCorrect t, hPair s t⟩

/-- Finite-footprint amalgamation supplies a globally pairwise-compatible family
of local correcting gauges. -/
theorem hasGloballyCompatibleLocalCorrectionFamily_of_finiteFootprintAmalgamation
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (H : HasFiniteFootprintAmalgamation W R D) :
    HasGloballyCompatibleLocalCorrectionFamily W R D := by
  classical
  rcases H with ⟨Q, hQ⟩
  let Qlocal :
      ∀ s : ThreeQuotientRouteState W,
        GeneratedQuotientGaugeParameters W R D :=
    fun s => Classical.choose (hQ s)
  have hCorrect :
      ∀ s : ThreeQuotientRouteState W,
        Qlocal s ∈ quotientRouteCorrectionLocus W R D s := by
    intro s
    exact (Classical.choose_spec (hQ s)).1
  have hAgree :
      ∀ s : ThreeQuotientRouteState W,
        QuotientGaugesAgreeOnRouteState W R D Q (Qlocal s) s := by
    intro s
    exact (Classical.choose_spec (hQ s)).2
  refine ⟨Qlocal, hCorrect, ?_⟩
  intro s t c hsc htc
  have hs :=
    quotientGaugeCoordinateValue_eq_of_agreesOnRouteState
      W R D Q (Qlocal s) s (hAgree s) c hsc
  have ht :=
    quotientGaugeCoordinateValue_eq_of_agreesOnRouteState
      W R D Q (Qlocal t) t (hAgree t) c htc
  exact hs.symm.trans ht

/-- Given one globally compatible local family, build a single quotient gauge by
choosing, independently at every coordinate, one route state whose footprint
contains that coordinate.  Outside the union of all route footprints, use the
identity gauge. -/
noncomputable def globalQuotientGaugeOfLocalFamily
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (Qlocal :
      ∀ s : ThreeQuotientRouteState W,
        GeneratedQuotientGaugeParameters W R D) :
    GeneratedQuotientGaugeParameters W R D := by
  classical
  exact
    { mapIdGauge := fun X =>
        dite
          (∃ s : ThreeQuotientRouteState W,
            RouteFootprintContains W s (.identity X))
          (fun h =>
            (Qlocal (Classical.choose h)).mapIdGauge X)
          (fun _ => Iso.refl _)
      mapCompGauge := fun f g =>
        dite
          (∃ s : ThreeQuotientRouteState W,
            RouteFootprintContains W s (.composition f g))
          (fun h =>
            (Qlocal (Classical.choose h)).mapCompGauge f g)
          (fun _ => Iso.refl _) }

/-- The globally patched gauge agrees with the selected local family at every
coordinate of every route footprint. -/
theorem globalQuotientGaugeOfLocalFamily_value_eq
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (Qlocal :
      ∀ s : ThreeQuotientRouteState W,
        GeneratedQuotientGaugeParameters W R D)
    (hPair :
      ∀ s t : ThreeQuotientRouteState W,
        AgreeOnRouteFootprintOverlap W R D s t (Qlocal s) (Qlocal t))
    (s : ThreeQuotientRouteState W)
    (c : QuotientGaugeCoordinate W)
    (hc : RouteFootprintContains W s c) :
    quotientGaugeCoordinateValue W R D
        (globalQuotientGaugeOfLocalFamily W R D Qlocal) c =
      quotientGaugeCoordinateValue W R D (Qlocal s) c := by
  classical
  cases c with
  | identity X =>
      have hex :
          ∃ r : ThreeQuotientRouteState W,
            RouteFootprintContains W r (.identity X) :=
        ⟨s, hc⟩
      have hchosen :
          RouteFootprintContains W (Classical.choose hex) (.identity X) :=
        Classical.choose_spec hex
      rw [quotientGaugeCoordinateValue]
      simp only [globalQuotientGaugeOfLocalFamily]
      rw [dif_pos hex]
      exact
        hPair (Classical.choose hex) s (.identity X) hchosen hc
  | composition f g =>
      have hex :
          ∃ r : ThreeQuotientRouteState W,
            RouteFootprintContains W r (.composition f g) :=
        ⟨s, hc⟩
      have hchosen :
          RouteFootprintContains W
            (Classical.choose hex) (.composition f g) :=
        Classical.choose_spec hex
      rw [quotientGaugeCoordinateValue]
      simp only [globalQuotientGaugeOfLocalFamily]
      rw [dif_pos hex]
      exact
        hPair (Classical.choose hex) s (.composition f g) hchosen hc

/-- The global coordinate patch agrees with each local gauge on its full v3.12
route footprint. -/
theorem globalQuotientGaugeOfLocalFamily_agreesOnRouteState
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (Qlocal :
      ∀ s : ThreeQuotientRouteState W,
        GeneratedQuotientGaugeParameters W R D)
    (hPair :
      ∀ s t : ThreeQuotientRouteState W,
        AgreeOnRouteFootprintOverlap W R D s t (Qlocal s) (Qlocal t))
    (s : ThreeQuotientRouteState W) :
    QuotientGaugesAgreeOnRouteState W R D
      (globalQuotientGaugeOfLocalFamily W R D Qlocal) (Qlocal s) s := by
  apply quotientGaugesAgreeOnRouteState_of_coordinateValue_eq
    W R D
  intro c hc
  exact globalQuotientGaugeOfLocalFamily_value_eq
    W R D Qlocal hPair s c hc

/-- One globally pairwise-compatible correcting local family glues to one
finite-footprint amalgamating quotient gauge. -/
theorem hasFiniteFootprintAmalgamation_of_globalFamily
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (H : HasGloballyCompatibleLocalCorrectionFamily W R D) :
    HasFiniteFootprintAmalgamation W R D := by
  rcases H with ⟨Qlocal, hCorrect, hPair⟩
  refine
    ⟨globalQuotientGaugeOfLocalFamily W R D Qlocal, ?_⟩
  intro s
  exact
    ⟨Qlocal s, hCorrect s,
      globalQuotientGaugeOfLocalFamily_agreesOnRouteState
        W R D Qlocal hPair s⟩

/-- Global finite-footprint amalgamation is exactly equivalent to existence of
one globally chosen pairwise-compatible family of local correcting gauges. -/
theorem hasFiniteFootprintAmalgamation_iff_globalFamily
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R) :
    HasFiniteFootprintAmalgamation W R D ↔
      HasGloballyCompatibleLocalCorrectionFamily W R D := by
  constructor
  · exact
      hasGloballyCompatibleLocalCorrectionFamily_of_finiteFootprintAmalgamation
        W R D
  · exact hasFiniteFootprintAmalgamation_of_globalFamily W R D

/-- The remaining post-v3.15 gap: nested pairwise-compatible local witnesses
exist, but they cannot be correlated into one globally chosen compatible local
family.  Existence of such a gap is not asserted here. -/
def PairwiseWitnessCorrelationGap
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R) : Prop :=
  HasPairwiseSharedCoordinateCompatibleLocalCorrections W R D ∧
    ¬ HasGloballyCompatibleLocalCorrectionFamily W R D

/-- Shared-coordinate pairwise local compatibility already implies ordinary
statewise reachability. -/
theorem individuallyReachable_of_pairwiseSharedCoordinates
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (H : HasPairwiseSharedCoordinateCompatibleLocalCorrections W R D) :
    AllThreeQuotientRoutesIndividuallyReachable W R D := by
  rw [allThreeQuotientRoutesIndividuallyReachable_iff_loci_nonempty W R D]
  intro s
  rcases H s with ⟨Qs, hQs, _⟩
  exact ⟨Qs, hQs⟩

/-- The v3.13 pairwise-compatible-but-nonglobal obstruction is exactly the
correlation gap between nested pairwise witnesses and one globally compatible
local family. -/
theorem pairwiseCompatibleButNoGlobalAmalgamation_iff_correlationGap
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R) :
    PairwiseCompatibleButNoGlobalAmalgamation W R D ↔
      PairwiseWitnessCorrelationGap W R D := by
  constructor
  · rintro ⟨_, hPairwise, hNoGlobal⟩
    have hShared :
        HasPairwiseSharedCoordinateCompatibleLocalCorrections W R D :=
      (hasPairwiseOverlapCompatibleLocalCorrections_iff_sharedCoordinates
        W R D).1 hPairwise
    refine ⟨hShared, ?_⟩
    intro hFamily
    exact hNoGlobal
      ((hasFiniteFootprintAmalgamation_iff_globalFamily W R D).2 hFamily)
  · rintro ⟨hShared, hNoFamily⟩
    have hPoint :=
      individuallyReachable_of_pairwiseSharedCoordinates W R D hShared
    have hPairwise :
        HasPairwiseOverlapCompatibleLocalCorrections W R D :=
      (hasPairwiseOverlapCompatibleLocalCorrections_iff_sharedCoordinates
        W R D).2 hShared
    refine ⟨hPoint, hPairwise, ?_⟩
    intro hGlobal
    exact hNoFamily
      ((hasFiniteFootprintAmalgamation_iff_globalFamily W R D).1 hGlobal)

/-!
## Factorization frontier after v3.16

The actual quotient-gauge space now has two gluing theorems:

```text
v3.15:
  shared coordinates for one pair
    <-> one common pair extension

v3.16:
  one globally chosen pairwise-compatible local family
    <-> one global finite-footprint amalgamation.
```

Therefore no additional geometric obstruction lives inside coordinatewise
patching itself.

The only possible gap between the current v3.13 pairwise predicate and global
amalgamation is now the witness-correlation quantifier gap:

```text
∀ s, ∃ Q_s, ∀ t, ∃ Q_t, pairwise-compatible
        versus
∃ Qlocal, ∀ s t, Qlocal s and Qlocal t are pairwise-compatible.
```

This is the next theorem-sized problem.  One should either:

1. derive one globally correlated local family from the generated localization
   route structure; or
2. construct a genuine counterexample showing that the nested pairwise
   quantifiers do not suffice.

Only that issue remains before the quotient-stage global amalgamation theorem.
-/

end KUOS.DependentOriginationGlobalFootprintGluingV3_16
