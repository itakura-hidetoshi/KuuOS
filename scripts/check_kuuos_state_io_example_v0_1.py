#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_state_io_runner_v0_1 import run_state_io

RAW = ROOT / "examples" / "qi_state_io_v0_1" / "raw_state.json"
EVIDENCE = ROOT / "examples" / "qi_state_io_v0_1" / "evidence.json"

REQUIRED_OUTPUTS = [
    "kuuos_driver_result_v0_1.json",
    "next_raw_state_v0_1.json",
    "state_bundle_v0_1.json",
    "step_trace_v0_1.json",
    "run_manifest_v0_1.json",
]


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate_process_summary(summary, errors: list[str], label: str) -> None:
    required = [
        "process_tensor_visible",
        "transition_continuity_visible",
        "memory_continuity_visible",
        "nonmarkov_memory_visible",
        "process_history_length",
        "transition_support_count",
        "memory_support_count",
        "nonmarkov_support_count",
        "missing_process_requirements",
        "process_tensor_reason",
        "grants_execution_authority",
        "grants_truth_authority",
    ]
    if not isinstance(summary, dict):
        errors.append(f"{label}: summary is not an object")
        return
    for key in required:
        if key not in summary:
            errors.append(f"{label}: missing process summary key {key}")
    if summary.get("grants_execution_authority") is not False:
        errors.append(f"{label}: execution authority flag not false")
    if summary.get("grants_truth_authority") is not False:
        errors.append(f"{label}: truth authority flag not false")


def main() -> int:
    errors: list[str] = []
    if not RAW.is_file():
        errors.append(f"missing raw example: {RAW}")
    if not EVIDENCE.is_file():
        errors.append(f"missing evidence example: {EVIDENCE}")
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1

    with tempfile.TemporaryDirectory() as tmp:
        out = pathlib.Path(tmp) / "out"
        manifest = run_state_io(raw_state_path=RAW, evidence_path=EVIDENCE, output_dir=out, max_steps=2)

        for name in REQUIRED_OUTPUTS:
            if not (out / name).is_file():
                errors.append(f"missing output file: {name}")

        if not errors:
            result = load(out / "kuuos_driver_result_v0_1.json")
            next_state = load(out / "next_raw_state_v0_1.json")
            bundle = load(out / "state_bundle_v0_1.json")
            trace = load(out / "step_trace_v0_1.json")
            manifest_file = load(out / "run_manifest_v0_1.json")
            if manifest.stop_reason != "MAX_STEPS_REACHED":
                errors.append("manifest stop_reason mismatch")
            if manifest.steps_run != 2:
                errors.append("manifest steps_run mismatch")
            if manifest_file.get("steps_run") != 2:
                errors.append("manifest file steps_run mismatch")
            if result.get("steps_run") != 2:
                errors.append("driver result steps_run mismatch")
            if next_state.get("candidate_only") is not True:
                errors.append("next state candidate_only not preserved")
            if next_state.get("nonfinal_marker") is not True:
                errors.append("next state nonfinal marker not preserved")
            if len(trace) != 2:
                errors.append("step trace length mismatch")
            if len(bundle.get("loop_log", [])) != 2:
                errors.append("bundle loop log length mismatch")
            if trace:
                validate_process_summary(trace[0].get("qi_process_tensor_summary"), errors, "step_trace[0]")
            if bundle.get("loop_log"):
                validate_process_summary(bundle["loop_log"][0].get("qi_process_tensor_summary"), errors, "loop_log[0]")
            for flag in [
                "grants_execution_authority",
                "grants_truth_authority",
                "grants_final_commitment_authority",
                "grants_memory_overwrite_authority",
            ]:
                if bundle.get(flag) is not False:
                    errors.append(f"bundle authority flag not false: {flag}")

        if errors:
            for error in errors:
                print("ERROR:", error)
            return 1

    print("PASS: KuuOS State IO example check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
