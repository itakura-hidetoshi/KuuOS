import Mathlib
import KUOS.Architecture.QiWorldAdaptiveTraceAdapterV1_1

/-!
Native evidence-loop convergence for the Qi–WORLD OS bridge.

The structure records the canonical digest and lineage equalities exported by
ActOS, ObserveOS, VerifyOS, and LearnOS.  It does not replace their native
validators.  Theorems expose the transitive provenance chain and preserve the
separate Governance / external-authority requirement at the Act boundary.
-/

namespace KUOS.Architecture

structure QiWorldNativeEvidenceLoop where
  lineage : Nat

  actLineage : Nat
  observeLineage : Nat
  verifyLineage : Nat
  learnLineage : Nat
  act_lineage_eq : actLineage = lineage
  observe_lineage_eq : observeLineage = lineage
  verify_lineage_eq : verifyLineage = lineage
  learn_lineage_eq : learnLineage = lineage

  sourcePlanDigest : Nat
  actDigest : Nat
  observeDigest : Nat
  verifyDigest : Nat
  learnDigest : Nat

  observeSourceActDigest : Nat
  verifySourceActDigest : Nat
  verifySourceObserveDigest : Nat
  learnSourceActDigest : Nat
  learnSourceObserveDigest : Nat
  learnSourceVerifyDigest : Nat

  observe_binds_act : observeSourceActDigest = actDigest
  verify_binds_act : verifySourceActDigest = actDigest
  verify_binds_observe : verifySourceObserveDigest = observeDigest
  learn_binds_act : learnSourceActDigest = actDigest
  learn_binds_observe : learnSourceObserveDigest = observeDigest
  learn_binds_verify : learnSourceVerifyDigest = verifyDigest

  governanceCertificatePresent : Prop
  governanceCertificateProof : governanceCertificatePresent
  externalAuthorityReceiptPresent : Prop
  externalAuthorityReceiptProof : externalAuthorityReceiptPresent

  actEffectRecorded : Prop
  actEffectRecordedProof : actEffectRecorded
  observationRecorded : Prop
  observationRecordedProof : observationRecorded
  verificationRequiredAfterObservation : Prop
  verificationRequiredAfterObservationProof : verificationRequiredAfterObservation
  verificationRecorded : Prop
  verificationRecordedProof : verificationRecorded
  learningRequiredAfterVerification : Prop
  learningRequiredAfterVerificationProof : learningRequiredAfterVerification
  learningRecorded : Prop
  learningRecordedProof : learningRecorded
  replanRequiredAfterLearning : Prop
  replanRequiredAfterLearningProof : replanRequiredAfterLearning
  learningFutureOnly : Prop
  learningFutureOnlyProof : learningFutureOnly

  worldProjectionReadOnly : Prop
  worldProjectionReadOnlyProof : worldProjectionReadOnly
  exactWorldIdentified : Bool
  exact_world_not_identified : exactWorldIdentified = false
  runtimeUpdatesWorld : Bool
  no_runtime_world_update : runtimeUpdatesWorld = false

  adapterGrantsExecution : Bool
  no_adapter_execution_authority : adapterGrantsExecution = false
  adapterIssuesAuthority : Bool
  no_adapter_authority_issue : adapterIssuesAuthority = false
  adapterOverwritesHistory : Bool
  no_adapter_history_overwrite : adapterOverwritesHistory = false

namespace QiWorldNativeEvidenceLoop

variable (L : QiWorldNativeEvidenceLoop)

theorem all_native_states_share_lineage :
    L.actLineage = L.observeLineage ∧
    L.observeLineage = L.verifyLineage ∧
    L.verifyLineage = L.learnLineage := by
  constructor
  · rw [L.act_lineage_eq, L.observe_lineage_eq]
  constructor
  · rw [L.observe_lineage_eq, L.verify_lineage_eq]
  · rw [L.verify_lineage_eq, L.learn_lineage_eq]

theorem native_provenance_chain :
    L.observeSourceActDigest = L.actDigest ∧
    L.verifySourceObserveDigest = L.observeDigest ∧
    L.learnSourceVerifyDigest = L.verifyDigest :=
  ⟨L.observe_binds_act, L.verify_binds_observe, L.learn_binds_verify⟩

theorem verification_preserves_act_provenance :
    L.verifySourceActDigest = L.actDigest :=
  L.verify_binds_act

theorem learning_preserves_full_provenance :
    L.learnSourceActDigest = L.actDigest ∧
    L.learnSourceObserveDigest = L.observeDigest ∧
    L.learnSourceVerifyDigest = L.verifyDigest :=
  ⟨L.learn_binds_act, L.learn_binds_observe, L.learn_binds_verify⟩

theorem act_requires_governance_and_external_authority :
    L.governanceCertificatePresent ∧ L.externalAuthorityReceiptPresent :=
  ⟨L.governanceCertificateProof, L.externalAuthorityReceiptProof⟩

theorem native_evidence_debt_sequence :
    L.actEffectRecorded ∧
    L.observationRecorded ∧
    L.verificationRequiredAfterObservation ∧
    L.verificationRecorded ∧
    L.learningRequiredAfterVerification ∧
    L.learningRecorded ∧
    L.replanRequiredAfterLearning :=
  ⟨L.actEffectRecordedProof,
    L.observationRecordedProof,
    L.verificationRequiredAfterObservationProof,
    L.verificationRecordedProof,
    L.learningRequiredAfterVerificationProof,
    L.learningRecordedProof,
    L.replanRequiredAfterLearningProof⟩

theorem future_only_learning_boundary : L.learningFutureOnly :=
  L.learningFutureOnlyProof

theorem world_read_only_boundary :
    L.worldProjectionReadOnly ∧
    L.exactWorldIdentified = false ∧
    L.runtimeUpdatesWorld = false :=
  ⟨L.worldProjectionReadOnlyProof,
    L.exact_world_not_identified,
    L.no_runtime_world_update⟩

theorem native_adapter_non_authority :
    L.adapterGrantsExecution = false ∧
    L.adapterIssuesAuthority = false ∧
    L.adapterOverwritesHistory = false :=
  ⟨L.no_adapter_execution_authority,
    L.no_adapter_authority_issue,
    L.no_adapter_history_overwrite⟩

theorem native_loop_safety_package :
    L.observeSourceActDigest = L.actDigest ∧
    L.verifySourceObserveDigest = L.observeDigest ∧
    L.learnSourceVerifyDigest = L.verifyDigest ∧
    L.learningFutureOnly ∧
    L.worldProjectionReadOnly ∧
    L.adapterGrantsExecution = false :=
  ⟨L.observe_binds_act,
    L.verify_binds_observe,
    L.learn_binds_verify,
    L.learningFutureOnlyProof,
    L.worldProjectionReadOnlyProof,
    L.no_adapter_execution_authority⟩

end QiWorldNativeEvidenceLoop
end KUOS.Architecture
