import Mathlib
import KUOS.OpenHorizon.MemoryOSPointedSignatureLatticeV0_96

namespace KUOS.OpenHorizon.MemoryOSFiniteFamilySignatureLatticeV0_97

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

noncomputable def closedContextFiniteMeet
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    (family : Finset (Finset ι)) : Finset ι := by
  classical
  exact Finset.univ.filter fun i =>
    ∀ context ∈ family, i ∈ context

noncomputable def closedContextFiniteUnion
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    (family : Finset (Finset ι)) : Finset ι := by
  classical
  exact Finset.univ.filter fun i =>
    ∃ context ∈ family, i ∈ context

noncomputable def closedContextFiniteJoin
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (family : Finset (Finset ι))
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) : Finset ι :=
  sensorSupportClosure sensors (closedContextFiniteUnion family)
    atlas targetDefect root

noncomputable def decodedCompletedSignatureFamily
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (signatures : Finset (Finset (Finset ι)))
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) : Finset (Finset ι) := by
  classical
  exact signatures.image fun signature =>
    completedSignatureClosedHull sensors signature atlas targetDefect root

noncomputable def completedSignatureFiniteMeet
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (signatures : Finset (Finset (Finset ι)))
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) : Finset (Finset ι) :=
  completedClosedContextSignature sensors
    (closedContextFiniteMeet
      (decodedCompletedSignatureFamily sensors signatures
        atlas targetDefect root))
    atlas targetDefect root

noncomputable def completedSignatureFiniteJoin
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (signatures : Finset (Finset (Finset ι)))
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) : Finset (Finset ι) :=
  completedClosedContextSignature sensors
    (closedContextFiniteJoin sensors
      (decodedCompletedSignatureFamily sensors signatures
        atlas targetDefect root)
      atlas targetDefect root)
    atlas targetDefect root

theorem mem_closed_context_finite_meet_iff
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    (family : Finset (Finset ι)) (i : ι) :
    i ∈ closedContextFiniteMeet family ↔
      ∀ context ∈ family, i ∈ context := by
  classical
  simp [closedContextFiniteMeet]

theorem mem_closed_context_finite_union_iff
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    (family : Finset (Finset ι)) (i : ι) :
    i ∈ closedContextFiniteUnion family ↔
      ∃ context ∈ family, i ∈ context := by
  classical
  simp [closedContextFiniteUnion]

theorem closed_context_finite_meet_empty
    {ι : Type*} [Fintype ι] [DecidableEq ι] :
    closedContextFiniteMeet (∅ : Finset (Finset ι)) = Finset.univ := by
  classical
  ext i
  simp [closedContextFiniteMeet]

theorem closed_context_finite_union_empty
    {ι : Type*} [Fintype ι] [DecidableEq ι] :
    closedContextFiniteUnion (∅ : Finset (Finset ι)) = ∅ := by
  classical
  ext i
  simp [closedContextFiniteUnion]

theorem closed_context_finite_meet_singleton
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    (context : Finset ι) :
    closedContextFiniteMeet ({context} : Finset (Finset ι)) = context := by
  classical
  ext i
  simp [closedContextFiniteMeet]

theorem closed_context_finite_union_singleton
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    (context : Finset ι) :
    closedContextFiniteUnion ({context} : Finset (Finset ι)) = context := by
  classical
  ext i
  simp [closedContextFiniteUnion]

theorem closed_context_finite_meet_closed
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (family : Finset (Finset ι))
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel)
    (hclosed :
      ∀ context ∈ family,
        SensorSupportClosed sensors context atlas targetDefect root) :
    SensorSupportClosed sensors (closedContextFiniteMeet family)
      atlas targetDefect root := by
  unfold SensorSupportClosed
  apply Finset.Subset.antisymm
  · intro i hi
    rw [mem_closed_context_finite_meet_iff]
    intro context hcontext
    have hsubset :
        closedContextFiniteMeet family ⊆ context := by
      intro j hj
      exact
        (mem_closed_context_finite_meet_iff family j).1 hj
          context hcontext
    have hmono :=
      sensor_support_closure_mono sensors hsubset atlas targetDefect root
    have hiContext := hmono hi
    rw [hclosed context hcontext] at hiContext
    exact hiContext
  · exact sensor_support_subset_closure sensors
      (closedContextFiniteMeet family) atlas targetDefect root

