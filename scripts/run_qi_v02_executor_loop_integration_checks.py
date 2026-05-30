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


GRANT = {
    "gate_status": "QI_LIMITED_ONE_SHOT_EXECUTION_AUTHORITY_GRANT_GATE_READY",
    "grant_outcome": "LIMITED_ONE_SHOT_PROBE_EXECUTION_AUTHORITY_GRANTED",
    "authorized_probe_type": "observation_debt_probe",
    "authority_scope": "single_probe_execution_candidate_review",
    "authority_token_kind": "single_use_probe_execution_authority",
    "grants_probe_execution_authority": True,
    "grants_execution_authority": True,
    "grants_dry_run_execution_authority": False,
    "grants_next_tick_execution_authority": False,
    "grants_scheduler_authority": False,
    "grants_control_packet_authority": False,
    "grants_memory_overwrite_authority": False,
    "grants_world_update_authority": False,
    "one_shot": True,
    "single_probe_only": True,
    "rollback_required": True,
    "reentry_window_bound": True,
    "authority_expires_after_use": True,
    "authority_revocable": True,
    "memory_write_allowed": False,
    "world_update_allowed": False,
    "control_packet_mutation_allowed": False,
    "probe_execution_performed": False,
    "dry_run_execution_performed": False,
    "next_tick_execution_performed": False,
    "scheduler_state_mutation_performed": False,
    "control_packet_mutation_performed": False,
    "memory_write_performed": False,
    "world_update_performed": False
}

PROBE_PAYLOAD = {
    "probe_result_kind": "qi_probe_observation_debt_result",
    "probe_result_summary": "v0.2 one-shot observation debt probe result artifact only",
    "token_already_consumed": False,
    "request_multi_probe": False,
    "request_memory_write": False,
    "request_world_update": False,
    "request_control_packet_mutation": False,
    "request_scheduler_mutation": False
}

WRITEBACK_CONTEXT = {
    "memory_entry_kind": "qi_process_tensor_v02_probe_result_memory_entry",
    "memory_entry_summary": "append v0.2 process tensor probe result to MemoryOS",
    "memoryos_target_stream": "memoryos/qi_process_tensor/v02/append_only",
    "append_only_required": True,
    "lineage_preserved": True,
    "process_tensor_trace_preserved": True,
    "nonmarkov_trace_preserved": True,
    "observation_debt_trace_preserved": True,
    "recoverability_trace_preserved": True,
    "safe_reentry_trace_preserved": True,
    "no_memory_overwrite": True,
    "no_world_update": True,
    "no_control_packet_mutation": True,
    "request_memory_overwrite": False,
    "request_memory_delete": False,
    "request_world_update": False,
    "request_control_packet_mutation": False,
    "request_scheduler_mutation": False
}


def main() -> int:
    errors: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        grant = root / "grant.json"
        payload = root / "payload.json"
        result = root / "result.json"
        writeback_ctx = root / "writeback_ctx.json"
        writeback = root / "writeback.json"
        dump(grant, GRANT)
        dump(payload, PROBE_PAYLOAD)
        dump(writeback_ctx, WRITEBACK_CONTEXT)

        steps = [
            ["scripts/write_qi_one_shot_probe_executor_v0_1.py", "--grant", str(grant), "--probe-payload", str(payload), "--write", str(result), "--quiet"],
            ["scripts/write_qi_memoryos_process_tensor_append_writeback_v0_1.py", "--probe-result", str(result), "--context", str(writeback_ctx), "--write", str(writeback), "--quiet"],
        ]
        for step in steps:
            completed = run(step)
            if completed.returncode != 0:
                errors.append(f"step_failed:{step[0]}:{completed.returncode}")
                errors.append(completed.stdout.strip() or completed.stderr.strip())
                break

        if result.is_file():
            value = load(result)
            if value.get("execution_status") != "QI_ONE_SHOT_PROBE_EXECUTION_PERFORMED":
                errors.append("executor_not_performed")
            if value.get("one_shot_token_consumed") is not True:
                errors.append("token_not_consumed")
            if value.get("token_reuse_allowed") is not False:
                errors.append("token_reuse_not_false")
            if value.get("grants_probe_execution_authority") is not False:
                errors.append("executor_grants_probe_authority_not_false")
            for key in ["memory_write_performed", "world_update_performed", "control_packet_mutation_performed", "scheduler_state_mutation_performed"]:
                if value.get(key) is not False:
                    errors.append(f"executor_{key}_not_false")
        else:
            errors.append("executor_result_missing")

        if writeback.is_file():
            value = load(writeback)
            if value.get("writeback_status") != "QI_MEMORYOS_PROCESS_TENSOR_APPEND_WRITEBACK_PERFORMED":
                errors.append("writeback_not_performed")
            if value.get("memory_append_performed") is not True:
                errors.append("memory_append_not_true")
            if value.get("memory_write_performed") is not True:
                errors.append("memory_write_not_true")
            if value.get("append_only") is not True:
                errors.append("append_only_not_true")
            for key in ["memory_overwrite_performed", "memory_delete_performed", "world_update_performed", "control_packet_mutation_performed", "scheduler_state_mutation_performed", "grants_memory_overwrite_authority", "grants_world_update_authority", "grants_probe_execution_authority"]:
                if value.get(key) is not False:
                    errors.append(f"writeback_{key}_not_false")
        else:
            errors.append("writeback_missing")

        blocked_payload = dict(PROBE_PAYLOAD)
        blocked_payload["token_already_consumed"] = True
        blocked_payload_path = root / "blocked_payload.json"
        blocked_result = root / "blocked_result.json"
        dump(blocked_payload_path, blocked_payload)
        completed = run(["scripts/write_qi_one_shot_probe_executor_v0_1.py", "--grant", str(grant), "--probe-payload", str(blocked_payload_path), "--write", str(blocked_result), "--quiet"])
        if completed.returncode == 0:
            errors.append("reused_token_executor_succeeded")
        if blocked_result.is_file():
            blocked = load(blocked_result)
            if blocked.get("execution_status") != "QI_ONE_SHOT_PROBE_EXECUTION_BLOCKED":
                errors.append("reused_token_not_blocked")
            if "token_already_consumed" not in blocked.get("execution_blockers", []):
                errors.append("reused_token_blocker_missing")
            if blocked.get("probe_execution_performed") is not False:
                errors.append("reused_token_probe_execution_not_false")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi v0.2 executor loop integration checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
