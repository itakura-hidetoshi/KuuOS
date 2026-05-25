#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW = ROOT / "examples" / "qi_process_tensor_v0_1" / "raw_state_process_history.json"
EVIDENCE = ROOT / "examples" / "qi_process_tensor_v0_1" / "evidence.json"
WRITE_CONTROL = ROOT / "scripts" / "write_qi_supervisor_control_v0_1.py"
RUN_SUPERVISOR = ROOT / "scripts" / "run_qi_persistent_supervisor_v0_1.py"
VIEW_STATUS = ROOT / "scripts" / "view_qi_persistent_supervisor_status_v0_1.py"


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def run_cmd(command: list[str], errors: list[str], label: str) -> None:
    completed = subprocess.run(command, cwd=str(ROOT), text=True, capture_output=True, check=False)
    if completed.returncode != 0:
        errors.append(f"{label}_returned:{completed.returncode}")
        errors.append(completed.stderr.strip() or completed.stdout.strip())


def main() -> int:
    errors: list[str] = []
    for path in [RAW, EVIDENCE, WRITE_CONTROL, RUN_SUPERVISOR, VIEW_STATUS]:
        if not path.is_file():
            errors.append(f"missing:{path}")
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1

    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        control_path = root / "control.json"
        supervisor_out = root / "run"
        status_json = root / "status_view.json"
        status_text = root / "status_view.txt"
        stop_control_path = root / "stop_control.json"

        run_cmd([
            sys.executable,
            str(WRITE_CONTROL),
            "--allow",
            "--write",
            str(control_path),
            "--max-cycles",
            "1",
            "--sleep-seconds-between-cycles",
            "0",
            "--reason",
            "operator e2e allow",
            "--quiet",
        ], errors, "write_allow_control")

        compiled_allow = control_path.with_name(control_path.stem + "_compiled_v0_1.json")
        if not control_path.is_file():
            errors.append("allow control packet missing")
        if not compiled_allow.is_file():
            errors.append("allow compiled control missing")
        if not errors:
            allow_packet = load(control_path)
            allow_compiled = load(compiled_allow)
            if allow_packet.get("mode") != "allow":
                errors.append("allow packet mode mismatch")
            if allow_compiled.get("loop_allowed") is not True:
                errors.append("allow compiled control should allow loop")
            if allow_compiled.get("grants_execution_authority") is not False:
                errors.append("allow compiled execution authority mismatch")

        run_cmd([
            sys.executable,
            str(RUN_SUPERVISOR),
            "--raw-state",
            str(RAW),
            "--evidence",
            str(EVIDENCE),
            "--control",
            str(control_path),
            "--out-dir",
            str(supervisor_out),
            "--max-outer-iterations",
            "1",
            "--max-daemon-ticks",
            "1",
            "--max-steps-per-tick",
            "1",
            "--requested-max-reentry-cycles",
            "1",
            "--sleep-seconds-between-iterations",
            "0",
            "--quiet",
        ], errors, "run_supervisor")

        supervisor_result_path = supervisor_out / "qi_persistent_supervisor_result_v0_1.json"
        supervisor_manifest_path = supervisor_out / "qi_persistent_supervisor_manifest_v0_1.json"
        supervisor_overview_path = supervisor_out / "qi_persistent_supervisor_overview_v0_1.txt"
        supervisor_operator_manifest_path = supervisor_out / "qi_persistent_supervisor_operator_manifest_v0_1.json"
        for path in [supervisor_result_path, supervisor_manifest_path, supervisor_overview_path, supervisor_operator_manifest_path]:
            if not path.is_file():
                errors.append(f"missing supervisor output:{path.name}")
        if not errors:
            supervisor = load(supervisor_result_path)
            operator_manifest = load(supervisor_operator_manifest_path)
            if supervisor.get("supervisor_status") != "QI_PERSISTENT_SUPERVISOR_COMPLETED":
                errors.append("supervisor status mismatch")
            if supervisor.get("iterations_run") != 1:
                errors.append("supervisor should run exactly one outer iteration in e2e")
            if supervisor.get("persistent_supervisor_only") is not True:
                errors.append("persistent supervisor flag mismatch")
            if supervisor.get("grants_execution_authority") is not False:
                errors.append("supervisor execution authority mismatch")
            if operator_manifest.get("authority") != "none":
                errors.append("operator manifest authority mismatch")
            records = supervisor.get("iteration_records", [])
            if not records:
                errors.append("supervisor iteration records missing")
            else:
                record = records[-1]
                if not pathlib.Path(record.get("heartbeat_path", "")).is_file():
                    errors.append("e2e heartbeat missing")
                if not pathlib.Path(record.get("status_path", "")).is_file():
                    errors.append("e2e status missing")

        run_cmd([
            sys.executable,
            str(VIEW_STATUS),
            "--out-dir",
            str(supervisor_out),
            "--write-json",
            str(status_json),
            "--write-text",
            str(status_text),
            "--quiet",
        ], errors, "view_status")

        if not status_json.is_file():
            errors.append("status view json missing")
        if not status_text.is_file():
            errors.append("status view text missing")
        if not errors:
            status_view = load(status_json)
            text = status_text.read_text(encoding="utf-8")
            if status_view.get("status_view_status") != "QI_PERSISTENT_SUPERVISOR_STATUS_VIEW_READY":
                errors.append("status view should be ready")
            if status_view.get("iterations_run") != 1:
                errors.append("status view iterations mismatch")
            if status_view.get("latest_heartbeat_path") is None:
                errors.append("status view heartbeat missing")
            if "authority: none" not in text:
                errors.append("status view text authority missing")

        run_cmd([
            sys.executable,
            str(WRITE_CONTROL),
            "--stop",
            "--write",
            str(stop_control_path),
            "--max-cycles",
            "1",
            "--reason",
            "operator e2e stop",
            "--quiet",
        ], errors, "write_stop_control")

        compiled_stop = stop_control_path.with_name(stop_control_path.stem + "_compiled_v0_1.json")
        if not stop_control_path.is_file():
            errors.append("stop control packet missing")
        if not compiled_stop.is_file():
            errors.append("stop compiled control missing")
        if not errors:
            stop_packet = load(stop_control_path)
            stop_compiled = load(compiled_stop)
            if stop_packet.get("mode") != "stop":
                errors.append("stop packet mode mismatch")
            if stop_compiled.get("loop_allowed") is not False:
                errors.append("stop compiled control should block loop")
            if stop_compiled.get("control_reason") != "stop_requested":
                errors.append("stop compiled reason mismatch")
            if stop_compiled.get("grants_next_tick_execution_authority") is not False:
                errors.append("stop compiled next tick authority mismatch")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi persistent supervisor operator E2E check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
