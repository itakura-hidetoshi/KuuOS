from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_plan_os_reentry_kernel_v0_7 import (
    BOUND,
    REENTERED,
    apply_reentry_event,
    build_reentry_decision,
    validate_external_reentry_receipt,
    validate_reentry_controller_state,
)
from runtime.kuuos_plan_os_ownership_continuity_types_v0_8 import (
    ACTIVE,
    BOUNDARY,
    COMPLETED,
    NON_AUTHORITY,
    STAGES,
    STAGE_RECEIPT_VERSION,
    STATE_VERSION,
    copy_boundary,
    copy_non_authority,
    require_int,
    require_string,
    stage_receipt_digest,
    state_digest,
)


def build_ownership_continuity_state(
    *,
    source_controller_state: Mapping[str, Any],
    external_reentry_receipt: Mapping[str, Any],
    reentry_decision: Mapping[str, Any],
    reentry_event: Mapping[str, Any],
    reentered_controller_state: Mapping[str, Any],
    now_ms: int,
) -> dict[str, Any]:
    source_errors = validate_reentry_controller_state(source_controller_state)
    if source_errors:
        raise ValueError("ownership_source_controller_invalid:" + ";".join(source_errors))
    if source_controller_state.get("status") != BOUND:
        raise ValueError("ownership_source_controller_must_be_bound")
    receipt_errors = validate_external_reentry_receipt(external_reentry_receipt)
    if receipt_errors:
        raise ValueError("ownership_reentry_receipt_invalid:" + ";".join(receipt_errors))
    canonical_decision = build_reentry_decision(
        controller_state=source_controller_state,
        receipt=external_reentry_receipt,
        now_ms=int(reentry_decision.get("decided_at_ms", -1)),
    )
    if canonical_decision.get("reentry_decision_digest") != reentry_decision.get(
        "reentry_decision_digest"
    ):
        raise ValueError("ownership_reentry_decision_not_canonical")
    applied = apply_reentry_event(source_controller_state, reentry_event)
    if applied.get("status") != "APPLIED":
        raise ValueError("ownership_reentry_event_not_applicable")
    reentered_errors = validate_reentry_controller_state(reentered_controller_state)
    if reentered_errors:
        raise ValueError("ownership_reentered_controller_invalid:" + ";".join(reentered_errors))
    if reentered_controller_state.get("status") != REENTERED:
        raise ValueError("ownership_controller_not_reentered")
    if applied["state"].get("reentry_controller_state_digest") != reentered_controller_state.get(
        "reentry_controller_state_digest"
    ):
        raise ValueError("ownership_reentered_state_mismatch")
    if reentry_event.get("receipt", {}).get(
        "external_reentry_receipt_digest"
    ) != external_reentry_receipt.get("external_reentry_receipt_digest"):
        raise ValueError("ownership_reentry_event_receipt_mismatch")
    if reentry_event.get("decision", {}).get(
        "reentry_decision_digest"
    ) != reentry_decision.get("reentry_decision_digest"):
        raise ValueError("ownership_reentry_event_decision_mismatch")
    previous_owner = require_string(
        reentry_decision.get("previous_owner_id"), "previous_owner_id"
    )
    current_owner = require_string(
        reentry_decision.get("next_owner_id"), "next_owner_id"
    )
    if reentered_controller_state.get("current_owner_id") != current_owner:
        raise ValueError("ownership_reentered_owner_mismatch")
    target = dict(reentered_controller_state.get("target_active_state", {}))
    target_digest = require_string(
        target.get("multi_generation_supervisor_state_digest"),
        "target_active_state_digest",
    )
    state = {
        "version": STATE_VERSION,
        "continuity_id": "ownership:" + str(reentered_controller_state["controller_id"]),
        "lineage_id": reentered_controller_state["lineage_id"],
        "mission_contract_digest": reentered_controller_state[
            "mission_contract_digest"
        ],
        "policy_digest": reentered_controller_state["policy_digest"],
        "external_reentry_receipt_digest": external_reentry_receipt[
            "external_reentry_receipt_digest"
        ],
        "reentry_decision_digest": reentry_decision["reentry_decision_digest"],
        "reentry_event_digest": require_string(
            reentry_event.get("reentry_event_digest"), "reentry_event_digest"
        ),
        "source_terminal_state_digest": reentered_controller_state[
            "source_terminal_state_digest"
        ],
        "reentered_controller_state_digest": reentered_controller_state[
            "reentry_controller_state_digest"
        ],
        "target_active_state_digest": target_digest,
        "previous_owner_id": previous_owner,
        "current_owner_id": current_owner,
        "handover": previous_owner != current_owner,
        "status": ACTIVE,
        "stage_index": 0,
        "stage_receipt_digests": [],
        "underlying_completion_digests": [],
        "last_stage_receipt_digest": "",
        "created_at_ms": require_int(now_ms, "now_ms"),
        "updated_at_ms": require_int(now_ms, "now_ms"),
        "execution_granted": False,
        "host_license_granted": False,
        "memory_overwrite": False,
        "non_authority": copy_non_authority(),
        "boundary": copy_boundary(),
        "ownership_continuity_state_digest": "",
    }
    state["ownership_continuity_state_digest"] = state_digest(state)
    return state


