import Mathlib
import KUOS.Architecture.QiWorldLicensedEffectEvidenceClosureV1_8

/-!
Qi–WORLD licensed cycle receipt v1.9.

v1.9 seals a v1.7 licensed effect together with its v1.8 native evidence
closure into one immutable, append-only cycle receipt.  The consumed authority
is neither renewable nor inheritable.  A successor cycle may expose a fresh
authority requirement, but no successor ActOS activation occurs until a new
explicit discharge is supplied.
-/

namespace KUOS.Architecture

structure LicensedCycleTerminalLineage where
  handoffReceiptDigest : Nat
  closureReceiptDigest : Nat
  authorityConsumptionDigest : Nat
  terminalStateDigest : Nat
  successorBasisDigest : Nat
  sourceHandoffBoundToClosure : Prop
  source_handoff_bound_to_closure : sourceHandoffBoundToClosure

structure ClosedLicensedCycleBoundary where
  cycleStarted : Bool
  effectRecorded : Bool
  observationClosed : Bool
  verificationClosed : Bool
  learningClosed : Bool
  replanClosed : Bool
  cycleClosed : Bool
  receiptReplayForbidden : Bool
  receiptConsumptionCount : Nat
  closedCycleImmutable : Bool
  closedCycleAppendOnly : Bool
  cycle_started : cycleStarted = true
  effect_recorded : effectRecorded = true
  observation_closed : observationClosed = true
  verification_closed : verificationClosed = true
  learning_closed : learningClosed = true
  replan_closed : replanClosed = true
  cycle_closed : cycleClosed = true
  replay_forbidden : receiptReplayForbidden = true
  receipt_not_consumed : receiptConsumptionCount = 0
  immutable : closedCycleImmutable = true
  append_only : closedCycleAppendOnly = true

structure ConsumedAuthorityBoundary where
  consumptionCount : Nat
  singleUse : Bool
  renewable : Bool
  inheritable : Bool
  consumption_once : consumptionCount = 1
  single_use : singleUse = true
  not_renewable : renewable = false
  not_inheritable : inheritable = false

structure SuccessorAuthorityRequirement where
  predecessorCycleOrdinal : Nat
  targetCycleOrdinal : Nat
  freshExternalAuthorityRequired : Bool
  distinctAuthorityDigestRequired : Bool
  newHumanApprovalRequired : Bool
  newHostLicenseRequired : Bool
  externalIssuerRequired : Bool
  selfIssueForbidden : Bool
  singleUseRequired : Bool
  predecessorReceiptReadOnly : Bool
  successorActStarted : Bool
  explicitDischargeStillRequired : Bool
  target_is_successor : targetCycleOrdinal = predecessorCycleOrdinal + 1
  fresh_authority_required : freshExternalAuthorityRequired = true
  distinct_authority_required : distinctAuthorityDigestRequired = true
  new_human_approval_required : newHumanApprovalRequired = true
  new_host_license_required : newHostLicenseRequired = true
  external_issuer_required : externalIssuerRequired = true
  self_issue_forbidden : selfIssueForbidden = true
  single_use_required : singleUseRequired = true
  predecessor_read_only : predecessorReceiptReadOnly = true
  successor_act_not_started : successorActStarted = false
  explicit_discharge_required : explicitDischargeStillRequired = true

structure SuccessorAuthorityFreshnessIntake where
  authorityDigestDistinct : Bool
  humanApprovalDistinct : Bool
  hostLicenseDistinct : Bool
  externalIssuer : Bool
  selfIssued : Bool
  singleUse : Bool
  boundToNextPlan : Bool
  freshnessQualified : Bool
  predecessorAuthorityInherited : Bool
  predecessorAuthorityRenewed : Bool
  successorActStarted : Bool
  explicitDischargeStillRequired : Bool
  authority_distinct : authorityDigestDistinct = true
  approval_distinct : humanApprovalDistinct = true
  host_distinct : hostLicenseDistinct = true
  external_issuer : externalIssuer = true
  not_self_issued : selfIssued = false
  single_use : singleUse = true
  bound_to_next_plan : boundToNextPlan = true
  freshness_qualified : freshnessQualified = true
  predecessor_not_inherited : predecessorAuthorityInherited = false
  predecessor_not_renewed : predecessorAuthorityRenewed = false
  successor_act_not_started : successorActStarted = false
  explicit_discharge_required : explicitDischargeStillRequired = true

structure QiWorldLicensedCycleReceipt where
  sourceClosure : QiWorldLicensedEffectEvidenceClosure
  lineage : LicensedCycleTerminalLineage
  closedBoundary : ClosedLicensedCycleBoundary
  consumedAuthority : ConsumedAuthorityBoundary
  successorRequirement : SuccessorAuthorityRequirement
  successorIntake : SuccessorAuthorityFreshnessIntake

  allPostEffectBlockersActive : AllBlockersActive sourceClosure.blockerVector
  nextActStarted : Bool
  next_act_not_started : nextActStarted = false
  indraTransportRealized : Bool
  indra_transport_unrealized : indraTransportRealized = false
  exactWorldUpdated : Bool
  no_exact_world_update : exactWorldUpdated = false
  historyOverwritten : Bool
  no_history_overwrite : historyOverwritten = false
  truthPromoted : Bool
  no_truth_promotion : truthPromoted = false

  receiptGrantsExecution : Bool
  no_execution_authority : receiptGrantsExecution = false
  receiptIssuesSuccessorAuthority : Bool
  no_successor_authority_issue : receiptIssuesSuccessorAuthority = false
  receiptRenewsConsumedAuthority : Bool
  no_consumed_authority_renewal : receiptRenewsConsumedAuthority = false

