import Mathlib.Analysis.InnerProductSpace.LinearPMap
import KUOS.WORLD.KuuVacuumArakiHessianPhysicalRealizationV0_56

/-!
WORLD v0.57 relative-Tomita closability foundation.

The Tomita map is conjugate-linear over `ℂ`, hence linear over `ℝ`.  This module
uses mathlib's `LinearPMap` theory on the underlying real Hilbert space.

A densely defined Tomita core together with a densely defined formal-adjoint
core yields a closed extension, namely the adjoint of the formal-adjoint core.
Lean then proves closability, existence of the closed graph closure, closedness
of the closure, and the core property.  These are no longer stored as analytic
claim/proof receipts.
-/

namespace KUOS
namespace WORLD

noncomputable section

/--
A real-linear core presentation of a relative Tomita operator on a Hilbert
space.  Real linearity is the correct linearized carrier for a complex
conjugate-linear Tomita map.
-/
structure RelativeTomitaCore
    (H : Type*)
    [NormedAddCommGroup H]
    [InnerProductSpace ℝ H]
    [CompleteSpace H] where
  referenceDomain : Submodule ℝ H
  referenceDomainDense : Dense (referenceDomain : Set H)
  relativeTomitaMap : referenceDomain →ₗ[ℝ] H

  formalAdjointDomain : Submodule ℝ H
  formalAdjointDomainDense : Dense (formalAdjointDomain : Set H)
  formalAdjointMap : formalAdjointDomain →ₗ[ℝ] H

  formalAdjointPairing :
    (relativeTomitaMap.toPMap referenceDomain).IsFormalAdjoint
      (formalAdjointMap.toPMap formalAdjointDomain)

namespace RelativeTomitaCore

variable {H : Type*}
variable [NormedAddCommGroup H]
variable [InnerProductSpace ℝ H]
variable [CompleteSpace H]
variable (T : RelativeTomitaCore H)

/-- The densely defined relative Tomita operator. -/
def relativeTomita : H →ₗ.[ℝ] H :=
  T.relativeTomitaMap.toPMap T.referenceDomain

/-- A densely defined formal-adjoint core. -/
def formalAdjointCore : H →ₗ.[ℝ] H :=
  T.formalAdjointMap.toPMap T.formalAdjointDomain

/-- The graph closure of the relative Tomita operator. -/
def closedRelativeTomita : H →ₗ.[ℝ] H :=
  T.relativeTomita.closure

@[simp]
theorem relativeTomita_domain :
    T.relativeTomita.domain = T.referenceDomain := by
  simp [relativeTomita]

@[simp]
theorem formalAdjointCore_domain :
    T.formalAdjointCore.domain = T.formalAdjointDomain := by
  simp [formalAdjointCore]

theorem relativeTomita_domain_dense :
    Dense (T.relativeTomita.domain : Set H) := by
  simpa [relativeTomita] using T.referenceDomainDense

theorem formalAdjointCore_domain_dense :
    Dense (T.formalAdjointCore.domain : Set H) := by
  simpa [formalAdjointCore] using T.formalAdjointDomainDense

theorem relativeTomita_isFormalAdjoint_formalAdjointCore :
    T.relativeTomita.IsFormalAdjoint T.formalAdjointCore := by
  simpa [relativeTomita, formalAdjointCore] using T.formalAdjointPairing

/-- The Tomita core is contained in the adjoint of its formal-adjoint core. -/
theorem relativeTomita_le_formalAdjointCore_adjoint :
    T.relativeTomita ≤ T.formalAdjointCore.adjoint := by
  exact LinearPMap.IsFormalAdjoint.le_adjoint
    T.formalAdjointCore_domain_dense
    T.relativeTomita_isFormalAdjoint_formalAdjointCore.symm

/-- The supplied formal-adjoint core is contained in the actual adjoint. -/
theorem formalAdjointCore_le_relativeTomita_adjoint :
    T.formalAdjointCore ≤ T.relativeTomita.adjoint := by
  exact LinearPMap.IsFormalAdjoint.le_adjoint
    T.relativeTomita_domain_dense
    T.relativeTomita_isFormalAdjoint_formalAdjointCore

