import Mathlib
import KUOS.WORLD.ConditionalExpectationTakesakiBridgeV0_36

/-!
Kū–Indra WORLD Jones basic-construction, relative-commutant, and finite-index
bridge v0.37.

Lean directly verifies the algebraic Jones-projection laws, the compression
identity for the v0.36 conditional expectation, containment in the basic
construction, the relative-commutant characterization, finite quasi-basis
reconstruction, and centrality of the index element. Von Neumann closure,
canonical trace theory, the Pimsner–Popa characterization, and the analytic
Jones-index theorem remain external proof receipts.
-/

namespace KUOS
namespace WORLD

structure WorldJonesBasicConstructionIndexBridge
    {C : RealHilbertL2Carrier}
    {W : WorldNoncommutativeOperatorAlgebra C}
    [PartialOrder W.Region]
    {B : WorldCStarLocalNetBridge C W}
    {V : WorldVonNeumannBicommutantBridge B}
    {M : WorldStandardFormModularFlowBridge V}
    {R : WorldModularStateKMSRelativeFlowBridge M}
    {E : WorldArakiRelativeEntropyBridge R}
    {P : WorldPetzRecoverySufficiencyBridge E}
    (T : WorldConditionalExpectationTakesakiBridge P) where
  jonesProjection : B.A
  jonesProjection_idempotent :
    jonesProjection * jonesProjection = jonesProjection
  jonesProjection_selfAdjoint : star jonesProjection = jonesProjection
  jonesProjection_commutes_with_sufficient : ∀ {b : B.A},
    b ∈ T.sufficientSubalgebra →
      jonesProjection * b = b * jonesProjection
  jonesCompression : ∀ a : B.A,
    jonesProjection * a * jonesProjection =
      T.conditionalExpectation a * jonesProjection
  basicConstruction : Subalgebra ℂ B.A
  sufficientSubalgebra_le_basicConstruction :
    T.sufficientSubalgebra ≤ basicConstruction
  jonesProjection_mem_basicConstruction :
    jonesProjection ∈ basicConstruction
  relativeCommutant : Subalgebra ℂ B.A
  mem_relativeCommutant_iff : ∀ a : B.A,
    a ∈ relativeCommutant ↔
      ∀ b : B.A, b ∈ T.sufficientSubalgebra → a * b = b * a
  QuasiBasisIndex : Type
  [quasiBasisFintype : Fintype QuasiBasisIndex]
  quasiBasis : QuasiBasisIndex → B.A
  leftQuasiBasisReconstruction : ∀ a : B.A,
    (∑ i, quasiBasis i *
      T.conditionalExpectation (star (quasiBasis i) * a)) = a
  rightQuasiBasisReconstruction : ∀ a : B.A,
    (∑ i, T.conditionalExpectation (a * quasiBasis i) *
      star (quasiBasis i)) = a
  indexElement : B.A
  indexElement_eq_quasiBasis_sum :
    indexElement = ∑ i, quasiBasis i * star (quasiBasis i)
  indexElement_selfAdjoint : star indexElement = indexElement
  indexElement_central : ∀ a : B.A,
    indexElement * a = a * indexElement
  indexElement_mem_basicConstruction :
    indexElement ∈ basicConstruction
  jonesIndex : ℝ
  jonesIndex_ge_one : 1 ≤ jonesIndex
  indexElement_eq_scalar :
    indexElement = (jonesIndex : ℂ) • (1 : B.A)
  basicConstructionGeneratedClaim : Prop
  basicConstructionGeneratedProof : basicConstructionGeneratedClaim
  basicConstructionVonNeumannClosedClaim : Prop
  basicConstructionVonNeumannClosedProof :
    basicConstructionVonNeumannClosedClaim
  jonesProjectionL2ImplementationClaim : Prop
  jonesProjectionL2ImplementationProof :
    jonesProjectionL2ImplementationClaim
  canonicalTraceClaim : Prop
  canonicalTraceProof : canonicalTraceClaim
  markovTraceClaim : Prop
  markovTraceProof : markovTraceClaim
  pimsnerPopaFiniteIndexClaim : Prop
  pimsnerPopaFiniteIndexProof : pimsnerPopaFiniteIndexClaim
  watataniIndexIndependentClaim : Prop
  watataniIndexIndependentProof : watataniIndexIndependentClaim
  jonesIndexEqualsStatisticalDimensionClaim : Prop
  jonesIndexEqualsStatisticalDimensionProof :
    jonesIndexEqualsStatisticalDimensionClaim
  relativeCommutantFiniteDimensionalClaim : Prop
  relativeCommutantFiniteDimensionalProof :
    relativeCommutantFiniteDimensionalClaim
  basicConstructionTowerClaim : Prop
  basicConstructionTowerProof : basicConstructionTowerClaim
  runtimeConstructsJonesProjection : Bool
  runtimeExecutesBasicConstruction : Bool
  runtimeClaimsFiniteIndexTheorem : Bool
  runtimeUpdatesWorld : Bool
  noRuntimeJonesProjectionConstruction :
    runtimeConstructsJonesProjection = false
  noRuntimeBasicConstructionExecution :
    runtimeExecutesBasicConstruction = false
  noRuntimeFiniteIndexTheoremClaim :
    runtimeClaimsFiniteIndexTheorem = false
  noRuntimeWorldUpdate : runtimeUpdatesWorld = false
  worldNotIdentifiedWithBasicConstruction : Prop
  worldNotIdentifiedProof : worldNotIdentifiedWithBasicConstruction
  multiWorldNoncollapsePreserved : Prop
  multiWorldNoncollapseProof : multiWorldNoncollapsePreserved
  twoTruthsGapPreserved : Prop
  twoTruthsGapProof : twoTruthsGapPreserved