namespace QiWorldLicensedCycleReceipt

variable (R : QiWorldLicensedCycleReceipt)

theorem source_cycle_was_fully_closed :
    R.closedBoundary.cycleStarted = true ∧
    R.closedBoundary.effectRecorded = true ∧
    R.closedBoundary.observationClosed = true ∧
    R.closedBoundary.verificationClosed = true ∧
    R.closedBoundary.learningClosed = true ∧
    R.closedBoundary.replanClosed = true ∧
    R.closedBoundary.cycleClosed = true :=
  ⟨R.closedBoundary.cycle_started,
    R.closedBoundary.effect_recorded,
    R.closedBoundary.observation_closed,
    R.closedBoundary.verification_closed,
    R.closedBoundary.learning_closed,
    R.closedBoundary.replan_closed,
    R.closedBoundary.cycle_closed⟩

theorem closed_receipt_is_immutable_append_only_evidence :
    R.closedBoundary.receiptReplayForbidden = true ∧
    R.closedBoundary.receiptConsumptionCount = 0 ∧
    R.closedBoundary.closedCycleImmutable = true ∧
    R.closedBoundary.closedCycleAppendOnly = true :=
  ⟨R.closedBoundary.replay_forbidden,
    R.closedBoundary.receipt_not_consumed,
    R.closedBoundary.immutable,
    R.closedBoundary.append_only⟩

theorem consumed_authority_cannot_cross_cycle :
    R.consumedAuthority.consumptionCount = 1 ∧
    R.consumedAuthority.singleUse = true ∧
    R.consumedAuthority.renewable = false ∧
    R.consumedAuthority.inheritable = false :=
  ⟨R.consumedAuthority.consumption_once,
    R.consumedAuthority.single_use,
    R.consumedAuthority.not_renewable,
    R.consumedAuthority.not_inheritable⟩

theorem successor_requires_fresh_external_authority :
    R.successorRequirement.targetCycleOrdinal =
      R.successorRequirement.predecessorCycleOrdinal + 1 ∧
    R.successorRequirement.freshExternalAuthorityRequired = true ∧
    R.successorRequirement.distinctAuthorityDigestRequired = true ∧
    R.successorRequirement.newHumanApprovalRequired = true ∧
    R.successorRequirement.newHostLicenseRequired = true ∧
    R.successorRequirement.successorActStarted = false ∧
    R.successorRequirement.explicitDischargeStillRequired = true :=
  ⟨R.successorRequirement.target_is_successor,
    R.successorRequirement.fresh_authority_required,
    R.successorRequirement.distinct_authority_required,
    R.successorRequirement.new_human_approval_required,
    R.successorRequirement.new_host_license_required,
    R.successorRequirement.successor_act_not_started,
    R.successorRequirement.explicit_discharge_required⟩

theorem freshness_intake_does_not_activate_successor :
    R.successorIntake.authorityDigestDistinct = true ∧
    R.successorIntake.humanApprovalDistinct = true ∧
    R.successorIntake.hostLicenseDistinct = true ∧
    R.successorIntake.freshnessQualified = true ∧
    R.successorIntake.predecessorAuthorityInherited = false ∧
    R.successorIntake.predecessorAuthorityRenewed = false ∧
    R.successorIntake.successorActStarted = false ∧
    R.successorIntake.explicitDischargeStillRequired = true :=
  ⟨R.successorIntake.authority_distinct,
    R.successorIntake.approval_distinct,
    R.successorIntake.host_distinct,
    R.successorIntake.freshness_qualified,
    R.successorIntake.predecessor_not_inherited,
    R.successorIntake.predecessor_not_renewed,
    R.successorIntake.successor_act_not_started,
    R.successorIntake.explicit_discharge_required⟩

theorem licensed_cycle_receipt_boundary :
    R.closedBoundary.cycleClosed = true ∧
    R.closedBoundary.receiptReplayForbidden = true ∧
    R.closedBoundary.receiptConsumptionCount = 0 ∧
    R.consumedAuthority.consumptionCount = 1 ∧
    R.consumedAuthority.renewable = false ∧
    R.consumedAuthority.inheritable = false ∧
    R.successorRequirement.freshExternalAuthorityRequired = true ∧
    R.successorRequirement.successorActStarted = false ∧
    R.successorIntake.freshnessQualified = true ∧
    R.successorIntake.successorActStarted = false ∧
    R.nextActStarted = false ∧
    R.indraTransportRealized = false ∧
    R.exactWorldUpdated = false ∧
    AllBlockersActive R.sourceClosure.blockerVector :=
  ⟨R.closedBoundary.cycle_closed,
    R.closedBoundary.replay_forbidden,
    R.closedBoundary.receipt_not_consumed,
    R.consumedAuthority.consumption_once,
    R.consumedAuthority.not_renewable,
    R.consumedAuthority.not_inheritable,
    R.successorRequirement.fresh_authority_required,
    R.successorRequirement.successor_act_not_started,
    R.successorIntake.freshness_qualified,
    R.successorIntake.successor_act_not_started,
    R.next_act_not_started,
    R.indra_transport_unrealized,
    R.no_exact_world_update,
    R.allPostEffectBlockersActive⟩

end QiWorldLicensedCycleReceipt
end KUOS.Architecture