theorem closed_context_finite_join_closed
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (family : Finset (Finset ι))
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    SensorSupportClosed sensors
      (closedContextFiniteJoin sensors family atlas targetDefect root)
      atlas targetDefect root := by
  exact sensor_support_closure_closed sensors
    (closedContextFiniteUnion family) atlas targetDefect root

theorem closed_context_finite_meet_universal
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    (lower : Finset ι) (family : Finset (Finset ι)) :
    lower ⊆ closedContextFiniteMeet family ↔
      ∀ context ∈ family, lower ⊆ context := by
  constructor
  · intro hlower context hcontext i hi
    exact
      (mem_closed_context_finite_meet_iff family i).1
        (hlower hi) context hcontext
  · intro hall i hi
    exact
      (mem_closed_context_finite_meet_iff family i).2
        (fun context hcontext => hall context hcontext hi)

theorem closed_context_finite_join_universal
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (family : Finset (Finset ι))
    (upper : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel)
    (hupperClosed :
      SensorSupportClosed sensors upper atlas targetDefect root) :
    closedContextFiniteJoin sensors family atlas targetDefect root ⊆ upper ↔
      ∀ context ∈ family, context ⊆ upper := by
  constructor
  · intro hjoin context hcontext i hi
    apply hjoin
    apply sensor_support_subset_closure sensors
      (closedContextFiniteUnion family) atlas targetDefect root
    exact
      (mem_closed_context_finite_union_iff family i).2
        ⟨context, hcontext, hi⟩
  · intro hall
    have hunion : closedContextFiniteUnion family ⊆ upper := by
      intro i hi
      obtain ⟨context, hcontext, hiContext⟩ :=
        (mem_closed_context_finite_union_iff family i).1 hi
      exact hall context hcontext hiContext
    have hmono :=
      sensor_support_closure_mono sensors hunion atlas targetDefect root
    rw [hupperClosed] at hmono
    exact hmono

theorem closed_context_finite_join_empty
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    closedContextFiniteJoin sensors (∅ : Finset (Finset ι))
      atlas targetDefect root =
      sensorSupportClosure sensors (∅ : Finset ι)
        atlas targetDefect root := by
  unfold closedContextFiniteJoin
  rw [closed_context_finite_union_empty]

theorem closed_context_finite_join_singleton
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (context : Finset ι)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel)
    (hclosed :
      SensorSupportClosed sensors context atlas targetDefect root) :
    closedContextFiniteJoin sensors ({context} : Finset (Finset ι))
      atlas targetDefect root = context := by
  unfold closedContextFiniteJoin
  rw [closed_context_finite_union_singleton, hclosed]

theorem sensor_support_univ_closed
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    SensorSupportClosed sensors (Finset.univ : Finset ι)
      atlas targetDefect root := by
  unfold SensorSupportClosed
  apply Finset.Subset.antisymm
  · exact Finset.subset_univ _
  · exact sensor_support_subset_closure sensors
      (Finset.univ : Finset ι) atlas targetDefect root

theorem completed_signature_closed_hull_closed
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (signature : Finset (Finset ι))
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    SensorSupportClosed sensors
      (completedSignatureClosedHull sensors signature atlas targetDefect root)
      atlas targetDefect root := by
  classical
  by_cases hempty : signature = ∅
  · rw [hempty, completed_signature_closed_hull_empty]
    exact sensor_support_univ_closed sensors atlas targetDefect root
  · unfold completedSignatureClosedHull
    rw [if_neg hempty]
    unfold minimalGeneratorAntichainClosedHull
    exact sensor_support_closure_closed sensors
      (minimalGeneratorAntichainEnvelope signature)
      atlas targetDefect root

