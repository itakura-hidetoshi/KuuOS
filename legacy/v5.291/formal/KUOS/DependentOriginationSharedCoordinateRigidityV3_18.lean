import KUOS.DependentOriginationPairwiseCorrelationCountermodelV3_17

namespace KUOS.DependentOriginationSharedCoordinateRigidityV3_18

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationQuotientGaugeIndependenceV3_03
open KUOS.DependentOriginationThreeRouteCorrectionCompatibilityGapV3_09
open KUOS.DependentOriginationQuotientGaugeIntersectionObstructionV3_11
open KUOS.DependentOriginationQuotientGaugeCoordinateFootprintV3_12
open KUOS.DependentOriginationQuotientGaugeFootprintOverlapV3_13
open KUOS.DependentOriginationQuotientGaugeCoordinateKeyV3_14
open KUOS.DependentOriginationPairwiseFiniteExtensionV3_15
open KUOS.DependentOriginationGlobalFootprintGluingV3_16
open KUOS.DependentOriginationPairwiseCorrelationCountermodelV3_17

universe u v uH vH

set_option linter.unnecessarySimpa false

/-!
# Shared-coordinate rigidity criterion v3.18

v3.17 proves that nested pairwise-compatible correction witnesses do not, by
pure quantifier logic, determine one globally correlated compatible family.

The finite parity countermodel reveals the missing structural ingredient.  For a
fixed route state, different correcting witnesses can carry different values on
coordinates shared with other route states.  Which witness is chosen for that
state may therefore depend on the anchor state.

This file isolates a sufficient condition that removes exactly that freedom.

A correction locus is **shared-coordinate rigid** when any two gauges correcting
the same route state have equal values at every coordinate of that state's
footprint which is also contained in the footprint of any second route state.

Under this condition, the nested v3.14 pairwise witness predicate upgrades to a
single globally compatible local correction family.  By v3.16 that family glues
to one global finite-footprint amalgamation.

Thus

```text
pairwise shared-coordinate compatible local corrections
+ shared-coordinate rigidity of each correction locus
    =>
globally compatible local correction family
    =>
finite-footprint amalgamation.
```

The condition is stronger than local correctability and is not assumed to hold
automatically for the actual generated-localization route equations.  The
v3.17 parity countermodel is proved not to satisfy its abstract analogue, so
the criterion excludes that obstruction for the precise structural reason
identified above.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Within each route-state correction locus, every coordinate shared with a
second route state has a uniquely determined value. -/
def SharedCoordinateRigidCorrectionLoci
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R) : Prop :=
  ∀ s : ThreeQuotientRouteState W,
    ∀ Q Q' : GeneratedQuotientGaugeParameters W R D,
      Q ∈ quotientRouteCorrectionLocus W R D s →
      Q' ∈ quotientRouteCorrectionLocus W R D s →
      ∀ t : ThreeQuotientRouteState W,
        ∀ c : QuotientGaugeCoordinate W,
          RouteFootprintContains W s c →
          RouteFootprintContains W t c →
            quotientGaugeCoordinateValue W R D Q c =
              quotientGaugeCoordinateValue W R D Q' c

/-- Shared-coordinate rigidity turns the nested pairwise witnesses of v3.14
into one globally correlated compatible local family. -/
theorem hasGloballyCompatibleLocalCorrectionFamily_of_pairwiseShared_of_rigid
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (hPair :
      HasPairwiseSharedCoordinateCompatibleLocalCorrections W R D)
    (hRigid : SharedCoordinateRigidCorrectionLoci W R D) :
    HasGloballyCompatibleLocalCorrectionFamily W R D := by
  classical
  let Qlocal :
      ∀ s : ThreeQuotientRouteState W,
        GeneratedQuotientGaugeParameters W R D :=
    fun s => Classical.choose (hPair s)
  have hCorrect :
      ∀ s : ThreeQuotientRouteState W,
        Qlocal s ∈ quotientRouteCorrectionLocus W R D s := by
    intro s
    exact (Classical.choose_spec (hPair s)).1
  refine ⟨Qlocal, hCorrect, ?_⟩
  intro s t c hsc htc
  have hst :=
    (Classical.choose_spec (hPair s)).2 t
  let QtFromS : GeneratedQuotientGaugeParameters W R D :=
    Classical.choose hst
  have hQtFromSCorrect :
      QtFromS ∈ quotientRouteCorrectionLocus W R D t := by
    exact (Classical.choose_spec hst).1
  have hOverlap :
      AgreeOnRouteFootprintOverlap W R D s t (Qlocal s) QtFromS := by
    exact (Classical.choose_spec hst).2
  have hAnchor :
      quotientGaugeCoordinateValue W R D (Qlocal s) c =
        quotientGaugeCoordinateValue W R D QtFromS c :=
    hOverlap c hsc htc
  have hRigidAtT :
      quotientGaugeCoordinateValue W R D QtFromS c =
        quotientGaugeCoordinateValue W R D (Qlocal t) c :=
    hRigid t QtFromS (Qlocal t)
      hQtFromSCorrect (hCorrect t) s c htc hsc
  exact hAnchor.trans hRigidAtT

