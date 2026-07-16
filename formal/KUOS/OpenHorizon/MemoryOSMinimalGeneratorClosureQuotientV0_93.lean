import Mathlib
import KUOS.OpenHorizon.MemoryOSFiniteBatchContextSaturationV0_92

namespace KUOS.OpenHorizon.MemoryOSMinimalGeneratorClosureQuotientV0_93

open KUOS.OpenHorizon.MemoryOSNonAbelianWilsonLoopV0_72
open KUOS.OpenHorizon.MemoryOSRootedRouteAtlasNielsenChangeV0_78
open KUOS.OpenHorizon.MemoryOSAllRootChartDefectAwareWordTransportV0_80
open KUOS.OpenHorizon.MemoryOSNormalizedRootWordGroupoidDescentV0_81
open KUOS.OpenHorizon.MemoryOSGlobalWordCechDescentV0_82
open KUOS.OpenHorizon.MemoryOSGlobalSectionGroupAnchorCoherenceV0_83
open KUOS.OpenHorizon.MemoryOSGlobalObservableKernelQuotientV0_84
open KUOS.OpenHorizon.MemoryOSObservableSensorCoarseningV0_85
open KUOS.OpenHorizon.MemoryOSJointSensorProductRefinementV0_86
open KUOS.OpenHorizon.MemoryOSFiniteSensorFamilyRefinementV0_87
open KUOS.OpenHorizon.MemoryOSExactSensorCoreV0_88
open KUOS.OpenHorizon.MemoryOSSensorSupportClosureV0_89
open KUOS.OpenHorizon.MemoryOSFullClosedSupportRepresentationV0_90
open KUOS.OpenHorizon.MemoryOSCounterexampleGuidedContextRefinementV0_91
open KUOS.OpenHorizon.MemoryOSFiniteBatchContextSaturationV0_92

/-- Two finite supports are closure-equivalent when they generate the same exact
sensor-support closure. -/
def ClosureEquivalent
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (left right : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) : Prop :=
  sensorSupportClosure sensors left atlas targetDefect root =
    sensorSupportClosure sensors right atlas targetDefect root

/-- A support is an inclusion-minimal generator of its closure class when no
strictly smaller sub-support generates the same closure. -/
def ClosureMinimalGenerator
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (support : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) : Prop :=
  ∀ candidate : Finset ι,
    candidate ⊆ support →
    ClosureEquivalent sensors candidate support atlas targetDefect root →
    candidate = support

