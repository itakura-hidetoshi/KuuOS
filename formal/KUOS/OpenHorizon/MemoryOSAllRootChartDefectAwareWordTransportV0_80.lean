import Mathlib
import KUOS.OpenHorizon.MemoryOSFreeGroupMixedWilsonWordV0_79

namespace KUOS.OpenHorizon.MemoryOSAllRootChartDefectAwareWordTransportV0_80

open KUOS.OpenHorizon.MemoryOSNonAbelianWilsonLoopV0_72
open KUOS.OpenHorizon.MemoryOSRootedRouteAtlasNielsenChangeV0_78
open KUOS.OpenHorizon.MemoryOSFreeGroupMixedWilsonWordV0_79

/-- The four routes of the finite dual atlas. -/
inductive RouteLabel
  | route0
  | route1
  | route2
  | route3
deriving DecidableEq, Repr, Fintype

/-- Exact path transport selected by a route label. -/
def routePath {G : Type*} [Group G]
    (atlas : DualFourRouteAtlas G) : RouteLabel → G
  | .route0 => path0 atlas
  | .route1 => path1 atlas
  | .route2 => path2 atlas
  | .route3 => path3 atlas

/-- Every route path has the same endpoint-covariant gauge law. -/
theorem route_path_gauge_covariant
    {G : Type*} [Group G]
    (atlas : DualFourRouteAtlas G) (frame : FourRouteGaugeFrame G)
    (route : RouteLabel) :
    routePath (gaugeTransformAtlas atlas frame) route =
      frame.g0⁻¹ * routePath atlas route * frame.g5 := by
  cases route
  · exact path0_gauge_covariant atlas frame
  · exact path1_gauge_covariant atlas frame
  · exact path2_gauge_covariant atlas frame
  · exact path3_gauge_covariant atlas frame

/-- A root chart retains all four route coordinates and the root-localized target defect. -/
structure RootChart (G : Type*) where
  coordinate : RouteLabel → G
  defect : G

/-- The exact chart based at any selected route. -/
def atlasRootChart {G : Type*} [Group G]
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) : RootChart G :=
  {
    coordinate := fun route =>
      routeCycle (routePath atlas root) (routePath atlas route)
    defect := localizedDefect (routePath atlas root) targetDefect
  }

/-- A chart is normalized when its selected root coordinate is identity. -/
def RootChart.NormalizedAt {G : Type*} [Group G]
    (chart : RootChart G) (root : RouteLabel) : Prop :=
  chart.coordinate root = 1

/-- Every atlas chart is normalized at its own root. -/
theorem atlas_root_chart_normalized
    {G : Type*} [Group G]
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (root : RouteLabel) :
    (atlasRootChart atlas targetDefect root).NormalizedAt root := by
  simp [RootChart.NormalizedAt, atlasRootChart, routeCycle]

/-- Exact defect-aware change from the current chart to a target root chart. -/
def rebaseRootChart {G : Type*} [Group G]
    (chart : RootChart G) (targetRoot : RouteLabel) : RootChart G :=
  {
    coordinate := fun route =>
      (chart.coordinate targetRoot)⁻¹ * chart.coordinate route
    defect :=
      (chart.coordinate targetRoot)⁻¹ * chart.defect *
        chart.coordinate targetRoot
  }

/-- Rebasing an actual atlas chart gives the direct chart at the new root. -/
theorem atlas_root_chart_rebase_exact
    {G : Type*} [Group G]
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (sourceRoot targetRoot : RouteLabel) :
    rebaseRootChart (atlasRootChart atlas targetDefect sourceRoot) targetRoot =
      atlasRootChart atlas targetDefect targetRoot := by
  apply RootChart.ext
  · funext route
    unfold rebaseRootChart atlasRootChart routeCycle
    group
  · unfold rebaseRootChart atlasRootChart localizedDefect routeCycle
    group

/-- The defect field changes by the target route coordinate conjugation. -/
theorem atlas_root_defect_transition
    {G : Type*} [Group G]
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (sourceRoot targetRoot : RouteLabel) :
    (atlasRootChart atlas targetDefect targetRoot).defect =
      ((atlasRootChart atlas targetDefect sourceRoot).coordinate targetRoot)⁻¹ *
        (atlasRootChart atlas targetDefect sourceRoot).defect *
        (atlasRootChart atlas targetDefect sourceRoot).coordinate targetRoot := by
  unfold atlasRootChart localizedDefect routeCycle
  group

/-- Rebase composition is independent of an intermediate root chart. -/
theorem rebase_root_chart_composition
    {G : Type*} [Group G]
    (chart : RootChart G) (middleRoot targetRoot : RouteLabel) :
    rebaseRootChart (rebaseRootChart chart middleRoot) targetRoot =
      rebaseRootChart chart targetRoot := by
  apply RootChart.ext
  · funext route
    unfold rebaseRootChart
    group
  · unfold rebaseRootChart
    group

