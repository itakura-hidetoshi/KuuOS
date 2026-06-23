#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
VERSION = "kuuos_memoryos_qi_world_validation_matrix_v0_36"
CASES_VERSION = "kuuos_memoryos_qi_world_validation_matrix_cases_v0_36"
MATRIX_PATH = ROOT / "manifests/kuuos_memoryos_qi_world_validation_matrix_v0_36.json"
CASES_PATH = ROOT / "validation_cases/kuuos_memoryos_qi_world_validation_matrix_cases_v0_36.json"

REQUIRED_LAYERS = {
    "static_registration",
    "runtime_unit_regression",
    "upstream_source_validation",
    "lean_typed_boundary",
    "central_runtime_regression",
}
REQUIRED_FAILURES = {
    "stale_digest",
    "replay_duplication",
    "substituted_source_packet",
    "blocker_certificate_structural_error",
    "inactive_blocker_evidence",
    "blocked_capability_inventory_mismatch",
    "memory_root_overwrite_attempt",
    "world_store_identity_change",
    "world_root_lineage_change",
    "world_generation_regression",
    "world_fragment_change_without_generation",
    "authority_promotion_from_validation",
    "test_fixture_inventory_inconsistency",
}
REQUIRED_CASES = {
    "inactive_only_exact_certificate",
    "structural_blocker_corruption",
    "blocked_capability_inventory_mismatch",
    "world_generation_regression",
    "world_fragment_change_without_generation",
    "snapshot_digest_tamper",
    "legacy_incomplete_fixture_inventory_mismatch",
    "validation_truth_promotion_attempt",
}
PATH_KEYS = {
    "component": {
        "runtime", "manifest", "validator", "tests", "documentation",
        "formal_module", "formal_root", "workflow",
    },
    "matrix_artifacts": {
        "documentation", "manifest", "validator", "tests",
        "validation_cases", "workflow", "central_runtime_check",
    },
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_matrix(matrix: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if matrix.get("version") != VERSION:
        errors.append("matrix_version_invalid")
    if matrix.get("subject_version") != "kuuos_memoryos_qi_world_blocker_integration_v0_35":
        errors.append("matrix_subject_version_invalid")
    if matrix.get("classification") != "validation_and_release_matrix":
        errors.append("matrix_classification_invalid")

    for section_name, required in PATH_KEYS.items():
        section = matrix.get(section_name)
        if not isinstance(section, dict):
            errors.append(f"{section_name}_invalid")
            continue
        for key in sorted(required):
            value = section.get(key)
            if not isinstance(value, str) or not value:
                errors.append(f"{section_name}_{key}_invalid")
            elif not (ROOT / value).is_file():
                errors.append(f"{section_name}_{key}_missing_file")

    layers = matrix.get("validation_layers")
    if not isinstance(layers, list):
        errors.append("validation_layers_invalid")
    else:
        ids: list[str] = []
        for layer in layers:
            if not isinstance(layer, dict) or not isinstance(layer.get("id"), str):
                errors.append("validation_layer_invalid")
                continue
            layer_id = layer["id"]
            ids.append(layer_id)
            if not isinstance(layer.get("command"), str) or not layer["command"]:
                errors.append(f"validation_layer_{layer_id}_command_invalid")
            for field in ("pass_means", "pass_does_not_mean"):
                values = layer.get(field)
                if not isinstance(values, list) or not values or not all(
                    isinstance(value, str) and value for value in values
                ):
                    errors.append(f"validation_layer_{layer_id}_{field}_invalid")
        if len(ids) != len(set(ids)):
            errors.append("validation_layer_ids_not_unique")
        for layer_id in sorted(REQUIRED_LAYERS - set(ids)):
            errors.append(f"validation_layer_missing_{layer_id}")

    failures = matrix.get("required_failure_classes")
    if not isinstance(failures, list):
        errors.append("required_failure_classes_invalid")
    else:
        for name in sorted(REQUIRED_FAILURES - set(failures)):
            errors.append(f"required_failure_class_missing_{name}")

    proof = matrix.get("proof_status")
    if not isinstance(proof, dict):
        errors.append("proof_status_invalid")
    else:
        if proof.get("formal_boundary") != "Lean-derived typed boundary":
            errors.append("proof_status_formal_boundary_invalid")
        if proof.get("empirical_truth") != "not established":
            errors.append("proof_status_empirical_truth_promoted")
        if proof.get("physical_persistence") != "not established":
            errors.append("proof_status_physical_persistence_promoted")

    for section_name, expected in (("non_authority", False), ("release_gate", True)):
        section = matrix.get(section_name)
        if not isinstance(section, dict) or not section:
            errors.append(f"{section_name}_invalid")
            continue
        for key, value in sorted(section.items()):
            if value is not expected:
                errors.append(f"{section_name}_{key}_invalid")
    return errors


def validate_cases(cases: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if cases.get("version") != CASES_VERSION:
        errors.append("cases_version_invalid")
    if cases.get("matrix_version") != VERSION:
        errors.append("cases_matrix_version_invalid")
    items = cases.get("cases")
    if not isinstance(items, list):
        return errors + ["cases_invalid"]
    ids: list[str] = []
    for item in items:
        if not isinstance(item, dict) or not isinstance(item.get("case_id"), str):
            errors.append("case_invalid")
            continue
        case_id = item["case_id"]
        ids.append(case_id)
        if not isinstance(item.get("failure_class"), str):
            errors.append(f"case_{case_id}_failure_class_invalid")
        if not isinstance(item.get("expected_route"), str):
            errors.append(f"case_{case_id}_expected_route_invalid")
        if item.get("authority_granted") is not False:
            errors.append(f"case_{case_id}_authority_promoted")
        if not isinstance(item.get("current_runtime_regression"), bool):
            errors.append(f"case_{case_id}_runtime_regression_flag_invalid")
    if len(ids) != len(set(ids)):
        errors.append("case_ids_not_unique")
    for case_id in sorted(REQUIRED_CASES - set(ids)):
        errors.append(f"case_missing_{case_id}")
    return errors


def validate_bindings() -> list[str]:
    checks = {
        "scripts/check_memoryos_qi_world_blocker_integration_v0_35.py": (
            "inactive_errors = {", "structural_errors = [",
        ),
        "tests/test_memoryos_qi_world_blocker_integration_v0_35.py": (
            "test_real_incomplete_blocker_certificate_is_quarantined",
            "test_real_structural_blocker_corruption_is_rejected",
            "test_blocked_capability_inventory_mismatch_is_rejected",
        ),
        "formal/KUOS/OpenHorizon/MemoryOSQiWorldBlockerIntegrationKernelV0_35.lean": (
            "memoryos_qi_world_blocker_integration_boundary",
            "memory_cannot_discharge_blocker",
        ),
        "formal/KUOS.lean": (
            "import KUOS.OpenHorizon.MemoryOSQiWorldBlockerIntegrationKernelV0_35",
        ),
        "scripts/run_kuuos_runtime_full_check_v0_48.py": (
            "check_memoryos_v036", "check_memoryos_v036()",
        ),
    }
    errors: list[str] = []
    for relative, phrases in checks.items():
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"binding_missing_file_{relative}")
            continue
        text = path.read_text(encoding="utf-8")
        for phrase in phrases:
            if phrase not in text:
                errors.append(f"binding_missing_phrase_{relative}:{phrase}")
    return errors


def main() -> int:
    errors = validate_matrix(load_json(MATRIX_PATH))
    errors += validate_cases(load_json(CASES_PATH))
    errors += validate_bindings()
    if errors:
        print("\n".join(errors))
        return 1
    print("MemoryOS Qi-WORLD validation matrix v0.36 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
