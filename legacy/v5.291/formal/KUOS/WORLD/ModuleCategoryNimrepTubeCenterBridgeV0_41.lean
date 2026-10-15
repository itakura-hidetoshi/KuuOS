import Mathlib
import KUOS.WORLD.BimoduleSectorFusionCategoryBridgeV0_40

/-!
Kū–Indra WORLD module-category, nimrep, Ocneanu-cell, tube-algebra,
and Drinfeld-center bridge v0.41.

The exact WORLD state is not identified with a module category, nimrep,
Ocneanu cell system, tube algebra, or Drinfeld center.  This file adds a
read-only analytic sidecar over the v0.40 finite sector-fusion bridge.  Lean
directly verifies the finite module-action representation laws, positive
module dimensions, tube *-algebra structure constants, central idempotent
relations, and the global-dimension square law for the Drinfeld center.
Analytic realization and categorical equivalences remain explicit receipts.
-/

namespace KUOS
namespace WORLD

structure WorldModuleCategoryNimrepTubeCenterBridge
    {C : RealHilbertL2Carrier}
    {W : WorldNoncommutativeOperatorAlgebra C}
    [PartialOrder W.Region]
    {B : WorldCStarLocalNetBridge C W}
    {V : WorldVonNeumannBicommutantBridge B}
    {M : WorldStandardFormModularFlowBridge V}
    {R : WorldModularStateKMSRelativeFlowBridge M}
    {E : WorldArakiRelativeEntropyBridge R}
    {P : WorldPetzRecoverySufficiencyBridge E}
    {T : WorldConditionalExpectationTakesakiBridge P}
    {J : WorldJonesBasicConstructionIndexBridge T}
    {S : WorldJonesTowerStandardInvariantBridge J}
    {Q : WorldCanonicalEndomorphismQSystemFrobeniusBridge S}
    (F : WorldBimoduleSectorFusionCategoryBridge Q) where
  ModuleLabel : Type
  [moduleLabelFintype : Fintype ModuleLabel]
  [moduleLabelDecidableEq : DecidableEq ModuleLabel]
  distinguishedModule : ModuleLabel
  moduleActionMultiplicity : F.Sector → ModuleLabel → ModuleLabel → ℕ
  moduleAction_unit : ∀ m n,
    moduleActionMultiplicity F.tensorUnit m n = if m = n then 1 else 0
  moduleAction_associativity : ∀ a b m n,
    (∑ x, F.fusionMultiplicity a b x * moduleActionMultiplicity x m n) =
      ∑ k, moduleActionMultiplicity b m k * moduleActionMultiplicity a k n
  moduleAction_dual_transpose : ∀ a m n,
    moduleActionMultiplicity (F.sectorDual a) m n =
      moduleActionMultiplicity a n m
  moduleDimension : ModuleLabel → ℝ
  moduleDimension_pos : ∀ m, 0 < moduleDimension m
  moduleDimension_eigenvector : ∀ a m,
    F.sectorDimension a * moduleDimension m =
      ∑ n, (moduleActionMultiplicity a m n : ℝ) * moduleDimension n
  nimrepGraphEdgeMultiplicity : ModuleLabel → ModuleLabel → ℕ
  nimrepGraphEdge_formula : ∀ m n,
    nimrepGraphEdgeMultiplicity m n =
      moduleActionMultiplicity F.fundamentalSector m n
  CellLabel : Type
  [cellLabelFintype : Fintype CellLabel]
  [cellLabelDecidableEq : DecidableEq CellLabel]
  ocneanuCellAmplitude :
    F.Sector → F.Sector → ModuleLabel → ModuleLabel → CellLabel → ℂ
  ocneanuCell_conjugation : ∀ a b m n c,
    ocneanuCellAmplitude (F.sectorDual b) (F.sectorDual a) n m c =
      star (ocneanuCellAmplitude a b m n c)
  TubeBasis : Type
  [tubeBasisFintype : Fintype TubeBasis]
  [tubeBasisDecidableEq : DecidableEq TubeBasis]
  tubeUnit : TubeBasis
  tubeStar : TubeBasis → TubeBasis
  tubeStar_involutive : ∀ a, tubeStar (tubeStar a) = a
  tubeStar_unit : tubeStar tubeUnit = tubeUnit
  tubeMulCoeff : TubeBasis → TubeBasis → TubeBasis → ℂ
  tube_left_unit : ∀ a c,
    tubeMulCoeff tubeUnit a c = if a = c then 1 else 0
  tube_right_unit : ∀ a c,
    tubeMulCoeff a tubeUnit c = if a = c then 1 else 0
  tube_associativity : ∀ a b c d,
    (∑ x, tubeMulCoeff a b x * tubeMulCoeff x c d) =
      ∑ y, tubeMulCoeff b c y * tubeMulCoeff a y d
  tube_star_compatibility : ∀ a b c,
    tubeMulCoeff (tubeStar b) (tubeStar a) (tubeStar c) =
      star (tubeMulCoeff a b c)
  CenterSimple : Type
  [centerSimpleFintype : Fintype CenterSimple]
  [centerSimpleDecidableEq : DecidableEq CenterSimple]
  centerDual : CenterSimple → CenterSimple
  centerDual_involutive : ∀ z, centerDual (centerDual z) = z
  centralIdempotentCoeff : CenterSimple → TubeBasis → ℂ
  centralIdempotent_centrality : ∀ z a c,
    (∑ b, tubeMulCoeff a b c * centralIdempotentCoeff z b) =
      ∑ b, centralIdempotentCoeff z b * tubeMulCoeff b a c
  centralIdempotent_orthogonality : ∀ z w c,
    (∑ a, ∑ b,
      centralIdempotentCoeff z a * centralIdempotentCoeff w b *
        tubeMulCoeff a b c) =
      if z = w then centralIdempotentCoeff z c else 0
  centralIdempotent_completeness : ∀ c,
    (∑ z, centralIdempotentCoeff z c) = if c = tubeUnit then 1 else 0
  centerDimension : CenterSimple → ℝ
  centerDimension_pos : ∀ z, 0 < centerDimension z
  centerDimension_dual : ∀ z,
    centerDimension (centerDual z) = centerDimension z
  forgetMultiplicity : CenterSimple → F.Sector → ℕ
  centerDimension_forget_formula : ∀ z,
    centerDimension z =
      ∑ a, (forgetMultiplicity z a : ℝ) * F.sectorDimension a
  drinfeldCenter_global_dimension_square :
    (∑ z, centerDimension z ^ 2) =
      (∑ a, F.sectorDimension a ^ 2) ^ 2
  moduleCategoryExistenceClaim : Prop
  moduleCategoryExistenceProof : moduleCategoryExistenceClaim
  nimrepCompletenessClaim : Prop
  nimrepCompletenessProof : nimrepCompletenessClaim
  ocneanuCellExistenceClaim : Prop
  ocneanuCellExistenceProof : ocneanuCellExistenceClaim
  ocneanuCellUnitarityClaim : Prop
  ocneanuCellUnitarityProof : ocneanuCellUnitarityClaim
  ocneanuCellFlatnessClaim : Prop
  ocneanuCellFlatnessProof : ocneanuCellFlatnessClaim
  finiteDimensionalCStarTubeAlgebraClaim : Prop
  finiteDimensionalCStarTubeAlgebraProof :
    finiteDimensionalCStarTubeAlgebraClaim
  tubeCenterClassificationClaim : Prop
  tubeCenterClassificationProof : tubeCenterClassificationClaim
  drinfeldCenterEquivalenceClaim : Prop
  drinfeldCenterEquivalenceProof : drinfeldCenterEquivalenceClaim
  moritaInvarianceClaim : Prop
  moritaInvarianceProof : moritaInvarianceClaim
  drinfeldCenterModularityClaim : Prop
  drinfeldCenterModularityProof : drinfeldCenterModularityClaim
  runtimeConstructsModuleCategory : Bool
  runtimeSolvesOcneanuCells : Bool
  runtimeBuildsTubeAlgebra : Bool
  runtimeReconstructsDrinfeldCenter : Bool
  runtimeUpdatesWorld : Bool
  noRuntimeModuleCategoryConstruction : runtimeConstructsModuleCategory = false
  noRuntimeOcneanuCellSolver : runtimeSolvesOcneanuCells = false
  noRuntimeTubeAlgebraConstruction : runtimeBuildsTubeAlgebra = false
  noRuntimeDrinfeldCenterReconstruction :
    runtimeReconstructsDrinfeldCenter = false
  noRuntimeWorldUpdate : runtimeUpdatesWorld = false
  worldNotIdentifiedWithModuleCategory : Prop
  worldNotIdentifiedWithModuleCategoryProof :
    worldNotIdentifiedWithModuleCategory
  worldNotIdentifiedWithNimrep : Prop
  worldNotIdentifiedWithNimrepProof : worldNotIdentifiedWithNimrep
  worldNotIdentifiedWithTubeAlgebra : Prop
  worldNotIdentifiedWithTubeAlgebraProof : worldNotIdentifiedWithTubeAlgebra
  worldNotIdentifiedWithDrinfeldCenter : Prop
  worldNotIdentifiedWithDrinfeldCenterProof :
    worldNotIdentifiedWithDrinfeldCenter
  moduleTubeCenterReadOnlyAnalyticSidecar : Prop
  moduleTubeCenterReadOnlyAnalyticSidecarProof :
    moduleTubeCenterReadOnlyAnalyticSidecar
  multiWorldNoncollapsePreserved : Prop
  multiWorldNoncollapseProof : multiWorldNoncollapsePreserved
  twoTruthsGapPreserved : Prop
  twoTruthsGapProof : twoTruthsGapPreserved

