from __future__ import annotations

from typing import Any, Mapping, Sequence

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_plan_os_ownership_continuity_kernel_v0_8 import validate_ownership_continuity_state
from runtime.kuuos_plan_os_ownership_continuity_types_v0_8 import ACTIVE as OWNERSHIP_ACTIVE
from runtime.kuuos_plan_os_capability_rotation_types_v0_9 import (
    BOUND,
    BOUNDARY,
    CAPABILITY_KINDS,
    NON_AUTHORITY,
    ROTATED,
    ROTATION_RECEIPT_VERSION,
    STATE_VERSION,
    copy_boundary,
    copy_non_authority,
    require_int,
    require_string,
    rotation_receipt_digest,
    state_digest,
)


def _inventory(
    ownership_state: Mapping[str, Any],
    previous_epoch_digest: str,
    entries: Sequence[Mapping[str, Any]],
) -> list[dict[str, str]]:
    if len(entries) != len(CAPABILITY_KINDS):
        raise ValueError("previous_inventory_incomplete")
    owner = str(ownership_state["previous_owner_id"])
    kinds: set[str] = set()
    digests: set[str] = set()
    result: list[dict[str, str]] = []
    for raw in entries:
        kind = require_string(raw.get("kind"), "kind")
        digest = require_string(raw.get("capability_digest"), "capability_digest")
        item_owner = require_string(raw.get("owner_id"), "owner_id")
        epoch = require_string(raw.get("epoch_digest"), "epoch_digest")
        if kind not in CAPABILITY_KINDS or kind in kinds:
            raise ValueError("previous_inventory_kind_invalid")
        if digest in digests:
            raise ValueError("previous_inventory_digest_duplicate")
        if item_owner != owner:
            raise ValueError("previous_inventory_owner_mismatch")
        if epoch != previous_epoch_digest:
            raise ValueError("previous_inventory_epoch_mismatch")
        kinds.add(kind)
        digests.add(digest)
        result.append({
            "kind": kind,
            "capability_digest": digest,
            "owner_id": item_owner,
            "epoch_digest": epoch,
        })
    if kinds != set(CAPABILITY_KINDS):
        raise ValueError("previous_inventory_incomplete")
    result.sort(key=lambda item: CAPABILITY_KINDS.index(item["kind"]))
    return result


def build_capability_rotation_receipt(
    *,
    ownership_state: Mapping[str, Any],
    previous_epoch_index: int,
    previous_epoch_digest: str,
    previous_capabilities: Sequence[Mapping[str, Any]],
    now_ms: int,
) -> dict[str, Any]:
    errors = validate_ownership_continuity_state(ownership_state)
    if errors:
        raise ValueError("ownership_state_invalid:" + ";".join(errors))
    if ownership_state.get("status") != OWNERSHIP_ACTIVE:
        raise ValueError("rotation_requires_active_ownership")
    if ownership_state.get("stage_index") != 0:
        raise ValueError("rotation_must_precede_plan_stage")
    old_index = require_int(previous_epoch_index, "previous_epoch_index")
    old_epoch = require_string(previous_epoch_digest, "previous_epoch_digest")
    inventory = _inventory(ownership_state, old_epoch, previous_capabilities)
    new_index = old_index + 1
    new_epoch = sha({
        "ownership_state_digest": ownership_state["ownership_continuity_state_digest"],
        "previous_epoch_index": old_index,
        "previous_epoch_digest": old_epoch,
        "current_epoch_index": new_index,
        "previous_owner_id": ownership_state["previous_owner_id"],
        "current_owner_id": ownership_state["current_owner_id"],
        "revoked": [item["capability_digest"] for item in inventory],
    })
    receipt = {
        "version": ROTATION_RECEIPT_VERSION,
        "continuity_id": ownership_state["continuity_id"],
        "lineage_id": ownership_state["lineage_id"],
        "mission_contract_digest": ownership_state["mission_contract_digest"],
        "policy_digest": ownership_state["policy_digest"],
        "ownership_state_digest": ownership_state["ownership_continuity_state_digest"],
        "external_reentry_receipt_digest": ownership_state["external_reentry_receipt_digest"],
        "reentry_decision_digest": ownership_state["reentry_decision_digest"],
        "reentry_event_digest": ownership_state["reentry_event_digest"],
        "previous_owner_id": ownership_state["previous_owner_id"],
        "current_owner_id": ownership_state["current_owner_id"],
        "handover": bool(ownership_state["handover"]),
        "previous_epoch_index": old_index,
        "previous_epoch_digest": old_epoch,
        "current_epoch_index": new_index,
        "current_epoch_digest": new_epoch,
        "revoked_capabilities": inventory,
        "revoked_capability_digests": [item["capability_digest"] for item in inventory],
        "required_reissue_kinds": list(CAPABILITY_KINDS),
        "all_previous_capabilities_revoked": True,
        "lower_authority_reissue_required": True,
        "execution_granted": False,
        "host_license_granted": False,
        "memory_overwrite": False,
        "rotated_at_ms": require_int(now_ms, "now_ms"),
        "non_authority": copy_non_authority(),
        "boundary": copy_boundary(),
        "capability_rotation_receipt_digest": "",
    }
    receipt["capability_rotation_receipt_digest"] = rotation_receipt_digest(receipt)
    return receipt


