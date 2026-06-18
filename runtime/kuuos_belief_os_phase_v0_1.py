from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_belief_os_state_v0_1 import append_unique
from runtime.kuuos_belief_os_types_v0_1 import (
    NON_AUTHORITY_FLAGS,
    QI_ALLOWED_ROLES,
    QI_FORBIDDEN_ROLES,
    ROUTES,
    normalize_credal_state,
    normalize_uncertainty,
    require_bool,
    require_finite_number,
    require_mapping,
    require_nonempty_string,
    require_unique_strings,
)


def _lists(payload: Mapping[str, Any], names: tuple[str, ...]) -> dict[str, list[str]]:
    return {
        name: require_unique_strings(payload.get(name, []), name, allow_empty=True)
        for name in names
    }


def apply_phase_payload(
    state: dict[str, Any], target: str, payload: Mapping[str, Any]
) -> None:
    if target == "contextualize":
        context = dict(require_mapping(payload.get("context"), "context"))
        for field in (
            "context_id",
            "observer_id",
            "observer_role",
            "temporal_scope",
            "scale",
            "task_scope",
            "world_model_id",
        ):
            context[field] = require_nonempty_string(context.get(field), field)
        state["context"] = context
        return

    if target == "trace":
        values = _lists(
            payload,
            (
                "evidence_digests",
                "observation_digests",
                "verification_receipt_digests",
                "causal_support_digests",
            ),
        )
        if not any(values.values()):
            raise ValueError("trace_support_missing")
        for name, incoming in values.items():
            state[name] = append_unique(state[name], incoming)
        return

    if target == "weigh":
        state["credal_state"] = normalize_credal_state(
            require_mapping(payload.get("credal_state"), "credal_state")
        )
        state["uncertainty"] = normalize_uncertainty(
            require_mapping(payload.get("uncertainty"), "uncertainty")
        )
        return

    if target == "challenge":
        values = _lists(
            payload,
            (
                "counterevidence_digests",
                "contradiction_digests",
                "alternative_hypothesis_digests",
                "unresolved_residual_digests",
            ),
        )
        for name, incoming in values.items():
            state[name] = append_unique(state[name], incoming)
        return

    if target == "qi_condition":
        roles = set(
            require_unique_strings(payload.get("roles", []), "qi_roles", allow_empty=False)
        )
        if roles & QI_FORBIDDEN_ROLES:
            raise ValueError("qi_forbidden_role")
        if not roles.issubset(QI_ALLOWED_ROLES):
            raise ValueError("qi_role_unlicensed")
        if require_bool(payload.get("authority_source", False), "authority_source"):
            raise ValueError("qi_authority_forbidden")
        state["qi_process"] = {
            "process_tensor_digest": require_nonempty_string(
                payload.get("process_tensor_digest"), "process_tensor_digest"
            ),
            "history_window_digest": require_nonempty_string(
                payload.get("history_window_digest"), "history_window_digest"
            ),
            "roles": sorted(roles),
            "flow_phase": require_nonempty_string(payload.get("flow_phase"), "flow_phase"),
            "authority_source": False,
        }
        return

    if target == "two_truths_check":
        data = dict(require_mapping(payload.get("two_truths"), "two_truths"))
        samvrti = require_bool(
            data.get("samvrti_operationally_usable"),
            "samvrti_operationally_usable",
        )
        if not require_bool(data.get("paramartha_non_reified"), "paramartha_non_reified"):
            raise ValueError("paramartha_reification_forbidden")
        if not require_bool(data.get("two_truths_separated"), "two_truths_separated"):
            raise ValueError("two_truths_collapse_forbidden")
        state["two_truths"] = {
            "samvrti_operationally_usable": samvrti,
            "paramartha_non_reified": True,
            "two_truths_separated": True,
        }
        return

    if target == "middle_way_gate":
        data = dict(require_mapping(payload.get("middle_way"), "middle_way"))
        fields = (
            "reification_risk",
            "nihilistic_erasure_risk",
            "premature_closure_risk",
            "responsibility_abandonment_risk",
            "repairability",
        )
        middle_way = {
            name: require_finite_number(
                data.get(name), name, minimum=0.0, maximum=1.0
            )
            for name in fields
        }
        route = require_nonempty_string(payload.get("route"), "route").upper()
        if route not in ROUTES:
            raise ValueError("middle_way_route_invalid")
        if max(
            middle_way["reification_risk"], middle_way["nihilistic_erasure_risk"]
        ) > 0.75 and route == "CANDIDATE":
            raise ValueError("middle_way_candidate_with_high_collapse_risk")
        state["middle_way"] = middle_way
        state["route"] = route
        state["reasoning_license"] = require_bool(
            payload.get("reasoning_license", False), "reasoning_license"
        )
        state["planning_support_license"] = require_bool(
            payload.get("planning_support_license", False),
            "planning_support_license",
        )
        return

    if target == "commit":
        if not require_bool(payload.get("future_only"), "future_only"):
            raise ValueError("belief_commit_not_future_only")
        if require_bool(payload.get("memory_overwrite"), "memory_overwrite"):
            raise ValueError("belief_commit_memory_overwrite_forbidden")
        if require_nonempty_string(
            payload.get("activation_boundary"), "activation_boundary"
        ) != "mission_replan_only":
            raise ValueError("belief_commit_activation_boundary_invalid")
        if dict(require_mapping(payload.get("non_authority"), "commit_non_authority")) != NON_AUTHORITY_FLAGS:
            raise ValueError("commit_non_authority_authority_escalation")
        state["pending_replan_activation"] = True
        return

    if target == "propose":
        if not require_bool(
            payload.get("preserve_prior_revision"), "preserve_prior_revision"
        ):
            raise ValueError("prior_revision_preservation_required")
        if payload.get("claim") is not None:
            state["claim"] = require_nonempty_string(payload.get("claim"), "claim")
        if payload.get("claim_digest") is not None:
            state["claim_digest"] = require_nonempty_string(
                payload.get("claim_digest"), "claim_digest"
            )
        return

    raise ValueError("target_phase_unsupported")
