from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_plan_os_state_v0_1 import (
    build_initial_plan_state,
    build_plan_event,
    validate_plan_event_base,
    validate_plan_state,
)
from runtime.kuuos_plan_os_types_v0_1 import (
    ACTIVE_ROUTES,
    ACTIVATION_RECEIPT_VERSION,
    APPLY_RESULT_VERSION,
    STEP_CLASSES,
    copy_non_authority,
    nonnegative_number,
    normalize_string_list,
    plan_activation_receipt_digest,
    plan_apply_result_digest,
    plan_state_digest,
    require_mapping,
    require_nonempty_string,
    require_nonnegative_int,
    unit_number,
)

__all__ = [
    "apply_plan_event",
    "build_initial_plan_state",
    "build_plan_event",
    "build_plan_phase_activation_receipt",
    "validate_plan_state",
]


def _require_bool(value: Any, name: str) -> bool:
    if not isinstance(value, bool):
        raise TypeError(f"{name}_must_be_bool")
    return value


def _step_digest(value: Mapping[str, Any]) -> str:
    item = dict(value)
    item.pop("step_digest", None)
    return sha(item)


def _normalize_step(state: Mapping[str, Any], raw: Mapping[str, Any]) -> dict[str, Any]:
    step_id = require_nonempty_string(raw.get("step_id"), "step_id")
    step_class = require_nonempty_string(raw.get("step_class"), "step_class")
    if step_class not in STEP_CLASSES:
        raise ValueError("plan_step_class_invalid")
    source_option_id = str(raw.get("source_option_id", ""))
    if source_option_id and source_option_id not in set(state["source_option_ids"]):
        raise ValueError("plan_step_source_option_unknown")
    rollback_step_id = str(raw.get("rollback_step_id", ""))
    step = {
        "step_id": step_id,
        "step_class": step_class,
        "rank": require_nonnegative_int(raw.get("rank"), "rank"),
        "depends_on": normalize_string_list(raw.get("depends_on", []), "depends_on"),
        "precondition_digests": normalize_string_list(
            raw.get("precondition_digests", []), "precondition_digests"
        ),
        "expected_observation_digest": require_nonempty_string(
            raw.get("expected_observation_digest"), "expected_observation_digest"
        ),
        "verification_criterion_digest": require_nonempty_string(
            raw.get("verification_criterion_digest"),
            "verification_criterion_digest",
        ),
        "estimated_cost": nonnegative_number(raw.get("estimated_cost"), "estimated_cost"),
        "estimated_risk": unit_number(raw.get("estimated_risk"), "estimated_risk"),
        "reversibility": unit_number(raw.get("reversibility"), "reversibility"),
        "rollback_step_id": rollback_step_id,
        "stop_condition_digests": normalize_string_list(
            raw.get("stop_condition_digests", []), "stop_condition_digests"
        ),
        "requires_external_license": _require_bool(
            raw.get("requires_external_license"), "requires_external_license"
        ),
        "requires_human_review": _require_bool(
            raw.get("requires_human_review"), "requires_human_review"
        ),
        "effectful": _require_bool(raw.get("effectful"), "effectful"),
        "source_option_id": source_option_id,
        "stakeholder_scope_digests": normalize_string_list(
            raw.get("stakeholder_scope_digests", []), "stakeholder_scope_digests"
        ),
        "step_digest": "",
    }
    step["step_digest"] = _step_digest(step)
    supplied = raw.get("step_digest")
    if supplied not in (None, "", step["step_digest"]):
        raise ValueError("plan_step_digest_invalid")
    return step


def _route_classes(route: str) -> set[str]:
    if route == "PLAN_CANDIDATE":
        return set(STEP_CLASSES)
    if route == "OBSERVATION_PLAN":
        return {"observe", "prepare", "verify", "hold"}
    if route == "REPAIR_PLAN":
        return {"repair", "observe", "prepare", "verify", "hold"}
    if route == "HANDOVER_PLAN":
        return {"handover", "prepare", "observe", "verify", "hold"}
    return set()


