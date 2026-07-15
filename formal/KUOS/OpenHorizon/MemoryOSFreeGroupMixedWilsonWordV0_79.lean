import Mathlib
import KUOS.OpenHorizon.MemoryOSRootedRouteAtlasNielsenChangeV0_78

namespace KUOS.OpenHorizon.MemoryOSFreeGroupMixedWilsonWordV0_79

open KUOS.OpenHorizon.MemoryOSNonAbelianWilsonLoopV0_72
open KUOS.OpenHorizon.MemoryOSDualCycleBasisTreeChangeV0_77
open KUOS.OpenHorizon.MemoryOSRootedRouteAtlasNielsenChangeV0_78

/-- Four formal generators retained by the v0.79 rooted word atlas. -/
inductive AtlasWordGenerator
  | cycle01
  | cycle02
  | cycle03
  | defect0
deriving DecidableEq, Repr

/-- Assignment of the formal generators to exact rooted observables. -/
def atlasWordAssignment {G : Type*} [Group G]
    (atlas : DualFourRouteAtlas G) (defect : G) : AtlasWordGenerator → G
  | .cycle01 => cycle01 atlas
  | .cycle02 => cycle02 atlas
  | .cycle03 => cycle03 atlas
  | .defect0 => localizedDefect0 atlas defect

/-- Universal free-group evaluation of a rooted atlas word. -/
def evalAtlasWord {G : Type*} [Group G]
    (atlas : DualFourRouteAtlas G) (defect : G) :
    FreeGroup AtlasWordGenerator →* G :=
  FreeGroup.lift (atlasWordAssignment atlas defect)

@[simp] theorem eval_atlas_word_generator
    {G : Type*} [Group G]
    (atlas : DualFourRouteAtlas G) (defect : G)
    (generator : AtlasWordGenerator) :
    evalAtlasWord atlas defect (FreeGroup.of generator) =
      atlasWordAssignment atlas defect generator := by
  simp [evalAtlasWord]

/-- A class-function Wilson observable for an arbitrary rooted free-group word. -/
def atlasWordWilson {G : Type*} [Group G] {R : Type*}
    (χ : ClassFunction G R) (atlas : DualFourRouteAtlas G)
    (defect : G) (word : FreeGroup AtlasWordGenerator) : R :=
  χ.toFun (evalAtlasWord atlas defect word)

/-- The mixed word that resolves the canonical AB/BA cycle-only ambiguity. -/
def cycle03DefectWord : FreeGroup AtlasWordGenerator :=
  FreeGroup.of .cycle03 * FreeGroup.of .defect0

/-- The reversed mixed word is retained as a separate order-sensitive representative. -/
def defectCycle03Word : FreeGroup AtlasWordGenerator :=
  FreeGroup.of .defect0 * FreeGroup.of .cycle03

/-- Exact commutator word of the first two rooted cycle coordinates. -/
def commutator12Word : FreeGroup AtlasWordGenerator :=
  FreeGroup.of .cycle01 * FreeGroup.of .cycle02 *
    (FreeGroup.of .cycle01)⁻¹ * (FreeGroup.of .cycle02)⁻¹

/-- Reversed commutator word. -/
def reverseCommutator12Word : FreeGroup AtlasWordGenerator :=
  FreeGroup.of .cycle02 * FreeGroup.of .cycle01 *
    (FreeGroup.of .cycle02)⁻¹ * (FreeGroup.of .cycle01)⁻¹

@[simp] theorem eval_cycle03_defect_word
    {G : Type*} [Group G]
    (atlas : DualFourRouteAtlas G) (defect : G) :
    evalAtlasWord atlas defect cycle03DefectWord =
      cycle03 atlas * localizedDefect0 atlas defect := by
  simp [cycle03DefectWord, evalAtlasWord, atlasWordAssignment]

@[simp] theorem eval_defect_cycle03_word
    {G : Type*} [Group G]
    (atlas : DualFourRouteAtlas G) (defect : G) :
    evalAtlasWord atlas defect defectCycle03Word =
      localizedDefect0 atlas defect * cycle03 atlas := by
  simp [defectCycle03Word, evalAtlasWord, atlasWordAssignment]

