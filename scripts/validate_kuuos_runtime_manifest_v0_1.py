#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifests" / "kuuos_runtime_manifest_v0_1.json"

LIST_KEYS = [
    "core_runtime_files",
    "core_test_files",
    "example_files",
    "script_files",
    "workflow_files",
    "policy_files",
]

NEEDED_KEYS = [
    "manifest_version",
    "runtime_status",
    "required_output_paths",
    "required_trace_fields",
    "authority_flags_must_be_false",
    "stop_reasons",
]

ALLOWED_RUNTIME_STATUS = {
    "bounded_non_authoritative_closed_loop",
    "bounded_non_authoritative_closed_loop_with_daemon",
    "bounded_non_authoritative_closed_loop_with_daemon_geometric_active_inference",
}

NEEDED_TRACE = [
    "qi_process_tensor_summary",
    "process_tensor_visible",
    "transition_continuity_visible",
    "memory_continuity_visible",
    "nonmarkov_memory_visible",
    "process_history_length",
    "process_tensor_reason",
]

NEEDED_OUTPUTS = [
    "kuuos_driver_result_v0_1.json",
    "next_raw_state_v0_1.json",
    "state_bundle_v0_1.json",
    "step_trace_v0_1.json",
    "run_manifest_v0_1.json",
]

DAEMON_OUTPUTS = [
    "daemon_tick_log_v0_1.json",
    "daemon_result_v0_1.json",
    "daemon_qi_process_tensor_tick_scheduler_v0_1.json",
    "daemon_qi_process_tensor_closed_loop_receipt_v0_1.json",
]

REQUIRED_POLICY_FILES = [
    "manifests/kuuos_validator_tiering_policy_v0_1.json",
]

REQUIRED_SCRIPT_FILES = [
    "scripts/validate_kuuos_validator_tiering_policy_v0_1.py",
]


def main() -> int:
    errors: list[str] = []
    if not MANIFEST.exists():
        print("ERROR: missing manifest")
        return 1
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    for key in NEEDED_KEYS + LIST_KEYS:
        if key not in data:
            errors.append(f"missing key: {key}")
    for key in LIST_KEYS:
        for rel in data.get(key, []):
            if not (ROOT / rel).exists():
                errors.append(f"missing path: {rel}")
    if data.get("manifest_version") != "kuuos_runtime_manifest_v0_1":
        errors.append("bad manifest_version")
    if data.get("runtime_status") not in ALLOWED_RUNTIME_STATUS:
        errors.append("bad runtime_status")
    for item in NEEDED_TRACE:
        if item not in data.get("required_trace_fields", []):
            errors.append(f"missing trace item: {item}")
    outputs = data.get("required_output_paths", [])
    for item in NEEDED_OUTPUTS:
        if item not in outputs:
            errors.append(f"missing output item: {item}")
    if data.get("runtime_status") in {"bounded_non_authoritative_closed_loop_with_daemon", "bounded_non_authoritative_closed_loop_with_daemon_geometric_active_inference"}:
        for item in DAEMON_OUTPUTS:
            if item not in outputs:
                errors.append(f"missing daemon output item: {item}")
    policy_files = data.get("policy_files", [])
    for item in REQUIRED_POLICY_FILES:
        if item not in policy_files:
            errors.append(f"missing policy file item: {item}")
    script_files = data.get("script_files", [])
    for item in REQUIRED_SCRIPT_FILES:
        if item not in script_files:
            errors.append(f"missing script file item: {item}")
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: KuuOS runtime manifest v0.1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