def _validate_dependencies(steps: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    by_id = {step["step_id"]: step for step in steps}
    for step in steps:
        for dependency_id in step["depends_on"]:
            dependency = by_id.get(dependency_id)
            if dependency is None:
                errors.append(f"plan_dependency_missing:{step['step_id']}:{dependency_id}")
                continue
            if dependency_id == step["step_id"]:
                errors.append(f"plan_self_dependency:{step['step_id']}")
            if int(dependency["rank"]) >= int(step["rank"]):
                errors.append(
                    f"plan_dependency_rank_not_lower:{step['step_id']}:{dependency_id}"
                )
    return errors


def _topological_order(steps: list[dict[str, Any]]) -> list[str]:
    return [
        step["step_id"]
        for step in sorted(steps, key=lambda item: (int(item["rank"]), item["step_id"]))
    ]


def _apply_phase_payload(
    state: dict[str, Any], target_phase: str, payload: Mapping[str, Any]
) -> None:
    if target_phase == "decompose":
        raw_steps = payload.get("steps")
        if not isinstance(raw_steps, list):
            raise TypeError("plan_steps_must_be_list")
        if state["route"] in ACTIVE_ROUTES and not raw_steps:
            raise ValueError("active_plan_steps_required")
        if state["route"] not in ACTIVE_ROUTES and raw_steps:
            raise ValueError("inactive_route_steps_forbidden")
        steps = [
            _normalize_step(state, require_mapping(item, "plan_step"))
            for item in raw_steps
        ]
        step_ids = [step["step_id"] for step in steps]
        if len(step_ids) != len(set(step_ids)):
            raise ValueError("plan_step_id_duplicate")
        state["steps"] = steps
        return

    if target_phase == "order":
        require_nonempty_string(
            payload.get("dependency_receipt_digest"), "dependency_receipt_digest"
        )
        errors = _validate_dependencies(state["steps"])
        if errors:
            raise ValueError(";".join(errors))
        state["topological_order"] = _topological_order(state["steps"])
        state["dependency_receipt_digest"] = payload["dependency_receipt_digest"]
        return

    if target_phase == "resource":
        require_nonempty_string(
            payload.get("resource_receipt_digest"), "resource_receipt_digest"
        )
        total_cost = sum(float(step["estimated_cost"]) for step in state["steps"])
        peak_risk = max(
            (float(step["estimated_risk"]) for step in state["steps"]),
            default=0.0,
        )
        within_budget = total_cost <= float(state["plan_budget"]) + 1e-12
        within_risk = peak_risk <= float(state["maximum_step_risk"]) + 1e-12
        if not within_budget:
            raise ValueError("plan_budget_exceeded")
        if not within_risk:
            raise ValueError("plan_step_risk_exceeded")
        state["resource_summary"] = {
            "total_cost": total_cost,
            "peak_step_risk": peak_risk,
            "within_budget": within_budget,
            "within_risk": within_risk,
        }
        state["resource_receipt_digest"] = payload["resource_receipt_digest"]
        return

    if target_phase == "guard":
        require_nonempty_string(
            payload.get("guard_receipt_digest"), "guard_receipt_digest"
        )
        by_id = {step["step_id"]: step for step in state["steps"]}
        allowed_classes = _route_classes(state["route"])
        route_class_valid = all(step["step_class"] in allowed_classes for step in state["steps"])
        if not route_class_valid:
            raise ValueError("plan_route_step_class_invalid")
        endorsed = set(state["source_endorsed_option_ids"])
        review = set(state["source_review_option_ids"])
        all_guarded = True
        source_identity_preserved = True
        for step in state["steps"]:
            source_option_id = step["source_option_id"]
            if state["route"] == "PLAN_CANDIDATE":
                if source_option_id not in endorsed:
                    source_identity_preserved = False
            elif source_option_id and source_option_id not in review and source_option_id not in set(
                state["source_option_ids"]
            ):
                source_identity_preserved = False
            if step["effectful"]:
                if state["route"] != "PLAN_CANDIDATE" or step["step_class"] != "act_candidate":
                    all_guarded = False
                    continue
                if not step["stop_condition_digests"]:
                    all_guarded = False
                rollback_id = step["rollback_step_id"]
                rollback_valid = bool(
                    rollback_id
                    and rollback_id in by_id
                    and by_id[rollback_id]["step_class"] == "repair"
                    and int(by_id[rollback_id]["rank"]) > int(step["rank"])
                )
                escalation_valid = bool(
                    step["requires_human_review"]
                    and step["requires_external_license"]
                )
                if not (rollback_valid or escalation_valid):
                    all_guarded = False
        if not all_guarded:
            raise ValueError("plan_effect_guard_invalid")
        if not source_identity_preserved:
            raise ValueError("plan_source_identity_changed")
        state["guard_summary"] = {
            "all_effects_guarded": all_guarded,
            "source_identity_preserved": source_identity_preserved,
            "route_class_valid": route_class_valid,
        }
        state["guard_receipt_digest"] = payload["guard_receipt_digest"]
        return

    if target_phase == "checkpoint":
        require_nonempty_string(
            payload.get("checkpoint_receipt_digest"), "checkpoint_receipt_digest"
        )
        observation_ids = [
            step["step_id"] for step in state["steps"] if step["step_class"] == "observe"
        ]
        verification_ids = [
            step["step_id"] for step in state["steps"] if step["step_class"] == "verify"
        ]
        all_effects_have_checkpoint = True
        for effect in [step for step in state["steps"] if step["effectful"]]:
            found = any(
                checkpoint["step_class"] in {"observe", "verify"}
                and effect["step_id"] in checkpoint["depends_on"]
                and int(checkpoint["rank"]) > int(effect["rank"])
                for checkpoint in state["steps"]
            )
            if not found:
                all_effects_have_checkpoint = False
        if not all_effects_have_checkpoint:
            raise ValueError("plan_effect_checkpoint_missing")
        state["checkpoint_summary"] = {
            "all_effects_have_checkpoint": all_effects_have_checkpoint,
            "observation_step_ids": observation_ids,
            "verification_step_ids": verification_ids,
        }
        state["checkpoint_receipt_digest"] = payload["checkpoint_receipt_digest"]
        return

    if target_phase == "verify":
        require_nonempty_string(
            payload.get("verification_receipt_digest"),
            "verification_receipt_digest",
        )
        dependency_valid = not _validate_dependencies(state["steps"])
        resource_valid = bool(
            state["resource_summary"]["within_budget"]
            and state["resource_summary"]["within_risk"]
        )
        guard_valid = bool(
            state["guard_summary"]["all_effects_guarded"]
            and state["guard_summary"]["source_identity_preserved"]
            and state["guard_summary"]["route_class_valid"]
        )
        checkpoint_valid = bool(
            state["checkpoint_summary"]["all_effects_have_checkpoint"]
        )
        source_binding_valid = bool(
            state["source_wa_state_digest"]
            and state["source_wa_basis_digest"]
            and state["replan_activation_receipt_digest"]
            and state["next_plan_basis_digest"]
        )
        plan_verified = all(
            (
                dependency_valid,
                resource_valid,
                guard_valid,
                checkpoint_valid,
                source_binding_valid,
            )
        )
        if not plan_verified:
            raise ValueError("plan_verification_failed")
        state["verification_summary"] = {
            "dependency_valid": dependency_valid,
            "resource_valid": resource_valid,
            "guard_valid": guard_valid,
            "checkpoint_valid": checkpoint_valid,
            "source_binding_valid": source_binding_valid,
            "plan_verified": plan_verified,
        }
        state["verification_receipt_digest"] = payload[
            "verification_receipt_digest"
        ]
        state["plan_basis_digest"] = sha(
            {
                "plan_id": state["plan_id"],
                "source_wa_state_digest": state["source_wa_state_digest"],
                "source_committed_wa_digest": state[
                    "source_committed_wa_digest"
                ],
                "source_wa_basis_digest": state["source_wa_basis_digest"],
                "replan_activation_receipt_digest": state[
                    "replan_activation_receipt_digest"
                ],
                "next_plan_basis_digest": state["next_plan_basis_digest"],
                "route": state["route"],
                "steps": state["steps"],
                "topological_order": state["topological_order"],
                "resource_summary": state["resource_summary"],
                "guard_summary": state["guard_summary"],
                "checkpoint_summary": state["checkpoint_summary"],
                "verification_summary": state["verification_summary"],
            }
        )
        state["pending_plan_phase_activation"] = state["route"] in ACTIVE_ROUTES
        return

    if target_phase == "commit":
        required = {
            "future_only": True,
            "memory_overwrite": False,
            "plan_not_execution": True,
            "plan_not_host_license": True,
            "source_identity_preserved": True,
            "activation_boundary": "mission_plan_phase_only",
        }
        for field, expected in required.items():
            if payload.get(field) != expected:
                raise ValueError(f"plan_commit_{field}_invalid")
        if dict(payload.get("non_authority", {})) != copy_non_authority():
            raise ValueError("plan_commit_authority_escalation")
        if state["route"] in ACTIVE_ROUTES and not state.get("plan_basis_digest"):
            raise ValueError("plan_basis_missing")
        return

    raise ValueError("plan_target_phase_unsupported")


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
        "plan_event_digest": event_id,
        "predecessor_plan_state_digest": predecessor,
        "result_plan_state_digest": state["plan_state_digest"],
        "state": deepcopy(dict(state)),
        "errors": list(errors),
        "plan_apply_result_digest": "",
    }
    value["plan_apply_result_digest"] = plan_apply_result_digest(value)
    return value


