#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "write_qi_process_tensor_aware_scheduler_state_v0_1.py"


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
        state = root / "state.json"
        proposal = root / "proposal.json"
        metrics = root / "metrics.json"
        out = root / "out.json"
        out_state = root / "state_out.json"
        dump(state, {"last_scheduled_tick": 4})
        dump(proposal, {
            "scheduler_status": "QI_PROBE_SCHEDULER_PROPOSAL_READY",
            "recommended_schedule_mode": "medium_horizon_revisit",
            "recommended_revisit_after_ticks": 3,
            "source_recommended_probe_type": "nonmarkov_memory_link_probe",
            "schedule_proposal_only": True,
            "authority": "none",
            "grants_execution_authority": False,
            "grants_probe_execution_authority": False,
            "grants_dry_run_execution_authority": False,
            "grants_next_tick_execution_authority": False,
            "grants_control_packet_authority": False,
            "grants_memory_overwrite_authority": False,
            "grants_world_update_authority": False,
        })
        dump(metrics, {
            "process_tensor_advantage_level": "QI_PROCESS_TENSOR_ADVANTAGE_READY",
            "history_depth": 5,
            "observation_debt_resolution_priority": 0.82,
            "safe_reentry_window_score": 0.28,
            "nonmarkov_link_density": 0.20,
            "memory_kernel_preservation_score": 0.40,
        })
        completed = subprocess.run([
            sys.executable, str(CLI),
            "--state", str(state),
            "--proposal", str(proposal),
            "--metrics", str(metrics),
            "--current-tick", "5",
            "--write", str(out),
            "--write-state", str(out_state),
            "--quiet",
        ], cwd=str(ROOT), text=True, capture_output=True, check=False)
        if completed.returncode != 0:
            errors.append(f"cli_returncode:{completed.returncode}")
        if not out.is_file():
            errors.append("output_missing")
        else:
            value = load(out)
            if value.get("adjustment_status") != "QI_PROCESS_TENSOR_AWARE_SCHEDULER_STATE_UPDATED":
                errors.append("adjustment_status_mismatch")
            if value.get("base_revisit_after_ticks") != 3:
                errors.append("base_tick_mismatch")
            if value.get("adjusted_revisit_after_ticks") != 1:
                errors.append("adjusted_tick_mismatch")
            if value.get("process_tensor_pressure_level") != "high_process_tensor_pressure":
                errors.append("pressure_level_mismatch")
            if value.get("authority") != "scheduler_state":
                errors.append("authority_mismatch")
            if value.get("grants_scheduler_authority") is not True:
                errors.append("scheduler_authority_not_true")
            for key in [
                "grants_execution_authority",
                "grants_probe_execution_authority",
                "grants_dry_run_execution_authority",
                "grants_next_tick_execution_authority",
                "grants_control_packet_authority",
                "grants_memory_overwrite_authority",
                "grants_world_update_authority",
                "control_packet_mutation_performed",
                "probe_execution_performed",
                "memory_write_performed",
                "world_update_performed",
            ]:
                if value.get(key) is not False:
                    errors.append(f"{key}_not_false")
        if not out_state.is_file():
            errors.append("state_output_missing")
        else:
            state_value = load(out_state)
            if state_value.get("next_due_tick") != 5:
                errors.append("state_next_due_tick_mismatch")
            if state_value.get("due_status") != "DUE":
                errors.append("state_due_status_mismatch")
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi process tensor aware scheduler state check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
