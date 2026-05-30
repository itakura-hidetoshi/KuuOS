#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "write_qi_persistent_event_log_cursor_ledger_v0_1.py"


def dump(path: pathlib.Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


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

PRIOR = {
    "ledger_version": "qi_persistent_event_log_cursor_ledger_v0_1",
    "event_log": [],
    "replay_cursor": {"stream": "memoryos/qi_process_tensor/append_only", "position": 0},
    "token_ledger": {"consumed_token_ids": []},
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

TOKEN = {
    "token_event_kind": "one_shot_token_consumed",
    "token_id": "tok-001",
}


def main() -> int:
    errors: list[str] = []
    if not CLI.is_file():
        errors.append(f"missing:{CLI}")
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        tick = root / "tick.json"
        prior = root / "prior.json"
        ctx = root / "ctx.json"
        token = root / "token.json"
        out = root / "update.json"
        ledger = root / "ledger.json"
        dump(tick, TICK)
        dump(prior, PRIOR)
        dump(ctx, CTX)
        dump(token, TOKEN)
        completed = subprocess.run([
            sys.executable, str(CLI), "--tick", str(tick), "--prior-ledger", str(prior), "--context", str(ctx), "--token-event", str(token), "--write", str(out), "--write-ledger", str(ledger), "--quiet"
        ], cwd=str(ROOT), text=True, capture_output=True, check=False)
        if completed.returncode != 0:
            errors.append(f"cli_returncode:{completed.returncode}")
            errors.append(completed.stdout.strip() or completed.stderr.strip())
        if not out.is_file() or not ledger.is_file():
            errors.append("ledger_output_missing")
        else:
            value = load(out)
            next_ledger = load(ledger)
            if value.get("ledger_status") != "QI_PERSISTENT_EVENT_LOG_CURSOR_LEDGER_UPDATED":
                errors.append("ledger_status_mismatch")
            if value.get("event_append_performed") is not True:
                errors.append("event_append_not_true")
            if value.get("append_only") is not True:
                errors.append("append_only_not_true")
            if value.get("event_log_size_after") != 1:
                errors.append("event_log_size_after_mismatch")
            if value.get("replay_cursor_after") != 1:
                errors.append("replay_cursor_after_mismatch")
            if value.get("replay_cursor_monotone") is not True:
                errors.append("replay_cursor_monotone_not_true")
            if value.get("token_consumption_recorded") is not True:
                errors.append("token_consumption_not_recorded")
            if "tok-001" not in next_ledger.get("token_ledger", {}).get("consumed_token_ids", []):
                errors.append("token_missing_from_next_ledger")
            for key in ["memory_write_performed", "memory_append_performed", "memory_overwrite_performed", "world_update_performed", "control_packet_mutation_performed", "probe_execution_performed", "grants_probe_execution_authority"]:
                if value.get(key) is not False:
                    errors.append(f"{key}_not_false")

        blocked = root / "blocked.json"
        consumed_prior = dict(PRIOR)
        consumed_prior["token_ledger"] = {"consumed_token_ids": ["tok-001"]}
        dump(prior, consumed_prior)
        completed = subprocess.run([
            sys.executable, str(CLI), "--tick", str(tick), "--prior-ledger", str(prior), "--context", str(ctx), "--token-event", str(token), "--write", str(blocked), "--quiet"
        ], cwd=str(ROOT), text=True, capture_output=True, check=False)
        if completed.returncode == 0:
            errors.append("double_token_cli_returncode_zero")
        if blocked.is_file():
            value = load(blocked)
            if value.get("ledger_status") != "QI_PERSISTENT_EVENT_LOG_CURSOR_LEDGER_BLOCKED":
                errors.append("double_token_status_mismatch")
            if "token_already_consumed" not in value.get("ledger_blockers", []):
                errors.append("token_already_consumed_blocker_missing")
            if value.get("token_double_consume_blocked") is not True:
                errors.append("token_double_consume_not_true")
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Qi persistent event log cursor ledger check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
