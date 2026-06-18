from __future__ import annotations

import hashlib
import json
from collections import Counter
from copy import deepcopy
from typing import Any, Mapping

VERSION = "kuuos_autonomous_agent_completion_architecture_v0_19"
REQUIRED_GLOBAL_INVARIANTS = {
    "bounded_cycle",
    "explicit_authority",
    "append_only_lineage",
    "checkpoint_before_handoff",
    "foreground_user_control_available",
    "unknown_not_false",
    "execution_success_not_mission_success",
    "plan_not_permission",
    "memory_not_truth",
    "learning_not_self_license",
    "wake_up_not_authority",
    "queue_not_running",
    "running_not_verified",
    "verified_not_automatic_renewal",
    "resource_exhaustion_requires_feedback",
    "self_modification_requires_externalized_gate_and_rollback",
    "graph_semantics_forbidden",
}
REQUIRED_COMPONENT_FIELDS = {
    "component_id",
    "plane_id",
    "dependency_rank",
    "target_release",
    "status",
    "depends_on",
    "consumes",
    "produces",
    "failure_states",
    "non_authority",
}
ALLOWED_STATUSES = {"implemented", "open_gap", "partial_gap"}
REQUIRED_INTEGRATION_DEPENDENCIES = {
    "mission_renewal_termination",
    "observation_belief_kernel",
    "semantic_planner_replanner",
    "outcome_verifier",
    "cognitive_memory_consolidator",
    "bounded_credit_assignment",
    "transactional_tool_fabric",
    "world_state_reconciliation",
    "event_wakeup_fabric",
    "user_control_status_plane",
    "resource_model_governor",
    "governed_self_modification",
}
FORBIDDEN_TARGET_EQUIVALENCES = {
    "unbounded_authority",
    "unbounded_resource_use",
    "arbitrary_shell_execution",
    "arbitrary_network_execution",
    "irreversible_self_modification",
    "hidden_background_execution",
}


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def architecture_digest(manifest: Mapping[str, Any]) -> str:
    return hashlib.sha256(canonical_json(dict(manifest)).encode("utf-8")).hexdigest()


def _as_list(value: Any) -> list[Any]:
    return list(value) if isinstance(value, list) else []


def _as_mapping(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, Mapping) else {}


def _rank(value: Mapping[str, Any]) -> int:
    try:
        return int(value.get("dependency_rank", -1))
    except (TypeError, ValueError):
        return -1


def _dependency_cycle_errors(component_by_id: Mapping[str, Mapping[str, Any]]) -> list[str]:
    state: dict[str, int] = {}
    stack: list[str] = []
    errors: list[str] = []
    recorded: set[str] = set()

    def visit(component_id: str) -> None:
        marker = state.get(component_id, 0)
        if marker == 2:
            return
        if marker == 1:
            if component_id in stack:
                start = stack.index(component_id)
                cycle = stack[start:] + [component_id]
                canonical = "->".join(cycle)
                if canonical not in recorded:
                    recorded.add(canonical)
                    errors.append("component_dependency_cycle:" + canonical)
            return
        state[component_id] = 1
        stack.append(component_id)
        component = component_by_id.get(component_id, {})
        for dependency_id in sorted(str(item) for item in _as_list(component.get("depends_on"))):
            if dependency_id in component_by_id:
                visit(dependency_id)
        stack.pop()
        state[component_id] = 2

    for component_id in sorted(component_by_id):
        visit(component_id)
    return errors


