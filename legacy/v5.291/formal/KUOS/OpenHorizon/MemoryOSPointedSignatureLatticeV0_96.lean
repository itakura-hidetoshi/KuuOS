import Mathlib
import KUOS.OpenHorizon.MemoryOSChoiceFreeSignatureHullKernelOrderDualityV0_95

namespace KUOS.OpenHorizon.MemoryOSPointedSignatureLatticeV0_96

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

/-- Pointed completion of the proper-context signature.
The empty outer finset is reserved for the universal closed context. -/
noncomputable def completedClosedContextSignature
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (context : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) : Finset (Finset ι) := by
  classical
  exact if context = Finset.univ then ∅ else
    properContextMinimalGeneratorSignature sensors context atlas targetDefect root

/-- Empty is the explicit top sentinel; a nonempty signature is decoded through
its choice-free antichain closed hull. -/
noncomputable def completedSignatureClosedHull
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (signature : Finset (Finset ι))
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) : Finset ι := by
  classical
  exact if signature = ∅ then Finset.univ else
    minimalGeneratorAntichainClosedHull sensors signature atlas targetDefect root

def CompletedSignatureHullLe
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (left right : Finset (Finset ι))
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) : Prop :=
  completedSignatureClosedHull sensors left atlas targetDefect root ⊆
    completedSignatureClosedHull sensors right atlas targetDefect root

def closedContextMeet {ι : Type*} [DecidableEq ι]
    (left right : Finset ι) : Finset ι :=
  left ∩ right

noncomputable def closedContextJoin
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (left right : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) : Finset ι :=
  sensorSupportClosure sensors (left ∪ right) atlas targetDefect root

noncomputable def completedSignatureMeet
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (left right : Finset (Finset ι))
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) : Finset (Finset ι) :=
  completedClosedContextSignature sensors
    (closedContextMeet
      (completedSignatureClosedHull sensors left atlas targetDefect root)
      (completedSignatureClosedHull sensors right atlas targetDefect root))
    atlas targetDefect root

noncomputable def completedSignatureJoin
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (left right : Finset (Finset ι))
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) : Finset (Finset ι) :=
  completedClosedContextSignature sensors
    (closedContextJoin sensors
      (completedSignatureClosedHull sensors left atlas targetDefect root)
      (completedSignatureClosedHull sensors right atlas targetDefect root)
      atlas targetDefect root)
    atlas targetDefect root

theorem completed_closed_context_signature_univ
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    completedClosedContextSignature sensors (Finset.univ : Finset ι)
      atlas targetDefect root = ∅ := by
  classical
  simp [completedClosedContextSignature]

theorem completed_closed_context_signature_of_proper
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (context : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) (hproper : context ≠ Finset.univ) :
    completedClosedContextSignature sensors context atlas targetDefect root =
      properContextMinimalGeneratorSignature sensors context
        atlas targetDefect root := by
  classical
  simp [completedClosedContextSignature, hproper]

theorem completed_closed_context_signature_eq_empty_iff
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (context : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel)
    (hclosed : SensorSupportClosed sensors context atlas targetDefect root) :
    completedClosedContextSignature sensors context atlas targetDefect root = ∅ ↔
      context = Finset.univ := by
  constructor
  · intro hempty
    by_contra hproper
    have hnonempty :=
      proper_context_minimal_generator_signature_nonempty sensors context
        atlas targetDefect root hclosed hproper
    have hcompleted :
        (completedClosedContextSignature sensors context
          atlas targetDefect root).Nonempty := by
      rw [completed_closed_context_signature_of_proper sensors context
        atlas targetDefect root hproper]
      exact hnonempty
    rw [hempty] at hcompleted
    simpa using hcompleted
  · intro htop
    subst context
    exact completed_closed_context_signature_univ sensors
      atlas targetDefect root

theorem completed_signature_closed_hull_empty
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    completedSignatureClosedHull sensors (∅ : Finset (Finset ι))
      atlas targetDefect root = Finset.univ := by
  classical
  simp [completedSignatureClosedHull]

/-- Pointed encode/decode is exact on every closed context, including top. -/
theorem completed_signature_closed_hull_encode_eq
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (context : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel)
    (hclosed : SensorSupportClosed sensors context atlas targetDefect root) :
    completedSignatureClosedHull sensors
        (completedClosedContextSignature sensors context atlas targetDefect root)
        atlas targetDefect root =
      context := by
  classical
  by_cases htop : context = Finset.univ
  · subst context
    simp [completedClosedContextSignature, completedSignatureClosedHull]
  · rw [completed_closed_context_signature_of_proper sensors context
      atlas targetDefect root htop]
    obtain ⟨generator, hgenerator⟩ :=
      proper_context_minimal_generator_signature_nonempty sensors context
        atlas targetDefect root hclosed htop
    have hsignature_ne :
        properContextMinimalGeneratorSignature sensors context
          atlas targetDefect root ≠ ∅ := by
      intro hempty
      rw [hempty] at hgenerator
      simp at hgenerator
    change
      (if properContextMinimalGeneratorSignature sensors context
            atlas targetDefect root = ∅
        then Finset.univ
        else minimalGeneratorAntichainClosedHull sensors
          (properContextMinimalGeneratorSignature sensors context
            atlas targetDefect root)
          atlas targetDefect root) =
        context
    rw [if_neg hsignature_ne]
    exact proper_context_signature_closed_hull_eq sensors context
      atlas targetDefect root hclosed htop