theorem decoded_completed_signature_family_closed
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (signatures : Finset (Finset (Finset ι)))
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    ∀ context ∈ decodedCompletedSignatureFamily sensors signatures
        atlas targetDefect root,
      SensorSupportClosed sensors context atlas targetDefect root := by
  classical
  intro context hcontext
  rw [decodedCompletedSignatureFamily, Finset.mem_image] at hcontext
  obtain ⟨signature, hsignature, rfl⟩ := hcontext
  exact completed_signature_closed_hull_closed sensors signature
    atlas targetDefect root

theorem completed_signature_finite_meet_decode_eq
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (signatures : Finset (Finset (Finset ι)))
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    completedSignatureClosedHull sensors
        (completedSignatureFiniteMeet sensors signatures
          atlas targetDefect root)
        atlas targetDefect root =
      closedContextFiniteMeet
        (decodedCompletedSignatureFamily sensors signatures
          atlas targetDefect root) := by
  unfold completedSignatureFiniteMeet
  exact completed_signature_closed_hull_encode_eq sensors
    (closedContextFiniteMeet
      (decodedCompletedSignatureFamily sensors signatures
        atlas targetDefect root))
    atlas targetDefect root
    (closed_context_finite_meet_closed sensors
      (decodedCompletedSignatureFamily sensors signatures
        atlas targetDefect root)
      atlas targetDefect root
      (decoded_completed_signature_family_closed sensors signatures
        atlas targetDefect root))

theorem completed_signature_finite_join_decode_eq
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (signatures : Finset (Finset (Finset ι)))
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    completedSignatureClosedHull sensors
        (completedSignatureFiniteJoin sensors signatures
          atlas targetDefect root)
        atlas targetDefect root =
      closedContextFiniteJoin sensors
        (decodedCompletedSignatureFamily sensors signatures
          atlas targetDefect root)
        atlas targetDefect root := by
  unfold completedSignatureFiniteJoin
  exact completed_signature_closed_hull_encode_eq sensors
    (closedContextFiniteJoin sensors
      (decodedCompletedSignatureFamily sensors signatures
        atlas targetDefect root)
      atlas targetDefect root)
    atlas targetDefect root
    (closed_context_finite_join_closed sensors
      (decodedCompletedSignatureFamily sensors signatures
        atlas targetDefect root)
      atlas targetDefect root)

theorem completed_signature_finite_meet_universal
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (lower : Finset (Finset ι))
    (signatures : Finset (Finset (Finset ι)))
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    CompletedSignatureHullLe sensors lower
        (completedSignatureFiniteMeet sensors signatures
          atlas targetDefect root)
        atlas targetDefect root ↔
      ∀ signature ∈ signatures,
        CompletedSignatureHullLe sensors lower signature
          atlas targetDefect root := by
  unfold CompletedSignatureHullLe
  rw [completed_signature_finite_meet_decode_eq]
  constructor
  · intro hlower signature hsignature
    have hcontext :
        completedSignatureClosedHull sensors signature atlas targetDefect root ∈
          decodedCompletedSignatureFamily sensors signatures
            atlas targetDefect root := by
      classical
      apply Finset.mem_image.mpr
      exact ⟨signature, hsignature, rfl⟩
    exact
      (closed_context_finite_meet_universal
        (completedSignatureClosedHull sensors lower atlas targetDefect root)
        (decodedCompletedSignatureFamily sensors signatures
          atlas targetDefect root)).1 hlower
        _ hcontext
  · intro hall
    apply
      (closed_context_finite_meet_universal
        (completedSignatureClosedHull sensors lower atlas targetDefect root)
        (decodedCompletedSignatureFamily sensors signatures
          atlas targetDefect root)).2
    intro context hcontext
    classical
    rw [decodedCompletedSignatureFamily, Finset.mem_image] at hcontext
    obtain ⟨signature, hsignature, rfl⟩ := hcontext
    exact hall signature hsignature

