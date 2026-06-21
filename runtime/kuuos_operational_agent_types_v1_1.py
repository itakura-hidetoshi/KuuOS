from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping, Sequence

from runtime.kuuos_belief_os_types_v0_1 import sha

TYPES_VERSION = "kuuos_operational_agent_types_v1_1"
CAPABILITY_VERSION = "kuuos_operational_agent_capability_v1_1"
LEASE_VERSION = "kuuos_operational_agent_execution_lease_v1_1"
INTENT_VERSION = "kuuos_operational_agent_action_intent_v1_1"
ADAPTER_RESULT_VERSION = "kuuos_operational_agent_adapter_result_v1_1"

EFFECT_CLASSES = ("READ_ONLY", "STAGED_WRITE", "EXTERNAL_COMMIT")
EFFECT_RANK = {name: index for index, name in enumerate(EFFECT_CLASSES)}

BOUNDARIES = {
    "controller_owns_ordering_only": True,
    "capability_presence_grants_execution": False,
    "plan_grants_execution": False,
    "lease_grants_truth": False,
    "adapter_result_grants_truth": False,
    "verification_grants_root_rewrite": False,
    "learning_mutates_current_cycle": False,
    "receipt_grants_successor_authority": False,
    "external_commit_supported": False,
}


def copy_boundaries() -> dict[str, bool]:
    return deepcopy(BOUNDARIES)


def digest_without(value: Mapping[str, Any], field: str) -> str:
    packet = deepcopy(dict(value))
    packet.pop(field, None)
    return sha(packet)


def require_string(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name}_required")
    return value.strip()