theorem completed_signature_hull_le_iff_subset
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (left right : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel)
    (hleftClosed : SensorSupportClosed sensors left atlas targetDefect root)
    (hrightClosed : SensorSupportClosed sensors right atlas targetDefect root) :
    CompletedSignatureHullLe sensors
        (completedClosedContextSignature sensors left atlas targetDefect root)
        (completedClosedContextSignature sensors right atlas targetDefect root)
        atlas targetDefect root ↔
      left ⊆ right := by
  unfold CompletedSignatureHullLe
  rw [completed_signature_closed_hull_encode_eq sensors left
      atlas targetDefect root hleftClosed,
    completed_signature_closed_hull_encode_eq sensors right
      atlas targetDefect root hrightClosed]

/-- Intersections of closed contexts are closed. -/
theorem closed_context_meet_closed
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (left right : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel)
    (hleftClosed : SensorSupportClosed sensors left atlas targetDefect root)
    (hrightClosed : SensorSupportClosed sensors right atlas targetDefect root) :
    SensorSupportClosed sensors (closedContextMeet left right)
      atlas targetDefect root := by
  unfold SensorSupportClosed closedContextMeet
  apply Finset.Subset.antisymm
  · intro i hi
    have hleftMono :
        i ∈ sensorSupportClosure sensors left atlas targetDefect root :=
      (sensor_support_closure_mono sensors
        (Finset.inter_subset_left : left ∩ right ⊆ left)
        atlas targetDefect root) hi
    have hrightMono :
        i ∈ sensorSupportClosure sensors right atlas targetDefect root :=
      (sensor_support_closure_mono sensors
        (Finset.inter_subset_right : left ∩ right ⊆ right)
        atlas targetDefect root) hi
    rw [hleftClosed] at hleftMono
    rw [hrightClosed] at hrightMono
    exact Finset.mem_inter.mpr ⟨hleftMono, hrightMono⟩
  · exact sensor_support_subset_closure sensors (left ∩ right)
      atlas targetDefect root

theorem closed_context_join_closed
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (left right : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    SensorSupportClosed sensors
      (closedContextJoin sensors left right atlas targetDefect root)
      atlas targetDefect root := by
  exact sensor_support_closure_closed sensors (left ∪ right)
    atlas targetDefect root

/-- Intersection is the greatest closed lower bound. -/
theorem closed_context_meet_universal
    {ι : Type*} [DecidableEq ι]
    (lower left right : Finset ι) :
    lower ⊆ closedContextMeet left right ↔
      lower ⊆ left ∧ lower ⊆ right := by
  constructor
  · intro h
    exact ⟨h.trans Finset.inter_subset_left,
      h.trans Finset.inter_subset_right⟩
  · rintro ⟨hleft, hright⟩ i hi
    exact Finset.mem_inter.mpr ⟨hleft hi, hright hi⟩

/-- Closure of union is the least closed upper bound. -/
theorem closed_context_join_universal
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (left right upper : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel)
    (hupperClosed : SensorSupportClosed sensors upper atlas targetDefect root) :
    closedContextJoin sensors left right atlas targetDefect root ⊆ upper ↔
      left ⊆ upper ∧ right ⊆ upper := by
  constructor
  · intro h
    refine ⟨?_, ?_⟩
    · intro i hi
      exact h ((sensor_support_subset_closure sensors (left ∪ right)
        atlas targetDefect root) (Finset.mem_union_left right hi))
    · intro i hi
      exact h ((sensor_support_subset_closure sensors (left ∪ right)
        atlas targetDefect root) (Finset.mem_union_right left hi))
  · rintro ⟨hleft, hright⟩
    have hunion : left ∪ right ⊆ upper := by
      intro i hi
      rw [Finset.mem_union] at hi
      exact hi.elim hleft hright
    have hmono :=
      sensor_support_closure_mono sensors hunion atlas targetDefect root
    rw [hupperClosed] at hmono
    exact hmono

theorem completed_signature_meet_decode_eq
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (left right : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel)
    (hleftClosed : SensorSupportClosed sensors left atlas targetDefect root)
    (hrightClosed : SensorSupportClosed sensors right atlas targetDefect root) :
    completedSignatureClosedHull sensors
        (completedSignatureMeet sensors
          (completedClosedContextSignature sensors left atlas targetDefect root)
          (completedClosedContextSignature sensors right atlas targetDefect root)
          atlas targetDefect root)
        atlas targetDefect root =
      closedContextMeet left right := by
  unfold completedSignatureMeet
  rw [completed_signature_closed_hull_encode_eq sensors left
      atlas targetDefect root hleftClosed,
    completed_signature_closed_hull_encode_eq sensors right
      atlas targetDefect root hrightClosed]
  exact completed_signature_closed_hull_encode_eq sensors
    (closedContextMeet left right) atlas targetDefect root
    (closed_context_meet_closed sensors left right atlas targetDefect root
      hleftClosed hrightClosed)

theorem completed_signature_join_decode_eq
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (left right : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel)
    (hleftClosed : SensorSupportClosed sensors left atlas targetDefect root)
    (hrightClosed : SensorSupportClosed sensors right atlas targetDefect root) :
    completedSignatureClosedHull sensors
        (completedSignatureJoin sensors
          (completedClosedContextSignature sensors left atlas targetDefect root)
          (completedClosedContextSignature sensors right atlas targetDefect root)
          atlas targetDefect root)
        atlas targetDefect root =
      closedContextJoin sensors left right atlas targetDefect root := by
  unfold completedSignatureJoin
  rw [completed_signature_closed_hull_encode_eq sensors left
      atlas targetDefect root hleftClosed,
    completed_signature_closed_hull_encode_eq sensors right
      atlas targetDefect root hrightClosed]
  exact completed_signature_closed_hull_encode_eq sensors
    (closedContextJoin sensors left right atlas targetDefect root)
    atlas targetDefect root
    (closed_context_join_closed sensors left right atlas targetDefect root)

def completedSignatureTop {ι : Type*} : Finset (Finset ι) := ∅

noncomputable def completedSignatureBottom
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) : Finset (Finset ι) :=
  completedClosedContextSignature sensors
    (sensorSupportClosure sensors (∅ : Finset ι) atlas targetDefect root)
    atlas targetDefect root

