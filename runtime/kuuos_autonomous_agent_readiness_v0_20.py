from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from runtime.kuuos_autonomous_agent_completion_architecture_v0_19 import (
    architecture_digest,
    readiness_report,
    validate_architecture,
)
from runtime.kuuos_mission_contract_kernel_v0_20 import digest_without

STATUS_VERSION = "kuuos_autonomous_agent_completion_status_v0_20"
REQUIRED_EVIDENCE = {
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
IMPLEMENTED_COMPONENTS = {
    "mission_contract_kernel",
    "goal_portfolio_arbitration",
    "mission_renewal_termination",
}


def status_overlay_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "status_overlay_digest")


def seal_status_overlay(value: Mapping[str, Any]) -> dict[str, Any]:
    result = deepcopy(dict(value))
    result["status_overlay_digest"] = ""
    result["status_overlay_digest"] = status_overlay_digest(result)
    return result


def validate_status_overlay(
    base_manifest: Mapping[str, Any], overlay: Mapping[str, Any]
) -> list[str]:
    errors: list[str] = []
    base_errors = validate_architecture(base_manifest)
    if base_errors:
        errors.extend("base_architecture:" + item for item in base_errors)
    if overlay.get("version") != STATUS_VERSION:
        errors.append("status_version_invalid")
    if overlay.get("release") != "v0.20":
        errors.append("status_release_invalid")
    if overlay.get("base_architecture_version") != base_manifest.get("version"):
        errors.append("base_architecture_version_mismatch")
    if overlay.get("base_architecture_digest") != architecture_digest(base_manifest):
        errors.append("base_architecture_digest_mismatch")
    if overlay.get("execution_authority_opened") is not False:
        errors.append("status_overlay_execution_authority_forbidden")
    updates = overlay.get("component_updates")
    if not isinstance(updates, list):
        errors.append("component_updates_invalid")
        updates = []
    component_by_id = {
        str(item.get("component_id", "")): item
        for item in base_manifest.get("components", [])
        if isinstance(item, Mapping)
    }
    seen: set[str] = set()
    for update in updates:
        if not isinstance(update, Mapping):
            errors.append("component_update_invalid")
            continue
        component_id = str(update.get("component_id", ""))
        if component_id in seen:
            errors.append("component_update_duplicate:" + component_id)
        seen.add(component_id)
        base_component = component_by_id.get(component_id)
        if base_component is None:
            errors.append("component_update_unknown:" + component_id)
            continue
        if update.get("from_status") != base_component.get("status"):
            errors.append("component_update_from_status_mismatch:" + component_id)
        if update.get("to_status") != "implemented":
            errors.append("component_update_target_not_implemented:" + component_id)
        if update.get("target_release") != base_component.get("target_release"):
            errors.append("component_update_release_mismatch:" + component_id)
        if base_component.get("target_release") != "v0.20":
            errors.append("component_update_not_v020_target:" + component_id)
        evidence = update.get("evidence")
        if not isinstance(evidence, Mapping):
            errors.append("component_update_evidence_missing:" + component_id)
        else:
            missing = sorted(REQUIRED_EVIDENCE - set(str(key) for key in evidence))
            if missing:
                errors.append(
                    "component_update_evidence_incomplete:" + component_id + ":" + ",".join(missing)
                )
            if any(not str(value).strip() for value in evidence.values()):
                errors.append("component_update_evidence_blank:" + component_id)
    if seen != IMPLEMENTED_COMPONENTS:
        errors.append("component_update_set_invalid:" + ",".join(sorted(seen)))
    if overlay.get("status_overlay_digest") != status_overlay_digest(overlay):
        errors.append("status_overlay_digest_invalid")
    return errors


def resolve_readiness(
    base_manifest: Mapping[str, Any], overlay: Mapping[str, Any]
) -> dict[str, Any]:
    errors = validate_status_overlay(base_manifest, overlay)
    if errors:
        raise ValueError(";".join(errors))
    resolved = deepcopy(dict(base_manifest))
    update_by_id = {
        str(item["component_id"]): item
        for item in overlay["component_updates"]
    }
    for component in resolved["components"]:
        component_id = str(component.get("component_id", ""))
        if component_id in update_by_id:
            component["status"] = "implemented"
            component["completion_evidence"] = deepcopy(dict(update_by_id[component_id]["evidence"]))
            component["implemented_release"] = "v0.20"
    report = readiness_report(resolved)
    expected = overlay.get("expected_resolved_readiness", {})
    expected_counts = {
        "implemented": int(expected.get("implemented", -1)),
        "open_gap": int(expected.get("open_gap", -1)),
        "partial_gap": int(expected.get("partial_gap", -1)),
    }
    if report["status_counts"] != expected_counts:
        raise ValueError("resolved_status_counts_mismatch")
    if report["open_component_count"] != int(expected.get("open_component_count", -1)):
        raise ValueError("resolved_open_component_count_mismatch")
    if report["next_dependency_rank"] != int(expected.get("next_dependency_rank", -1)):
        raise ValueError("resolved_next_dependency_rank_mismatch")
    if report["next_release"] != expected.get("next_release"):
        raise ValueError("resolved_next_release_mismatch")
    return {
        "version": STATUS_VERSION,
        "base_architecture_digest": architecture_digest(base_manifest),
        "status_overlay_digest": overlay["status_overlay_digest"],
        "resolved_architecture": resolved,
        "readiness_report": report,
        "classification": str(overlay["classification"]),
        "execution_authority_opened": False,
    }


def load_and_resolve(
    *,
    base_manifest_path: str | Path,
    status_overlay_path: str | Path,
) -> dict[str, Any]:
    base = json.loads(Path(base_manifest_path).read_text(encoding="utf-8"))
    overlay = json.loads(Path(status_overlay_path).read_text(encoding="utf-8"))
    if not isinstance(base, dict) or not isinstance(overlay, dict):
        raise ValueError("readiness_files_must_be_objects")
    return resolve_readiness(base, overlay)
