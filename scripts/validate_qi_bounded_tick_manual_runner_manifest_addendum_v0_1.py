#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
ADDENDUM = ROOT / "manifests" / "kuuos_qi_bounded_tick_manual_runner_manifest_addendum_v0_1.json"

REQUIRED_SCRIPT = "scripts/run_qi_process_tensor_bounded_tick_from_daemon_v0_1.py"
REQUIRED_CHECKER = "scripts/check_qi_bounded_tick_manual_runner_example_v0_1.py"
REQUIRED_CASE_CHECKER = "scripts/check_qi_bounded_tick_executor_receipt_contract_cases_v0_1.py"
REQUIRED_RECEIPT_VALIDATOR = "scripts/validate_qi_bounded_tick_executor_receipt_v0_1.py"
REQUIRED_VALIDATOR = "scripts/validate_qi_bounded_tick_manual_runner_manifest_addendum_v0_1.py"
REQUIRED_TEST = "tests/test_qi_process_tensor_bounded_tick_manual_runner_v0_1.py"
REQUIRED_RECEIPT_VALIDATOR_TEST = "tests/test_qi_bounded_tick_executor_receipt_validator_v0_1.py"
REQUIRED_WORKFLOW = ".github/workflows/qi_bounded_tick_manual_runner_example_validation.yml"
REQUIRED_RECEIPT_WORKFLOW = ".github/workflows/qi_bounded_tick_executor_receipt_contract_validation.yml"
REQUIRED_OUTPUT = "daemon_qi_process_tensor_bounded_tick_executor_receipt_v0_1.json"
REQUIRED_CASE_MANIFEST = "validation/qi_bounded_tick_executor_receipt_contract_v0_1/cases_manifest.json"
REQUIRED_INPUTS = {
    "daemon_qi_process_tensor_reentry_license_gate_v0_1.json",
    "daemon_qi_process_tensor_bounded_tick_invocation_boundary_v0_1.json",
}
REQUIRED_EXAMPLES = {
    "examples/qi_bounded_tick_manual_runner_v0_1/raw_state.json",
    "examples/qi_bounded_tick_manual_runner_v0_1/evidence.json",
    "examples/qi_bounded_tick_manual_runner_v0_1/daemon/daemon_qi_process_tensor_reentry_license_gate_v0_1.json",
    "examples/qi_bounded_tick_manual_runner_v0_1/daemon/daemon_qi_process_tensor_bounded_tick_invocation_boundary_v0_1.json",
    "examples/qi_bounded_tick_manual_runner_v0_1/README.md",
}
REQUIRED_CASE_FILES = {
    "validation/qi_bounded_tick_executor_receipt_contract_v0_1/valid_invoked_receipt.json",
    "validation/qi_bounded_tick_executor_receipt_contract_v0_1/valid_denied_receipt.json",
    "validation/qi_bounded_tick_executor_receipt_contract_v0_1/invalid_invoked_missing_token.json",
    "validation/qi_bounded_tick_executor_receipt_contract_v0_1/invalid_denied_grants_execution.json",
    "validation/qi_bounded_tick_executor_receipt_contract_v0_1/invalid_truth_authority.json",
    "validation/qi_bounded_tick_executor_receipt_contract_v0_1/invalid_unbounded_max_steps.json",
}


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def main() -> int:
    errors: list[str] = []
    if not ADDENDUM.exists():
        print("ERROR: missing Qi bounded tick manual runner addendum")
        return 1
    data = json.loads(ADDENDUM.read_text(encoding="utf-8"))
    if data.get("addendum_version") != "kuuos_qi_bounded_tick_manual_runner_manifest_addendum_v0_1":
        errors.append("bad addendum_version")
    if data.get("addendum_status") != "active_manifest_addendum":
        errors.append("bad addendum_status")
    if data.get("parent_manifest") != "manifests/kuuos_runtime_manifest_v0_1.json":
        errors.append("bad parent_manifest")

    scripts = set(_as_list(data.get("script_files")))
    tests = set(_as_list(data.get("test_files")))
    examples = set(_as_list(data.get("example_files")))
    workflows = set(_as_list(data.get("workflow_files")))
    inputs = set(_as_list(data.get("input_receipts")))
    outputs = set(_as_list(data.get("output_receipts")))
    modules = set(_as_list(data.get("runtime_full_check_modules")))
    receipt_validators = set(_as_list(data.get("receipt_contract_validators")))
    case_files = set(_as_list(data.get("receipt_contract_case_files")))

    for item, label in [
        (REQUIRED_SCRIPT, "manual runner script"),
        (REQUIRED_CHECKER, "manual runner example checker"),
        (REQUIRED_CASE_CHECKER, "receipt contract case checker"),
        (REQUIRED_RECEIPT_VALIDATOR, "bounded tick executor receipt validator"),
        (REQUIRED_VALIDATOR, "manual runner addendum validator"),
    ]:
        if item not in scripts:
            errors.append(f"{label} not registered")
    for item, label in [
        (REQUIRED_TEST, "manual runner test"),
        (REQUIRED_RECEIPT_VALIDATOR_TEST, "receipt validator test"),
    ]:
        if item not in tests:
            errors.append(f"{label} not registered")
    if REQUIRED_RECEIPT_VALIDATOR not in receipt_validators:
        errors.append("receipt contract validator not registered")
    if data.get("receipt_contract_case_manifest") != REQUIRED_CASE_MANIFEST:
        errors.append("receipt contract case manifest not registered")
    for item in REQUIRED_CASE_FILES - case_files:
        errors.append(f"missing receipt contract case file: {item}")
    for item, label in [
        (REQUIRED_WORKFLOW, "manual runner example workflow"),
        (REQUIRED_RECEIPT_WORKFLOW, "receipt contract workflow"),
    ]:
        if item not in workflows:
            errors.append(f"{label} not registered")
    if REQUIRED_OUTPUT not in outputs:
        errors.append("executor receipt output not registered")
    for item in REQUIRED_INPUTS - inputs:
        errors.append(f"missing input receipt: {item}")
    for item in REQUIRED_EXAMPLES - examples:
        errors.append(f"missing example file: {item}")
    for module in [
        "tests.test_qi_process_tensor_bounded_tick_manual_runner_v0_1",
        "tests.test_qi_bounded_tick_executor_receipt_validator_v0_1",
        "scripts.check_qi_bounded_tick_executor_receipt_contract_cases_v0_1",
        "scripts.check_qi_bounded_tick_manual_runner_example_v0_1",
    ]:
        if module not in modules:
            errors.append(f"runtime full check module not registered: {module}")

    for rel in [
        REQUIRED_SCRIPT,
        REQUIRED_CHECKER,
        REQUIRED_CASE_CHECKER,
        REQUIRED_RECEIPT_VALIDATOR,
        REQUIRED_VALIDATOR,
        REQUIRED_TEST,
        REQUIRED_RECEIPT_VALIDATOR_TEST,
        REQUIRED_WORKFLOW,
        REQUIRED_RECEIPT_WORKFLOW,
        REQUIRED_CASE_MANIFEST,
        *sorted(REQUIRED_CASE_FILES),
        *sorted(REQUIRED_EXAMPLES),
    ]:
        if not (ROOT / rel).exists():
            errors.append(f"registered path missing: {rel}")

    boundary = data.get("execution_boundary") or {}
    if boundary.get("daemon_auto_invocation_allowed") is not False:
        errors.append("daemon_auto_invocation_allowed must be false")
    if boundary.get("manual_invocation_required") is not True:
        errors.append("manual_invocation_required must be true")
    if boundary.get("requires_single_tick_invocation_token") is not True:
        errors.append("requires_single_tick_invocation_token must be true")
    if boundary.get("max_invocation_depth") != 0:
        errors.append("max_invocation_depth must be 0")
    if boundary.get("executor_invokes_at_most_one_state_io_tick") is not True:
        errors.append("executor must be at most one State IO tick")

    authority = data.get("authority_boundary") or {}
    if authority.get("manual_runner_may_open_bounded_tick_execution") is not True:
        errors.append("manual runner bounded tick execution authority not declared")
    for key in [
        "grants_truth_authority",
        "grants_final_commitment_authority",
        "grants_memory_overwrite_authority",
        "grants_clinical_authority",
        "grants_theorem_authority",
        "grants_completed_identity_authority",
    ]:
        if authority.get(key) is not False:
            errors.append(f"{key} must remain false")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi bounded tick manual runner manifest addendum v0.1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
