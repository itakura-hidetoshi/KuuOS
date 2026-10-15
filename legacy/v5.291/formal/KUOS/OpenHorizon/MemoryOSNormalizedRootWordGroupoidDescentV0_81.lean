import Mathlib
import KUOS.OpenHorizon.MemoryOSAllRootChartDefectAwareWordTransportV0_80

namespace KUOS.OpenHorizon.MemoryOSNormalizedRootWordGroupoidDescentV0_81

open KUOS.OpenHorizon.MemoryOSNonAbelianWilsonLoopV0_72
open KUOS.OpenHorizon.MemoryOSRootedRouteAtlasNielsenChangeV0_78
open KUOS.OpenHorizon.MemoryOSFreeGroupMixedWilsonWordV0_79
open KUOS.OpenHorizon.MemoryOSAllRootChartDefectAwareWordTransportV0_80

/-- Three route slots remain after deleting the selected root coordinate. -/
inductive NormalizedRouteSlot
  | first
  | second
  | third
deriving DecidableEq, Repr, Fintype

/-- Four generators in a normalized root chart: three route slots and one defect. -/
inductive NormalizedRootWordGenerator
  | route (slot : NormalizedRouteSlot)
  | defect
deriving DecidableEq, Repr

/-- Ordered complement of the selected root route. -/
def slotRoute : RouteLabel → NormalizedRouteSlot → RouteLabel
  | .route0, .first => .route1
  | .route0, .second => .route2
  | .route0, .third => .route3
  | .route1, .first => .route0
  | .route1, .second => .route2
  | .route1, .third => .route3
  | .route2, .first => .route0
  | .route2, .second => .route1
  | .route2, .third => .route3
  | .route3, .first => .route0
  | .route3, .second => .route1
  | .route3, .third => .route2

/-- Word representing any physical route coordinate in a normalized chart. -/
def normalizedCoordinateWord
    (root route : RouteLabel) : FreeGroup NormalizedRootWordGenerator :=
  match root, route with
  | .route0, .route0 => 1
  | .route0, .route1 => FreeGroup.of (.route .first)
  | .route0, .route2 => FreeGroup.of (.route .second)
  | .route0, .route3 => FreeGroup.of (.route .third)
  | .route1, .route0 => FreeGroup.of (.route .first)
  | .route1, .route1 => 1
  | .route1, .route2 => FreeGroup.of (.route .second)
  | .route1, .route3 => FreeGroup.of (.route .third)
  | .route2, .route0 => FreeGroup.of (.route .first)
  | .route2, .route1 => FreeGroup.of (.route .second)
  | .route2, .route2 => 1
  | .route2, .route3 => FreeGroup.of (.route .third)
  | .route3, .route0 => FreeGroup.of (.route .first)
  | .route3, .route1 => FreeGroup.of (.route .second)
  | .route3, .route2 => FreeGroup.of (.route .third)
  | .route3, .route3 => 1

/-- Generator assignment of a normalized word chart. -/
def normalizedRootWordAssignment {G : Type*}
    (chart : RootChart G) (root : RouteLabel) :
    NormalizedRootWordGenerator → G
  | .route slot => chart.coordinate (slotRoute root slot)
  | .defect => chart.defect

/-- Universal evaluation of normalized root-chart words. -/
def evalNormalizedRootWord {G : Type*} [Group G]
    (chart : RootChart G) (root : RouteLabel) :
    FreeGroup NormalizedRootWordGenerator →* G :=
  FreeGroup.lift (normalizedRootWordAssignment chart root)

@[simp] theorem eval_normalized_root_word_generator
    {G : Type*} [Group G]
    (chart : RootChart G) (root : RouteLabel)
    (generator : NormalizedRootWordGenerator) :
    evalNormalizedRootWord chart root (FreeGroup.of generator) =
      normalizedRootWordAssignment chart root generator := by
  simp [evalNormalizedRootWord]