/-- The adjoint of the formal-adjoint core is a closed extension. -/
theorem formalAdjointCore_adjoint_isClosed :
    T.formalAdjointCore.adjoint.IsClosed :=
  LinearPMap.adjoint_isClosed T.formalAdjointCore_domain_dense

/-- The adjoint of the relative Tomita operator is closed. -/
theorem relativeTomita_adjoint_isClosed :
    T.relativeTomita.adjoint.IsClosed :=
  LinearPMap.adjoint_isClosed T.relativeTomita_domain_dense

/--
The relative Tomita operator is closable because it has the closed extension
`formalAdjointCore.adjoint`.
-/
theorem relativeTomita_isClosable : T.relativeTomita.IsClosable := by
  rw [LinearPMap.isClosable_iff_exists_closed_extension]
  exact ⟨T.formalAdjointCore.adjoint,
    T.formalAdjointCore_adjoint_isClosed,
    T.relativeTomita_le_formalAdjointCore_adjoint⟩

/-- The formal-adjoint core is closable by the symmetric argument. -/
theorem formalAdjointCore_isClosable : T.formalAdjointCore.IsClosable := by
  rw [LinearPMap.isClosable_iff_exists_closed_extension]
  exact ⟨T.relativeTomita.adjoint,
    T.relativeTomita_adjoint_isClosed,
    T.formalAdjointCore_le_relativeTomita_adjoint⟩

/-- The closure of the relative Tomita operator is closed. -/
theorem closedRelativeTomita_isClosed :
    T.closedRelativeTomita.IsClosed := by
  exact T.relativeTomita_isClosable.closure_isClosed

/-- The original Tomita core is contained in its graph closure. -/
theorem relativeTomita_le_closedRelativeTomita :
    T.relativeTomita ≤ T.closedRelativeTomita := by
  exact LinearPMap.le_closure T.relativeTomita

/-- The topological graph closure is exactly the graph of the closed operator. -/
theorem relativeTomita_graph_closure :
    T.relativeTomita.graph.topologicalClosure =
      T.closedRelativeTomita.graph := by
  exact T.relativeTomita_isClosable.graph_closure_eq_closure_graph

/-- The original domain is a core for the closed relative Tomita operator. -/
theorem relativeTomita_domain_isCore :
    T.closedRelativeTomita.HasCore T.relativeTomita.domain := by
  exact LinearPMap.closureHasCore T.relativeTomita

end RelativeTomitaCore

structure WorldKuuVacuumRelativeTomitaClosability
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
    {H : WorldArakiPetzQuantumInformationGeometryBridge I}
    {D : WorldQuantumExponentialDualAffineProjectionBridge H}
    {Vary : WorldQuantumGeodesicMirrorDescentFreeEnergyBridge D}
    {Flow : WorldQuantumGradientJKOEntropyProductionBridge Vary}
    {Mix : WorldQuantumLogSobolevContractivityMixingBridge Flow}
    {K : WorldKuuVacuumOSHilbertCompletionBridge Mix}
    {Central : WorldKuuVacuumCentralReferenceStateBridge K}
    {Geom : WorldKuuVacuumInformationGeometryBridge Central}
    (Realization : WorldKuuVacuumArakiHessianPhysicalRealization Geom) where
  comparisonVector : M.H
  comparisonVector_mem_naturalCone : comparisonVector ∈ M.naturalCone
  comparisonVector_ne_zero : comparisonVector ≠ 0

  tomitaCore : RelativeTomitaCore M.H

  vacuumOrbitMem : ∀ observable : B.A,
    M.representation observable K.kuuVacuum ∈
      tomitaCore.referenceDomain

  relativeTomita_on_vacuumOrbit : ∀ observable : B.A,
    tomitaCore.relativeTomitaMap
        ⟨M.representation observable K.kuuVacuum,
          vacuumOrbitMem observable⟩ =
      M.representation (star observable) comparisonVector

  relativeTomitaNotExecutionAuthority : Prop
  relativeTomitaNotExecutionAuthorityProof :
    relativeTomitaNotExecutionAuthority
  closedGraphNotWorldIdentity : Prop
  closedGraphNotWorldIdentityProof : closedGraphNotWorldIdentity
  realLinearizationPreservesConjugateLinearMeaning : Prop
  realLinearizationPreservesConjugateLinearMeaningProof :
    realLinearizationPreservesConjugateLinearMeaning
  modularTimeNotPhysicalTime : Prop
  modularTimeNotPhysicalTimeProof : modularTimeNotPhysicalTime
  readOnlyAnalyticSidecar : Prop
  readOnlyAnalyticSidecarProof : readOnlyAnalyticSidecar