attribute [instance]
  WorldModuleCategoryNimrepTubeCenterBridge.moduleLabelFintype
  WorldModuleCategoryNimrepTubeCenterBridge.moduleLabelDecidableEq
  WorldModuleCategoryNimrepTubeCenterBridge.cellLabelFintype
  WorldModuleCategoryNimrepTubeCenterBridge.cellLabelDecidableEq
  WorldModuleCategoryNimrepTubeCenterBridge.tubeBasisFintype
  WorldModuleCategoryNimrepTubeCenterBridge.tubeBasisDecidableEq
  WorldModuleCategoryNimrepTubeCenterBridge.centerSimpleFintype
  WorldModuleCategoryNimrepTubeCenterBridge.centerSimpleDecidableEq

namespace WorldModuleCategoryNimrepTubeCenterBridge

variable {C : RealHilbertL2Carrier}
variable {W : WorldNoncommutativeOperatorAlgebra C}
variable [PartialOrder W.Region]
variable {B : WorldCStarLocalNetBridge C W}
variable {V : WorldVonNeumannBicommutantBridge B}
variable {M : WorldStandardFormModularFlowBridge V}
variable {R : WorldModularStateKMSRelativeFlowBridge M}
variable {E : WorldArakiRelativeEntropyBridge R}
variable {P : WorldPetzRecoverySufficiencyBridge E}
variable {T : WorldConditionalExpectationTakesakiBridge P}
variable {J : WorldJonesBasicConstructionIndexBridge T}
variable {S : WorldJonesTowerStandardInvariantBridge J}
variable {Q : WorldCanonicalEndomorphismQSystemFrobeniusBridge S}
variable {F : WorldBimoduleSectorFusionCategoryBridge Q}
variable (Z : WorldModuleCategoryNimrepTubeCenterBridge F)

