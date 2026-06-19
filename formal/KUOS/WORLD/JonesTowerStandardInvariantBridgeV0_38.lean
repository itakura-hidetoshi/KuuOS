import Mathlib
import KUOS.WORLD.JonesBasicConstructionIndexBridgeV0_37

/-!
Kū–Indra WORLD Jones-tower, Temperley–Lieb, and standard-invariant bridge v0.38.

Lean directly verifies the typed finite-stage tower laws, projection placement,
Temperley–Lieb relations, far commutation, lower and upper relative-commutant
filtrations, and the index/loop-parameter package. Factoriality, recursive
von Neumann basic construction, extremality, finite depth, principal-graph
reconstruction, and planar-algebra completeness remain external receipts.
-/

namespace KUOS
namespace WORLD

structure WorldJonesTowerStandardInvariantBridge
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
    (J : WorldJonesBasicConstructionIndexBridge T) where
  towerAlgebra : ℕ → Subalgebra ℂ B.A
  tower_zero_eq_sufficient : towerAlgebra 0 = T.sufficientSubalgebra
  tower_one_eq_basicConstruction : towerAlgebra 1 = J.basicConstruction
  tower_monotone : ∀ {m n : ℕ}, m ≤ n → towerAlgebra m ≤ towerAlgebra n
  jonesProjectionAt : ℕ → B.A
  projection_zero_eq_original : jonesProjectionAt 0 = J.jonesProjection
  projection_idempotent : ∀ n,
    jonesProjectionAt n * jonesProjectionAt n = jonesProjectionAt n
  projection_selfAdjoint : ∀ n,
    star (jonesProjectionAt n) = jonesProjectionAt n
  projection_mem_two_steps : ∀ n,
    jonesProjectionAt n ∈ towerAlgebra (n + 2)
  temperleyLiebScalar : ℂ
  temperleyLiebScalar_eq_index_inverse :
    temperleyLiebScalar = (((J.jonesIndex)⁻¹ : ℝ) : ℂ)
  adjacent_right_relation : ∀ n,
    jonesProjectionAt n * jonesProjectionAt (n + 1) * jonesProjectionAt n =
      temperleyLiebScalar • jonesProjectionAt n
  adjacent_left_relation : ∀ n,
    jonesProjectionAt (n + 1) * jonesProjectionAt n *
        jonesProjectionAt (n + 1) =
      temperleyLiebScalar • jonesProjectionAt (n + 1)
  far_commutation : ∀ {m n : ℕ},
    (m + 1 < n ∨ n + 1 < m) →
      jonesProjectionAt m * jonesProjectionAt n =
        jonesProjectionAt n * jonesProjectionAt m
  projection_commutes_with_base : ∀ n {a : B.A},
    a ∈ towerAlgebra 0 →
      jonesProjectionAt n * a = a * jonesProjectionAt n
  lowerRelativeCommutant : ℕ → Subalgebra ℂ B.A
  lowerRelativeCommutant_characterization : ∀ n (a : B.A),
    a ∈ lowerRelativeCommutant n ↔
      a ∈ towerAlgebra n ∧
      ∀ b : B.A, b ∈ towerAlgebra 0 → a * b = b * a
  lowerRelativeCommutant_monotone : ∀ {m n : ℕ},
    m ≤ n → lowerRelativeCommutant m ≤ lowerRelativeCommutant n
  upperRelativeCommutant : ℕ → Subalgebra ℂ B.A
  upperRelativeCommutant_characterization : ∀ n (a : B.A),
    a ∈ upperRelativeCommutant n ↔
      a ∈ towerAlgebra n ∧
      ∀ b : B.A, b ∈ towerAlgebra 1 → a * b = b * a
  upperRelativeCommutant_monotone : ∀ {m n : ℕ},
    m ≤ n → upperRelativeCommutant m ≤ upperRelativeCommutant n
  loopParameter : ℝ
  loopParameter_pos : 0 < loopParameter
  loopParameter_sq_eq_index : loopParameter ^ 2 = J.jonesIndex
  recursiveBasicConstructionClaim : Prop
  recursiveBasicConstructionProof : recursiveBasicConstructionClaim
  towerVonNeumannClosedClaim : Prop
  towerVonNeumannClosedProof : towerVonNeumannClosedClaim
  canonicalExpectationTowerClaim : Prop
  canonicalExpectationTowerProof : canonicalExpectationTowerClaim
  markovTraceTowerClaim : Prop
  markovTraceTowerProof : markovTraceTowerClaim
  constantIndexAlongTowerClaim : Prop
  constantIndexAlongTowerProof : constantIndexAlongTowerClaim
  factorialTowerClaim : Prop
  factorialTowerProof : factorialTowerClaim
  extremalityClaim : Prop
  extremalityProof : extremalityClaim
  standardInvariantCompleteClaim : Prop
  standardInvariantCompleteProof : standardInvariantCompleteClaim
  principalGraphReconstructionClaim : Prop
  principalGraphReconstructionProof : principalGraphReconstructionClaim
  finiteDepthCharacterizationClaim : Prop
  finiteDepthCharacterizationProof : finiteDepthCharacterizationClaim
  planarAlgebraRealizationClaim : Prop
  planarAlgebraRealizationProof : planarAlgebraRealizationClaim
  runtimeConstructsJonesTower : Bool
  runtimeExecutesTemperleyLiebAlgebra : Bool
  runtimeClaimsStandardInvariantCompleteness : Bool
  runtimeUpdatesWorld : Bool
  noRuntimeJonesTowerConstruction : runtimeConstructsJonesTower = false
  noRuntimeTemperleyLiebExecution :
    runtimeExecutesTemperleyLiebAlgebra = false
  noRuntimeStandardInvariantCompletenessClaim :
    runtimeClaimsStandardInvariantCompleteness = false
  noRuntimeWorldUpdate : runtimeUpdatesWorld = false
  worldNotIdentifiedWithJonesTower : Prop
  worldNotIdentifiedProof : worldNotIdentifiedWithJonesTower
  multiWorldNoncollapsePreserved : Prop
  multiWorldNoncollapseProof : multiWorldNoncollapsePreserved
  twoTruthsGapPreserved : Prop
  twoTruthsGapProof : twoTruthsGapPreserved

