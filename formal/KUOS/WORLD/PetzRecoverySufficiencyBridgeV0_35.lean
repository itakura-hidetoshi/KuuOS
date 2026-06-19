import Mathlib
import KUOS.WORLD.ArakiRelativeEntropyBridgeV0_34

/-!
Kū–Indra WORLD Petz-recovery, sufficiency, and equality-case bridge v0.35.

Normality and complete positivity of the coarse channel and Petz recovery map,
the analytic Petz formula, and the full equality/sufficiency characterization
remain external proof receipts. Lean directly verifies unitality of the
recovered channel, exact recovery of the distinguished state pair, local-net
preservation, idempotence induced by the channel-range projection law, and the
relative-entropy equality package.
-/

namespace KUOS
namespace WORLD

structure WorldPetzRecoverySufficiencyBridge
    {C : RealHilbertL2Carrier}
    {W : WorldNoncommutativeOperatorAlgebra C}
    [PartialOrder W.Region]
    {B : WorldCStarLocalNetBridge C W}
    {V : WorldVonNeumannBicommutantBridge B}
    {M : WorldStandardFormModularFlowBridge V}
    {R : WorldModularStateKMSRelativeFlowBridge M}
    (E : WorldArakiRelativeEntropyBridge R) where
  coarseChannel : B.A →ₗ[ℂ] B.A
  petzRecovery : B.A →ₗ[ℂ] B.A
  coarseChannel_one : coarseChannel 1 = 1
  petzRecovery_one : petzRecovery 1 = 1
  coarseChannel_preserves_local : ∀ (i : W.Region) (a : B.A),
    a ∈ V.weakOperatorClosure i →
      coarseChannel a ∈ V.weakOperatorClosure i
  petzRecovery_preserves_local : ∀ (i : W.Region) (a : B.A),
    a ∈ V.weakOperatorClosure i →
      petzRecovery a ∈ V.weakOperatorClosure i
  referenceStateRecovered : ∀ a,
    R.referenceState (petzRecovery (coarseChannel a)) =
      R.referenceState a
  comparisonStateRecovered : ∀ a,
    R.comparisonState (petzRecovery (coarseChannel a)) =
      R.comparisonState a
  channelRangeProjection : ∀ a,
    coarseChannel (petzRecovery (coarseChannel a)) = coarseChannel a
  coarseRelativeEntropy : ENNReal
  dataProcessingBound :
    coarseRelativeEntropy ≤ E.globalRelativeEntropy
  entropyEquality :
    coarseRelativeEntropy = E.globalRelativeEntropy
  coarseChannelPositiveClaim : Prop
  coarseChannelPositiveProof : coarseChannelPositiveClaim
  coarseChannelCompletelyPositiveClaim : Prop
  coarseChannelCompletelyPositiveProof :
    coarseChannelCompletelyPositiveClaim
  coarseChannelNormalClaim : Prop
  coarseChannelNormalProof : coarseChannelNormalClaim
  petzRecoveryPositiveClaim : Prop
  petzRecoveryPositiveProof : petzRecoveryPositiveClaim
  petzRecoveryCompletelyPositiveClaim : Prop
  petzRecoveryCompletelyPositiveProof :
    petzRecoveryCompletelyPositiveClaim
  petzRecoveryNormalClaim : Prop
  petzRecoveryNormalProof : petzRecoveryNormalClaim
  petzFormulaClaim : Prop
  petzFormulaProof : petzFormulaClaim
  entropyEqualityIffRecoveryClaim : Prop
  entropyEqualityIffRecoveryProof : entropyEqualityIffRecoveryClaim
  sufficiencyIffRecoveryClaim : Prop
  sufficiencyIffRecoveryProof : sufficiencyIffRecoveryClaim
  modularIntertwiningClaim : Prop
  modularIntertwiningProof : modularIntertwiningClaim
  recoveryUniquenessOnSupportClaim : Prop
  recoveryUniquenessOnSupportProof : recoveryUniquenessOnSupportClaim
  runtimeConstructsNormalUCPChannel : Bool
  runtimeConstructsPetzRecovery : Bool
  runtimeClaimsEntropyEqualityTheorem : Bool
  runtimeClaimsSufficiencyTheorem : Bool
  runtimeUpdatesWorld : Bool
  noRuntimeUCPChannelConstruction :
    runtimeConstructsNormalUCPChannel = false
  noRuntimePetzConstruction : runtimeConstructsPetzRecovery = false
  noRuntimeEqualityTheoremClaim :
    runtimeClaimsEntropyEqualityTheorem = false
  noRuntimeSufficiencyTheoremClaim :
    runtimeClaimsSufficiencyTheorem = false
  noRuntimeWorldUpdate : runtimeUpdatesWorld = false
  worldNotIdentifiedWithRecoveryCarrier : Prop
  worldNotIdentifiedProof : worldNotIdentifiedWithRecoveryCarrier
  multiWorldNoncollapsePreserved : Prop
  multiWorldNoncollapseProof : multiWorldNoncollapsePreserved
  twoTruthsGapPreserved : Prop
  twoTruthsGapProof : twoTruthsGapPreserved

