#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
SUMMARY_CLI = ROOT / "scripts" / "write_qi_process_tensor_probe_plan_trend_summary_v0_1.py"


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    errors: list[str] = []
    if not SUMMARY_CLI.is_file():
        errors.append(f"missing:{SUMMARY_CLI}")
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1

    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        index_path = root / "index.json"
        summary_json = root / "summary.json"
        summary_text = root / "summary.txt"
        blocked_index_path = root / "blocked_index.json"
        blocked_summary_json = root / "blocked_summary.json"
        dump(index_path, {
            "index_status": "QI_PROCESS_TENSOR_PROBE_PLAN_ARTIFACT_INDEX_READY",
            "dominant_probe_type": "observation_debt_probe",
            "latest_recommended_probe_type": "observation_debt_probe",
            "latest_probe_target_time_slice": "t2",
            "repeated_probe_types": ["observation_debt_probe"],
            "index_only": True,
            "read_only": True,
            "authority": "none",
            "grants_probe_execution_authority": False,
            "grants_next_tick_execution_authority": False,
            "grants_control_packet_authority": False,
            "grants_memory_overwrite_authority": False,
        })
        completed = subprocess.run([
            sys.executable,
            str(SUMMARY_CLI),
            "--index", str(index_path),
            "--write-json", str(summary_json),
            "--write-text", str(summary_text),
            "--quiet",
        ], cwd=str(ROOT), text=True, capture_output=True, check=False)
        if completed.returncode != 0:
            errors.append(f"summary_ready_returned:{completed.returncode}")
            errors.append(completed.stderr.strip() or completed.stdout.strip())
        if not summary_json.is_file() or not summary_text.is_file():
            errors.append("summary outputs missing")
        else:
            summary = load(summary_json)
            text = summary_text.read_text(encoding="utf-8")
            if summary.get("summary_status") != "QI_PROCESS_TENSOR_PROBE_PLAN_TREND_SUMMARY_READY":
                errors.append("summary should be ready")
            if summary.get("qi_process_tensor_characterization") != "observation_debt_limited_qi_process_tensor":
                errors.append("characterization mismatch")
            if summary.get("authority") != "none":
                errors.append("summary authority mismatch")
            if summary.get("summary_only") is not True:
                errors.append("summary_only mismatch")
            if summary.get("read_only") is not True:
                errors.append("read_only mismatch")
            for key in [
                "grants_execution_authority",
                "grants_probe_execution_authority",
                "grants_next_tick_execution_authority",
                "grants_control_packet_authority",
                "grants_memory_overwrite_authority",
            ]:
                if summary.get(key) is not False:
                    errors.append(f"{key} should be false")
            if "trend_interpretation:" not in text:
                errors.append("text trend interpretation missing")
            if "recommended_operator_focus:" not in text:
                errors.append("text operator focus missing")
            if "authority: none" not in text:
                errors.append("text authority missing")

        dump(blocked_index_path, {
            "index_status": "QI_PROCESS_TENSOR_PROBE_PLAN_ARTIFACT_INDEX_BLOCKED",
            "index_only": True,
            "read_only": True,
            "authority": "none",
            "grants_probe_execution_authority": False,
            "grants_next_tick_execution_authority": False,
            "grants_control_packet_authority": False,
            "grants_memory_overwrite_authority": False,
        })
        completed = subprocess.run([
            sys.executable,
            str(SUMMARY_CLI),
            "--index", str(blocked_index_path),
            "--write-json", str(blocked_summary_json),
            "--quiet",
        ], cwd=str(ROOT), text=True, capture_output=True, check=False)
        if completed.returncode == 0:
            errors.append("blocked summary should return nonzero")
        if not blocked_summary_json.is_file():
            errors.append("blocked summary output missing")
        else:
            blocked = load(blocked_summary_json)
            if blocked.get("summary_status") != "QI_PROCESS_TENSOR_PROBE_PLAN_TREND_SUMMARY_BLOCKED":
                errors.append("blocked summary status mismatch")
            if "artifact_index_not_ready" not in blocked.get("summary_blockers", []):
                errors.append("blocked reason missing")
            if blocked.get("authority") != "none":
                errors.append("blocked authority mismatch")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi process tensor probe plan trend summary check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
