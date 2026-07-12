import Mathlib
import KUOS.ActOS.DukkhaPreservingBoundedAdapterInvocationV0_8

namespace KUOS.ActOS.DukkhaPreservingEffectCommitAuthorizationIntakeV0_9

open KUOS.ActOS.DukkhaPreservingBoundedAdapterInvocationV0_8

inductive EffectCommitAuthorizationDisposition where
  | effectCommitAuthorizationReady
  | worldRefreshRequired
  | effectReverificationRequired
  | checkpointReviewRequired
  | observationRouteRepairRequired
  | verificationRouteRepairRequired
  | compensationRouteRepairRequired
  | effectScopeRepairRequired
  | replayConflictRejected
  deriving DecidableEq, Repr

inductive EffectCommitAuthorizationState where
  | invokedEffectNotCommitted
  | authorizedNotCommitted
  deriving DecidableEq, Repr

structure DukkhaPreservingEffectCommitAuthorizationIntakeReceipt where
  sourceReceipt : DukkhaPreservingBoundedAdapterInvocationReceipt
  sourceInvocationReceiptDigest : String
  adapterResultEnvelopeDigest : String
  effectCommitReviewCertificateDigest : String
  effectCommitAuthorizationContextDigest : String
  effectCommitAuthorizationPolicyDigest : String
  invokedFrontierCandidateId : String
  invokedFrontierAdapterId : String
  invokedFrontierBindingDigest : String
  authorizationDisposition : EffectCommitAuthorizationDisposition
  effectCommitStateBefore : EffectCommitAuthorizationState
  effectCommitStateAfter : EffectCommitAuthorizationState
  effectCommitAuthorizationAdmitted : Bool
  effectCommitAuthorizationReceiptIssued : Bool
  singleUseEffectCommitAuthorizationReserved : Bool
  effectCommitAuthorizationTokenDigest : String
  effectCommitIntakeAdmitted : Bool
  effectCommitReviewSupported : Bool
  worldConditionsCurrent : Bool
  authorizationDelayCurrent : Bool
  commitSessionReplayFresh : Bool
  commitNonceReplayFresh : Bool
  sourceInvocationReplayFresh : Bool
  effectScopeExact : Bool
  effectCeilingExact : Bool
  checkpointSatisfied : Bool
  stopConditionsCurrent : Bool
  compensationRouteReady : Bool
  observationRouteReady : Bool
  verificationRouteReady : Bool
  adapterInvocationPerformed : Bool
  adapterLeaseUseConsumed : Bool
  effectProposalRecorded : Bool
  effectCommitRequired : Bool
  effectCommitPerformed : Bool
  toolInvocationPerformed : Bool
  externalSideEffectPerformed : Bool
  persistentWorldStateChanged : Bool
  observationIntakeRequired : Bool
  verificationDebtOpen : Bool
  checkpointGuardsPreserved : Bool
  evidenceLineagePreserved : Bool
  alternativeCandidatesPreserved : Bool
  dissentPreserved : Bool
  minorityPreserved : Bool
  dukkhaReductionSupportPreserved : Bool
  protectedGroupNonexternalizationPreserved : Bool
  futureNonexternalizationPreserved : Bool
  revisionCapacityPreserved : Bool
  persistentLoopReductionPreserved : Bool
  singleScalarUtilityNotIntroduced : Bool
  selectionRemainsDecisionOSOwned : Bool
  selectionAuthorityGrantedToActOS : Bool
  planRevisionAuthorityGrantedToActOS : Bool
  dukkhaMinimizationAuthorityGrantedToActOS : Bool
  executionAuthorityGranted : Bool
  executionPermission : Bool
  activeNow : Bool
  sourceLineage : Finset String
  resultingLineage : Finset String
  sourceResponsibility : Finset String
  resultingResponsibility : Finset String
  sourceEffectUncommitted :
    sourceReceipt.invocationStateAfter = .invokedEffectNotCommitted
  admissionMatchesReady :
    effectCommitAuthorizationAdmitted = true ↔
      authorizationDisposition = .effectCommitAuthorizationReady
  nonReadyAdmissionFalse :
    authorizationDisposition ≠ .effectCommitAuthorizationReady →
      effectCommitAuthorizationAdmitted = false
  receiptMatchesAdmission :
    effectCommitAuthorizationReceiptIssued = effectCommitAuthorizationAdmitted
  reservationMatchesAdmission :
    singleUseEffectCommitAuthorizationReserved = effectCommitAuthorizationAdmitted
  intakeMatchesAdmission :
    effectCommitIntakeAdmitted = effectCommitAuthorizationAdmitted
  stateBeforeExact :
    effectCommitStateBefore = .invokedEffectNotCommitted
  readyStateExact :
    authorizationDisposition = .effectCommitAuthorizationReady →
      effectCommitStateAfter = .authorizedNotCommitted
  nonReadyStateExact :
    authorizationDisposition ≠ .effectCommitAuthorizationReady →
      effectCommitStateAfter = .invokedEffectNotCommitted
  readyReviewSupported :
    authorizationDisposition = .effectCommitAuthorizationReady →
      effectCommitReviewSupported = true
  readyWorldCurrent :
    authorizationDisposition = .effectCommitAuthorizationReady →
      worldConditionsCurrent = true
  readyDelayCurrent :
    authorizationDisposition = .effectCommitAuthorizationReady →
      authorizationDelayCurrent = true
  readyReplayFresh :
    authorizationDisposition = .effectCommitAuthorizationReady →
      commitSessionReplayFresh = true ∧
      commitNonceReplayFresh = true ∧
      sourceInvocationReplayFresh = true
  readyEffectBoundaryExact :
    authorizationDisposition = .effectCommitAuthorizationReady →
      effectScopeExact = true ∧ effectCeilingExact = true
  readyCheckpointAndRoutes :
    authorizationDisposition = .effectCommitAuthorizationReady →
      checkpointSatisfied = true ∧
      stopConditionsCurrent = true ∧
      compensationRouteReady = true ∧
      observationRouteReady = true ∧
      verificationRouteReady = true
  lineageMonotone : sourceLineage ⊆ resultingLineage
  responsibilityMonotone : sourceResponsibility ⊆ resultingResponsibility