namespace WorldPetzRecoverySufficiencyBridge

variable {C : RealHilbertL2Carrier}
variable {W : WorldNoncommutativeOperatorAlgebra C}
variable [PartialOrder W.Region]
variable {B : WorldCStarLocalNetBridge C W}
variable {V : WorldVonNeumannBicommutantBridge B}
variable {M : WorldStandardFormModularFlowBridge V}
variable {R : WorldModularStateKMSRelativeFlowBridge M}
variable {E : WorldArakiRelativeEntropyBridge R}
variable (P : WorldPetzRecoverySufficiencyBridge E)

/-- The recovered channel `R_Petz ∘ Φ`. -/
noncomputable def recoveredChannel : B.A →ₗ[ℂ] B.A :=
  P.petzRecovery.comp P.coarseChannel

theorem recoveredChannel_apply (a : B.A) :
    P.recoveredChannel a = P.petzRecovery (P.coarseChannel a) :=
  rfl

theorem recoveredChannel_unital :
    P.recoveredChannel 1 = 1 := by
  change P.petzRecovery (P.coarseChannel 1) = 1
  rw [P.coarseChannel_one, P.petzRecovery_one]

theorem referenceState_exactly_recovered (a : B.A) :
    R.referenceState (P.recoveredChannel a) = R.referenceState a :=
  P.referenceStateRecovered a

theorem comparisonState_exactly_recovered (a : B.A) :
    R.comparisonState (P.recoveredChannel a) = R.comparisonState a :=
  P.comparisonStateRecovered a

theorem distinguished_state_pair_sufficient :
    (∀ a, R.referenceState (P.recoveredChannel a) = R.referenceState a) ∧
    (∀ a, R.comparisonState (P.recoveredChannel a) = R.comparisonState a) :=
  ⟨P.referenceStateRecovered, P.comparisonStateRecovered⟩

theorem coarseChannel_after_recovery_on_range (a : B.A) :
    P.coarseChannel (P.petzRecovery (P.coarseChannel a)) =
      P.coarseChannel a :=
  P.channelRangeProjection a

theorem recoveredChannel_idempotent (a : B.A) :
    P.recoveredChannel (P.recoveredChannel a) =
      P.recoveredChannel a := by
  change
    P.petzRecovery
        (P.coarseChannel (P.petzRecovery (P.coarseChannel a))) =
      P.petzRecovery (P.coarseChannel a)
  rw [P.channelRangeProjection a]

theorem coarseChannel_preserves_weakClosure
    (i : W.Region) {a : B.A}
    (ha : a ∈ V.weakOperatorClosure i) :
    P.coarseChannel a ∈ V.weakOperatorClosure i :=
  P.coarseChannel_preserves_local i a ha

