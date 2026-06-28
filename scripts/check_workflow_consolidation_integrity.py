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

CANONICAL_FILES = [
    ".github/workflows/all_governance_validation.yml",
    ".github/workflows/pr-governance-gate.yml",
    ".github/workflows/core_governance_validation.yml",
    ".github/workflows/kuuos_runtime_full_check.yml",
    ".github/workflows/lean-formal-validation.yml",
    ".github/workflows/decision-os-validation.yml",
    ".github/workflows/evidence-cycle-os-validation.yml",
    ".github/workflows/plan-os-validation.yml",
    ".github/workflows/world-four-great-phase-dynamics-v0-59.yml",
    "scripts/run_plan_os_full_checks.py",
    "scripts/run_decision_os_full_checks.py",
    "scripts/run_evidence_cycle_os_full_checks.py",
    "scripts/select_impacted_checks.py",
    "scripts/run_ci_check.py",
    "scripts/build_audit_summary.py",
    "tests/test_ci_audit_selector_v0_1.py",
    "ci/check_registry.yaml",
    ".github/WORKFLOW_INDEX.md",
]

MANUAL_VERSION_WORKFLOWS = [
    ".github/workflows/kuuos-connection-improvement-candidate-v0-62.yml",
    ".github/workflows/kuuos-connection-review-v0-63.yml",
    ".github/workflows/kuuos-connection-evaluation-v0-64.yml",
    ".github/workflows/kuuos-staging-v065.yml",
    ".github/workflows/kuuos-shadow-v066.yml",
    ".github/workflows/kuuos-finite-gauge-v067.yml",
    ".github/workflows/kuuos-evidence-v068.yml",
    ".github/workflows/kuuos-external-evidence-review-v069.yml",
    ".github/workflows/kuuos-module-bundle-v070.yml",
    ".github/workflows/kuuos-noncommutative-leibniz-v071.yml",
    ".github/workflows/kuuos-memory-v072.yml",
    ".github/workflows/kuuos-memory-evaluation-v073.yml",
    ".github/workflows/kuuos-memory-review-v074.yml",
    ".github/workflows/kuuos-v075.yml",
    ".github/workflows/kuuos-v076.yml",
]

REQUIRED_FILES = CANONICAL_FILES + MANUAL_VERSION_WORKFLOWS

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

MIGRATED_PR_ENTRY_POINTS = [
    ".github/workflows/all_governance_validation.yml",
    ".github/workflows/core_governance_validation.yml",
    ".github/workflows/kuuos_runtime_full_check.yml",
    ".github/workflows/lean-formal-validation.yml",
    ".github/workflows/decision-os-validation.yml",
    ".github/workflows/evidence-cycle-os-validation.yml",
    ".github/workflows/plan-os-validation.yml",
    *MANUAL_VERSION_WORKFLOWS,
]

REQUIRED_MARKERS = {
    ".github/workflows/all_governance_validation.yml": [
        "workflow_dispatch:",
        "- main",
        "KUUOS_FULL_WORKFLOW_SCAN: '1'",
        "scripts/run_all_governance_full_checks_v0_1.py",
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
        "scripts/run_core_governance_full_checks_v0_1.py",
    ],
    ".github/workflows/kuuos_runtime_full_check.yml": [
        "workflow_dispatch:",
        "- main",
        "scripts/run_kuuos_runtime_full_check_v0_55.py",
    ],
    ".github/workflows/lean-formal-validation.yml": [
        "workflow_dispatch:",
        "- main",
        "sorryAsError=true",
    ],
    ".github/workflows/decision-os-validation.yml": [
        "workflow_dispatch:",
        "- main",
        "scripts/run_decision_os_full_checks.py",
    ],
    ".github/workflows/evidence-cycle-os-validation.yml": [
        "workflow_dispatch:",
        "- main",
        "scripts/run_evidence_cycle_os_full_checks.py",
    ],
    ".github/workflows/plan-os-validation.yml": [
        "workflow_dispatch:",
        "- main",
        "scripts/run_plan_os_full_checks.py",
    ],
    "scripts/run_plan_os_full_checks.py": [
        "check_plan_os_closed_loop_replan_intake_adapter_v0_4.py",
        "check_plan_os_generational_replan_cycle_driver_v0_5.py",
        "check_planos_activation_admission_actos_handoff_v0_23.py",
        "PASS: PlanOS v0.1-v0.23 validation completed",
    ],
    "scripts/run_decision_os_full_checks.py": [
        "runtime.v01_decision_os_relational_deliberation",
        "check_decisionos_admissible_candidate_selection_v0_4.py",
        "PASS: DecisionOS v0.1-v0.4 validation completed",
    ],
    "scripts/run_evidence_cycle_os_full_checks.py": [
        "runtime.v01_act_os_authority_bound_invocation",
        "check_observeos_world_host_effect_observation_v0_4.py",
        "PASS: Evidence Cycle OS validation completed",
    ],
    "ci/check_registry.yaml": [
        "selection optimization != authority expansion",
        "unknown_impact",
        "unmapped_impact",
        "pr_supersedes",
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

    for required_check in ("workflow-integrity", "ci-audit-tests", "full-governance"):
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
        if not isinstance(check.get("paths"), list):
            errors.append(f"CI paths must be a list for {check_id}")
        for relation in ("depends_on", "supersedes", "pr_supersedes"):
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

    for relative in MIGRATED_PR_ENTRY_POINTS:
        path = ROOT / relative
        if path.is_file() and "pull_request:" in path.read_text(encoding="utf-8"):
            errors.append(f"migrated workflow still has pull_request trigger: {relative}")

    for relative in MANUAL_VERSION_WORKFLOWS:
        path = ROOT / relative
        if path.is_file() and "workflow_dispatch:" not in path.read_text(encoding="utf-8"):
            errors.append(f"manual workflow lost workflow_dispatch trigger: {relative}")

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