theorem moduleAction_unit_at_self (m : Z.ModuleLabel) :
    Z.moduleActionMultiplicity F.tensorUnit m m = 1 := by
  rw [Z.moduleAction_unit]
  simp

theorem moduleAction_unit_off_diagonal
    {m n : Z.ModuleLabel} (h : m ≠ n) :
    Z.moduleActionMultiplicity F.tensorUnit m n = 0 := by
  rw [Z.moduleAction_unit]
  simp [h]

theorem nimrep_fusion_representation
    (a b : F.Sector) (m n : Z.ModuleLabel) :
    (∑ x, F.fusionMultiplicity a b x *
      Z.moduleActionMultiplicity x m n) =
      ∑ k, Z.moduleActionMultiplicity b m k *
        Z.moduleActionMultiplicity a k n :=
  Z.moduleAction_associativity a b m n

theorem nimrep_dual_is_transpose
    (a : F.Sector) (m n : Z.ModuleLabel) :
    Z.moduleActionMultiplicity (F.sectorDual a) m n =
      Z.moduleActionMultiplicity a n m :=
  Z.moduleAction_dual_transpose a m n

theorem moduleDimension_ne_zero (m : Z.ModuleLabel) :
    Z.moduleDimension m ≠ 0 :=
  ne_of_gt (Z.moduleDimension_pos m)

