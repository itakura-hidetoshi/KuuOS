import Mathlib
import KUOS.WORLD.ArakiPetzQuantumInformationGeometryBridgeV0_44

/-!
Kū–Indra WORLD quantum exponential-family and dual-affine projection bridge v0.45.

This finite read-only sidecar adds natural/expectation coordinates, a finite
Fenchel–Young gap, quantum Bregman divergence, and exponential/mixture
information projections over the v0.44 Araki–Petz quantum information geometry.
It does not identify WORLD with a quantum exponential family, a Legendre dual
coordinate system, or an information projection.
-/

namespace KUOS
namespace WORLD

structure WorldQuantumExponentialDualAffineProjectionBridge
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
    {F : WorldBimoduleSectorFusionCategoryBridge Q}
    {Z : WorldModuleCategoryNimrepTubeCenterBridge F}
    {G : WorldGaugeCategoricalIndraNetBridge Z}
    {I : WorldInformationGeometricHigherGaugeBridge G}
    (H : WorldArakiPetzQuantumInformationGeometryBridge I) where
  naturalCoordinate : G.Patch → I.Parameter → I.Tangent
  expectationCoordinate : G.Patch → I.Parameter → I.Tangent
  naturalCoordinate_injective : ∀ i,
    Function.Injective (naturalCoordinate i)
  expectationCoordinate_injective : ∀ i,
    Function.Injective (expectationCoordinate i)

  logPartition : G.Patch → I.Parameter → ℝ
  dualPotential : G.Patch → I.Parameter → ℝ
  fenchelYoung_nonnegative : ∀ i θ η,
    0 ≤ logPartition i θ + dualPotential i η -
      H.quantumFisherMetric i θ
        (naturalCoordinate i θ) (expectationCoordinate i η)
  fenchelYoung_eq_zero_iff : ∀ i θ η,
    logPartition i θ + dualPotential i η -
      H.quantumFisherMetric i θ
        (naturalCoordinate i θ) (expectationCoordinate i η) = 0 ↔ θ = η

  quantumBregmanDivergence : G.Patch → I.Parameter → I.Parameter → ℝ
  quantumBregman_eq_divergence : ∀ i θ η,
    quantumBregmanDivergence i θ η = I.divergence i θ η

  exponentialProjection : G.Patch → I.Parameter → I.Parameter
  mixtureProjection : G.Patch → I.Parameter → I.Parameter
  exponentialProjection_idempotent : ∀ i θ,
    exponentialProjection i (exponentialProjection i θ) =
      exponentialProjection i θ
  mixtureProjection_idempotent : ∀ i θ,
    mixtureProjection i (mixtureProjection i θ) = mixtureProjection i θ

  exponentialPythagorean : ∀ i θ η,
    quantumBregmanDivergence i θ η =
      quantumBregmanDivergence i θ (exponentialProjection i θ) +
      quantumBregmanDivergence i (exponentialProjection i θ) η
  mixturePythagorean : ∀ i θ η,
    quantumBregmanDivergence i θ η =
      quantumBregmanDivergence i θ (mixtureProjection i η) +
      quantumBregmanDivergence i (mixtureProjection i η) η

  projectedNaturalCoordinate_recoverable : ∀ i θ,
    H.IsPetzRecoverable i (exponentialProjection i θ)
      (naturalCoordinate i (exponentialProjection i θ))
  projectedExpectationCoordinate_recoverable : ∀ i θ,
    H.IsPetzRecoverable i (mixtureProjection i θ)
      (expectationCoordinate i (mixtureProjection i θ))

  naturalCoordinate_transport : ∀ i j θ,
    I.tangentTransport i j (naturalCoordinate i θ) =
      naturalCoordinate j (I.parameterTransport i j θ)
  expectationCoordinate_transport : ∀ i j θ,
    I.tangentTransport i j (expectationCoordinate i θ) =
      expectationCoordinate j (I.parameterTransport i j θ)
  logPartition_transport : ∀ i j θ,
    logPartition j (I.parameterTransport i j θ) = logPartition i θ
  dualPotential_transport : ∀ i j θ,
    dualPotential j (I.parameterTransport i j θ) = dualPotential i θ
  fenchelYoung_transport : ∀ i j θ η,
    logPartition j (I.parameterTransport i j θ) +
        dualPotential j (I.parameterTransport i j η) -
        H.quantumFisherMetric j (I.parameterTransport i j θ)
          (naturalCoordinate j (I.parameterTransport i j θ))
          (expectationCoordinate j (I.parameterTransport i j η)) =
      logPartition i θ + dualPotential i η -
        H.quantumFisherMetric i θ
          (naturalCoordinate i θ) (expectationCoordinate i η)
  exponentialProjection_transport : ∀ i j θ,
    I.parameterTransport i j (exponentialProjection i θ) =
      exponentialProjection j (I.parameterTransport i j θ)
  mixtureProjection_transport : ∀ i j θ,
    I.parameterTransport i j (mixtureProjection i θ) =
      mixtureProjection j (I.parameterTransport i j θ)

  genuineQuantumExponentialFamilyClaim : Prop
  genuineQuantumExponentialFamilyProof : genuineQuantumExponentialFamilyClaim
  smoothLegendreDualityClaim : Prop
  smoothLegendreDualityProof : smoothLegendreDualityClaim
  strictConvexPotentialClaim : Prop
  strictConvexPotentialProof : strictConvexPotentialClaim
  arakiBregmanIdentificationClaim : Prop
  arakiBregmanIdentificationProof : arakiBregmanIdentificationClaim
  dualAffineAutoparallelClaim : Prop
  dualAffineAutoparallelProof : dualAffineAutoparallelClaim
  quantumInformationProjectionTheoremClaim : Prop
  quantumInformationProjectionTheoremProof :
    quantumInformationProjectionTheoremClaim
  petzSufficiencyProjectionEquivalenceClaim : Prop
  petzSufficiencyProjectionEquivalenceProof :
    petzSufficiencyProjectionEquivalenceClaim
  infiniteDimensionalDuallyFlatGeometryClaim : Prop
  infiniteDimensionalDuallyFlatGeometryProof :
    infiniteDimensionalDuallyFlatGeometryClaim
  continuumQuantumExponentialFieldClaim : Prop
  continuumQuantumExponentialFieldProof :
    continuumQuantumExponentialFieldClaim
  higherStackDualAffineGeometryClaim : Prop
  higherStackDualAffineGeometryProof : higherStackDualAffineGeometryClaim

  runtimeConstructsQuantumExponentialFamily : Bool
  runtimeComputesLogPartition : Bool
  runtimeExecutesLegendreTransform : Bool
  runtimeExecutesInformationProjection : Bool
  runtimeInfersWorldIdentityFromProjection : Bool
  runtimeOptimizesWorldState : Bool
  runtimeUpdatesWorld : Bool
  noRuntimeQuantumExponentialFamilyConstruction :
    runtimeConstructsQuantumExponentialFamily = false
  noRuntimeLogPartitionComputation : runtimeComputesLogPartition = false
  noRuntimeLegendreTransform : runtimeExecutesLegendreTransform = false
  noRuntimeInformationProjection : runtimeExecutesInformationProjection = false
  noRuntimeWorldIdentityInference :
    runtimeInfersWorldIdentityFromProjection = false
  noRuntimeWorldOptimization : runtimeOptimizesWorldState = false
  noRuntimeWorldUpdate : runtimeUpdatesWorld = false

  worldNotIdentifiedWithQuantumExponentialFamily : Prop
  worldNotIdentifiedWithQuantumExponentialFamilyProof :
    worldNotIdentifiedWithQuantumExponentialFamily
  worldNotIdentifiedWithDualCoordinates : Prop
  worldNotIdentifiedWithDualCoordinatesProof :
    worldNotIdentifiedWithDualCoordinates
  worldNotIdentifiedWithInformationProjection : Prop
  worldNotIdentifiedWithInformationProjectionProof :
    worldNotIdentifiedWithInformationProjection
  zeroProjectionDefectNotOntologicalIdentity : Prop
  zeroProjectionDefectNotOntologicalIdentityProof :
    zeroProjectionDefectNotOntologicalIdentity
  dualAffineGeometryReadOnlySidecar : Prop
  dualAffineGeometryReadOnlySidecarProof : dualAffineGeometryReadOnlySidecar
  candidateNotAuthority : Prop
  candidateNotAuthorityProof : candidateNotAuthority
  validationNotTruth : Prop
  validationNotTruthProof : validationNotTruth
  multiWorldNoncollapsePreserved : Prop
  multiWorldNoncollapseProof : multiWorldNoncollapsePreserved
  nonMarkovianHistoryPreserved : Prop
  nonMarkovianHistoryProof : nonMarkovianHistoryPreserved
  twoTruthsGapPreserved : Prop
  twoTruthsGapProof : twoTruthsGapPreserved

