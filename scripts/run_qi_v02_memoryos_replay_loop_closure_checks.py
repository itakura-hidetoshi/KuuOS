#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]


def dump(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def run(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, *args], cwd=str(ROOT), text=True, capture_output=True, check=False)


MEMORY_ENTRY = {
    "writeback_status": "QI_MEMORYOS_PROCESS_TENSOR_APPEND_WRITEBACK_PERFORMED",
    "source_probe_type": "observation_debt_probe",
    "append_only": True,
    "memory_append_performed": True,
    "process_tensor_trace_preserved": True,
    "nonmarkov_trace_preserved": True,
    "observation_debt_trace_preserved": True,
    "recoverability_trace_preserved": True,
    "safe_reentry_trace_preserved": True,
    "lineage_preserved": True
}

REPLAY_CONTEXT = {
    "request_memory_write": False,
    "request_memory_overwrite": False,
    "request_world_update": False,
    "request_scheduler_mutation": False,
    "request_probe_execution": False
}

SCHEDULER_STATE = {
    "scheduler_status": "QI_SCHEDULER_STATE_UPDATED",
    "lineage": ["v02_memoryos_writeback"]
}

APPLY_CONTEXT = {
    "allow_scheduler_state_update": True,
    "scheduler_update_scope": "replay_hint_only",
    "scheduler_lineage_preserved": True,
    "request_probe_execution": False,
    "request_memory_write": False,
    "request_world_update": False,
    "request_control_packet_mutation": False
}

REUSE_CONTEXT = {
    "reuse_scope": "proposal_only",
    "request_scheduler_state_mutation": False,
    "request_probe_execution": False,
    "request_memory_write": False,
    "request_world_update": False,
    "request_control_packet_mutation": False
}

BASE_SCHEDULER_STATE = {
    "current_tick": 9,
    "last_scheduled_tick": 8,
    "scheduler_status": "QI_SCHEDULER_STATE_UPDATED"
}

BASE_PROPOSAL = {
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
    "grants_world_update_authority": False
}

PROCESS_TENSOR_METRICS = {
    "process_tensor_advantage_level": "moderate",
    "observation_debt_resolution_priority": 0.9,
    "safe_reentry_window_score": 0.5,
    "nonmarkov_link_density": 0.6,
    "memory_kernel_preservation_score": 0.8,
    "history_depth": 7
}