def apply_plan_event(
    state: Mapping[str, Any], event: Mapping[str, Any]
) -> dict[str, Any]:
    state_errors = validate_plan_state(state)
    if state_errors:
        raise ValueError("invalid_plan_state:" + ";".join(state_errors))
    event_id = str(event.get("plan_event_digest", ""))
    predecessor = str(state["plan_state_digest"])
    if event_id and event_id in set(state.get("processed_event_digests", [])):
        return _result(
            status="REPLAYED",
            state=state,
            event_id=event_id,
            predecessor=predecessor,
            errors=[],
        )
    errors = validate_plan_event_base(state, event)
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
        _apply_phase_payload(next_state, target, dict(event["payload"]))
    except (TypeError, ValueError) as exc:
        return _result(
            status="REJECTED",
            state=state,
            event_id=event_id,
            predecessor=predecessor,
            errors=[str(exc)],
        )
    next_state["predecessor_plan_state_digest"] = predecessor
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
            "plan_event_digest": event_id,
            "created_at_ms": event["created_at_ms"],
        }
    ]
    if target == "commit":
        next_state["plan_version"] += 1
        next_state["completed_plans"] += 1
        next_state["latest_committed_plan_digest"] = sha(
            {
                "plan_id": next_state["plan_id"],
                "plan_version": next_state["plan_version"],
                "source_committed_wa_digest": next_state[
                    "source_committed_wa_digest"
                ],
                "plan_basis_digest": next_state["plan_basis_digest"],
                "route": next_state["route"],
                "commit_event_digest": event_id,
            }
        )
        next_state["plan_summaries"] = list(next_state["plan_summaries"]) + [
            {
                "plan_version": next_state["plan_version"],
                "route": next_state["route"],
                "step_ids": [step["step_id"] for step in next_state["steps"]],
                "topological_order": deepcopy(next_state["topological_order"]),
                "plan_basis_digest": next_state["plan_basis_digest"],
                "commit_artifact_digest": event["artifact_digest"],
                "commit_event_digest": event_id,
            }
        ]
    next_state["plan_state_digest"] = ""
    next_state["plan_state_digest"] = plan_state_digest(next_state)
    next_errors = validate_plan_state(next_state)
    if next_errors:
        raise ValueError("next_plan_state_invalid:" + ";".join(next_errors))
    return _result(
        status="APPLIED",
        state=next_state,
        event_id=event_id,
        predecessor=predecessor,
        errors=[],
    )


