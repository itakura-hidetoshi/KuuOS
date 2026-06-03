#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_rhythm_memory_cadence_history_layer_v0_1.py"
ROOT_ID = "qi-root-rhythm-0001"

MEMORY = {
    "entries": [
        {
            "writeback_status": "QI_MEMORYOS_PROCESS_TENSOR_APPEND_WRITEBACK_PERFORMED",
            "source_probe_type": "observation_debt_probe",
            "append_only": True,
            "memory_append_performed": True,
            "process_tensor_trace_preserved": True,
            "nonmarkov_trace_preserved": True,
            "observation_debt_trace_preserved": True,
            "recoverability_trace_preserved": True,
            "safe_reentry_trace_preserved": True,
            "lineage_preserved": True,
        }
    ]
}
STATE = {"scheduler_status": "QI_SCHEDULER_STATE_UPDATED", "lineage": ["rhythm-memory"]}
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
BASE_METRICS = {
    "process_tensor_advantage_level": "moderate",
    "observation_debt_resolution_priority": 0.2,
    "safe_reentry_window_score": 0.9,
    "nonmarkov_link_density": 0.9,
    "memory_kernel_preservation_score": 0.95,
    "history_depth": 7,
}


def dump(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def read_jsonl(path: pathlib.Path):
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def base_packets() -> dict:
    return {
        "decision": {"root_id": ROOT_ID, "decision_id": "d1", "decision_action": "advance_tick", "uncertainty": 0.1},
        "cbf": {"root_id": ROOT_ID, "cbf_id": "c1", "cbf_ok": True, "cbf_action": "advance_tick", "barrier_closed": False},
        "token": {"root_id": ROOT_ID, "token_ledger_id": "t1", "token_ledger_ok": True, "token_ledger_action": "advance_tick", "remaining_tokens": 10, "minimum_required_tokens": 1, "current_tick": 7},
        "pt": {
            "root_id": ROOT_ID,
            "process_tensor_id": "p1",
            "process_tensor_ok": True,
            "process_tensor_action": "advance_tick",
            "non_markov_unresolved": False,
            "recovery_witness_missing": False,
            "memory_complexity_score": 0.2,
            "memory_complexity_threshold": 1.0,
            "qcmi_value": 0.01,
            "recovery_epsilon": 0.1,
            "recovery_witness_present": True,
        },
    }


def ctx(name: str, extra: dict | None = None) -> dict:
    value = {
        "rhythm_memory_layer_enabled": True,
        "read_only_rhythm_memory": True,
        "jsonl_backend_required": True,
        "history_window_size": 8,
        "base_min_window_ticks": 1,
        "base_max_window_ticks": 4,
        "absolute_max_window_ticks": 16,
        "current_tick": 7,
        "tick_id_prefix": f"{name}-rhythm",
    }
    if extra:
        value.update(extra)
    return value


def hist(kind: str) -> dict:
    if kind == "stable":
        return {"entries": [
            {"process_tensor_pressure_score": 0.1, "recommended_window_ticks": 4, "delegated_completed_tick_count": 4, "stop_reason": "window_completed", "cadence_mode": "wide_compressed_window"},
            {"process_tensor_pressure_score": 0.15, "recommended_window_ticks": 4, "delegated_completed_tick_count": 4, "stop_reason": "window_completed", "cadence_mode": "wide_compressed_window"},
            {"process_tensor_pressure_score": 0.2, "recommended_window_ticks": 4, "delegated_completed_tick_count": 4, "stop_reason": "window_completed", "cadence_mode": "wide_compressed_window"},
        ]}
    if kind == "observe":
        return {"entries": [
            {"process_tensor_pressure_score": 0.45, "recommended_window_ticks": 2, "delegated_completed_tick_count": 0, "delegated_stop_reason": "process_tensor_observe_required"},
            {"process_tensor_pressure_score": 0.5, "recommended_window_ticks": 2, "delegated_completed_tick_count": 0, "delegated_stop_reason": "process_tensor_observe_required"},
            {"process_tensor_pressure_score": 0.3, "recommended_window_ticks": 2, "delegated_completed_tick_count": 1, "stop_reason": "window_completed"},
        ]}
    if kind == "full":
        return {"entries": [
            {"process_tensor_pressure_score": 0.6, "recommended_window_ticks": 2, "delegated_completed_tick_count": 0, "delegated_stop_reason": "process_tensor_full_history_required"},
            {"process_tensor_pressure_score": 0.65, "recommended_window_ticks": 2, "delegated_completed_tick_count": 0, "delegated_stop_reason": "process_tensor_full_history_required"},
            {"process_tensor_pressure_score": 0.4, "recommended_window_ticks": 2, "delegated_completed_tick_count": 1, "stop_reason": "window_completed"},
        ]}
    if kind == "freeze":
        return {"entries": [
            {"process_tensor_pressure_score": 0.9, "recommended_window_ticks": 1, "delegated_completed_tick_count": 0, "delegated_stop_reason": "freeze_required"},
            {"process_tensor_pressure_score": 0.85, "recommended_window_ticks": 1, "delegated_completed_tick_count": 0, "delegated_stop_reason": "freeze_required"},
            {"process_tensor_pressure_score": 0.2, "recommended_window_ticks": 1, "delegated_completed_tick_count": 1, "stop_reason": "window_completed"},
        ]}
    return {"entries": []}


def run_case(root: pathlib.Path, name: str, packets: dict, history: dict, context: dict) -> tuple[int, dict, pathlib.Path]:
    paths = {}
    for key in ("decision", "cbf", "token", "pt"):
        paths[key] = root / f"{name}_{key}.json"
        dump(paths[key], packets[key])
    dump(root / f"{name}_memory.json", MEMORY)
    dump(root / f"{name}_state.json", STATE)
    dump(root / f"{name}_proposal.json", PROPOSAL)
    dump(root / f"{name}_metrics.json", BASE_METRICS)
    hist_path = root / f"{name}_history.json"
    dump(hist_path, history)
    ctx_path = root / f"{name}_ctx.json"
    dump(ctx_path, context)
    event_log = root / f"{name}_event_log.jsonl"
    ledger = root / f"{name}_ledger_state.json"
    out = root / f"{name}_out.json"
    done = subprocess.run([
        sys.executable, str(CLI),
        "--decisionos", str(paths["decision"]),
        "--cbf", str(paths["cbf"]),
        "--token-ledger", str(paths["token"]),
        "--process-tensor", str(paths["pt"]),
        "--memory", str(root / f"{name}_memory.json"),
        "--scheduler-state", str(root / f"{name}_state.json"),
        "--scheduler-proposal", str(root / f"{name}_proposal.json"),
        "--process-tensor-metrics", str(root / f"{name}_metrics.json"),
        "--rhythm-history", str(hist_path),
        "--event-log", str(event_log),
        "--ledger-state", str(ledger),
        "--context", str(ctx_path),
        "--write", str(out),
        "--quiet",
    ], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    return done.returncode, load(out), event_log


def main() -> int:
    errors: list[str] = []
    if not CLI.is_file():
        errors.append(f"missing:{CLI}")
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        packets = base_packets()

        rc, out, event_log = run_case(root, "stable", packets, hist("stable"), ctx("stable"))
        if rc != 0 or out.get("rhythm_bias") != "expand_if_low_pressure" or out.get("rhythm_mode") != "stable_expansion":
            errors.append("stable_expansion_failed")
        if out.get("recommended_max_window_ticks") < 4 or out.get("rhythm_history_projection_only") is not True:
            errors.append("stable_projection_failed")
        if out.get("memory_append_performed") is not False or out.get("rhythm_entry_candidate", {}).get("memory_append_performed") is not False:
            errors.append("stable_memory_append_boundary_failed")

        rc, out, event_log = run_case(root, "observe", packets, hist("observe"), ctx("observe"))
        if rc != 0 or out.get("rhythm_bias") != "observe_sensitive" or out.get("rhythm_mode") != "observation_guarded":
            errors.append("observe_sensitive_failed")
        if out.get("recommended_max_window_ticks") > 2:
            errors.append("observe_window_not_contracted")

        rc, out, event_log = run_case(root, "full", packets, hist("full"), ctx("full"))
        if rc != 0 or out.get("rhythm_bias") != "full_history_sensitive" or out.get("recommended_max_window_ticks") != 1:
            errors.append("full_history_sensitive_failed")

        rc, out, event_log = run_case(root, "freeze", packets, hist("freeze"), ctx("freeze"))
        if rc != 0 or out.get("rhythm_bias") != "freeze_guarded" or out.get("recommended_max_window_ticks") != 1:
            errors.append("freeze_guarded_failed")

        bad = ctx("blocked")
        bad["rhythm_memory_layer_enabled"] = False
        rc, out, event_log = run_case(root, "blocked", packets, hist("stable"), bad)
        if rc != 1 or out.get("rhythm_layer_status") != "QI_RHYTHM_MEMORY_CADENCE_HISTORY_LAYER_BLOCKED":
            errors.append("blocked_rhythm_layer_failed")

    if errors:
        for item in errors:
            print("ERROR:", item)
        return 1
    print("PASS: Qi rhythm memory cadence history layer check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
