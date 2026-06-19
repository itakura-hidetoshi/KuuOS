from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_plan_os_capability_renewal_v0_10 import (
    apply_lease_renewal,
    validate_lease_renewal_receipt,
)
from runtime.kuuos_plan_os_bounded_renewal_state_v0_11 import (
    validate_bounded_renewal_state,
)
from runtime.kuuos_plan_os_bounded_renewal_types_v0_11 import (
    ACTIVE,
    ESCALATION_REQUIRED,
    RECEIPT_VERSION,
    copy_boundary,
    copy_non_authority,
    receipt_digest,
    require_int,
    require_string,
    state_digest,
)


def build_governed_renewal_receipt(
    *,
    state: Mapping[str, Any],
    lease_renewal_receipt: Mapping[str, Any],
    renewal_authority_id: str,
    authority_receipt_digest: str,
    now_ms: int,
) -> dict[str, Any]:
    errors = validate_bounded_renewal_state(state)
    if errors:
        raise ValueError("bounded_renewal_state_invalid:" + ";".join(errors))
    renewal_errors = validate_lease_renewal_receipt(lease_renewal_receipt)
    if renewal_errors:
        raise ValueError("lease_renewal_receipt_invalid:" + ";".join(renewal_errors))
    kind = require_string(lease_renewal_receipt.get("kind"), "kind")
    policy = dict(state["policies"].get(kind, {}))
    if not policy:
        raise ValueError("bounded_renewal_policy_missing")
    if policy["status"] != ACTIVE:
        raise ValueError("bounded_renewal_escalation_required")
    authority = require_string(renewal_authority_id, "renewal_authority_id")
    if authority != policy["renewal_authority_id"]:
        raise ValueError("bounded_renewal_authority_mismatch")
    current = state["current_lease_state"]
    lease = current["leases"][kind]
    expected = {
        "lease_supervisor_id": current["lease_supervisor_id"],
        "predecessor_state_digest": current["capability_lease_state_digest"],
        "owner_id": current["current_owner_id"],
        "epoch_digest": current["current_epoch_digest"],
        "scope_digest": lease["scope_digest"],
    }
    for field, value in expected.items():
        if lease_renewal_receipt.get(field) != value:
            raise ValueError(f"bounded_renewal_{field}_mismatch")
    now = require_int(now_ms, "now_ms")
    last = int(policy["last_renewed_at_ms"])
    if last > 0 and now < last + int(policy["cooldown_ms"]):
        raise ValueError("bounded_renewal_cooldown_active")
    next_count = int(policy["renewal_count"]) + 1
    next_uses = int(policy["cumulative_added_uses"]) + int(
        lease_renewal_receipt["additional_uses"]
    )
    next_cost = int(policy["cumulative_added_cost_units"]) + int(
        lease_renewal_receipt["additional_cost_units"]
    )
    if next_count > int(policy["max_renewals"]):
        raise ValueError("bounded_renewal_count_ceiling")
    if next_uses > int(policy["max_cumulative_added_uses"]):
        raise ValueError("bounded_renewal_use_ceiling")
    if next_cost > int(policy["max_cumulative_added_cost_units"]):
        raise ValueError("bounded_renewal_cost_ceiling")
    if int(lease_renewal_receipt["new_expires_at_ms"]) > int(
        policy["absolute_expires_at_ms"]
    ):
        raise ValueError("bounded_renewal_absolute_expiry_ceiling")
    receipt = {
        "version": RECEIPT_VERSION,
        "renewal_governor_id": state["renewal_governor_id"],
        "predecessor_state_digest": state["bounded_renewal_state_digest"],
        "kind": kind,
        "owner_id": current["current_owner_id"],
        "epoch_digest": current["current_epoch_digest"],
        "scope_digest": lease["scope_digest"],
        "renewal_authority_id": authority,
        "authority_receipt_digest": require_string(
            authority_receipt_digest, "authority_receipt_digest"
        ),
        "lease_renewal_receipt": deepcopy(dict(lease_renewal_receipt)),
        "next_renewal_count": next_count,
        "next_cumulative_added_uses": next_uses,
        "next_cumulative_added_cost_units": next_cost,
        "governed_at_ms": now,
        "automatic_renewal": False,
        "execution_granted": False,
        "host_license_granted": False,
        "memory_overwrite": False,
        "non_authority": copy_non_authority(),
        "boundary": copy_boundary(),
        "governed_renewal_receipt_digest": "",
    }
    receipt["governed_renewal_receipt_digest"] = receipt_digest(receipt)
    return receipt


