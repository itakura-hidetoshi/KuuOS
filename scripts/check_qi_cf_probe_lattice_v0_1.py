#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "write_qi_cf_probe_lattice_v0_1.py"


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
        sim = root / "sim.json"
        summary = root / "summary.json"
        out = root / "lattice.json"
        dump(sim, {
            "simulation_status": "QI_DRY_RUN_PROBE_SIMULATION_READY",
            "simulated_probe_type": "observation_debt_probe",
            "simulated_target_time_slice": "recent_transition_window",
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
        dump(summary, {
            "summary_status": "QI_PROCESS_TENSOR_PROBE_PLAN_TREND_SUMMARY_READY",
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
            sys.executable, str(CLI), "--simulation", str(sim), "--summary", str(summary), "--write", str(out), "--quiet"
        ], cwd=str(ROOT), text=True, capture_output=True, check=False)
        if completed.returncode != 0:
            errors.append(f"cli_returncode:{completed.returncode}")
        if not out.is_file():
            errors.append("lattice_output_missing")
        else:
            value = load(out)
            if value.get("lattice_status") != "QI_COUNTERFACTUAL_PROBE_LATTICE_READY":
                errors.append("lattice_status_mismatch")
            if value.get("counterfactual_only") is not True:
                errors.append("counterfactual_only_not_true")
            if value.get("simulation_only") is not True:
                errors.append("simulation_only_not_true")
            if value.get("dry_run_only") is not True:
                errors.append("dry_run_only_not_true")
            if value.get("candidate_count", 0) < 2:
                errors.append("candidate_count_too_low")
            roles = {item.get("candidate_role") for item in value.get("ranked_candidates", [])}
            if "chosen_probe" not in roles:
                errors.append("chosen_probe_missing")
            if "unchosen_counterfactual_probe" not in roles:
                errors.append("unchosen_probe_missing")
            for key in [
                "state_mutation_performed",
                "control_packet_mutation_performed",
                "memory_write_performed",
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
    if errors:
        for e in errors:
            print("ERROR:", e)
        return 1
    print("PASS: Qi CF probe lattice check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
