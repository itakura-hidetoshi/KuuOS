from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_adaptive_agent_transition_kernel_v1_0 import (
    apply_adaptive_event,
    build_adaptive_event,
    validate_adaptive_state,
)
from runtime.kuuos_operational_agent_adapter_contract_v1_1 import (
    LEARNING_VERSION,
    OBSERVATION_VERSION,
    VERIFICATION_VERSION,
)
from runtime.kuuos_operational_agent_capability_registry_v1_1 import CapabilityRegistry
from runtime.kuuos_operational_agent_lease_ledger_v1_1 import (
    ExecutionLeaseUsageLedger,
)
from runtime.kuuos_operational_agent_receipt_store_v1_1 import AppendOnlyReceiptStore
from runtime.kuuos_operational_agent_recovery_v1_1 import recovery_decision_for
from runtime.kuuos_operational_agent_types_v1_1 import (
    effect_at_most,
    sha,
    validate_action_intent,
    validate_adapter_result,
    validate_capability,
    validate_execution_lease,
)

CONTROLLER_VERSION = "kuuos_operational_agent_controller_v1_1"


def _emit(state: Mapping[str, Any], kind: str, **payload: object) -> dict[str, Any]:
    event = build_adaptive_event(
        kind=kind,
        event_index=int(state["sequence"]) + 1,
        payload=payload,
    )
    return apply_adaptive_event(state, event)


def _authorization_errors(
    *,
    state: Mapping[str, Any],
    capability: Mapping[str, Any] | None,
    lease: Mapping[str, Any],
    intent: Mapping[str, Any],
    adapter_kind: str,
    lease_ledger: ExecutionLeaseUsageLedger,
) -> list[str]:
    errors: list[str] = []
    if validate_adaptive_state(state):
        errors.append("adaptive_state_invalid")
    if state.get("control_mode") != "ACTIVE":
        errors.append("adaptive_state_not_active")
    if state.get("task_stage") != "PLAN":
        errors.append("adaptive_state_not_plan_stage")
    if state.get("authority_mode") != "LEASED":
        errors.append("adaptive_state_not_leased")
    if not state.get("active_session_digest"):
        errors.append("adaptive_session_missing")

    if validate_action_intent(intent):
        errors.append("intent_validation_failed")
    if validate_execution_lease(lease):
        errors.append("lease_validation_failed")

    if capability is None:
        errors.append("capability_missing")
        return sorted(set(errors))
    if validate_capability(capability):
        errors.append("capability_validation_failed")
    if capability.get("active") is not True:
        errors.append("capability_inactive")
    if lease.get("active") is not True:
        errors.append("lease_inactive")

    owner = intent.get("owner_id")
    if state.get("owner_id") != owner or capability.get("owner_id") != owner or lease.get(
        "owner_id"
    ) != owner:
        errors.append("owner_mismatch")
    if state.get("lineage_id") != intent.get("lineage_id") or lease.get(
        "lineage_id"
    ) != intent.get("lineage_id"):
        errors.append("lineage_mismatch")
    if state.get("active_session_digest") != intent.get("session_digest") or lease.get(
        "session_digest"
    ) != intent.get("session_digest"):
        errors.append("session_mismatch")
    if capability.get("capability_id") != intent.get("capability_id") or lease.get(
        "capability_id"
    ) != intent.get("capability_id"):
        errors.append("capability_id_mismatch")
    if capability.get("adapter_kind") != intent.get("adapter_kind") or adapter_kind != intent.get(
        "adapter_kind"
    ):
        errors.append("adapter_kind_mismatch")

    state_epoch = int(state.get("epoch_index", -1))
    capability_epoch = int(capability.get("capability_epoch", -2))
    intent_epoch = int(intent.get("capability_epoch", -3))
    lease_epoch = int(lease.get("capability_epoch", -4))
    if capability_epoch != state_epoch:
        errors.append("capability_epoch_stale")
    if intent_epoch != capability_epoch:
        errors.append("capability_epoch_mismatch")
    if lease_epoch != capability_epoch:
        errors.append("lease_capability_epoch_mismatch")

    operation = str(intent.get("operation", ""))
    resource = str(intent.get("resource", ""))
    effect_class = str(intent.get("effect_class", ""))
    if operation not in capability.get("operation_allowlist", []):
        errors.append("operation_outside_capability")
    if resource not in capability.get("resource_scope", []):
        errors.append("resource_outside_capability")
    if operation not in lease.get("allowed_operations", []):
        errors.append("operation_outside_lease")
    if resource not in lease.get("resource_scope", []):
        errors.append("resource_outside_lease")
    if not effect_at_most(effect_class, str(capability.get("effect_ceiling", ""))):
        errors.append("effect_above_capability_ceiling")
    if not effect_at_most(effect_class, str(lease.get("effect_ceiling", ""))):
        errors.append("effect_above_lease_ceiling")

    sequence = int(state.get("sequence", 0))
    if sequence < int(lease.get("issued_at_sequence", 0)):
        errors.append("lease_not_yet_active")
    if sequence >= int(lease.get("expires_at_sequence", 0)):
        errors.append("lease_expired")
    if not lease.get("host_license_digest"):
        errors.append("host_license_missing")
    errors.extend(lease_ledger.can_consume(lease, intent))
    if intent.get("external_commit_requested") is True:
        errors.append("external_commit_not_supported_by_v1_1")
    return sorted(set(errors))


