#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "run_qi_advisory_aware_adaptive_scheduler_integration_v0_1.py"
ROOT_ID = "qi-root-advisory-aware-0001"

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
STATE = {"scheduler_status": "QI_SCHEDULER_STATE_UPDATED", "lineage": ["advisory-aware"]}
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


def advisory(max_hint: int, cadence: str = "wide_compressed_window", reason: str = "stable_low_pressure_forecast") -> dict:
    return {
        "bridge_status": "QI_FORECAST_TO_SCHEDULER_ADVISORY_BRIDGE_READY",
        "advisory_packet_id": f"qi-forecast-advisory-{max_hint}",
        "source_forecast_packet_id": "qi-rhythm-forecast-demo",
        "source_ledger_root_digest": "ledger-root-demo",
        "source_last_entry_digest": "last-entry-demo",
        "forecast_window_bias": "expand_if_low_pressure" if max_hint > 1 else "contract_window",
        "forecast_cadence_mode_hint": cadence,
        "forecast_risk_class": "low" if max_hint > 1 else "moderate",
        "forecast_confidence": 1.0,
        "advisory_min_window_ticks_hint": 1,
        "advisory_max_window_ticks_hint": max_hint,
        "advisory_cadence_mode_hint": cadence,
        "advisory_reason": reason,
        "advisory_only": True,
        "scheduler_context_patch_authoritative": False,
        "forecast_directly_sets_window": False,
        "bounded_hint_enforced": True,
        "replaces_forecast_packet": False,
        "replaces_ledger_root": False,
        "memory_write_performed": False,
        "memory_append_performed": False,
        "memory_overwrite_performed": False,
        "world_update_performed": False,
        "control_packet_mutation_performed": False,
        "probe_execution_performed": False,
        "grants_probe_execution_authority": False,
        "grants_world_update_authority": False,
        "grants_memory_overwrite_authority": False,
    }


def ctx(extra: dict | None = None) -> dict:
    value = {
        "advisory_aware_scheduler_enabled": True,
        "advisory_only_required": True,
        "live_scheduler_must_decide": True,
        "base_min_window_ticks": 1,
        "base_max_window_ticks": 4,
        "absolute_max_window_ticks": 16,
        "current_tick": 7,
        "tick_id_prefix": "advisory-aware",
        "allow_advisory_expansion": False,
    }
    if extra:
        value.update(extra)
    return value


def run_case(root: pathlib.Path, name: str, packets: dict, advisory_packet: dict, context: dict, metrics: dict | None = None) -> tuple[int, dict, pathlib.Path]:
    paths = {}
    for key in ("decision", "cbf", "token", "pt"):
        paths[key] = root / f"{name}_{key}.json"
        dump(paths[key], packets[key])
    advisory_path = root / f"{name}_advisory.json"
    dump(advisory_path, advisory_packet)
    dump(root / f"{name}_memory.json", MEMORY)
    dump(root / f"{name}_state.json", STATE)
    dump(root / f"{name}_proposal.json", PROPOSAL)
    dump(root / f"{name}_metrics.json", metrics or BASE_METRICS)
    ctx_path = root / f"{name}_ctx.json"
    dump(ctx_path, context)
    event_log = root / f"{name}_event_log.jsonl"
    ledger = root / f"{name}_ledger_state.json"
    out = root / f"{name}_out.json"
    done = subprocess.run([
        sys.executable, str(CLI),
        "--advisory", str(advisory_path),
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

        rc, out, event_log = run_case(root, "wide", packets, advisory(4), ctx())
        if rc != 0 or out.get("integration_status") != "QI_ADVISORY_AWARE_ADAPTIVE_SCHEDULER_INTEGRATION_COMPLETED":
            errors.append("wide_integration_not_completed")
        if out.get("advisory_applied_as_hint") is not True or out.get("advisory_direct_authority") is not False:
            errors.append("wide_advisory_boundary_failed")
        if out.get("delegated_recommended_window_ticks") != 4 or len(read_jsonl(event_log)) != 4:
            errors.append("wide_delegated_window_failed")
        if out.get("live_scheduler_still_decides") is not True:
            errors.append("live_scheduler_flag_missing")

        rc, out, event_log = run_case(root, "contract", packets, advisory(1, "single_tick_high_pressure", "pressure_contract_forecast"), ctx())
        if rc != 0 or out.get("advisory_max_window_ticks_hint") != 1:
            errors.append("contract_hint_not_applied")
        if out.get("delegated_recommended_window_ticks") != 1 or len(read_jsonl(event_log)) != 1:
            errors.append("contract_delegation_failed")

        high_metrics = dict(BASE_METRICS)
        high_metrics.update({"observation_debt_resolution_priority": 0.95, "safe_reentry_window_score": 0.1})
        rc, out, event_log = run_case(root, "live_high", packets, advisory(4), ctx(), high_metrics)
        if rc != 0 or out.get("delegated_recommended_window_ticks") > 2:
            errors.append("live_scheduler_pressure_not_respected")

        bad = advisory(4)
        bad["forecast_directly_sets_window"] = True
        rc, out, event_log = run_case(root, "bad_advisory", packets, bad, ctx())
        if rc != 1 or out.get("integration_status") != "QI_ADVISORY_AWARE_ADAPTIVE_SCHEDULER_INTEGRATION_BLOCKED":
            errors.append("bad_advisory_not_blocked")

        rc, out, event_log = run_case(root, "direct_request", packets, advisory(4), ctx({"request_direct_window_set": True}))
        if rc != 1 or out.get("integration_status") != "QI_ADVISORY_AWARE_ADAPTIVE_SCHEDULER_INTEGRATION_BLOCKED":
            errors.append("direct_window_request_not_blocked")

    if errors:
        for item in errors:
            print("ERROR:", item)
        return 1
    print("PASS: Qi advisory-aware adaptive scheduler integration check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
