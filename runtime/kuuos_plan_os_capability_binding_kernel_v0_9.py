from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_plan_os_capability_rotation_kernel_v0_9 import validate_capability_epoch_state
from runtime.kuuos_plan_os_capability_rotation_types_v0_9 import (
    BINDING_VERSION,
    BOUND,
    BOUNDARY,
    CAPABILITY_KINDS,
    NON_AUTHORITY,
    ROTATED,
    binding_digest,
    copy_boundary,
    copy_non_authority,
    require_int,
    require_string,
    state_digest,
)


def build_capability_reissue_binding(
    *,
    state: Mapping[str, Any],
    kind: str,
    owner_id: str,
    source_authority_receipt_digest: str,
    issued_capability_digest: str,
    scope_digest: str,
    issued_at_ms: int,
    expires_at_ms: int,
) -> dict[str, Any]:
    errors = validate_capability_epoch_state(state)
    if errors:
        raise ValueError("capability_state_invalid:" + ";".join(errors))
    capability_kind = require_string(kind, "kind")
    if capability_kind not in CAPABILITY_KINDS:
        raise ValueError("capability_binding_kind_invalid")
    if capability_kind in dict(state["capability_bindings"]):
        raise ValueError("capability_kind_already_bound")
    owner = require_string(owner_id, "owner_id")
    if owner != state.get("current_owner_id"):
        raise ValueError("capability_binding_current_owner_mismatch")
    if state.get("handover") is True and owner == state.get("previous_owner_id"):
        raise ValueError("capability_binding_previous_owner_forbidden")
    authority_receipt = require_string(
        source_authority_receipt_digest, "source_authority_receipt_digest"
    )
    capability_digest = require_string(
        issued_capability_digest, "issued_capability_digest"
    )
    if capability_digest in set(state.get("revoked_capability_digests", [])):
        raise ValueError("capability_reissued_digest_is_revoked")
    issued = require_int(issued_at_ms, "issued_at_ms")
    expires = require_int(expires_at_ms, "expires_at_ms", minimum=issued + 1)
    binding = {
        "version": BINDING_VERSION,
        "rotation_id": state["rotation_id"],
        "continuity_id": state["continuity_id"],
        "ownership_state_digest": state["ownership_state_digest"],
        "capability_rotation_receipt_digest": state[
            "capability_rotation_receipt_digest"
        ],
        "previous_owner_id": state["previous_owner_id"],
        "current_owner_id": state["current_owner_id"],
        "owner_id": owner,
        "kind": capability_kind,
        "previous_epoch_digest": state["previous_epoch_digest"],
        "current_epoch_index": state["current_epoch_index"],
        "current_epoch_digest": state["current_epoch_digest"],
        "predecessor_state_digest": state["capability_epoch_state_digest"],
        "source_authority_receipt_digest": authority_receipt,
        "issued_capability_digest": capability_digest,
        "scope_digest": require_string(scope_digest, "scope_digest"),
        "issued_at_ms": issued,
        "expires_at_ms": expires,
        "lower_authority_validated": True,
        "authority_granted_by_binding": False,
        "single_use": True,
        "execution_granted": False,
        "host_license_granted": False,
        "memory_overwrite": False,
        "non_authority": copy_non_authority(),
        "boundary": copy_boundary(),
        "capability_reissue_binding_digest": "",
    }
    binding["capability_reissue_binding_digest"] = binding_digest(binding)
    return binding