theorem closure_equivalent_refl
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (support : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    ClosureEquivalent sensors support support atlas targetDefect root := by
  rfl

theorem closure_equivalent_symm
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (left right : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel)
    (h : ClosureEquivalent sensors left right atlas targetDefect root) :
    ClosureEquivalent sensors right left atlas targetDefect root := by
  exact h.symm

theorem closure_equivalent_trans
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (left middle right : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel)
    (hlm : ClosureEquivalent sensors left middle atlas targetDefect root)
    (hmr : ClosureEquivalent sensors middle right atlas targetDefect root) :
    ClosureEquivalent sensors left right atlas targetDefect root := by
  exact hlm.trans hmr

/-- Closure equivalence is exactly equality of finite invisible kernels. -/
theorem closure_equivalent_iff_kernel_eq
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (left right : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    ClosureEquivalent sensors left right atlas targetDefect root ↔
      finiteSensorSupportKernel sensors left atlas targetDefect root =
        finiteSensorSupportKernel sensors right atlas targetDefect root := by
  exact (finite_sensor_support_kernel_eq_iff_closure_eq sensors left right
    atlas targetDefect root).symm

/-- Every finite support contains an inclusion-minimal representative of the
same closure class. -/
theorem exists_closure_minimal_generator_below
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (support : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    ∃ generator : Finset ι,
      generator ⊆ support ∧
      ClosureEquivalent sensors generator support atlas targetDefect root ∧
      ClosureMinimalGenerator sensors generator atlas targetDefect root := by
  classical
  refine Finset.strongInductionOn support ?_
  intro current ih
  by_cases hminimal :
      ClosureMinimalGenerator sensors current atlas targetDefect root
  · exact ⟨current, Finset.Subset.rfl, rfl, hminimal⟩
  · simp only [ClosureMinimalGenerator] at hminimal
    push_neg at hminimal
    obtain ⟨candidate, hsubset, hclosure, hne⟩ := hminimal
    have hstrict : candidate ⊂ current :=
      Finset.ssubset_iff_subset_ne.mpr ⟨hsubset, hne⟩
    obtain ⟨generator, hgsubset, hgeq, hgminimal⟩ := ih candidate hstrict
    exact ⟨generator, hgsubset.trans hsubset, hgeq.trans hclosure, hgminimal⟩

/-- Every closure class therefore has an exact-kernel minimal representative
below each chosen support. -/
theorem exists_exact_kernel_minimal_generator_below
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (support : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    ∃ generator : Finset ι,
      generator ⊆ support ∧
      finiteSensorSupportKernel sensors generator atlas targetDefect root =
        finiteSensorSupportKernel sensors support atlas targetDefect root ∧
      ClosureMinimalGenerator sensors generator atlas targetDefect root := by
  obtain ⟨generator, hsubset, hclosure, hminimal⟩ :=
    exists_closure_minimal_generator_below sensors support atlas targetDefect root
  exact ⟨generator, hsubset,
    (closure_equivalent_iff_kernel_eq sensors generator support
      atlas targetDefect root).mp hclosure,
    hminimal⟩

/-- All inclusion-minimal generators whose closure is proper. -/
noncomputable def properClosureMinimalGenerators
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) : Finset (Finset ι) := by
  classical
  exact Finset.univ.filter fun generator =>
    ClosureMinimalGenerator sensors generator atlas targetDefect root ∧
      sensorSupportClosure sensors generator atlas targetDefect root ≠ Finset.univ

theorem mem_proper_closure_minimal_generators_iff
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (generator : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    generator ∈ properClosureMinimalGenerators sensors atlas targetDefect root ↔
      ClosureMinimalGenerator sensors generator atlas targetDefect root ∧
        sensorSupportClosure sensors generator atlas targetDefect root ≠
          Finset.univ := by
  classical
  simp [properClosureMinimalGenerators]

/-- Every proper closed context is generated by at least one inclusion-minimal
sub-support. Uniqueness is intentionally not asserted. -/
theorem exists_minimal_generator_for_proper_closed_context
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (context : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel)
    (hclosed : SensorSupportClosed sensors context atlas targetDefect root)
    (hproper : context ≠ Finset.univ) :
    ∃ generator ∈ properClosureMinimalGenerators sensors atlas targetDefect root,
      generator ⊆ context ∧
        sensorSupportClosure sensors generator atlas targetDefect root = context := by
  obtain ⟨generator, hsubset, hclosure, hminimal⟩ :=
    exists_closure_minimal_generator_below sensors context atlas targetDefect root
  have hgeneratorClosure :
      sensorSupportClosure sensors generator atlas targetDefect root = context :=
    hclosure.trans hclosed
  refine ⟨generator, ?_, hsubset, hgeneratorClosure⟩
  rw [mem_proper_closure_minimal_generators_iff]
  exact ⟨hminimal, by
    rw [hgeneratorClosure]
    exact hproper⟩

/-- The proper closure image of all minimal generators is exactly the full
proper closed-context family. -/
theorem canonical_minimal_generator_contexts_eq_proper_closed
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    canonicalProperClosureContexts sensors
        (properClosureMinimalGenerators sensors atlas targetDefect root)
        atlas targetDefect root =
      properClosedSensorSupports sensors atlas targetDefect root := by
  classical
  apply Finset.ext
  intro context
  rw [mem_canonical_proper_closure_contexts_iff,
    mem_proper_closed_sensor_supports_iff]
  constructor
  · rintro ⟨⟨generator, hgenerator, hclosure⟩, hproper⟩
    subst context
    exact ⟨sensor_support_closure_closed sensors generator
      atlas targetDefect root, hproper⟩
  · rintro ⟨hclosed, hproper⟩
    obtain ⟨generator, hgenerator, _, hclosure⟩ :=
      exists_minimal_generator_for_proper_closed_context sensors context
        atlas targetDefect root hclosed hproper
    exact ⟨⟨generator, hgenerator, hclosure⟩, hproper⟩

/-- Refining by minimal generators alone recovers the same complete proper
context family as refining by all finite supports. -/
theorem minimal_generator_batch_saturation_eq_proper_closed
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    batchRefineClosedContexts sensors ∅
        (properClosureMinimalGenerators sensors atlas targetDefect root)
        atlas targetDefect root =
      properClosedSensorSupports sensors atlas targetDefect root := by
  classical
  unfold batchRefineClosedContexts
  rw [canonical_minimal_generator_contexts_eq_proper_closed]
  simp

theorem minimal_generator_and_all_support_saturation_eq
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    batchRefineClosedContexts sensors ∅
        (properClosureMinimalGenerators sensors atlas targetDefect root)
        atlas targetDefect root =
      batchRefineClosedContexts sensors ∅ Finset.univ
        atlas targetDefect root := by
  rw [minimal_generator_batch_saturation_eq_proper_closed,
    batch_refine_all_supports_eq_proper_closed]

/-- Minimal-generator saturation remains complete for every singleton query. -/
theorem minimal_generator_saturated_singleton_consequence_complete
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (premise : Finset ι) (i : ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    i ∈ sensorSupportClosure sensors premise atlas targetDefect root ↔
      supportTruthRegion
          (batchRefineClosedContexts sensors ∅
            (properClosureMinimalGenerators sensors atlas targetDefect root)
            atlas targetDefect root)
          premise ⊆
        sensorTruthRegion
          (batchRefineClosedContexts sensors ∅
            (properClosureMinimalGenerators sensors atlas targetDefect root)
            atlas targetDefect root)
          i := by
  rw [minimal_generator_batch_saturation_eq_proper_closed]
  exact mem_sensor_support_closure_iff_proper_truth_region_subset
    sensors premise i atlas targetDefect root

/-- Minimal-generator saturation is also complete for finite conclusions. -/
theorem minimal_generator_saturated_finite_support_consequence_complete
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (premise target : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    target ⊆ sensorSupportClosure sensors premise atlas targetDefect root ↔
      supportTruthRegion
          (batchRefineClosedContexts sensors ∅
            (properClosureMinimalGenerators sensors atlas targetDefect root)
            atlas targetDefect root)
          premise ⊆
        supportTruthRegion
          (batchRefineClosedContexts sensors ∅
            (properClosureMinimalGenerators sensors atlas targetDefect root)
            atlas targetDefect root)
          target := by
  rw [minimal_generator_batch_saturation_eq_proper_closed]
  exact support_subset_closure_iff_proper_truth_region_subset
    sensors premise target atlas targetDefect root

/-- Minimal-generator status is root independent. -/
theorem closure_minimal_generator_root_independent
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (support : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (sourceRoot targetRoot : RouteLabel) :
    ClosureMinimalGenerator sensors support atlas targetDefect sourceRoot ↔
      ClosureMinimalGenerator sensors support atlas targetDefect targetRoot := by
  constructor
  · intro hminimal candidate hsubset hclosure
    apply hminimal candidate hsubset
    calc
      sensorSupportClosure sensors candidate atlas targetDefect sourceRoot =
          sensorSupportClosure sensors candidate atlas targetDefect targetRoot :=
        sensor_support_closure_root_independent sensors candidate atlas targetDefect
          sourceRoot targetRoot
      _ = sensorSupportClosure sensors support atlas targetDefect targetRoot :=
        hclosure
      _ = sensorSupportClosure sensors support atlas targetDefect sourceRoot :=
        (sensor_support_closure_root_independent sensors support atlas targetDefect
          sourceRoot targetRoot).symm
  · intro hminimal candidate hsubset hclosure
    apply hminimal candidate hsubset
    calc
      sensorSupportClosure sensors candidate atlas targetDefect targetRoot =
          sensorSupportClosure sensors candidate atlas targetDefect sourceRoot :=
        (sensor_support_closure_root_independent sensors candidate atlas targetDefect
          sourceRoot targetRoot).symm
      _ = sensorSupportClosure sensors support atlas targetDefect sourceRoot :=
        hclosure
      _ = sensorSupportClosure sensors support atlas targetDefect targetRoot :=
        sensor_support_closure_root_independent sensors support atlas targetDefect
          sourceRoot targetRoot

/-- The complete family of proper minimal generators is root independent. -/
theorem proper_closure_minimal_generators_root_independent
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (sourceRoot targetRoot : RouteLabel) :
    properClosureMinimalGenerators sensors atlas targetDefect sourceRoot =
      properClosureMinimalGenerators sensors atlas targetDefect targetRoot := by
  classical
  apply Finset.ext
  intro generator
  rw [mem_proper_closure_minimal_generators_iff,
    mem_proper_closure_minimal_generators_iff]
  constructor
  · rintro ⟨hminimal, hproper⟩
    refine ⟨(closure_minimal_generator_root_independent sensors generator
      atlas targetDefect sourceRoot targetRoot).mp hminimal, ?_⟩
    intro htop
    apply hproper
    calc
      sensorSupportClosure sensors generator atlas targetDefect sourceRoot =
          sensorSupportClosure sensors generator atlas targetDefect targetRoot :=
        sensor_support_closure_root_independent sensors generator atlas targetDefect
          sourceRoot targetRoot
      _ = Finset.univ := htop
  · rintro ⟨hminimal, hproper⟩
    refine ⟨(closure_minimal_generator_root_independent sensors generator
      atlas targetDefect sourceRoot targetRoot).mpr hminimal, ?_⟩
    intro htop
    apply hproper
    calc
      sensorSupportClosure sensors generator atlas targetDefect targetRoot =
          sensorSupportClosure sensors generator atlas targetDefect sourceRoot :=
        (sensor_support_closure_root_independent sensors generator atlas targetDefect
          sourceRoot targetRoot).symm
      _ = Finset.univ := htop

/-- Finite formal authority boundary of the v0.93 certificate. -/
structure MinimalGeneratorClosureQuotientCertificate where
  sourceMemoryOSV092Bound : Bool
  closureEquivalenceKernelExact : Bool
  everyClosureClassHasMinimalRepresentativeExact : Bool
  properMinimalGeneratorCoverageExact : Bool
  minimalGeneratorSaturationExact : Bool
  allQueryCompletenessPreservedExact : Bool
  rootIndependenceExact : Bool
  uniqueMinimalGeneratorClaimed : Bool
  globalMinimumImplicationBasisClaimed : Bool
  canonicalImplicationBasisClaimed : Bool
  optimalQueryOrderClaimed : Bool
  externalOracleAuthorityGranted : Bool
  candidateRankingPerformed : Bool
  executionPermission : Bool
  persistentWorldStateMutated : Bool
  truthAuthorityGranted : Bool

end KUOS.OpenHorizon.MemoryOSMinimalGeneratorClosureQuotientV0_93
