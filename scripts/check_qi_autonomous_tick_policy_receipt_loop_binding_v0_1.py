#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
KERNEL_CLI = ROOT / "scripts" / "run_qi_autonomous_tick_policy_kernel_v0_1.py"
LOOP_CLI = ROOT / "scripts" / "run_qi_autonomous_tick_loop_binding_v0_1.py"
ROOT_ID = "qi-root-loop-binding-0001"

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
STATE = {"scheduler_status": "QI_SCHEDULER_STATE_UPDATED", "lineage": ["loop-binding"]}
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


def packet(action: str = "advance_tick", uncertainty: float = 0.1) -> dict:
    return {
        "decision": {"root_id": ROOT_ID, "decision_id": "d1", "decision_action": action, "uncertainty": uncertainty},
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
        "ctx": {
            "current_tick": 7,
            "tick_policy_enabled": True,
            "read_only_policy_surface": True,
            "notify_uncertainty_threshold": 0.45,
            "ticket_uncertainty_threshold": 0.65,
            "handover_uncertainty_threshold": 0.85,
        },
    }


def build_policy(root: pathlib.Path, name: str, data: dict) -> tuple[int, pathlib.Path, pathlib.Path]:
    paths = {}
    for key in ("decision", "cbf", "token", "pt", "ctx"):
        paths[key] = root / f"{name}_{key}.json"
        dump(paths[key], data[key])
    policy_path = root / f"{name}_policy.json"
    done = subprocess.run([
        sys.executable, str(KERNEL_CLI),
        "--decisionos", str(paths["decision"]),
        "--cbf", str(paths["cbf"]),
        "--token-ledger", str(paths["token"]),
        "--process-tensor", str(paths["pt"]),
        "--context", str(paths["ctx"]),
        "--write", str(policy_path),
        "--quiet",
    ], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    return done.returncode, policy_path, paths["pt"]


def run_loop(root: pathlib.Path, name: str, policy_path: pathlib.Path, pt_path: pathlib.Path) -> tuple[int, dict, pathlib.Path]:
    event_log = root / f"{name}_event_log.jsonl"
    ledger = root / f"{name}_ledger_state.json"
    out = root / f"{name}_loop_out.json"
    ctx = root / f"{name}_loop_ctx.json"
    dump(root / f"{name}_memory.json", MEMORY)
    dump(root / f"{name}_state.json", STATE)
    dump(root / f"{name}_proposal.json", PROPOSAL)
    dump(root / f"{name}_metrics.json", METRICS)
    dump(ctx, {
        "loop_binding_enabled": True,
        "jsonl_backend_required": True,
        "read_only_loop_binding": True,
        "tick_id_prefix": f"{name}-loop",
        "memory_complexity_threshold": 1.0,
        "recovery_epsilon": 0.1,
    })
    done = subprocess.run([
        sys.executable, str(LOOP_CLI),
        "--policy", str(policy_path),
        "--process-tensor", str(pt_path),
        "--memory", str(root / f"{name}_memory.json"),
        "--scheduler-state", str(root / f"{name}_state.json"),
        "--scheduler-proposal", str(root / f"{name}_proposal.json"),
        "--process-tensor-metrics", str(root / f"{name}_metrics.json"),
        "--event-log", str(event_log),
        "--ledger-state", str(ledger),
        "--context", str(ctx),
        "--write", str(out),
        "--quiet",
    ], cwd=str(ROOT), text=True, capture_output=True, check=False)
    if done.returncode not in (0, 1):
        print(done.stdout)
        print(done.stderr)
    return done.returncode, load(out), event_log


def main() -> int:
    errors: list[str] = []
    for path in (KERNEL_CLI, LOOP_CLI):
        if not path.is_file():
            errors.append(f"missing:{path}")
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)

        rc, policy_path, pt_path = build_policy(root, "advance", packet())
        lrc, out, event_log = run_loop(root, "advance", policy_path, pt_path)
        if rc != 0 or lrc != 0 or out.get("safe_resume_invoked") is not True:
            errors.append("advance_loop_failed")
        if out.get("jsonl_event_lines_appended") != 1 or len(read_jsonl(event_log)) != 1:
            errors.append("advance_event_line_mismatch")
        if out.get("process_tensor_optimization_mode") not in {"markov_advance", "compressed_recovery_advance"}:
            errors.append("advance_process_tensor_optimization_mismatch")

        low = packet()
        low["token"]["remaining_tokens"] = 0
        rc, policy_path, pt_path = build_policy(root, "hold", low)
        lrc, out, event_log = run_loop(root, "hold", policy_path, pt_path)
        if rc != 0 or lrc != 0 or out.get("daemon_loop_action") != "hold" or out.get("safe_resume_invoked") is not False:
            errors.append("hold_no_invoke_failed")
        if len(read_jsonl(event_log)) != 0:
            errors.append("hold_appended_event")

        obs = packet()
        obs["pt"]["non_markov_unresolved"] = True
        rc, policy_path, pt_path = build_policy(root, "observe", obs)
        lrc, out, event_log = run_loop(root, "observe", policy_path, pt_path)
        if rc != 0 or lrc != 0 or out.get("observe_required") is not True or out.get("safe_resume_invoked") is not False:
            errors.append("observe_no_invoke_failed")

        full = packet()
        full["pt"]["memory_complexity_score"] = 2.0
        full["pt"]["recovery_witness_present"] = False
        rc, policy_path, pt_path = build_policy(root, "full_history", full)
        lrc, out, event_log = run_loop(root, "full_history", policy_path, pt_path)
        if rc != 0 or lrc != 0 or out.get("process_tensor_full_history_required") is not True:
            errors.append("full_history_not_required")
        if out.get("safe_resume_invoked") is not False or len(read_jsonl(event_log)) != 0:
            errors.append("full_history_advanced")

        fr = packet()
        fr["decision"]["freeze_required"] = True
        rc, policy_path, pt_path = build_policy(root, "freeze", fr)
        lrc, out, event_log = run_loop(root, "freeze", policy_path, pt_path)
        if rc != 0 or lrc != 0 or out.get("freeze_required") is not True or out.get("safe_resume_invoked") is not False:
            errors.append("freeze_no_invoke_failed")

        bad = packet()
        bad["pt"]["root_id"] = "other-root"
        rc, policy_path, pt_path = build_policy(root, "blocked", bad)
        lrc, out, event_log = run_loop(root, "blocked", policy_path, pt_path)
        if rc != 1 or lrc != 1 or out.get("loop_binding_status") != "QI_AUTONOMOUS_TICK_LOOP_BINDING_BLOCKED":
            errors.append("blocked_loop_not_blocked")

    if errors:
        for item in errors:
            print("ERROR:", item)
        return 1
    print("PASS: Qi autonomous tick policy receipt loop binding check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