def validate_capability_reissue_binding(binding: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if binding.get("version") != BINDING_VERSION:
            errors.append("binding_version_invalid")
        if binding.get("capability_reissue_binding_digest") != binding_digest(binding):
            errors.append("binding_digest_invalid")
        if binding.get("kind") not in CAPABILITY_KINDS:
            errors.append("binding_kind_invalid")
        for field in (
            "rotation_id", "continuity_id", "ownership_state_digest",
            "capability_rotation_receipt_digest", "previous_owner_id",
            "current_owner_id", "owner_id", "previous_epoch_digest",
            "current_epoch_digest", "predecessor_state_digest",
            "source_authority_receipt_digest", "issued_capability_digest",
            "scope_digest",
        ):
            require_string(binding.get(field), field)
        require_int(binding.get("current_epoch_index"), "current_epoch_index", minimum=1)
        issued = require_int(binding.get("issued_at_ms"), "issued_at_ms")
        require_int(binding.get("expires_at_ms"), "expires_at_ms", minimum=issued + 1)
        for field, expected in {
            "lower_authority_validated": True,
            "authority_granted_by_binding": False,
            "single_use": True,
            "execution_granted": False,
            "host_license_granted": False,
            "memory_overwrite": False,
        }.items():
            if binding.get(field) != expected:
                errors.append(f"binding_{field}_invalid")
        if dict(binding.get("non_authority", {})) != NON_AUTHORITY:
            errors.append("binding_non_authority_invalid")
        if dict(binding.get("boundary", {})) != BOUNDARY:
            errors.append("binding_boundary_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def apply_capability_reissue_binding(
    state: Mapping[str, Any], binding: Mapping[str, Any]
) -> dict[str, Any]:
    state_errors = validate_capability_epoch_state(state)
    if state_errors:
        raise ValueError("capability_state_invalid:" + ";".join(state_errors))
    binding_id = str(binding.get("capability_reissue_binding_digest", ""))
    if binding_id in set(state.get("processed_binding_digests", [])):
        return {"status": "REPLAYED", "state": deepcopy(dict(state)), "errors": []}
    binding_errors = validate_capability_reissue_binding(binding)
    if binding_errors:
        return {"status": "REJECTED", "state": deepcopy(dict(state)), "errors": binding_errors}
    kind = str(binding.get("kind"))
    bindings = dict(state.get("capability_bindings", {}))
    if kind in bindings:
        return {"status": "REJECTED", "state": deepcopy(dict(state)), "errors": ["capability_kind_already_bound"]}
    expected = {
        "rotation_id": state.get("rotation_id"),
        "continuity_id": state.get("continuity_id"),
        "ownership_state_digest": state.get("ownership_state_digest"),
        "capability_rotation_receipt_digest": state.get("capability_rotation_receipt_digest"),
        "previous_owner_id": state.get("previous_owner_id"),
        "current_owner_id": state.get("current_owner_id"),
        "owner_id": state.get("current_owner_id"),
        "previous_epoch_digest": state.get("previous_epoch_digest"),
        "current_epoch_index": state.get("current_epoch_index"),
        "current_epoch_digest": state.get("current_epoch_digest"),
        "predecessor_state_digest": state.get("capability_epoch_state_digest"),
    }
    errors: list[str] = []
    for field, value in expected.items():
        if binding.get(field) != value:
            errors.append(f"binding_{field}_mismatch")
    capability_digest = binding.get("issued_capability_digest")
    if capability_digest in set(state.get("revoked_capability_digests", [])):
        errors.append("capability_reissued_digest_is_revoked")
    if errors:
        return {"status": "REJECTED", "state": deepcopy(dict(state)), "errors": errors}
    next_state = deepcopy(dict(state))
    next_bindings = dict(next_state["capability_bindings"])
    next_bindings[kind] = deepcopy(dict(binding))
    next_state["capability_bindings"] = next_bindings
    next_state["processed_binding_digests"] = list(next_state["processed_binding_digests"]) + [binding_id]
    next_state["updated_at_ms"] = int(binding["issued_at_ms"])
    next_state["status"] = BOUND if len(next_bindings) == len(CAPABILITY_KINDS) else ROTATED
    next_state["capability_epoch_state_digest"] = ""
    next_state["capability_epoch_state_digest"] = state_digest(next_state)
    next_errors = validate_capability_epoch_state(next_state)
    if next_errors:
        raise ValueError("capability_next_state_invalid:" + ";".join(next_errors))
    return {"status": "APPLIED", "state": next_state, "errors": []}


def validate_capability_reference(
    *,
    state: Mapping[str, Any],
    kind: str,
    owner_id: str,
    epoch_digest: str,
    capability_digest: str,
    source_authority_receipt_digest: str,
    now_ms: int,
) -> list[str]:
    errors = validate_capability_epoch_state(state)
    if errors:
        return ["capability_state_invalid:" + ";".join(errors)]
    if capability_digest in set(state.get("revoked_capability_digests", [])):
        return ["capability_reference_revoked"]
    if owner_id != state.get("current_owner_id"):
        errors.append("capability_reference_owner_mismatch")
    if epoch_digest != state.get("current_epoch_digest"):
        errors.append("capability_reference_epoch_mismatch")
    binding = dict(state.get("capability_bindings", {})).get(kind)
    if not isinstance(binding, dict):
        errors.append("capability_reference_binding_missing")
        return errors
    if binding.get("issued_capability_digest") != capability_digest:
        errors.append("capability_reference_digest_mismatch")
    if binding.get("source_authority_receipt_digest") != source_authority_receipt_digest:
        errors.append("capability_reference_authority_receipt_mismatch")
    now = require_int(now_ms, "now_ms")
    if now < int(binding["issued_at_ms"]) or now >= int(binding["expires_at_ms"]):
        errors.append("capability_reference_not_current")
    return errors
