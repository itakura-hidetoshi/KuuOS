import Mathlib
import KUOS.ActOS.DukkhaSupportedBoundedPlanMaterializationIntakeV0_5

namespace KUOS.ActOS.DukkhaPreservingAdapterBindingAuthorizationIntakeV0_6

open KUOS.ActOS.DukkhaSupportedBoundedPlanMaterializationIntakeV0_5

inductive ActivationAuthorizationDisposition where
  | activationAuthorizationReady
  | worldRefreshRequired
  | freshnessRefreshRequired
  | adapterRegistryRepairRequired
  | leaseRefreshRequired
  | replayConflictRejected
  | verifyOSStepReverificationRequired
  deriving DecidableEq, Repr

def admittedForDisposition
    (disposition : ActivationAuthorizationDisposition) : Bool :=
  disposition = .activationAuthorizationReady

structure CandidateAdapterBinding where
  materializationCandidateId : String
  adapterId : String
  adapterRegistryEntryDigest : String
  capabilityDigest : String
  scopeDigest : String
  effectCeilingDigest : String
  leaseId : String
  bindingDigest : String
  boundNotInvoked : Bool

structure DukkhaPreservingAdapterBindingAuthorizationIntakeReceipt where
  sourceReceipt : DukkhaSupportedBoundedPlanMaterializationIntakeReceipt
  sourceMaterializationReceiptDigest : String
  sourceVerifyOSDukkhaCertificateDigest : String
  sourcePlanReceiptDigest : String
  sourceConcretePlanDigest : String
  sourceWorldBindingDigest : String
  sourceWorldStateDigest : String
  sourceWorldRevision : Nat
  sourceWorldLineageDigest : String
  selectedCandidateId : String
  selectedCandidatePlanIntentDigest : String
  dukkhaAssessmentDigest : String
  referencePlanDigest : String
  adapterRegistrySnapshotDigest : String
  authorizationContextDigest : String
  adapterBindings : List CandidateAdapterBinding
  adapterBindingCount : Nat
  completedMaterializationCandidateIds : Finset String
  activationFrontierCandidateId : String
  frontierAdapterId : String
  frontierLeaseId : String
  authorizationDisposition : ActivationAuthorizationDisposition
  activationAuthorizationAdmitted : Bool
  activationAuthorizationReceiptIssued : Bool
  singleUseAuthorizationReserved : Bool
  leaseUseConsumed : Bool
  adapterRegistrySnapshotUnchanged : Bool
  worldConditionsCurrent : Bool
  freshnessCurrent : Bool
  adapterRegistryReady : Bool
  frontierLeaseAvailable : Bool
  sessionIntentNonceReplayFresh : Bool
  irreversibleStepReverificationSatisfied : Bool
  adapterBindingPerformed : Bool
  allMaterializationCandidatesBound : Bool
  oneToOneCandidateBindingPreserved : Bool
  activationFrontierSequencePreserved : Bool
  scopeAndEffectCeilingExact : Bool
  checkpointGuardsPreserved : Bool
  stopConditionsPreserved : Bool
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
  sourceLineage : Finset String
  resultingLineage : Finset String
  sourceResponsibility : Finset String
  resultingResponsibility : Finset String
  selectionRemainsDecisionOSOwned : Bool
  selectionAuthorityGrantedToActOS : Bool
  planRevisionAuthorityGrantedToActOS : Bool
  dukkhaMinimizationAuthorityGrantedToActOS : Bool
  planActivated : Bool
  adapterInvocationPerformed : Bool
  toolInvocationPerformed : Bool
  externalSideEffectPerformed : Bool
  executionAuthorityGranted : Bool
  executionPermission : Bool
  persistentWorldStateChanged : Bool
  activeNow : Bool
  admissionMatches :
    activationAuthorizationAdmitted =
      admittedForDisposition authorizationDisposition
  authorizationReceiptMatches :
    activationAuthorizationReceiptIssued =
      admittedForDisposition authorizationDisposition
  singleUseReservationMatches :
    singleUseAuthorizationReserved =
      admittedForDisposition authorizationDisposition
  bindingCountMatches : adapterBindingCount = adapterBindings.length
  bindingsNonempty : adapterBindings ≠ []
  lineageMonotone : sourceLineage ⊆ resultingLineage
  responsibilityMonotone : sourceResponsibility ⊆ resultingResponsibility

