import KUOS.DependentOriginationSharedCoordinateRigidityV3_18

namespace KUOS.DependentOriginationSharedCoordinateNormalizerV3_19

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
open KUOS.DependentOriginationSharedCoordinateRigidityV3_18

universe u v uH vH

/-!
# Shared-coordinate gauge-fixing normalizer v3.19

v3.18 gives a clean sufficient criterion for closing the v3.17 witness-
correlation gap: each correction locus is rigid on coordinates shared with
other route footprints.

The concrete quotient defect equations show why literal rigidity may be too
strong.  A left- or right-unitor equation relates a composition gauge to an
identity gauge, while an associator equation relates four composition gauges.
A correction locus can therefore retain internal gauge freedom even when its
essential overlap data admit a canonical representative.

This file weakens v3.18 from uniqueness of every correcting witness to
uniqueness **after gauge fixing**.

A shared-coordinate gauge-fixing normalizer supplies, for every route state,
a normalization operation on quotient gauges such that:

* correcting gauges remain correcting after normalization;
* pairwise overlap agreement is preserved by normalization;
* normalized correcting gauges for the same route state are rigid on shared
  coordinates.

Under these three conditions, the nested pairwise witnesses of v3.14 correlate
into one globally compatible local family, and hence by v3.16 into one global
finite-footprint amalgamation.

