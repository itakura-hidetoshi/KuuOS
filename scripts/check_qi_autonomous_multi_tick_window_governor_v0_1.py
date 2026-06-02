#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_autonomous_multi_tick_window_governor_v0_1.py"
ROOT_ID = "qi-root-window-0001"

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
STATE = {"scheduler_status": "QI_SCHEDULER_STATE_UPDATED", "lineage": ["multi-window"]}
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
    "observation_debt_resolution_priority": 0.4,
    "safe_reentry_window_score": 0.7,
    "nonmarkov_link_density": 0.8,
    "memory_kernel_preservation_score": 0.85,
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


def run_case(root: pathlib.Path, name: str, packets: dict, ctx: dict) -> tuple[int, dict, pathlib.Path]:
    paths = {}
    for key in ("decision", "cbf", "token", "pt"):
        paths[key] = root / f"{name}_{key}.json"
        dump(paths[key], packets[key])
    dump(root / f"{name}_memory.json", MEMORY)
    dump(root / f"{name}_state.json", STATE)
    dump(root / f"{name}_proposal.json", PROPOSAL)
    dump(root / f"{name}_metrics.json", METRICS)
    ctx_path = root / f"{name}_ctx.json"
    dump(ctx_path, ctx)
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


def window_ctx(name: str, ticks: int, schedule: list[dict] | None = None) -> dict:
    return {
        "window_governor_enabled": True,
        "read_only_window_governor": True,
        "jsonl_backend_required": True,
        "requested_window_ticks": ticks,
        "max_window_ticks": ticks,
        "absolute_max_window_ticks": 16,
        "current_tick": 7,
        "tick_id_prefix": f"{name}-window",
        "stop_on_observe": True,
        "stop_on_full_history": True,
        "process_tensor_schedule": schedule or [],
    }


def main() -> int:
    errors: list[str] = []
    if not CLI.is_file():
        errors.append(f"missing:{CLI}")
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)

        packets = base_packets()
        rc, out, event_log = run_case(root, "three", packets, window_ctx("three", 3, [
            {"memory_complexity_score": 0.2, "qcmi_value": 0.01, "recovery_witness_present": True},
            {"memory_complexity_score": 0.3, "qcmi_value": 0.02, "recovery_witness_present": True},
            {"memory_complexity_score": 0.4, "qcmi_value": 0.03, "recovery_witness_present": True},
        ]))
        if rc != 0 or out.get("completed_tick_count") != 3 or out.get("stop_reason") != "window_completed":
            errors.append("three_tick_window_failed")
        if out.get("jsonl_event_lines_appended") != 3 or len(read_jsonl(event_log)) != 3:
            errors.append("three_tick_event_count_mismatch")
        if out.get("one_tick_receipt_delegation_enforced") is not True:
            errors.append("one_tick_delegation_not_enforced")

        packets = base_packets()
        rc, out, event_log = run_case(root, "observe", packets, window_ctx("observe", 3, [
            {"memory_complexity_score": 0.2, "qcmi_value": 0.01, "recovery_witness_present": True},
            {"non_markov_unresolved": True},
            {"memory_complexity_score": 0.2},
        ]))
        if rc != 0 or out.get("completed_tick_count") != 1 or out.get("stop_reason") != "process_tensor_observe_required":
            errors.append("observe_stop_failed")
        if len(read_jsonl(event_log)) != 1:
            errors.append("observe_event_count_mismatch")

        packets = base_packets()
        rc, out, event_log = run_case(root, "full", packets, window_ctx("full", 3, [
            {"memory_complexity_score": 0.2, "qcmi_value": 0.01, "recovery_witness_present": True},
            {"memory_complexity_score": 2.0, "recovery_witness_present": False},
        ]))
        if rc != 0 or out.get("completed_tick_count") != 1 or out.get("stop_reason") not in {"process_tensor_full_history_required", "process_tensor_observe_required"}:
            errors.append("full_history_stop_failed")
        if out.get("process_tensor_window_mode") != "full_history_guarded":
            errors.append("full_history_window_mode_mismatch")

        packets = base_packets()
        packets["cbf"]["barrier_closed"] = True
        rc, out, event_log = run_case(root, "freeze", packets, window_ctx("freeze", 3))
        if rc != 0 or out.get("completed_tick_count") != 0 or out.get("stop_reason") != "freeze_required":
            errors.append("freeze_stop_failed")
        if len(read_jsonl(event_log)) != 0:
            errors.append("freeze_appended_event")

        packets = base_packets()
        bad = window_ctx("blocked", 4)
        bad["max_window_ticks"] = 2
        rc, out, event_log = run_case(root, "blocked", packets, bad)
        if rc != 1 or out.get("window_governor_status") != "QI_AUTONOMOUS_MULTI_TICK_WINDOW_GOVERNOR_BLOCKED":
            errors.append("blocked_window_failed")

    if errors:
        for item in errors:
            print("ERROR:", item)
        return 1
    print("PASS: Qi autonomous multi-tick window governor check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