def validate_capability_rotation_receipt(receipt: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if receipt.get("version") != ROTATION_RECEIPT_VERSION:
            errors.append("rotation_version_invalid")
        if receipt.get("capability_rotation_receipt_digest") != rotation_receipt_digest(receipt):
            errors.append("rotation_digest_invalid")
        for field in (
            "continuity_id", "lineage_id", "mission_contract_digest", "policy_digest",
            "ownership_state_digest", "external_reentry_receipt_digest",
            "reentry_decision_digest", "reentry_event_digest", "previous_owner_id",
            "current_owner_id", "previous_epoch_digest", "current_epoch_digest",
        ):
            require_string(receipt.get(field), field)
        old_index = require_int(receipt.get("previous_epoch_index"), "previous_epoch_index")
        new_index = require_int(receipt.get("current_epoch_index"), "current_epoch_index", minimum=1)
        if new_index != old_index + 1:
            errors.append("rotation_epoch_not_monotone")
        inventory = list(receipt.get("revoked_capabilities", []))
        digests = list(receipt.get("revoked_capability_digests", []))
        if {item.get("kind") for item in inventory} != set(CAPABILITY_KINDS):
            errors.append("rotation_inventory_kinds_invalid")
        if [item.get("capability_digest") for item in inventory] != digests:
            errors.append("rotation_inventory_digest_mismatch")
        if len(digests) != len(CAPABILITY_KINDS) or len(digests) != len(set(digests)):
            errors.append("rotation_revocation_set_invalid")
        for item in inventory:
            if item.get("owner_id") != receipt.get("previous_owner_id"):
                errors.append("rotation_revoked_owner_invalid")
            if item.get("epoch_digest") != receipt.get("previous_epoch_digest"):
                errors.append("rotation_revoked_epoch_invalid")
        if list(receipt.get("required_reissue_kinds", [])) != list(CAPABILITY_KINDS):
            errors.append("rotation_required_kinds_invalid")
        for field, expected in {
            "all_previous_capabilities_revoked": True,
            "lower_authority_reissue_required": True,
            "execution_granted": False,
            "host_license_granted": False,
            "memory_overwrite": False,
        }.items():
            if receipt.get(field) != expected:
                errors.append(f"rotation_{field}_invalid")
        if dict(receipt.get("non_authority", {})) != NON_AUTHORITY:
            errors.append("rotation_non_authority_invalid")
        if dict(receipt.get("boundary", {})) != BOUNDARY:
            errors.append("rotation_boundary_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def build_initial_capability_epoch_state(
    *, rotation_receipt: Mapping[str, Any], now_ms: int
) -> dict[str, Any]:
    errors = validate_capability_rotation_receipt(rotation_receipt)
    if errors:
        raise ValueError("rotation_receipt_invalid:" + ";".join(errors))
    state = {
        "version": STATE_VERSION,
        "rotation_id": "capability:" + str(rotation_receipt["continuity_id"]),
        "continuity_id": rotation_receipt["continuity_id"],
        "lineage_id": rotation_receipt["lineage_id"],
        "mission_contract_digest": rotation_receipt["mission_contract_digest"],
        "policy_digest": rotation_receipt["policy_digest"],
        "ownership_state_digest": rotation_receipt["ownership_state_digest"],
        "capability_rotation_receipt_digest": rotation_receipt["capability_rotation_receipt_digest"],
        "previous_owner_id": rotation_receipt["previous_owner_id"],
        "current_owner_id": rotation_receipt["current_owner_id"],
        "handover": rotation_receipt["handover"],
        "previous_epoch_index": rotation_receipt["previous_epoch_index"],
        "previous_epoch_digest": rotation_receipt["previous_epoch_digest"],
        "current_epoch_index": rotation_receipt["current_epoch_index"],
        "current_epoch_digest": rotation_receipt["current_epoch_digest"],
        "revoked_capability_digests": list(rotation_receipt["revoked_capability_digests"]),
        "required_reissue_kinds": list(CAPABILITY_KINDS),
        "capability_bindings": {},
        "processed_binding_digests": [],
        "status": ROTATED,
        "created_at_ms": require_int(now_ms, "now_ms"),
        "updated_at_ms": require_int(now_ms, "now_ms"),
        "execution_granted": False,
        "host_license_granted": False,
        "memory_overwrite": False,
        "non_authority": copy_non_authority(),
        "boundary": copy_boundary(),
        "capability_epoch_state_digest": "",
    }
    state["capability_epoch_state_digest"] = state_digest(state)
    return state


def validate_capability_epoch_state(state: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if state.get("version") != STATE_VERSION:
            errors.append("state_version_invalid")
        if state.get("capability_epoch_state_digest") != state_digest(state):
            errors.append("state_digest_invalid")
        for field in (
            "rotation_id", "continuity_id", "lineage_id", "mission_contract_digest",
            "policy_digest", "ownership_state_digest", "capability_rotation_receipt_digest",
            "previous_owner_id", "current_owner_id", "previous_epoch_digest",
            "current_epoch_digest",
        ):
            require_string(state.get(field), field)
        old_index = require_int(state.get("previous_epoch_index"), "previous_epoch_index")
        new_index = require_int(state.get("current_epoch_index"), "current_epoch_index", minimum=1)
        if new_index != old_index + 1:
            errors.append("state_epoch_not_monotone")
        revoked = list(state.get("revoked_capability_digests", []))
        if len(revoked) != len(CAPABILITY_KINDS) or len(revoked) != len(set(revoked)):
            errors.append("state_revocation_set_invalid")
        bindings = dict(state.get("capability_bindings", {}))
        processed = list(state.get("processed_binding_digests", []))
        if not set(bindings).issubset(set(CAPABILITY_KINDS)):
            errors.append("state_binding_kind_invalid")
        if len(processed) != len(bindings) or len(processed) != len(set(processed)):
            errors.append("state_binding_history_invalid")
        expected_status = BOUND if len(bindings) == len(CAPABILITY_KINDS) else ROTATED
        if state.get("status") != expected_status:
            errors.append("state_status_invalid")
        for field in ("execution_granted", "host_license_granted", "memory_overwrite"):
            if state.get(field) is not False:
                errors.append(f"state_{field}_invalid")
        if dict(state.get("non_authority", {})) != NON_AUTHORITY:
            errors.append("state_non_authority_invalid")
        if dict(state.get("boundary", {})) != BOUNDARY:
            errors.append("state_boundary_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors
