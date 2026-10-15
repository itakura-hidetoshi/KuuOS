import Mathlib
import KUOS.PlanOS.ConjugateEventSequenceInjectivityRadiusV1_11

namespace KUOS.PlanOS.ExponentialMapNormalCoordinateBallV1_12

structure ExponentialMapNormalCoordinateBallCertificate where
  finiteSecondOrderExponentialModelRecomputed : Bool
  normalBallStrictlyInsideInjectivityBound : Bool
  radialGeodesicUniqueFromBasepoint : Bool
  finiteSampleExponentialMapInjective : Bool
  normalCoordinateCandidatesRetained : Bool
  chartSafeGeodesicBallCovering : Bool
  chartBoundariesRespected : Bool
  atlasTransitionAuthorityNotExtended : Bool
  localModelOnly : Bool
  globalExponentialMapNotClaimed : Bool
  strongConvexityNotClaimed : Bool
  pairwiseEndpointGeodesicUniquenessNotClaimed : Bool
  candidateIdentityRetained : Bool
  sourceInjectivityCertificateNotMutated : Bool
  sourceAtlasCertificateNotMutated : Bool
  persistentWorldStateUnchanged : Bool
  decisionSelectionPerformed : Bool
  historyReadOnly : Bool
  exponentialMapGrantsNoAuthority : Bool
  normalBallGrantsNoAuthority : Bool
  chartCoverGrantsNoAuthority : Bool
  futureOnly : Bool
  activeNow : Bool
  executionPermission : Bool

/-- Finite-coordinate metric norm squared at the normal-coordinate base point. -/
def metricNormSquared {n : ℕ}
    (metric : Fin n → Fin n → ℝ)
    (vector : Fin n → ℝ) : ℝ :=
  ∑ i, ∑ j, metric i j * vector i * vector j

/-- Second-order local exponential-map model at one base point. -/
def secondOrderExp {n : ℕ}
    (base tangent : Fin n → ℝ)
    (christoffel : Fin n → Fin n → Fin n → ℝ) : Fin n → ℝ :=
  fun i =>
    base i + tangent i -
      (1 / 2 : ℝ) *
        ∑ j, ∑ k, christoffel i j k * tangent j * tangent k

/-- Radial second-order local model at parameter `t`. -/
def secondOrderRadialPoint {n : ℕ}
    (base tangent : Fin n → ℝ)
    (christoffel : Fin n → Fin n → Fin n → ℝ)
    (t : ℝ) : Fin n → ℝ :=
  fun i =>
    base i + t * tangent i -
      (1 / 2 : ℝ) * t ^ 2 *
        ∑ j, ∑ k, christoffel i j k * tangent j * tangent k

/-- The normal-coordinate radius is positive and strictly below the retained injectivity bound. -/
def WithinInjectivityBound
    (normalRadius injectivityRadius : ℝ) : Prop :=
  0 < normalRadius ∧ normalRadius < injectivityRadius

/-- A finite set of retained exponential samples is injective. -/
def FiniteSampleInjective {α β : Type}
    (sampleMap : α → β) : Prop :=
  Function.Injective sampleMap

/-- A retained point is covered by at least one chart-safe predicate. -/
def CoveredByChart {α β : Type}
    (chartSafe : α → β → Prop)
    (point : β) : Prop :=
  ∃ chart, chartSafe chart point

@[simp] theorem metricNormSquared_zero {n : ℕ}
    (metric : Fin n → Fin n → ℝ) :
    metricNormSquared metric (fun _ => 0) = 0 := by
  simp [metricNormSquared]

@[simp] theorem secondOrderExp_zero_tangent {n : ℕ}
    (base : Fin n → ℝ)
    (christoffel : Fin n → Fin n → Fin n → ℝ) :
    secondOrderExp base (fun _ => 0) christoffel = base := by
  funext i
  simp [secondOrderExp]

@[simp] theorem secondOrderExp_zero_connection {n : ℕ}
    (base tangent : Fin n → ℝ) :
    secondOrderExp base tangent (fun _ _ _ => 0) =
      fun i => base i + tangent i := by
  funext i
  simp [secondOrderExp]

