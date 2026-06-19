from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_plan_os_capability_lease_kernel_v0_10 import validate_capability_lease_state
from runtime.kuuos_plan_os_capability_lease_types_v0_10 import (
    ACTIVE,
    RENEWAL_VERSION,
    copy_boundary,
    copy_non_authority,
    renewal_digest,
    require_int,
    require_string,
    state_digest,
)


def build_lease_renewal_receipt(
    *,
    state: Mapping[str, Any],
    kind: str,
    owner_id: str,
    epoch_digest: str,
    scope_digest: str,
    external_renewal_receipt_digest: str,
    additional_uses: int,
    additional_cost_units: int,
    new_expires_at_ms: int,
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
    scope = require_string(scope_digest, "scope_digest")
    if owner != state.get("current_owner_id") or owner != lease.get("owner_id"):
        raise ValueError("renewal_owner_mismatch")
    if epoch != state.get("current_epoch_digest") or epoch != lease.get("epoch_digest"):
        raise ValueError("renewal_epoch_mismatch")
    if scope != lease.get("scope_digest"):
        raise ValueError("renewal_scope_mismatch")
    add_uses = require_int(additional_uses, "additional_uses", minimum=1)
    add_cost = require_int(additional_cost_units, "additional_cost_units", minimum=1)
    now = require_int(now_ms, "now_ms")
    new_expiry = require_int(new_expires_at_ms, "new_expires_at_ms", minimum=now + 1)
    if new_expiry <= int(lease["expires_at_ms"]):
        raise ValueError("renewal_expiry_not_extended")
    receipt = {
        "version": RENEWAL_VERSION,
        "lease_supervisor_id": state["lease_supervisor_id"],
        "rotation_id": state["rotation_id"],
        "predecessor_state_digest": state["capability_lease_state_digest"],
        "kind": capability_kind,
        "owner_id": owner,
        "epoch_digest": epoch,
        "scope_digest": scope,
        "external_renewal_receipt_digest": require_string(
            external_renewal_receipt_digest, "external_renewal_receipt_digest"
        ),
        "additional_uses": add_uses,
        "additional_cost_units": add_cost,
        "new_expires_at_ms": new_expiry,
        "renewed_at_ms": now,
        "automatic_renewal": False,
        "execution_granted": False,
        "host_license_granted": False,
        "memory_overwrite": False,
        "non_authority": copy_non_authority(),
        "boundary": copy_boundary(),
        "lease_renewal_receipt_digest": "",
    }
    receipt["lease_renewal_receipt_digest"] = renewal_digest(receipt)
    return receipt


def validate_lease_renewal_receipt(receipt: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if receipt.get("version") != RENEWAL_VERSION:
            errors.append("lease_renewal_version_invalid")
        if receipt.get("lease_renewal_receipt_digest") != renewal_digest(receipt):
            errors.append("lease_renewal_digest_invalid")
        for field in (
            "lease_supervisor_id", "rotation_id", "predecessor_state_digest",
            "kind", "owner_id", "epoch_digest", "scope_digest",
            "external_renewal_receipt_digest",
        ):
            require_string(receipt.get(field), field)
        require_int(receipt.get("additional_uses"), "additional_uses", minimum=1)
        require_int(receipt.get("additional_cost_units"), "additional_cost_units", minimum=1)
        renewed = require_int(receipt.get("renewed_at_ms"), "renewed_at_ms")
        require_int(receipt.get("new_expires_at_ms"), "new_expires_at_ms", minimum=renewed + 1)
        if receipt.get("automatic_renewal") is not False:
            errors.append("automatic_renewal_forbidden")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def apply_lease_renewal(
    state: Mapping[str, Any], receipt: Mapping[str, Any]
) -> dict[str, Any]:
    state_errors = validate_capability_lease_state(state)
    if state_errors:
        raise ValueError("lease_state_invalid:" + ";".join(state_errors))
    receipt_id = str(receipt.get("lease_renewal_receipt_digest", ""))
    if receipt_id in set(state.get("processed_renewal_digests", [])):
        return {"status": "REPLAYED", "state": deepcopy(dict(state)), "errors": []}
    receipt_errors = validate_lease_renewal_receipt(receipt)
    if receipt_errors:
        return {"status": "REJECTED", "state": deepcopy(dict(state)), "errors": receipt_errors}
    kind = str(receipt.get("kind"))
    lease = dict(state.get("leases", {}).get(kind, {}))
    expected = {
        "lease_supervisor_id": state.get("lease_supervisor_id"),
        "rotation_id": state.get("rotation_id"),
        "predecessor_state_digest": state.get("capability_lease_state_digest"),
        "owner_id": state.get("current_owner_id"),
        "epoch_digest": state.get("current_epoch_digest"),
        "scope_digest": lease.get("scope_digest"),
    }
    errors: list[str] = []
    for field, value in expected.items():
        if receipt.get(field) != value:
            errors.append(f"lease_renewal_{field}_mismatch")
    if int(receipt.get("new_expires_at_ms", 0)) <= int(lease.get("expires_at_ms", 0)):
        errors.append("renewal_expiry_not_extended")
    if errors:
        return {"status": "REJECTED", "state": deepcopy(dict(state)), "errors": errors}
    next_state = deepcopy(dict(state))
    target = next_state["leases"][kind]
    target["max_uses"] += int(receipt["additional_uses"])
    target["remaining_uses"] += int(receipt["additional_uses"])
    target["max_cost_units"] += int(receipt["additional_cost_units"])
    target["remaining_cost_units"] += int(receipt["additional_cost_units"])
    target["expires_at_ms"] = int(receipt["new_expires_at_ms"])
    target["status"] = ACTIVE
    target["renewal_count"] += 1
    target["last_renewal_receipt_digest"] = receipt_id
    next_state["processed_renewal_digests"] = list(
        next_state["processed_renewal_digests"]
    ) + [receipt_id]
    next_state["updated_at_ms"] = int(receipt["renewed_at_ms"])
    next_state["capability_lease_state_digest"] = ""
    next_state["capability_lease_state_digest"] = state_digest(next_state)
    return {"status": "APPLIED", "state": next_state, "errors": []}