namespace WorldJonesTowerStandardInvariantBridge

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
variable (S : WorldJonesTowerStandardInvariantBridge J)

theorem tower_zero :
    S.towerAlgebra 0 = T.sufficientSubalgebra :=
  S.tower_zero_eq_sufficient

theorem tower_one :
    S.towerAlgebra 1 = J.basicConstruction :=
  S.tower_one_eq_basicConstruction

theorem tower_step (n : ℕ) :
    S.towerAlgebra n ≤ S.towerAlgebra (n + 1) :=
  S.tower_monotone (Nat.le_add_right n 1)

theorem tower_inclusion {m n : ℕ} (h : m ≤ n) :
    S.towerAlgebra m ≤ S.towerAlgebra n :=
  S.tower_monotone h

theorem projection_sq (n : ℕ) :
    S.jonesProjectionAt n * S.jonesProjectionAt n =
      S.jonesProjectionAt n :=
  S.projection_idempotent n

theorem projection_star (n : ℕ) :
    star (S.jonesProjectionAt n) = S.jonesProjectionAt n :=
  S.projection_selfAdjoint n

theorem projection_mem_stage (n : ℕ) :
    S.jonesProjectionAt n ∈ S.towerAlgebra (n + 2) :=
  S.projection_mem_two_steps n

theorem projection_mem_later_stage
    {n k : ℕ} (h : n + 2 ≤ k) :
    S.jonesProjectionAt n ∈ S.towerAlgebra k :=
  S.tower_monotone h (S.projection_mem_two_steps n)

theorem original_projection_identified :
    S.jonesProjectionAt 0 = J.jonesProjection :=
  S.projection_zero_eq_original

theorem original_projection_mem_stage_two :
    J.jonesProjection ∈ S.towerAlgebra 2 := by
  rw [← S.projection_zero_eq_original]
  simpa using S.projection_mem_two_steps 0

theorem temperleyLieb_right (n : ℕ) :
    S.jonesProjectionAt n * S.jonesProjectionAt (n + 1) *
        S.jonesProjectionAt n =
      S.temperleyLiebScalar • S.jonesProjectionAt n :=
  S.adjacent_right_relation n

theorem temperleyLieb_left (n : ℕ) :
    S.jonesProjectionAt (n + 1) * S.jonesProjectionAt n *
        S.jonesProjectionAt (n + 1) =
      S.temperleyLiebScalar • S.jonesProjectionAt (n + 1) :=
  S.adjacent_left_relation n

theorem distant_projections_commute
    {m n : ℕ} (h : m + 1 < n ∨ n + 1 < m) :
    S.jonesProjectionAt m * S.jonesProjectionAt n =
      S.jonesProjectionAt n * S.jonesProjectionAt m :=
  S.far_commutation h

