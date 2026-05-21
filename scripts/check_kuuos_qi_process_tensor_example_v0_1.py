#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.qi_process_tensor_v0_1 import evaluate_qi_process_tensor
from runtime.qi_total_field_v0_1 import evaluate_qi_total_field
from runtime.kuuos_state_io_runner_v0_1 import run_state_io

RAW = ROOT / "examples" / "qi_process_tensor_v0_1" / "raw_state_process_history.json"
EVIDENCE = ROOT / "examples" / "qi_process_tensor_v0_1" / "evidence.json"


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


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

    raw = load(RAW)
    receipt = evaluate_qi_process_tensor(raw)
    if receipt.process_tensor_visible is not True:
        errors.append("process_tensor_visible was not derived")
    if receipt.transition_continuity_visible is not True:
        errors.append("transition continuity not derived")
    if receipt.memory_continuity_visible is not True:
        errors.append("memory continuity not derived")
    if receipt.nonmarkov_memory_visible is not True:
        errors.append("nonmarkov memory not derived")
    if receipt.process_tensor_reason != "process_tensor_support_visible":
        errors.append("unexpected process tensor reason")

    total = evaluate_qi_total_field(raw)
    if total.qi_cycle_decision.get("qi_signal") != "ALLOW_CANDIDATE":
        errors.append("Qi Total Field did not allow candidate")
    if "process_tensor_visible" not in total.source_support.get("process_qi", []):
        errors.append("process tensor support missing from total field source_support")
    if "nonmarkov_memory_visible" not in total.source_support.get("process_qi", []):
        errors.append("nonmarkov support missing from total field source_support")

    with tempfile.TemporaryDirectory() as tmp:
        out = pathlib.Path(tmp) / "out"
        manifest = run_state_io(raw_state_path=RAW, evidence_path=EVIDENCE, output_dir=out, max_steps=2)
        if manifest.stop_reason != "MAX_STEPS_REACHED":
            errors.append("state IO stop reason mismatch")
        result = load(out / "kuuos_driver_result_v0_1.json")
        trace = load(out / "step_trace_v0_1.json")
        if result.get("steps_run") != 2:
            errors.append("driver result steps_run mismatch")
        if len(trace) != 2:
            errors.append("step trace length mismatch")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1

    print("PASS: KuuOS Qi process tensor example check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