structure DukkhaPreservingEffectCommitAuthorizationIntakeReceiptValid
    (receipt : DukkhaPreservingEffectCommitAuthorizationIntakeReceipt) : Prop where
  source_valid :
    DukkhaPreservingBoundedAdapterInvocationReceiptValid receipt.sourceReceipt
  adapter_invocation_performed : receipt.adapterInvocationPerformed = true
  adapter_lease_consumed : receipt.adapterLeaseUseConsumed = true
  effect_proposal_recorded : receipt.effectProposalRecorded = true
  effect_commit_required : receipt.effectCommitRequired = true
  effect_commit_not_performed : receipt.effectCommitPerformed = false
  tool_not_invoked : receipt.toolInvocationPerformed = false
  external_side_effect_not_performed :
    receipt.externalSideEffectPerformed = false
  persistent_world_state_unchanged :
    receipt.persistentWorldStateChanged = false
  observation_intake_required : receipt.observationIntakeRequired = true
  verification_debt_open : receipt.verificationDebtOpen = true
  checkpoint_guards_preserved : receipt.checkpointGuardsPreserved = true
  evidence_lineage_preserved : receipt.evidenceLineagePreserved = true
  alternatives_preserved : receipt.alternativeCandidatesPreserved = true
  dissent_preserved : receipt.dissentPreserved = true
  minority_preserved : receipt.minorityPreserved = true
  dukkha_reduction_support_preserved :
    receipt.dukkhaReductionSupportPreserved = true
  protected_group_nonexternalization_preserved :
    receipt.protectedGroupNonexternalizationPreserved = true
  future_nonexternalization_preserved :
    receipt.futureNonexternalizationPreserved = true
  revision_capacity_preserved : receipt.revisionCapacityPreserved = true
  persistent_loop_reduction_preserved :
    receipt.persistentLoopReductionPreserved = true
  scalar_utility_not_introduced :
    receipt.singleScalarUtilityNotIntroduced = true
  selection_remains_decisionos_owned :
    receipt.selectionRemainsDecisionOSOwned = true
  selection_authority_not_granted :
    receipt.selectionAuthorityGrantedToActOS = false
  plan_revision_authority_not_granted :
    receipt.planRevisionAuthorityGrantedToActOS = false
  dukkha_minimization_authority_not_granted :
    receipt.dukkhaMinimizationAuthorityGrantedToActOS = false
  execution_authority_not_granted :
    receipt.executionAuthorityGranted = false
  execution_permission_false : receipt.executionPermission = false
  active_now_false : receipt.activeNow = false