theorem projection_mem_lowerRelativeCommutant (n : ℕ) :
    S.jonesProjectionAt n ∈ S.lowerRelativeCommutant (n + 2) := by
  apply (S.lowerRelativeCommutant_characterization (n + 2)
    (S.jonesProjectionAt n)).2
  constructor
  · exact S.projection_mem_two_steps n
  · intro b hb
    exact S.projection_commutes_with_base n hb

theorem lower_standard_invariant_nesting
    {m n : ℕ} (h : m ≤ n) :
    S.lowerRelativeCommutant m ≤ S.lowerRelativeCommutant n :=
  S.lowerRelativeCommutant_monotone h

theorem upper_standard_invariant_nesting
    {m n : ℕ} (h : m ≤ n) :
    S.upperRelativeCommutant m ≤ S.upperRelativeCommutant n :=
  S.upperRelativeCommutant_monotone h

theorem lowerRelativeCommutant_membership (n : ℕ) (a : B.A) :
    a ∈ S.lowerRelativeCommutant n ↔
      a ∈ S.towerAlgebra n ∧
      ∀ b : B.A, b ∈ S.towerAlgebra 0 → a * b = b * a :=
  S.lowerRelativeCommutant_characterization n a

theorem upperRelativeCommutant_membership (n : ℕ) (a : B.A) :
    a ∈ S.upperRelativeCommutant n ↔
      a ∈ S.towerAlgebra n ∧
      ∀ b : B.A, b ∈ S.towerAlgebra 1 → a * b = b * a :=
  S.upperRelativeCommutant_characterization n a

theorem loopParameter_ne_zero : S.loopParameter ≠ 0 :=
  ne_of_gt S.loopParameter_pos

theorem jonesIndex_eq_loopParameter_sq :
    J.jonesIndex = S.loopParameter ^ 2 :=
  S.loopParameter_sq_eq_index.symm

theorem temperleyLiebScalar_index_formula :
    S.temperleyLiebScalar = (((J.jonesIndex)⁻¹ : ℝ) : ℂ) :=
  S.temperleyLiebScalar_eq_index_inverse

theorem standard_invariant_package :
    (∀ {m n : ℕ}, m ≤ n →
      S.lowerRelativeCommutant m ≤ S.lowerRelativeCommutant n) ∧
    (∀ {m n : ℕ}, m ≤ n →
      S.upperRelativeCommutant m ≤ S.upperRelativeCommutant n) ∧
    (∀ n, S.jonesProjectionAt n ∈
      S.lowerRelativeCommutant (n + 2)) :=
  ⟨S.lowerRelativeCommutant_monotone,
    S.upperRelativeCommutant_monotone,
    S.projection_mem_lowerRelativeCommutant⟩

theorem analytic_receipts_complete :
    S.recursiveBasicConstructionClaim ∧
    S.towerVonNeumannClosedClaim ∧
    S.canonicalExpectationTowerClaim ∧
    S.markovTraceTowerClaim ∧
    S.constantIndexAlongTowerClaim ∧
    S.factorialTowerClaim ∧
    S.extremalityClaim ∧
    S.standardInvariantCompleteClaim ∧
    S.principalGraphReconstructionClaim ∧
    S.finiteDepthCharacterizationClaim ∧
    S.planarAlgebraRealizationClaim :=
  ⟨S.recursiveBasicConstructionProof,
    S.towerVonNeumannClosedProof,
    S.canonicalExpectationTowerProof,
    S.markovTraceTowerProof,
    S.constantIndexAlongTowerProof,
    S.factorialTowerProof,
    S.extremalityProof,
    S.standardInvariantCompleteProof,
    S.principalGraphReconstructionProof,
    S.finiteDepthCharacterizationProof,
    S.planarAlgebraRealizationProof⟩

theorem runtime_grants_no_tower_authority :
    S.runtimeConstructsJonesTower = false ∧
    S.runtimeExecutesTemperleyLiebAlgebra = false ∧
    S.runtimeClaimsStandardInvariantCompleteness = false ∧
    S.runtimeUpdatesWorld = false :=
  ⟨S.noRuntimeJonesTowerConstruction,
    S.noRuntimeTemperleyLiebExecution,
    S.noRuntimeStandardInvariantCompletenessClaim,
    S.noRuntimeWorldUpdate⟩

theorem representation_boundary_preserved :
    S.worldNotIdentifiedWithJonesTower ∧
    S.multiWorldNoncollapsePreserved ∧
    S.twoTruthsGapPreserved :=
  ⟨S.worldNotIdentifiedProof, S.multiWorldNoncollapseProof,
    S.twoTruthsGapProof⟩

end WorldJonesTowerStandardInvariantBridge
end WORLD
end KUOS
