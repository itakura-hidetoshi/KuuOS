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
RUN_CLI = ROOT / "scripts" / "run_qi_persistent_supervisor_v0_1.py"
VIEW_CLI = ROOT / "scripts" / "view_qi_persistent_supervisor_status_v0_1.py"


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    errors: list[str] = []
    for path in [RAW, EVIDENCE, RUN_CLI, VIEW_CLI]:
        if not path.is_file():
            errors.append(f"missing:{path}")
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1

    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        out_dir = root / "supervisor"
        control_path = root / "control.json"
        dump(control_path, {"enabled": True, "stop_requested": False, "max_cycles": 1, "sleep_seconds_between_cycles": 0})
        run_cmd = [
            sys.executable,
            str(RUN_CLI),
            "--raw-state",
            str(RAW),
            "--evidence",
            str(EVIDENCE),
            "--out-dir",
            str(out_dir),
            "--control",
            str(control_path),
            "--max-outer-iterations",
            "1",
            "--max-daemon-ticks",
            "1",
            "--max-steps-per-tick",
            "1",
            "--requested-max-reentry-cycles",
            "1",
            "--quiet",
        ]
        completed = subprocess.run(run_cmd, cwd=str(ROOT), text=True, capture_output=True, check=False)
        if completed.returncode != 0:
            errors.append(f"run_cli_returned:{completed.returncode}")
            errors.append(completed.stderr.strip() or completed.stdout.strip())
        view_json = root / "status_view.json"
        view_text = root / "status_view.txt"
        view_cmd = [
            sys.executable,
            str(VIEW_CLI),
            "--out-dir",
            str(out_dir),
            "--write-json",
            str(view_json),
            "--write-text",
            str(view_text),
            "--quiet",
        ]
        completed = subprocess.run(view_cmd, cwd=str(ROOT), text=True, capture_output=True, check=False)
        if completed.returncode != 0:
            errors.append(f"view_cli_returned:{completed.returncode}")
            errors.append(completed.stderr.strip() or completed.stdout.strip())
        for path in [view_json, view_text]:
            if not path.is_file():
                errors.append(f"missing view output:{path.name}")
        if not errors:
            view = load(view_json)
            text = view_text.read_text(encoding="utf-8")
            if view.get("status_view_status") != "QI_PERSISTENT_SUPERVISOR_STATUS_VIEW_READY":
                errors.append("view status not ready")
            if view.get("iterations_run", 0) < 1:
                errors.append("view iterations missing")
            if view.get("latest_heartbeat_path") is None:
                errors.append("latest heartbeat path missing")
            if view.get("latest_status_path") is None:
                errors.append("latest status path missing")
            if view.get("status_view_only") is not True:
                errors.append("status_view_only mismatch")
            if view.get("read_only") is not True:
                errors.append("read_only mismatch")
            if view.get("grants_execution_authority") is not False:
                errors.append("execution authority mismatch")
            if "Qi Persistent Supervisor Status" not in text:
                errors.append("status text title missing")
            if "authority: none" not in text:
                errors.append("status text authority missing")
            if "latest_heartbeat_path:" not in text:
                errors.append("status text heartbeat missing")

        missing_out = root / "missing_supervisor"
        missing_json = root / "missing_status_view.json"
        missing_text = root / "missing_status_view.txt"
        missing_cmd = [
            sys.executable,
            str(VIEW_CLI),
            "--out-dir",
            str(missing_out),
            "--write-json",
            str(missing_json),
            "--write-text",
            str(missing_text),
            "--quiet",
        ]
        completed = subprocess.run(missing_cmd, cwd=str(ROOT), text=True, capture_output=True, check=False)
        if completed.returncode != 0:
            errors.append(f"missing_view_cli_returned:{completed.returncode}")
        if not missing_json.is_file() or not missing_text.is_file():
            errors.append("missing view outputs not written")
        elif not errors:
            missing_view = load(missing_json)
            missing_text_value = missing_text.read_text(encoding="utf-8")
            if missing_view.get("status_view_status") != "QI_PERSISTENT_SUPERVISOR_STATUS_VIEW_BLOCKED":
                errors.append("missing view should be blocked")
            if "supervisor_manifest_missing" not in missing_text_value:
                errors.append("missing view text lacks blocker")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi persistent supervisor status view CLI check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
