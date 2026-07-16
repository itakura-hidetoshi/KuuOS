import Mathlib
import KUOS.OpenHorizon.MemoryOSClosedSupportRepresentableKernelOrderIsoV0_99

namespace KUOS.OpenHorizon.MemoryOSFiniteBoundedClosedSupportLatticeV1_00

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
open KUOS.OpenHorizon.MemoryOSClosedSupportRepresentableKernelOrderIsoV0_99

/-- The closed-support fixed-point type carries the exact binary lattice
operations already constructed in v0.99. -/
noncomputable instance closedSensorSupportLattice
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    Lattice (ClosedSensorSupport sensors atlas targetDefect root) where
  sup := closedSensorSupportBinaryJoin sensors atlas targetDefect root
  le_sup_left := by
    intro left right
    change left.1 ⊆
      sensorSupportClosure sensors
        (closedContextFiniteUnion ({left.1, right.1} : Finset (Finset ι)))
        atlas targetDefect root
    intro i hi
    apply sensor_support_subset_closure sensors
      (closedContextFiniteUnion ({left.1, right.1} : Finset (Finset ι)))
      atlas targetDefect root
    exact (mem_closed_context_finite_union_iff
      ({left.1, right.1} : Finset (Finset ι)) i).2
      ⟨left.1, by simp, hi⟩
  le_sup_right := by
    intro left right
    change right.1 ⊆
      sensorSupportClosure sensors
        (closedContextFiniteUnion ({left.1, right.1} : Finset (Finset ι)))
        atlas targetDefect root
    intro i hi
    apply sensor_support_subset_closure sensors
      (closedContextFiniteUnion ({left.1, right.1} : Finset (Finset ι)))
      atlas targetDefect root
    exact (mem_closed_context_finite_union_iff
      ({left.1, right.1} : Finset (Finset ι)) i).2
      ⟨right.1, by simp, hi⟩
  sup_le := by
    intro left right upper hleft hright
    change closedContextFiniteJoin sensors
      ({left.1, right.1} : Finset (Finset ι))
      atlas targetDefect root ⊆ upper.1
    apply (closed_context_finite_join_universal sensors
      ({left.1, right.1} : Finset (Finset ι)) upper.1
      atlas targetDefect root upper.2).2
    intro support hsupport
    simp only [Finset.mem_insert, Finset.mem_singleton] at hsupport
    rcases hsupport with rfl | rfl
    · exact hleft
    · exact hright
  inf := closedSensorSupportBinaryMeet sensors atlas targetDefect root
  inf_le_left := by
    intro left right
    change closedContextFiniteMeet
      ({left.1, right.1} : Finset (Finset ι)) ⊆ left.1
    intro i hi
    exact (mem_closed_context_finite_meet_iff
      ({left.1, right.1} : Finset (Finset ι)) i).1 hi left.1 (by simp)
  inf_le_right := by
    intro left right
    change closedContextFiniteMeet
      ({left.1, right.1} : Finset (Finset ι)) ⊆ right.1
    intro i hi
    exact (mem_closed_context_finite_meet_iff
      ({left.1, right.1} : Finset (Finset ι)) i).1 hi right.1 (by simp)
  le_inf := by
    intro lower left right hleft hright
    change lower.1 ⊆ closedContextFiniteMeet
      ({left.1, right.1} : Finset (Finset ι))
    apply (closed_context_finite_meet_universal lower.1
      ({left.1, right.1} : Finset (Finset ι))).2
    intro support hsupport
    simp only [Finset.mem_insert, Finset.mem_singleton] at hsupport
    rcases hsupport with rfl | rfl
    · exact hleft
    · exact hright

/-- Greatest closed support: every available sensor. -/
noncomputable def closedSensorSupportTop
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    ClosedSensorSupport sensors atlas targetDefect root :=
  ⟨Finset.univ, sensor_support_univ_closed sensors atlas targetDefect root⟩