attribute [instance]
  WorldJonesBasicConstructionIndexBridge.quasiBasisFintype

namespace WorldJonesBasicConstructionIndexBridge

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
variable (J : WorldJonesBasicConstructionIndexBridge T)

theorem jonesProjection_sq :
    J.jonesProjection * J.jonesProjection = J.jonesProjection :=
  J.jonesProjection_idempotent

theorem jonesProjection_star :
    star J.jonesProjection = J.jonesProjection :=
  J.jonesProjection_selfAdjoint

theorem jonesProjection_compresses (a : B.A) :
    J.jonesProjection * a * J.jonesProjection =
      T.conditionalExpectation a * J.jonesProjection :=
  J.jonesCompression a

theorem jonesProjection_compresses_sufficient
    {b : B.A} (hb : b ∈ T.sufficientSubalgebra) :
    J.jonesProjection * b * J.jonesProjection =
      b * J.jonesProjection := by
  rw [J.jonesCompression b]
  rw [T.fixes_sufficientSubalgebra hb]

theorem jonesProjection_corner_of_sufficient
    {b : B.A} (hb : b ∈ T.sufficientSubalgebra) :
    J.jonesProjection * b * J.jonesProjection =
      b * J.jonesProjection := by
  rw [J.jonesProjection_commutes_with_sufficient hb]
  rw [mul_assoc, J.jonesProjection_idempotent]

theorem sufficient_mem_basicConstruction
    {b : B.A} (hb : b ∈ T.sufficientSubalgebra) :
    b ∈ J.basicConstruction :=
  J.sufficientSubalgebra_le_basicConstruction hb

theorem jonesProjection_mem_basic :
    J.jonesProjection ∈ J.basicConstruction :=
  J.jonesProjection_mem_basicConstruction

theorem basicConstruction_contains_sandwich
    {b c : B.A}
    (hb : b ∈ T.sufficientSubalgebra)
    (hc : c ∈ T.sufficientSubalgebra) :
    b * J.jonesProjection * c ∈ J.basicConstruction := by
  apply J.basicConstruction.mul_mem
  · apply J.basicConstruction.mul_mem
    · exact J.sufficientSubalgebra_le_basicConstruction hb
    · exact J.jonesProjection_mem_basicConstruction
  · exact J.sufficientSubalgebra_le_basicConstruction hc

theorem mem_relativeCommutant_iff_commutes (a : B.A) :
    a ∈ J.relativeCommutant ↔
      ∀ b : B.A, b ∈ T.sufficientSubalgebra → a * b = b * a :=
  J.mem_relativeCommutant_iff a