def validate_governed_renewal_receipt(receipt: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if receipt.get("version") != RECEIPT_VERSION:
            errors.append("governed_renewal_version_invalid")
        if receipt.get("governed_renewal_receipt_digest") != receipt_digest(receipt):
            errors.append("governed_renewal_digest_invalid")
        for field in (
            "renewal_governor_id", "predecessor_state_digest", "kind",
            "owner_id", "epoch_digest", "scope_digest",
            "renewal_authority_id", "authority_receipt_digest",
        ):
            require_string(receipt.get(field), field)
        require_int(receipt.get("next_renewal_count"), "next_renewal_count", minimum=1)
        require_int(receipt.get("next_cumulative_added_uses"), "next_cumulative_added_uses", minimum=1)
        require_int(receipt.get("next_cumulative_added_cost_units"), "next_cumulative_added_cost_units", minimum=1)
        require_int(receipt.get("governed_at_ms"), "governed_at_ms")
        if validate_lease_renewal_receipt(dict(receipt.get("lease_renewal_receipt", {}))):
            errors.append("governed_renewal_inner_receipt_invalid")
        for field in ("automatic_renewal", "execution_granted", "host_license_granted", "memory_overwrite"):
            if receipt.get(field) is not False:
                errors.append(f"governed_renewal_{field}_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def apply_governed_renewal(
    state: Mapping[str, Any], receipt: Mapping[str, Any]
) -> dict[str, Any]:
    state_errors = validate_bounded_renewal_state(state)
    if state_errors:
        raise ValueError("bounded_renewal_state_invalid:" + ";".join(state_errors))
    receipt_id = str(receipt.get("governed_renewal_receipt_digest", ""))
    if receipt_id in set(state.get("processed_governed_receipt_digests", [])):
        return {"status": "REPLAYED", "state": deepcopy(dict(state)), "errors": []}
    receipt_errors = validate_governed_renewal_receipt(receipt)
    if receipt_errors:
        return {"status": "REJECTED", "state": deepcopy(dict(state)), "errors": receipt_errors}
    kind = str(receipt.get("kind"))
    policy = dict(state["policies"].get(kind, {}))
    inner = dict(receipt["lease_renewal_receipt"])
    expected = {
        "renewal_governor_id": state["renewal_governor_id"],
        "predecessor_state_digest": state["bounded_renewal_state_digest"],
        "owner_id": state["current_owner_id"],
        "epoch_digest": state["current_epoch_digest"],
        "scope_digest": state["current_lease_state"]["leases"][kind]["scope_digest"],
        "renewal_authority_id": policy.get("renewal_authority_id"),
    }
    errors: list[str] = []
    for field, value in expected.items():
        if receipt.get(field) != value:
            errors.append(f"governed_renewal_{field}_mismatch")
    if receipt.get("next_renewal_count") != int(policy.get("renewal_count", 0)) + 1:
        errors.append("governed_renewal_count_transition_invalid")
    if receipt.get("next_cumulative_added_uses") != int(policy.get("cumulative_added_uses", 0)) + int(inner.get("additional_uses", 0)):
        errors.append("governed_renewal_use_transition_invalid")
    if receipt.get("next_cumulative_added_cost_units") != int(policy.get("cumulative_added_cost_units", 0)) + int(inner.get("additional_cost_units", 0)):
        errors.append("governed_renewal_cost_transition_invalid")
    if errors:
        return {"status": "REJECTED", "state": deepcopy(dict(state)), "errors": errors}
    renewed = apply_lease_renewal(state["current_lease_state"], inner)
    if renewed.get("status") != "APPLIED":
        return {"status": "REJECTED", "state": deepcopy(dict(state)), "errors": ["governed_renewal_inner_application_rejected"]}
    next_state = deepcopy(dict(state))
    next_state["current_lease_state"] = renewed["state"]
    target = next_state["policies"][kind]
    target["renewal_count"] = int(receipt["next_renewal_count"])
    target["cumulative_added_uses"] = int(receipt["next_cumulative_added_uses"])
    target["cumulative_added_cost_units"] = int(receipt["next_cumulative_added_cost_units"])
    target["last_renewed_at_ms"] = int(receipt["governed_at_ms"])
    target["last_governed_receipt_digest"] = receipt_id
    if (
        target["renewal_count"] >= target["max_renewals"]
        or target["cumulative_added_uses"] >= target["max_cumulative_added_uses"]
        or target["cumulative_added_cost_units"] >= target["max_cumulative_added_cost_units"]
    ):
        target["status"] = ESCALATION_REQUIRED
    next_state["processed_governed_receipt_digests"] = list(next_state["processed_governed_receipt_digests"]) + [receipt_id]
    next_state["updated_at_ms"] = int(receipt["governed_at_ms"])
    next_state["bounded_renewal_state_digest"] = ""
    next_state["bounded_renewal_state_digest"] = state_digest(next_state)
    next_errors = validate_bounded_renewal_state(next_state)
    if next_errors:
        raise ValueError("bounded_renewal_next_state_invalid:" + ";".join(next_errors))
    return {"status": "APPLIED", "state": next_state, "errors": []}