/-- Rebasing a normalized chart to its own root is identity. -/
theorem rebase_root_chart_self_of_normalized
    {G : Type*} [Group G]
    (chart : RootChart G) (root : RouteLabel)
    (h : chart.NormalizedAt root) :
    rebaseRootChart chart root = chart := by
  apply RootChart.ext
  · funext route
    change (chart.coordinate root)⁻¹ * chart.coordinate route =
      chart.coordinate route
    rw [h]
    simp
  · change (chart.coordinate root)⁻¹ * chart.defect *
      chart.coordinate root = chart.defect
    rw [h]
    simp

/-- A normalized chart returns exactly after a round trip through any root. -/
theorem rebase_root_chart_round_trip
    {G : Type*} [Group G]
    (chart : RootChart G) (sourceRoot targetRoot : RouteLabel)
    (h : chart.NormalizedAt sourceRoot) :
    rebaseRootChart (rebaseRootChart chart targetRoot) sourceRoot = chart := by
  rw [rebase_root_chart_composition]
  exact rebase_root_chart_self_of_normalized chart sourceRoot h

/-- Simultaneous root-frame conjugation of all chart observables. -/
def conjugateRootChart {G : Type*} [Group G]
    (frame : G) (chart : RootChart G) : RootChart G :=
  {
    coordinate := fun route => frame⁻¹ * chart.coordinate route * frame
    defect := frame⁻¹ * chart.defect * frame
  }

/-- Chart rebasing commutes with simultaneous root-frame conjugation. -/
theorem rebase_root_chart_conjugation_covariant
    {G : Type*} [Group G]
    (frame : G) (chart : RootChart G) (targetRoot : RouteLabel) :
    rebaseRootChart (conjugateRootChart frame chart) targetRoot =
      conjugateRootChart frame (rebaseRootChart chart targetRoot) := by
  apply RootChart.ext
  · funext route
    unfold rebaseRootChart conjugateRootChart
    group
  · unfold rebaseRootChart conjugateRootChart
    group

/-- An atlas root chart transforms by one common root conjugation. -/
theorem atlas_root_chart_gauge_covariant
    {G : Type*} [Group G]
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (frame : FourRouteGaugeFrame G) (root : RouteLabel) :
    atlasRootChart (gaugeTransformAtlas atlas frame)
        (gaugeTransformTargetDefect targetDefect frame) root =
      conjugateRootChart frame.g0 (atlasRootChart atlas targetDefect root) := by
  apply RootChart.ext
  · funext route
    unfold atlasRootChart conjugateRootChart routeCycle
    rw [route_path_gauge_covariant atlas frame root,
      route_path_gauge_covariant atlas frame route]
    group
  · unfold atlasRootChart conjugateRootChart localizedDefect
      gaugeTransformTargetDefect
    rw [route_path_gauge_covariant atlas frame root]
    group

/-- Five generators: four route coordinates and one root-localized defect. -/
inductive RootChartWordGenerator
  | route (label : RouteLabel)
  | defect
deriving DecidableEq, Repr

/-- Generator assignment for an arbitrary root chart. -/
def rootChartWordAssignment {G : Type*}
    (chart : RootChart G) : RootChartWordGenerator → G
  | .route route => chart.coordinate route
  | .defect => chart.defect

/-- Universal evaluation of root-chart words. -/
def evalRootChartWord {G : Type*} [Group G]
    (chart : RootChart G) : FreeGroup RootChartWordGenerator →* G :=
  FreeGroup.lift (rootChartWordAssignment chart)

@[simp] theorem eval_root_chart_word_generator
    {G : Type*} [Group G]
    (chart : RootChart G) (generator : RootChartWordGenerator) :
    evalRootChartWord chart (FreeGroup.of generator) =
      rootChartWordAssignment chart generator := by
  simp [evalRootChartWord]

/-- Word-level transition to a selected root chart, including defect conjugation. -/
def rootTransitionGenerator (targetRoot : RouteLabel) :
    RootChartWordGenerator → FreeGroup RootChartWordGenerator
  | .route route =>
      (FreeGroup.of (.route targetRoot))⁻¹ * FreeGroup.of (.route route)
  | .defect =>
      (FreeGroup.of (.route targetRoot))⁻¹ * FreeGroup.of .defect *
        FreeGroup.of (.route targetRoot)

/-- Universal root transition homomorphism on the free group. -/
def rootTransitionHom (targetRoot : RouteLabel) :
    FreeGroup RootChartWordGenerator →* FreeGroup RootChartWordGenerator :=
  FreeGroup.lift (rootTransitionGenerator targetRoot)