/-- Least closed support: the closure generated by the empty support. -/
noncomputable def closedSensorSupportBottom
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    ClosedSensorSupport sensors atlas targetDefect root :=
  ⟨sensorSupportClosure sensors (∅ : Finset ι) atlas targetDefect root,
    sensor_support_closure_closed sensors (∅ : Finset ι)
      atlas targetDefect root⟩

/-- Closed supports form a bounded finite-order lattice. This is deliberately
weaker than a `CompleteLattice` claim. -/
noncomputable instance closedSensorSupportBoundedOrder
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    BoundedOrder (ClosedSensorSupport sensors atlas targetDefect root) where
  top := closedSensorSupportTop sensors atlas targetDefect root
  le_top := by
    intro support
    exact Finset.subset_univ support.1
  bot := closedSensorSupportBottom sensors atlas targetDefect root
  bot_le := by
    intro support
    change sensorSupportClosure sensors (∅ : Finset ι)
      atlas targetDefect root ⊆ support.1
    have hmono := sensor_support_closure_mono sensors
      (Finset.empty_subset support.1) atlas targetDefect root
    rw [support.2] at hmono
    exact hmono

@[simp] theorem closed_sensor_support_sup_val
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel)
    (left right : ClosedSensorSupport sensors atlas targetDefect root) :
    (left ⊔ right).1 =
      closedContextFiniteJoin sensors
        ({left.1, right.1} : Finset (Finset ι))
        atlas targetDefect root := rfl

@[simp] theorem closed_sensor_support_inf_val
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel)
    (left right : ClosedSensorSupport sensors atlas targetDefect root) :
    (left ⊓ right).1 =
      closedContextFiniteMeet
        ({left.1, right.1} : Finset (Finset ι)) := rfl

@[simp] theorem closed_sensor_support_top_val
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    ((⊤ : ClosedSensorSupport sensors atlas targetDefect root)).1 =
      (Finset.univ : Finset ι) := rfl

@[simp] theorem closed_sensor_support_bottom_val
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    ((⊥ : ClosedSensorSupport sensors atlas targetDefect root)).1 =
      sensorSupportClosure sensors (∅ : Finset ι)
        atlas targetDefect root := rfl

/-- Typed finite meet of closed supports. -/
noncomputable def closedSensorSupportFiniteMeet
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel)
    (family : Finset (ClosedSensorSupport sensors atlas targetDefect root)) :
    ClosedSensorSupport sensors atlas targetDefect root := by
  classical
  refine ⟨closedContextFiniteMeet (family.image Subtype.val), ?_⟩
  apply closed_context_finite_meet_closed sensors
    (family.image Subtype.val) atlas targetDefect root
  intro support hsupport
  rcases Finset.mem_image.mp hsupport with ⟨context, hcontext, rfl⟩
  exact context.2

/-- Typed finite join of closed supports. -/
noncomputable def closedSensorSupportFiniteJoin
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel)
    (family : Finset (ClosedSensorSupport sensors atlas targetDefect root)) :
    ClosedSensorSupport sensors atlas targetDefect root := by
  classical
  exact
    ⟨closedContextFiniteJoin sensors (family.image Subtype.val)
        atlas targetDefect root,
      closed_context_finite_join_closed sensors (family.image Subtype.val)
        atlas targetDefect root⟩

/-- Universal property of the typed finite meet. -/
theorem le_closed_sensor_support_finite_meet_iff
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel)
    (lower : ClosedSensorSupport sensors atlas targetDefect root)
    (family : Finset (ClosedSensorSupport sensors atlas targetDefect root)) :
    lower ≤ closedSensorSupportFiniteMeet sensors atlas targetDefect root family ↔
      ∀ context ∈ family, lower ≤ context := by
  classical
  constructor
  · intro hlower context hcontext
    change lower.1 ⊆ context.1
    have hall :=
      (closed_context_finite_meet_universal lower.1
        (family.image Subtype.val)).1 hlower
    exact hall context.1
      (Finset.mem_image.mpr ⟨context, hcontext, rfl⟩)
  · intro hall
    change lower.1 ⊆ closedContextFiniteMeet (family.image Subtype.val)
    apply (closed_context_finite_meet_universal lower.1
      (family.image Subtype.val)).2
    intro support hsupport
    rcases Finset.mem_image.mp hsupport with ⟨context, hcontext, rfl⟩
    exact hall context hcontext