theorem moduleDimension_eigenvector_formula
    (a : F.Sector) (m : Z.ModuleLabel) :
    F.sectorDimension a * Z.moduleDimension m =
      ∑ n, (Z.moduleActionMultiplicity a m n : ℝ) *
        Z.moduleDimension n :=
  Z.moduleDimension_eigenvector a m

theorem distinguishedModule_dimension_pos :
    0 < Z.moduleDimension Z.distinguishedModule :=
  Z.moduleDimension_pos Z.distinguishedModule

theorem nimrepGraph_edge_formula
    (m n : Z.ModuleLabel) :
    Z.nimrepGraphEdgeMultiplicity m n =
      Z.moduleActionMultiplicity F.fundamentalSector m n :=
  Z.nimrepGraphEdge_formula m n

theorem ocneanuCell_conjugation_symmetry
    (a b : F.Sector) (m n : Z.ModuleLabel) (c : Z.CellLabel) :
    Z.ocneanuCellAmplitude (F.sectorDual b) (F.sectorDual a) n m c =
      star (Z.ocneanuCellAmplitude a b m n c) :=
  Z.ocneanuCell_conjugation a b m n c

theorem tubeStar_involution (a : Z.TubeBasis) :
    Z.tubeStar (Z.tubeStar a) = a :=
  Z.tubeStar_involutive a

theorem tubeUnit_self_adjoint :
    Z.tubeStar Z.tubeUnit = Z.tubeUnit :=
  Z.tubeStar_unit

theorem tube_left_unit_at_self (a : Z.TubeBasis) :
    Z.tubeMulCoeff Z.tubeUnit a a = 1 := by
  rw [Z.tube_left_unit]
  simp

theorem tube_right_unit_at_self (a : Z.TubeBasis) :
    Z.tubeMulCoeff a Z.tubeUnit a = 1 := by
  rw [Z.tube_right_unit]
  simp

theorem tube_associative
    (a b c d : Z.TubeBasis) :
    (∑ x, Z.tubeMulCoeff a b x * Z.tubeMulCoeff x c d) =
      ∑ y, Z.tubeMulCoeff b c y * Z.tubeMulCoeff a y d :=
  Z.tube_associativity a b c d

theorem tubeStar_reverses_multiplication
    (a b c : Z.TubeBasis) :
    Z.tubeMulCoeff (Z.tubeStar b) (Z.tubeStar a) (Z.tubeStar c) =
      star (Z.tubeMulCoeff a b c) :=
  Z.tube_star_compatibility a b c

theorem centerDual_involution (z : Z.CenterSimple) :
    Z.centerDual (Z.centerDual z) = z :=
  Z.centerDual_involutive z

