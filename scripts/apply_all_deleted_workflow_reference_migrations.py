#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {ROOT / "scripts" / "check_workflow_consolidation_integrity.py"}

MAPPINGS = {
    ".github/workflows/all_governance_validation.yml": ".github/workflows/all_governance_validation.yml",
    ".github/workflows/all_governance_validation.yml": ".github/workflows/all_governance_validation.yml",
    ".github/workflows/all_governance_validation.yml": ".github/workflows/all_governance_validation.yml",
    ".github/workflows/all_governance_validation.yml": ".github/workflows/all_governance_validation.yml",
    ".github/workflows/all_governance_validation.yml": ".github/workflows/all_governance_validation.yml",
    ".github/workflows/all_governance_validation.yml": ".github/workflows/all_governance_validation.yml",
    ".github/workflows/all_governance_validation.yml": ".github/workflows/all_governance_validation.yml",
    ".github/workflows/all_governance_validation.yml": ".github/workflows/all_governance_validation.yml",
    ".github/workflows/decision-os-validation.yml": ".github/workflows/decision-os-validation.yml",
    ".github/workflows/decision-os-validation.yml": ".github/workflows/decision-os-validation.yml",
    ".github/workflows/decision-os-validation.yml": ".github/workflows/decision-os-validation.yml",
    ".github/workflows/evidence-cycle-os-validation.yml": ".github/workflows/evidence-cycle-os-validation.yml",
    ".github/workflows/evidence-cycle-os-validation.yml": ".github/workflows/evidence-cycle-os-validation.yml",
    ".github/workflows/evidence-cycle-os-validation.yml": ".github/workflows/evidence-cycle-os-validation.yml",
    ".github/workflows/evidence-cycle-os-validation.yml": ".github/workflows/evidence-cycle-os-validation.yml",
    ".github/workflows/evidence-cycle-os-validation.yml": ".github/workflows/evidence-cycle-os-validation.yml",
    ".github/workflows/plan-os-validation.yml": ".github/workflows/plan-os-validation.yml",
    ".github/workflows/plan-os-validation.yml": ".github/workflows/plan-os-validation.yml",
    ".github/workflows/plan-os-validation.yml": ".github/workflows/plan-os-validation.yml",
    ".github/workflows/plan-os-validation.yml": ".github/workflows/plan-os-validation.yml",
    ".github/workflows/memoryos-world-observe-intake-v0-39.yml": ".github/workflows/memoryos-world-observe-intake-v0-39.yml",
    ".github/workflows/memoryos-qi-world-validation-matrix-v0-36.yml": ".github/workflows/memoryos-qi-world-validation-matrix-v0-36.yml",
    ".github/workflows/kuuos_qi_naming_cleanup_validation.yml": ".github/workflows/kuuos_qi_naming_cleanup_validation.yml",
    ".github/workflows/kuuos_qi_naming_cleanup_validation.yml": ".github/workflows/kuuos_qi_naming_cleanup_validation.yml",
}

RUNTIME_WORKFLOWS = [
    "efe_landscape_validation.yml",
    "kuuos_closed_loop_validation.yml",
    "kuuos_example_runner_validation.yml",
    "kuuos_loop_driver_validation.yml",
    "kuuos_qi_process_tensor_downstream_validation.yml",
    "kuuos_qi_process_tensor_example_validation.yml",
    "kuuos_qi_process_tensor_validation.yml",
    "kuuos_runtime_daemon_active_inference_feature_compiler_validation.yml",
    "kuuos_runtime_daemon_active_inference_kernel_validation.yml",
    "kuuos_runtime_daemon_active_inference_output_validation.yml",
    "kuuos_runtime_daemon_belief_state_manifold_validation.yml",
    "kuuos_runtime_daemon_emptiness_gate_validation.yml",
    "kuuos_runtime_daemon_example_validation.yml",
    "kuuos_runtime_daemon_four_image_phase_gauge_validation.yml",
    "kuuos_runtime_daemon_qi_policy_validation.yml",
    "kuuos_runtime_daemon_qique_gauge_validation.yml",
    "kuuos_runtime_daemon_status_validation.yml",
    "kuuos_runtime_daemon_validation.yml",
    "kuuos_runtime_daemon_wa_function_validation.yml",
    "kuuos_runtime_daemon_wa_output_validation.yml",
    "kuuos_runtime_daemon_yinyang_polarity_gauge_validation.yml",
    "kuuos_runtime_manifest_validation.yml",
    "kuuos_state_io_example_validation.yml",
    "kuuos_state_io_validation.yml",
    "policy_flow_governor_validation.yml",
    "policy_flow_validation.yml",
    "precision_geometry_validation.yml",
    "qi_process_tensor_actuator_validation.yml",
]

for workflow in RUNTIME_WORKFLOWS:
    MAPPINGS[f".github/workflows/{workflow}"] = ".github/workflows/kuuos_runtime_full_check.yml"


def main() -> int:
    changed: list[Path] = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path in EXCLUDED or ".git" in path.parts:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        migrated = text
        for old, new in MAPPINGS.items():
            migrated = migrated.replace(old, new)
        if migrated != text:
            path.write_text(migrated, encoding="utf-8")
            changed.append(path.relative_to(ROOT))

    for path in changed:
        print(path)
    print(f"updated={len(changed)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
