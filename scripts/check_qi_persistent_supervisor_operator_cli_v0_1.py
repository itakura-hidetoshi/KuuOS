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
CLI = ROOT / "scripts" / "run_qi_persistent_supervisor_v0_1.py"


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run_cli(out_dir: pathlib.Path, control_path: pathlib.Path):
    command = [
        sys.executable,
        str(CLI),
        "--raw-state",
        str(RAW),
        "--evidence",
        str(EVIDENCE),
        "--out-dir",
        str(out_dir),
        "--control",
        str(control_path),
        "--max-outer-iterations",
        "2",
        "--max-daemon-ticks",
        "1",
        "--max-steps-per-tick",
        "1",
        "--requested-max-reentry-cycles",
        "1",
        "--sleep-seconds-between-iterations",
        "0",
        "--quiet",
    ]
    return subprocess.run(command, cwd=str(ROOT), text=True, capture_output=True, check=False)


def check_outputs(out_dir: pathlib.Path, errors: list[str]) -> tuple[dict, dict, str]:
    result_path = out_dir / "qi_persistent_supervisor_result_v0_1.json"
    overview_path = out_dir / "qi_persistent_supervisor_overview_v0_1.txt"
    operator_manifest_path = out_dir / "qi_persistent_supervisor_operator_manifest_v0_1.json"
    supervisor_manifest_path = out_dir / "qi_persistent_supervisor_manifest_v0_1.json"
    for path in [result_path, overview_path, operator_manifest_path, supervisor_manifest_path]:
        if not path.is_file():
            errors.append(f"missing output:{path.name}")
    if errors:
        return {}, {}, ""
    return load(result_path), load(operator_manifest_path), overview_path.read_text(encoding="utf-8")


def main() -> int:
    errors: list[str] = []
    for path in [RAW, EVIDENCE, CLI]:
        if not path.is_file():
            errors.append(f"missing:{path}")
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1

    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)

        allow_control = root / "allow_control.json"
        dump(allow_control, {"enabled": True, "stop_requested": False, "max_cycles": 1, "sleep_seconds_between_cycles": 0})
        allow_out = root / "allow_supervisor"
        completed = run_cli(allow_out, allow_control)
        if completed.returncode != 0:
            errors.append(f"allow_cli_returned:{completed.returncode}")
            errors.append(completed.stderr.strip() or completed.stdout.strip())
        allow_result, allow_manifest, allow_overview = check_outputs(allow_out, errors)
        if not errors:
            if allow_result.get("supervisor_status") != "QI_PERSISTENT_SUPERVISOR_COMPLETED":
                errors.append("allow supervisor status mismatch")
            if allow_result.get("iterations_run", 0) < 1:
                errors.append("allow iterations below 1")
            if allow_result.get("iterations_run", 0) > 2:
                errors.append("allow iterations exceeded max")
            if allow_result.get("persistent_supervisor_only") is not True:
                errors.append("persistent supervisor flag mismatch")
            if allow_result.get("bounded") is not True:
                errors.append("bounded mismatch")
            if allow_result.get("read_only") is not True:
                errors.append("read_only mismatch")
            if allow_result.get("grants_execution_authority") is not False:
                errors.append("execution flag mismatch")
            if allow_result.get("grants_next_tick_execution_authority") is not False:
                errors.append("next tick flag mismatch")
            if allow_manifest.get("scope") != "persistent_supervisor_bounded_read_only":
                errors.append("allow manifest scope mismatch")
            if allow_manifest.get("authority") != "none":
                errors.append("allow manifest authority mismatch")
            if allow_manifest.get("iterations_run") != allow_result.get("iterations_run"):
                errors.append("allow manifest iterations mismatch")
            if "Qi Persistent Supervisor" not in allow_overview:
                errors.append("allow overview title missing")
            if "total_control_checks:" not in allow_overview:
                errors.append("allow overview control checks missing")
            if "authority: none" not in allow_overview:
                errors.append("allow overview authority missing")
            for record in allow_result.get("iteration_records", []):
                if not pathlib.Path(record["heartbeat_path"]).is_file():
                    errors.append("allow missing heartbeat file")
                if not pathlib.Path(record["status_path"]).is_file():
                    errors.append("allow missing status file")

        stop_control = root / "stop_control.json"
        dump(stop_control, {"enabled": True, "stop_requested": True, "max_cycles": 1})
        stop_out = root / "stop_supervisor"
        completed = run_cli(stop_out, stop_control)
        if completed.returncode != 0:
            errors.append(f"stop_cli_returned:{completed.returncode}")
            errors.append(completed.stderr.strip() or completed.stdout.strip())
        stop_result, stop_manifest, stop_overview = check_outputs(stop_out, errors)
        if not errors:
            if stop_result.get("iterations_run") != 1:
                errors.append("stop iterations should be 1")
            if stop_result.get("total_cycles_run") != 0:
                errors.append("stop total cycles should be 0")
            if stop_result.get("final_stop_reason") != "stop_requested":
                errors.append("stop reason mismatch")
            if stop_manifest.get("final_stop_reason") != "stop_requested":
                errors.append("stop manifest reason mismatch")
            records = stop_result.get("iteration_records", [])
            if not records or records[0].get("loop_allowed") is not False:
                errors.append("stop iteration should be blocked")
            if "allowed=False" not in stop_overview:
                errors.append("stop overview missing allowed false")
            if "stop_requested" not in stop_overview:
                errors.append("stop overview missing stop reason")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi persistent supervisor operator CLI check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