structure DukkhaPreservingAdapterBindingAuthorizationIntakeReceiptValid
    (receipt : DukkhaPreservingAdapterBindingAuthorizationIntakeReceipt) : Prop where
  source_valid :
    DukkhaSupportedBoundedPlanMaterializationIntakeReceiptValid
      receipt.sourceReceipt
  adapter_binding_performed : receipt.adapterBindingPerformed = true
  all_candidates_bound : receipt.allMaterializationCandidatesBound = true
  one_to_one_binding_preserved :
    receipt.oneToOneCandidateBindingPreserved = true
  frontier_sequence_preserved :
    receipt.activationFrontierSequencePreserved = true
  scope_and_effect_ceiling_exact :
    receipt.scopeAndEffectCeilingExact = true
  checkpoint_guards_preserved :
    receipt.checkpointGuardsPreserved = true
  stop_conditions_preserved :
    receipt.stopConditionsPreserved = true
  evidence_lineage_preserved :
    receipt.evidenceLineagePreserved = true
  alternative_candidates_preserved :
    receipt.alternativeCandidatesPreserved = true
  dissent_preserved : receipt.dissentPreserved = true
  minority_preserved : receipt.minorityPreserved = true
  dukkha_reduction_support_preserved :
    receipt.dukkhaReductionSupportPreserved = true
  protected_group_nonexternalization_preserved :
    receipt.protectedGroupNonexternalizationPreserved = true
  future_nonexternalization_preserved :
    receipt.futureNonexternalizationPreserved = true
  revision_capacity_preserved :
    receipt.revisionCapacityPreserved = true
  persistent_loop_reduction_preserved :
    receipt.persistentLoopReductionPreserved = true
  single_scalar_utility_not_introduced :
    receipt.singleScalarUtilityNotIntroduced = true
  lease_use_not_consumed : receipt.leaseUseConsumed = false
  registry_snapshot_unchanged :
    receipt.adapterRegistrySnapshotUnchanged = true
  selection_remains_decisionos_owned :
    receipt.selectionRemainsDecisionOSOwned = true
  selection_authority_not_granted :
    receipt.selectionAuthorityGrantedToActOS = false
  plan_revision_authority_not_granted :
    receipt.planRevisionAuthorityGrantedToActOS = false
  dukkha_minimization_authority_not_granted :
    receipt.dukkhaMinimizationAuthorityGrantedToActOS = false
  plan_not_activated : receipt.planActivated = false
  adapter_not_invoked : receipt.adapterInvocationPerformed = false
  tool_not_invoked : receipt.toolInvocationPerformed = false
  external_side_effect_not_performed :
    receipt.externalSideEffectPerformed = false
  execution_authority_not_granted :
    receipt.executionAuthorityGranted = false
  execution_permission_false : receipt.executionPermission = false
  persistent_world_state_unchanged :
    receipt.persistentWorldStateChanged = false
  active_now_false : receipt.activeNow = false

theorem ready_disposition_admits_single_use_authorization
    (receipt : DukkhaPreservingAdapterBindingAuthorizationIntakeReceipt)
    (ready :
      receipt.authorizationDisposition =
        .activationAuthorizationReady) :
    receipt.activationAuthorizationAdmitted = true ∧
      receipt.activationAuthorizationReceiptIssued = true ∧
      receipt.singleUseAuthorizationReserved = true := by
  constructor
  · calc
      receipt.activationAuthorizationAdmitted =
          admittedForDisposition receipt.authorizationDisposition :=
        receipt.admissionMatches
      _ = true := by simp [admittedForDisposition, ready]
  constructor
  · calc
      receipt.activationAuthorizationReceiptIssued =
          admittedForDisposition receipt.authorizationDisposition :=
        receipt.authorizationReceiptMatches
      _ = true := by simp [admittedForDisposition, ready]
  · calc
      receipt.singleUseAuthorizationReserved =
          admittedForDisposition receipt.authorizationDisposition :=
        receipt.singleUseReservationMatches
      _ = true := by simp [admittedForDisposition, ready]

theorem refresh_route_does_not_authorize
    (receipt : DukkhaPreservingAdapterBindingAuthorizationIntakeReceipt)
    (route :
      receipt.authorizationDisposition = .worldRefreshRequired ∨
      receipt.authorizationDisposition = .freshnessRefreshRequired) :
    receipt.activationAuthorizationAdmitted = false := by
  rcases route with world | freshness
  · calc
      receipt.activationAuthorizationAdmitted =
          admittedForDisposition receipt.authorizationDisposition :=
        receipt.admissionMatches
      _ = false := by simp [admittedForDisposition, world]
  · calc
      receipt.activationAuthorizationAdmitted =
          admittedForDisposition receipt.authorizationDisposition :=
        receipt.admissionMatches
      _ = false := by simp [admittedForDisposition, freshness]

theorem repair_replay_or_reverification_route_does_not_authorize
    (receipt : DukkhaPreservingAdapterBindingAuthorizationIntakeReceipt)
    (route :
      receipt.authorizationDisposition = .adapterRegistryRepairRequired ∨
      receipt.authorizationDisposition = .leaseRefreshRequired ∨
      receipt.authorizationDisposition = .replayConflictRejected ∨
      receipt.authorizationDisposition = .verifyOSStepReverificationRequired) :
    receipt.activationAuthorizationAdmitted = false := by
  rcases route with registry | lease | replay | reverify
  · calc
      receipt.activationAuthorizationAdmitted =
          admittedForDisposition receipt.authorizationDisposition :=
        receipt.admissionMatches
      _ = false := by simp [admittedForDisposition, registry]
  · calc
      receipt.activationAuthorizationAdmitted =
          admittedForDisposition receipt.authorizationDisposition :=
        receipt.admissionMatches
      _ = false := by simp [admittedForDisposition, lease]
  · calc
      receipt.activationAuthorizationAdmitted =
          admittedForDisposition receipt.authorizationDisposition :=
        receipt.admissionMatches
      _ = false := by simp [admittedForDisposition, replay]
  · calc
      receipt.activationAuthorizationAdmitted =
          admittedForDisposition receipt.authorizationDisposition :=
        receipt.admissionMatches
      _ = false := by simp [admittedForDisposition, reverify]

