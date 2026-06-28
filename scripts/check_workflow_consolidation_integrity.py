#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import pathlib
import re
import shlex

ROOT = pathlib.Path(__file__).resolve().parents[1]
SELF = pathlib.Path(__file__).resolve()
DIRECT_WORKFLOW_PATTERN = re.compile(r"\.github/workflows/[A-Za-z0-9_./-]+\.ya?ml")
CONSTRUCTED_WORKFLOW_PATTERN = re.compile(
    r"ROOT\s*/\s*[\"']\.github[\"']\s*/\s*[\"']workflows[\"']\s*/\s*[\"']([^\"']+\.ya?ml)[\"']"
)

REQUIRED_FILES = [
    ".github/workflows/all_governance_validation.yml",
    ".github/workflows/pr-governance-gate.yml",
    ".github/workflows/core_governance_validation.yml",
    ".github/workflows/world-four-great-phase-dynamics-v0-59.yml",
    ".github/workflows/decision-os-validation.yml",
    ".github/workflows/evidence-cycle-os-validation.yml",
    ".github/workflows/plan-os-validation.yml",
    "scripts/run_plan_os_full_checks.py",
    "scripts/select_impacted_checks.py",
    "scripts/run_ci_check.py",
    "scripts/build_audit_summary.py",
    "ci/check_registry.yaml",
    ".github/WORKFLOW_INDEX.md",
]

FORBIDDEN_LEGACY_FILES = [
    ".github/workflows/gpt_github_integration_validation.yml",
    ".github/workflows/teni_observability_validation.yml",
    ".github/workflows/qi_motion_chain_validation.yml",
    ".github/workflows/physical_quantum_qi_runtime_validation.yml",
    ".github/workflows/physical_quantum_qi_deepening_validation.yml",
    ".github/workflows/mgap4d_external_audit_readiness_ci_ledger_v0_1.yml",
    ".github/workflows/emptiness_two_truths_runtime_audit_validation.yml",
    ".github/workflows/emptiness_superposition_noncollapse_validation.yml",
    ".github/workflows/decision-os-v0-1-relational-deliberation-validation.yml",
    ".github/workflows/decision-os-v0-2-plural-harmony-appeal-validation.yml",
    ".github/workflows/decision-os-wa-v0-3-validation.yml",
    ".github/workflows/act-os-v0-1-validation.yml",
    ".github/workflows/act-os-v0-2-validation.yml",
    ".github/workflows/observe-os-v0-1-validation.yml",
    ".github/workflows/verify-os-v0-1-validation.yml",
    ".github/workflows/learn-os-v0-1-validation.yml",
    ".github/workflows/plan-os-v0-1-validation.yml",
    ".github/workflows/plan-os-v0-2-validation.yml",
    ".github/workflows/plan-os-v0-3-validation.yml",
    ".github/workflows/plan-os-v0-17-validation.yml",
    ".github/workflows/memoryos-analytic-hilbert-context-v0-38.yml",
    ".github/workflows/memoryos-qi-world-blocker-integration-v0-35.yml",
    ".github/workflows/kuuos_qi_meridian_validation.yml",
    ".github/workflows/kuuos_qi_sanjiao_validation.yml",
    "scripts/run_plan_os_full_checks_v0_17.py",
]

REQUIRED_MARKERS = {
    ".github/workflows/all_governance_validation.yml": [
        "workflow_dispatch:",
        "branches:",
        "- main",
        "KUUOS_FULL_WORKFLOW_SCAN: '1'",
        "scripts/run_all_governance_full_checks_v0_1.py",
        "cancel-in-progress: false",
    ],
    ".github/workflows/pr-governance-gate.yml": [
        "pull_request:",
        "scripts/select_impacted_checks.py",
        "max-parallel: 4",
        "scripts/run_ci_check.py",
        "scripts/build_audit_summary.py",
        "audit-report.md",
    ],
    ".github/workflows/core_governance_validation.yml": [
        "workflow_dispatch:",
        "set -euo pipefail",
        "scripts/run_core_governance_full_checks_v0_1.py",
        "core-governance.log",
        "actions/upload-artifact@v4",
    ],
    ".github/workflows/world-four-great-phase-dynamics-v0-59.yml": [
        "workflow_dispatch:",
        "set -euo pipefail",
        "scripts/check_world_four_great_phase_dynamics_v0_59.py",
        "manifests/world_four_great_phase_dynamics_v0_59.json",
        "formal/KUOS/WORLD/**",
        "formal/KuuOSFourGreatCoreV0_59.lean",
        "formal/KuuOSFormalV0_59.lean",
        "build KuuOSFourGreatCoreV0_59 KuuOSFormalV0_59",
        "world-v059-diagnostics-${{ github.run_id }}-${{ github.run_attempt }}",
        "actions/upload-artifact@v4",
    ],
    ".github/workflows/decision-os-validation.yml": [
        "set -euo pipefail",
        "check_decisionos_admissible_candidate_selection_v0_4.py",
        "scripts/check_decision_os_*.py",
        "scripts/check_decisionos_*.py",
    ],
    ".github/workflows/evidence-cycle-os-validation.yml": [
        "set -euo pipefail",
        "PYTHONPATH=.",
        "check_observe_os_replan_lineage_observation_envelope_v0_2.py",
        "check_verify_os_replan_lineage_verification_envelope_v0_2.py",
        "check_learn_os_replan_lineage_future_only_learning_envelope_v0_2.py",
        "check_actos_bounded_adapter_invocation_v0_4.py",
        "check_observeos_world_host_effect_observation_v0_4.py",
    ],
    ".github/workflows/plan-os-validation.yml": [
        "scripts/run_plan_os_full_checks.py",
        "scripts/check_plan_os_*.py",
        "scripts/check_planos_*.py",
    ],
    "scripts/run_plan_os_full_checks.py": [
        "PYTHONPATH",
        "check_plan_os_closed_loop_replan_intake_adapter_v0_4.py",
        "check_plan_os_generational_replan_cycle_driver_v0_5.py",
        "check_planos_activation_admission_actos_handoff_v0_23.py",
        "PASS: PlanOS v0.1-v0.23 validation completed",
    ],
    "ci/check_registry.yaml": [
        "selection optimization != authority expansion",
        "unknown_impact",
        "full_audit_paths",
        "full-governance",
    ],
}