namespace WorldQuantumExponentialDualAffineProjectionBridge

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
variable {Z : WorldModuleCategoryNimrepTubeCenterBridge F}
variable {G : WorldGaugeCategoricalIndraNetBridge Z}
variable {I : WorldInformationGeometricHigherGaugeBridge G}
variable {H : WorldArakiPetzQuantumInformationGeometryBridge I}
variable (D : WorldQuantumExponentialDualAffineProjectionBridge H)

def fenchelYoungGap
    (i : G.Patch) (θ η : I.Parameter) : ℝ :=
  D.logPartition i θ + D.dualPotential i η -
    H.quantumFisherMetric i θ
      (D.naturalCoordinate i θ) (D.expectationCoordinate i η)

def exponentialProjectionDefect
    (i : G.Patch) (θ : I.Parameter) : ℝ :=
  D.quantumBregmanDivergence i θ (D.exponentialProjection i θ)

def mixtureProjectionDefect
    (i : G.Patch) (θ : I.Parameter) : ℝ :=
  D.quantumBregmanDivergence i (D.mixtureProjection i θ) θ

theorem fenchel_young_nonnegative
    (i : G.Patch) (θ η : I.Parameter) :
    0 ≤ D.fenchelYoungGap i θ η := by
  simpa [fenchelYoungGap] using D.fenchelYoung_nonnegative i θ η

