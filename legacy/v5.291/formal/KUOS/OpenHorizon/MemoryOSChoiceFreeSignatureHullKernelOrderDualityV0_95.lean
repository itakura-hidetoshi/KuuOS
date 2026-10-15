import Mathlib
import KUOS.OpenHorizon.MemoryOSChoiceFreeGeneratorAntichainSignaturesV0_94

namespace KUOS.OpenHorizon.MemoryOSChoiceFreeSignatureHullKernelOrderDualityV0_95

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
open KUOS.OpenHorizon.MemoryOSChoiceFreeGeneratorAntichainSignaturesV0_94

/-- Choice-free union of every finite support retained in an antichain
signature. No representative is selected. -/
noncomputable def minimalGeneratorAntichainEnvelope
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    (signature : Finset (Finset ι)) : Finset ι := by
  classical
  exact Finset.univ.filter fun i =>
    ∃ generator ∈ signature, i ∈ generator

theorem mem_minimal_generator_antichain_envelope_iff
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    (signature : Finset (Finset ι)) (i : ι) :
    i ∈ minimalGeneratorAntichainEnvelope signature ↔
      ∃ generator ∈ signature, i ∈ generator := by
  classical
  simp [minimalGeneratorAntichainEnvelope]

theorem signature_member_subset_antichain_envelope
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    (signature : Finset (Finset ι)) (generator : Finset ι)
    (hgenerator : generator ∈ signature) :
    generator ⊆ minimalGeneratorAntichainEnvelope signature := by
  intro i hi
  rw [mem_minimal_generator_antichain_envelope_iff]
  exact ⟨generator, hgenerator, hi⟩

/-- Closure of a choice-free minimal-generator antichain envelope. -/
noncomputable def minimalGeneratorAntichainClosedHull
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (signature : Finset (Finset ι))
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) : Finset ι :=
  sensorSupportClosure sensors
    (minimalGeneratorAntichainEnvelope signature)
    atlas targetDefect root

/-- The order represented by two antichain signatures is inclusion of their
choice-free closed hulls. -/
def MinimalGeneratorAntichainHullLe
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (left right : Finset (Finset ι))
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) : Prop :=
  minimalGeneratorAntichainClosedHull sensors left atlas targetDefect root ⊆
    minimalGeneratorAntichainClosedHull sensors right atlas targetDefect root