@[simp] theorem root_transition_hom_generator
    (targetRoot : RouteLabel) (generator : RootChartWordGenerator) :
    rootTransitionHom targetRoot (FreeGroup.of generator) =
      rootTransitionGenerator targetRoot generator := by
  simp [rootTransitionHom]

/-- Applying any root transition after another leaves the latter transition unchanged. -/
theorem root_transition_hom_absorbing
    (firstRoot secondRoot : RouteLabel) :
    (rootTransitionHom firstRoot).comp (rootTransitionHom secondRoot) =
      rootTransitionHom secondRoot := by
  apply FreeGroup.ext_hom
  intro generator
  cases generator with
  | route route =>
      simp [rootTransitionHom, rootTransitionGenerator]
      group
  | defect =>
      simp [rootTransitionHom, rootTransitionGenerator]
      group

/-- Pointwise absorption law for all free-group words. -/
theorem root_transition_word_absorbing
    (firstRoot secondRoot : RouteLabel)
    (word : FreeGroup RootChartWordGenerator) :
    rootTransitionHom firstRoot (rootTransitionHom secondRoot word) =
      rootTransitionHom secondRoot word := by
  have h := DFunLike.congr_fun
    (root_transition_hom_absorbing firstRoot secondRoot) word
  exact h

/-- Transition before evaluation equals direct evaluation in the rebased chart. -/
theorem root_transition_evaluation_compatibility
    {G : Type*} [Group G]
    (chart : RootChart G) (targetRoot : RouteLabel)
    (word : FreeGroup RootChartWordGenerator) :
    evalRootChartWord chart (rootTransitionHom targetRoot word) =
      evalRootChartWord (rebaseRootChart chart targetRoot) word := by
  have hhom :
      (evalRootChartWord chart).comp (rootTransitionHom targetRoot) =
        evalRootChartWord (rebaseRootChart chart targetRoot) := by
    apply FreeGroup.ext_hom
    intro generator
    cases generator with
    | route route =>
        simp [evalRootChartWord, rootChartWordAssignment, rootTransitionHom,
          rootTransitionGenerator, rebaseRootChart]
        group
    | defect =>
        simp [evalRootChartWord, rootChartWordAssignment, rootTransitionHom,
          rootTransitionGenerator, rebaseRootChart]
        group
  have h := DFunLike.congr_fun hhom word
  exact h

/-- Word evaluation through an intermediate root equals direct target-root evaluation. -/
theorem root_transition_evaluation_via_intermediate
    {G : Type*} [Group G]
    (chart : RootChart G) (middleRoot targetRoot : RouteLabel)
    (word : FreeGroup RootChartWordGenerator) :
    evalRootChartWord (rebaseRootChart chart middleRoot)
        (rootTransitionHom targetRoot word) =
      evalRootChartWord (rebaseRootChart chart targetRoot) word := by
  rw [← root_transition_evaluation_compatibility chart middleRoot
      (rootTransitionHom targetRoot word)]
  rw [root_transition_word_absorbing]
  exact root_transition_evaluation_compatibility chart targetRoot word

/-- Every root-chart free-group word transforms by simultaneous conjugation. -/
theorem root_chart_word_evaluation_conjugation_covariant
    {G : Type*} [Group G]
    (chart : RootChart G) (frame : G)
    (word : FreeGroup RootChartWordGenerator) :
    evalRootChartWord (conjugateRootChart frame chart) word =
      frame⁻¹ * evalRootChartWord chart word * frame := by
  have hhom :
      evalRootChartWord (conjugateRootChart frame chart) =
        (conjugationHom frame).comp (evalRootChartWord chart) := by
    apply FreeGroup.ext_hom
    intro generator
    cases generator with
    | route route =>
        simp [evalRootChartWord, rootChartWordAssignment,
          conjugateRootChart, conjugationHom]
    | defect =>
        simp [evalRootChartWord, rootChartWordAssignment,
          conjugateRootChart, conjugationHom]
  calc
    evalRootChartWord (conjugateRootChart frame chart) word =
        ((conjugationHom frame).comp (evalRootChartWord chart)) word := by
      rw [hhom]
    _ = frame⁻¹ * evalRootChartWord chart word * frame := rfl

/-- Class-function Wilson evaluation for an arbitrary root-chart word. -/
def rootChartWordWilson {G : Type*} [Group G] {R : Type*}
    (χ : ClassFunction G R) (chart : RootChart G)
    (word : FreeGroup RootChartWordGenerator) : R :=
  χ.toFun (evalRootChartWord chart word)

