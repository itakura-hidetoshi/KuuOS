from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_decision_os_phase_v0_1 import apply_phase_payload
from runtime.kuuos_decision_os_state_v0_1 import (
    build_decision_event,
    build_initial_decision_state,
    validate_decision_state,
    validate_event_base,
)
from runtime.kuuos_decision_os_types_v0_1 import (
    ACTIVATION_RECEIPT_VERSION,
    APPLY_RESULT_VERSION,
    activation_receipt_digest,
    apply_result_digest,
    copy_non_authority,
    require_nonempty_string,
    require_nonnegative_int,
    sha,
    state_digest,
)

__all__ = [
    "apply_decision_event",
    "build_decision_event",
    "build_initial_decision_state",
    "build_replan_decision_activation_receipt",
    "validate_decision_state",
]


def _result(
    *,
    status: str,
    state: Mapping[str, Any],
    event_id: str,
    predecessor: str,
    errors: list[str],
) -> dict[str, Any]:
    value = {
        "version": APPLY_RESULT_VERSION,
        "status": status,
        "decision_event_digest": event_id,
        "predecessor_decision_state_digest": predecessor,
        "result_decision_state_digest": state["decision_state_digest"],
        "state": deepcopy(dict(state)),
        "errors": list(errors),
        "decision_apply_result_digest": "",
    }
    value["decision_apply_result_digest"] = apply_result_digest(value)
    return value


def apply_decision_event(
    state: Mapping[str, Any], event: Mapping[str, Any]
) -> dict[str, Any]:
    state_errors = validate_decision_state(state)
    if state_errors:
        raise ValueError("invalid_decision_state:" + ";".join(state_errors))
    event_id = str(event.get("decision_event_digest", ""))
    predecessor = str(state["decision_state_digest"])
    if event_id and event_id in set(state.get("processed_event_digests", [])):
        return _result(
            status="REPLAYED",
            state=state,
            event_id=event_id,
            predecessor=predecessor,
            errors=[],
        )
    errors = validate_event_base(state, event)
    if errors:
        return _result(
            status="REJECTED",
            state=state,
            event_id=event_id,
            predecessor=predecessor,
            errors=errors,
        )

    next_state = deepcopy(dict(state))
    target = str(event["target_phase"])
    try:
        apply_phase_payload(next_state, target, dict(event["payload"]))
    except (TypeError, ValueError) as exc:
        return _result(
            status="REJECTED",
            state=state,
            event_id=event_id,
            predecessor=predecessor,
            errors=[str(exc)],
        )

    next_state["predecessor_decision_state_digest"] = predecessor
    next_state["current_phase"] = target
    next_state["event_index"] = int(event["event_index"])
    next_state["updated_at_ms"] = int(event["created_at_ms"])
    next_state["processed_event_digests"] = list(
        next_state["processed_event_digests"]
    ) + [event_id]
    next_state["event_history"] = list(next_state["event_history"]) + [
        {
            "event_index": event["event_index"],
            "source_phase": event["source_phase"],
            "target_phase": target,
            "artifact_digest": event["artifact_digest"],
            "decision_event_digest": event_id,
            "created_at_ms": event["created_at_ms"],
        }
    ]

    if target == "commit":
        next_state["decision_version"] += 1
        next_state["completed_deliberations"] += 1
        next_state["latest_committed_decision_digest"] = sha(
            {
                "decision_id": next_state["decision_id"],
                "decision_version": next_state["decision_version"],
                "mission_contract_digest": next_state["mission_contract_digest"],
                "mission_state_digest": next_state["mission_state_digest"],
                "source_belief_receipt_digest": next_state[
                    "source_belief_receipt_digest"
                ],
                "route": next_state["route"],
                "selected_option_id": next_state["selected_option_id"],
                "recommended_option_ids": next_state[
                    "recommended_option_ids"
                ],
                "decision_basis_digest": next_state["decision_basis_digest"],
                "commit_event_digest": event_id,
            }
        )
        next_state["decision_summaries"] = list(
            next_state["decision_summaries"]
        ) + [
            {
                "decision_version": next_state["decision_version"],
                "route": next_state["route"],
                "selected_option_id": next_state["selected_option_id"],
                "recommended_option_ids": deepcopy(
                    next_state["recommended_option_ids"]
                ),
                "admissible_option_ids": deepcopy(
                    next_state["admissible_option_ids"]
                ),
                "retained_alternative_ids": deepcopy(
                    next_state["retained_alternative_ids"]
                ),
                "decision_basis_digest": next_state["decision_basis_digest"],
                "commit_artifact_digest": event["artifact_digest"],
                "commit_event_digest": event_id,
            }
        ]

    next_state["decision_state_digest"] = ""
    next_state["decision_state_digest"] = state_digest(next_state)
    next_errors = validate_decision_state(next_state)
    if next_errors:
        raise ValueError("next_decision_state_invalid:" + ";".join(next_errors))
    return _result(
        status="APPLIED",
        state=next_state,
        event_id=event_id,
        predecessor=predecessor,
        errors=[],
    )


def build_replan_decision_activation_receipt(
    *,
    state: Mapping[str, Any],
    mission_cycle_phase: str,
    mission_cycle_state_digest: str,
    replan_receipt_digest: str,
    next_plan_basis_digest: str,
    now_ms: int,
) -> dict[str, Any]:
    errors = validate_decision_state(state)
    if errors:
        raise ValueError("invalid_decision_state:" + ";".join(errors))
    if state.get("current_phase") != "commit":
        raise ValueError("decision_not_committed")
    if state.get("pending_replan_activation") is not True:
        raise ValueError("decision_not_pending_activation")
    if mission_cycle_phase != "replan":
        raise ValueError("mission_replan_required")
    receipt = {
        "version": ACTIVATION_RECEIPT_VERSION,
        "decision_id": state["decision_id"],
        "lineage_id": state["lineage_id"],
        "decision_state_digest": state["decision_state_digest"],
        "committed_decision_digest": state[
            "latest_committed_decision_digest"
        ],
        "decision_basis_digest": state["decision_basis_digest"],
        "route": state["route"],
        "selected_option_id": state["selected_option_id"],
        "recommended_option_ids": deepcopy(state["recommended_option_ids"]),
        "mission_cycle_state_digest": require_nonempty_string(
            mission_cycle_state_digest, "mission_cycle_state_digest"
        ),
        "mission_cycle_phase": "replan",
        "replan_receipt_digest": require_nonempty_string(
            replan_receipt_digest, "replan_receipt_digest"
        ),
        "next_plan_basis_digest": require_nonempty_string(
            next_plan_basis_digest, "next_plan_basis_digest"
        ),
        "future_only": True,
        "memory_overwrite": False,
        "decision_not_execution": True,
        "host_license_granted": False,
        "non_authority": copy_non_authority(),
        "created_at_ms": require_nonnegative_int(now_ms, "now_ms"),
        "decision_activation_receipt_digest": "",
    }
    receipt["decision_activation_receipt_digest"] = activation_receipt_digest(
        receipt
    )
    return receipt