def main() -> int:
    errors: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        memory = root / "memory.json"
        replay_ctx = root / "replay_ctx.json"
        replay = root / "replay.json"
        scheduler_state = root / "scheduler_state.json"
        apply_ctx = root / "apply_ctx.json"
        apply = root / "apply.json"
        next_state = root / "next_state.json"
        reuse_ctx = root / "reuse_ctx.json"
        reuse = root / "reuse.json"
        base_state = root / "base_state.json"
        base_proposal = root / "base_proposal.json"
        metrics = root / "metrics.json"
        v02 = root / "v02.json"

        dump(memory, {"entries": [MEMORY_ENTRY]})
        dump(replay_ctx, REPLAY_CONTEXT)
        dump(scheduler_state, SCHEDULER_STATE)
        dump(apply_ctx, APPLY_CONTEXT)
        dump(reuse_ctx, REUSE_CONTEXT)
        dump(base_state, BASE_SCHEDULER_STATE)
        dump(base_proposal, BASE_PROPOSAL)
        dump(metrics, PROCESS_TENSOR_METRICS)

        steps = [
            ["scripts/write_qi_memoryos_process_tensor_retrieval_replay_v0_1.py", "--memory", str(memory), "--context", str(replay_ctx), "--write", str(replay), "--quiet"],
            ["scripts/write_qi_replay_scheduler_state_apply_v0_1.py", "--replay", str(replay), "--scheduler-state", str(scheduler_state), "--context", str(apply_ctx), "--write", str(apply), "--write-state", str(next_state), "--quiet"],
            ["scripts/write_qi_probe_scheduler_proposal_reuse_v0_1.py", "--scheduler-apply", str(apply), "--context", str(reuse_ctx), "--write", str(reuse), "--quiet"],
            ["scripts/write_qi_process_tensor_aware_scheduler_state_v0_2.py", "--scheduler-state", str(base_state), "--scheduler-proposal", str(base_proposal), "--process-tensor-metrics", str(metrics), "--proposal-reuse", str(reuse), "--current-tick", "9", "--write", str(v02), "--quiet"],
        ]
        for step in steps:
            completed = run(step)
            if completed.returncode != 0:
                errors.append(f"step_failed:{step[0]}:{completed.returncode}")
                errors.append(completed.stdout.strip() or completed.stderr.strip())
                break

        if replay.is_file():
            value = load(replay)
            if value.get("replay_status") != "QI_MEMORYOS_PROCESS_TENSOR_RETRIEVAL_REPLAY_READY":
                errors.append("replay_not_ready")
            if value.get("dominant_probe_type") != "observation_debt_probe":
                errors.append("dominant_probe_type_mismatch")
            if value.get("memory_write_performed") is not False:
                errors.append("replay_memory_write_not_false")
        else:
            errors.append("replay_missing")

        if apply.is_file():
            value = load(apply)
            if value.get("apply_status") != "QI_REPLAY_SCHEDULER_STATE_APPLY_PERFORMED":
                errors.append("scheduler_apply_not_performed")
            if value.get("scheduler_state_mutation_performed") is not True:
                errors.append("scheduler_apply_mutation_not_true")
            if value.get("scheduler_update_scope") != "replay_hint_only":
                errors.append("scheduler_apply_scope_mismatch")
            for key in ["memory_write_performed", "world_update_performed", "control_packet_mutation_performed", "probe_execution_performed"]:
                if value.get(key) is not False:
                    errors.append(f"apply_{key}_not_false")
        else:
            errors.append("apply_missing")

        if reuse.is_file():
            value = load(reuse)
            if value.get("reuse_status") != "QI_PROBE_SCHEDULER_PROPOSAL_REUSE_READY":
                errors.append("proposal_reuse_not_ready")
            if value.get("schedule_proposal_only") is not True:
                errors.append("proposal_reuse_not_proposal_only")
            if value.get("reused_probe_family") != "observation_debt_probe":
                errors.append("proposal_reuse_probe_family_mismatch")
        else:
            errors.append("reuse_missing")

        if v02.is_file():
            value = load(v02)
            if value.get("adjustment_status") != "QI_PROCESS_TENSOR_AWARE_SCHEDULER_STATE_V0_2_UPDATED":
                errors.append("v02_not_updated")
            if value.get("replay_reuse_integrated") is not True:
                errors.append("v02_reuse_not_integrated")
            if value.get("reused_probe_family") != "observation_debt_probe":
                errors.append("v02_reused_probe_family_mismatch")
            if value.get("scheduler_state_mutation_performed") is not True:
                errors.append("v02_scheduler_mutation_not_true")
            for key in ["probe_execution_performed", "memory_write_performed", "world_update_performed", "control_packet_mutation_performed", "grants_probe_execution_authority", "grants_world_update_authority"]:
                if value.get(key) is not False:
                    errors.append(f"v02_{key}_not_false")
        else:
            errors.append("v02_missing")

        blocked_replay_ctx = dict(REPLAY_CONTEXT)
        blocked_replay_ctx["request_probe_execution"] = True
        blocked_ctx = root / "blocked_replay_ctx.json"
        blocked_replay = root / "blocked_replay.json"
        dump(blocked_ctx, blocked_replay_ctx)
        completed = run(["scripts/write_qi_memoryos_process_tensor_retrieval_replay_v0_1.py", "--memory", str(memory), "--context", str(blocked_ctx), "--write", str(blocked_replay), "--quiet"])
        if completed.returncode == 0:
            errors.append("blocked_replay_succeeded")
        if blocked_replay.is_file():
            blocked = load(blocked_replay)
            if blocked.get("replay_status") != "QI_MEMORYOS_PROCESS_TENSOR_RETRIEVAL_REPLAY_BLOCKED":
                errors.append("blocked_replay_status_mismatch")
            if "request_probe_execution" not in blocked.get("replay_blockers", []):
                errors.append("blocked_replay_probe_execution_blocker_missing")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi v0.2 MemoryOS replay loop closure checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
