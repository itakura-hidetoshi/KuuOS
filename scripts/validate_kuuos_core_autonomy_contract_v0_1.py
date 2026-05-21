#!/usr/bin/env python3
"""Validate the KuuOS core autonomy v0.1 minimal runtime surface."""

from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "specs" / "kuuos_core_autonomy_contract_v0_1.json"
RUNNER = ROOT / "scripts" / "run_kuuos_core_autonomy_v0_1.py"

REQUIRED_TOP_LEVEL = {
    "contract_id": "kuuos_core_autonomy_contract_v0_1",
    "version": "v0.1",
    "status": "CORE_AUTONOMY_MINIMAL_BASELINE",
    "repository": "itakura-hidetoshi/KuuOS",
    "runtime_entrypoint": "scripts/run_kuuos_core_autonomy_v0_1.py",
}

REQUIRED_PHASES = ["sense", "validate", "decide", "audit"]
REQUIRED_MODES = ["contract-check", "once", "daemon"]
REQUIRED_STATES = ["PASS", "HOLD", "REPAIR", "REJECT", "QUARANTINE"]
REQUIRED_FILES = [
    "README.md",
    "Makefile",
    "scripts/run_core_governance_full_checks_v0_1.py",
    "scripts/run_kuuos_core_autonomy_v0_1.py",
    "scripts/validate_kuuos_core_autonomy_contract_v0_1.py",
    "specs/kuuos_core_autonomy_contract_v0_1.json",
]
REQUIRED_FALSE_BOUNDARY = [
    "grants_execution_authority",
    "grants_clinical_authority",
    "grants_diagnosis_authority",
    "grants_treatment_authority",
    "grants_prescription_authority",
    "grants_triage_authority",
    "grants_theorem_authority",
    "grants_truth_authority",
    "grants_memory_overwrite_authority",
    "grants_governance_bypass_authority",
    "uses_external_services",
]
REQUIRED_TRUE_BOUNDARY = [
    "validation_only",
    "candidate_only",
    "local_runtime_only",
    "audit_receipt_only",
]
FORBIDDEN_MARKERS = [
    "grants execution authority",
    "grants clinical authority",
    "grants treatment authority",
    "grants diagnosis authority",
    "grants theorem truth",
    "permits governance bypass",
]


def load_contract() -> dict[str, Any]:
    with CONTRACT.open("r", encoding="utf-8") as f:
        return json.load(f)


def validate_contract_shape(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for key, expected in REQUIRED_TOP_LEVEL.items():
        if data.get(key) != expected:
            errors.append(f"{key} expected {expected!r}, got {data.get(key)!r}")

    for phase in REQUIRED_PHASES:
        if phase not in data.get("cycle_phases", []):
            errors.append(f"missing cycle phase: {phase}")
    for mode in REQUIRED_MODES:
        if mode not in data.get("operation_modes", []):
            errors.append(f"missing operation mode: {mode}")
    for state in REQUIRED_STATES:
        if state not in data.get("decision_states", []):
            errors.append(f"missing decision state: {state}")

    default_policy = data.get("default_policy", {})
    if default_policy.get("fail_closed") is not True:
        errors.append("default_policy.fail_closed must be true")
    if default_policy.get("audit_hash_chain_required") is not True:
        errors.append("default_policy.audit_hash_chain_required must be true")
    if default_policy.get("external_api_calls_allowed") is not False:
        errors.append("default_policy.external_api_calls_allowed must be false")
    if default_policy.get("network_required") is not False:
        errors.append("default_policy.network_required must be false")
    if default_policy.get("stdlib_only") is not True:
        errors.append("default_policy.stdlib_only must be true")

    boundary = data.get("authority_boundary", {})
    for key in REQUIRED_TRUE_BOUNDARY:
        if boundary.get(key) is not True:
            errors.append(f"authority_boundary.{key} must be true")
    for key in REQUIRED_FALSE_BOUNDARY:
        if boundary.get(key) is not False:
            errors.append(f"authority_boundary.{key} must be false")

    audit_schema = data.get("audit_event_schema", {})
    if audit_schema.get("schema") != "kuuos_core_autonomy_audit_event_v0_1":
        errors.append("unexpected audit schema")
    for field in [
        "schema",
        "timestamp_utc",
        "cycle_id",
        "contract_id",
        "runtime_mode",
        "phase_results",
        "decision_state",
        "safety_stop",
        "previous_event_hash",
        "event_hash",
    ]:
        if field not in audit_schema.get("required_fields", []):
            errors.append(f"missing audit required field: {field}")

    for path in REQUIRED_FILES:
        if not (ROOT / path).is_file():
            errors.append(f"missing repository file: {path}")

    text = CONTRACT.read_text(encoding="utf-8")
    for marker in FORBIDDEN_MARKERS:
        if marker in text and marker not in " ".join(data.get("forbidden_interpretations", [])):
            errors.append(f"forbidden marker outside explicit forbidden_interpretations: {marker}")

    return errors


def validate_runner_fast_path() -> list[str]:
    errors: list[str] = []
    if not RUNNER.is_file():
        return ["missing runner"]

    with tempfile.TemporaryDirectory() as tmp:
        audit_log = pathlib.Path(tmp) / "audit.jsonl"
        cmd = [
            sys.executable,
            str(RUNNER.relative_to(ROOT)),
            "--mode",
            "once",
            "--self-test-check",
            "--audit-log",
            str(audit_log),
            "--timeout-seconds",
            "30",
        ]
        completed = subprocess.run(
            cmd,
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=60,
        )
        if completed.returncode != 0:
            errors.append(f"runner self-test returned {completed.returncode}: {completed.stdout[-1000:]}")
            return errors
        if not audit_log.is_file():
            errors.append("runner did not create audit log")
            return errors
        lines = [line for line in audit_log.read_text(encoding="utf-8").splitlines() if line.strip()]
        if len(lines) != 1:
            errors.append(f"expected one audit line, got {len(lines)}")
            return errors
        event = json.loads(lines[0])
        if event.get("schema") != "kuuos_core_autonomy_audit_event_v0_1":
            errors.append("unexpected runner audit schema")
        if event.get("decision_state") != "PASS":
            errors.append("runner self-test did not PASS")
        if event.get("safety_stop") is not False:
            errors.append("runner self-test safety_stop must be false")
        if not isinstance(event.get("event_hash"), str) or len(event["event_hash"]) != 64:
            errors.append("runner audit event_hash must be sha256 hex")

    return errors


def main() -> int:
    errors: list[str] = []
    if not CONTRACT.is_file():
        print(f"ERROR: missing contract: {CONTRACT.relative_to(ROOT)}")
        return 1
    data = load_contract()
    errors.extend(validate_contract_shape(data))
    errors.extend(validate_runner_fast_path())

    if errors:
        for err in errors:
            print("ERROR:", err)
        return 1

    print("PASS: KuuOS core autonomy contract v0.1 validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
