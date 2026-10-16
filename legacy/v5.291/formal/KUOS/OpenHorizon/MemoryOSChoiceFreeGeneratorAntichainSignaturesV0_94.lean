import Mathlib
import KUOS.OpenHorizon.MemoryOSMinimalGeneratorClosureQuotientV0_93

namespace KUOS.OpenHorizon.MemoryOSChoiceFreeGeneratorAntichainSignaturesV0_94

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
open KUOS.OpenHorizon.MemoryOSMinimalGeneratorClosureQuotientV0_93

/-- The choice-free signature of a context is the complete finite antichain of
all proper inclusion-minimal supports that generate exactly that context. -/
noncomputable def properContextMinimalGeneratorSignature
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (context : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) : Finset (Finset ι) := by
  classical
  exact
    (properClosureMinimalGenerators sensors atlas targetDefect root).filter
      (fun generator =>
        sensorSupportClosure sensors generator atlas targetDefect root = context)

theorem mem_proper_context_minimal_generator_signature_iff
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (context generator : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    generator ∈
        properContextMinimalGeneratorSignature sensors context atlas targetDefect root ↔
      generator ∈ properClosureMinimalGenerators sensors atlas targetDefect root ∧
        sensorSupportClosure sensors generator atlas targetDefect root = context := by
  classical
  simp [properContextMinimalGeneratorSignature]

/-- Every proper closed context has a nonempty choice-free signature. -/
theorem proper_context_minimal_generator_signature_nonempty
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (context : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel)
    (hclosed : SensorSupportClosed sensors context atlas targetDefect root)
    (hproper : context ≠ Finset.univ) :
    (properContextMinimalGeneratorSignature sensors context atlas targetDefect root).Nonempty := by
  obtain ⟨generator, hgenerator, _, hclosure⟩ :=
    exists_minimal_generator_for_proper_closed_context sensors context
      atlas targetDefect root hclosed hproper
  exact ⟨generator,
    (mem_proper_context_minimal_generator_signature_iff sensors context generator
      atlas targetDefect root).2 ⟨hgenerator, hclosure⟩⟩

/-- Every member of a context signature is a sub-support of that context. -/
theorem signature_member_subset_context
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (context generator : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel)
    (hgenerator :
      generator ∈
        properContextMinimalGeneratorSignature sensors context atlas targetDefect root) :
    generator ⊆ context := by
  have hclosure :=
    ((mem_proper_context_minimal_generator_signature_iff sensors context generator
      atlas targetDefect root).1 hgenerator).2
  rw [← hclosure]
  exact sensor_support_subset_closure sensors generator atlas targetDefect root

/-- A choice-free signature is an inclusion antichain: two comparable minimal
generators in the same closure class are equal. -/
theorem proper_context_minimal_generator_signature_antichain
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (context : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    ∀ left ∈
        properContextMinimalGeneratorSignature sensors context atlas targetDefect root,
      ∀ right ∈
        properContextMinimalGeneratorSignature sensors context atlas targetDefect root,
        left ⊆ right → left = right := by
  intro left hleft right hright hsubset
  have hleftData :=
    (mem_proper_context_minimal_generator_signature_iff sensors context left
      atlas targetDefect root).1 hleft
  have hrightData :=
    (mem_proper_context_minimal_generator_signature_iff sensors context right
      atlas targetDefect root).1 hright
  have hrightMinimal :=
    ((mem_proper_closure_minimal_generators_iff sensors right
      atlas targetDefect root).1 hrightData.1).1
  exact hrightMinimal left hsubset (hleftData.2.trans hrightData.2.symm)

/-- A nonempty proper closed-context signature determines its context exactly. -/
theorem proper_context_signature_eq_iff_context_eq
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (left right : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel)
    (hleftClosed : SensorSupportClosed sensors left atlas targetDefect root)
    (hleftProper : left ≠ Finset.univ) :
    properContextMinimalGeneratorSignature sensors left atlas targetDefect root =
        properContextMinimalGeneratorSignature sensors right atlas targetDefect root ↔
      left = right := by
  constructor
  · intro hsignature
    obtain ⟨generator, hgenerator⟩ :=
      proper_context_minimal_generator_signature_nonempty sensors left
        atlas targetDefect root hleftClosed hleftProper
    have hgeneratorRight :
        generator ∈
          properContextMinimalGeneratorSignature sensors right atlas targetDefect root := by
      rw [← hsignature]
      exact hgenerator
    have hleftData :=
      (mem_proper_context_minimal_generator_signature_iff sensors left generator
        atlas targetDefect root).1 hgenerator
    have hrightData :=
      (mem_proper_context_minimal_generator_signature_iff sensors right generator
        atlas targetDefect root).1 hgeneratorRight
    exact hleftData.2.symm.trans hrightData.2
  · intro hcontext
    subst right
    rfl

/-- Shared membership in two signatures forces the represented contexts equal. -/
theorem signature_member_context_unique
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (left right generator : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel)
    (hleft :
      generator ∈
        properContextMinimalGeneratorSignature sensors left atlas targetDefect root)
    (hright :
      generator ∈
        properContextMinimalGeneratorSignature sensors right atlas targetDefect root) :
    left = right := by
  have hleftClosure :=
    ((mem_proper_context_minimal_generator_signature_iff sensors left generator
      atlas targetDefect root).1 hleft).2
  have hrightClosure :=
    ((mem_proper_context_minimal_generator_signature_iff sensors right generator
      atlas targetDefect root).1 hright).2
  exact hleftClosure.symm.trans hrightClosure

/-- For proper closed contexts, equality of choice-free signatures is exactly
equality of invisible kernels. -/
theorem proper_closed_context_signature_eq_iff_kernel_eq
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (left right : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel)
    (hleftClosed : SensorSupportClosed sensors left atlas targetDefect root)
    (hleftProper : left ≠ Finset.univ)
    (hrightClosed : SensorSupportClosed sensors right atlas targetDefect root) :
    properContextMinimalGeneratorSignature sensors left atlas targetDefect root =
        properContextMinimalGeneratorSignature sensors right atlas targetDefect root ↔
      finiteSensorSupportKernel sensors left atlas targetDefect root =
        finiteSensorSupportKernel sensors right atlas targetDefect root := by
  constructor
  · intro hsignature
    have hcontext :=
      (proper_context_signature_eq_iff_context_eq sensors left right atlas
        targetDefect root hleftClosed hleftProper).1 hsignature
    subst right
    rfl
  · intro hkernel
    have hclosure :
        ClosureEquivalent sensors left right atlas targetDefect root :=
      (closure_equivalent_iff_kernel_eq sensors left right
        atlas targetDefect root).2 hkernel
    have hcontext : left = right := by
      calc
        left = sensorSupportClosure sensors left atlas targetDefect root :=
          hleftClosed.symm
        _ = sensorSupportClosure sensors right atlas targetDefect root := hclosure
        _ = right := hrightClosed
    subst right
    rfl

/-- Canonical signature of a support's closure class. No representative is
chosen; every proper minimal generator in the class is retained. -/
noncomputable def closureClassMinimalGeneratorSignature
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (support : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) : Finset (Finset ι) :=
  properContextMinimalGeneratorSignature sensors
    (sensorSupportClosure sensors support atlas targetDefect root)
    atlas targetDefect root

theorem closure_class_signature_nonempty_of_proper
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (support : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel)
    (hproper :
      sensorSupportClosure sensors support atlas targetDefect root ≠ Finset.univ) :
    (closureClassMinimalGeneratorSignature sensors support atlas targetDefect root).Nonempty := by
  exact proper_context_minimal_generator_signature_nonempty sensors
    (sensorSupportClosure sensors support atlas targetDefect root)
    atlas targetDefect root
    (sensor_support_closure_closed sensors support atlas targetDefect root) hproper

theorem closure_class_signature_antichain
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (support : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    ∀ left ∈
        closureClassMinimalGeneratorSignature sensors support atlas targetDefect root,
      ∀ right ∈
        closureClassMinimalGeneratorSignature sensors support atlas targetDefect root,
        left ⊆ right → left = right := by
  exact proper_context_minimal_generator_signature_antichain sensors
    (sensorSupportClosure sensors support atlas targetDefect root)
    atlas targetDefect root

/-- On proper closure classes, the signature is a complete invariant of closure
equivalence. -/
theorem closure_class_signature_eq_iff_closure_equivalent
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (left right : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel)
    (hleftProper :
      sensorSupportClosure sensors left atlas targetDefect root ≠ Finset.univ) :
    closureClassMinimalGeneratorSignature sensors left atlas targetDefect root =
        closureClassMinimalGeneratorSignature sensors right atlas targetDefect root ↔
      ClosureEquivalent sensors left right atlas targetDefect root := by
  simpa [closureClassMinimalGeneratorSignature, ClosureEquivalent] using
    (proper_context_signature_eq_iff_context_eq sensors
      (sensorSupportClosure sensors left atlas targetDefect root)
      (sensorSupportClosure sensors right atlas targetDefect root)
      atlas targetDefect root
      (sensor_support_closure_closed sensors left atlas targetDefect root)
      hleftProper)

/-- The same choice-free signature classifies exact invisible kernels. -/
theorem closure_class_signature_eq_iff_kernel_eq
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (left right : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel)
    (hleftProper :
      sensorSupportClosure sensors left atlas targetDefect root ≠ Finset.univ) :
    closureClassMinimalGeneratorSignature sensors left atlas targetDefect root =
        closureClassMinimalGeneratorSignature sensors right atlas targetDefect root ↔
      finiteSensorSupportKernel sensors left atlas targetDefect root =
        finiteSensorSupportKernel sensors right atlas targetDefect root := by
  rw [closure_class_signature_eq_iff_closure_equivalent sensors left right
    atlas targetDefect root hleftProper]
  exact closure_equivalent_iff_kernel_eq sensors left right atlas targetDefect root

/-- Context signatures are independent of the selected route root. -/
theorem proper_context_minimal_generator_signature_root_independent
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (context : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (sourceRoot targetRoot : RouteLabel) :
    properContextMinimalGeneratorSignature sensors context atlas targetDefect sourceRoot =
      properContextMinimalGeneratorSignature sensors context atlas targetDefect targetRoot := by
  classical
  apply Finset.ext
  intro generator
  rw [mem_proper_context_minimal_generator_signature_iff,
    mem_proper_context_minimal_generator_signature_iff]
  constructor
  · rintro ⟨hgenerator, hclosure⟩
    refine ⟨?_, ?_⟩
    · rw [← proper_closure_minimal_generators_root_independent sensors
        atlas targetDefect sourceRoot targetRoot]
      exact hgenerator
    · calc
        sensorSupportClosure sensors generator atlas targetDefect targetRoot =
            sensorSupportClosure sensors generator atlas targetDefect sourceRoot :=
          (sensor_support_closure_root_independent sensors generator atlas targetDefect
            sourceRoot targetRoot).symm
        _ = context := hclosure
  · rintro ⟨hgenerator, hclosure⟩
    refine ⟨?_, ?_⟩
    · rw [proper_closure_minimal_generators_root_independent sensors
        atlas targetDefect sourceRoot targetRoot]
      exact hgenerator
    · calc
        sensorSupportClosure sensors generator atlas targetDefect sourceRoot =
            sensorSupportClosure sensors generator atlas targetDefect targetRoot :=
          sensor_support_closure_root_independent sensors generator atlas targetDefect
            sourceRoot targetRoot
        _ = context := hclosure

/-- Closure-class signatures are root independent, including their represented
context and their complete minimal-generator antichain. -/
theorem closure_class_minimal_generator_signature_root_independent
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (support : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (sourceRoot targetRoot : RouteLabel) :
    closureClassMinimalGeneratorSignature sensors support atlas targetDefect sourceRoot =
      closureClassMinimalGeneratorSignature sensors support atlas targetDefect targetRoot := by
  unfold closureClassMinimalGeneratorSignature
  calc
    properContextMinimalGeneratorSignature sensors
        (sensorSupportClosure sensors support atlas targetDefect sourceRoot)
        atlas targetDefect sourceRoot =
      properContextMinimalGeneratorSignature sensors
        (sensorSupportClosure sensors support atlas targetDefect sourceRoot)
        atlas targetDefect targetRoot :=
      proper_context_minimal_generator_signature_root_independent sensors
        (sensorSupportClosure sensors support atlas targetDefect sourceRoot)
        atlas targetDefect sourceRoot targetRoot
    _ = properContextMinimalGeneratorSignature sensors
        (sensorSupportClosure sensors support atlas targetDefect targetRoot)
        atlas targetDefect targetRoot := by
      rw [sensor_support_closure_root_independent sensors support atlas targetDefect
        sourceRoot targetRoot]

/-- Finite formal authority boundary of the v0.94 certificate. -/
structure ChoiceFreeGeneratorAntichainSignatureCertificate where
  sourceMemoryOSV093Bound : Bool
  completeMinimalGeneratorFiberExact : Bool
  properSignatureNonemptyExact : Bool
  signatureAntichainExact : Bool
  signatureContextClassificationExact : Bool
  signatureKernelClassificationExact : Bool
  signatureRootIndependenceExact : Bool
  representativeChoicePerformed : Bool
  uniqueMinimalGeneratorClaimed : Bool
  globalMinimumImplicationBasisClaimed : Bool
  hypergraphDualizationComplexityClaimed : Bool
  externalOracleAuthorityGranted : Bool
  candidateRankingPerformed : Bool
  executionPermission : Bool
  persistentWorldStateMutated : Bool
  truthAuthorityGranted : Bool

end KUOS.OpenHorizon.MemoryOSChoiceFreeGeneratorAntichainSignaturesV0_94