Literal v3.18 rigidity is recovered as the special case where normalization is
the identity.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- A routewise gauge-fixing operation whose normalized correction loci are
rigid on shared coordinates and which respects already compatible overlaps. -/
structure SharedCoordinateGaugeFixingNormalizer
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R) where
  normalize :
    ThreeQuotientRouteState W →
      GeneratedQuotientGaugeParameters W R D →
        GeneratedQuotientGaugeParameters W R D
  preservesCorrection :
    ∀ s : ThreeQuotientRouteState W,
      ∀ Q : GeneratedQuotientGaugeParameters W R D,
        Q ∈ quotientRouteCorrectionLocus W R D s →
          normalize s Q ∈ quotientRouteCorrectionLocus W R D s
  preservesOverlap :
    ∀ s t : ThreeQuotientRouteState W,
      ∀ Qs Qt : GeneratedQuotientGaugeParameters W R D,
        Qs ∈ quotientRouteCorrectionLocus W R D s →
        Qt ∈ quotientRouteCorrectionLocus W R D t →
        AgreeOnRouteFootprintOverlap W R D s t Qs Qt →
          AgreeOnRouteFootprintOverlap W R D s t
            (normalize s Qs) (normalize t Qt)
  normalizedSharedRigid :
    ∀ s : ThreeQuotientRouteState W,
      ∀ Q Q' : GeneratedQuotientGaugeParameters W R D,
        Q ∈ quotientRouteCorrectionLocus W R D s →
        Q' ∈ quotientRouteCorrectionLocus W R D s →
        ∀ t : ThreeQuotientRouteState W,
          ∀ c : QuotientGaugeCoordinate W,
            RouteFootprintContains W s c →
            RouteFootprintContains W t c →
              quotientGaugeCoordinateValue W R D (normalize s Q) c =
                quotientGaugeCoordinateValue W R D (normalize s Q') c

/-- A shared-coordinate gauge-fixing normalizer correlates the nested pairwise
local correction witnesses into one globally compatible normalized family. -/
theorem hasGloballyCompatibleLocalCorrectionFamily_of_pairwiseShared_of_normalizer
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (hPair :
      HasPairwiseSharedCoordinateCompatibleLocalCorrections W R D)
    (N : SharedCoordinateGaugeFixingNormalizer W R D) :
    HasGloballyCompatibleLocalCorrectionFamily W R D := by
  classical
  let Qraw :
      ∀ s : ThreeQuotientRouteState W,
        GeneratedQuotientGaugeParameters W R D :=
    fun s => Classical.choose (hPair s)
  let Qlocal :
      ∀ s : ThreeQuotientRouteState W,
        GeneratedQuotientGaugeParameters W R D :=
    fun s => N.normalize s (Qraw s)
  have hRawCorrect :
      ∀ s : ThreeQuotientRouteState W,
        Qraw s ∈ quotientRouteCorrectionLocus W R D s := by
    intro s
    exact (Classical.choose_spec (hPair s)).1
  have hLocalCorrect :
      ∀ s : ThreeQuotientRouteState W,
        Qlocal s ∈ quotientRouteCorrectionLocus W R D s := by
    intro s
    exact N.preservesCorrection s (Qraw s) (hRawCorrect s)
  refine ⟨Qlocal, hLocalCorrect, ?_⟩
  intro s t c hsc htc
  have hst :=
    (Classical.choose_spec (hPair s)).2 t
  let QtFromS : GeneratedQuotientGaugeParameters W R D :=
    Classical.choose hst
  have hQtFromSCorrect :
      QtFromS ∈ quotientRouteCorrectionLocus W R D t := by
    exact (Classical.choose_spec hst).1
  have hRawOverlap :
      AgreeOnRouteFootprintOverlap W R D s t (Qraw s) QtFromS := by
    exact (Classical.choose_spec hst).2
  have hNormalizedOverlap :
      AgreeOnRouteFootprintOverlap W R D s t
        (N.normalize s (Qraw s)) (N.normalize t QtFromS) :=
    N.preservesOverlap s t (Qraw s) QtFromS
      (hRawCorrect s) hQtFromSCorrect hRawOverlap
  have hAnchor :
      quotientGaugeCoordinateValue W R D (Qlocal s) c =
        quotientGaugeCoordinateValue W R D (N.normalize t QtFromS) c := by
    exact hNormalizedOverlap c hsc htc
  have hNormalFormAtT :
      quotientGaugeCoordinateValue W R D (N.normalize t QtFromS) c =
        quotientGaugeCoordinateValue W R D (Qlocal t) c := by
    exact
      N.normalizedSharedRigid t QtFromS (Qraw t)
        hQtFromSCorrect (hRawCorrect t) s c htc hsc
  exact hAnchor.trans hNormalFormAtT

/-- Therefore a gauge-fixing normalizer is sufficient to close the finite
footprint amalgamation problem from nested pairwise local compatibility. -/
theorem hasFiniteFootprintAmalgamation_of_pairwiseShared_of_normalizer
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (hPair :
      HasPairwiseSharedCoordinateCompatibleLocalCorrections W R D)
    (N : SharedCoordinateGaugeFixingNormalizer W R D) :
    HasFiniteFootprintAmalgamation W R D := by
  exact
    hasFiniteFootprintAmalgamation_of_globalFamily W R D
      (hasGloballyCompatibleLocalCorrectionFamily_of_pairwiseShared_of_normalizer
        W R D hPair N)

/-- Consequently existence of a shared-coordinate normalizer rules out the
v3.16 witness-correlation gap. -/
theorem not_pairwiseWitnessCorrelationGap_of_normalizer
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (N : SharedCoordinateGaugeFixingNormalizer W R D) :
    ¬ PairwiseWitnessCorrelationGap W R D := by
  rintro ⟨hPair, hNoGlobal⟩
  exact hNoGlobal
    (hasGloballyCompatibleLocalCorrectionFamily_of_pairwiseShared_of_normalizer
      W R D hPair N)

/-- Literal shared-coordinate rigidity from v3.18 gives the identity
gauge-fixing normalizer.  Thus v3.19 strictly generalizes the shape of the
previous sufficient criterion: normalization may now remove internal gauge
freedom before uniqueness is required. -/
def identitySharedCoordinateGaugeFixingNormalizer_of_rigid
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (hRigid : SharedCoordinateRigidCorrectionLoci W R D) :
    SharedCoordinateGaugeFixingNormalizer W R D where
  normalize := fun _ Q => Q
  preservesCorrection := by
    intro s Q hQ
    exact hQ
  preservesOverlap := by
    intro s t Qs Qt _ _ hOverlap
    exact hOverlap
  normalizedSharedRigid := by
    intro s Q Q' hQ hQ' t c hsc htc
    exact hRigid s Q Q' hQ hQ' t c hsc htc

/-- v3.18's global-family theorem is recovered through the identity normalizer. -/
theorem hasGloballyCompatibleLocalCorrectionFamily_of_pairwiseShared_of_rigid_via_normalizer
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (hPair :
      HasPairwiseSharedCoordinateCompatibleLocalCorrections W R D)
    (hRigid : SharedCoordinateRigidCorrectionLoci W R D) :
    HasGloballyCompatibleLocalCorrectionFamily W R D := by
  exact
    hasGloballyCompatibleLocalCorrectionFamily_of_pairwiseShared_of_normalizer
      W R D hPair
      (identitySharedCoordinateGaugeFixingNormalizer_of_rigid
        W R D hRigid)

/-!
## Factorization frontier after v3.19

The post-v3.17 correlation problem now admits two nested sufficient criteria:

```text
literal shared-coordinate rigidity                 (v3.18)
        |
        v
shared-coordinate gauge-fixing normalizer          (v3.19)
        |
        v
globally compatible local correction family        (v3.16)
        |
        v
finite-footprint amalgamation
        |
        v
coherent quotient transport.
```

v3.19 is better adapted to the actual quotient defect equations because it
allows nonessential gauge freedom inside each correction locus.  What must be
canonical is only the normalized shared-coordinate data.

The next route-specific task is therefore precise: construct such a normalizer
from the concrete associator and unitor correction equations, or exhibit an
actual residual cycle showing that no overlap-preserving normalization can
exist without an additional hypothesis.
-/

end KUOS.DependentOriginationSharedCoordinateNormalizerV3_19
