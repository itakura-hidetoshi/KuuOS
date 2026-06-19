from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_plan_os_renewal_escalation_state_v0_12 import (
    validate_renewal_escalation_state,
)
from runtime.kuuos_plan_os_renewal_escalation_types_v0_12 import (
    BOUNDARY,
    DECISION_VERSION,
    DENY,
    HANDOVER_PENDING,
    HUMAN_HANDOVER,
    NON_AUTHORITY,
    OPEN,
    RE_ROTATE,
    RESOLVED_DENIED,
    REROTATION_AUTHORIZED,
    ROUTES,
    copy_boundary,
    copy_non_authority,
    decision_digest,
    require_int,
    require_string,
    state_digest,
)


def build_escalation_decision(
    *,
    state: Mapping[str, Any],
    route: str,
    governance_authority_id: str,
    governance_receipt_digest: str,
    target_owner_id: str = "",
    human_acceptance_digest: str = "",
    rerotation_scope_digest: str = "",
    now_ms: int,
) -> dict[str, Any]:
    errors = validate_renewal_escalation_state(state)
    if errors:
        raise ValueError("escalation_state_invalid:" + ";".join(errors))
    if state.get("status") != OPEN:
        raise ValueError("escalation_already_resolved")
    selected = require_string(route, "route")
    if selected not in ROUTES:
        raise ValueError("escalation_route_invalid")
    authority = require_string(
        governance_authority_id, "governance_authority_id"
    )
    authority_receipt = require_string(
        governance_receipt_digest, "governance_receipt_digest"
    )
    target = target_owner_id
    acceptance = human_acceptance_digest
    scope = rerotation_scope_digest
    next_epoch = 0
    seed = ""
    continuation = False
    if selected == DENY:
        if target or acceptance or scope:
            raise ValueError("deny_route_extra_fields_forbidden")
    elif selected == HUMAN_HANDOVER:
        target = require_string(target, "target_owner_id")
        if target == state.get("current_owner_id"):
            raise ValueError("handover_target_must_differ")
        acceptance = require_string(
            acceptance, "human_acceptance_digest"
        )
        if scope:
            raise ValueError("handover_rerotation_scope_forbidden")
    else:
        if target and target != state.get("current_owner_id"):
            raise ValueError("rerotation_owner_mismatch")
        target = str(state["current_owner_id"])
        scope = require_string(scope, "rerotation_scope_digest")
        if acceptance:
            raise ValueError("rerotation_human_acceptance_forbidden")
        next_epoch = int(state["current_epoch_index"]) + 1
        seed = sha(
            {
                "escalation_state_digest": state[
                    "renewal_escalation_state_digest"
                ],
                "governance_authority_id": authority,
                "governance_receipt_digest": authority_receipt,
                "current_epoch_index": state["current_epoch_index"],
                "next_epoch_index": next_epoch,
                "current_owner_id": state["current_owner_id"],
                "rerotation_scope_digest": scope,
            }
        )
        continuation = True
    decision = {
        "version": DECISION_VERSION,
        "escalation_id": state["escalation_id"],
        "predecessor_state_digest": state[
            "renewal_escalation_state_digest"
        ],
        "bounded_renewal_state_digest": state[
            "bounded_renewal_state_digest"
        ],
        "capability_kind": state["capability_kind"],
        "current_owner_id": state["current_owner_id"],
        "current_epoch_index": state["current_epoch_index"],
        "current_epoch_digest": state["current_epoch_digest"],
        "route": selected,
        "governance_authority_id": authority,
        "governance_receipt_digest": authority_receipt,
        "target_owner_id": target,
        "human_acceptance_digest": acceptance,
        "rerotation_scope_digest": scope,
        "next_epoch_index": next_epoch,
        "next_epoch_seed_digest": seed,
        "old_lease_lineage_closed": True,
        "new_v09_chain_required": selected == RE_ROTATE,
        "continuation_granted": continuation,
        "decided_at_ms": require_int(now_ms, "now_ms"),
        "execution_granted": False,
        "host_license_granted": False,
        "memory_overwrite": False,
        "non_authority": copy_non_authority(),
        "boundary": copy_boundary(),
        "renewal_escalation_decision_digest": "",
    }
    decision["renewal_escalation_decision_digest"] = decision_digest(
        decision
    )
    return decision


