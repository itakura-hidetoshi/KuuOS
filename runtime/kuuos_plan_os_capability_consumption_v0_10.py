from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_plan_os_capability_lease_kernel_v0_10 import (
    refresh_expired_leases,
    validate_capability_lease_state,
)
from runtime.kuuos_plan_os_capability_lease_types_v0_10 import (
    ACTIVE,
    CONSUMPTION_VERSION,
    EXHAUSTED,
    consumption_digest,
    copy_boundary,
    copy_non_authority,
    require_int,
    require_string,
    state_digest,
)


def build_lease_consumption_receipt(
    *,
    state: Mapping[str, Any],
    kind: str,
    owner_id: str,
    epoch_digest: str,
    stage: str,
    operation_id: str,
    scope_digest: str,
    cost_units: int,
    usage_id: str,
    now_ms: int,
) -> dict[str, Any]:
    errors = validate_capability_lease_state(state)
    if errors:
        raise ValueError("lease_state_invalid:" + ";".join(errors))
    capability_kind = require_string(kind, "kind")
    lease = dict(state["leases"].get(capability_kind, {}))
    if not lease:
        raise ValueError("lease_kind_missing")
    owner = require_string(owner_id, "owner_id")
    epoch = require_string(epoch_digest, "epoch_digest")
    selected_stage = require_string(stage, "stage")
    operation = require_string(operation_id, "operation_id")
    scope = require_string(scope_digest, "scope_digest")
    cost = require_int(cost_units, "cost_units", minimum=1)
    now = require_int(now_ms, "now_ms")
    if owner != state.get("current_owner_id") or owner != lease.get("owner_id"):
        raise ValueError("lease_owner_mismatch")
    if epoch != state.get("current_epoch_digest") or epoch != lease.get("epoch_digest"):
        raise ValueError("lease_epoch_mismatch")
    if selected_stage not in list(lease.get("allowed_stages", [])):
        raise ValueError("lease_stage_not_allowed")
    if operation not in list(lease.get("operation_allowlist", [])):
        raise ValueError("lease_operation_not_allowed")
    if scope != lease.get("scope_digest"):
        raise ValueError("lease_scope_mismatch")
    if lease.get("status") != ACTIVE:
        raise ValueError("lease_not_active")
    if now < int(lease["not_before_ms"]) or now >= int(lease["expires_at_ms"]):
        raise ValueError("lease_not_current")
    if int(lease["remaining_uses"]) < 1:
        raise ValueError("lease_use_budget_exhausted")
    if int(lease["remaining_cost_units"]) < cost:
        raise ValueError("lease_cost_budget_exceeded")
    receipt = {
        "version": CONSUMPTION_VERSION,
        "lease_supervisor_id": state["lease_supervisor_id"],
        "rotation_id": state["rotation_id"],
        "capability_lease_state_digest": state["capability_lease_state_digest"],
        "kind": capability_kind,
        "owner_id": owner,
        "epoch_digest": epoch,
        "capability_digest": lease["capability_digest"],
        "capability_binding_digest": lease["capability_binding_digest"],
        "stage": selected_stage,
        "operation_id": operation,
        "scope_digest": scope,
        "cost_units": cost,
        "usage_id": require_string(usage_id, "usage_id"),
        "consumed_at_ms": now,
        "single_use": True,
        "execution_granted": False,
        "host_license_granted": False,
        "memory_overwrite": False,
        "non_authority": copy_non_authority(),
        "boundary": copy_boundary(),
        "lease_consumption_receipt_digest": "",
    }
    receipt["lease_consumption_receipt_digest"] = consumption_digest(receipt)
    return receipt