/-- Normalization makes the deleted root coordinate evaluate as identity. -/
theorem eval_normalized_coordinate_word_of_normalized
    {G : Type*} [Group G]
    (chart : RootChart G) (root route : RouteLabel)
    (h : chart.NormalizedAt root) :
    evalNormalizedRootWord chart root (normalizedCoordinateWord root route) =
      chart.coordinate route := by
  cases root <;> cases route <;>
    simp_all [normalizedCoordinateWord, evalNormalizedRootWord,
      normalizedRootWordAssignment, slotRoute, RootChart.NormalizedAt]

/-- Defect-aware substitution from a target normalized chart to a source chart. -/
def normalizedTransitionGenerator
    (sourceRoot targetRoot : RouteLabel) :
    NormalizedRootWordGenerator → FreeGroup NormalizedRootWordGenerator
  | .route slot =>
      (normalizedCoordinateWord sourceRoot targetRoot)⁻¹ *
        normalizedCoordinateWord sourceRoot (slotRoute targetRoot slot)
  | .defect =>
      (normalizedCoordinateWord sourceRoot targetRoot)⁻¹ *
        FreeGroup.of .defect *
        normalizedCoordinateWord sourceRoot targetRoot

/-- Pair-groupoid transport homomorphism on normalized free words. -/
def normalizedTransitionHom
    (sourceRoot targetRoot : RouteLabel) :
    FreeGroup NormalizedRootWordGenerator →*
      FreeGroup NormalizedRootWordGenerator :=
  FreeGroup.lift (normalizedTransitionGenerator sourceRoot targetRoot)

@[simp] theorem normalized_transition_hom_generator
    (sourceRoot targetRoot : RouteLabel)
    (generator : NormalizedRootWordGenerator) :
    normalizedTransitionHom sourceRoot targetRoot (FreeGroup.of generator) =
      normalizedTransitionGenerator sourceRoot targetRoot generator := by
  simp [normalizedTransitionHom]

/-- Coordinate words obey the exact pair-groupoid transition law. -/
@[simp] theorem normalized_transition_coordinate_word
    (sourceRoot targetRoot route : RouteLabel) :
    normalizedTransitionHom sourceRoot targetRoot
        (normalizedCoordinateWord targetRoot route) =
      (normalizedCoordinateWord sourceRoot targetRoot)⁻¹ *
        normalizedCoordinateWord sourceRoot route := by
  cases sourceRoot <;> cases targetRoot <;> cases route <;>
    simp [normalizedTransitionHom, normalizedTransitionGenerator,
      normalizedCoordinateWord, slotRoute] <;> group

/-- Every root has an identity transport. -/
theorem normalized_transition_hom_identity (root : RouteLabel) :
    normalizedTransitionHom root root =
      MonoidHom.id (FreeGroup NormalizedRootWordGenerator) := by
  apply FreeGroup.ext_hom
  intro generator
  cases generator with
  | route slot =>
      cases root <;> cases slot <;>
        simp [normalizedTransitionHom, normalizedTransitionGenerator,
          normalizedCoordinateWord, slotRoute]
  | defect =>
      cases root <;>
        simp [normalizedTransitionHom, normalizedTransitionGenerator,
          normalizedCoordinateWord]

/-- Composition through an intermediate root equals direct transport. -/
theorem normalized_transition_hom_comp
    (sourceRoot middleRoot targetRoot : RouteLabel) :
    (normalizedTransitionHom sourceRoot middleRoot).comp
        (normalizedTransitionHom middleRoot targetRoot) =
      normalizedTransitionHom sourceRoot targetRoot := by
  apply FreeGroup.ext_hom
  intro generator
  cases generator with
  | route slot =>
      simp [normalizedTransitionHom, normalizedTransitionGenerator]
      group
  | defect =>
      simp [normalizedTransitionHom, normalizedTransitionGenerator]
      group

/-- Pointwise composition law for every normalized word. -/
theorem normalized_transition_word_comp
    (sourceRoot middleRoot targetRoot : RouteLabel)
    (word : FreeGroup NormalizedRootWordGenerator) :
    normalizedTransitionHom sourceRoot middleRoot
        (normalizedTransitionHom middleRoot targetRoot word) =
      normalizedTransitionHom sourceRoot targetRoot word := by
  exact DFunLike.congr_fun
    (normalized_transition_hom_comp sourceRoot middleRoot targetRoot) word

/-- Reversing a root transition is its two-sided inverse. -/
theorem normalized_transition_hom_inverse
    (sourceRoot targetRoot : RouteLabel) :
    (normalizedTransitionHom sourceRoot targetRoot).comp
        (normalizedTransitionHom targetRoot sourceRoot) =
      MonoidHom.id (FreeGroup NormalizedRootWordGenerator) := by
  rw [normalized_transition_hom_comp]
  exact normalized_transition_hom_identity sourceRoot

/-- Pointwise round-trip identity. -/
theorem normalized_transition_word_round_trip
    (sourceRoot targetRoot : RouteLabel)
    (word : FreeGroup NormalizedRootWordGenerator) :
    normalizedTransitionHom sourceRoot targetRoot
        (normalizedTransitionHom targetRoot sourceRoot word) = word := by
  have h := DFunLike.congr_fun
    (normalized_transition_hom_inverse sourceRoot targetRoot) word
  exact h

/-- Evaluation commutes with normalized chart transport. -/
theorem normalized_transition_evaluation_compatibility
    {G : Type*} [Group G]
    (chart : RootChart G) (sourceRoot targetRoot : RouteLabel)
    (h : chart.NormalizedAt sourceRoot)
    (word : FreeGroup NormalizedRootWordGenerator) :
    evalNormalizedRootWord chart sourceRoot
        (normalizedTransitionHom sourceRoot targetRoot word) =
      evalNormalizedRootWord (rebaseRootChart chart targetRoot) targetRoot word := by
  have hhom :
      (evalNormalizedRootWord chart sourceRoot).comp
          (normalizedTransitionHom sourceRoot targetRoot) =
        evalNormalizedRootWord (rebaseRootChart chart targetRoot) targetRoot := by
    apply FreeGroup.ext_hom
    intro generator
    cases generator with
    | route slot =>
        simp [normalizedTransitionHom, normalizedTransitionGenerator,
          evalNormalizedRootWord, normalizedRootWordAssignment]
        rw [eval_normalized_coordinate_word_of_normalized chart sourceRoot
            targetRoot h,
          eval_normalized_coordinate_word_of_normalized chart sourceRoot
            (slotRoute targetRoot slot) h]
        rfl
    | defect =>
        simp [normalizedTransitionHom, normalizedTransitionGenerator,
          evalNormalizedRootWord, normalizedRootWordAssignment]
        rw [eval_normalized_coordinate_word_of_normalized chart sourceRoot
            targetRoot h]
        rfl
  exact DFunLike.congr_fun hhom word

/-- Actual atlas charts realize exact pair-groupoid descent. -/
theorem normalized_atlas_word_transport_exact
    {G : Type*} [Group G]
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (sourceRoot targetRoot : RouteLabel)
    (word : FreeGroup NormalizedRootWordGenerator) :
    evalNormalizedRootWord (atlasRootChart atlas targetDefect sourceRoot)
        sourceRoot (normalizedTransitionHom sourceRoot targetRoot word) =
      evalNormalizedRootWord (atlasRootChart atlas targetDefect targetRoot)
        targetRoot word := by
  rw [normalized_transition_evaluation_compatibility
    (atlasRootChart atlas targetDefect sourceRoot) sourceRoot targetRoot
    (atlas_root_chart_normalized atlas targetDefect sourceRoot)]
  rw [atlas_root_chart_rebase_exact]

