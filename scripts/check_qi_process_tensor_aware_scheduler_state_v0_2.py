#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "write_qi_process_tensor_aware_scheduler_state_v0_2.py"


def dump(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


STATE = {"current_tick": 4, "last_revisit_tick": 2, "scheduler_status": "QI_SCHEDULER_STATE_UPDATED"}
PROPOSAL = {
    "scheduler_status": "QI_PROBE_SCHEDULER_PROPOSAL_READY",
    "recommended_schedule_mode": "routine_revisit",
    "recommended_revisit_after_ticks": 5,
    "recommended_revisit_reason": "base routine",
    "source_recommended_probe_type": "continue_process_tensor_supervision_probe",
    "schedule_proposal_only": True,
    "authority": "none",
    "grants_execution_authority": False,
    "grants_probe_execution_authority": False,
    "grants_dry_run_execution_authority": False,
    "grants_next_tick_execution_authority": False,
    "grants_control_packet_authority": False,
    "grants_memory_overwrite_authority": False,
    "grants_world_update_authority": False,
}
METRICS = {
    "process_tensor_advantage_level": "moderate",
    "observation_debt_resolution_priority": 0.8,
    "safe_reentry_window_score": 0.5,
    "nonmarkov_link_density": 0.4,
    "memory_kernel_preservation_score": 0.7,
    "history_depth": 5,
}
REUSE = {
    "reuse_status": "QI_PROBE_SCHEDULER_PROPOSAL_REUSE_READY",
    "proposal_reuse_only": True,
    "schedule_proposal_only": True,
    "reused_probe_family": "observation_debt_probe",
    "reused_scheduler_hint": "reuse_nonmarkov_history_for_observation_debt_probe",
    "reused_probe_planner_hint": "prioritize_probe_family_observation_debt_probe",
    "proposed_schedule_mode": "near_term_revisit",
    "proposed_revisit_after_ticks": 1,
    "proposed_revisit_reason": "MemoryOS replay suggests observation debt remains scheduler-relevant",
    "scheduler_state_mutation_performed": False,
    "memory_write_performed": False,
    "world_update_performed": False,
    "control_packet_mutation_performed": False,
    "probe_execution_performed": False,
    "grants_probe_execution_authority": False,
    "grants_world_update_authority": False,
    "grants_memory_write_authority": False,
}


def main() -> int:
    errors: list[str] = []
    if not CLI.is_file():
        errors.append(f"missing:{CLI}")
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        state = root / "state.json"
        proposal = root / "proposal.json"
        metrics = root / "metrics.json"
        reuse = root / "reuse.json"
        out = root / "v02.json"
        dump(state, STATE)
        dump(proposal, PROPOSAL)
        dump(metrics, METRICS)
        dump(reuse, REUSE)
        completed = subprocess.run([
            sys.executable, str(CLI), "--scheduler-state", str(state), "--scheduler-proposal", str(proposal), "--process-tensor-metrics", str(metrics), "--proposal-reuse", str(reuse), "--current-tick", "4", "--write", str(out), "--quiet"
        ], cwd=str(ROOT), text=True, capture_output=True, check=False)
        if completed.returncode != 0:
            errors.append(f"cli_returncode:{completed.returncode}")
            errors.append(completed.stderr.strip() or completed.stdout.strip())
        if not out.is_file():
            errors.append("v02_output_missing")
        else:
            value = load(out)
            if value.get("adjustment_status") != "QI_PROCESS_TENSOR_AWARE_SCHEDULER_STATE_V0_2_UPDATED":
                errors.append("adjustment_status_mismatch")
            if value.get("replay_reuse_integrated") is not True:
                errors.append("replay_reuse_integrated_not_true")
            if value.get("reused_probe_family") != "observation_debt_probe":
                errors.append("reused_probe_family_mismatch")
            if value.get("scheduler_authority_scope") != "scheduler_state_only":
                errors.append("scheduler_authority_scope_mismatch")
            if value.get("scheduler_state_mutation_performed") is not True:
                errors.append("scheduler_state_mutation_not_true")
            for key in ["probe_execution_performed", "memory_write_performed", "world_update_performed", "control_packet_mutation_performed", "grants_probe_execution_authority", "grants_world_update_authority", "grants_memory_overwrite_authority"]:
                if value.get(key) is not False:
                    errors.append(f"{key}_not_false")

        blocked = root / "blocked.json"
        bad_reuse = dict(REUSE)
        bad_reuse["probe_execution_performed"] = True
        dump(reuse, bad_reuse)
        completed = subprocess.run([
            sys.executable, str(CLI), "--scheduler-state", str(state), "--scheduler-proposal", str(proposal), "--process-tensor-metrics", str(metrics), "--proposal-reuse", str(reuse), "--current-tick", "4", "--write", str(blocked), "--quiet"
        ], cwd=str(ROOT), text=True, capture_output=True, check=False)
        if completed.returncode == 0:
            errors.append("blocked_cli_returncode_zero")
        if blocked.is_file():
            value = load(blocked)
            if value.get("adjustment_status") != "QI_PROCESS_TENSOR_AWARE_SCHEDULER_STATE_V0_2_BLOCKED":
                errors.append("blocked_status_mismatch")
            if "reuse_probe_execution_performed_not_false" not in value.get("v02_blockers", []):
                errors.append("probe_execution_blocker_missing")
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi process tensor aware scheduler state v0.2 check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
