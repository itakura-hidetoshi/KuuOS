#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "write_qi_dry_run_probe_sim_v0_1.py"


def dump(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    errors: list[str] = []
    if not CLI.is_file():
        errors.append(f"missing:{CLI}")
    if errors:
        for e in errors:
            print("ERROR:", e)
        return 1

    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        license_path = root / "license.json"
        summary_path = root / "summary.json"
        out_path = root / "simulation.json"

        dump(license_path, {
            "gate_status": "QI_ACTUATION_LICENSE_DRY_RUN_CANDIDATE_READY",
            "candidate_license_kind": "dry_run_probe_simulation_candidate",
            "license_candidate_only": True,
            "dry_run_candidate_only": True,
            "authority": "none",
            "grants_execution_authority": False,
            "grants_probe_execution_authority": False,
            "grants_dry_run_execution_authority": False,
            "grants_next_tick_execution_authority": False,
            "grants_control_packet_authority": False,
            "grants_memory_overwrite_authority": False,
            "grants_world_update_authority": False,
        })

        dump(summary_path, {
            "summary_status": "QI_PROCESS_TENSOR_PROBE_PLAN_TREND_SUMMARY_READY",
            "summary_only": True,
            "read_only": True,
            "latest_recommended_probe_type": "observation_debt_probe",
            "latest_probe_target_time_slice": "recent_transition_window",
            "authority": "none",
            "grants_execution_authority": False,
            "grants_probe_execution_authority": False,
            "grants_dry_run_execution_authority": False,
            "grants_next_tick_execution_authority": False,
            "grants_control_packet_authority": False,
            "grants_memory_overwrite_authority": False,
            "grants_world_update_authority": False,
        })

        completed = subprocess.run([
            sys.executable, str(CLI),
            "--license", str(license_path),
            "--summary", str(summary_path),
            "--write", str(out_path),
            "--quiet",
        ], cwd=str(ROOT), text=True, capture_output=True, check=False)

        if completed.returncode != 0:
            errors.append(f"cli_returncode:{completed.returncode}")

        if not out_path.is_file():
            errors.append("simulation_output_missing")
        else:
            value = load(out_path)
            if value.get("simulation_status") != "QI_DRY_RUN_PROBE_SIMULATION_READY":
                errors.append("simulation_status_mismatch")
            if value.get("authority") != "none":
                errors.append("authority_not_none")
            for key in [
                "grants_execution_authority",
                "grants_probe_execution_authority",
                "grants_dry_run_execution_authority",
                "grants_next_tick_execution_authority",
                "grants_control_packet_authority",
                "grants_memory_overwrite_authority",
                "grants_world_update_authority",
            ]:
                if value.get(key) is not False:
                    errors.append(f"{key}_not_false")
            if value.get("state_mutation_performed") is not False:
                errors.append("state_mutation_performed_not_false")
            if value.get("control_packet_mutation_performed") is not False:
                errors.append("control_packet_mutation_performed_not_false")
            if value.get("memory_write_performed") is not False:
                errors.append("memory_write_performed_not_false")

    if errors:
        for e in errors:
            print("ERROR:", e)
        return 1

    print("PASS: Qi dry-run probe simulation check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