def validate_ownership_continuity_state(state: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if state.get("version") != STATE_VERSION:
            errors.append("ownership_state_version_invalid")
        if state.get("ownership_continuity_state_digest") != state_digest(state):
            errors.append("ownership_state_digest_invalid")
        for field in (
            "continuity_id",
            "lineage_id",
            "mission_contract_digest",
            "policy_digest",
            "external_reentry_receipt_digest",
            "reentry_decision_digest",
            "reentry_event_digest",
            "source_terminal_state_digest",
            "reentered_controller_state_digest",
            "target_active_state_digest",
            "previous_owner_id",
            "current_owner_id",
        ):
            require_string(state.get(field), field)
        stage_index = require_int(state.get("stage_index"), "stage_index")
        if stage_index > len(STAGES):
            errors.append("ownership_stage_index_out_of_range")
        receipts = list(state.get("stage_receipt_digests", []))
        completions = list(state.get("underlying_completion_digests", []))
        if len(receipts) != stage_index or len(receipts) != len(set(receipts)):
            errors.append("ownership_stage_receipt_history_invalid")
        if len(completions) != stage_index or len(completions) != len(set(completions)):
            errors.append("ownership_underlying_completion_history_invalid")
        expected_last = receipts[-1] if receipts else ""
        if state.get("last_stage_receipt_digest") != expected_last:
            errors.append("ownership_last_stage_receipt_invalid")
        expected_status = COMPLETED if stage_index == len(STAGES) else ACTIVE
        if state.get("status") != expected_status:
            errors.append("ownership_status_invalid")
        handover = state.get("handover")
        if not isinstance(handover, bool):
            errors.append("ownership_handover_bool_required")
        elif handover != (state.get("previous_owner_id") != state.get("current_owner_id")):
            errors.append("ownership_handover_identity_invalid")
        for field in ("execution_granted", "host_license_granted", "memory_overwrite"):
            if state.get(field) is not False:
                errors.append(f"ownership_{field}_invalid")
        if dict(state.get("non_authority", {})) != NON_AUTHORITY:
            errors.append("ownership_non_authority_invalid")
        if dict(state.get("boundary", {})) != BOUNDARY:
            errors.append("ownership_boundary_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def build_ownership_stage_receipt(
    *,
    state: Mapping[str, Any],
    stage: str,
    owner_id: str,
    handoff_receipt_digest: str,
    completion_receipt_digest: str,
    stage_packet_digest: str,
    now_ms: int,
) -> dict[str, Any]:
    state_errors = validate_ownership_continuity_state(state)
    if state_errors:
        raise ValueError("ownership_state_invalid:" + ";".join(state_errors))
    if state.get("status") != ACTIVE:
        raise ValueError("ownership_continuity_already_completed")
    expected_stage = STAGES[int(state["stage_index"])]
    if stage != expected_stage:
        raise ValueError(f"ownership_stage_order_invalid:expected_{expected_stage}")
    owner = require_string(owner_id, "owner_id")
    if owner != state.get("current_owner_id"):
        raise ValueError("ownership_current_owner_mismatch")
    if state.get("handover") is True and owner == state.get("previous_owner_id"):
        raise ValueError("ownership_previous_owner_reuse_forbidden")
    handoff = require_string(handoff_receipt_digest, "handoff_receipt_digest")
    completion = require_string(
        completion_receipt_digest, "completion_receipt_digest"
    )
    packet_digest = require_string(stage_packet_digest, "stage_packet_digest")
    if completion in set(state.get("underlying_completion_digests", [])):
        raise ValueError("ownership_underlying_completion_reuse_forbidden")
    receipt = {
        "version": STAGE_RECEIPT_VERSION,
        "continuity_id": state["continuity_id"],
        "lineage_id": state["lineage_id"],
        "mission_contract_digest": state["mission_contract_digest"],
        "policy_digest": state["policy_digest"],
        "external_reentry_receipt_digest": state[
            "external_reentry_receipt_digest"
        ],
        "reentry_decision_digest": state["reentry_decision_digest"],
        "reentry_event_digest": state["reentry_event_digest"],
        "reentered_controller_state_digest": state[
            "reentered_controller_state_digest"
        ],
        "target_active_state_digest": state["target_active_state_digest"],
        "previous_owner_id": state["previous_owner_id"],
        "current_owner_id": state["current_owner_id"],
        "owner_id": owner,
        "stage": stage,
        "stage_index": int(state["stage_index"]) + 1,
        "predecessor_state_digest": state["ownership_continuity_state_digest"],
        "predecessor_stage_receipt_digest": state[
            "last_stage_receipt_digest"
        ],
        "handoff_receipt_digest": handoff,
        "completion_receipt_digest": completion,
        "stage_packet_digest": packet_digest,
        "single_use": True,
        "execution_granted": False,
        "host_license_granted": False,
        "memory_overwrite": False,
        "issued_at_ms": require_int(now_ms, "now_ms"),
        "non_authority": copy_non_authority(),
        "boundary": copy_boundary(),
        "ownership_stage_receipt_digest": "",
    }
    receipt["ownership_stage_receipt_digest"] = stage_receipt_digest(receipt)
    return receipt


def validate_ownership_stage_receipt(receipt: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if receipt.get("version") != STAGE_RECEIPT_VERSION:
            errors.append("ownership_stage_receipt_version_invalid")
        if receipt.get("ownership_stage_receipt_digest") != stage_receipt_digest(
            receipt
        ):
            errors.append("ownership_stage_receipt_digest_invalid")
        if receipt.get("stage") not in STAGES:
            errors.append("ownership_stage_invalid")
        require_int(receipt.get("stage_index"), "stage_index", minimum=1)
        for field in (
            "continuity_id",
            "lineage_id",
            "mission_contract_digest",
            "policy_digest",
            "external_reentry_receipt_digest",
            "reentry_decision_digest",
            "reentry_event_digest",
            "reentered_controller_state_digest",
            "target_active_state_digest",
            "previous_owner_id",
            "current_owner_id",
            "owner_id",
            "predecessor_state_digest",
            "handoff_receipt_digest",
            "completion_receipt_digest",
            "stage_packet_digest",
        ):
            require_string(receipt.get(field), field)
        if not isinstance(receipt.get("predecessor_stage_receipt_digest"), str):
            errors.append("predecessor_stage_receipt_digest_string_required")
        if receipt.get("single_use") is not True:
            errors.append("ownership_stage_single_use_required")
        for field in ("execution_granted", "host_license_granted", "memory_overwrite"):
            if receipt.get(field) is not False:
                errors.append(f"ownership_stage_{field}_invalid")
        if dict(receipt.get("non_authority", {})) != NON_AUTHORITY:
            errors.append("ownership_stage_non_authority_invalid")
        if dict(receipt.get("boundary", {})) != BOUNDARY:
            errors.append("ownership_stage_boundary_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def apply_ownership_stage_receipt(
    state: Mapping[str, Any], receipt: Mapping[str, Any]
) -> dict[str, Any]:
    state_errors = validate_ownership_continuity_state(state)
    if state_errors:
        raise ValueError("ownership_state_invalid:" + ";".join(state_errors))
    receipt_id = str(receipt.get("ownership_stage_receipt_digest", ""))
    if receipt_id in set(state.get("stage_receipt_digests", [])):
        return {"status": "REPLAYED", "state": deepcopy(dict(state)), "errors": []}
    receipt_errors = validate_ownership_stage_receipt(receipt)
    if receipt_errors:
        return {"status": "REJECTED", "state": deepcopy(dict(state)), "errors": receipt_errors}
    if state.get("status") != ACTIVE:
        return {"status": "REJECTED", "state": deepcopy(dict(state)), "errors": ["ownership_continuity_already_completed"]}
    expected_stage = STAGES[int(state["stage_index"])]
    bindings = {
        "continuity_id": state.get("continuity_id"),
        "lineage_id": state.get("lineage_id"),
        "mission_contract_digest": state.get("mission_contract_digest"),
        "policy_digest": state.get("policy_digest"),
        "external_reentry_receipt_digest": state.get("external_reentry_receipt_digest"),
        "reentry_decision_digest": state.get("reentry_decision_digest"),
        "reentry_event_digest": state.get("reentry_event_digest"),
        "reentered_controller_state_digest": state.get("reentered_controller_state_digest"),
        "target_active_state_digest": state.get("target_active_state_digest"),
        "previous_owner_id": state.get("previous_owner_id"),
        "current_owner_id": state.get("current_owner_id"),
        "owner_id": state.get("current_owner_id"),
        "stage": expected_stage,
        "stage_index": int(state.get("stage_index", 0)) + 1,
        "predecessor_state_digest": state.get("ownership_continuity_state_digest"),
        "predecessor_stage_receipt_digest": state.get("last_stage_receipt_digest"),
    }
    errors: list[str] = []
    for field, expected in bindings.items():
        if receipt.get(field) != expected:
            errors.append(f"ownership_stage_{field}_mismatch")
    if state.get("handover") is True and receipt.get("owner_id") == state.get(
        "previous_owner_id"
    ):
        errors.append("ownership_previous_owner_reuse_forbidden")
    completion = receipt.get("completion_receipt_digest")
    if completion in set(state.get("underlying_completion_digests", [])):
        errors.append("ownership_underlying_completion_reuse_forbidden")
    if errors:
        return {"status": "REJECTED", "state": deepcopy(dict(state)), "errors": errors}
    next_state = deepcopy(dict(state))
    next_state["stage_index"] = int(state["stage_index"]) + 1
    next_state["stage_receipt_digests"] = list(state["stage_receipt_digests"]) + [
        receipt_id
    ]
    next_state["underlying_completion_digests"] = list(
        state["underlying_completion_digests"]
    ) + [str(completion)]
    next_state["last_stage_receipt_digest"] = receipt_id
    next_state["updated_at_ms"] = int(receipt["issued_at_ms"])
    next_state["status"] = (
        COMPLETED if next_state["stage_index"] == len(STAGES) else ACTIVE
    )
    next_state["ownership_continuity_state_digest"] = ""
    next_state["ownership_continuity_state_digest"] = state_digest(next_state)
    next_errors = validate_ownership_continuity_state(next_state)
    if next_errors:
        raise ValueError("ownership_next_state_invalid:" + ";".join(next_errors))
    return {"status": "APPLIED", "state": next_state, "errors": []}