def _validate_observation(
    observation: Mapping[str, Any],
    *,
    intent: Mapping[str, Any],
    adapter_result: Mapping[str, Any],
) -> list[str]:
    errors: list[str] = []
    if observation.get("version") != OBSERVATION_VERSION:
        errors.append("observation_version_invalid")
    if observation.get("independent_from_adapter") is not True:
        errors.append("observation_not_independent")
    if observation.get("external_commit_observed") is not False:
        errors.append("external_commit_observed")
    if observation.get("intent_digest") != intent.get("intent_digest"):
        errors.append("observation_intent_mismatch")
    if observation.get("effect_digest") != adapter_result.get("effect_digest"):
        errors.append("observation_effect_mismatch")
    packet = dict(observation)
    digest = packet.pop("observation_digest", None)
    if digest != sha(packet):
        errors.append("observation_digest_invalid")
    return errors


def _validate_verification(
    verification: Mapping[str, Any], *, observation: Mapping[str, Any]
) -> list[str]:
    errors: list[str] = []
    if verification.get("version") != VERIFICATION_VERSION:
        errors.append("verification_version_invalid")
    if verification.get("observation_digest") != observation.get("observation_digest"):
        errors.append("verification_observation_mismatch")
    if verification.get("passed") is not True:
        errors.append("verification_failed")
    if verification.get("truth_authority_granted") is not False:
        errors.append("verification_truth_authority_invalid")
    if verification.get("root_rewrite_authority_granted") is not False:
        errors.append("verification_root_rewrite_invalid")
    packet = dict(verification)
    digest = packet.pop("verification_digest", None)
    if digest != sha(packet):
        errors.append("verification_digest_invalid")
    return errors


def _validate_learning(
    learning: Mapping[str, Any], *, verification: Mapping[str, Any]
) -> list[str]:
    errors: list[str] = []
    if learning.get("version") != LEARNING_VERSION:
        errors.append("learning_version_invalid")
    if learning.get("verification_digest") != verification.get("verification_digest"):
        errors.append("learning_verification_mismatch")
    if learning.get("future_only") is not True:
        errors.append("learning_not_future_only")
    if learning.get("current_cycle_mutated") is not False:
        errors.append("learning_current_cycle_mutation_forbidden")
    packet = dict(learning)
    digest = packet.pop("learning_digest", None)
    if digest != sha(packet):
        errors.append("learning_digest_invalid")
    return errors


def _stop(
    *,
    state: Mapping[str, Any],
    store: AppendOnlyReceiptStore,
    errors: list[str],
    adapter_invoked: bool,
) -> dict[str, Any]:
    decision = recovery_decision_for(errors)
    current = deepcopy(dict(state))
    state_valid = not validate_adaptive_state(current)
    if (
        state_valid
        and current.get("control_mode") == "ACTIVE"
        and current.get("active_session_digest")
        and decision != "CONTINUE"
    ):
        current = _emit(current, "LEASE_ANOMALY", recovery_decision=decision)
    store.append(
        record_type="OPERATIONAL_CYCLE_STOPPED",
        payload={
            "status": "HOLD",
            "errors": sorted(set(errors)),
            "recovery_decision": decision,
            "adapter_invoked": adapter_invoked,
            "external_commit_performed": False,
        },
    )
    return {
        "version": CONTROLLER_VERSION,
        "status": "HOLD",
        "recovery_decision": decision,
        "authorization_errors": sorted(set(errors)),
        "adapter_invoked": adapter_invoked,
        "external_commit_performed": False,
        "state": current,
        "receipt_count": len(store.records()),
    }