def validate_architecture(manifest: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    if str(manifest.get("version", "")) != VERSION:
        errors.append("architecture_version_invalid")
    if str(manifest.get("status", "")) != "architecture_contract_only":
        errors.append("architecture_status_invalid")

    target = _as_mapping(manifest.get("target_definition"))
    definition = str(target.get("definition", ""))
    if "bounded" not in definition or "licensed" not in definition or "replay-safe" not in definition:
        errors.append("target_definition_missing_bounded_continuation")
    non_equivalences = {str(item) for item in _as_list(target.get("explicit_non_equivalences"))}
    missing_non_equivalences = sorted(FORBIDDEN_TARGET_EQUIVALENCES - non_equivalences)
    if missing_non_equivalences:
        errors.append("target_non_equivalences_missing:" + ",".join(missing_non_equivalences))

    global_invariants = {str(item) for item in _as_list(manifest.get("global_invariants"))}
    missing_invariants = sorted(REQUIRED_GLOBAL_INVARIANTS - global_invariants)
    if missing_invariants:
        errors.append("global_invariants_missing:" + ",".join(missing_invariants))

    components = [_as_mapping(item) for item in _as_list(manifest.get("components"))]
    component_ids = [str(item.get("component_id", "")) for item in components]
    if not components:
        errors.append("components_missing")
    if any(not item for item in component_ids):
        errors.append("component_id_missing")
    duplicate_components = sorted(key for key, count in Counter(component_ids).items() if key and count > 1)
    if duplicate_components:
        errors.append("duplicate_component_id:" + ",".join(duplicate_components))
    component_by_id = {
        str(item.get("component_id", "")): item
        for item in components
        if str(item.get("component_id", ""))
    }

    planes = [_as_mapping(item) for item in _as_list(manifest.get("planes"))]
    plane_ids = [str(item.get("plane_id", "")) for item in planes]
    duplicate_planes = sorted(key for key, count in Counter(plane_ids).items() if key and count > 1)
    if duplicate_planes:
        errors.append("duplicate_plane_id:" + ",".join(duplicate_planes))
    declared_plane_ids = set(plane_ids) | {"existing_substrate"}
    referenced_components: set[str] = set()
    for plane in planes:
        for component_id in _as_list(plane.get("component_ids")):
            key = str(component_id)
            referenced_components.add(key)
            if key not in component_by_id:
                errors.append(f"plane_component_unknown:{plane.get('plane_id', '')}:{key}")

    for component in components:
        component_id = str(component.get("component_id", ""))
        missing_fields = sorted(field for field in REQUIRED_COMPONENT_FIELDS if field not in component)
        if missing_fields:
            errors.append(f"component_fields_missing:{component_id}:" + ",".join(missing_fields))
        plane_id = str(component.get("plane_id", ""))
        if plane_id not in declared_plane_ids:
            errors.append(f"component_plane_unknown:{component_id}:{plane_id}")
        if plane_id != "existing_substrate" and component_id not in referenced_components:
            errors.append(f"component_not_listed_in_plane:{component_id}")
        status = str(component.get("status", ""))
        if status not in ALLOWED_STATUSES:
            errors.append(f"component_status_invalid:{component_id}:{status}")
        rank = _rank(component)
        if rank < 0:
            errors.append(f"component_rank_invalid:{component_id}")
        target_release = str(component.get("target_release", ""))
        if status != "implemented" and not target_release.startswith("v0."):
            errors.append(f"component_target_release_missing:{component_id}")
        if not _as_list(component.get("consumes")):
            errors.append(f"component_consumes_missing:{component_id}")
        if not _as_list(component.get("produces")):
            errors.append(f"component_produces_missing:{component_id}")
        if not _as_list(component.get("failure_states")):
            errors.append(f"component_failure_states_missing:{component_id}")
        if not str(component.get("non_authority", "")).strip():
            errors.append(f"component_non_authority_missing:{component_id}")
        dependencies = [str(item) for item in _as_list(component.get("depends_on"))]
        if component_id in dependencies:
            errors.append(f"component_self_dependency:{component_id}")
        for dependency_id in dependencies:
            dependency = component_by_id.get(dependency_id)
            if dependency is None:
                errors.append(f"component_dependency_unknown:{component_id}:{dependency_id}")
                continue
            dependency_rank = _rank(dependency)
            if dependency_rank > rank:
                errors.append(
                    f"component_dependency_rank_reversed:{component_id}:{dependency_id}:{rank}:{dependency_rank}"
                )

    errors.extend(_dependency_cycle_errors(component_by_id))

    substrate = component_by_id.get("execution_substrate", {})
    if substrate.get("status") != "implemented" or _rank(substrate) != 0:
        errors.append("execution_substrate_baseline_invalid")

    integration = component_by_id.get("integrated_indefinite_operation", {})
    integration_dependencies = {str(item) for item in _as_list(integration.get("depends_on"))}
    missing_integration_dependencies = sorted(REQUIRED_INTEGRATION_DEPENDENCIES - integration_dependencies)
    if missing_integration_dependencies:
        errors.append("integration_dependencies_missing:" + ",".join(missing_integration_dependencies))
    if _rank(integration) != 8:
        errors.append("integration_rank_invalid")

    releases = [_as_mapping(item) for item in _as_list(manifest.get("release_order"))]
    release_ranks = [_rank(item) for item in releases]
    if release_ranks != sorted(release_ranks) or release_ranks != list(range(1, 9)):
        errors.append("release_order_invalid")
    releases_by_rank = {
        _rank(item): str(item.get("release", ""))
        for item in releases
    }
    for component in components:
        status = str(component.get("status", ""))
        rank = _rank(component)
        if status == "implemented" or rank == 0:
            continue
        expected_release = releases_by_rank.get(rank)
        if expected_release and str(component.get("target_release", "")) != expected_release:
            errors.append(
                f"component_release_rank_mismatch:{component.get('component_id', '')}:{component.get('target_release', '')}:{expected_release}"
            )

    completion_rule = _as_mapping(manifest.get("completion_rule"))
    required_evidence = {str(item) for item in _as_list(completion_rule.get("required_evidence"))}
    expected_evidence = {
        "versioned_contract",
        "typed_inputs_outputs",
        "failure_states",
        "non_authority_boundary",
        "identity_binding",
        "replay_and_stale_state_behavior",
        "persistence_semantics",
        "kernel_validation",
        "lower_layer_integration_validation",
        "honest_formal_status",
    }
    missing_evidence = sorted(expected_evidence - required_evidence)
    if missing_evidence:
        errors.append("completion_evidence_missing:" + ",".join(missing_evidence))
    return errors


def readiness_report(manifest: Mapping[str, Any]) -> dict[str, Any]:
    errors = validate_architecture(manifest)
    components = [_as_mapping(item) for item in _as_list(manifest.get("components"))]
    status_counts = Counter(str(item.get("status", "")) for item in components)
    open_components = [
        {
            "component_id": str(item.get("component_id", "")),
            "target_release": str(item.get("target_release", "")),
            "dependency_rank": _rank(item),
            "status": str(item.get("status", "")),
        }
        for item in components
        if str(item.get("status", "")) != "implemented"
    ]
    open_components.sort(key=lambda item: (item["dependency_rank"], item["component_id"]))
    next_rank = min((item["dependency_rank"] for item in open_components), default=None)
    next_components = [item for item in open_components if item["dependency_rank"] == next_rank]
    return {
        "version": VERSION,
        "architecture_digest": architecture_digest(manifest),
        "valid": not errors,
        "errors": errors,
        "component_count": len(components),
        "status_counts": dict(sorted(status_counts.items())),
        "open_component_count": len(open_components),
        "next_dependency_rank": next_rank,
        "next_components": next_components,
        "next_release": next_components[0]["target_release"] if next_components else "complete",
        "classification": "structured_completion_architecture" if not errors else "invalid_architecture",
        "execution_authority_opened": False,
    }


def assert_valid_architecture(manifest: Mapping[str, Any]) -> dict[str, Any]:
    report = readiness_report(manifest)
    if not report["valid"]:
        raise ValueError(";".join(report["errors"]))
    return deepcopy(report)
