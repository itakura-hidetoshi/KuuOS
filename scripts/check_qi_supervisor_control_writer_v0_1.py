#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "write_qi_supervisor_control_v0_1.py"


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def run_writer(path: pathlib.Path, mode: str):
    command = [
        sys.executable,
        str(CLI),
        f"--{mode}",
        "--write",
        str(path),
        "--max-cycles",
        "2",
        "--sleep-seconds-between-cycles",
        "0",
        "--quiet",
    ]
    return subprocess.run(command, cwd=str(ROOT), text=True, capture_output=True, check=False)


def compiled_path(path: pathlib.Path) -> pathlib.Path:
    return path.with_name(path.stem + "_compiled_v0_1.json")


def main() -> int:
    errors: list[str] = []
    if not CLI.is_file():
        errors.append(f"missing:{CLI}")
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1

    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        cases = [
            ("allow", True, False, True, "QI_SUPERVISED_LOOP_CONTROL_ALLOWED"),
            ("stop", True, True, False, "QI_SUPERVISED_LOOP_CONTROL_BLOCKED"),
            ("disable", False, False, False, "QI_SUPERVISED_LOOP_CONTROL_BLOCKED"),
        ]
        for mode, expected_enabled, expected_stop, expected_allowed, expected_status in cases:
            path = root / f"{mode}_control.json"
            completed = run_writer(path, mode)
            if completed.returncode != 0:
                errors.append(f"{mode}_writer_returned:{completed.returncode}")
                errors.append(completed.stderr.strip() or completed.stdout.strip())
                continue
            cpath = compiled_path(path)
            if not path.is_file():
                errors.append(f"{mode}: packet missing")
                continue
            if not cpath.is_file():
                errors.append(f"{mode}: compiled control missing")
                continue
            packet = load(path)
            compiled = load(cpath)
            if packet.get("mode") != mode:
                errors.append(f"{mode}: mode mismatch")
            if packet.get("enabled") is not expected_enabled:
                errors.append(f"{mode}: enabled mismatch")
            if packet.get("stop_requested") is not expected_stop:
                errors.append(f"{mode}: stop mismatch")
            if packet.get("authority") != "none":
                errors.append(f"{mode}: packet authority mismatch")
            if compiled.get("loop_allowed") is not expected_allowed:
                errors.append(f"{mode}: loop_allowed mismatch")
            if compiled.get("control_status") != expected_status:
                errors.append(f"{mode}: control status mismatch")
            if compiled.get("grants_execution_authority") is not False:
                errors.append(f"{mode}: execution authority mismatch")
            if compiled.get("grants_next_tick_execution_authority") is not False:
                errors.append(f"{mode}: next tick authority mismatch")

        bad_path = root / "bad_control.json"
        bad = subprocess.run([
            sys.executable,
            str(CLI),
            "--allow",
            "--write",
            str(bad_path),
            "--max-cycles",
            "0",
            "--quiet",
        ], cwd=str(ROOT), text=True, capture_output=True, check=False)
        if bad.returncode != 2:
            errors.append("invalid max cycles should return 2")
        if bad_path.exists():
            errors.append("invalid max cycles should not write packet")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi supervisor control writer check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
