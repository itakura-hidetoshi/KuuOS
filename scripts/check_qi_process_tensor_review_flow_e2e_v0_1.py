#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CONTROL_WRITER = ROOT / "scripts" / "write_qi_supervisor_control_v0_1.py"
SUPERVISOR_CLI = ROOT / "scripts" / "run_qi_persistent_supervisor_v0_1.py"
STATUS_CLI = ROOT / "scripts" / "view_qi_persistent_supervisor_status_v0_1.py"
ARTIFACT_CLI = ROOT / "scripts" / "write_qi_process_tensor_probe_plan_artifact_v0_1.py"
INDEX_CLI = ROOT / "scripts" / "write_qi_process_tensor_probe_plan_artifact_index_v0_1.py"
SUMMARY_CLI = ROOT / "scripts" / "write_qi_process_tensor_probe_plan_trend_summary_v0_1.py"
RAW = ROOT / "examples" / "qi_process_tensor_v0_1" / "raw_state_process_history.json"
EVIDENCE = ROOT / "examples" / "qi_process_tensor_v0_1" / "evidence.json"


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def run(args: list[str]):
    return subprocess.run(args, cwd=str(ROOT), text=True, capture_output=True, check=False)


def require_no_authority(payload: dict, errors: list[str], prefix: str) -> None:
    if payload.get("authority") != "none":
        errors.append(f"{prefix}:authority_not_none")
    for key in [
        "grants_execution_authority",
        "grants_probe_execution_authority",
        "grants_next_tick_execution_authority",
        "grants_control_packet_authority",
        "grants_memory_overwrite_authority",
    ]:
        if payload.get(key) is not False:
            errors.append(f"{prefix}:{key}_not_false")


def main() -> int:
    errors: list[str] = []
    for path in [CONTROL_WRITER, SUPERVISOR_CLI, STATUS_CLI, ARTIFACT_CLI, INDEX_CLI, SUMMARY_CLI, RAW, EVIDENCE]:
        if not path.is_file():
            errors.append(f"missing:{path}")
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1

    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        control = root / "control.json"
        out_dir = root / "run"
        status_json = root / "status_view.json"
        status_text = root / "status_view.txt"
        artifact_a = root / "probe_plan_artifact_a.json"
        artifact_b = root / "probe_plan_artifact_b.json"
        index_json = root / "probe_plan_artifact_index.json"
        summary_json = root / "probe_plan_trend_summary.json"
        summary_text = root / "probe_plan_trend_summary.txt"

        steps = [
            [sys.executable, str(CONTROL_WRITER), "--allow", "--write", str(control), "--max-cycles", "1", "--sleep-seconds-between-cycles", "0", "--reason", "process tensor review e2e", "--quiet"],
            [sys.executable, str(SUPERVISOR_CLI), "--raw-state", str(RAW), "--evidence", str(EVIDENCE), "--control", str(control), "--out-dir", str(out_dir), "--max-outer-iterations", "1", "--max-daemon-ticks", "1", "--max-steps-per-tick", "1", "--requested-max-reentry-cycles", "1", "--sleep-seconds-between-iterations", "0", "--quiet"],
            [sys.executable, str(STATUS_CLI), "--out-dir", str(out_dir), "--write-json", str(status_json), "--write-text", str(status_text), "--quiet"],
            [sys.executable, str(ARTIFACT_CLI), "--status-view", str(status_json), "--write", str(artifact_a), "--quiet"],
            [sys.executable, str(ARTIFACT_CLI), "--out-dir", str(out_dir), "--write", str(artifact_b), "--quiet"],
            [sys.executable, str(INDEX_CLI), "--artifact", str(artifact_a), "--artifact", str(artifact_b), "--write", str(index_json), "--quiet"],
            [sys.executable, str(SUMMARY_CLI), "--index", str(index_json), "--write-json", str(summary_json), "--write-text", str(summary_text), "--quiet"],
        ]
        for step in steps:
            completed = run(step)
            if completed.returncode != 0:
                errors.append(f"step_returned:{completed.returncode}:{' '.join(step[1:3])}")
                errors.append(completed.stderr.strip() or completed.stdout.strip())
                break

        expected_paths = [control, status_json, status_text, artifact_a, artifact_b, index_json, summary_json, summary_text]
        for path in expected_paths:
            if not path.is_file():
                errors.append(f"missing_output:{path.name}")
        if not errors:
            status = load(status_json)
            artifact = load(artifact_a)
            artifact_b_value = load(artifact_b)
            index = load(index_json)
            summary = load(summary_json)
            text = summary_text.read_text(encoding="utf-8")

            if status.get("status_view_status") != "QI_PERSISTENT_SUPERVISOR_STATUS_VIEW_READY":
                errors.append("status_view_not_ready")
            if not status.get("latest_process_tensor_probe_plan"):
                errors.append("status_probe_plan_missing")
            if artifact.get("artifact_status") != "QI_PROCESS_TENSOR_PROBE_PLAN_ARTIFACT_READY":
                errors.append("artifact_a_not_ready")
            if artifact_b_value.get("artifact_status") != "QI_PROCESS_TENSOR_PROBE_PLAN_ARTIFACT_READY":
                errors.append("artifact_b_not_ready")
            if index.get("index_status") != "QI_PROCESS_TENSOR_PROBE_PLAN_ARTIFACT_INDEX_READY":
                errors.append("index_not_ready")
            if index.get("artifact_count") != 2:
                errors.append("index_artifact_count_mismatch")
            if summary.get("summary_status") != "QI_PROCESS_TENSOR_PROBE_PLAN_TREND_SUMMARY_READY":
                errors.append("summary_not_ready")
            if summary.get("summary_only") is not True:
                errors.append("summary_only_mismatch")
            if "recommended_operator_focus:" not in text:
                errors.append("summary_text_operator_focus_missing")
            if "authority: none" not in text:
                errors.append("summary_text_authority_missing")

            require_no_authority(status, errors, "status")
            require_no_authority(artifact, errors, "artifact_a")
            require_no_authority(artifact_b_value, errors, "artifact_b")
            require_no_authority(index, errors, "index")
            require_no_authority(summary, errors, "summary")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi process tensor review flow E2E check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
