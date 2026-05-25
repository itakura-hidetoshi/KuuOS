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
CLI = ROOT / "scripts" / "run_qi_daemon_once_v0_1.py"


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
        out_dir = pathlib.Path(tmp) / "out"
        command = [
            sys.executable,
            str(CLI),
            "--raw-state",
            str(RAW),
            "--evidence",
            str(EVIDENCE),
            "--out-dir",
            str(out_dir),
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
        manifest_path = out_dir / "qi_daemon_once_manifest_v0_1.json"
        result_path = out_dir / "qi_daemon_once_result_v0_1.json"
        readable_json_path = out_dir / "qi_daemon_once_readable_summary_v0_1.json"
        readable_text_path = out_dir / "qi_daemon_once_readable_summary_v0_1.txt"
        for path in [manifest_path, result_path, readable_json_path, readable_text_path]:
            if not path.is_file():
                errors.append(f"missing output:{path.name}")
        if not errors:
            manifest = load(manifest_path)
            result = load(result_path)
            readable = load(readable_json_path)
            readable_text = readable_text_path.read_text(encoding="utf-8")
            if manifest.get("authority") != "none":
                errors.append("manifest authority mismatch")
            if manifest.get("scope") != "operator_cli_once_read_only":
                errors.append("manifest scope mismatch")
            if manifest.get("recommended_next_runtime_mode") != result.get("recommended_next_runtime_mode"):
                errors.append("manifest mode mismatch")
            if manifest.get("next_tick_preparation") != result.get("next_tick_preparation"):
                errors.append("manifest preparation mismatch")
            if readable.get("recommended_next_runtime_mode") != result.get("recommended_next_runtime_mode"):
                errors.append("readable mode mismatch")
            if "Qi Routed Cycle Projection Plan" not in readable_text:
                errors.append("readable text missing title")
            if "authority: none" not in readable_text:
                errors.append("readable text missing authority line")
            if not isinstance(result.get("projection_statuses"), dict):
                errors.append("projection statuses missing")
            if result.get("grants_execution_authority") is not False:
                errors.append("execution flag mismatch")
            if result.get("grants_next_tick_execution_authority") is not False:
                errors.append("next tick flag mismatch")
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi daemon once operator CLI check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
