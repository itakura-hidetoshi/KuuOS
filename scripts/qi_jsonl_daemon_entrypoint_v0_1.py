#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import pathlib
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_runtime_daemon_qi_jsonl_safe_resume_controller_v0_1 import run_qi_jsonl_safe_resume_controller


def read_json(path: pathlib.Path | None) -> Any:
    if path is None or not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def require_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def require_entries(value: Any) -> list[dict[str, Any]]:
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    if isinstance(value, dict):
        if isinstance(value.get("entries"), list):
            return [item for item in value["entries"] if isinstance(item, dict)]
        return [value]
    return []


def resolve(base: pathlib.Path, value: str) -> pathlib.Path:
    path = pathlib.Path(value)
    return path if path.is_absolute() else base / path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Qi JSONL daemon deployment entrypoint v0.1")
    parser.add_argument("--config", type=pathlib.Path, required=True)
    parser.add_argument("--write-status", type=pathlib.Path, default=None)
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)

    config = require_dict(read_json(args.config))
    base_dir = resolve(args.config.parent, str(config.get("base_dir", ".")))
    state_dir = resolve(base_dir, str(config.get("state_dir", ".state/qi-jsonl")))
    input_dir = resolve(base_dir, str(config.get("input_dir", ".state/qi-input")))
    state_dir.mkdir(parents=True, exist_ok=True)
    input_dir.mkdir(parents=True, exist_ok=True)

    memory_path = resolve(input_dir, str(config.get("memory_path", "memory.json")))
    scheduler_state_path = resolve(input_dir, str(config.get("scheduler_state_path", "scheduler_state.json")))
    scheduler_proposal_path = resolve(input_dir, str(config.get("scheduler_proposal_path", "scheduler_proposal.json")))
    metrics_path = resolve(input_dir, str(config.get("process_tensor_metrics_path", "process_tensor_metrics.json")))
    event_log_path = resolve(state_dir, str(config.get("event_log_path", "event_log.jsonl")))
    ledger_state_path = resolve(state_dir, str(config.get("ledger_state_path", "ledger_state.json")))

    desired_start_tick = int(config.get("desired_start_tick", 1))
    desired_tick_count = int(config.get("desired_tick_count", 1))
    max_tick_count = int(config.get("max_tick_count", desired_tick_count))
    tick_id_prefix = str(config.get("tick_id_prefix", "deploy"))

    resume_context = {
        "allow_safe_resume": True,
        "jsonl_backend_required": True,
        "skip_processed_ticks": True,
        "max_tick_count": max_tick_count,
        "tick_id_prefix": tick_id_prefix,
        "request_probe_execution": False,
        "request_memory_write": False,
        "request_world_update": False,
        "request_control_packet_mutation": False,
    }
    result = run_qi_jsonl_safe_resume_controller(
        memory_entries=require_entries(read_json(memory_path)),
        scheduler_state=require_dict(read_json(scheduler_state_path)),
        scheduler_proposal=require_dict(read_json(scheduler_proposal_path)),
        process_tensor_metrics=require_dict(read_json(metrics_path)),
        event_log_path=event_log_path,
        ledger_state_path=ledger_state_path,
        desired_start_tick=desired_start_tick,
        desired_tick_count=desired_tick_count,
        resume_context=resume_context,
    )
    payload = result.to_dict()
    status_path = args.write_status or resolve(state_dir, str(config.get("status_path", "daemon_status.json")))
    status_path.parent.mkdir(parents=True, exist_ok=True)
    status_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if not args.quiet:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result.resume_status == "QI_JSONL_SAFE_RESUME_CONTROLLER_COMPLETED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
