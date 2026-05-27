#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "write_qi_probe_scheduler_proposal_v0_1.py"


def dump(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    errors: list[str] = []
    if not CLI.is_file():
        errors.append(f"missing:{CLI}")
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        lattice = root / "lattice.json"
        out = root / "scheduler.json"
        dump(lattice, {
            "lattice_status": "QI_COUNTERFACTUAL_PROBE_LATTICE_READY",
            "recommended_probe_type": "observation_debt_probe",
            "chosen_probe_type": "observation_debt_probe",
            "counterfactual_only": True,
            "simulation_only": True,
            "dry_run_only": True,
            "state_mutation_performed": False,
            "control_packet_mutation_performed": False,
            "memory_write_performed": False,
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
            sys.executable, str(CLI), "--lattice", str(lattice), "--write", str(out), "--quiet"
        ], cwd=str(ROOT), text=True, capture_output=True, check=False)
        if completed.returncode != 0:
            errors.append(f"cli_returncode:{completed.returncode}")
        if not out.is_file():
            errors.append("scheduler_output_missing")
        else:
            value = load(out)
            if value.get("scheduler_status") != "QI_PROBE_SCHEDULER_PROPOSAL_READY":
                errors.append("scheduler_status_mismatch")
            for key in ["schedule_proposal_only", "counterfactual_only", "simulation_only", "dry_run_only"]:
                if value.get(key) is not True:
                    errors.append(f"{key}_not_true")
            for key in [
                "scheduler_mutation_performed",
                "control_packet_mutation_performed",
                "memory_write_performed",
                "grants_execution_authority",
                "grants_probe_execution_authority",
                "grants_dry_run_execution_authority",
                "grants_next_tick_execution_authority",
                "grants_scheduler_authority",
                "grants_control_packet_authority",
                "grants_memory_overwrite_authority",
                "grants_world_update_authority",
            ]:
                if value.get(key) is not False:
                    errors.append(f"{key}_not_false")
            if value.get("authority") != "none":
                errors.append("authority_not_none")
            if value.get("recommended_revisit_after_ticks") != 1:
                errors.append("recommended_revisit_after_ticks_mismatch")
    if errors:
        for e in errors:
            print("ERROR:", e)
        return 1
    print("PASS: Qi probe scheduler proposal check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