theorem completed_signature_finite_join_universal
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (signatures : Finset (Finset (Finset ι)))
    (upper : Finset (Finset ι))
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    CompletedSignatureHullLe sensors
        (completedSignatureFiniteJoin sensors signatures
          atlas targetDefect root)
        upper atlas targetDefect root ↔
      ∀ signature ∈ signatures,
        CompletedSignatureHullLe sensors signature upper
          atlas targetDefect root := by
  unfold CompletedSignatureHullLe
  rw [completed_signature_finite_join_decode_eq]
  have hupperClosed :=
    completed_signature_closed_hull_closed sensors upper
      atlas targetDefect root
  constructor
  · intro hjoin signature hsignature
    have hcontext :
        completedSignatureClosedHull sensors signature atlas targetDefect root ∈
          decodedCompletedSignatureFamily sensors signatures
            atlas targetDefect root := by
      classical
      apply Finset.mem_image.mpr
      exact ⟨signature, hsignature, rfl⟩
    exact
      (closed_context_finite_join_universal sensors
        (decodedCompletedSignatureFamily sensors signatures
          atlas targetDefect root)
        (completedSignatureClosedHull sensors upper atlas targetDefect root)
        atlas targetDefect root hupperClosed).1 hjoin
        _ hcontext
  · intro hall
    apply
      (closed_context_finite_join_universal sensors
        (decodedCompletedSignatureFamily sensors signatures
          atlas targetDefect root)
        (completedSignatureClosedHull sensors upper atlas targetDefect root)
        atlas targetDefect root hupperClosed).2
    intro context hcontext
    classical
    rw [decodedCompletedSignatureFamily, Finset.mem_image] at hcontext
    obtain ⟨signature, hsignature, rfl⟩ := hcontext
    exact hall signature hsignature

theorem completed_signature_finite_meet_empty_decode_eq
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    completedSignatureClosedHull sensors
        (completedSignatureFiniteMeet sensors
          (∅ : Finset (Finset (Finset ι)))
          atlas targetDefect root)
        atlas targetDefect root =
      Finset.univ := by
  rw [completed_signature_finite_meet_decode_eq]
  classical
  simp [decodedCompletedSignatureFamily, closedContextFiniteMeet]

theorem completed_signature_finite_join_empty_decode_eq
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    completedSignatureClosedHull sensors
        (completedSignatureFiniteJoin sensors
          (∅ : Finset (Finset (Finset ι)))
          atlas targetDefect root)
        atlas targetDefect root =
      sensorSupportClosure sensors (∅ : Finset ι)
        atlas targetDefect root := by
  rw [completed_signature_finite_join_decode_eq]
  classical
  simp [decodedCompletedSignatureFamily, closedContextFiniteJoin,
    closedContextFiniteUnion]

theorem decoded_completed_signature_family_root_independent
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (signatures : Finset (Finset (Finset ι)))
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (sourceRoot targetRoot : RouteLabel) :
    decodedCompletedSignatureFamily sensors signatures
        atlas targetDefect sourceRoot =
      decodedCompletedSignatureFamily sensors signatures
        atlas targetDefect targetRoot := by
  classical
  ext context
  constructor
  · intro hcontext
    rw [decodedCompletedSignatureFamily, Finset.mem_image] at hcontext
    obtain ⟨signature, hsignature, hcontextEq⟩ := hcontext
    rw [decodedCompletedSignatureFamily, Finset.mem_image]
    refine ⟨signature, hsignature, ?_⟩
    calc
      completedSignatureClosedHull sensors signature
          atlas targetDefect targetRoot =
        completedSignatureClosedHull sensors signature
          atlas targetDefect sourceRoot :=
        (completed_signature_closed_hull_root_independent sensors signature
          atlas targetDefect targetRoot sourceRoot)
      _ = context := hcontextEq
  · intro hcontext
    rw [decodedCompletedSignatureFamily, Finset.mem_image] at hcontext
    obtain ⟨signature, hsignature, hcontextEq⟩ := hcontext
    rw [decodedCompletedSignatureFamily, Finset.mem_image]
    refine ⟨signature, hsignature, ?_⟩
    calc
      completedSignatureClosedHull sensors signature
          atlas targetDefect sourceRoot =
        completedSignatureClosedHull sensors signature
          atlas targetDefect targetRoot :=
        completed_signature_closed_hull_root_independent sensors signature
          atlas targetDefect sourceRoot targetRoot
      _ = context := hcontextEq