def run_operational_cycle(
    *,
    state: Mapping[str, Any],
    registry: CapabilityRegistry,
    lease: Mapping[str, Any],
    intent: Mapping[str, Any],
    adapter: Any,
    observer: Any,
    verifier: Any,
    learner: Any,
    lease_ledger: ExecutionLeaseUsageLedger,
    receipt_store: AppendOnlyReceiptStore,
) -> dict[str, Any]:
    """Run one finite, licensed operational cycle.

    The controller orders existing OS responsibilities.  It does not mint a
    capability, lease, host license, truth claim, external commit, root rewrite or
    successor-cycle authority.
    """

    current = deepcopy(dict(state))
    receipt_store.append(
        record_type="OPERATIONAL_CYCLE_OPENED",
        payload={
            "controller_version": CONTROLLER_VERSION,
            "state_digest": current.get("adaptive_control_state_digest", ""),
            "intent_digest": intent.get("intent_digest", ""),
        },
    )
    capability = registry.get(str(intent.get("capability_id", "")))
    errors = _authorization_errors(
        state=current,
        capability=capability,
        lease=lease,
        intent=intent,
        adapter_kind=str(getattr(adapter, "adapter_kind", "")),
        lease_ledger=lease_ledger,
    )
    if errors:
        receipt_store.append(
            record_type="AUTHORIZATION_DENIED",
            payload={"errors": errors, "recovery_decision": recovery_decision_for(errors)},
        )
        return _stop(
            state=current,
            store=receipt_store,
            errors=errors,
            adapter_invoked=False,
        )

    assert capability is not None
    receipt_store.append(
        record_type="AUTHORIZATION_PASSED",
        payload={
            "capability_digest": capability["capability_digest"],
            "lease_digest": lease["lease_digest"],
            "intent_digest": intent["intent_digest"],
        },
    )
    usage = lease_ledger.reserve(
        lease=lease,
        intent=intent,
        session_digest=str(current["active_session_digest"]),
    )
    receipt_store.append(record_type="LEASE_USE_RESERVED", payload=usage)
    current = _emit(current, "ACT_AUTHORIZED")

    try:
        adapter_result = dict(adapter.stage(intent))
    except Exception as exc:  # adapter failures are converted into bounded recovery
        receipt_store.append(
            record_type="ADAPTER_FAILED",
            payload={"error_type": type(exc).__name__, "error": str(exc)},
        )
        return _stop(
            state=current,
            store=receipt_store,
            errors=["adapter_exception"],
            adapter_invoked=True,
        )

    result_errors = validate_adapter_result(adapter_result)
    if adapter_result.get("intent_digest") != intent.get("intent_digest"):
        result_errors.append("adapter_intent_mismatch")
    if adapter_result.get("adapter_kind") != getattr(adapter, "adapter_kind", ""):
        result_errors.append("adapter_kind_mismatch")
    if result_errors:
        receipt_store.append(
            record_type="ADAPTER_RESULT_REJECTED", payload={"errors": result_errors}
        )
        return _stop(
            state=current,
            store=receipt_store,
            errors=["adapter_result_invalid", *result_errors],
            adapter_invoked=True,
        )

    receipt_store.append(
        record_type="ACTOS_STAGED_EFFECT", payload={"adapter_result": adapter_result}
    )
    current = _emit(current, "EFFECT_RECORDED")

    try:
        observation = dict(observer.observe(intent=intent, adapter_result=adapter_result))
    except Exception as exc:
        receipt_store.append(
            record_type="OBSERVATION_FAILED",
            payload={"error_type": type(exc).__name__, "error": str(exc)},
        )
        return _stop(
            state=current,
            store=receipt_store,
            errors=["observer_exception"],
            adapter_invoked=True,
        )
    observation_errors = _validate_observation(
        observation, intent=intent, adapter_result=adapter_result
    )
    if observation_errors:
        receipt_store.append(
            record_type="OBSERVATION_REJECTED", payload={"errors": observation_errors}
        )
        return _stop(
            state=current,
            store=receipt_store,
            errors=["observation_invalid", *observation_errors],
            adapter_invoked=True,
        )
    receipt_store.append(record_type="OBSERVEOS_EVIDENCE", payload=observation)
    current = _emit(
        current,
        "OBSERVATION_COMMITTED",
        evidence_digest=observation["observation_digest"],
    )

    try:
        verification = dict(
            verifier.verify(
                intent=intent,
                adapter_result=adapter_result,
                observation=observation,
            )
        )
    except Exception as exc:
        receipt_store.append(
            record_type="VERIFICATION_FAILED_TO_RUN",
            payload={"error_type": type(exc).__name__, "error": str(exc)},
        )
        return _stop(
            state=current,
            store=receipt_store,
            errors=["verifier_exception"],
            adapter_invoked=True,
        )
    verification_errors = _validate_verification(
        verification, observation=observation
    )
    if verification_errors:
        verification_digest = str(verification.get("verification_digest", sha(verification)))
        current = _emit(
            current,
            "VERIFICATION_FAILED",
            verification_digest=verification_digest,
            recovery_decision="REVALIDATE",
        )
        receipt_store.append(
            record_type="VERIFYOS_REJECTED",
            payload={"verification": verification, "errors": verification_errors},
        )
        return {
            "version": CONTROLLER_VERSION,
            "status": "HOLD",
            "recovery_decision": "REVALIDATE",
            "authorization_errors": verification_errors,
            "adapter_invoked": True,
            "external_commit_performed": False,
            "state": current,
            "receipt_count": len(receipt_store.records()),
        }
    receipt_store.append(record_type="VERIFYOS_PASSED", payload=verification)
    current = _emit(
        current,
        "VERIFICATION_PASSED",
        verification_digest=verification["verification_digest"],
    )

    try:
        learning = dict(
            learner.learn(
                intent=intent,
                observation=observation,
                verification=verification,
            )
        )
    except Exception as exc:
        receipt_store.append(
            record_type="LEARNING_FAILED",
            payload={"error_type": type(exc).__name__, "error": str(exc)},
        )
        return _stop(
            state=current,
            store=receipt_store,
            errors=["learner_exception"],
            adapter_invoked=True,
        )
    learning_errors = _validate_learning(learning, verification=verification)
    if learning_errors:
        receipt_store.append(
            record_type="LEARNING_REJECTED", payload={"errors": learning_errors}
        )
        return _stop(
            state=current,
            store=receipt_store,
            errors=["learning_invalid", *learning_errors],
            adapter_invoked=True,
        )
    next_plan_digest = sha(
        {
            "kind": "future_only_next_plan_basis",
            "source_plan_digest": state.get("plan_digest", ""),
            "learning_digest": learning["learning_digest"],
        }
    )
    receipt_store.append(
        record_type="LEARNOS_FUTURE_ONLY_DELTA",
        payload={"learning": learning, "next_plan_digest": next_plan_digest},
    )
    current = _emit(
        current,
        "LEARNING_COMMITTED",
        next_plan_digest=next_plan_digest,
    )
    receipt_store.append(
        record_type="OPERATIONAL_CYCLE_CLOSED",
        payload={
            "status": "COMPLETED",
            "effect_digest": adapter_result["effect_digest"],
            "observation_digest": observation["observation_digest"],
            "verification_digest": verification["verification_digest"],
            "learning_digest": learning["learning_digest"],
            "next_plan_digest": next_plan_digest,
            "external_commit_performed": False,
            "successor_authority_granted": False,
        },
    )
    receipt_errors = receipt_store.validate()
    if receipt_errors:
        raise ValueError("receipt_chain_invalid:" + ";".join(receipt_errors))
    return {
        "version": CONTROLLER_VERSION,
        "status": "COMPLETED",
        "recovery_decision": "CONTINUE",
        "authorization_errors": [],
        "adapter_invoked": True,
        "external_commit_performed": False,
        "adapter_result": adapter_result,
        "observation": observation,
        "verification": verification,
        "learning": learning,
        "state": current,
        "receipt_count": len(receipt_store.records()),
    }
