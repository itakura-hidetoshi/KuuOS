import Mathlib
import KUOS.OpenHorizon.MemoryOSSensorKernelPolarityV0_98

namespace KUOS.OpenHorizon.MemoryOSClosedSupportRepresentableKernelOrderIsoV0_99

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
open KUOS.OpenHorizon.MemoryOSChoiceFreeSignatureHullKernelOrderDualityV0_95
open KUOS.OpenHorizon.MemoryOSPointedSignatureLatticeV0_96
open KUOS.OpenHorizon.MemoryOSFiniteFamilySignatureLatticeV0_97
open KUOS.OpenHorizon.MemoryOSSensorKernelPolarityV0_98

/-- Closed finite sensor supports at a fixed route root. -/
abbrev ClosedSensorSupport
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :=
  { support : Finset ι //
    SensorSupportClosed sensors support atlas targetDefect root }

/-- Sensor-representable invisible kernels at a fixed route root. -/
abbrev RepresentableSensorKernel
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :=
  { kernel : Subgroup GlobalNormalizedWordSection //
    SensorKernelRepresentable sensors kernel atlas targetDefect root }

/-- A closed support determines a representable kernel. -/
noncomputable def closedSupportToRepresentableKernel
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    ClosedSensorSupport sensors atlas targetDefect root →
      RepresentableSensorKernel sensors atlas targetDefect root :=
  fun support =>
    ⟨finiteSensorSupportKernel sensors support.1 atlas targetDefect root,
      support_kernel_representable sensors support.1 atlas targetDefect root⟩

/-- A representable kernel determines its canonical closed dominated support. -/
noncomputable def representableKernelToClosedSupport
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    RepresentableSensorKernel sensors atlas targetDefect root →
      ClosedSensorSupport sensors atlas targetDefect root :=
  fun kernel =>
    ⟨kernelDominatedSensorSupport sensors kernel.1 atlas targetDefect root,
      kernel_dominated_sensor_support_closed sensors kernel.1
        atlas targetDefect root⟩

@[simp] theorem representable_kernel_to_closed_support_to_kernel
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel)
    (support : ClosedSensorSupport sensors atlas targetDefect root) :
    representableKernelToClosedSupport sensors atlas targetDefect root
        (closedSupportToRepresentableKernel sensors atlas targetDefect root support) =
      support := by
  apply Subtype.ext
  exact kernel_dominated_support_of_closed_eq sensors support.1
    atlas targetDefect root support.2

@[simp] theorem closed_support_to_representable_kernel_to_support
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel)
    (kernel : RepresentableSensorKernel sensors atlas targetDefect root) :
    closedSupportToRepresentableKernel sensors atlas targetDefect root
        (representableKernelToClosedSupport sensors atlas targetDefect root kernel) =
      kernel := by
  apply Subtype.ext
  exact kernel.2

/-- The closed-support and representable-kernel fixed-point types are equivalent. -/
noncomputable def closedSupportRepresentableKernelEquiv
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    ClosedSensorSupport sensors atlas targetDefect root ≃
      RepresentableSensorKernel sensors atlas targetDefect root where
  toFun := closedSupportToRepresentableKernel sensors atlas targetDefect root
  invFun := representableKernelToClosedSupport sensors atlas targetDefect root
  left_inv :=
    representable_kernel_to_closed_support_to_kernel sensors
      atlas targetDefect root
  right_inv :=
    closed_support_to_representable_kernel_to_support sensors
      atlas targetDefect root

/-- Explicit order anti-isomorphism: support inclusion becomes reverse kernel
inclusion. -/
noncomputable def closedSupportRepresentableKernelOrderIso
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    ClosedSensorSupport sensors atlas targetDefect root ≃o
      OrderDual (RepresentableSensorKernel sensors atlas targetDefect root) where
  toFun := closedSupportToRepresentableKernel sensors atlas targetDefect root
  invFun := representableKernelToClosedSupport sensors atlas targetDefect root
  left_inv :=
    representable_kernel_to_closed_support_to_kernel sensors
      atlas targetDefect root
  right_inv :=
    closed_support_to_representable_kernel_to_support sensors
      atlas targetDefect root
  map_rel_iff' := by
    intro left right
    change
      finiteSensorSupportKernel sensors right.1 atlas targetDefect root ≤
          finiteSensorSupportKernel sensors left.1 atlas targetDefect root ↔
        left.1 ⊆ right.1
    exact
      (closed_support_order_anti_equivalence sensors left.1 right.1
        atlas targetDefect root left.2 right.2).symm

@[simp] theorem closed_support_order_iso_apply_val
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel)
    (support : ClosedSensorSupport sensors atlas targetDefect root) :
    ((closedSupportRepresentableKernelOrderIso sensors atlas targetDefect root
      support :
      OrderDual (RepresentableSensorKernel sensors atlas targetDefect root))).1 =
      finiteSensorSupportKernel sensors support.1 atlas targetDefect root := rfl

@[simp] theorem closed_support_order_iso_symm_apply_val
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel)
    (kernel :
      OrderDual (RepresentableSensorKernel sensors atlas targetDefect root)) :
    ((closedSupportRepresentableKernelOrderIso sensors atlas targetDefect root).symm
      kernel).1 =
      kernelDominatedSensorSupport sensors kernel.1 atlas targetDefect root := rfl