def validate_lease_consumption_receipt(receipt: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if receipt.get("version") != CONSUMPTION_VERSION:
            errors.append("lease_consumption_version_invalid")
        if receipt.get("lease_consumption_receipt_digest") != consumption_digest(receipt):
            errors.append("lease_consumption_digest_invalid")
        for field in (
            "lease_supervisor_id", "rotation_id", "capability_lease_state_digest",
            "kind", "owner_id", "epoch_digest", "capability_digest",
            "capability_binding_digest", "stage", "operation_id", "scope_digest",
            "usage_id",
        ):
            require_string(receipt.get(field), field)
        require_int(receipt.get("cost_units"), "cost_units", minimum=1)
        require_int(receipt.get("consumed_at_ms"), "consumed_at_ms")
        if receipt.get("single_use") is not True:
            errors.append("lease_consumption_single_use_required")
        for field in ("execution_granted", "host_license_granted", "memory_overwrite"):
            if receipt.get(field) is not False:
                errors.append(f"lease_consumption_{field}_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def apply_lease_consumption(
    state: Mapping[str, Any], receipt: Mapping[str, Any]
) -> dict[str, Any]:
    current = refresh_expired_leases(state, now_ms=int(receipt.get("consumed_at_ms", 0)))
    state_errors = validate_capability_lease_state(current)
    if state_errors:
        raise ValueError("lease_state_invalid:" + ";".join(state_errors))
    receipt_id = str(receipt.get("lease_consumption_receipt_digest", ""))
    if receipt_id in set(current.get("processed_consumption_digests", [])):
        return {"status": "REPLAYED", "state": deepcopy(current), "errors": []}
    receipt_errors = validate_lease_consumption_receipt(receipt)
    if receipt_errors:
        return {"status": "REJECTED", "state": deepcopy(current), "errors": receipt_errors}
    kind = str(receipt.get("kind"))
    lease = dict(current.get("leases", {}).get(kind, {}))
    expected = {
        "lease_supervisor_id": current.get("lease_supervisor_id"),
        "rotation_id": current.get("rotation_id"),
        "capability_lease_state_digest": current.get("capability_lease_state_digest"),
        "owner_id": current.get("current_owner_id"),
        "epoch_digest": current.get("current_epoch_digest"),
        "capability_digest": lease.get("capability_digest"),
        "capability_binding_digest": lease.get("capability_binding_digest"),
        "scope_digest": lease.get("scope_digest"),
    }
    errors: list[str] = []
    for field, value in expected.items():
        if receipt.get(field) != value:
            errors.append(f"lease_consumption_{field}_mismatch")
    if receipt.get("stage") not in list(lease.get("allowed_stages", [])):
        errors.append("lease_stage_not_allowed")
    if receipt.get("operation_id") not in list(lease.get("operation_allowlist", [])):
        errors.append("lease_operation_not_allowed")
    cost = int(receipt.get("cost_units", 0))
    now = int(receipt.get("consumed_at_ms", 0))
    if lease.get("status") != ACTIVE:
        errors.append("lease_not_active")
    if now < int(lease.get("not_before_ms", 0)) or now >= int(lease.get("expires_at_ms", 0)):
        errors.append("lease_not_current")
    if int(lease.get("remaining_uses", 0)) < 1:
        errors.append("lease_use_budget_exhausted")
    if int(lease.get("remaining_cost_units", 0)) < cost:
        errors.append("lease_cost_budget_exceeded")
    if errors:
        return {"status": "REJECTED", "state": deepcopy(current), "errors": errors}
    next_state = deepcopy(current)
    target = next_state["leases"][kind]
    target["remaining_uses"] -= 1
    target["remaining_cost_units"] -= cost
    if target["remaining_uses"] == 0 or target["remaining_cost_units"] == 0:
        target["status"] = EXHAUSTED
    next_state["processed_consumption_digests"] = list(
        next_state["processed_consumption_digests"]
    ) + [receipt_id]
    next_state["updated_at_ms"] = now
    next_state["capability_lease_state_digest"] = ""
    next_state["capability_lease_state_digest"] = state_digest(next_state)
    return {"status": "APPLIED", "state": next_state, "errors": []}