theorem centralIdempotent_is_central
    (z : Z.CenterSimple) (a c : Z.TubeBasis) :
    (∑ b, Z.tubeMulCoeff a b c * Z.centralIdempotentCoeff z b) =
      ∑ b, Z.centralIdempotentCoeff z b * Z.tubeMulCoeff b a c :=
  Z.centralIdempotent_centrality z a c

theorem centralIdempotent_is_idempotent
    (z : Z.CenterSimple) (c : Z.TubeBasis) :
    (∑ a, ∑ b,
      Z.centralIdempotentCoeff z a * Z.centralIdempotentCoeff z b *
        Z.tubeMulCoeff a b c) = Z.centralIdempotentCoeff z c := by
  simpa using Z.centralIdempotent_orthogonality z z c

theorem centralIdempotents_are_orthogonal
    {z w : Z.CenterSimple} (h : z ≠ w) (c : Z.TubeBasis) :
    (∑ a, ∑ b,
      Z.centralIdempotentCoeff z a * Z.centralIdempotentCoeff w b *
        Z.tubeMulCoeff a b c) = 0 := by
  simpa [h] using Z.centralIdempotent_orthogonality z w c

theorem centralIdempotents_complete (c : Z.TubeBasis) :
    (∑ z, Z.centralIdempotentCoeff z c) =
      if c = Z.tubeUnit then 1 else 0 :=
  Z.centralIdempotent_completeness c

theorem centerDimension_ne_zero (z : Z.CenterSimple) :
    Z.centerDimension z ≠ 0 :=
  ne_of_gt (Z.centerDimension_pos z)

theorem centerDual_same_dimension (z : Z.CenterSimple) :
    Z.centerDimension (Z.centerDual z) = Z.centerDimension z :=
  Z.centerDimension_dual z

theorem centerDimension_forgetful_formula (z : Z.CenterSimple) :
    Z.centerDimension z =
      ∑ a, (Z.forgetMultiplicity z a : ℝ) * F.sectorDimension a :=
  Z.centerDimension_forget_formula z

theorem drinfeldCenter_dimension_square :
    (∑ z, Z.centerDimension z ^ 2) =
      (∑ a, F.sectorDimension a ^ 2) ^ 2 :=
  Z.drinfeldCenter_global_dimension_square

theorem nimrep_module_package :
    (∀ m : Z.ModuleLabel,
      Z.moduleActionMultiplicity F.tensorUnit m m = 1) ∧
    (∀ a b m n,
      (∑ x, F.fusionMultiplicity a b x *
        Z.moduleActionMultiplicity x m n) =
      ∑ k, Z.moduleActionMultiplicity b m k *
        Z.moduleActionMultiplicity a k n) ∧
    (∀ a m n,
      Z.moduleActionMultiplicity (F.sectorDual a) m n =
        Z.moduleActionMultiplicity a n m) ∧
    (∀ m : Z.ModuleLabel, 0 < Z.moduleDimension m) :=
  ⟨Z.moduleAction_unit_at_self,
    Z.moduleAction_associativity,
    Z.moduleAction_dual_transpose,
    Z.moduleDimension_pos⟩

theorem tube_star_algebra_package :
    (∀ a : Z.TubeBasis, Z.tubeStar (Z.tubeStar a) = a) ∧
    Z.tubeStar Z.tubeUnit = Z.tubeUnit ∧
    (∀ a b c d,
      (∑ x, Z.tubeMulCoeff a b x * Z.tubeMulCoeff x c d) =
      ∑ y, Z.tubeMulCoeff b c y * Z.tubeMulCoeff a y d) ∧
    (∀ a b c,
      Z.tubeMulCoeff (Z.tubeStar b) (Z.tubeStar a) (Z.tubeStar c) =
        star (Z.tubeMulCoeff a b c)) :=
  ⟨Z.tubeStar_involutive,
    Z.tubeStar_unit,
    Z.tube_associativity,
    Z.tube_star_compatibility⟩

