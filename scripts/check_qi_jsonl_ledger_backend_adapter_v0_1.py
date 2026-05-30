#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "write_qi_jsonl_ledger_backend_adapter_v0_1.py"


def dump(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: pathlib.Path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


TICK = {
    "daemon_status": "QI_PERSISTENT_PROCESS_TENSOR_DAEMON_TICK_READY",
    "tick_id": "tick-001",
    "heartbeat_emitted": True,
    "closed_loop_tick_performed": True,
    "memory_entry_count": 1,
    "process_tensor_pressure": "high",
    "dominant_probe_type": "observation_debt_probe",
    "scheduler_update_scope": "replay_hint_only",
    "memory_read_performed": True,
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
CTX = {
    "event_id": "evt-001",
    "idempotency_key": "idem-001",
    "append_only_required": True,
    "idempotency_required": True,
    "replay_cursor_required": True,
    "token_ledger_required": True,
    "replay_cursor_stream": "memoryos/qi_process_tensor/append_only",
    "replay_cursor_advance_by": 1,
    "request_memory_overwrite": False,
    "request_world_update": False,
    "request_probe_execution": False,
}
TOKEN = {"token_event_kind": "one_shot_token_consumed", "token_id": "tok-001"}


def main() -> int:
    errors: list[str] = []
    if not CLI.is_file():
        errors.append(f"missing:{CLI}")
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        tick = root / "tick.json"
        ctx = root / "ctx.json"
        token = root / "token.json"
        event_log = root / "event_log.jsonl"
        ledger_state = root / "ledger_state.json"
        out = root / "backend.json"
        dump(tick, TICK)
        dump(ctx, CTX)
        dump(token, TOKEN)
        completed = subprocess.run([
            sys.executable, str(CLI), "--tick", str(tick), "--event-log", str(event_log), "--ledger-state", str(ledger_state), "--context", str(ctx), "--token-event", str(token), "--write", str(out), "--quiet"
        ], cwd=str(ROOT), text=True, capture_output=True, check=False)
        if completed.returncode != 0:
            errors.append(f"cli_returncode:{completed.returncode}")
            errors.append(completed.stdout.strip() or completed.stderr.strip())
        if not out.is_file() or not event_log.is_file() or not ledger_state.is_file():
            errors.append("backend_outputs_missing")
        else:
            value = load(out)
            state = load(ledger_state)
            events = read_jsonl(event_log)
            if value.get("backend_status") != "QI_JSONL_LEDGER_BACKEND_ADAPTER_UPDATED":
                errors.append("backend_status_mismatch")
            if value.get("event_line_appended") is not True:
                errors.append("event_line_appended_not_true")
            if value.get("ledger_state_written") is not True:
                errors.append("ledger_state_written_not_true")
            if len(events) != 1:
                errors.append("event_log_len_mismatch")
            if state.get("replay_cursor", {}).get("position") != 1:
                errors.append("state_cursor_position_mismatch")
            if "tok-001" not in state.get("token_ledger", {}).get("consumed_token_ids", []):
                errors.append("state_token_missing")
            for key in ["memory_write_performed", "memory_append_performed", "memory_overwrite_performed", "world_update_performed", "control_packet_mutation_performed", "probe_execution_performed", "grants_probe_execution_authority"]:
                if value.get(key) is not False:
                    errors.append(f"{key}_not_false")

        blocked_out = root / "blocked.json"
        completed = subprocess.run([
            sys.executable, str(CLI), "--tick", str(tick), "--event-log", str(event_log), "--ledger-state", str(ledger_state), "--context", str(ctx), "--token-event", str(token), "--write", str(blocked_out), "--quiet"
        ], cwd=str(ROOT), text=True, capture_output=True, check=False)
        if completed.returncode == 0:
            errors.append("duplicate_cli_returncode_zero")
        if blocked_out.is_file():
            value = load(blocked_out)
            if value.get("backend_status") != "QI_JSONL_LEDGER_BACKEND_ADAPTER_BLOCKED":
                errors.append("duplicate_backend_status_mismatch")
            blockers = value.get("ledger_update_packet", {}).get("ledger_blockers", [])
            if "idempotency_key_already_seen" not in blockers and "token_already_consumed" not in blockers:
                errors.append("duplicate_blocker_missing")
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi JSONL ledger backend adapter check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