theorem invoked_uncommitted_effect_is_required_for_commit_authorization
    (receipt : DukkhaPreservingEffectCommitAuthorizationIntakeReceipt) :
    receipt.sourceReceipt.invocationStateAfter = .invokedEffectNotCommitted ∧
      receipt.effectCommitStateBefore = .invokedEffectNotCommitted := by
  exact ⟨receipt.sourceEffectUncommitted, receipt.stateBeforeExact⟩

theorem ready_commit_authorization_reserves_single_use_token_without_commit
    (receipt : DukkhaPreservingEffectCommitAuthorizationIntakeReceipt)
    (valid : DukkhaPreservingEffectCommitAuthorizationIntakeReceiptValid receipt)
    (ready :
      receipt.authorizationDisposition = .effectCommitAuthorizationReady) :
    receipt.effectCommitAuthorizationAdmitted = true ∧
      receipt.effectCommitAuthorizationReceiptIssued = true ∧
      receipt.singleUseEffectCommitAuthorizationReserved = true ∧
      receipt.effectCommitIntakeAdmitted = true ∧
      receipt.effectCommitStateAfter = .authorizedNotCommitted ∧
      receipt.effectCommitPerformed = false := by
  have admitted : receipt.effectCommitAuthorizationAdmitted = true :=
    receipt.admissionMatchesReady.mpr ready
  exact ⟨admitted,
    receipt.receiptMatchesAdmission.trans admitted,
    receipt.reservationMatchesAdmission.trans admitted,
    receipt.intakeMatchesAdmission.trans admitted,
    receipt.readyStateExact ready,
    valid.effect_commit_not_performed⟩

theorem nonready_commit_authorization_issues_no_authorization
    (receipt : DukkhaPreservingEffectCommitAuthorizationIntakeReceipt)
    (notReady :
      receipt.authorizationDisposition ≠ .effectCommitAuthorizationReady) :
    receipt.effectCommitAuthorizationAdmitted = false ∧
      receipt.effectCommitAuthorizationReceiptIssued = false ∧
      receipt.singleUseEffectCommitAuthorizationReserved = false ∧
      receipt.effectCommitIntakeAdmitted = false ∧
      receipt.effectCommitStateAfter = .invokedEffectNotCommitted := by
  have denied := receipt.nonReadyAdmissionFalse notReady
  exact ⟨denied,
    receipt.receiptMatchesAdmission.trans denied,
    receipt.reservationMatchesAdmission.trans denied,
    receipt.intakeMatchesAdmission.trans denied,
    receipt.nonReadyStateExact notReady⟩

theorem ready_commit_authorization_requires_current_exact_routes
    (receipt : DukkhaPreservingEffectCommitAuthorizationIntakeReceipt)
    (ready :
      receipt.authorizationDisposition = .effectCommitAuthorizationReady) :
    receipt.effectCommitReviewSupported = true ∧
      receipt.worldConditionsCurrent = true ∧
      receipt.authorizationDelayCurrent = true ∧
      receipt.commitSessionReplayFresh = true ∧
      receipt.commitNonceReplayFresh = true ∧
      receipt.sourceInvocationReplayFresh = true ∧
      receipt.effectScopeExact = true ∧
      receipt.effectCeilingExact = true ∧
      receipt.checkpointSatisfied = true ∧
      receipt.stopConditionsCurrent = true ∧
      receipt.compensationRouteReady = true ∧
      receipt.observationRouteReady = true ∧
      receipt.verificationRouteReady = true := by
  rcases receipt.readyReplayFresh ready with ⟨sessionFresh, nonceFresh, sourceFresh⟩
  rcases receipt.readyEffectBoundaryExact ready with ⟨scopeExact, ceilingExact⟩
  rcases receipt.readyCheckpointAndRoutes ready with
    ⟨checkpoint, stopCurrent, compensation, observation, verification⟩
  exact ⟨receipt.readyReviewSupported ready,
    receipt.readyWorldCurrent ready,
    receipt.readyDelayCurrent ready,
    sessionFresh,
    nonceFresh,
    sourceFresh,
    scopeExact,
    ceilingExact,
    checkpoint,
    stopCurrent,
    compensation,
    observation,
    verification⟩

