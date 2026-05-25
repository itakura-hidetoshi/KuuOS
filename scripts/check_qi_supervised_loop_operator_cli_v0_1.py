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
        out_dir = pathlib.Path(tmp) / "loop"
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
        completed = subprocess.run(command, cwd=str(ROOT), text=True, capture_output=True, check=False)
        if completed.returncode != 0:
            errors.append(f"cli_returned:{completed.returncode}")
            errors.append(completed.stderr.strip() or completed.stdout.strip())
        result_path = out_dir / "qi_supervised_loop_result_v0_1.json"
        overview_path = out_dir / "qi_supervised_loop_overview_v0_1.txt"
        operator_manifest_path = out_dir / "qi_supervised_loop_operator_manifest_v0_1.json"
        loop_manifest_path = out_dir / "qi_supervised_loop_manifest_v0_1.json"
        for path in [result_path, overview_path, operator_manifest_path, loop_manifest_path]:
            if not path.is_file():
                errors.append(f"missing output:{path.name}")
        if not errors:
            result = load(result_path)
            operator_manifest = load(operator_manifest_path)
            overview = overview_path.read_text(encoding="utf-8")
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

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi supervised loop operator CLI check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