/-- Evaluation is independent of an intermediate transport root. -/
theorem normalized_atlas_word_transport_path_independent
    {G : Type*} [Group G]
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (sourceRoot middleRoot targetRoot : RouteLabel)
    (word : FreeGroup NormalizedRootWordGenerator) :
    evalNormalizedRootWord (atlasRootChart atlas targetDefect sourceRoot)
        sourceRoot
        (normalizedTransitionHom sourceRoot middleRoot
          (normalizedTransitionHom middleRoot targetRoot word)) =
      evalNormalizedRootWord (atlasRootChart atlas targetDefect sourceRoot)
        sourceRoot (normalizedTransitionHom sourceRoot targetRoot word) := by
  rw [normalized_transition_word_comp]

/-- Normalized word evaluation is covariant under common root conjugation. -/
theorem normalized_root_word_evaluation_conjugation_covariant
    {G : Type*} [Group G]
    (chart : RootChart G) (root : RouteLabel) (frame : G)
    (word : FreeGroup NormalizedRootWordGenerator) :
    evalNormalizedRootWord (conjugateRootChart frame chart) root word =
      frame⁻¹ * evalNormalizedRootWord chart root word * frame := by
  have hhom :
      evalNormalizedRootWord (conjugateRootChart frame chart) root =
        (conjugationHom frame).comp (evalNormalizedRootWord chart root) := by
    apply FreeGroup.ext_hom
    intro generator
    cases generator with
    | route slot =>
        simp [evalNormalizedRootWord, normalizedRootWordAssignment,
          conjugateRootChart, conjugationHom]
    | defect =>
        simp [evalNormalizedRootWord, normalizedRootWordAssignment,
          conjugateRootChart, conjugationHom]
  calc
    evalNormalizedRootWord (conjugateRootChart frame chart) root word =
        ((conjugationHom frame).comp
          (evalNormalizedRootWord chart root)) word := by rw [hhom]
    _ = frame⁻¹ * evalNormalizedRootWord chart root word * frame := rfl

/-- Class-function Wilson evaluation of a normalized word. -/
def normalizedRootWordWilson {G : Type*} [Group G] {R : Type*}
    (χ : ClassFunction G R) (chart : RootChart G) (root : RouteLabel)
    (word : FreeGroup NormalizedRootWordGenerator) : R :=
  χ.toFun (evalNormalizedRootWord chart root word)

/-- Every normalized-word Wilson observable is gauge invariant. -/
theorem normalized_root_word_wilson_gauge_invariant
    {G : Type*} [Group G] {R : Type*}
    (χ : ClassFunction G R) (chart : RootChart G) (root : RouteLabel)
    (frame : G) (word : FreeGroup NormalizedRootWordGenerator) :
    normalizedRootWordWilson χ (conjugateRootChart frame chart) root word =
      normalizedRootWordWilson χ chart root word := by
  unfold normalizedRootWordWilson
  rw [normalized_root_word_evaluation_conjugation_covariant]
  simpa using χ.conjugationInvariant frame
    (evalNormalizedRootWord chart root word)

/-- Wilson descent is exact between every pair of atlas roots. -/
theorem normalized_atlas_word_wilson_transport_exact
    {G : Type*} [Group G] {R : Type*}
    (χ : ClassFunction G R)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (sourceRoot targetRoot : RouteLabel)
    (word : FreeGroup NormalizedRootWordGenerator) :
    normalizedRootWordWilson χ (atlasRootChart atlas targetDefect sourceRoot)
        sourceRoot (normalizedTransitionHom sourceRoot targetRoot word) =
      normalizedRootWordWilson χ (atlasRootChart atlas targetDefect targetRoot)
        targetRoot word := by
  unfold normalizedRootWordWilson
  rw [normalized_atlas_word_transport_exact]

/-- Mixed route-slot / defect word in a normalized chart. -/
def normalizedRouteDefectWord (slot : NormalizedRouteSlot) :
    FreeGroup NormalizedRootWordGenerator :=
  FreeGroup.of (.route slot) * FreeGroup.of .defect