def build_plan_phase_activation_receipt(
    *,
    state: Mapping[str, Any],
    mission_cycle_phase: str,
    mission_cycle_state_digest: str,
    plan_phase_receipt_digest: str,
    now_ms: int,
) -> dict[str, Any]:
    errors = validate_plan_state(state)
    if errors:
        raise ValueError("invalid_plan_state:" + ";".join(errors))
    if state.get("current_phase") != "commit":
        raise ValueError("plan_not_committed")
    if state.get("pending_plan_phase_activation") is not True:
        raise ValueError("plan_not_pending_activation")
    if mission_cycle_phase != "plan":
        raise ValueError("mission_plan_phase_required")
    receipt = {
        "version": ACTIVATION_RECEIPT_VERSION,
        "plan_id": state["plan_id"],
        "lineage_id": state["lineage_id"],
        "plan_state_digest": state["plan_state_digest"],
        "committed_plan_digest": state["latest_committed_plan_digest"],
        "plan_basis_digest": state["plan_basis_digest"],
        "source_wa_basis_digest": state["source_wa_basis_digest"],
        "replan_activation_receipt_digest": state[
            "replan_activation_receipt_digest"
        ],
        "next_plan_basis_digest": state["next_plan_basis_digest"],
        "route": state["route"],
        "topological_order": deepcopy(state["topological_order"]),
        "mission_cycle_phase": "plan",
        "mission_cycle_state_digest": require_nonempty_string(
            mission_cycle_state_digest, "mission_cycle_state_digest"
        ),
        "plan_phase_receipt_digest": require_nonempty_string(
            plan_phase_receipt_digest, "plan_phase_receipt_digest"
        ),
        "future_only": True,
        "memory_overwrite": False,
        "plan_not_execution": True,
        "host_license_granted": False,
        "non_authority": copy_non_authority(),
        "created_at_ms": require_nonnegative_int(now_ms, "now_ms"),
        "plan_activation_receipt_digest": "",
    }
    receipt["plan_activation_receipt_digest"] = plan_activation_receipt_digest(
        receipt
    )
    return receipt
