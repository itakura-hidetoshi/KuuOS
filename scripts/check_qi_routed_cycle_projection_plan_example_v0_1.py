#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_runtime_daemon_qi_routed_cycle_projection_plan_runner_v0_1 import run_qi_routed_cycle_projection_plan

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

    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        daemon_dir = root / "daemon"
        dispatch_dir = root / "dispatch"
        result = run_qi_routed_cycle_projection_plan(
            raw_state_path=RAW,
            evidence_path=EVIDENCE,
            daemon_dir=daemon_dir,
            dispatch_dir=dispatch_dir,
            max_daemon_ticks=1,
            max_steps_per_tick=1,
            sleep_seconds=0.0,
            requested_max_reentry_cycles=1,
        )
        required_files = [
            result.routed_cycle_result_path,
            result.projection_plan_bridge_result_path,
            result.qi_routed_cycle_operational_summary_path,
            result.qi_next_runtime_mode_plan_path,
        ]
        for item in required_files:
            if not pathlib.Path(item).is_file():
                errors.append(f"missing output file: {item}")
        for key in ["recoverability", "health", "observation_debt", "trace_compaction"]:
            if key not in result.projection_statuses:
                errors.append(f"missing projection status: {key}")
        if not isinstance(result.required_pre_tick_actions, list):
            errors.append("required_pre_tick_actions is not a list")
        if result.runner_status != "QI_ROUTED_CYCLE_PROJECTION_PLAN_COMPILED":
            errors.append("runner status mismatch")
        if result.bridge_only is not True:
            errors.append("bridge_only flag mismatch")
        if result.read_only is not True:
            errors.append("read_only flag mismatch")
        if result.plan_only is not True:
            errors.append("plan_only flag mismatch")
        if result.grants_execution_authority is not False:
            errors.append("execution flag not false")
        if result.grants_next_tick_execution_authority is not False:
            errors.append("next tick flag not false")

        if not errors:
            summary = load(pathlib.Path(result.qi_routed_cycle_operational_summary_path))
            plan = load(pathlib.Path(result.qi_next_runtime_mode_plan_path))
            if summary.get("recommended_next_runtime_mode") != result.recommended_next_runtime_mode:
                errors.append("summary mode mismatch")
            if plan.get("next_tick_preparation") != result.next_tick_preparation:
                errors.append("plan preparation mismatch")
            if plan.get("required_pre_tick_actions") != result.required_pre_tick_actions:
                errors.append("plan actions mismatch")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi routed cycle projection plan example check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