def require_nonnegative_int(value: Any, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{name}_nonnegative_int_required")
    return value


def require_positive_int(value: Any, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError(f"{name}_positive_int_required")
    return value


def normalize_unique_strings(
    values: Sequence[Any], name: str, *, allow_empty: bool = False
) -> list[str]:
    if isinstance(values, (str, bytes)):
        raise ValueError(f"{name}_sequence_required")
    result = [require_string(value, name) for value in values]
    if not allow_empty and not result:
        raise ValueError(f"{name}_required")
    if len(result) != len(set(result)):
        raise ValueError(f"{name}_duplicate")
    return sorted(result)


def effect_at_most(effect_class: str, ceiling: str) -> bool:
    if effect_class not in EFFECT_RANK or ceiling not in EFFECT_RANK:
        return False
    return EFFECT_RANK[effect_class] <= EFFECT_RANK[ceiling]


def build_capability(
    *,
    capability_id: str,
    owner_id: str,
    adapter_kind: str,
    operation_allowlist: Sequence[str],
    resource_scope: Sequence[str],
    capability_epoch: int,
    effect_ceiling: str = "STAGED_WRITE",
) -> dict[str, Any]:
    if effect_ceiling not in EFFECT_CLASSES:
        raise ValueError("capability_effect_ceiling_invalid")
    value = {
        "version": CAPABILITY_VERSION,
        "capability_id": require_string(capability_id, "capability_id"),
        "owner_id": require_string(owner_id, "owner_id"),
        "adapter_kind": require_string(adapter_kind, "adapter_kind"),
        "operation_allowlist": normalize_unique_strings(
            operation_allowlist, "operation_allowlist"
        ),
        "resource_scope": normalize_unique_strings(resource_scope, "resource_scope"),
        "capability_epoch": require_nonnegative_int(
            capability_epoch, "capability_epoch"
        ),
        "effect_ceiling": effect_ceiling,
        "active": True,
        **copy_boundaries(),
        "capability_digest": "",
    }
    value["capability_digest"] = digest_without(value, "capability_digest")
    errors = validate_capability(value)
    if errors:
        raise ValueError("capability_invalid:" + ";".join(errors))
    return value


def validate_capability(value: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if value.get("version") != CAPABILITY_VERSION:
            errors.append("capability_version_invalid")
        require_string(value.get("capability_id"), "capability_id")
        require_string(value.get("owner_id"), "owner_id")
        require_string(value.get("adapter_kind"), "adapter_kind")
        require_nonnegative_int(value.get("capability_epoch"), "capability_epoch")
        if value.get("effect_ceiling") not in EFFECT_CLASSES:
            errors.append("capability_effect_ceiling_invalid")
        if value.get("active") is not True:
            errors.append("capability_active_required")
        for field in ("operation_allowlist", "resource_scope"):
            items = value.get(field)
            if (
                not isinstance(items, list)
                or not items
                or items != sorted(set(items))
                or any(not isinstance(item, str) or not item for item in items)
            ):
                errors.append(f"capability_{field}_invalid")
        for key, expected in BOUNDARIES.items():
            if value.get(key) is not expected:
                errors.append(f"capability_boundary_{key}_invalid")
        if value.get("capability_digest") != digest_without(
            value, "capability_digest"
        ):
            errors.append("capability_digest_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def build_execution_lease(
    *,
    lease_id: str,
    capability_id: str,
    owner_id: str,
    lineage_id: str,
    session_digest: str,
    capability_epoch: int,
    allowed_operations: Sequence[str],
    resource_scope: Sequence[str],
    max_uses: int,
    issued_at_sequence: int,
    expires_at_sequence: int,
    host_license_digest: str,
    effect_ceiling: str = "STAGED_WRITE",
) -> dict[str, Any]:
    issued = require_nonnegative_int(issued_at_sequence, "issued_at_sequence")
    expires = require_nonnegative_int(expires_at_sequence, "expires_at_sequence")
    if expires <= issued:
        raise ValueError("lease_window_invalid")
    if effect_ceiling not in EFFECT_CLASSES:
        raise ValueError("lease_effect_ceiling_invalid")
    value = {
        "version": LEASE_VERSION,
        "lease_id": require_string(lease_id, "lease_id"),
        "capability_id": require_string(capability_id, "capability_id"),
        "owner_id": require_string(owner_id, "owner_id"),
        "lineage_id": require_string(lineage_id, "lineage_id"),
        "session_digest": require_string(session_digest, "session_digest"),
        "capability_epoch": require_nonnegative_int(
            capability_epoch, "capability_epoch"
        ),
        "allowed_operations": normalize_unique_strings(
            allowed_operations, "allowed_operations"
        ),
        "resource_scope": normalize_unique_strings(resource_scope, "resource_scope"),
        "effect_ceiling": effect_ceiling,
        "max_uses": require_positive_int(max_uses, "max_uses"),
        "issued_at_sequence": issued,
        "expires_at_sequence": expires,
        "host_license_digest": require_string(
            host_license_digest, "host_license_digest"
        ),
        "active": True,
        **copy_boundaries(),
        "lease_digest": "",
    }
    value["lease_digest"] = digest_without(value, "lease_digest")
    errors = validate_execution_lease(value)
    if errors:
        raise ValueError("execution_lease_invalid:" + ";".join(errors))
    return value


def validate_execution_lease(value: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if value.get("version") != LEASE_VERSION:
            errors.append("lease_version_invalid")
        for field in (
            "lease_id",
            "capability_id",
            "owner_id",
            "lineage_id",
            "session_digest",
            "host_license_digest",
        ):
            require_string(value.get(field), field)
        require_nonnegative_int(value.get("capability_epoch"), "capability_epoch")
        issued = require_nonnegative_int(
            value.get("issued_at_sequence"), "issued_at_sequence"
        )
        expires = require_nonnegative_int(
            value.get("expires_at_sequence"), "expires_at_sequence"
        )
        if expires <= issued:
            errors.append("lease_window_invalid")
        require_positive_int(value.get("max_uses"), "max_uses")
        if value.get("effect_ceiling") not in EFFECT_CLASSES:
            errors.append("lease_effect_ceiling_invalid")
        if value.get("active") is not True:
            errors.append("lease_active_required")
        for field in ("allowed_operations", "resource_scope"):
            items = value.get(field)
            if (
                not isinstance(items, list)
                or not items
                or items != sorted(set(items))
                or any(not isinstance(item, str) or not item for item in items)
            ):
                errors.append(f"lease_{field}_invalid")
        for key, expected in BOUNDARIES.items():
            if value.get(key) is not expected:
                errors.append(f"lease_boundary_{key}_invalid")
        if value.get("lease_digest") != digest_without(value, "lease_digest"):
            errors.append("lease_digest_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def build_action_intent(
    *,
    intent_id: str,
    owner_id: str,
    lineage_id: str,
    session_digest: str,
    capability_id: str,
    capability_epoch: int,
    adapter_kind: str,
    operation: str,
    resource: str,
    effect_class: str,
    payload: Mapping[str, Any],
    idempotency_key: str,
) -> dict[str, Any]:
    if effect_class not in EFFECT_CLASSES:
        raise ValueError("intent_effect_class_invalid")
    if not isinstance(payload, Mapping):
        raise ValueError("intent_payload_mapping_required")
    value = {
        "version": INTENT_VERSION,
        "intent_id": require_string(intent_id, "intent_id"),
        "owner_id": require_string(owner_id, "owner_id"),
        "lineage_id": require_string(lineage_id, "lineage_id"),
        "session_digest": require_string(session_digest, "session_digest"),
        "capability_id": require_string(capability_id, "capability_id"),
        "capability_epoch": require_nonnegative_int(
            capability_epoch, "capability_epoch"
        ),
        "adapter_kind": require_string(adapter_kind, "adapter_kind"),
        "operation": require_string(operation, "operation"),
        "resource": require_string(resource, "resource"),
        "effect_class": effect_class,
        "payload": deepcopy(dict(payload)),
        "payload_digest": sha(dict(payload)),
        "idempotency_key": require_string(idempotency_key, "idempotency_key"),
        "external_commit_requested": effect_class == "EXTERNAL_COMMIT",
        **copy_boundaries(),
        "intent_digest": "",
    }
    value["intent_digest"] = digest_without(value, "intent_digest")
    errors = validate_action_intent(value)
    if errors:
        raise ValueError("action_intent_invalid:" + ";".join(errors))
    return value


def validate_action_intent(value: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if value.get("version") != INTENT_VERSION:
            errors.append("intent_version_invalid")
        for field in (
            "intent_id",
            "owner_id",
            "lineage_id",
            "session_digest",
            "capability_id",
            "adapter_kind",
            "operation",
            "resource",
            "idempotency_key",
        ):
            require_string(value.get(field), field)
        require_nonnegative_int(value.get("capability_epoch"), "capability_epoch")
        effect_class = value.get("effect_class")
        if effect_class not in EFFECT_CLASSES:
            errors.append("intent_effect_class_invalid")
        if not isinstance(value.get("payload"), dict):
            errors.append("intent_payload_invalid")
        elif value.get("payload_digest") != sha(value.get("payload")):
            errors.append("intent_payload_digest_invalid")
        if value.get("external_commit_requested") is not (
            effect_class == "EXTERNAL_COMMIT"
        ):
            errors.append("intent_external_commit_flag_invalid")
        for key, expected in BOUNDARIES.items():
            if value.get(key) is not expected:
                errors.append(f"intent_boundary_{key}_invalid")
        if value.get("intent_digest") != digest_without(value, "intent_digest"):
            errors.append("intent_digest_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def build_adapter_result(
    *,
    adapter_kind: str,
    intent_digest: str,
    effect_digest: str,
    evidence_digest: str,
    staged: bool,
) -> dict[str, Any]:
    value = {
        "version": ADAPTER_RESULT_VERSION,
        "adapter_kind": require_string(adapter_kind, "adapter_kind"),
        "intent_digest": require_string(intent_digest, "intent_digest"),
        "effect_digest": require_string(effect_digest, "effect_digest"),
        "evidence_digest": require_string(evidence_digest, "evidence_digest"),
        "staged": bool(staged),
        "external_commit_performed": False,
        **copy_boundaries(),
        "adapter_result_digest": "",
    }
    value["adapter_result_digest"] = digest_without(
        value, "adapter_result_digest"
    )
    errors = validate_adapter_result(value)
    if errors:
        raise ValueError("adapter_result_invalid:" + ";".join(errors))
    return value


def validate_adapter_result(value: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if value.get("version") != ADAPTER_RESULT_VERSION:
            errors.append("adapter_result_version_invalid")
        for field in (
            "adapter_kind",
            "intent_digest",
            "effect_digest",
            "evidence_digest",
        ):
            require_string(value.get(field), field)
        if value.get("staged") is not True:
            errors.append("adapter_result_staged_required")
        if value.get("external_commit_performed") is not False:
            errors.append("adapter_external_commit_forbidden")
        for key, expected in BOUNDARIES.items():
            if value.get(key) is not expected:
                errors.append(f"adapter_boundary_{key}_invalid")
        if value.get("adapter_result_digest") != digest_without(
            value, "adapter_result_digest"
        ):
            errors.append("adapter_result_digest_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors
