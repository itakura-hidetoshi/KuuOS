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
CLI = ROOT / "scripts" / "run_qi_supervised_loop_v0_1.py"


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run_cli(out_dir: pathlib.Path, extra_args: list[str] | None = None):
    command = [
        sys.executable,
        str(CLI),
        "--raw-state",
        str(RAW),
        "--evidence",
        str(EVIDENCE),
        "--out-dir",
        str(out_dir),
        "--max-cycles",
        "2",
        "--max-daemon-ticks",
        "1",
        "--max-steps-per-tick",
        "1",
        "--requested-max-reentry-cycles",
        "1",
        "--quiet",
    ]
    if extra_args:
        command.extend(extra_args)
    return subprocess.run(command, cwd=str(ROOT), text=True, capture_output=True, check=False)


def check_standard_outputs(out_dir: pathlib.Path, errors: list[str]) -> tuple[dict, dict, str]:
    result_path = out_dir / "qi_supervised_loop_result_v0_1.json"
    overview_path = out_dir / "qi_supervised_loop_overview_v0_1.txt"
    operator_manifest_path = out_dir / "qi_supervised_loop_operator_manifest_v0_1.json"
    loop_manifest_path = out_dir / "qi_supervised_loop_manifest_v0_1.json"
    for path in [result_path, overview_path, operator_manifest_path, loop_manifest_path]:
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
        out_dir = root / "loop"
        completed = run_cli(out_dir)
        if completed.returncode != 0:
            errors.append(f"cli_returned:{completed.returncode}")
            errors.append(completed.stderr.strip() or completed.stdout.strip())
        result, operator_manifest, overview = check_standard_outputs(out_dir, errors)
        if not errors:
            if operator_manifest.get("authority") != "none":
                errors.append("operator manifest authority mismatch")
            if operator_manifest.get("scope") != "supervised_bounded_loop_only":
                errors.append("operator manifest scope mismatch")
            if operator_manifest.get("cycles_run") != result.get("cycles_run"):
                errors.append("cycles_run mismatch")
            if result.get("cycles_run", 0) < 1:
                errors.append("cycles_run below 1")
            if result.get("cycles_run", 0) > 2:
                errors.append("cycles_run exceeded max")
            if result.get("bounded") is not True:
                errors.append("bounded flag mismatch")
            if result.get("read_only") is not True:
                errors.append("read_only flag mismatch")
            if result.get("supervised_loop_only") is not True:
                errors.append("supervised_loop_only flag mismatch")
            if result.get("grants_execution_authority") is not False:
                errors.append("execution flag mismatch")
            if result.get("grants_next_tick_execution_authority") is not False:
                errors.append("next tick flag mismatch")
            if "Qi Supervised Loop" not in overview:
                errors.append("overview missing title")
            if "final_stop_reason:" not in overview:
                errors.append("overview missing stop reason")
            if "authority: none" not in overview:
                errors.append("overview missing authority line")

        allow_control = root / "allow_control.json"
        dump(allow_control, {"enabled": True, "stop_requested": False, "max_cycles": 1, "sleep_seconds_between_cycles": 0})
        allow_out = root / "allow_loop"
        completed = run_cli(allow_out, ["--control", str(allow_control)])
        if completed.returncode != 0:
            errors.append(f"allow_control_cli_returned:{completed.returncode}")
            errors.append(completed.stderr.strip() or completed.stdout.strip())
        allow_result, allow_manifest, allow_overview = check_standard_outputs(allow_out, errors)
        control_result_path = allow_out / "qi_supervised_loop_control_v0_1.json"
        if not control_result_path.is_file():
            errors.append("missing allow control result")
        elif not errors:
            control_result = load(control_result_path)
            if control_result.get("loop_allowed") is not True:
                errors.append("allow control did not allow loop")
            if allow_result.get("cycles_run") != 1:
                errors.append("allow control max_cycles not honored")
            if allow_manifest.get("control_result_path") != str(control_result_path):
                errors.append("allow manifest control result path mismatch")
            if "control_status: QI_SUPERVISED_LOOP_CONTROL_ALLOWED" not in allow_overview:
                errors.append("allow overview missing control status")

        stop_control = root / "stop_control.json"
        dump(stop_control, {"enabled": True, "stop_requested": True, "max_cycles": 2, "sleep_seconds_between_cycles": 0})
        stop_out = root / "stop_loop"
        completed = run_cli(stop_out, ["--control", str(stop_control)])
        if completed.returncode != 0:
            errors.append(f"stop_control_cli_returned:{completed.returncode}")
            errors.append(completed.stderr.strip() or completed.stdout.strip())
        stop_result, stop_manifest, stop_overview = check_standard_outputs(stop_out, errors)
        stop_control_result_path = stop_out / "qi_supervised_loop_control_v0_1.json"
        if not stop_control_result_path.is_file():
            errors.append("missing stop control result")
        elif not errors:
            control_result = load(stop_control_result_path)
            if control_result.get("loop_allowed") is not False:
                errors.append("stop control did not block loop")
            if stop_result.get("cycles_run") != 0:
                errors.append("stop control should not run cycles")
            if stop_result.get("loop_status") != "QI_SUPERVISED_LOOP_BLOCKED_BY_CONTROL":
                errors.append("stop result status mismatch")
            if stop_manifest.get("final_stop_reason") != "stop_requested":
                errors.append("stop manifest reason mismatch")
            if "loop_allowed: False" not in stop_overview:
                errors.append("stop overview missing loop_allowed false")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi supervised loop operator CLI check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