def workflow_references(text: str) -> set[str]:
    references = set(DIRECT_WORKFLOW_PATTERN.findall(text))
    references.update(
        f".github/workflows/{name}"
        for name in CONSTRUCTED_WORKFLOW_PATTERN.findall(text)
    )
    return references


def all_repository_files() -> list[pathlib.Path]:
    return [
        path
        for path in sorted(ROOT.rglob("*"))
        if path.is_file() and path.resolve() != SELF and ".git" not in path.parts
    ]


def selected_reference_files() -> list[pathlib.Path]:
    if os.environ.get("KUUOS_FULL_WORKFLOW_SCAN") == "1":
        return all_repository_files()

    selection_path = os.environ.get("KUUOS_CI_SELECTION")
    if not selection_path:
        # Local/manual use without a selection receipt remains conservative.
        return all_repository_files()

    try:
        selection = json.loads(pathlib.Path(selection_path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return all_repository_files()

    candidates = {ROOT / relative for relative in REQUIRED_FILES}
    candidates.update(ROOT / relative for relative in selection.get("changed_paths", []))
    return [
        path
        for path in sorted(candidates)
        if path.is_file() and path.resolve() != SELF and ".git" not in path.parts
    ]


def check_repository_workflow_references(errors: list[str]) -> None:
    for path in selected_reference_files():
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for workflow in sorted(workflow_references(text)):
            if not (ROOT / workflow).is_file():
                errors.append(
                    f"missing workflow reference: {path.relative_to(ROOT)} -> {workflow}"
                )


def check_registry(errors: list[str]) -> None:
    path = ROOT / "ci/check_registry.yaml"
    if not path.is_file():
        return
    try:
        registry = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid CI registry: {exc}")
        return

    if registry.get("schema_version") != "0.1":
        errors.append("CI registry schema_version must be 0.1")
    checks = registry.get("checks")
    if not isinstance(checks, dict) or not checks:
        errors.append("CI registry checks must be a non-empty object")
        return

    for required_check in ("workflow-integrity", "full-governance"):
        if required_check not in checks:
            errors.append(f"CI registry missing required check: {required_check}")

    for check_id, check in sorted(checks.items()):
        if not isinstance(check, dict):
            errors.append(f"CI registry check must be an object: {check_id}")
            continue
        runner = check.get("runner")
        if runner not in {"python", "lean"}:
            errors.append(f"unsupported CI runner for {check_id}: {runner}")
        command = check.get("command")
        if not isinstance(command, str) or not command.strip():
            errors.append(f"missing CI command for {check_id}")
            continue
        patterns = check.get("paths")
        if not isinstance(patterns, list):
            errors.append(f"CI paths must be a list for {check_id}")
        for relation in ("depends_on", "supersedes"):
            values = check.get(relation, [])
            if not isinstance(values, list):
                errors.append(f"CI {relation} must be a list for {check_id}")
                continue
            for target in values:
                if target not in checks:
                    errors.append(f"CI {relation} target missing for {check_id}: {target}")

        if runner == "python":
            try:
                argv = shlex.split(command)
            except ValueError as exc:
                errors.append(f"invalid CI command for {check_id}: {exc}")
                continue
            if len(argv) >= 2 and argv[0].endswith("python3"):
                target = ROOT / argv[1]
                if not target.is_file():
                    errors.append(f"CI command target missing for {check_id}: {argv[1]}")


def main() -> int:
    errors: list[str] = []

    for relative in REQUIRED_FILES:
        if not (ROOT / relative).is_file():
            errors.append(f"missing required file: {relative}")

    for relative in FORBIDDEN_LEGACY_FILES:
        if (ROOT / relative).exists():
            errors.append(f"legacy file still present: {relative}")

    for relative, markers in REQUIRED_MARKERS.items():
        path = ROOT / relative
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                errors.append(f"missing marker in {relative}: {marker}")

    check_registry(errors)
    check_repository_workflow_references(errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    scope = "full" if os.environ.get("KUUOS_FULL_WORKFLOW_SCAN") == "1" else "selected"
    print(f"PASS: workflow consolidation integrity ({scope} reference scan)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
