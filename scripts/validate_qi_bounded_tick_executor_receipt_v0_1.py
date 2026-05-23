#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import pathlib
from typing import Any

VALID_STATUSES = {
    "QI_PROCESS_TENSOR_BOUNDED_TICK_INVOKED",
    "QI_PROCESS_TENSOR_BOUNDED_TICK_NOT_INVOKED",
}

FALSE_AUTHORITY_FLAGS = [
    "grants_truth_authority",
    "grants_final_commitment_authority",
    "grants_memory_overwrite_authority",
    "grants_clinical_authority",
    "grants_theorem_authority",
    "grants_completed_identity_authority",
]

REQUIRED_FIELDS = [
    "executor_version",
    "executor_status",
    "source_gate_status",
    "source_license_decision",
    "source_boundary_status",
    "source_invocation_decision",
    "bounded_tick_license",
    "single_tick_invocation_token",
    "tick_invoked",
    "grants_execution_authority",
]


def _load_json(path: pathlib.Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("receipt is not a JSON object")
    return data


def validate_receipt(data: dict[str, Any], *, require_paths_exist: bool = False, base_dir: pathlib.Path | None = None) -> list[str]:
    errors: list[str] = []
    for field in REQUIRED_FIELDS:
        if field not in data:
            errors.append(f"missing field: {field}")

    if data.get("executor_version") != "kuuos_runtime_daemon_qi_process_tensor_bounded_tick_executor_v0_1":
        errors.append("bad executor_version")
    status = data.get("executor_status")
    if status not in VALID_STATUSES:
        errors.append("bad executor_status")

    for flag in FALSE_AUTHORITY_FLAGS:
        if data.get(flag) is not False:
            errors.append(f"{flag} must be false")

    tick_invoked = data.get("tick_invoked") is True
    token = data.get("single_tick_invocation_token") is True
    execution_authority = data.get("grants_execution_authority") is True

    if status == "QI_PROCESS_TENSOR_BOUNDED_TICK_INVOKED":
        if not tick_invoked:
            errors.append("invoked receipt must set tick_invoked true")
        if not token:
            errors.append("invoked receipt must have single_tick_invocation_token true")
        if data.get("source_invocation_decision") != "SINGLE_TICK_INVOCATION_TOKEN_GRANTED":
            errors.append("invoked receipt must cite SINGLE_TICK_INVOCATION_TOKEN_GRANTED")
        if data.get("denied_reason") is not None:
            errors.append("invoked receipt must not have denied_reason")
        if not execution_authority:
            errors.append("invoked receipt must open bounded execution authority")
        steps_run = data.get("steps_run")
        if not isinstance(steps_run, int) or steps_run < 0:
            errors.append("invoked receipt steps_run must be a nonnegative integer")
        max_steps = data.get("licensed_max_steps_per_tick")
        if not isinstance(max_steps, int) or not (1 <= max_steps <= 25):
            errors.append("licensed_max_steps_per_tick must be in 1..25 for invoked receipt")
        for field in [
            "run_manifest_path",
            "next_raw_state_path",
            "state_bundle_path",
            "step_trace_path",
        ]:
            if not data.get(field):
                errors.append(f"invoked receipt missing output path: {field}")
    elif status == "QI_PROCESS_TENSOR_BOUNDED_TICK_NOT_INVOKED":
        if tick_invoked:
            errors.append("denial receipt must set tick_invoked false")
        if execution_authority:
            errors.append("denial receipt must not grant execution authority")
        if data.get("steps_run") != 0:
            errors.append("denial receipt steps_run must be 0")
        if data.get("denied_reason") in (None, ""):
            errors.append("denial receipt must include denied_reason")
        if data.get("run_manifest_path") is not None:
            errors.append("denial receipt must not have run_manifest_path")

    if require_paths_exist:
        root = base_dir or pathlib.Path.cwd()
        for field in ["run_manifest_path", "next_raw_state_path", "state_bundle_path", "step_trace_path"]:
            value = data.get(field)
            if value:
                path = pathlib.Path(value)
                if not path.is_absolute():
                    path = root / path
                if not path.exists():
                    errors.append(f"output path missing on disk: {field}={value}")

    return errors


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate Qi bounded tick executor receipt v0.1")
    parser.add_argument("--receipt", type=pathlib.Path, required=True)
    parser.add_argument("--require-paths-exist", action="store_true")
    parser.add_argument("--base-dir", type=pathlib.Path, default=None)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    receipt = _load_json(args.receipt)
    errors = validate_receipt(
        receipt,
        require_paths_exist=args.require_paths_exist,
        base_dir=args.base_dir,
    )
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi bounded tick executor receipt v0.1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