theorem commit_authorization_preserves_dukkha_and_nonexternalization
    (receipt : DukkhaPreservingEffectCommitAuthorizationIntakeReceipt)
    (valid : DukkhaPreservingEffectCommitAuthorizationIntakeReceiptValid receipt) :
    receipt.dukkhaReductionSupportPreserved = true ∧
      receipt.protectedGroupNonexternalizationPreserved = true ∧
      receipt.futureNonexternalizationPreserved = true ∧
      receipt.revisionCapacityPreserved = true ∧
      receipt.persistentLoopReductionPreserved = true ∧
      receipt.singleScalarUtilityNotIntroduced = true := by
  exact ⟨valid.dukkha_reduction_support_preserved,
    valid.protected_group_nonexternalization_preserved,
    valid.future_nonexternalization_preserved,
    valid.revision_capacity_preserved,
    valid.persistent_loop_reduction_preserved,
    valid.scalar_utility_not_introduced⟩

theorem commit_authorization_preserves_alternatives_dissent_and_minority
    (receipt : DukkhaPreservingEffectCommitAuthorizationIntakeReceipt)
    (valid : DukkhaPreservingEffectCommitAuthorizationIntakeReceiptValid receipt) :
    receipt.alternativeCandidatesPreserved = true ∧
      receipt.dissentPreserved = true ∧
      receipt.minorityPreserved = true := by
  exact ⟨valid.alternatives_preserved,
    valid.dissent_preserved,
    valid.minority_preserved⟩

theorem commit_authorization_preserves_lineage_and_responsibility
    (receipt : DukkhaPreservingEffectCommitAuthorizationIntakeReceipt) :
    receipt.sourceLineage ⊆ receipt.resultingLineage ∧
      receipt.sourceResponsibility ⊆ receipt.resultingResponsibility := by
  exact ⟨receipt.lineageMonotone, receipt.responsibilityMonotone⟩

theorem commit_authorization_grants_no_selection_revision_or_minimization_authority
    (receipt : DukkhaPreservingEffectCommitAuthorizationIntakeReceipt)
    (valid : DukkhaPreservingEffectCommitAuthorizationIntakeReceiptValid receipt) :
    receipt.selectionRemainsDecisionOSOwned = true ∧
      receipt.selectionAuthorityGrantedToActOS = false ∧
      receipt.planRevisionAuthorityGrantedToActOS = false ∧
      receipt.dukkhaMinimizationAuthorityGrantedToActOS = false := by
  exact ⟨valid.selection_remains_decisionos_owned,
    valid.selection_authority_not_granted,
    valid.plan_revision_authority_not_granted,
    valid.dukkha_minimization_authority_not_granted⟩

theorem effect_commit_authorization_is_not_commit_external_effect_or_execution
    (receipt : DukkhaPreservingEffectCommitAuthorizationIntakeReceipt)
    (valid : DukkhaPreservingEffectCommitAuthorizationIntakeReceiptValid receipt) :
    receipt.effectCommitPerformed = false ∧
      receipt.toolInvocationPerformed = false ∧
      receipt.externalSideEffectPerformed = false ∧
      receipt.persistentWorldStateChanged = false ∧
      receipt.executionAuthorityGranted = false ∧
      receipt.executionPermission = false ∧
      receipt.activeNow = false := by
  exact ⟨valid.effect_commit_not_performed,
    valid.tool_not_invoked,
    valid.external_side_effect_not_performed,
    valid.persistent_world_state_unchanged,
    valid.execution_authority_not_granted,
    valid.execution_permission_false,
    valid.active_now_false⟩

end KUOS.ActOS.DukkhaPreservingEffectCommitAuthorizationIntakeV0_9