theorem adapter_binding_preserves_candidate_bijection_and_frontier
    (receipt : DukkhaPreservingAdapterBindingAuthorizationIntakeReceipt)
    (valid :
      DukkhaPreservingAdapterBindingAuthorizationIntakeReceiptValid receipt) :
    receipt.adapterBindingPerformed = true ∧
      receipt.allMaterializationCandidatesBound = true ∧
      receipt.oneToOneCandidateBindingPreserved = true ∧
      receipt.activationFrontierSequencePreserved = true := by
  exact ⟨valid.adapter_binding_performed,
    valid.all_candidates_bound,
    valid.one_to_one_binding_preserved,
    valid.frontier_sequence_preserved⟩

theorem adapter_binding_preserves_scope_checkpoint_stop_and_evidence
    (receipt : DukkhaPreservingAdapterBindingAuthorizationIntakeReceipt)
    (valid :
      DukkhaPreservingAdapterBindingAuthorizationIntakeReceiptValid receipt) :
    receipt.scopeAndEffectCeilingExact = true ∧
      receipt.checkpointGuardsPreserved = true ∧
      receipt.stopConditionsPreserved = true ∧
      receipt.evidenceLineagePreserved = true := by
  exact ⟨valid.scope_and_effect_ceiling_exact,
    valid.checkpoint_guards_preserved,
    valid.stop_conditions_preserved,
    valid.evidence_lineage_preserved⟩

theorem authorization_intake_preserves_dukkha_and_nonexternalization
    (receipt : DukkhaPreservingAdapterBindingAuthorizationIntakeReceipt)
    (valid :
      DukkhaPreservingAdapterBindingAuthorizationIntakeReceiptValid receipt) :
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
    valid.single_scalar_utility_not_introduced⟩

theorem authorization_intake_preserves_alternatives_dissent_and_minority
    (receipt : DukkhaPreservingAdapterBindingAuthorizationIntakeReceipt)
    (valid :
      DukkhaPreservingAdapterBindingAuthorizationIntakeReceiptValid receipt) :
    receipt.alternativeCandidatesPreserved = true ∧
      receipt.dissentPreserved = true ∧
      receipt.minorityPreserved = true := by
  exact ⟨valid.alternative_candidates_preserved,
    valid.dissent_preserved,
    valid.minority_preserved⟩

theorem authorization_intake_preserves_lineage_and_responsibility
    (receipt : DukkhaPreservingAdapterBindingAuthorizationIntakeReceipt) :
    receipt.sourceLineage ⊆ receipt.resultingLineage ∧
      receipt.sourceResponsibility ⊆ receipt.resultingResponsibility := by
  exact ⟨receipt.lineageMonotone, receipt.responsibilityMonotone⟩

theorem authorization_intake_grants_no_selection_revision_or_minimization_authority
    (receipt : DukkhaPreservingAdapterBindingAuthorizationIntakeReceipt)
    (valid :
      DukkhaPreservingAdapterBindingAuthorizationIntakeReceiptValid receipt) :
    receipt.selectionRemainsDecisionOSOwned = true ∧
      receipt.selectionAuthorityGrantedToActOS = false ∧
      receipt.planRevisionAuthorityGrantedToActOS = false ∧
      receipt.dukkhaMinimizationAuthorityGrantedToActOS = false := by
  exact ⟨valid.selection_remains_decisionos_owned,
    valid.selection_authority_not_granted,
    valid.plan_revision_authority_not_granted,
    valid.dukkha_minimization_authority_not_granted⟩

theorem activation_authorization_is_not_activation_invocation_or_execution
    (receipt : DukkhaPreservingAdapterBindingAuthorizationIntakeReceipt)
    (valid :
      DukkhaPreservingAdapterBindingAuthorizationIntakeReceiptValid receipt) :
    receipt.planActivated = false ∧
      receipt.adapterInvocationPerformed = false ∧
      receipt.toolInvocationPerformed = false ∧
      receipt.externalSideEffectPerformed = false ∧
      receipt.executionAuthorityGranted = false ∧
      receipt.executionPermission = false ∧
      receipt.leaseUseConsumed = false ∧
      receipt.adapterRegistrySnapshotUnchanged = true ∧
      receipt.persistentWorldStateChanged = false ∧
      receipt.activeNow = false := by
  exact ⟨valid.plan_not_activated,
    valid.adapter_not_invoked,
    valid.tool_not_invoked,
    valid.external_side_effect_not_performed,
    valid.execution_authority_not_granted,
    valid.execution_permission_false,
    valid.lease_use_not_consumed,
    valid.registry_snapshot_unchanged,
    valid.persistent_world_state_unchanged,
    valid.active_now_false⟩

end KUOS.ActOS.DukkhaPreservingAdapterBindingAuthorizationIntakeV0_6