theorem fenchel_young_zero_iff
    (i : G.Patch) (θ η : I.Parameter) :
    D.fenchelYoungGap i θ η = 0 ↔ θ = η := by
  simpa [fenchelYoungGap] using D.fenchelYoung_eq_zero_iff i θ η

theorem natural_coordinate_injective
    (i : G.Patch) : Function.Injective (D.naturalCoordinate i) :=
  D.naturalCoordinate_injective i

theorem expectation_coordinate_injective
    (i : G.Patch) : Function.Injective (D.expectationCoordinate i) :=
  D.expectationCoordinate_injective i

theorem quantum_bregman_eq_divergence
    (i : G.Patch) (θ η : I.Parameter) :
    D.quantumBregmanDivergence i θ η = I.divergence i θ η :=
  D.quantumBregman_eq_divergence i θ η

theorem quantum_bregman_nonnegative
    (i : G.Patch) (θ η : I.Parameter) :
    0 ≤ D.quantumBregmanDivergence i θ η := by
  rw [D.quantum_bregman_eq_divergence]
  exact I.divergence_nonneg i θ η

theorem quantum_bregman_zero_iff
    (i : G.Patch) (θ η : I.Parameter) :
    D.quantumBregmanDivergence i θ η = 0 ↔ θ = η := by
  rw [D.quantum_bregman_eq_divergence]
  exact I.divergence_eq_zero_iff i θ η

theorem exponential_projection_idempotent
    (i : G.Patch) (θ : I.Parameter) :
    D.exponentialProjection i (D.exponentialProjection i θ) =
      D.exponentialProjection i θ :=
  D.exponentialProjection_idempotent i θ

theorem mixture_projection_idempotent
    (i : G.Patch) (θ : I.Parameter) :
    D.mixtureProjection i (D.mixtureProjection i θ) =
      D.mixtureProjection i θ :=
  D.mixtureProjection_idempotent i θ