/-- Consequently pairwise compatible local correction data already yield one
global finite-footprint amalgamation whenever correction loci are rigid on
shared coordinates. -/
theorem hasFiniteFootprintAmalgamation_of_pairwiseShared_of_rigid
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (hPair :
      HasPairwiseSharedCoordinateCompatibleLocalCorrections W R D)
    (hRigid : SharedCoordinateRigidCorrectionLoci W R D) :
    HasFiniteFootprintAmalgamation W R D := by
  exact
    hasFiniteFootprintAmalgamation_of_globalFamily W R D
      (hasGloballyCompatibleLocalCorrectionFamily_of_pairwiseShared_of_rigid
        W R D hPair hRigid)

/-- In particular, shared-coordinate rigidity rules out the v3.16
pairwise-witness correlation gap. -/
theorem not_pairwiseWitnessCorrelationGap_of_rigid
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (hRigid : SharedCoordinateRigidCorrectionLoci W R D) :
    ¬ PairwiseWitnessCorrelationGap W R D := by
  rintro ⟨hPair, hNoGlobal⟩
  exact hNoGlobal
    (hasGloballyCompatibleLocalCorrectionFamily_of_pairwiseShared_of_rigid
      W R D hPair hRigid)

/-- Abstract analogue of shared-coordinate rigidity for the finite v3.17
countermodel. -/
def AbstractSharedCoordinateRigid : Prop :=
  ∀ s : CorrelationState,
    ∀ q q' : CorrelationCoord → Bool,
      LocalCorrected s q →
      LocalCorrected s q' →
      ∀ t : CorrelationState,
        ∀ k : CorrelationCoord,
          footprint s k →
          footprint t k →
            q k = q' k

/-- The v3.17 parity countermodel fails shared-coordinate rigidity already at
state `b`: both the all-zero and all-one sections correct `b`, but they
disagree on coordinate `ab`, which is shared with state `a`. -/
theorem not_abstractSharedCoordinateRigid :
    ¬ AbstractSharedCoordinateRigid := by
  intro hRigid
  have hEq :=
    hRigid .b zeroSection oneSection
      zeroSection_local_b oneSection_local_b
      .a .ab
      (by simp [footprint])
      (by simp [footprint])
  simpa [zeroSection, oneSection] using hEq

/-!
## Factorization frontier after v3.18

v3.17 shows that pairwise witness correlation can fail in general.  v3.18 now
identifies one concrete structural condition that kills exactly that failure:

```text
same route-state correction locus
  -> shared coordinates have unique values.
```

Under this rigidity condition, anchor-dependent pairwise witnesses cannot
disagree on overlaps, so arbitrary statewise choices automatically form one
globally compatible family and hence one finite-footprint amalgamation.

The next question is no longer logical.  It is route-specific:

```text
Do the actual generated quotient correction loci satisfy shared-coordinate
rigidity, or some weaker property sufficient to correlate their witnesses?
```

Because each associator or unitor equation constrains several gauge coordinates
at once, full rigidity should not be assumed without proof.  The next theorem
unit should inspect the concrete quotient defect equations and test this
criterion coordinate by coordinate, weakening it if the actual gauge freedom
shows that uniqueness is too strong.
-/

end KUOS.DependentOriginationSharedCoordinateRigidityV3_18
