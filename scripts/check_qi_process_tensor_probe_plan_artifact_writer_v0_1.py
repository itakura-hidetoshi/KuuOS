#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
WRITER = ROOT / "scripts" / "write_qi_process_tensor_probe_plan_artifact_v0_1.py"


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    errors: list[str] = []
    if not WRITER.is_file():
        errors.append(f"missing:{WRITER}")
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1

    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        status_view = root / "status_view.json"
        artifact_path = root / "probe_plan_artifact.json"
        blocked_status_view = root / "blocked_status_view.json"
        blocked_artifact_path = root / "blocked_probe_plan_artifact.json"

        dump(status_view, {
            "status_view_status": "QI_PERSISTENT_SUPERVISOR_STATUS_VIEW_READY",
            "out_dir": str(root / "supervisor"),
            "latest_controlled_loop_result_path": str(root / "loop.json"),
            "recommended_probe_type": "observation_debt_probe",
            "probe_target_time_slice": "t_debt",
            "probe_risk_level": "medium",
            "grants_probe_execution_authority": False,
            "latest_process_tensor_advantage_metrics": {"metrics_status": "QI_PROCESS_TENSOR_ADVANTAGE_READY"},
            "latest_process_tensor_probe_plan": {
                "probe_plan_status": "QI_PROCESS_TENSOR_PROBE_PLAN_READY_WITH_WARNINGS",
                "recommended_probe_type": "observation_debt_probe",
                "probe_target_time_slice": "t_debt",
                "probe_expected_recoverability_gain": 0.12,
                "probe_expected_observation_debt_reduction": 0.66,
                "probe_risk_level": "medium",
                "probe_plan_only": True,
                "read_only": True,
                "authority": "none",
                "grants_probe_execution_authority": False,
                "grants_next_tick_execution_authority": False,
                "grants_memory_overwrite_authority": False,
            },
        })
        completed = subprocess.run([
            sys.executable,
            str(WRITER),
            "--status-view",
            str(status_view),
            "--write",
            str(artifact_path),
            "--quiet",
        ], cwd=str(ROOT), text=True, capture_output=True, check=False)
        if completed.returncode != 0:
            errors.append(f"writer_ready_returned:{completed.returncode}")
            errors.append(completed.stderr.strip() or completed.stdout.strip())
        if not artifact_path.is_file():
            errors.append("artifact output missing")
        else:
            artifact = load(artifact_path)
            if artifact.get("artifact_status") != "QI_PROCESS_TENSOR_PROBE_PLAN_ARTIFACT_READY":
                errors.append("artifact should be ready")
            if artifact.get("recommended_probe_type") != "observation_debt_probe":
                errors.append("recommended probe mismatch")
            if artifact.get("proposal_artifact_only") is not True:
                errors.append("proposal artifact flag mismatch")
            if artifact.get("read_only") is not True:
                errors.append("artifact read_only mismatch")
            if artifact.get("authority") != "none":
                errors.append("artifact authority mismatch")
            for key in [
                "grants_execution_authority",
                "grants_probe_execution_authority",
                "grants_next_tick_execution_authority",
                "grants_control_packet_authority",
                "grants_memory_overwrite_authority",
            ]:
                if artifact.get(key) is not False:
                    errors.append(f"{key} should be false")

        dump(blocked_status_view, {
            "status_view_status": "QI_PERSISTENT_SUPERVISOR_STATUS_VIEW_READY",
            "latest_process_tensor_probe_plan": {
                "probe_plan_status": "QI_PROCESS_TENSOR_PROBE_PLAN_READY",
                "probe_plan_only": True,
                "read_only": True,
                "authority": "none",
                "grants_probe_execution_authority": True,
            },
            "grants_probe_execution_authority": False,
        })
        completed = subprocess.run([
            sys.executable,
            str(WRITER),
            "--status-view",
            str(blocked_status_view),
            "--write",
            str(blocked_artifact_path),
            "--quiet",
        ], cwd=str(ROOT), text=True, capture_output=True, check=False)
        if completed.returncode == 0:
            errors.append("writer blocked case should return nonzero")
        if not blocked_artifact_path.is_file():
            errors.append("blocked artifact output missing")
        else:
            blocked = load(blocked_artifact_path)
            if blocked.get("artifact_status") != "QI_PROCESS_TENSOR_PROBE_PLAN_ARTIFACT_BLOCKED":
                errors.append("blocked artifact status mismatch")
            if "probe_plan_execution_authority_not_false" not in blocked.get("artifact_blockers", []):
                errors.append("blocked authority reason missing")
            if blocked.get("authority") != "none":
                errors.append("blocked artifact authority mismatch")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi process tensor probe plan artifact writer check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