@[simp] theorem eval_commutator12_word
    {G : Type*} [Group G]
    (atlas : DualFourRouteAtlas G) (defect : G) :
    evalAtlasWord atlas defect commutator12Word =
      cycle01 atlas * cycle02 atlas * (cycle01 atlas)⁻¹ *
        (cycle02 atlas)⁻¹ := by
  simp [commutator12Word, evalAtlasWord, atlasWordAssignment]

/-- Elementary Nielsen inversion of the first rooted coordinate. -/
def nielsenInvertFirst {G : Type*} [Group G]
    (coordinates : RootedCoordinates G) : RootedCoordinates G :=
  {
    toFirst := coordinates.toFirst⁻¹
    toSecond := coordinates.toSecond
    toThird := coordinates.toThird
  }

/-- Elementary Nielsen multiplication of the second coordinate by the first. -/
def nielsenLeftMultiplySecond {G : Type*} [Group G]
    (coordinates : RootedCoordinates G) : RootedCoordinates G :=
  {
    toFirst := coordinates.toFirst
    toSecond := coordinates.toFirst * coordinates.toSecond
    toThird := coordinates.toThird
  }

/-- Elementary Nielsen multiplication of the third coordinate by the first. -/
def nielsenLeftMultiplyThird {G : Type*} [Group G]
    (coordinates : RootedCoordinates G) : RootedCoordinates G :=
  {
    toFirst := coordinates.toFirst
    toSecond := coordinates.toSecond
    toThird := coordinates.toFirst * coordinates.toThird
  }

/-- The v0.78 root change decomposes into three elementary Nielsen moves. -/
theorem rebase_at_first_eq_elementary_nielsen_moves
    {G : Type*} [Group G] (coordinates : RootedCoordinates G) :
    rebaseAtFirst coordinates =
      nielsenLeftMultiplyThird
        (nielsenLeftMultiplySecond (nielsenInvertFirst coordinates)) := by
  cases coordinates
  rfl

/-- Substitution of each formal generator under route-0 to route-1 rebasing. -/
def nielsenRebaseGenerator :
    AtlasWordGenerator → FreeGroup AtlasWordGenerator
  | .cycle01 => (FreeGroup.of .cycle01)⁻¹
  | .cycle02 => (FreeGroup.of .cycle01)⁻¹ * FreeGroup.of .cycle02
  | .cycle03 => (FreeGroup.of .cycle01)⁻¹ * FreeGroup.of .cycle03
  | .defect0 => FreeGroup.of .defect0

/-- Universal Nielsen substitution homomorphism on rooted free-group words. -/
def nielsenRebaseHom :
    FreeGroup AtlasWordGenerator →* FreeGroup AtlasWordGenerator :=
  FreeGroup.lift nielsenRebaseGenerator

@[simp] theorem nielsen_rebase_hom_generator
    (generator : AtlasWordGenerator) :
    nielsenRebaseHom (FreeGroup.of generator) =
      nielsenRebaseGenerator generator := by
  simp [nielsenRebaseHom]

/-- The rooted Nielsen substitution is an involution on the entire free group. -/
theorem nielsen_rebase_hom_comp_self :
    nielsenRebaseHom.comp nielsenRebaseHom =
      MonoidHom.id (FreeGroup AtlasWordGenerator) := by
  apply FreeGroup.ext_hom
  intro generator
  cases generator <;>
    simp [nielsenRebaseHom, nielsenRebaseGenerator, mul_assoc]

/-- Pointwise form of the universal involution theorem. -/
theorem nielsen_rebase_word_involutive
    (word : FreeGroup AtlasWordGenerator) :
    nielsenRebaseHom (nielsenRebaseHom word) = word := by
  calc
    nielsenRebaseHom (nielsenRebaseHom word) =
        (nielsenRebaseHom.comp nielsenRebaseHom) word := rfl
    _ = word := by rw [nielsen_rebase_hom_comp_self]; rfl

/-- Assignment directly from a rooted coordinate triple and rooted defect. -/
def coordinateWordAssignment {G : Type*} [Group G]
    (coordinates : RootedCoordinates G) (rootDefect : G) :
    AtlasWordGenerator → G
  | .cycle01 => coordinates.toFirst
  | .cycle02 => coordinates.toSecond
  | .cycle03 => coordinates.toThird
  | .defect0 => rootDefect

/-- Universal evaluation from an abstract rooted coordinate triple. -/
def evalCoordinateWord {G : Type*} [Group G]
    (coordinates : RootedCoordinates G) (rootDefect : G) :
    FreeGroup AtlasWordGenerator →* G :=
  FreeGroup.lift (coordinateWordAssignment coordinates rootDefect)

/-- Nielsen substitution before evaluation equals evaluation in rebased coordinates. -/
theorem nielsen_rebase_evaluation_compatibility
    {G : Type*} [Group G]
    (coordinates : RootedCoordinates G) (rootDefect : G)
    (word : FreeGroup AtlasWordGenerator) :
    evalCoordinateWord coordinates rootDefect (nielsenRebaseHom word) =
      evalCoordinateWord (rebaseAtFirst coordinates) rootDefect word := by
  have hhom :
      (evalCoordinateWord coordinates rootDefect).comp nielsenRebaseHom =
        evalCoordinateWord (rebaseAtFirst coordinates) rootDefect := by
    apply FreeGroup.ext_hom
    intro generator
    cases generator <;>
      simp [evalCoordinateWord, coordinateWordAssignment, nielsenRebaseHom,
        nielsenRebaseGenerator, rebaseAtFirst, mul_assoc]
  calc
    evalCoordinateWord coordinates rootDefect (nielsenRebaseHom word) =
        ((evalCoordinateWord coordinates rootDefect).comp nielsenRebaseHom) word := rfl
    _ = evalCoordinateWord (rebaseAtFirst coordinates) rootDefect word := by
      rw [hhom]

/-- Inner conjugation as a monoid homomorphism. -/
def conjugationHom {G : Type*} [Group G] (frame : G) : G →* G where
  toFun value := frame⁻¹ * value * frame
  map_one' := by group
  map_mul' := by
    intro left right
    group

/-- Evaluation of every free-group word commutes with simultaneous conjugation. -/
theorem free_word_evaluation_conjugation_covariant
    {G : Type*} [Group G]
    (assignment : AtlasWordGenerator → G) (frame : G)
    (word : FreeGroup AtlasWordGenerator) :
    FreeGroup.lift (fun generator =>
        frame⁻¹ * assignment generator * frame) word =
      frame⁻¹ * FreeGroup.lift assignment word * frame := by
  have hhom :
      FreeGroup.lift (fun generator =>
          frame⁻¹ * assignment generator * frame) =
        (conjugationHom frame).comp (FreeGroup.lift assignment) := by
    apply FreeGroup.ext_hom
    intro generator
    simp [conjugationHom]
  calc
    FreeGroup.lift (fun generator =>
        frame⁻¹ * assignment generator * frame) word =
        ((conjugationHom frame).comp (FreeGroup.lift assignment)) word := by
      rw [hhom]
    _ = frame⁻¹ * FreeGroup.lift assignment word * frame := rfl

/-- All four formal observables transform in the same root frame. -/
theorem atlas_word_assignment_gauge_covariant
    {G : Type*} [Group G]
    (atlas : DualFourRouteAtlas G) (defect : G)
    (frame : FourRouteGaugeFrame G) (generator : AtlasWordGenerator) :
    atlasWordAssignment (gaugeTransformAtlas atlas frame)
        (gaugeTransformTargetDefect defect frame) generator =
      frame.g0⁻¹ * atlasWordAssignment atlas defect generator * frame.g0 := by
  cases generator
  · exact cycle01_gauge_covariant atlas frame
  · exact cycle02_gauge_covariant atlas frame
  · exact cycle03_gauge_covariant atlas frame
  · exact localized_defect0_gauge_covariant atlas defect frame

/-- Every rooted free-group word transforms by root conjugation. -/
theorem eval_atlas_word_gauge_covariant
    {G : Type*} [Group G]
    (atlas : DualFourRouteAtlas G) (defect : G)
    (frame : FourRouteGaugeFrame G)
    (word : FreeGroup AtlasWordGenerator) :
    evalAtlasWord (gaugeTransformAtlas atlas frame)
        (gaugeTransformTargetDefect defect frame) word =
      frame.g0⁻¹ * evalAtlasWord atlas defect word * frame.g0 := by
  unfold evalAtlasWord
  have hassign :
      atlasWordAssignment (gaugeTransformAtlas atlas frame)
          (gaugeTransformTargetDefect defect frame) =
        fun generator =>
          frame.g0⁻¹ * atlasWordAssignment atlas defect generator * frame.g0 := by
    funext generator
    exact atlas_word_assignment_gauge_covariant atlas defect frame generator
  rw [hassign]
  exact free_word_evaluation_conjugation_covariant
    (atlasWordAssignment atlas defect) frame.g0 word

/-- Class-function evaluation of every rooted free-group word is gauge invariant. -/
theorem atlas_word_wilson_gauge_invariant
    {G : Type*} [Group G] {R : Type*}
    (χ : ClassFunction G R) (atlas : DualFourRouteAtlas G)
    (defect : G) (frame : FourRouteGaugeFrame G)
    (word : FreeGroup AtlasWordGenerator) :
    atlasWordWilson χ (gaugeTransformAtlas atlas frame)
        (gaugeTransformTargetDefect defect frame) word =
      atlasWordWilson χ atlas defect word := by
  unfold atlasWordWilson
  rw [eval_atlas_word_gauge_covariant]
  simpa using χ.conjugationInvariant frame.g0 (evalAtlasWord atlas defect word)

/-- Mixed cycle-defect Wilson observable used by the canonical separator. -/
def mixedCycle03DefectWilson {G : Type*} [Group G] {R : Type*}
    (χ : ClassFunction G R) (atlas : DualFourRouteAtlas G)
    (defect : G) : R :=
  atlasWordWilson χ atlas defect cycle03DefectWord

/-- The v0.78 cycle-only signature remains equal for the mirrored profiles. -/
theorem canonical_cycle_only_signature_limit :
    completePairwiseCycleSignature (identityWilsonClass S3) orderedABAtlas =
      completePairwiseCycleSignature (identityWilsonClass S3) orderedBAAtlas :=
  canonical_ordered_class_signature_limit

/-- Exact commutator representatives distinguish the mirrored profiles. -/
theorem canonical_ordered_commutator_values :
    evalAtlasWord orderedABAtlas atlasTargetDefect commutator12Word =
        swap12 * swap01 ∧
      evalAtlasWord orderedBAAtlas atlasTargetDefect commutator12Word =
        swap01 * swap12 := by
  native_decide

/-- The exact commutator representatives are different. -/
theorem canonical_ordered_commutator_exactly_differs :
    evalAtlasWord orderedABAtlas atlasTargetDefect commutator12Word ≠
      evalAtlasWord orderedBAAtlas atlasTargetDefect commutator12Word := by
  native_decide

/-- A single class trace of the commutator still cannot resolve the order. -/
theorem canonical_ordered_commutator_wilson_limit :
    atlasWordWilson (identityWilsonClass S3) orderedABAtlas atlasTargetDefect
        commutator12Word =
      atlasWordWilson (identityWilsonClass S3) orderedBAAtlas atlasTargetDefect
        commutator12Word := by
  native_decide

/-- The mixed word is identity in the ordered-AB profile and a 3-cycle in ordered-BA. -/
theorem canonical_ordered_mixed_word_values :
    evalAtlasWord orderedABAtlas atlasTargetDefect cycle03DefectWord = 1 ∧
      evalAtlasWord orderedBAAtlas atlasTargetDefect cycle03DefectWord =
        swap12 * swap01 := by
  native_decide

/-- Exact mixed-word Wilson values for the canonical mirrored profiles. -/
theorem canonical_ordered_ab_mixed_wilson :
    mixedCycle03DefectWilson (identityWilsonClass S3)
      orderedABAtlas atlasTargetDefect = 3 := by
  native_decide

theorem canonical_ordered_ba_mixed_wilson :
    mixedCycle03DefectWilson (identityWilsonClass S3)
      orderedBAAtlas atlasTargetDefect = 0 := by
  native_decide

/-- The gauge-invariant mixed Wilson word resolves the v0.78 class-signature ambiguity. -/
theorem canonical_ordered_mixed_wilson_separates :
    mixedCycle03DefectWilson (identityWilsonClass S3)
        orderedABAtlas atlasTargetDefect ≠
      mixedCycle03DefectWilson (identityWilsonClass S3)
        orderedBAAtlas atlasTargetDefect := by
  native_decide

end KUOS.OpenHorizon.MemoryOSFreeGroupMixedWilsonWordV0_79