/-- Universal property of the typed finite join. -/
theorem closed_sensor_support_finite_join_le_iff
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel)
    (family : Finset (ClosedSensorSupport sensors atlas targetDefect root))
    (upper : ClosedSensorSupport sensors atlas targetDefect root) :
    closedSensorSupportFiniteJoin sensors atlas targetDefect root family ≤ upper ↔
      ∀ context ∈ family, context ≤ upper := by
  classical
  constructor
  · intro hjoin context hcontext
    change context.1 ⊆ upper.1
    have hall :=
      (closed_context_finite_join_universal sensors
        (family.image Subtype.val) upper.1
        atlas targetDefect root upper.2).1 hjoin
    exact hall context.1
      (Finset.mem_image.mpr ⟨context, hcontext, rfl⟩)
  · intro hall
    change closedContextFiniteJoin sensors (family.image Subtype.val)
      atlas targetDefect root ⊆ upper.1
    apply (closed_context_finite_join_universal sensors
      (family.image Subtype.val) upper.1
      atlas targetDefect root upper.2).2
    intro support hsupport
    rcases Finset.mem_image.mp hsupport with ⟨context, hcontext, rfl⟩
    exact hall context hcontext

@[simp] theorem closed_sensor_support_finite_meet_empty
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    closedSensorSupportFiniteMeet sensors atlas targetDefect root ∅ =
      (⊤ : ClosedSensorSupport sensors atlas targetDefect root) := by
  apply Subtype.ext
  exact closed_context_finite_meet_empty

@[simp] theorem closed_sensor_support_finite_join_empty
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    closedSensorSupportFiniteJoin sensors atlas targetDefect root ∅ =
      (⊥ : ClosedSensorSupport sensors atlas targetDefect root) := by
  apply Subtype.ext
  exact closed_context_finite_join_empty sensors atlas targetDefect root

@[simp] theorem closed_sensor_support_finite_meet_singleton
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel)
    (context : ClosedSensorSupport sensors atlas targetDefect root) :
    closedSensorSupportFiniteMeet sensors atlas targetDefect root {context} =
      context := by
  apply Subtype.ext
  simpa [closedSensorSupportFiniteMeet] using
    (closed_context_finite_meet_singleton context.1)

@[simp] theorem closed_sensor_support_finite_join_singleton
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel)
    (context : ClosedSensorSupport sensors atlas targetDefect root) :
    closedSensorSupportFiniteJoin sensors atlas targetDefect root {context} =
      context := by
  apply Subtype.ext
  simpa [closedSensorSupportFiniteJoin] using
    (closed_context_finite_join_singleton sensors context.1
      atlas targetDefect root context.2)

/-- Typed finite join transports exactly to ambient kernel infimum. -/
theorem closed_sensor_support_finite_join_kernel_eq_inf
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel)
    (family : Finset (ClosedSensorSupport sensors atlas targetDefect root)) :
    (closedSupportToRepresentableKernel sensors atlas targetDefect root
      (closedSensorSupportFiniteJoin sensors atlas targetDefect root family)).1 =
      finiteSupportKernelInf sensors (family.image Subtype.val)
        atlas targetDefect root := by
  exact finite_join_support_kernel_eq_inf sensors
    (family.image Subtype.val) atlas targetDefect root