def validate_escalation_decision(decision: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if decision.get("version") != DECISION_VERSION:
            errors.append("escalation_decision_version_invalid")
        if decision.get("renewal_escalation_decision_digest") != decision_digest(
            decision
        ):
            errors.append("escalation_decision_digest_invalid")
        for field in (
            "escalation_id",
            "predecessor_state_digest",
            "bounded_renewal_state_digest",
            "capability_kind",
            "current_owner_id",
            "current_epoch_digest",
            "route",
            "governance_authority_id",
            "governance_receipt_digest",
        ):
            require_string(decision.get(field), field)
        require_int(
            decision.get("current_epoch_index"),
            "current_epoch_index",
            minimum=1,
        )
        require_int(decision.get("next_epoch_index"), "next_epoch_index")
        require_int(decision.get("decided_at_ms"), "decided_at_ms")
        route = decision.get("route")
        if route not in ROUTES:
            errors.append("escalation_decision_route_invalid")
        if decision.get("old_lease_lineage_closed") is not True:
            errors.append("escalation_decision_lineage_not_closed")
        if route == DENY:
            if any(
                (
                    decision.get("target_owner_id"),
                    decision.get("human_acceptance_digest"),
                    decision.get("rerotation_scope_digest"),
                    decision.get("next_epoch_seed_digest"),
                )
            ):
                errors.append("deny_decision_extra_fields_invalid")
            if decision.get("next_epoch_index") != 0:
                errors.append("deny_decision_next_epoch_invalid")
            if decision.get("new_v09_chain_required") is not False:
                errors.append("deny_decision_v09_invalid")
            if decision.get("continuation_granted") is not False:
                errors.append("deny_decision_continuation_invalid")
        elif route == HUMAN_HANDOVER:
            require_string(decision.get("target_owner_id"), "target_owner_id")
            require_string(
                decision.get("human_acceptance_digest"),
                "human_acceptance_digest",
            )
            if decision.get("target_owner_id") == decision.get(
                "current_owner_id"
            ):
                errors.append("handover_decision_owner_not_distinct")
            if decision.get("new_v09_chain_required") is not False:
                errors.append("handover_decision_v09_invalid")
            if decision.get("continuation_granted") is not False:
                errors.append("handover_decision_continuation_invalid")
        elif route == RE_ROTATE:
            require_string(decision.get("target_owner_id"), "target_owner_id")
            require_string(
                decision.get("rerotation_scope_digest"),
                "rerotation_scope_digest",
            )
            require_string(
                decision.get("next_epoch_seed_digest"),
                "next_epoch_seed_digest",
            )
            if decision.get("target_owner_id") != decision.get(
                "current_owner_id"
            ):
                errors.append("rerotation_decision_owner_invalid")
            if decision.get("next_epoch_index") != int(
                decision.get("current_epoch_index", 0)
            ) + 1:
                errors.append("rerotation_decision_epoch_invalid")
            if decision.get("new_v09_chain_required") is not True:
                errors.append("rerotation_decision_v09_invalid")
            if decision.get("continuation_granted") is not True:
                errors.append("rerotation_decision_continuation_invalid")
        for field in (
            "execution_granted",
            "host_license_granted",
            "memory_overwrite",
        ):
            if decision.get(field) is not False:
                errors.append(f"escalation_decision_{field}_invalid")
        if dict(decision.get("non_authority", {})) != NON_AUTHORITY:
            errors.append("escalation_decision_non_authority_invalid")
        if dict(decision.get("boundary", {})) != BOUNDARY:
            errors.append("escalation_decision_boundary_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def apply_escalation_decision(
    state: Mapping[str, Any], decision: Mapping[str, Any]
) -> dict[str, Any]:
    state_errors = validate_renewal_escalation_state(state)
    if state_errors:
        raise ValueError("escalation_state_invalid:" + ";".join(state_errors))
    decision_id = str(decision.get("renewal_escalation_decision_digest", ""))
    if state.get("resolution_decision_digest") == decision_id and decision_id:
        return {"status": "REPLAYED", "state": deepcopy(dict(state)), "errors": []}
    if state.get("status") != OPEN:
        return {
            "status": "REJECTED",
            "state": deepcopy(dict(state)),
            "errors": ["escalation_already_resolved"],
        }
    decision_errors = validate_escalation_decision(decision)
    if decision_errors:
        return {
            "status": "REJECTED",
            "state": deepcopy(dict(state)),
            "errors": decision_errors,
        }
    expected = {
        "escalation_id": state.get("escalation_id"),
        "predecessor_state_digest": state.get(
            "renewal_escalation_state_digest"
        ),
        "bounded_renewal_state_digest": state.get(
            "bounded_renewal_state_digest"
        ),
        "capability_kind": state.get("capability_kind"),
        "current_owner_id": state.get("current_owner_id"),
        "current_epoch_index": state.get("current_epoch_index"),
        "current_epoch_digest": state.get("current_epoch_digest"),
    }
    errors: list[str] = []
    for field, value in expected.items():
        if decision.get(field) != value:
            errors.append(f"escalation_decision_{field}_mismatch")
    if errors:
        return {
            "status": "REJECTED",
            "state": deepcopy(dict(state)),
            "errors": errors,
        }
    route = str(decision["route"])
    next_state = deepcopy(dict(state))
    next_state["status"] = {
        DENY: RESOLVED_DENIED,
        HUMAN_HANDOVER: HANDOVER_PENDING,
        RE_ROTATE: REROTATION_AUTHORIZED,
    }[route]
    next_state["resolution_route"] = route
    next_state["resolution_decision_digest"] = decision_id
    next_state["target_owner_id"] = decision["target_owner_id"]
    next_state["next_epoch_index"] = decision["next_epoch_index"]
    next_state["next_epoch_seed_digest"] = decision[
        "next_epoch_seed_digest"
    ]
    next_state["old_lease_lineage_closed"] = True
    next_state["new_v09_chain_required"] = decision[
        "new_v09_chain_required"
    ]
    next_state["continuation_granted"] = decision[
        "continuation_granted"
    ]
    next_state["updated_at_ms"] = int(decision["decided_at_ms"])
    next_state["renewal_escalation_state_digest"] = ""
    next_state["renewal_escalation_state_digest"] = state_digest(next_state)
    next_errors = validate_renewal_escalation_state(next_state)
    if next_errors:
        raise ValueError("escalation_next_state_invalid:" + ";".join(next_errors))
    return {"status": "APPLIED", "state": next_state, "errors": []}