@[simp] theorem eval_normalized_route_defect_word
    {G : Type*} [Group G]
    (chart : RootChart G) (root : RouteLabel) (slot : NormalizedRouteSlot) :
    evalNormalizedRootWord chart root (normalizedRouteDefectWord slot) =
      chart.coordinate (slotRoute root slot) * chart.defect := by
  simp [normalizedRouteDefectWord, evalNormalizedRootWord,
    normalizedRootWordAssignment]

/-- The route-0 third-slot word is exactly the v0.80 route-3 mixed word. -/
theorem normalized_route0_third_defect_matches_v080
    {G : Type*} [Group G]
    (atlas : DualFourRouteAtlas G) (targetDefect : G) :
    evalNormalizedRootWord (atlasRootChart atlas targetDefect .route0)
        .route0 (normalizedRouteDefectWord .third) =
      evalRootChartWord (atlasRootChart atlas targetDefect .route0)
        (routeDefectWord .route3) := by
  simp [normalizedRouteDefectWord, evalNormalizedRootWord,
    normalizedRootWordAssignment, slotRoute, routeDefectWord,
    evalRootChartWord, rootChartWordAssignment]

/-- Ordered-AB separator value descends from every normalized source root. -/
theorem canonical_ordered_ab_normalized_groupoid_mixed_wilson
    (sourceRoot : RouteLabel) :
    normalizedRootWordWilson (identityWilsonClass S3)
        (atlasRootChart orderedABAtlas atlasTargetDefect sourceRoot)
        sourceRoot
        (normalizedTransitionHom sourceRoot .route0
          (normalizedRouteDefectWord .third)) = 3 := by
  rw [normalized_atlas_word_wilson_transport_exact]
  native_decide

/-- Ordered-BA separator value descends from every normalized source root. -/
theorem canonical_ordered_ba_normalized_groupoid_mixed_wilson
    (sourceRoot : RouteLabel) :
    normalizedRootWordWilson (identityWilsonClass S3)
        (atlasRootChart orderedBAAtlas atlasTargetDefect sourceRoot)
        sourceRoot
        (normalizedTransitionHom sourceRoot .route0
          (normalizedRouteDefectWord .third)) = 0 := by
  rw [normalized_atlas_word_wilson_transport_exact]
  native_decide

/-- The canonical mixed Wilson word separates the mirrored profiles in every chart. -/
theorem canonical_normalized_groupoid_mixed_wilson_separates
    (sourceRoot : RouteLabel) :
    normalizedRootWordWilson (identityWilsonClass S3)
        (atlasRootChart orderedABAtlas atlasTargetDefect sourceRoot)
        sourceRoot
        (normalizedTransitionHom sourceRoot .route0
          (normalizedRouteDefectWord .third)) ≠
      normalizedRootWordWilson (identityWilsonClass S3)
        (atlasRootChart orderedBAAtlas atlasTargetDefect sourceRoot)
        sourceRoot
        (normalizedTransitionHom sourceRoot .route0
          (normalizedRouteDefectWord .third)) := by
  rw [canonical_ordered_ab_normalized_groupoid_mixed_wilson,
    canonical_ordered_ba_normalized_groupoid_mixed_wilson]
  norm_num

/-- Finite formal authority boundary of the v0.81 certificate. -/
structure NormalizedRootWordGroupoidDescentCertificate where
  sourceMemoryOSV080Bound : Bool
  selfCoordinateEliminationExact : Bool
  pairGroupoidIdentityExact : Bool
  pairGroupoidCompositionExact : Bool
  pairGroupoidInverseExact : Bool
  normalizedWordDescentExact : Bool
  normalizedWilsonDescentExact : Bool
  continuumGaugeGroupoidClaimed : Bool
  candidateRankingPerformed : Bool
  executionPermission : Bool
  persistentWorldStateMutated : Bool
  truthAuthorityGranted : Bool

end KUOS.OpenHorizon.MemoryOSNormalizedRootWordGroupoidDescentV0_81