theorem proper_context_signature_envelope_subset_context
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (context : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    minimalGeneratorAntichainEnvelope
        (properContextMinimalGeneratorSignature sensors context
          atlas targetDefect root) ⊆
      context := by
  intro i hi
  rw [mem_minimal_generator_antichain_envelope_iff] at hi
  obtain ⟨generator, hgenerator, hiGenerator⟩ := hi
  exact
    (signature_member_subset_context sensors context generator
      atlas targetDefect root hgenerator) hiGenerator

/-- The closure of the full minimal-generator antichain envelope reconstructs
the represented proper closed context exactly. -/
theorem proper_context_signature_closed_hull_eq
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (context : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel)
    (hclosed : SensorSupportClosed sensors context atlas targetDefect root)
    (hproper : context ≠ Finset.univ) :
    minimalGeneratorAntichainClosedHull sensors
        (properContextMinimalGeneratorSignature sensors context
          atlas targetDefect root)
        atlas targetDefect root =
      context := by
  apply Finset.Subset.antisymm
  · have hmono :=
      sensor_support_closure_mono sensors
        (proper_context_signature_envelope_subset_context sensors context
          atlas targetDefect root)
        atlas targetDefect root
    rw [hclosed] at hmono
    exact hmono
  · obtain ⟨generator, hgenerator⟩ :=
      proper_context_minimal_generator_signature_nonempty sensors context
        atlas targetDefect root hclosed hproper
    have hgeneratorSubset :
        generator ⊆
          minimalGeneratorAntichainEnvelope
            (properContextMinimalGeneratorSignature sensors context
              atlas targetDefect root) :=
      signature_member_subset_antichain_envelope
        (properContextMinimalGeneratorSignature sensors context
          atlas targetDefect root)
        generator hgenerator
    have hmono :=
      sensor_support_closure_mono sensors hgeneratorSubset
        atlas targetDefect root
    have hgeneratorClosure :=
      ((mem_proper_context_minimal_generator_signature_iff sensors
        context generator atlas targetDefect root).1 hgenerator).2
    rw [hgeneratorClosure] at hmono
    exact hmono

/-- A proper support closure is reconstructed from the choice-free antichain
signature of its closure class. -/
theorem closure_class_signature_closed_hull_eq
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (support : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel)
    (hproper :
      sensorSupportClosure sensors support atlas targetDefect root ≠
        Finset.univ) :
    minimalGeneratorAntichainClosedHull sensors
        (closureClassMinimalGeneratorSignature sensors support
          atlas targetDefect root)
        atlas targetDefect root =
      sensorSupportClosure sensors support atlas targetDefect root := by
  unfold closureClassMinimalGeneratorSignature
  exact proper_context_signature_closed_hull_eq sensors
    (sensorSupportClosure sensors support atlas targetDefect root)
    atlas targetDefect root
    (sensor_support_closure_closed sensors support atlas targetDefect root)
    hproper

/-- The choice-free signature envelope has exactly the same invisible kernel
as the support whose proper closure class it represents. -/
theorem closure_class_signature_envelope_kernel_eq
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (support : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel)
    (hproper :
      sensorSupportClosure sensors support atlas targetDefect root ≠
        Finset.univ) :
    finiteSensorSupportKernel sensors
        (minimalGeneratorAntichainEnvelope
          (closureClassMinimalGeneratorSignature sensors support
            atlas targetDefect root))
        atlas targetDefect root =
      finiteSensorSupportKernel sensors support atlas targetDefect root := by
  apply
    (finite_sensor_support_kernel_eq_iff_closure_eq sensors
      (minimalGeneratorAntichainEnvelope
        (closureClassMinimalGeneratorSignature sensors support
          atlas targetDefect root))
      support atlas targetDefect root).2
  exact closure_class_signature_closed_hull_eq sensors support
    atlas targetDefect root hproper

/-- Inclusion of closed sensor contexts is exactly reverse inclusion of their
finite invisible kernels. -/
theorem closed_context_subset_iff_kernel_reverse
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (left right : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel)
    (hleftClosed : SensorSupportClosed sensors left atlas targetDefect root)
    (hrightClosed : SensorSupportClosed sensors right atlas targetDefect root) :
    left ⊆ right ↔
      finiteSensorSupportKernel sensors right atlas targetDefect root ≤
        finiteSensorSupportKernel sensors left atlas targetDefect root := by
  constructor
  · intro hsubset
    exact finite_sensor_support_kernel_antitone sensors hsubset
      atlas targetDefect root
  · intro hkernel i hi
    have hiLeftClosure :
        i ∈ sensorSupportClosure sensors left atlas targetDefect root := by
      rw [hleftClosed]
      exact hi
    have hleftDominates :=
      (mem_sensor_support_closure_iff sensors left i
        atlas targetDefect root).1 hiLeftClosure
    have hiRightClosure :
        i ∈ sensorSupportClosure sensors right atlas targetDefect root :=
      (mem_sensor_support_closure_iff sensors right i
        atlas targetDefect root).2 (hkernel.trans hleftDominates)
    rw [hrightClosed] at hiRightClosure
    exact hiRightClosure

/-- On proper closed contexts, hull inclusion of the choice-free signatures is
exactly context inclusion. -/
theorem proper_context_signature_hull_le_iff_subset
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (left right : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel)
    (hleftClosed : SensorSupportClosed sensors left atlas targetDefect root)
    (hleftProper : left ≠ Finset.univ)
    (hrightClosed : SensorSupportClosed sensors right atlas targetDefect root)
    (hrightProper : right ≠ Finset.univ) :
    MinimalGeneratorAntichainHullLe sensors
        (properContextMinimalGeneratorSignature sensors left
          atlas targetDefect root)
        (properContextMinimalGeneratorSignature sensors right
          atlas targetDefect root)
        atlas targetDefect root ↔
      left ⊆ right := by
  unfold MinimalGeneratorAntichainHullLe
  rw [proper_context_signature_closed_hull_eq sensors left
      atlas targetDefect root hleftClosed hleftProper,
    proper_context_signature_closed_hull_eq sensors right
      atlas targetDefect root hrightClosed hrightProper]

/-- The same signature-hull order is exactly reverse invisible-kernel
inclusion. -/
theorem proper_context_signature_hull_le_iff_kernel_reverse
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (left right : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel)
    (hleftClosed : SensorSupportClosed sensors left atlas targetDefect root)
    (hleftProper : left ≠ Finset.univ)
    (hrightClosed : SensorSupportClosed sensors right atlas targetDefect root)
    (hrightProper : right ≠ Finset.univ) :
    MinimalGeneratorAntichainHullLe sensors
        (properContextMinimalGeneratorSignature sensors left
          atlas targetDefect root)
        (properContextMinimalGeneratorSignature sensors right
          atlas targetDefect root)
        atlas targetDefect root ↔
      finiteSensorSupportKernel sensors right atlas targetDefect root ≤
        finiteSensorSupportKernel sensors left atlas targetDefect root := by
  rw [proper_context_signature_hull_le_iff_subset sensors left right
    atlas targetDefect root hleftClosed hleftProper
    hrightClosed hrightProper]
  exact closed_context_subset_iff_kernel_reverse sensors left right
    atlas targetDefect root hleftClosed hrightClosed

/-- For proper closure classes, signature-hull inclusion is exactly inclusion
of the represented closures. -/
theorem closure_class_signature_hull_le_iff_closure_subset
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (left right : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel)
    (hleftProper :
      sensorSupportClosure sensors left atlas targetDefect root ≠
        Finset.univ)
    (hrightProper :
      sensorSupportClosure sensors right atlas targetDefect root ≠
        Finset.univ) :
    MinimalGeneratorAntichainHullLe sensors
        (closureClassMinimalGeneratorSignature sensors left
          atlas targetDefect root)
        (closureClassMinimalGeneratorSignature sensors right
          atlas targetDefect root)
        atlas targetDefect root ↔
      sensorSupportClosure sensors left atlas targetDefect root ⊆
        sensorSupportClosure sensors right atlas targetDefect root := by
  unfold MinimalGeneratorAntichainHullLe
  rw [closure_class_signature_closed_hull_eq sensors left
      atlas targetDefect root hleftProper,
    closure_class_signature_closed_hull_eq sensors right
      atlas targetDefect root hrightProper]

/-- For proper closure classes, the signature-hull order is exactly reverse
inclusion of the original support kernels. -/
theorem closure_class_signature_hull_le_iff_kernel_reverse
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (left right : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel)
    (hleftProper :
      sensorSupportClosure sensors left atlas targetDefect root ≠
        Finset.univ)
    (hrightProper :
      sensorSupportClosure sensors right atlas targetDefect root ≠
        Finset.univ) :
    MinimalGeneratorAntichainHullLe sensors
        (closureClassMinimalGeneratorSignature sensors left
          atlas targetDefect root)
        (closureClassMinimalGeneratorSignature sensors right
          atlas targetDefect root)
        atlas targetDefect root ↔
      finiteSensorSupportKernel sensors right atlas targetDefect root ≤
        finiteSensorSupportKernel sensors left atlas targetDefect root := by
  rw [closure_class_signature_hull_le_iff_closure_subset sensors left right
    atlas targetDefect root hleftProper hrightProper]
  have horder :=
    closed_context_subset_iff_kernel_reverse sensors
      (sensorSupportClosure sensors left atlas targetDefect root)
      (sensorSupportClosure sensors right atlas targetDefect root)
      atlas targetDefect root
      (sensor_support_closure_closed sensors left atlas targetDefect root)
      (sensor_support_closure_closed sensors right atlas targetDefect root)
  rw [sensor_support_closure_kernel_eq,
    sensor_support_closure_kernel_eq] at horder
  exact horder

/-- Bidirectional signature-hull order on proper closed contexts forces exact
equality of their choice-free signatures. -/
theorem proper_context_signature_hull_le_antisymm
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (left right : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel)
    (hleftClosed : SensorSupportClosed sensors left atlas targetDefect root)
    (hleftProper : left ≠ Finset.univ)
    (hrightClosed : SensorSupportClosed sensors right atlas targetDefect root)
    (hrightProper : right ≠ Finset.univ)
    (hleftRight :
      MinimalGeneratorAntichainHullLe sensors
        (properContextMinimalGeneratorSignature sensors left
          atlas targetDefect root)
        (properContextMinimalGeneratorSignature sensors right
          atlas targetDefect root)
        atlas targetDefect root)
    (hrightLeft :
      MinimalGeneratorAntichainHullLe sensors
        (properContextMinimalGeneratorSignature sensors right
          atlas targetDefect root)
        (properContextMinimalGeneratorSignature sensors left
          atlas targetDefect root)
        atlas targetDefect root) :
    properContextMinimalGeneratorSignature sensors left
        atlas targetDefect root =
      properContextMinimalGeneratorSignature sensors right
        atlas targetDefect root := by
  have hsubsetLeftRight :=
    (proper_context_signature_hull_le_iff_subset sensors left right
      atlas targetDefect root hleftClosed hleftProper
      hrightClosed hrightProper).1 hleftRight
  have hsubsetRightLeft :=
    (proper_context_signature_hull_le_iff_subset sensors right left
      atlas targetDefect root hrightClosed hrightProper
      hleftClosed hleftProper).1 hrightLeft
  have hcontext : left = right :=
    Finset.Subset.antisymm hsubsetLeftRight hsubsetRightLeft
  subst right
  rfl

/-- Context signature envelopes are root independent. -/
theorem proper_context_signature_envelope_root_independent
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (context : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (sourceRoot targetRoot : RouteLabel) :
    minimalGeneratorAntichainEnvelope
        (properContextMinimalGeneratorSignature sensors context
          atlas targetDefect sourceRoot) =
      minimalGeneratorAntichainEnvelope
        (properContextMinimalGeneratorSignature sensors context
          atlas targetDefect targetRoot) := by
  rw [proper_context_minimal_generator_signature_root_independent sensors
    context atlas targetDefect sourceRoot targetRoot]

/-- Context signature closed hulls are root independent. -/
theorem proper_context_signature_closed_hull_root_independent
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (context : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (sourceRoot targetRoot : RouteLabel) :
    minimalGeneratorAntichainClosedHull sensors
        (properContextMinimalGeneratorSignature sensors context
          atlas targetDefect sourceRoot)
        atlas targetDefect sourceRoot =
      minimalGeneratorAntichainClosedHull sensors
        (properContextMinimalGeneratorSignature sensors context
          atlas targetDefect targetRoot)
        atlas targetDefect targetRoot := by
  unfold minimalGeneratorAntichainClosedHull
  calc
    sensorSupportClosure sensors
        (minimalGeneratorAntichainEnvelope
          (properContextMinimalGeneratorSignature sensors context
            atlas targetDefect sourceRoot))
        atlas targetDefect sourceRoot =
      sensorSupportClosure sensors
        (minimalGeneratorAntichainEnvelope
          (properContextMinimalGeneratorSignature sensors context
            atlas targetDefect sourceRoot))
        atlas targetDefect targetRoot :=
      sensor_support_closure_root_independent sensors
        (minimalGeneratorAntichainEnvelope
          (properContextMinimalGeneratorSignature sensors context
            atlas targetDefect sourceRoot))
        atlas targetDefect sourceRoot targetRoot
    _ = sensorSupportClosure sensors
        (minimalGeneratorAntichainEnvelope
          (properContextMinimalGeneratorSignature sensors context
            atlas targetDefect targetRoot))
        atlas targetDefect targetRoot := by
      rw [proper_context_signature_envelope_root_independent sensors context
        atlas targetDefect sourceRoot targetRoot]

/-- Closure-class signature envelopes are root independent. -/
theorem closure_class_signature_envelope_root_independent
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (support : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (sourceRoot targetRoot : RouteLabel) :
    minimalGeneratorAntichainEnvelope
        (closureClassMinimalGeneratorSignature sensors support
          atlas targetDefect sourceRoot) =
      minimalGeneratorAntichainEnvelope
        (closureClassMinimalGeneratorSignature sensors support
          atlas targetDefect targetRoot) := by
  rw [closure_class_minimal_generator_signature_root_independent sensors
    support atlas targetDefect sourceRoot targetRoot]

/-- Closure-class signature closed hulls are root independent. -/
theorem closure_class_signature_closed_hull_root_independent
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (support : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (sourceRoot targetRoot : RouteLabel) :
    minimalGeneratorAntichainClosedHull sensors
        (closureClassMinimalGeneratorSignature sensors support
          atlas targetDefect sourceRoot)
        atlas targetDefect sourceRoot =
      minimalGeneratorAntichainClosedHull sensors
        (closureClassMinimalGeneratorSignature sensors support
          atlas targetDefect targetRoot)
        atlas targetDefect targetRoot := by
  unfold minimalGeneratorAntichainClosedHull
  calc
    sensorSupportClosure sensors
        (minimalGeneratorAntichainEnvelope
          (closureClassMinimalGeneratorSignature sensors support
            atlas targetDefect sourceRoot))
        atlas targetDefect sourceRoot =
      sensorSupportClosure sensors
        (minimalGeneratorAntichainEnvelope
          (closureClassMinimalGeneratorSignature sensors support
            atlas targetDefect sourceRoot))
        atlas targetDefect targetRoot :=
      sensor_support_closure_root_independent sensors
        (minimalGeneratorAntichainEnvelope
          (closureClassMinimalGeneratorSignature sensors support
            atlas targetDefect sourceRoot))
        atlas targetDefect sourceRoot targetRoot
    _ = sensorSupportClosure sensors
        (minimalGeneratorAntichainEnvelope
          (closureClassMinimalGeneratorSignature sensors support
            atlas targetDefect targetRoot))
        atlas targetDefect targetRoot := by
      rw [closure_class_signature_envelope_root_independent sensors support
        atlas targetDefect sourceRoot targetRoot]

/-- Finite formal authority boundary of the v0.95 certificate. -/
structure ChoiceFreeSignatureHullKernelOrderDualityCertificate where
  sourceMemoryOSV094Bound : Bool
  signatureEnvelopeExact : Bool
  properContextHullReconstructionExact : Bool
  closureClassHullReconstructionExact : Bool
  envelopeKernelPreservationExact : Bool
  signatureHullContextOrderExact : Bool
  signatureHullKernelOrderDualityExact : Bool
  signatureHullAntisymmetryExact : Bool
  rootIndependenceExact : Bool
  representativeChoicePerformed : Bool
  uniqueMinimalGeneratorClaimed : Bool
  completeLatticeStructureClaimed : Bool
  generalUniqueAntichainFactorizationClaimed : Bool
  externalOracleAuthorityGranted : Bool
  candidateRankingPerformed : Bool
  executionPermission : Bool
  persistentWorldStateMutated : Bool
  truthAuthorityGranted : Bool

end KUOS.OpenHorizon.MemoryOSChoiceFreeSignatureHullKernelOrderDualityV0_95