theorem petzRecovery_preserves_weakClosure
    (i : W.Region) {a : B.A}
    (ha : a ∈ V.weakOperatorClosure i) :
    P.petzRecovery a ∈ V.weakOperatorClosure i :=
  P.petzRecovery_preserves_local i a ha

theorem recoveredChannel_preserves_weakClosure
    (i : W.Region) {a : B.A}
    (ha : a ∈ V.weakOperatorClosure i) :
    P.recoveredChannel a ∈ V.weakOperatorClosure i := by
  apply P.petzRecovery_preserves_local i
  exact P.coarseChannel_preserves_local i a ha

theorem data_processing_bound :
    P.coarseRelativeEntropy ≤ E.globalRelativeEntropy :=
  P.dataProcessingBound

theorem entropy_equality_case :
    P.coarseRelativeEntropy = E.globalRelativeEntropy :=
  P.entropyEquality

theorem reverse_data_processing_bound :
    E.globalRelativeEntropy ≤ P.coarseRelativeEntropy := by
  rw [P.entropyEquality]

theorem equality_case_package :
    P.coarseRelativeEntropy ≤ E.globalRelativeEntropy ∧
    E.globalRelativeEntropy ≤ P.coarseRelativeEntropy ∧
    P.coarseRelativeEntropy = E.globalRelativeEntropy :=
  ⟨P.dataProcessingBound, P.reverse_data_processing_bound,
    P.entropyEquality⟩

theorem channel_receipts_complete :
    P.coarseChannelPositiveClaim ∧
    P.coarseChannelCompletelyPositiveClaim ∧
    P.coarseChannelNormalClaim :=
  ⟨P.coarseChannelPositiveProof,
    P.coarseChannelCompletelyPositiveProof,
    P.coarseChannelNormalProof⟩

theorem recovery_receipts_complete :
    P.petzRecoveryPositiveClaim ∧
    P.petzRecoveryCompletelyPositiveClaim ∧
    P.petzRecoveryNormalClaim :=
  ⟨P.petzRecoveryPositiveProof,
    P.petzRecoveryCompletelyPositiveProof,
    P.petzRecoveryNormalProof⟩

theorem equality_sufficiency_receipts_complete :
    P.petzFormulaClaim ∧
    P.entropyEqualityIffRecoveryClaim ∧
    P.sufficiencyIffRecoveryClaim ∧
    P.modularIntertwiningClaim ∧
    P.recoveryUniquenessOnSupportClaim :=
  ⟨P.petzFormulaProof, P.entropyEqualityIffRecoveryProof,
    P.sufficiencyIffRecoveryProof, P.modularIntertwiningProof,
    P.recoveryUniquenessOnSupportProof⟩

theorem runtime_grants_no_recovery_authority :
    P.runtimeConstructsNormalUCPChannel = false ∧
    P.runtimeConstructsPetzRecovery = false ∧
    P.runtimeClaimsEntropyEqualityTheorem = false ∧
    P.runtimeClaimsSufficiencyTheorem = false ∧
    P.runtimeUpdatesWorld = false :=
  ⟨P.noRuntimeUCPChannelConstruction, P.noRuntimePetzConstruction,
    P.noRuntimeEqualityTheoremClaim, P.noRuntimeSufficiencyTheoremClaim,
    P.noRuntimeWorldUpdate⟩

theorem representation_boundary_preserved :
    P.worldNotIdentifiedWithRecoveryCarrier ∧
    P.multiWorldNoncollapsePreserved ∧
    P.twoTruthsGapPreserved :=
  ⟨P.worldNotIdentifiedProof, P.multiWorldNoncollapseProof,
    P.twoTruthsGapProof⟩

end WorldPetzRecoverySufficiencyBridge
end WORLD
end KUOS