/-- Typed finite meet transports to the representable envelope of ambient
kernel supremum. -/
theorem closed_sensor_support_finite_meet_kernel_eq_envelope_sup
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel)
    (family : Finset (ClosedSensorSupport sensors atlas targetDefect root)) :
    (closedSupportToRepresentableKernel sensors atlas targetDefect root
      (closedSensorSupportFiniteMeet sensors atlas targetDefect root family)).1 =
      sensorKernelEnvelope sensors
        (finiteSupportKernelSup sensors (family.image Subtype.val)
          atlas targetDefect root)
        atlas targetDefect root := by
  classical
  apply finite_meet_support_kernel_eq_envelope_sup sensors
    (family.image Subtype.val) atlas targetDefect root
  intro support hsupport
  rcases Finset.mem_image.mp hsupport with ⟨context, hcontext, rfl⟩
  exact context.2

/-- Closed supports are a finite type because the sensor index is finite. -/
noncomputable instance closedSensorSupportFintype
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    Fintype (ClosedSensorSupport sensors atlas targetDefect root) :=
  Fintype.ofFinite _

/-- Representable kernels inherit finite enumerability through the v0.99
fixed-point equivalence. -/
noncomputable instance representableSensorKernelFintype
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    Fintype (RepresentableSensorKernel sensors atlas targetDefect root) :=
  Fintype.ofEquiv
    (ClosedSensorSupport sensors atlas targetDefect root)
    (closedSupportRepresentableKernelEquiv sensors atlas targetDefect root)

/-- The two typed fixed-point sides have exactly the same finite cardinality. -/
theorem card_closed_support_eq_card_representable_kernel
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    Fintype.card (ClosedSensorSupport sensors atlas targetDefect root) =
      Fintype.card (RepresentableSensorKernel sensors atlas targetDefect root) :=
  Fintype.card_congr
    (closedSupportRepresentableKernelEquiv sensors atlas targetDefect root)

/-- The two bounded endpoints are exchanged by the typed anti-isomorphism. -/
theorem closed_support_endpoints_map_to_dual_kernel_endpoints
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    ((closedSupportRepresentableKernelOrderIso sensors atlas targetDefect root
      (⊥ : ClosedSensorSupport sensors atlas targetDefect root) :
      OrderDual (RepresentableSensorKernel sensors atlas targetDefect root))).1 =
        finiteSensorSupportKernel sensors
          (sensorSupportClosure sensors (∅ : Finset ι)
            atlas targetDefect root)
          atlas targetDefect root ∧
    ((closedSupportRepresentableKernelOrderIso sensors atlas targetDefect root
      (⊤ : ClosedSensorSupport sensors atlas targetDefect root) :
      OrderDual (RepresentableSensorKernel sensors atlas targetDefect root))).1 =
        finiteSensorSupportKernel sensors (Finset.univ : Finset ι)
          atlas targetDefect root := by
  constructor <;> rfl

structure FiniteBoundedClosedSupportLatticeCertificate where
  sourceMemoryOSV099Bound : Bool
  closedSupportLatticeTypeclassExact : Bool
  closedSupportBoundedOrderExact : Bool
  typedFiniteMeetJoinUniversalExact : Bool
  emptySingletonLawsExact : Bool
  finiteKernelTransportExact : Bool
  fixedPointFintypeExact : Bool
  fixedPointCardinalityExact : Bool
  dualEndpointExchangeExact : Bool
  completeLatticeTypeclassClaimed : Bool
  arbitraryIndexedSupInfClaimed : Bool
  infiniteFamilyTheoremClaimed : Bool
  distributivityClaimed : Bool
  modularityClaimed : Bool
  ambientSubgroupLatticeEquivalenceClaimed : Bool
  externalOracleAuthorityGranted : Bool
  executionPermission : Bool
  persistentWorldStateMutated : Bool
  truthAuthorityGranted : Bool

end KUOS.OpenHorizon.MemoryOSFiniteBoundedClosedSupportLatticeV1_00