theorem exponential_projection_defect_nonnegative
    (i : G.Patch) (θ : I.Parameter) :
    0 ≤ D.exponentialProjectionDefect i θ := by
  exact D.quantum_bregman_nonnegative i θ (D.exponentialProjection i θ)

theorem mixture_projection_defect_nonnegative
    (i : G.Patch) (θ : I.Parameter) :
    0 ≤ D.mixtureProjectionDefect i θ := by
  exact D.quantum_bregman_nonnegative i (D.mixtureProjection i θ) θ

theorem exponential_projection_defect_zero_iff_fixed
    (i : G.Patch) (θ : I.Parameter) :
    D.exponentialProjectionDefect i θ = 0 ↔
      D.exponentialProjection i θ = θ := by
  unfold exponentialProjectionDefect
  rw [D.quantum_bregman_zero_iff]
  constructor
  · intro h
    exact h.symm
  · intro h
    exact h.symm

theorem mixture_projection_defect_zero_iff_fixed
    (i : G.Patch) (θ : I.Parameter) :
    D.mixtureProjectionDefect i θ = 0 ↔
      D.mixtureProjection i θ = θ := by
  unfold mixtureProjectionDefect
  exact D.quantum_bregman_zero_iff i (D.mixtureProjection i θ) θ

theorem exponential_pythagorean
    (i : G.Patch) (θ η : I.Parameter) :
    D.quantumBregmanDivergence i θ η =
      D.quantumBregmanDivergence i θ (D.exponentialProjection i θ) +
      D.quantumBregmanDivergence i (D.exponentialProjection i θ) η :=
  D.exponentialPythagorean i θ η

theorem mixture_pythagorean
    (i : G.Patch) (θ η : I.Parameter) :
    D.quantumBregmanDivergence i θ η =
      D.quantumBregmanDivergence i θ (D.mixtureProjection i η) +
      D.quantumBregmanDivergence i (D.mixtureProjection i η) η :=
  D.mixturePythagorean i θ η

theorem projected_coordinates_are_petz_recoverable
    (i : G.Patch) (θ : I.Parameter) :
    H.IsPetzRecoverable i (D.exponentialProjection i θ)
        (D.naturalCoordinate i (D.exponentialProjection i θ)) ∧
      H.IsPetzRecoverable i (D.mixtureProjection i θ)
        (D.expectationCoordinate i (D.mixtureProjection i θ)) :=
  ⟨D.projectedNaturalCoordinate_recoverable i θ,
    D.projectedExpectationCoordinate_recoverable i θ⟩

theorem quantum_bregman_gauge_invariant
    (i j : G.Patch) (θ η : I.Parameter) :
    D.quantumBregmanDivergence j
        (I.parameterTransport i j θ) (I.parameterTransport i j η) =
      D.quantumBregmanDivergence i θ η := by
  rw [D.quantum_bregman_eq_divergence, D.quantum_bregman_eq_divergence]
  exact I.divergence_transport i j θ η

theorem fenchel_young_gauge_invariant
    (i j : G.Patch) (θ η : I.Parameter) :
    D.fenchelYoungGap j
        (I.parameterTransport i j θ) (I.parameterTransport i j η) =
      D.fenchelYoungGap i θ η := by
  simpa [fenchelYoungGap] using D.fenchelYoung_transport i j θ η

theorem exponential_projection_gauge_covariant
    (i j : G.Patch) (θ : I.Parameter) :
    I.parameterTransport i j (D.exponentialProjection i θ) =
      D.exponentialProjection j (I.parameterTransport i j θ) :=
  D.exponentialProjection_transport i j θ

theorem mixture_projection_gauge_covariant
    (i j : G.Patch) (θ : I.Parameter) :
    I.parameterTransport i j (D.mixtureProjection i θ) =
      D.mixtureProjection j (I.parameterTransport i j θ) :=
  D.mixtureProjection_transport i j θ