@[simp] theorem secondOrderRadialPoint_zero {n : ℕ}
    (base tangent : Fin n → ℝ)
    (christoffel : Fin n → Fin n → Fin n → ℝ) :
    secondOrderRadialPoint base tangent christoffel 0 = base := by
  funext i
  simp [secondOrderRadialPoint]

@[simp] theorem secondOrderRadialPoint_one {n : ℕ}
    (base tangent : Fin n → ℝ)
    (christoffel : Fin n → Fin n → Fin n → ℝ) :
    secondOrderRadialPoint base tangent christoffel 1 =
      secondOrderExp base tangent christoffel := by
  funext i
  simp [secondOrderRadialPoint, secondOrderExp]

/-- A strict normal-ball witness gives a positive injectivity-radius bound. -/
theorem injectivityRadius_positive_of_within_bound
    {normalRadius injectivityRadius : ℝ}
    (hbound : WithinInjectivityBound normalRadius injectivityRadius) :
    0 < injectivityRadius := by
  exact lt_trans hbound.1 hbound.2

/-- Shrinking a positive normal ball preserves inclusion in the injectivity bound. -/
theorem withinInjectivityBound_mono
    {smaller larger injectivityRadius : ℝ}
    (hsmaller : 0 < smaller)
    (horder : smaller ≤ larger)
    (hlarger : WithinInjectivityBound larger injectivityRadius) :
    WithinInjectivityBound smaller injectivityRadius := by
  exact ⟨hsmaller, lt_of_le_of_lt horder hlarger.2⟩

/-- Finite-sample injectivity turns equal endpoints into equal retained tangents. -/
theorem equal_tangents_of_equal_finite_exp_samples
    {α β : Type}
    (sampleMap : α → β)
    (hinjective : FiniteSampleInjective sampleMap)
    {left right : α}
    (hequal : sampleMap left = sampleMap right) :
    left = right := by
  exact hinjective hequal

/-- An explicit chart witness proves finite chart coverage. -/
theorem coveredByChart_of_witness
    {α β : Type}
    (chartSafe : α → β → Prop)
    (chart : α)
    (point : β)
    (hsafe : chartSafe chart point) :
    CoveredByChart chartSafe point := by
  exact ⟨chart, hsafe⟩

/-- Local exponential, normal-ball, and chart-cover evidence grants no authority. -/
theorem local_exponential_geometry_grants_no_authority
    (certificate : ExponentialMapNormalCoordinateBallCertificate)
    (hexp : certificate.exponentialMapGrantsNoAuthority = true)
    (hball : certificate.normalBallGrantsNoAuthority = true)
    (hchart : certificate.chartCoverGrantsNoAuthority = true)
    (hselection : certificate.decisionSelectionPerformed = false)
    (hexecution : certificate.executionPermission = false) :
    certificate.exponentialMapGrantsNoAuthority = true ∧
      certificate.normalBallGrantsNoAuthority = true ∧
      certificate.chartCoverGrantsNoAuthority = true ∧
      certificate.decisionSelectionPerformed = false ∧
      certificate.executionPermission = false := by
  exact ⟨hexp, hball, hchart, hselection, hexecution⟩

/-- The v1.12 certificate remains local, read-only, future-only, and inactive. -/
theorem exponential_map_certificate_is_local_future_only
    (certificate : ExponentialMapNormalCoordinateBallCertificate)
    (hlocal : certificate.localModelOnly = true)
    (hglobal : certificate.globalExponentialMapNotClaimed = true)
    (hreadonly : certificate.historyReadOnly = true)
    (hfuture : certificate.futureOnly = true)
    (hactive : certificate.activeNow = false)
    (hexecution : certificate.executionPermission = false) :
    certificate.localModelOnly = true ∧
      certificate.globalExponentialMapNotClaimed = true ∧
      certificate.historyReadOnly = true ∧
      certificate.futureOnly = true ∧
      certificate.activeNow = false ∧
      certificate.executionPermission = false := by
  exact ⟨hlocal, hglobal, hreadonly, hfuture, hactive, hexecution⟩

end KUOS.PlanOS.ExponentialMapNormalCoordinateBallV1_12