/-- Every root-chart word Wilson observable is gauge invariant. -/
theorem root_chart_word_wilson_gauge_invariant
    {G : Type*} [Group G] {R : Type*}
    (χ : ClassFunction G R) (chart : RootChart G) (frame : G)
    (word : FreeGroup RootChartWordGenerator) :
    rootChartWordWilson χ (conjugateRootChart frame chart) word =
      rootChartWordWilson χ chart word := by
  unfold rootChartWordWilson
  rw [root_chart_word_evaluation_conjugation_covariant]
  simpa using χ.conjugationInvariant frame (evalRootChartWord chart word)

/-- Transported words evaluate identically from every source root chart. -/
theorem transported_atlas_root_word_exact
    {G : Type*} [Group G]
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (sourceRoot targetRoot : RouteLabel)
    (word : FreeGroup RootChartWordGenerator) :
    evalRootChartWord (atlasRootChart atlas targetDefect sourceRoot)
        (rootTransitionHom targetRoot word) =
      evalRootChartWord (atlasRootChart atlas targetDefect targetRoot) word := by
  rw [root_transition_evaluation_compatibility]
  rw [atlas_root_chart_rebase_exact]

/-- Class-function comparison of a transported word is root independent. -/
theorem transported_atlas_root_word_wilson_exact
    {G : Type*} [Group G] {R : Type*}
    (χ : ClassFunction G R)
    (atlas : DualFourRouteAtlas G) (targetDefect : G)
    (sourceRoot targetRoot : RouteLabel)
    (word : FreeGroup RootChartWordGenerator) :
    rootChartWordWilson χ (atlasRootChart atlas targetDefect sourceRoot)
        (rootTransitionHom targetRoot word) =
      rootChartWordWilson χ (atlasRootChart atlas targetDefect targetRoot)
        word := by
  unfold rootChartWordWilson
  rw [transported_atlas_root_word_exact]

/-- Mixed route-coordinate / root-defect word. -/
def routeDefectWord (route : RouteLabel) :
    FreeGroup RootChartWordGenerator :=
  FreeGroup.of (.route route) * FreeGroup.of .defect

@[simp] theorem eval_route_defect_word
    {G : Type*} [Group G]
    (chart : RootChart G) (route : RouteLabel) :
    evalRootChartWord chart (routeDefectWord route) =
      chart.coordinate route * chart.defect := by
  simp [routeDefectWord, evalRootChartWord, rootChartWordAssignment]

/-- The route-0 chart representation reproduces the v0.79 mixed word. -/
theorem route0_chart_cycle03_defect_matches_v079
    {G : Type*} [Group G]
    (atlas : DualFourRouteAtlas G) (targetDefect : G) :
    evalRootChartWord (atlasRootChart atlas targetDefect .route0)
        (routeDefectWord .route3) =
      evalAtlasWord atlas targetDefect cycle03DefectWord := by
  rw [eval_route_defect_word, eval_cycle03_defect_word]
  rfl

/-- The v0.79 separator value is recovered from every ordered-AB source root. -/
theorem canonical_ordered_ab_all_root_mixed_wilson
    (sourceRoot : RouteLabel) :
    rootChartWordWilson (identityWilsonClass S3)
        (atlasRootChart orderedABAtlas atlasTargetDefect sourceRoot)
        (rootTransitionHom .route0 (routeDefectWord .route3)) = 3 := by
  rw [transported_atlas_root_word_wilson_exact]
  native_decide

/-- The v0.79 separator value is recovered from every ordered-BA source root. -/
theorem canonical_ordered_ba_all_root_mixed_wilson
    (sourceRoot : RouteLabel) :
    rootChartWordWilson (identityWilsonClass S3)
        (atlasRootChart orderedBAAtlas atlasTargetDefect sourceRoot)
        (rootTransitionHom .route0 (routeDefectWord .route3)) = 0 := by
  rw [transported_atlas_root_word_wilson_exact]
  native_decide

/-- The mixed Wilson word separates the mirrored profiles from every source root. -/
theorem canonical_all_root_mixed_wilson_separates
    (sourceRoot : RouteLabel) :
    rootChartWordWilson (identityWilsonClass S3)
        (atlasRootChart orderedABAtlas atlasTargetDefect sourceRoot)
        (rootTransitionHom .route0 (routeDefectWord .route3)) ≠
      rootChartWordWilson (identityWilsonClass S3)
        (atlasRootChart orderedBAAtlas atlasTargetDefect sourceRoot)
        (rootTransitionHom .route0 (routeDefectWord .route3)) := by
  rw [canonical_ordered_ab_all_root_mixed_wilson,
    canonical_ordered_ba_all_root_mixed_wilson]
  norm_num

end KUOS.OpenHorizon.MemoryOSAllRootChartDefectAwareWordTransportV0_80