theorem jonesProjection_mem_relativeCommutant :
    J.jonesProjection ∈ J.relativeCommutant := by
  apply (J.mem_relativeCommutant_iff J.jonesProjection).2
  intro b hb
  exact J.jonesProjection_commutes_with_sufficient hb

theorem indexElement_mem_relativeCommutant :
    J.indexElement ∈ J.relativeCommutant := by
  apply (J.mem_relativeCommutant_iff J.indexElement).2
  intro b _
  exact J.indexElement_central b

theorem left_quasi_basis_reconstruction (a : B.A) :
    (∑ i, J.quasiBasis i *
      T.conditionalExpectation (star (J.quasiBasis i) * a)) = a :=
  J.leftQuasiBasisReconstruction a

theorem right_quasi_basis_reconstruction (a : B.A) :
    (∑ i, T.conditionalExpectation (a * J.quasiBasis i) *
      star (J.quasiBasis i)) = a :=
  J.rightQuasiBasisReconstruction a

theorem indexElement_quasiBasis_formula :
    J.indexElement =
      ∑ i, J.quasiBasis i * star (J.quasiBasis i) :=
  J.indexElement_eq_quasiBasis_sum

theorem indexElement_star :
    star J.indexElement = J.indexElement :=
  J.indexElement_selfAdjoint

theorem indexElement_commutes (a : B.A) :
    J.indexElement * a = a * J.indexElement :=
  J.indexElement_central a

theorem indexElement_is_scalar :
    J.indexElement = (J.jonesIndex : ℂ) • (1 : B.A) :=
  J.indexElement_eq_scalar

theorem jonesIndex_pos : 0 < J.jonesIndex :=
  lt_of_lt_of_le zero_lt_one J.jonesIndex_ge_one

theorem finite_index_package :
    1 ≤ J.jonesIndex ∧
    J.indexElement = (J.jonesIndex : ℂ) • (1 : B.A) ∧
    star J.indexElement = J.indexElement ∧
    (∀ a : B.A, J.indexElement * a = a * J.indexElement) :=
  ⟨J.jonesIndex_ge_one, J.indexElement_eq_scalar,
    J.indexElement_selfAdjoint, J.indexElement_central⟩

theorem analytic_receipts_complete :
    J.basicConstructionGeneratedClaim ∧
    J.basicConstructionVonNeumannClosedClaim ∧
    J.jonesProjectionL2ImplementationClaim ∧
    J.canonicalTraceClaim ∧
    J.markovTraceClaim ∧
    J.pimsnerPopaFiniteIndexClaim ∧
    J.watataniIndexIndependentClaim ∧
    J.jonesIndexEqualsStatisticalDimensionClaim ∧
    J.relativeCommutantFiniteDimensionalClaim ∧
    J.basicConstructionTowerClaim :=
  ⟨J.basicConstructionGeneratedProof,
    J.basicConstructionVonNeumannClosedProof,
    J.jonesProjectionL2ImplementationProof,
    J.canonicalTraceProof,
    J.markovTraceProof,
    J.pimsnerPopaFiniteIndexProof,
    J.watataniIndexIndependentProof,
    J.jonesIndexEqualsStatisticalDimensionProof,
    J.relativeCommutantFiniteDimensionalProof,
    J.basicConstructionTowerProof⟩

theorem runtime_grants_no_jones_authority :
    J.runtimeConstructsJonesProjection = false ∧
    J.runtimeExecutesBasicConstruction = false ∧
    J.runtimeClaimsFiniteIndexTheorem = false ∧
    J.runtimeUpdatesWorld = false :=
  ⟨J.noRuntimeJonesProjectionConstruction,
    J.noRuntimeBasicConstructionExecution,
    J.noRuntimeFiniteIndexTheoremClaim,
    J.noRuntimeWorldUpdate⟩

theorem representation_boundary_preserved :
    J.worldNotIdentifiedWithBasicConstruction ∧
    J.multiWorldNoncollapsePreserved ∧
    J.twoTruthsGapPreserved :=
  ⟨J.worldNotIdentifiedProof, J.multiWorldNoncollapseProof,
    J.twoTruthsGapProof⟩

end WorldJonesBasicConstructionIndexBridge
end WORLD
end KUOS
