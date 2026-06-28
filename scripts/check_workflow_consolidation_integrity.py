#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import pathlib
import re
import shlex

from select_impacted_checks import load_registry

ROOT = pathlib.Path(__file__).resolve().parents[1]
SELF = pathlib.Path(__file__).resolve()
DIRECT_WORKFLOW_PATTERN = re.compile(r"\.github/workflows/[A-Za-z0-9_./-]+\.ya?ml")
CONSTRUCTED_WORKFLOW_PATTERN = re.compile(
    r"ROOT\s*/\s*[\"']\.github[\"']\s*/\s*[\"']workflows[\"']\s*/\s*[\"']([^\"']+\.ya?ml)[\"']"
)

CANONICAL_FILES = [
    ".github/workflows/all_governance_validation.yml",
    ".github/workflows/all_governance_sharded_v0_2.yml",
    ".github/workflows/pr-governance-gate.yml",
    ".github/workflows/core_governance_validation.yml",
    ".github/workflows/kuuos_runtime_full_check.yml",
    ".github/workflows/lean-formal-validation.yml",
    ".github/workflows/decision-os-validation.yml",
    ".github/workflows/evidence-cycle-os-validation.yml",
    ".github/workflows/plan-os-validation.yml",
    ".github/workflows/regge_zero_governance_validation.yml",
    ".github/workflows/world-four-great-phase-dynamics-v0-59.yml",
    "scripts/run_plan_os_full_checks.py",
    "scripts/run_decision_os_full_checks.py",
    "scripts/run_evidence_cycle_os_full_checks.py",
    "scripts/run_all_governance_full_checks_v0_1.py",
    "scripts/run_all_governance_shard_v0_2.py",
    "scripts/run_full_governance_shard_ci_v0_2.py",
    "scripts/build_full_audit_selection_v0_2.py",
    "scripts/select_impacted_checks.py",
    "scripts/run_ci_check.py",
    "scripts/build_audit_summary.py",
    "tests/test_ci_audit_selector_v0_1.py",
    "tests/test_governance_sharding_v0_2.py",
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
    ".github/workflows/regge_zero_governance_validation.yml",
    ".github/workflows/kuuos_core_autonomy_validation.yml",
    ".github/workflows/belief-os-v0-1-validation.yml",
    ".github/workflows/kuuos_review_seal_validation.yml",
    *MANUAL_VERSION_WORKFLOWS,
]

REQUIRED_MARKERS = {
    ".github/workflows/all_governance_validation.yml": [
        "workflow_dispatch:",
        "uses: ./.github/workflows/all_governance_sharded_v0_2.yml",
    ],
    ".github/workflows/all_governance_sharded_v0_2.yml": [
        "workflow_call:",
        "max-parallel: 4",
        "index: [0, 1, 2, 3, 4, 5, 6, 7]",
        "scripts/run_full_governance_shard_ci_v0_2.py",
        "scripts/build_full_audit_selection_v0_2.py",
        "scripts/build_audit_summary.py",
    ],
    ".github/workflows/pr-governance-gate.yml": [
        "pull_request:",
        "scripts/select_impacted_checks.py",
        "max-parallel: 4",
        "scripts/run_ci_check.py",
        "scripts/build_audit_summary.py",
    ],
    ".github/workflows/regge_zero_governance_validation.yml": [
        "workflow_dispatch:",
        "branches: [main]",
        "scripts/run_regge_zero_governance_checks_v0_1.py",
        "cancel-in-progress: false",
    ],
    "scripts/run_all_governance_full_checks_v0_1.py": [
        "COMMANDS:",
        "for cmd in COMMANDS:",
        "failures.append((cmd, code))",
    ],
    "scripts/run_all_governance_shard_v0_2.py": [
        "partition_commands",
        "failed_commands",
        "sharding != authority expansion",
    ],
    "tests/test_governance_sharding_v0_2.py": [
        "test_every_command_is_assigned_exactly_once",
        "test_partition_is_deterministic",
    ],
    "ci/check_registry.yaml": [
        "\"schema_version\": \"0.2\"",
        "python-sharded",
        "shard_count",
        "sharding != authority expansion",
        "regge-zero",
    ],
}


def workflow_references(text: str) -> set[str]:
    refs = set(DIRECT_WORKFLOW_PATTERN.findall(text))
    refs.update(
        f".github/workflows/{name}" for name in CONSTRUCTED_WORKFLOW_PATTERN.findall(text)
    )
    return refs


def all_repository_files() -> list[pathlib.Path]:
    return [
        path for path in sorted(ROOT.rglob("*"))
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
    candidates = {ROOT / relative for relative in CANONICAL_FILES + MANUAL_VERSION_WORKFLOWS}
    candidates.update(ROOT / relative for relative in selection.get("changed_paths", []))
    return [path for path in sorted(candidates) if path.is_file()]


def check_workflow_references(errors: list[str]) -> None:
    for path in selected_reference_files():
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for workflow in sorted(workflow_references(text)):
            if not (ROOT / workflow).is_file():
                errors.append(f"missing workflow reference: {path.relative_to(ROOT)} -> {workflow}")


def check_registry(errors: list[str]) -> None:
    path = ROOT / "ci/check_registry.yaml"
    try:
        registry = load_registry(path)
    except ValueError as exc:
        errors.append(f"invalid merged CI registry: {exc}")
        return
    checks = registry.get("checks")
    if not isinstance(checks, dict) or not checks:
        errors.append("CI registry checks must be a non-empty object")
        return
    for required in (
        "workflow-integrity",
        "ci-audit-tests",
        "governance-shard-tests",
        "regge-zero",
        "full-governance",
        "core-autonomy-v01",
        "belief-os-v01",
        "review-seal-v01",
        "pr-entry-batch3-tests",
    ):
        if required not in checks:
            errors.append(f"CI registry missing required check: {required}")

    for check_id, check in sorted(checks.items()):
        if not isinstance(check, dict):
            errors.append(f"CI registry check must be an object: {check_id}")
            continue
        runner = check.get("runner")
        if runner not in {"python", "python-sharded", "lean"}:
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
        if runner == "python-sharded":
            count = check.get("shard_count")
            if not isinstance(count, int) or count <= 0:
                errors.append(f"positive shard_count required for {check_id}")
            if "{index}" not in command or "{count}" not in command:
                errors.append(f"sharded command template invalid for {check_id}")
        if runner in {"python", "python-sharded"}:
            try:
                argv = shlex.split(command.format(index=0, count=1))
            except (ValueError, KeyError) as exc:
                errors.append(f"invalid CI command for {check_id}: {exc}")
                continue
            if len(argv) >= 2 and argv[0].endswith("python3") and not (ROOT / argv[1]).is_file():
                errors.append(f"CI command target missing for {check_id}: {argv[1]}")


def main() -> int:
    errors: list[str] = []
    for relative in CANONICAL_FILES + MANUAL_VERSION_WORKFLOWS:
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
    check_workflow_references(errors)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    scope = "full" if os.environ.get("KUUOS_FULL_WORKFLOW_SCAN") == "1" else "selected"
    print(f"PASS: workflow consolidation integrity ({scope} reference scan)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
