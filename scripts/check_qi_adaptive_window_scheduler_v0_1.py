#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_adaptive_window_scheduler_v0_1.py"
ROOT_ID = "qi-root-adaptive-0001"

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
STATE = {"scheduler_status": "QI_SCHEDULER_STATE_UPDATED", "lineage": ["adaptive-window"]}
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


def ctx(name: str, max_ticks: int = 4, extra: dict | None = None) -> dict:
    value = {
        "adaptive_window_scheduler_enabled": True,
        "read_only_adaptive_scheduler": True,
        "jsonl_backend_required": True,
        "min_window_ticks": 1,
        "max_window_ticks": max_ticks,
        "absolute_max_window_ticks": 16,
        "current_tick": 7,
        "tick_id_prefix": f"{name}-adaptive",
    }
    if extra:
        value.update(extra)
    return value


def run_case(root: pathlib.Path, name: str, packets: dict, metrics: dict, context: dict) -> tuple[int, dict, pathlib.Path]:
    paths = {}
    for key in ("decision", "cbf", "token", "pt"):
        paths[key] = root / f"{name}_{key}.json"
        dump(paths[key], packets[key])
    dump(root / f"{name}_memory.json", MEMORY)
    dump(root / f"{name}_state.json", STATE)
    dump(root / f"{name}_proposal.json", PROPOSAL)
    dump(root / f"{name}_metrics.json", metrics)
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
        rc, out, event_log = run_case(root, "low", packets, BASE_METRICS, ctx("low", 4))
        if rc != 0 or out.get("cadence_mode") != "wide_compressed_window" or out.get("recommended_window_ticks") != 4:
            errors.append("low_pressure_window_failed")
        if out.get("delegated_completed_tick_count") != 4 or len(read_jsonl(event_log)) != 4:
            errors.append("low_pressure_delegation_count_failed")
        if out.get("delegates_only_to_multi_tick_window_governor") is not True:
            errors.append("delegation_invariant_missing")

        packets = base_packets()
        metrics = dict(BASE_METRICS)
        metrics.update({"observation_debt_resolution_priority": 0.7, "safe_reentry_window_score": 0.45})
        rc, out, event_log = run_case(root, "moderate", packets, metrics, ctx("moderate", 4))
        if rc != 0 or out.get("recommended_window_ticks") != 2 or out.get("cadence_mode") != "moderate_guarded_window":
            errors.append("moderate_pressure_window_failed")

        packets = base_packets()
        metrics = dict(BASE_METRICS)
        metrics.update({"observation_debt_resolution_priority": 0.95, "safe_reentry_window_score": 0.1})
        rc, out, event_log = run_case(root, "high", packets, metrics, ctx("high", 4))
        if rc != 0 or out.get("recommended_window_ticks") != 1 or out.get("cadence_mode") not in {"single_tick_high_pressure", "moderate_guarded_window"}:
            errors.append("high_pressure_single_tick_failed")

        packets = base_packets()
        packets["pt"]["non_markov_unresolved"] = True
        rc, out, event_log = run_case(root, "observe", packets, BASE_METRICS, ctx("observe", 4))
        if rc != 0 or out.get("recommended_window_ticks") != 1 or out.get("cadence_mode") != "observe_first_single_tick":
            errors.append("observe_first_failed")
        if out.get("delegated_completed_tick_count") != 0 or out.get("delegated_stop_reason") != "process_tensor_observe_required":
            errors.append("observe_first_stop_failed")

        packets = base_packets()
        packets["pt"]["memory_complexity_score"] = 1.5
        packets["pt"]["recovery_witness_present"] = False
        rc, out, event_log = run_case(root, "full", packets, BASE_METRICS, ctx("full", 4))
        if rc != 0 or out.get("recommended_window_ticks") != 1 or out.get("cadence_mode") != "full_history_single_tick":
            errors.append("full_history_single_tick_failed")

        packets = base_packets()
        packets["token"]["remaining_tokens"] = 1
        rc, out, event_log = run_case(root, "token", packets, BASE_METRICS, ctx("token", 4))
        if rc != 0 or out.get("recommended_window_ticks") != 1:
            errors.append("token_budget_clamp_failed")

        packets = base_packets()
        bad = ctx("blocked", 4)
        bad["adaptive_window_scheduler_enabled"] = False
        rc, out, event_log = run_case(root, "blocked", packets, BASE_METRICS, bad)
        if rc != 1 or out.get("adaptive_scheduler_status") != "QI_ADAPTIVE_WINDOW_SCHEDULER_BLOCKED":
            errors.append("blocked_scheduler_failed")

    if errors:
        for item in errors:
            print("ERROR:", item)
        return 1
    print("PASS: Qi adaptive window scheduler check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