theorem dual_affine_projection_package :
    (∀ i θ η, 0 ≤ D.fenchelYoungGap i θ η) ∧
    (∀ i θ η, D.fenchelYoungGap i θ η = 0 ↔ θ = η) ∧
    (∀ i θ η, 0 ≤ D.quantumBregmanDivergence i θ η) ∧
    (∀ i θ η, D.quantumBregmanDivergence i θ η = 0 ↔ θ = η) ∧
    (∀ i θ, D.exponentialProjectionDefect i θ = 0 ↔
      D.exponentialProjection i θ = θ) ∧
    (∀ i θ, D.mixtureProjectionDefect i θ = 0 ↔
      D.mixtureProjection i θ = θ) :=
  ⟨D.fenchel_young_nonnegative,
    D.fenchel_young_zero_iff,
    D.quantum_bregman_nonnegative,
    D.quantum_bregman_zero_iff,
    D.exponential_projection_defect_zero_iff_fixed,
    D.mixture_projection_defect_zero_iff_fixed⟩

theorem analytic_dual_affine_receipts_complete :
    D.genuineQuantumExponentialFamilyClaim ∧
    D.smoothLegendreDualityClaim ∧
    D.strictConvexPotentialClaim ∧
    D.arakiBregmanIdentificationClaim ∧
    D.dualAffineAutoparallelClaim ∧
    D.quantumInformationProjectionTheoremClaim ∧
    D.petzSufficiencyProjectionEquivalenceClaim ∧
    D.infiniteDimensionalDuallyFlatGeometryClaim ∧
    D.continuumQuantumExponentialFieldClaim ∧
    D.higherStackDualAffineGeometryClaim :=
  ⟨D.genuineQuantumExponentialFamilyProof,
    D.smoothLegendreDualityProof,
    D.strictConvexPotentialProof,
    D.arakiBregmanIdentificationProof,
    D.dualAffineAutoparallelProof,
    D.quantumInformationProjectionTheoremProof,
    D.petzSufficiencyProjectionEquivalenceProof,
    D.infiniteDimensionalDuallyFlatGeometryProof,
    D.continuumQuantumExponentialFieldProof,
    D.higherStackDualAffineGeometryProof⟩

theorem runtime_grants_no_dual_affine_authority :
    D.runtimeConstructsQuantumExponentialFamily = false ∧
    D.runtimeComputesLogPartition = false ∧
    D.runtimeExecutesLegendreTransform = false ∧
    D.runtimeExecutesInformationProjection = false ∧
    D.runtimeInfersWorldIdentityFromProjection = false ∧
    D.runtimeOptimizesWorldState = false ∧
    D.runtimeUpdatesWorld = false :=
  ⟨D.noRuntimeQuantumExponentialFamilyConstruction,
    D.noRuntimeLogPartitionComputation,
    D.noRuntimeLegendreTransform,
    D.noRuntimeInformationProjection,
    D.noRuntimeWorldIdentityInference,
    D.noRuntimeWorldOptimization,
    D.noRuntimeWorldUpdate⟩

theorem dual_affine_representation_boundary_preserved :
    D.worldNotIdentifiedWithQuantumExponentialFamily ∧
    D.worldNotIdentifiedWithDualCoordinates ∧
    D.worldNotIdentifiedWithInformationProjection ∧
    D.zeroProjectionDefectNotOntologicalIdentity ∧
    D.dualAffineGeometryReadOnlySidecar ∧
    D.candidateNotAuthority ∧
    D.validationNotTruth ∧
    D.multiWorldNoncollapsePreserved ∧
    D.nonMarkovianHistoryPreserved ∧
    D.twoTruthsGapPreserved :=
  ⟨D.worldNotIdentifiedWithQuantumExponentialFamilyProof,
    D.worldNotIdentifiedWithDualCoordinatesProof,
    D.worldNotIdentifiedWithInformationProjectionProof,
    D.zeroProjectionDefectNotOntologicalIdentityProof,
    D.dualAffineGeometryReadOnlySidecarProof,
    D.candidateNotAuthorityProof,
    D.validationNotTruthProof,
    D.multiWorldNoncollapseProof,
    D.nonMarkovianHistoryProof,
    D.twoTruthsGapProof⟩

end WorldQuantumExponentialDualAffineProjectionBridge
end WORLD
end KUOS