/-- Binary join in the closed-support fixed-point type. -/
noncomputable def closedSensorSupportBinaryJoin
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel)
    (left right : ClosedSensorSupport sensors atlas targetDefect root) :
    ClosedSensorSupport sensors atlas targetDefect root :=
  ⟨closedContextFiniteJoin sensors ({left.1, right.1} : Finset (Finset ι))
      atlas targetDefect root,
    closed_context_finite_join_closed sensors
      ({left.1, right.1} : Finset (Finset ι)) atlas targetDefect root⟩

/-- Binary meet in the closed-support fixed-point type. -/
noncomputable def closedSensorSupportBinaryMeet
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel)
    (left right : ClosedSensorSupport sensors atlas targetDefect root) :
    ClosedSensorSupport sensors atlas targetDefect root :=
  ⟨closedContextFiniteMeet ({left.1, right.1} : Finset (Finset ι)),
    by
      apply closed_context_finite_meet_closed sensors
        ({left.1, right.1} : Finset (Finset ι)) atlas targetDefect root
      intro support hsupport
      simp only [Finset.mem_insert, Finset.mem_singleton] at hsupport
      rcases hsupport with rfl | rfl
      · exact left.2
      · exact right.2⟩

/-- Binary closed-support join maps to ambient kernel infimum. -/
theorem closed_support_binary_join_kernel_eq_inf
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel)
    (left right : ClosedSensorSupport sensors atlas targetDefect root) :
    (closedSupportToRepresentableKernel sensors atlas targetDefect root
      (closedSensorSupportBinaryJoin sensors atlas targetDefect root left right)).1 =
      finiteSupportKernelInf sensors
        ({left.1, right.1} : Finset (Finset ι)) atlas targetDefect root := by
  exact finite_join_support_kernel_eq_inf sensors
    ({left.1, right.1} : Finset (Finset ι)) atlas targetDefect root

/-- Binary closed-support meet maps to the representable envelope of ambient
kernel supremum. -/
theorem closed_support_binary_meet_kernel_eq_envelope_sup
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel)
    (left right : ClosedSensorSupport sensors atlas targetDefect root) :
    (closedSupportToRepresentableKernel sensors atlas targetDefect root
      (closedSensorSupportBinaryMeet sensors atlas targetDefect root left right)).1 =
      sensorKernelEnvelope sensors
        (finiteSupportKernelSup sensors
          ({left.1, right.1} : Finset (Finset ι)) atlas targetDefect root)
        atlas targetDefect root := by
  apply finite_meet_support_kernel_eq_envelope_sup sensors
    ({left.1, right.1} : Finset (Finset ι)) atlas targetDefect root
  intro support hsupport
  simp only [Finset.mem_insert, Finset.mem_singleton] at hsupport
  rcases hsupport with rfl | rfl
  · exact left.2
  · exact right.2

/-- The support-to-kernel map has root-independent underlying kernel values. -/
theorem closed_support_to_kernel_root_independent
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (support : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (sourceRoot targetRoot : RouteLabel)
    (hsource : SensorSupportClosed sensors support atlas targetDefect sourceRoot)
    (htarget : SensorSupportClosed sensors support atlas targetDefect targetRoot) :
    (closedSupportToRepresentableKernel sensors atlas targetDefect sourceRoot
      ⟨support, hsource⟩).1 =
    (closedSupportToRepresentableKernel sensors atlas targetDefect targetRoot
      ⟨support, htarget⟩).1 := by
  exact finite_sensor_support_kernel_root_independent sensors support
    atlas targetDefect sourceRoot targetRoot

/-- The kernel-to-support map has root-independent underlying support values. -/
theorem representable_kernel_to_support_root_independent
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (kernel : Subgroup GlobalNormalizedWordSection)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (sourceRoot targetRoot : RouteLabel)
    (hsource : SensorKernelRepresentable sensors kernel
      atlas targetDefect sourceRoot)
    (htarget : SensorKernelRepresentable sensors kernel
      atlas targetDefect targetRoot) :
    (representableKernelToClosedSupport sensors atlas targetDefect sourceRoot
      ⟨kernel, hsource⟩).1 =
    (representableKernelToClosedSupport sensors atlas targetDefect targetRoot
      ⟨kernel, htarget⟩).1 := by
  exact kernel_dominated_sensor_support_root_independent sensors kernel
    atlas targetDefect sourceRoot targetRoot

structure ClosedSupportRepresentableKernelOrderIsoCertificate where
  sourceMemoryOSV098Bound : Bool
  closedSupportSubtypeExact : Bool
  representableKernelSubtypeExact : Bool
  inverseMapsExact : Bool
  orderAntiIsoExact : Bool
  binaryJoinKernelInfCompatibilityExact : Bool
  binaryMeetKernelEnvelopeSupCompatibilityExact : Bool
  underlyingMapsRootIndependentExact : Bool
  completeLatticeTypeclassClaimed : Bool
  infiniteFamilyTheoremClaimed : Bool
  distributivityClaimed : Bool
  modularityClaimed : Bool
  universalRepresentabilityClaimed : Bool
  externalOracleAuthorityGranted : Bool
  executionPermission : Bool
  persistentWorldStateMutated : Bool
  truthAuthorityGranted : Bool

end KUOS.OpenHorizon.MemoryOSClosedSupportRepresentableKernelOrderIsoV0_99