namespace WorldKuuVacuumRelativeTomitaClosability

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
variable {D : WorldQuantumExponentialDualAffineProjectionBridge H}
variable {Vary : WorldQuantumGeodesicMirrorDescentFreeEnergyBridge D}
variable {Flow : WorldQuantumGradientJKOEntropyProductionBridge Vary}
variable {Mix : WorldQuantumLogSobolevContractivityMixingBridge Flow}
variable {K : WorldKuuVacuumOSHilbertCompletionBridge Mix}
variable {Central : WorldKuuVacuumCentralReferenceStateBridge K}
variable {Geom : WorldKuuVacuumInformationGeometryBridge Central}
variable {Realization : WorldKuuVacuumArakiHessianPhysicalRealization Geom}
variable (Tomita : WorldKuuVacuumRelativeTomitaClosability Realization)

/-- The physical relative Tomita operator on the real-linearized Hilbert space. -/
def relativeTomita : M.H →ₗ.[ℝ] M.H :=
  Tomita.tomitaCore.relativeTomita

/-- Its closed graph closure. -/
def closedRelativeTomita : M.H →ₗ.[ℝ] M.H :=
  Tomita.tomitaCore.closedRelativeTomita

theorem relativeTomita_isClosable : Tomita.relativeTomita.IsClosable :=
  Tomita.tomitaCore.relativeTomita_isClosable

theorem closedRelativeTomita_isClosed :
    Tomita.closedRelativeTomita.IsClosed :=
  Tomita.tomitaCore.closedRelativeTomita_isClosed

theorem relativeTomita_graph_closure :
    Tomita.relativeTomita.graph.topologicalClosure =
      Tomita.closedRelativeTomita.graph :=
  Tomita.tomitaCore.relativeTomita_graph_closure

theorem relativeTomita_domain_isCore :
    Tomita.closedRelativeTomita.HasCore Tomita.relativeTomita.domain :=
  Tomita.tomitaCore.relativeTomita_domain_isCore

/-- The relative Tomita formula on the physical vacuum orbit. -/
theorem relativeTomita_on_vacuumOrbit (observable : B.A) :
    let hmem : M.representation observable K.kuuVacuum ∈
        Tomita.relativeTomita.domain := by
      simpa [relativeTomita, RelativeTomitaCore.relativeTomita] using
        Tomita.vacuumOrbitMem observable
    Tomita.relativeTomita
        ⟨M.representation observable K.kuuVacuum, hmem⟩ =
      M.representation (star observable) Tomita.comparisonVector := by
  dsimp
  simpa [relativeTomita, RelativeTomitaCore.relativeTomita] using
    Tomita.relativeTomita_on_vacuumOrbit observable

theorem comparison_vector_is_physical_nonzero_cone_vector :
    Tomita.comparisonVector ∈ M.naturalCone ∧
      Tomita.comparisonVector ≠ 0 :=
  ⟨Tomita.comparisonVector_mem_naturalCone,
    Tomita.comparisonVector_ne_zero⟩

theorem tomita_boundary_package :
    Tomita.relativeTomitaNotExecutionAuthority ∧
    Tomita.closedGraphNotWorldIdentity ∧
    Tomita.realLinearizationPreservesConjugateLinearMeaning ∧
    Tomita.modularTimeNotPhysicalTime ∧
    Tomita.readOnlyAnalyticSidecar :=
  ⟨Tomita.relativeTomitaNotExecutionAuthorityProof,
    Tomita.closedGraphNotWorldIdentityProof,
    Tomita.realLinearizationPreservesConjugateLinearMeaningProof,
    Tomita.modularTimeNotPhysicalTimeProof,
    Tomita.readOnlyAnalyticSidecarProof⟩

end WorldKuuVacuumRelativeTomitaClosability
end
end WORLD
end KUOS
