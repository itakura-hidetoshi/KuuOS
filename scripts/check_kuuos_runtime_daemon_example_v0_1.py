#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_runtime_daemon_v0_1 import run_runtime_daemon

RAW = ROOT / "examples" / "qi_process_tensor_v0_1" / "raw_state_process_history.json"
EVIDENCE = ROOT / "examples" / "qi_process_tensor_v0_1" / "evidence.json"


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate_tick_entry(entry: dict, errors: list[str], label: str) -> None:
    required = [
        "tick_index",
        "output_dir",
        "run_status",
        "stop_reason",
        "steps_run",
        "next_raw_state_path",
        "state_bundle_path",
        "step_trace_path",
        "grants_execution_authority",
        "grants_truth_authority",
    ]
    for key in required:
        if key not in entry:
            errors.append(f"{label}: missing {key}")
    for key in ["next_raw_state_path", "state_bundle_path", "step_trace_path"]:
        if key in entry and not pathlib.Path(entry[key]).is_file():
            errors.append(f"{label}: missing file {key}")
    if entry.get("grants_execution_authority") is not False:
        errors.append(f"{label}: execution flag not false")
    if entry.get("grants_truth_authority") is not False:
        errors.append(f"{label}: truth flag not false")


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
        result = run_runtime_daemon(
            raw_state_path=RAW,
            evidence_path=EVIDENCE,
            daemon_dir=daemon_dir,
            max_ticks=2,
            max_steps_per_tick=1,
            sleep_seconds=0.0,
        )
        if result.daemon_status != "DAEMON_MAX_TICKS_REACHED_APPEND_ONLY":
            errors.append("daemon status mismatch")
        if result.stop_reason != "MAX_TICKS_REACHED":
            errors.append("stop reason mismatch")
        if result.ticks_run != 2:
            errors.append("ticks_run mismatch")
        if result.yinyang_polarity_state != "RECOVERY_YANG_PRESENT":
            errors.append("yinyang polarity mismatch")
        if result.four_image_phase != "LESSER_YANG":
            errors.append("four image phase mismatch")
        if result.qi_policy_recommended_tick_mode != "CONTINUE_WITH_QI_MEMORY_MONITOR":
            errors.append("qi policy mode mismatch")
        if result.emptiness_recommended_action != "CONTINUE_ADVISORY_ONLY":
            errors.append("emptiness action mismatch")
        if not pathlib.Path(result.tick_log_path).is_file():
            errors.append("missing tick log")
        if not pathlib.Path(result.final_raw_state_path).is_file():
            errors.append("missing final raw state")
        if not pathlib.Path(result.final_state_bundle_path).is_file():
            errors.append("missing final state bundle")
        if not result.yinyang_polarity_result_path or not pathlib.Path(result.yinyang_polarity_result_path).is_file():
            errors.append("missing yinyang polarity result")
        if not result.four_image_phase_result_path or not pathlib.Path(result.four_image_phase_result_path).is_file():
            errors.append("missing four image phase result")
        if not result.qi_policy_result_path or not pathlib.Path(result.qi_policy_result_path).is_file():
            errors.append("missing qi policy result")
        if not result.emptiness_gate_result_path or not pathlib.Path(result.emptiness_gate_result_path).is_file():
            errors.append("missing emptiness gate result")
        if not (daemon_dir / "daemon_result_v0_1.json").is_file():
            errors.append("missing daemon result")

        if not errors:
            tick_log = load(pathlib.Path(result.tick_log_path))
            daemon_result = load(daemon_dir / "daemon_result_v0_1.json")
            yy_result = load(pathlib.Path(result.yinyang_polarity_result_path))
            four_result = load(pathlib.Path(result.four_image_phase_result_path))
            policy_result = load(pathlib.Path(result.qi_policy_result_path))
            emptiness_result = load(pathlib.Path(result.emptiness_gate_result_path))
            if len(tick_log) != 2:
                errors.append("tick log length mismatch")
            for index, entry in enumerate(tick_log):
                validate_tick_entry(entry, errors, f"tick_log[{index}]")
            if daemon_result.get("ticks_run") != 2:
                errors.append("daemon_result ticks_run mismatch")
            if daemon_result.get("yinyang_polarity_state") != "RECOVERY_YANG_PRESENT":
                errors.append("daemon_result yinyang mismatch")
            if daemon_result.get("four_image_phase") != "LESSER_YANG":
                errors.append("daemon_result four image mismatch")
            if daemon_result.get("qi_policy_recommended_tick_mode") != "CONTINUE_WITH_QI_MEMORY_MONITOR":
                errors.append("daemon_result qi policy mismatch")
            if daemon_result.get("emptiness_recommended_action") != "CONTINUE_ADVISORY_ONLY":
                errors.append("daemon_result emptiness action mismatch")
            if yy_result.get("yinyang_polarity_state") != "RECOVERY_YANG_PRESENT":
                errors.append("yinyang_result state mismatch")
            if four_result.get("four_image_phase") != "LESSER_YANG":
                errors.append("four_result phase mismatch")
            if policy_result.get("recommended_tick_mode") != "CONTINUE_WITH_QI_MEMORY_MONITOR":
                errors.append("policy_result mode mismatch")
            if emptiness_result.get("recommended_emptiness_action") != "CONTINUE_ADVISORY_ONLY":
                errors.append("emptiness_result action mismatch")
            if not emptiness_result.get("non_reification_assertions", {}).get("policy_hint_is_not_command"):
                errors.append("emptiness_result missing non-reification assertion")
            if yy_result.get("grants_execution_authority") is not False:
                errors.append("yinyang_result execution flag not false")
            if four_result.get("grants_execution_authority") is not False:
                errors.append("four_result execution flag not false")
            if policy_result.get("grants_execution_authority") is not False:
                errors.append("policy_result execution flag not false")
            if emptiness_result.get("grants_execution_authority") is not False:
                errors.append("emptiness_result execution flag not false")
            if daemon_result.get("grants_execution_authority") is not False:
                errors.append("daemon_result execution flag not false")

            first_trace = load(pathlib.Path(tick_log[0]["step_trace_path"]))
            if not first_trace:
                errors.append("first tick trace empty")
            else:
                summary = first_trace[0].get("qi_process_tensor_summary")
                if not isinstance(summary, dict):
                    errors.append("missing qi process tensor summary")
                elif summary.get("process_tensor_visible") is not True:
                    errors.append("process tensor summary not visible")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: KuuOS runtime daemon example check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
