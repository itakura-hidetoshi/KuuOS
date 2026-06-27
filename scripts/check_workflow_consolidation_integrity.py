#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
SELF = pathlib.Path(__file__).resolve()
DIRECT_WORKFLOW_PATTERN = re.compile(r"\.github/workflows/[A-Za-z0-9_./-]+\.ya?ml")
CONSTRUCTED_WORKFLOW_PATTERN = re.compile(
    r"ROOT\s*/\s*[\"']\.github[\"']\s*/\s*[\"']workflows[\"']\s*/\s*[\"']([^\"']+\.ya?ml)[\"']"
)

REQUIRED_FILES = [
    ".github/workflows/all_governance_validation.yml",
    ".github/workflows/decision-os-validation.yml",
    ".github/workflows/evidence-cycle-os-validation.yml",
    ".github/workflows/plan-os-validation.yml",
    "scripts/run_plan_os_full_checks.py",
    ".github/WORKFLOW_INDEX.md",
]

FORBIDDEN_LEGACY_FILES = [
    ".github/workflows/core_governance_validation.yml",
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
}


def workflow_references(text: str) -> set[str]:
    references = set(DIRECT_WORKFLOW_PATTERN.findall(text))
    references.update(
        f".github/workflows/{name}"
        for name in CONSTRUCTED_WORKFLOW_PATTERN.findall(text)
    )
    return references


def check_repository_workflow_references(errors: list[str]) -> None:
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.resolve() == SELF or ".git" in path.parts:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for workflow in sorted(workflow_references(text)):
            if not (ROOT / workflow).is_file():
                errors.append(
                    f"missing workflow reference: {path.relative_to(ROOT)} -> {workflow}"
                )


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

    check_repository_workflow_references(errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("PASS: workflow consolidation integrity")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