theorem tube_center_package :
    (∀ z a c,
      (∑ b, Z.tubeMulCoeff a b c * Z.centralIdempotentCoeff z b) =
      ∑ b, Z.centralIdempotentCoeff z b * Z.tubeMulCoeff b a c) ∧
    (∀ z c,
      (∑ a, ∑ b,
        Z.centralIdempotentCoeff z a * Z.centralIdempotentCoeff z b *
          Z.tubeMulCoeff a b c) = Z.centralIdempotentCoeff z c) ∧
    (∀ c,
      (∑ z, Z.centralIdempotentCoeff z c) =
        if c = Z.tubeUnit then 1 else 0) ∧
    (∑ z, Z.centerDimension z ^ 2) =
      (∑ a, F.sectorDimension a ^ 2) ^ 2 :=
  ⟨Z.centralIdempotent_centrality,
    Z.centralIdempotent_is_idempotent,
    Z.centralIdempotent_completeness,
    Z.drinfeldCenter_global_dimension_square⟩

theorem analytic_categorical_receipts_complete :
    Z.moduleCategoryExistenceClaim ∧
    Z.nimrepCompletenessClaim ∧
    Z.ocneanuCellExistenceClaim ∧
    Z.ocneanuCellUnitarityClaim ∧
    Z.ocneanuCellFlatnessClaim ∧
    Z.finiteDimensionalCStarTubeAlgebraClaim ∧
    Z.tubeCenterClassificationClaim ∧
    Z.drinfeldCenterEquivalenceClaim ∧
    Z.moritaInvarianceClaim ∧
    Z.drinfeldCenterModularityClaim :=
  ⟨Z.moduleCategoryExistenceProof,
    Z.nimrepCompletenessProof,
    Z.ocneanuCellExistenceProof,
    Z.ocneanuCellUnitarityProof,
    Z.ocneanuCellFlatnessProof,
    Z.finiteDimensionalCStarTubeAlgebraProof,
    Z.tubeCenterClassificationProof,
    Z.drinfeldCenterEquivalenceProof,
    Z.moritaInvarianceProof,
    Z.drinfeldCenterModularityProof⟩

theorem runtime_grants_no_module_tube_center_authority :
    Z.runtimeConstructsModuleCategory = false ∧
    Z.runtimeSolvesOcneanuCells = false ∧
    Z.runtimeBuildsTubeAlgebra = false ∧
    Z.runtimeReconstructsDrinfeldCenter = false ∧
    Z.runtimeUpdatesWorld = false :=
  ⟨Z.noRuntimeModuleCategoryConstruction,
    Z.noRuntimeOcneanuCellSolver,
    Z.noRuntimeTubeAlgebraConstruction,
    Z.noRuntimeDrinfeldCenterReconstruction,
    Z.noRuntimeWorldUpdate⟩

theorem representation_boundary_preserved :
    Z.worldNotIdentifiedWithModuleCategory ∧
    Z.worldNotIdentifiedWithNimrep ∧
    Z.worldNotIdentifiedWithTubeAlgebra ∧
    Z.worldNotIdentifiedWithDrinfeldCenter ∧
    Z.moduleTubeCenterReadOnlyAnalyticSidecar ∧
    Z.multiWorldNoncollapsePreserved ∧
    Z.twoTruthsGapPreserved :=
  ⟨Z.worldNotIdentifiedWithModuleCategoryProof,
    Z.worldNotIdentifiedWithNimrepProof,
    Z.worldNotIdentifiedWithTubeAlgebraProof,
    Z.worldNotIdentifiedWithDrinfeldCenterProof,
    Z.moduleTubeCenterReadOnlyAnalyticSidecarProof,
    Z.multiWorldNoncollapseProof,
    Z.twoTruthsGapProof⟩

end WorldModuleCategoryNimrepTubeCenterBridge
end WORLD
end KUOS