theorem completed_signature_top_hull_eq_univ
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    completedSignatureClosedHull sensors
      (completedSignatureTop : Finset (Finset ι))
      atlas targetDefect root = Finset.univ := by
  exact completed_signature_closed_hull_empty sensors atlas targetDefect root

theorem completed_signature_bottom_hull_eq
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    completedSignatureClosedHull sensors
        (completedSignatureBottom sensors atlas targetDefect root)
        atlas targetDefect root =
      sensorSupportClosure sensors (∅ : Finset ι) atlas targetDefect root := by
  exact completed_signature_closed_hull_encode_eq sensors
    (sensorSupportClosure sensors (∅ : Finset ι) atlas targetDefect root)
    atlas targetDefect root
    (sensor_support_closure_closed sensors (∅ : Finset ι)
      atlas targetDefect root)

theorem completed_closed_context_signature_root_independent
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (context : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (sourceRoot targetRoot : RouteLabel) :
    completedClosedContextSignature sensors context atlas targetDefect sourceRoot =
      completedClosedContextSignature sensors context atlas targetDefect targetRoot := by
  classical
  unfold completedClosedContextSignature
  by_cases htop : context = Finset.univ
  · simp [htop]
  · simp only [htop, if_false]
    exact proper_context_minimal_generator_signature_root_independent sensors
      context atlas targetDefect sourceRoot targetRoot

theorem completed_signature_closed_hull_root_independent
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (signature : Finset (Finset ι))
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (sourceRoot targetRoot : RouteLabel) :
    completedSignatureClosedHull sensors signature atlas targetDefect sourceRoot =
      completedSignatureClosedHull sensors signature atlas targetDefect targetRoot := by
  classical
  unfold completedSignatureClosedHull
  by_cases hempty : signature = ∅
  · simp [hempty]
  · simp only [hempty, if_false]
    unfold minimalGeneratorAntichainClosedHull
    exact sensor_support_closure_root_independent sensors
      (minimalGeneratorAntichainEnvelope signature)
      atlas targetDefect sourceRoot targetRoot

structure PointedSignatureLatticeCertificate where
  sourceMemoryOSV095Bound : Bool
  universalContextTopSentinelExact : Bool
  allClosedContextEncodeDecodeExact : Bool
  pointedHullOrderExact : Bool
  binaryMeetUniversalPropertyExact : Bool
  binaryJoinUniversalPropertyExact : Bool
  boundedTopBottomExact : Bool
  rootIndependenceExact : Bool
  representativeChoicePerformed : Bool
  uniqueMinimalGeneratorClaimed : Bool
  completeLatticeTypeclassClaimed : Bool
  arbitraryFamilySupInfClaimed : Bool
  distributivityClaimed : Bool
  modularityClaimed : Bool
  externalOracleAuthorityGranted : Bool
  candidateRankingPerformed : Bool
  executionPermission : Bool
  persistentWorldStateMutated : Bool
  truthAuthorityGranted : Bool

end KUOS.OpenHorizon.MemoryOSPointedSignatureLatticeV0_96
