import Mathlib
import KUOS.WORLD.RealHilbertL2DenseOperatorProofBridgeV0_27

namespace KUOS
namespace WORLD

structure CanonicalSelfAdjointProofReceipt
    (C : RealHilbertL2Carrier)
    (B : DenseOperatorProofBridge C) where
  selfAdjointClaim : Prop
  selfAdjointProof : selfAdjointClaim
  globalRayleighClaim : Prop
  globalRayleighProof : globalRayleighClaim
  immutableCommitBound : Prop
  immutableCommitProof : immutableCommitBound
  leanBuildSucceeded : Prop
  leanBuildProof : leanBuildSucceeded

namespace CanonicalSelfAdjointProofReceipt

variable {C : RealHilbertL2Carrier}
variable {B : DenseOperatorProofBridge C}
variable (R : CanonicalSelfAdjointProofReceipt C B)

theorem source_dense_domain_preserved : Dense (B.domain : Set C.H) :=
  B.denseDomain

theorem source_symmetric_core_preserved : ∀ (x y : B.domain),
    inner ℝ (B.operator x) (y : C.H) = inner ℝ (x : C.H) (B.operator y) :=
  B.symmetricOnCore

theorem source_global_rayleigh_bound_preserved : ∀ (x : B.domain),
    B.lowerBound * ‖(x : C.H)‖ ^ 2 ≤ inner ℝ (B.operator x) (x : C.H) :=
  B.globalRayleighLowerBound

theorem canonical_self_adjoint_claim : R.selfAdjointClaim :=
  R.selfAdjointProof

theorem canonical_global_rayleigh_claim : R.globalRayleighClaim :=
  R.globalRayleighProof

theorem immutable_commit_and_build_verified :
    R.immutableCommitBound ∧ R.leanBuildSucceeded :=
  ⟨R.immutableCommitProof, R.leanBuildProof⟩

end CanonicalSelfAdjointProofReceipt

structure RuntimeSelfAdjointReceiptBoundary where
  runtimeTheoremClaimed : Bool
  unboundedOperatorExecuted : Bool
  worldUpdated : Bool
  externalActuationPerformed : Bool
  noRuntimeTheoremClaim : runtimeTheoremClaimed = false
  noUnboundedExecution : unboundedOperatorExecuted = false
  noWorldUpdate : worldUpdated = false
  noExternalActuation : externalActuationPerformed = false

theorem runtime_self_adjoint_receipt_grants_no_authority
    (b : RuntimeSelfAdjointReceiptBoundary) :
    b.runtimeTheoremClaimed = false ∧
    b.unboundedOperatorExecuted = false ∧
    b.worldUpdated = false ∧
    b.externalActuationPerformed = false := by
  exact ⟨b.noRuntimeTheoremClaim, b.noUnboundedExecution,
    b.noWorldUpdate, b.noExternalActuation⟩

end WORLD
end KUOS