theorem closed_context_finite_join_root_independent
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H) (family : Finset (Finset ι))
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (sourceRoot targetRoot : RouteLabel) :
    closedContextFiniteJoin sensors family atlas targetDefect sourceRoot =
      closedContextFiniteJoin sensors family atlas targetDefect targetRoot := by
  unfold closedContextFiniteJoin
  exact sensor_support_closure_root_independent sensors
    (closedContextFiniteUnion family)
    atlas targetDefect sourceRoot targetRoot

theorem completed_signature_finite_meet_root_independent
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (signatures : Finset (Finset (Finset ι)))
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (sourceRoot targetRoot : RouteLabel) :
    completedSignatureFiniteMeet sensors signatures
        atlas targetDefect sourceRoot =
      completedSignatureFiniteMeet sensors signatures
        atlas targetDefect targetRoot := by
  unfold completedSignatureFiniteMeet
  rw [decoded_completed_signature_family_root_independent sensors signatures
    atlas targetDefect sourceRoot targetRoot]
  exact completed_closed_context_signature_root_independent sensors
    (closedContextFiniteMeet
      (decodedCompletedSignatureFamily sensors signatures
        atlas targetDefect targetRoot))
    atlas targetDefect sourceRoot targetRoot

theorem completed_signature_finite_join_root_independent
    {ι G H : Type*}
    [Fintype ι] [DecidableEq ι] [Group G] [Group H]
    (sensors : ι → G →* H)
    (signatures : Finset (Finset (Finset ι)))
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (sourceRoot targetRoot : RouteLabel) :
    completedSignatureFiniteJoin sensors signatures
        atlas targetDefect sourceRoot =
      completedSignatureFiniteJoin sensors signatures
        atlas targetDefect targetRoot := by
  unfold completedSignatureFiniteJoin
  have hdecoded :=
    decoded_completed_signature_family_root_independent sensors signatures
      atlas targetDefect sourceRoot targetRoot
  have hjoin :
      closedContextFiniteJoin sensors
          (decodedCompletedSignatureFamily sensors signatures
            atlas targetDefect sourceRoot)
          atlas targetDefect sourceRoot =
        closedContextFiniteJoin sensors
          (decodedCompletedSignatureFamily sensors signatures
            atlas targetDefect targetRoot)
          atlas targetDefect targetRoot := by
    rw [hdecoded]
    exact closed_context_finite_join_root_independent sensors
      (decodedCompletedSignatureFamily sensors signatures
        atlas targetDefect targetRoot)
      atlas targetDefect sourceRoot targetRoot
  rw [hjoin]
  exact completed_closed_context_signature_root_independent sensors
    (closedContextFiniteJoin sensors
      (decodedCompletedSignatureFamily sensors signatures
        atlas targetDefect targetRoot)
      atlas targetDefect targetRoot)
    atlas targetDefect sourceRoot targetRoot

structure FiniteFamilySignatureLatticeCertificate where
  sourceMemoryOSV096Bound : Bool
  finiteContextMeetExact : Bool
  finiteContextJoinExact : Bool
  emptyFamilyBoundsExact : Bool
  finiteMeetUniversalPropertyExact : Bool
  finiteJoinUniversalPropertyExact : Bool
  pointedSignatureFiniteOperationsExact : Bool
  enumerationAndDuplicateInvarianceExact : Bool
  rootIndependenceExact : Bool
  representativeChoicePerformed : Bool
  uniqueMinimalGeneratorClaimed : Bool
  completeLatticeTypeclassClaimed : Bool
  arbitrarySetIndexedSupInfClaimed : Bool
  distributivityClaimed : Bool
  modularityClaimed : Bool
  externalOracleAuthorityGranted : Bool
  candidateRankingPerformed : Bool
  executionPermission : Bool
  persistentWorldStateMutated : Bool
  truthAuthorityGranted : Bool

end KUOS.OpenHorizon.MemoryOSFiniteFamilySignatureLatticeV0_97
